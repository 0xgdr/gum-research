#!/usr/bin/env python3
"""Analyze whether the root submitter funding event is exceptional within bk1PDA withdrawals."""

from __future__ import annotations

import argparse
import base64
import collections
import datetime as dt
import json
import re
from pathlib import Path

from analyze_root_submitter_history import account_keys
from analyze_root_submitter_history import programs
from analyze_root_update_authority_graph import JUP_MINT
from analyze_root_update_authority_graph import validator_related_keys


ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
GUM_BANK_REQUEST = "bk1PDAkbHEBGtVRiM94Lzets8gVFP7FgySyfkAc8MPN"
KNOWN_WITHDRAW_IMPL = "op16NNe3ZDePmRze6ySKvZzKgT1D2duqSWg9b1rfCnR"
ROOT_SUBMITTER = "6f5muRjigWVnoQHfXWLeXFfafUqMVJfzoBBJL8Gwquji"
WRAPPED_SOL = "So11111111111111111111111111111111111111112"


def b58encode(data: bytes) -> str:
    number = int.from_bytes(data, "big")
    out = ""
    while number:
        number, rem = divmod(number, 58)
        out = ALPHABET[rem] + out
    return ("1" * (len(data) - len(data.lstrip(b"\0")))) + (out or "")


def load(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def block_time(value: int | None) -> str:
    if value is None:
        return "unknown"
    return dt.datetime.fromtimestamp(value, dt.timezone.utc).isoformat()


def manifest_files(base: Path) -> list[str]:
    data = load(base / "solana-mainnet-bank-withdrawal-cohort-manifest.json")
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


def decoded_log_arrays(tx: dict) -> dict[str, dict]:
    rows = {}
    for line in tx.get("meta", {}).get("logMessages") or []:
        match = re.match(r"Program log: ([^\[]+) \[([^\]]+)\]$", line)
        if not match:
            continue
        label = match.group(1).strip()
        try:
            raw = bytes(int(part.strip()) for part in match.group(2).split(",") if part.strip())
        except ValueError:
            continue
        rows[label] = {
            "bytes": raw,
            "len": len(raw),
            "base58": b58encode(raw),
            "hex": raw.hex(),
            "u64_be": int.from_bytes(raw, "big") if len(raw) <= 8 else None,
            "u128_be": int.from_bytes(raw, "big") if len(raw) <= 16 else None,
        }
    return rows


def program_data_lengths(tx: dict) -> list[int]:
    lengths = []
    for line in tx.get("meta", {}).get("logMessages") or []:
        if not line.startswith("Program data: "):
            continue
        try:
            lengths.append(len(base64.b64decode(line.split(": ", 1)[1])))
        except ValueError:
            continue
    return lengths


def parsed_token_mints(tx: dict) -> set[str]:
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


def signers(tx: dict) -> set[str]:
    out = set()
    for key in tx.get("transaction", {}).get("message", {}).get("accountKeys") or []:
        if isinstance(key, dict) and key.get("signer"):
            out.add(key["pubkey"])
    return out


def fee_payer(tx: dict) -> str | None:
    keys = account_keys(tx)
    return keys[0] if keys else None


def event_row(filename: str, tx: dict, source: str) -> dict:
    logs = tx.get("meta", {}).get("logMessages") or []
    decoded = decoded_log_arrays(tx)
    program_set = set(programs(tx))
    keys = set(account_keys(tx))
    recipient = (decoded.get("recipient") or {}).get("base58")
    mint = (decoded.get("mint") or {}).get("base58")
    amount = (decoded.get("amount 0") or {}).get("u128_be")
    impl = (decoded.get("impl program key") or {}).get("base58")
    request = (decoded.get("withdrawal_request_pubkey") or {}).get("base58")
    jupnet = (decoded.get("jupnet") or {}).get("base58")
    return {
        "source": source,
        "filename": filename,
        "signature": (tx.get("transaction", {}).get("signatures") or [""])[0],
        "slot": tx.get("slot"),
        "time": block_time(tx.get("blockTime")),
        "fee_payer": fee_payer(tx),
        "signers": signers(tx),
        "programs": program_set,
        "keys": keys,
        "is_request": any("Instruction: Request" in line for line in logs),
        "is_withdraw": any("Instruction: Withdraw" in line for line in logs),
        "has_signature_verified": any("Signature verified" in line for line in logs),
        "has_jupnet_log": "jupnet" in decoded,
        "recipient": recipient,
        "mint": mint,
        "amount": amount,
        "impl": impl,
        "withdrawal_request": request,
        "jupnet": jupnet,
        "program_data_lengths": program_data_lengths(tx),
        "parsed_mints": parsed_token_mints(tx),
    }


def cohort_rows(base: Path) -> list[dict]:
    rows = []
    for filename in manifest_files(base):
        tx = tx_result(base, filename)
        if tx:
            rows.append(event_row(filename, tx, "cohort"))
    funding_manifest = load(base / "solana-mainnet-root-submitter-funding-history-manifest.json")
    for submitter in funding_manifest.get("submitters") or []:
        for filename in submitter.get("positive_delta_files") or []:
            tx = tx_result(base, filename)
            if tx:
                rows.append(event_row(filename, tx, "root_submitter_setup"))
    return rows


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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot_dir")
    args = parser.parse_args()
    base = Path(args.snapshot_dir)

    rows = cohort_rows(base)
    cohort = [row for row in rows if row["source"] == "cohort"]
    setup = [row for row in rows if row["source"] == "root_submitter_setup"]
    validators = set(validator_related_keys(base))

    request_withdraw = [row for row in cohort if row["is_request"] and row["is_withdraw"]]
    decoded_withdraw = [row for row in rows if row["recipient"] or row["impl"] or row["withdrawal_request"]]
    recipient_counter = collections.Counter(row["recipient"] for row in decoded_withdraw if row["recipient"])
    mint_counter = collections.Counter(row["mint"] or mint for row in decoded_withdraw for mint in ([row["mint"]] if row["mint"] else row["parsed_mints"]))
    impl_counter = collections.Counter(row["impl"] for row in decoded_withdraw if row["impl"])
    fee_payer_counter = collections.Counter(row["fee_payer"] for row in rows if row["fee_payer"])
    signer_counter = collections.Counter(signer for row in rows for signer in row["signers"])
    security_hits = {
        key
        for row in rows
        for key in (row["keys"] & validators) | ({JUP_MINT} if JUP_MINT in row["keys"] else set())
    }

    print("# Bank Withdrawal Cohort")
    print()
    print("## Scope")
    print()
    print(f"- Snapshot: `{base}`")
    print(f"- Target program/address: `{GUM_BANK_REQUEST}`")
    print(f"- Cohort transaction bodies analyzed: `{len(cohort)}`")
    print(f"- Root-submitter setup comparison events: `{len(setup)}`")
    print()

    if not rows:
        print("## Assessment")
        print()
        print("- No cohort transactions were available. Run `scripts/collect_bank_withdrawal_cohort.py` first.")
        return

    print("## Cohort Summary")
    print()
    print(f"- Cohort transactions with both `Instruction: Request` and `Instruction: Withdraw`: `{len(request_withdraw)}`")
    print(f"- Decoded withdrawal-like rows including setup comparison: `{len(decoded_withdraw)}`")
    print(f"- Unique decoded recipients: `{len(recipient_counter)}`")
    print(f"- Root submitter recipient hits: `{recipient_counter.get(ROOT_SUBMITTER, 0)}`")
    print(f"- Canonical JUP / current validator / vote / stake intersections: `{len(security_hits)}`")
    print()
    print("### Distributions")
    print()
    print("| Group | Values |")
    print("|---|---|")
    print(f"| Recipients | {fmt_counter(recipient_counter, limit=20)} |")
    print(f"| Mints | {fmt_counter(mint_counter, limit=20)} |")
    print(f"| Implementation programs | {fmt_counter(impl_counter, limit=20)} |")
    print(f"| Fee payers | {fmt_counter(fee_payer_counter, limit=20)} |")
    print(f"| Signers | {fmt_counter(signer_counter, limit=20)} |")
    print()

    print("## Transaction Rows")
    print()
    print("| Source | File | Time | Request | Withdraw | Recipient | Mint | Amount | Impl | Fee payer | Signers | Signature verified |")
    print("|---|---|---|---|---|---|---|---:|---|---|---|---|")
    for row in sorted(rows, key=lambda item: (item["source"], item["slot"] or 0, item["filename"])):
        print(
            f"| `{row['source']}` | `{row['filename']}` | `{row['time']}` | `{row['is_request']}` | "
            f"`{row['is_withdraw']}` | `{row['recipient'] or 'None'}` | `{row['mint'] or ', '.join(sorted(row['parsed_mints'])) or 'None'}` | "
            f"{row['amount'] if row['amount'] is not None else ''} | `{row['impl'] or 'None'}` | "
            f"`{row['fee_payer']}` | {fmt(row['signers'])} | `{row['has_signature_verified']}` |"
        )
    print()

    print("## Comparison Assessment")
    print()
    if recipient_counter.get(ROOT_SUBMITTER, 0) == 1 and len(recipient_counter) > 1:
        print("- The root submitter appears as one decoded recipient among multiple recipients, not as the only withdrawal recipient in the compared set.")
    elif recipient_counter.get(ROOT_SUBMITTER, 0) == 1:
        print("- The root submitter is the only decoded recipient in the current compared set; the cohort needs more decoded withdrawals before routine-vs-special can be decided.")
    else:
        print("- The root submitter did not appear as a decoded recipient in the fetched cohort; it only appears in the setup comparison event.")
    if impl_counter.get(KNOWN_WITHDRAW_IMPL, 0) > 1:
        print("- `op16...` is reused across withdrawal-like rows, so the root-submitter setup did not use a one-off implementation program.")
    else:
        print("- `op16...` only appears in the setup comparison row in this local cohort.")
    if security_hits:
        print(f"- Watched security intersections appeared: {fmt(security_hits)}")
    else:
        print("- No canonical JUP/current validator/vote/stake keys appeared in the cohort or setup comparison rows.")
    print("- The next useful expansion is to increase the `bk1PDA...` transaction window and, if needed, add a second cohort for `BankK...` withdraw rows so the two Solana-side withdrawal paths can be compared directly.")


if __name__ == "__main__":
    main()
