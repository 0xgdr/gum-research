#!/usr/bin/env python3
"""Compare bk1PDA and BankK Solana-side withdrawal surfaces."""

from __future__ import annotations

import argparse
import collections
import datetime as dt
import json
import re
from pathlib import Path

from analyze_bank_withdrawal_cohort import decoded_log_arrays
from analyze_root_submitter_history import account_keys
from analyze_root_submitter_history import programs
from analyze_root_update_authority_graph import JUP_MINT
from analyze_root_update_authority_graph import validator_related_keys


BK1PDA = "bk1PDAkbHEBGtVRiM94Lzets8gVFP7FgySyfkAc8MPN"
BANKK = "BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ"
ROOT_SUBMITTER = "6f5muRjigWVnoQHfXWLeXFfafUqMVJfzoBBJL8Gwquji"
KNOWN_IMPL = "op16NNe3ZDePmRze6ySKvZzKgT1D2duqSWg9b1rfCnR"
JUPW3 = "JUPW3tHBxmNRzVnLmTyYUsUDB6izZSEtupY6znBC5mo"
INBOX_HELPER = "JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw"
OUTBOX_HELPER = "jnoUtncGR9ZCCMixtys6Gzy5coTo6mnmUZuEHRQFTFV"
WRAPPED_SOL = "So11111111111111111111111111111111111111112"
USDC = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"


def load(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def block_time(value: int | None) -> str:
    if value is None:
        return "unknown"
    return dt.datetime.fromtimestamp(value, dt.timezone.utc).isoformat()


def manifest_files(base: Path, prefix: str) -> list[str]:
    data = load(base / f"solana-mainnet-{prefix}-manifest.json")
    return data.get("transaction_files") or []


def tx_result(base: Path, filename: str) -> dict | None:
    result = load(base / filename).get("result")
    if isinstance(result, dict) and "transaction" in result:
        return result
    return None


def all_instructions(tx: dict) -> list[dict]:
    rows = list(tx.get("transaction", {}).get("message", {}).get("instructions") or [])
    for group in tx.get("meta", {}).get("innerInstructions") or []:
        rows.extend(group.get("instructions") or [])
    return rows


def signers(tx: dict) -> set[str]:
    out = set()
    for key in tx.get("transaction", {}).get("message", {}).get("accountKeys") or []:
        if isinstance(key, dict) and key.get("signer"):
            out.add(key["pubkey"])
    return out


def fee_payer(tx: dict) -> str | None:
    keys = account_keys(tx)
    return keys[0] if keys else None


def instruction_names(logs: list[str]) -> list[str]:
    names = []
    for line in logs:
        match = re.search(r"Instruction: ([A-Za-z0-9_]+)", line)
        if match:
            names.append(match.group(1))
    return names


def token_flow(tx: dict) -> list[str]:
    rows = []
    for ix in all_instructions(tx):
        parsed = ix.get("parsed")
        if not isinstance(parsed, dict):
            continue
        if parsed.get("type") not in {"transfer", "transferChecked"}:
            continue
        info = parsed.get("info") or {}
        mint = info.get("mint")
        amount = info.get("amount") or (info.get("tokenAmount") or {}).get("amount")
        source = info.get("source")
        destination = info.get("destination")
        authority = info.get("authority")
        rows.append(f"{mint or 'SOL'} {amount} {source}->{destination} auth={authority}")
    return rows


def parsed_mints(tx: dict) -> set[str]:
    mints = set()
    for ix in all_instructions(tx):
        parsed = ix.get("parsed")
        if not isinstance(parsed, dict):
            continue
        info = parsed.get("info") or {}
        if isinstance(info.get("mint"), str):
            mints.add(info["mint"])
        amount = info.get("tokenAmount")
        if isinstance(amount, dict) and isinstance(amount.get("mint"), str):
            mints.add(amount["mint"])
    for key in ("preTokenBalances", "postTokenBalances"):
        for balance in tx.get("meta", {}).get(key) or []:
            if balance.get("mint"):
                mints.add(balance["mint"])
    return mints


def decoded_fields(tx: dict) -> dict[str, str | int | None]:
    decoded = decoded_log_arrays(tx)
    return {
        "recipient": (decoded.get("recipient") or {}).get("base58"),
        "mint": (decoded.get("mint") or {}).get("base58"),
        "amount": (decoded.get("amount 0") or {}).get("u128_be"),
        "impl": (decoded.get("impl program key") or {}).get("base58"),
        "withdrawal_request": (decoded.get("withdrawal_request_pubkey") or {}).get("base58"),
        "jupnet": (decoded.get("jupnet") or {}).get("base58"),
    }


def row_for(surface: str, filename: str, tx: dict) -> dict:
    logs = tx.get("meta", {}).get("logMessages") or []
    fields = decoded_fields(tx)
    program_set = set(programs(tx))
    return {
        "surface": surface,
        "filename": filename,
        "slot": tx.get("slot"),
        "time": block_time(tx.get("blockTime")),
        "fee_payer": fee_payer(tx),
        "signers": signers(tx),
        "instructions": instruction_names(logs),
        "programs": program_set,
        "keys": set(account_keys(tx)),
        "mints": parsed_mints(tx),
        "token_flows": token_flow(tx),
        "recipient": fields["recipient"],
        "decoded_mint": fields["mint"],
        "decoded_amount": fields["amount"],
        "impl": fields["impl"],
        "withdrawal_request": fields["withdrawal_request"],
        "jupnet": fields["jupnet"],
        "submit_inbox": any("SubmitInboxMessage" in line for line in logs),
        "verify_outbox": any("VerifyOutboxMessage" in line or "Outbox verification passed" in line for line in logs),
        "signature_verified": any("Signature verified" in line for line in logs),
    }


def rows(base: Path) -> list[dict]:
    out = []
    for filename in manifest_files(base, "bank-withdrawal-cohort"):
        tx = tx_result(base, filename)
        if tx:
            out.append(row_for("bk1PDA", filename, tx))
    for filename in manifest_files(base, "bank-program-withdrawal-cohort"):
        tx = tx_result(base, filename)
        if tx:
            out.append(row_for("BankK", filename, tx))
    funding_manifest = load(base / "solana-mainnet-root-submitter-funding-history-manifest.json")
    for submitter in funding_manifest.get("submitters") or []:
        for filename in submitter.get("positive_delta_files") or []:
            tx = tx_result(base, filename)
            if tx:
                out.append(row_for("root_submitter_setup", filename, tx))
    return out


def fmt(values, empty: str = "`None`", limit: int | None = None) -> str:
    items = sorted(values) if isinstance(values, set) else list(values)
    items = [str(item) for item in items if item]
    if limit is not None:
        items = items[:limit]
    if not items:
        return empty
    return "<br>".join(f"`{item}`" for item in items)


def fmt_counter(counter: collections.Counter, limit: int | None = None) -> str:
    return fmt([f"{key}: {value}" for key, value in counter.most_common(limit)])


def surface_summary(rows_for_surface: list[dict]) -> dict:
    return {
        "txs": len(rows_for_surface),
        "withdraw": sum("Withdraw" in row["instructions"] for row in rows_for_surface),
        "request": sum("Request" in row["instructions"] for row in rows_for_surface),
        "verify_request": sum("VerifyRequest" in row["instructions"] for row in rows_for_surface),
        "submit_inbox": sum(row["submit_inbox"] for row in rows_for_surface),
        "verify_outbox": sum(row["verify_outbox"] for row in rows_for_surface),
        "signature_verified": sum(row["signature_verified"] for row in rows_for_surface),
        "decoded_recipients": {row["recipient"] for row in rows_for_surface if row["recipient"]},
        "decoded_impls": {row["impl"] for row in rows_for_surface if row["impl"]},
        "fee_payers": collections.Counter(row["fee_payer"] for row in rows_for_surface if row["fee_payer"]),
        "signers": collections.Counter(signer for row in rows_for_surface for signer in row["signers"]),
        "instructions": collections.Counter(name for row in rows_for_surface for name in row["instructions"]),
        "mints": collections.Counter(mint for row in rows_for_surface for mint in (({row["decoded_mint"]} if row["decoded_mint"] else set()) | row["mints"])),
        "programs": collections.Counter(program for row in rows_for_surface for program in row["programs"]),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot_dir")
    args = parser.parse_args()
    base = Path(args.snapshot_dir)
    all_rows = rows(base)
    related = set(validator_related_keys(base))
    security_hits = {
        key for row in all_rows for key in (row["keys"] & related) | ({JUP_MINT} if JUP_MINT in row["keys"] else set())
    }

    print("# Withdrawal Surface Comparison")
    print()
    print("## Scope")
    print()
    print(f"- Snapshot: `{base}`")
    print(f"- `bk1PDA...` surface: `{BK1PDA}`")
    print(f"- `BankK...` surface: `{BANKK}`")
    print(f"- Root submitter setup comparison recipient: `{ROOT_SUBMITTER}`")
    print(f"- Transactions compared: `{len(all_rows)}`")
    print()

    if not all_rows:
        print("## Assessment")
        print()
        print("- No withdrawal-surface rows were available. Run both cohort collectors first.")
        return

    print("## Surface Summary")
    print()
    print("| Surface | Txs | Withdraw | Request | VerifyRequest | SubmitInbox | VerifyOutbox | Signature verified | Decoded recipients | Decoded impls |")
    print("|---|---:|---:|---:|---:|---:|---:|---:|---|---|")
    summaries = {}
    for surface in ("bk1PDA", "BankK", "root_submitter_setup"):
        summary = surface_summary([row for row in all_rows if row["surface"] == surface])
        summaries[surface] = summary
        print(
            f"| `{surface}` | {summary['txs']} | {summary['withdraw']} | {summary['request']} | "
            f"{summary['verify_request']} | {summary['submit_inbox']} | {summary['verify_outbox']} | "
            f"{summary['signature_verified']} | {fmt(summary['decoded_recipients'], limit=8)} | {fmt(summary['decoded_impls'])} |"
        )
    print()

    print("## Cross-Surface Distributions")
    print()
    print("| Surface | Fee payers | Signers | Instructions | Mints | Helper / high-value programs |")
    print("|---|---|---|---|---|---|")
    high_value = {BK1PDA, BANKK, KNOWN_IMPL, INBOX_HELPER, OUTBOX_HELPER}
    for surface, summary in summaries.items():
        helper_programs = {f"{program}: {count}" for program, count in summary["programs"].items() if program in high_value}
        print(
            f"| `{surface}` | {fmt_counter(summary['fee_payers'], limit=8)} | "
            f"{fmt_counter(summary['signers'], limit=8)} | {fmt_counter(summary['instructions'], limit=12)} | "
            f"{fmt_counter(summary['mints'], limit=8)} | {fmt(helper_programs)} |"
        )
    print()

    print("## Representative Rows")
    print()
    print("| Surface | File | Time | Instructions | Recipient | Mints | Impl | Fee payer | Signers | Token flows |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    representative = []
    for surface in ("bk1PDA", "BankK", "root_submitter_setup"):
        candidates = [row for row in all_rows if row["surface"] == surface and ("Withdraw" in row["instructions"] or row["recipient"])]
        representative.extend(candidates[:8])
    for row in representative:
        mints = ({row["decoded_mint"]} if row["decoded_mint"] else set()) | row["mints"]
        print(
            f"| `{row['surface']}` | `{row['filename']}` | `{row['time']}` | {fmt(row['instructions'], limit=6)} | "
            f"`{row['recipient'] or 'None'}` | {fmt(mints, limit=6)} | `{row['impl'] or 'None'}` | "
            f"`{row['fee_payer']}` | {fmt(row['signers'])} | {fmt(row['token_flows'], limit=3)} |"
        )
    print()

    print("## Assessment")
    print()
    if summaries["bk1PDA"]["decoded_impls"] == {KNOWN_IMPL} and KNOWN_IMPL in summaries["root_submitter_setup"]["decoded_impls"]:
        print("- The root submitter setup and decoded `bk1PDA...` withdrawals share the same `op16...` implementation program.")
    if INBOX_HELPER in summaries["BankK"]["programs"]:
        print("- `BankK...` withdraw/sweep/RFQ rows invoke the inbox helper `JNiN...`, which is not the direct decoded shape of the `bk1PDA... -> op16...` rows.")
    if OUTBOX_HELPER in summaries["BankK"]["programs"]:
        print("- `BankK...` VerifyRequest rows invoke the outbox helper `jnoUtn...`, reinforcing that `BankK...` handles the public inbox/outbox layer.")
    if summaries["bk1PDA"]["fee_payers"].get(JUPW3, 0) and summaries["BankK"]["fee_payers"].get(JUPW3, 0):
        print("- `JUPW3...` signs/pays both surfaces in the sampled windows, strengthening its operational signer/fee-payer role.")
    if summaries["BankK"]["fee_payers"] and summaries["BankK"]["fee_payers"].get(JUPW3, 0) != summaries["BankK"]["txs"]:
        print("- `BankK...` also has a second sampled signer/fee payer, so `JUPW3...` is not the only observed signer on that surface.")
    if security_hits:
        print(f"- Watched canonical JUP / validator / vote / stake intersections appeared: {fmt(security_hits)}")
    else:
        print("- No canonical JUP/current validator/vote/stake key intersections appeared across the compared surfaces.")
    print("- The evidence supports two connected Solana-side withdrawal surfaces: `bk1PDA...` exposes the request/implementation withdrawal payload shape, while `BankK...` exposes inbox/outbox message handling around withdrawals and related operations.")
    print("- This improves the operational map but still does not expose Dove/JUP stake-weight or validator-security producer state.")


if __name__ == "__main__":
    main()
