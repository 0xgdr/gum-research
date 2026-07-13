#!/usr/bin/env python3
"""Correlate bk1PDA withdrawal requests with BankK inbox/outbox rows."""

from __future__ import annotations

import argparse
import base64
import collections
import datetime as dt
import json
import re
from pathlib import Path

from analyze_bank_account_graph import b58decode
from analyze_bank_withdrawal_cohort import decoded_log_arrays
from analyze_root_submitter_history import account_keys
from analyze_root_submitter_history import programs
from analyze_root_update_authority_graph import JUP_MINT
from analyze_root_update_authority_graph import validator_related_keys


BK1PDA = "bk1PDAkbHEBGtVRiM94Lzets8gVFP7FgySyfkAc8MPN"
BANKK = "BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ"
KNOWN_IMPL = "op16NNe3ZDePmRze6ySKvZzKgT1D2duqSWg9b1rfCnR"
JUPW3 = "JUPW3tHBxmNRzVnLmTyYUsUDB6izZSEtupY6znBC5mo"
INBOX_HELPER = "JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw"
OUTBOX_HELPER = "jnoUtncGR9ZCCMixtys6Gzy5coTo6mnmUZuEHRQFTFV"


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
    if isinstance(result, dict) and isinstance(result.get("transaction"), dict):
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


def raw_blobs(tx: dict) -> list[dict]:
    blobs = []
    for ix in all_instructions(tx):
        data = ix.get("data")
        if isinstance(data, str):
            try:
                raw = b58decode(data)
            except ValueError:
                raw = b""
            if raw:
                blobs.append(
                    {
                        "kind": "instruction-data",
                        "program": ix.get("programId"),
                        "len": len(raw),
                        "raw": raw,
                    }
                )
    for line in tx.get("meta", {}).get("logMessages") or []:
        if line.startswith("Program data: "):
            try:
                raw = base64.b64decode(line.split(": ", 1)[1])
            except ValueError:
                continue
            blobs.append({"kind": "program-data-log", "program": None, "len": len(raw), "raw": raw})
        elif line.startswith("Program return: "):
            parts = line.split()
            if len(parts) >= 4:
                try:
                    raw = base64.b64decode(parts[-1])
                except ValueError:
                    continue
                blobs.append({"kind": "program-return", "program": parts[2], "len": len(raw), "raw": raw})
    return blobs


def parsed_token_transfers(tx: dict) -> list[dict]:
    rows = []
    for ix in all_instructions(tx):
        parsed = ix.get("parsed")
        if not isinstance(parsed, dict):
            continue
        info = parsed.get("info") or {}
        if parsed.get("type") == "transferChecked":
            amount = (info.get("tokenAmount") or {}).get("amount")
            rows.append(
                {
                    "kind": "token",
                    "mint": info.get("mint"),
                    "amount": int(amount) if isinstance(amount, str) and amount.isdigit() else None,
                    "source": info.get("source"),
                    "destination": info.get("destination"),
                    "authority": info.get("authority"),
                }
            )
        elif parsed.get("type") == "transfer":
            lamports = info.get("lamports")
            rows.append(
                {
                    "kind": "sol",
                    "mint": "SOL",
                    "amount": int(lamports) if isinstance(lamports, int) else None,
                    "source": info.get("source"),
                    "destination": info.get("destination"),
                    "authority": None,
                }
            )
    return rows


def created_accounts(tx: dict) -> list[dict]:
    rows = []
    for ix in all_instructions(tx):
        parsed = ix.get("parsed")
        if not isinstance(parsed, dict) or parsed.get("type") != "createAccount":
            continue
        info = parsed.get("info") or {}
        rows.append(
            {
                "account": info.get("newAccount"),
                "owner": info.get("owner"),
                "source": info.get("source"),
                "space": info.get("space"),
                "lamports": info.get("lamports"),
            }
        )
    return rows


def decoded_fields(tx: dict) -> dict[str, dict]:
    decoded = decoded_log_arrays(tx)
    fields = {}
    for label in (
        "withdrawal_request_pubkey",
        "mint",
        "amount 0",
        "amount 1",
        "recipient",
        "jupnet",
        "impl program key",
        "message_hash",
        "valid_till",
    ):
        item = decoded.get(label)
        if item:
            fields[label] = item
    return fields


def row_for(surface: str, filename: str, tx: dict) -> dict:
    logs = tx.get("meta", {}).get("logMessages") or []
    fields = decoded_fields(tx)
    keys = set(account_keys(tx))
    return {
        "surface": surface,
        "filename": filename,
        "signature": (tx.get("transaction", {}).get("signatures") or [""])[0],
        "slot": tx.get("slot"),
        "time": block_time(tx.get("blockTime")),
        "fee_payer": fee_payer(tx),
        "signers": signers(tx),
        "instructions": instruction_names(logs),
        "programs": set(programs(tx)),
        "keys": keys,
        "fields": fields,
        "raw_blobs": raw_blobs(tx),
        "token_transfers": parsed_token_transfers(tx),
        "created_accounts": created_accounts(tx),
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


def raw_hit_locations(needle: bytes, target: dict) -> list[str]:
    hits = []
    if not needle:
        return hits
    for blob in target["raw_blobs"]:
        offset = blob["raw"].find(needle)
        while offset != -1:
            hits.append(f"{blob['kind']}:{blob['program'] or 'unknown'}:{blob['len']}@{offset}")
            offset = blob["raw"].find(needle, offset + 1)
    return hits


def exact_field_matches(source_rows: list[dict], target_rows: list[dict], labels: set[str] | None = None) -> list[dict]:
    matches = []
    for source in source_rows:
        for label, field in source["fields"].items():
            if labels is not None and label not in labels:
                continue
            raw = field.get("bytes") or b""
            base58_value = field.get("base58")
            if not raw:
                continue
            for target in target_rows:
                key_hit = base58_value in target["keys"] if isinstance(base58_value, str) else False
                raw_hits = raw_hit_locations(raw, target)
                if key_hit or raw_hits:
                    matches.append(
                        {
                            "source": source,
                            "target": target,
                            "label": label,
                            "value": base58_value or field.get("hex"),
                            "key_hit": key_hit,
                            "raw_hits": raw_hits,
                        }
                    )
    return matches


def token_near_matches(source_rows: list[dict], target_rows: list[dict]) -> list[dict]:
    matches = []
    for source in source_rows:
        source_mint = (source["fields"].get("mint") or {}).get("base58")
        source_amount = (source["fields"].get("amount 0") or {}).get("u128_be")
        source_recipient = (source["fields"].get("recipient") or {}).get("base58")
        if not source_mint or source_amount is None:
            continue
        for target in target_rows:
            for transfer in target["token_transfers"]:
                if transfer["kind"] != "token":
                    continue
                reasons = []
                if transfer["mint"] == source_mint:
                    reasons.append("mint")
                if transfer["amount"] == source_amount:
                    reasons.append("amount")
                if source_recipient and source_recipient in {transfer["source"], transfer["destination"], transfer["authority"]}:
                    reasons.append("recipient-account")
                if len(reasons) >= 2 or ("amount" in reasons and "recipient-account" in reasons):
                    matches.append(
                        {
                            "source": source,
                            "target": target,
                            "reasons": reasons,
                            "mint": transfer["mint"],
                            "amount": transfer["amount"],
                            "source_account": transfer["source"],
                            "destination": transfer["destination"],
                            "authority": transfer["authority"],
                        }
                    )
    return matches


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


def surface_summary(surface_rows: list[dict]) -> dict:
    return {
        "txs": len(surface_rows),
        "decoded_message_hashes": sum("message_hash" in row["fields"] for row in surface_rows),
        "decoded_requests": sum("withdrawal_request_pubkey" in row["fields"] for row in surface_rows),
        "submit_inbox": sum(row["submit_inbox"] for row in surface_rows),
        "verify_outbox": sum(row["verify_outbox"] for row in surface_rows),
        "signature_verified": sum(row["signature_verified"] for row in surface_rows),
        "created_account_spaces": collections.Counter(
            f"{item['owner']} space={item['space']}"
            for row in surface_rows
            for item in row["created_accounts"]
            if item.get("owner") and item.get("space") is not None
        ),
        "fee_payers": collections.Counter(row["fee_payer"] for row in surface_rows if row["fee_payer"]),
        "signers": collections.Counter(signer for row in surface_rows for signer in row["signers"]),
    }


def print_match_rows(matches: list[dict], title: str, limit: int = 20) -> None:
    print(f"## {title}")
    print()
    if not matches:
        print("- None")
        print()
        return
    print("| Source | Target | Field / reason | Value / transfer | Hit location |")
    print("|---|---|---|---|---|")
    for match in matches[:limit]:
        if "label" in match:
            locations = set(match["raw_hits"])
            if match["key_hit"]:
                locations.add("account-key")
            print(
                f"| `{match['source']['surface']}:{match['source']['filename']}` | "
                f"`{match['target']['surface']}:{match['target']['filename']}` | "
                f"`{match['label']}` | `{match['value']}` | {fmt(locations, limit=4)} |"
            )
        else:
            transfer = (
                f"{match['mint']} {match['amount']} "
                f"{match['source_account']}->{match['destination']} auth={match['authority']}"
            )
            print(
                f"| `{match['source']['surface']}:{match['source']['filename']}` | "
                f"`{match['target']['surface']}:{match['target']['filename']}` | "
                f"{fmt(match['reasons'])} | `{transfer}` | `near-match` |"
            )
    if len(matches) > limit:
        print(f"| ... | ... | ... | `{len(matches) - limit} additional rows omitted` | ... |")
    print()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot_dir")
    args = parser.parse_args()
    base = Path(args.snapshot_dir)

    all_rows = rows(base)
    bk1_rows = [row for row in all_rows if row["surface"] == "bk1PDA"]
    setup_rows = [row for row in all_rows if row["surface"] == "root_submitter_setup"]
    bankk_rows = [row for row in all_rows if row["surface"] == "BankK"]
    decoded_bk1_rows = [
        row
        for row in bk1_rows + setup_rows
        if "message_hash" in row["fields"] or "withdrawal_request_pubkey" in row["fields"]
    ]
    bankk_withdraw_rows = [row for row in bankk_rows if "Withdraw" in row["instructions"]]
    bankk_verify_rows = [row for row in bankk_rows if "VerifyRequest" in row["instructions"]]
    related = set(validator_related_keys(base))
    security_hits = {
        key for row in all_rows for key in (row["keys"] & related) | ({JUP_MINT} if JUP_MINT in row["keys"] else set())
    }

    watched_labels = {
        "withdrawal_request_pubkey",
        "mint",
        "recipient",
        "jupnet",
        "impl program key",
        "message_hash",
    }
    field_matches = exact_field_matches(decoded_bk1_rows, bankk_rows, watched_labels)
    high_value_matches = [
        match
        for match in field_matches
        if match["label"] in {"message_hash", "withdrawal_request_pubkey", "jupnet", "recipient"}
    ]
    message_hash_matches = [match for match in field_matches if match["label"] == "message_hash"]
    request_matches = [match for match in field_matches if match["label"] in {"withdrawal_request_pubkey", "jupnet"}]
    recipient_matches = [match for match in field_matches if match["label"] == "recipient"]
    common_context_matches = [match for match in field_matches if match["label"] in {"mint", "impl program key"}]
    token_matches = token_near_matches(decoded_bk1_rows, bankk_withdraw_rows)

    print("# Bank Request / Message Correlation")
    print()
    print("## Scope")
    print()
    print(f"- Snapshot: `{base}`")
    print(f"- `bk1PDA...` rows loaded: `{len(bk1_rows)}`")
    print(f"- root-submitter setup rows loaded: `{len(setup_rows)}`")
    print(f"- `BankK...` rows loaded: `{len(bankk_rows)}`")
    print(f"- decoded `bk1PDA...` / setup request rows: `{len(decoded_bk1_rows)}`")
    print(f"- `BankK...` Withdraw rows: `{len(bankk_withdraw_rows)}`")
    print(f"- `BankK...` VerifyRequest rows: `{len(bankk_verify_rows)}`")
    print(f"- canonical JUP / current validator / vote / stake intersections: `{len(security_hits)}`")
    print()

    print("## Surface Decodability")
    print()
    print("| Surface | Txs | Decoded message hashes | Decoded request pubkeys | SubmitInbox | VerifyOutbox | Signature verified | Created account spaces | Fee payers | Signers |")
    print("|---|---:|---:|---:|---:|---:|---:|---|---|---|")
    for surface, surface_rows in (
        ("bk1PDA", bk1_rows),
        ("root_submitter_setup", setup_rows),
        ("BankK", bankk_rows),
    ):
        summary = surface_summary(surface_rows)
        print(
            f"| `{surface}` | {summary['txs']} | {summary['decoded_message_hashes']} | "
            f"{summary['decoded_requests']} | {summary['submit_inbox']} | {summary['verify_outbox']} | "
            f"{summary['signature_verified']} | {fmt_counter(summary['created_account_spaces'], limit=8)} | "
            f"{fmt_counter(summary['fee_payers'], limit=4)} | {fmt_counter(summary['signers'], limit=4)} |"
        )
    print()

    print("## Correlation Summary")
    print()
    print(f"- Exact high-value request/message/recipient hits from `bk1PDA...`/setup into `BankK...`: `{len(high_value_matches)}`")
    print(f"- Exact `message_hash` hits inside `BankK...` account keys or raw payload blobs: `{len(message_hash_matches)}`")
    print(f"- Exact withdrawal-request / `jupnet` pubkey hits inside `BankK...`: `{len(request_matches)}`")
    print(f"- Exact recipient pubkey hits inside `BankK...`: `{len(recipient_matches)}`")
    print(f"- Exact common mint/implementation context hits inside `BankK...`: `{len(common_context_matches)}`")
    print(f"- Token near-matches between decoded `bk1PDA...` withdrawals and `BankK...` Withdraw transfers: `{len(token_matches)}`")
    print()

    print_match_rows(message_hash_matches, "Exact Message Hash Matches")
    print_match_rows(request_matches, "Exact Request / JupNet Pubkey Matches")
    print_match_rows(token_matches, "Token Near-Matches", limit=30)

    print("## BankK Role Map")
    print()
    print("| Instruction | Count | SubmitInbox | VerifyOutbox | Programs | Created account spaces | Token authorities |")
    print("|---|---:|---:|---:|---|---|---|")
    by_instruction: dict[str, list[dict]] = collections.defaultdict(list)
    for row in bankk_rows:
        names = row["instructions"] or ["unknown"]
        for name in names:
            by_instruction[name].append(row)
    for name, grouped in sorted(by_instruction.items()):
        program_counter = collections.Counter(program for row in grouped for program in row["programs"])
        created_counter = collections.Counter(
            f"{item['owner']} space={item['space']}"
            for row in grouped
            for item in row["created_accounts"]
            if item.get("owner") and item.get("space") is not None
        )
        authority_counter = collections.Counter(
            transfer["authority"]
            for row in grouped
            for transfer in row["token_transfers"]
            if transfer["kind"] == "token" and transfer.get("authority")
        )
        print(
            f"| `{name}` | {len(grouped)} | {sum(row['submit_inbox'] for row in grouped)} | "
            f"{sum(row['verify_outbox'] for row in grouped)} | {fmt_counter(program_counter, limit=6)} | "
            f"{fmt_counter(created_counter, limit=6)} | {fmt_counter(authority_counter, limit=6)} |"
        )
    print()

    print("## Assessment")
    print()
    if message_hash_matches or request_matches:
        print("- At least one decoded `bk1PDA...` request/message field appears directly in the sampled `BankK...` account keys or raw payload blobs.")
    else:
        print("- No decoded `bk1PDA...` message hash, withdrawal-request pubkey or `jupnet` pubkey appeared directly in sampled `BankK...` account keys or raw payload blobs.")
    if token_matches:
        print("- Token-level near-matches exist, but they are not enough to prove the same request moved through both surfaces without a shared message hash, request account or recipient account.")
    else:
        print("- No amount+recipient or amount+mint token near-match was found between decoded `bk1PDA...` withdrawals and sampled `BankK...` Withdraw transfers.")
    print("- The strongest connection remains structural: shared operational signer behavior, shared Bank/Gum domain, and adjacent inbox/outbox helper behavior, not a per-message proof across the two sampled windows.")
    print("- The `BankK...` rows create Bank-owned request/state accounts with 41-byte and 223-byte layouts, while decoded `bk1PDA...` request rows create 72-byte request accounts; this supports separate public state layouts for the two surfaces.")
    if security_hits:
        print(f"- Watched canonical JUP / validator / vote / stake intersections appeared: {fmt(security_hits)}")
    else:
        print("- No canonical JUP/current validator/vote/stake key intersections appeared in the correlation corpus.")


if __name__ == "__main__":
    main()
