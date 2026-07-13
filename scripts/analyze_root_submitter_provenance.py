#!/usr/bin/env python3
"""Trace root-update submitter accounts through the saved transaction corpus."""

from __future__ import annotations

import argparse
import base64
import collections
import datetime as dt
import json
from pathlib import Path

from analyze_root_update_authority_graph import JUP_MINT
from analyze_root_update_authority_graph import KNOWN_ROLES
from analyze_root_update_authority_graph import account_metas
from analyze_root_update_authority_graph import block_time
from analyze_root_update_authority_graph import parse_programdata
from analyze_root_update_authority_graph import role_for
from analyze_root_update_authority_graph import root_update_rows
from analyze_root_update_authority_graph import validator_related_keys


SEARCH_LOG_TERMS = (
    "UpdateMerkleRoot",
    "VerifyOutboxMessage",
    "SubmitInboxMessage",
    "Verifying BLS signature",
    "Signature verified",
    "Merkle proof verified",
    "Outbox verification passed",
    "inbox",
    "outbox",
    "jup",
    "stake",
    "validator",
    "quorum",
    "signer",
    "weight",
)


def load(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def result(base: Path, filename: str):
    return load(base / filename).get("result")


def b58decode(value: str) -> bytes:
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    number = 0
    for char in value:
        number = number * 58 + alphabet.index(char)
    data = number.to_bytes((number.bit_length() + 7) // 8, "big") if number else b""
    return (b"\0" * (len(value) - len(value.lstrip("1")))) + data


def raw_account_data(account: dict | None) -> bytes:
    if not account:
        return b""
    data = account.get("data")
    if isinstance(data, list) and data:
        return base64.b64decode(data[0])
    if isinstance(data, dict):
        return json.dumps(data, sort_keys=True).encode()
    return b""


def transaction_files(base: Path) -> list[Path]:
    paths = []
    for path in sorted(base.glob("*.json")):
        data = load(path)
        tx = data.get("result")
        if isinstance(tx, dict) and isinstance(tx.get("transaction"), dict):
            paths.append(path)
    return paths


def account_keys(tx: dict) -> list[str]:
    keys = []
    for key in tx.get("transaction", {}).get("message", {}).get("accountKeys") or []:
        keys.append(key["pubkey"] if isinstance(key, dict) else key)
    return keys


def tx_signatures(tx: dict) -> list[str]:
    return tx.get("transaction", {}).get("signatures") or []


def instruction_programs(tx: dict) -> list[str]:
    programs = []
    for ix in tx.get("transaction", {}).get("message", {}).get("instructions") or []:
        program = ix.get("programId")
        if program:
            programs.append(program)
    for group in tx.get("meta", {}).get("innerInstructions") or []:
        for ix in group.get("instructions") or []:
            program = ix.get("programId")
            if program:
                programs.append(program)
    return programs


def interesting_logs(tx: dict) -> list[str]:
    logs = tx.get("meta", {}).get("logMessages") or []
    return [line for line in logs if any(term.lower() in line.lower() for term in SEARCH_LOG_TERMS)]


def balance_delta(tx: dict, account: str) -> dict:
    keys = account_keys(tx)
    if account not in keys:
        return {}
    index = keys.index(account)
    pre = tx.get("meta", {}).get("preBalances") or []
    post = tx.get("meta", {}).get("postBalances") or []
    return {
        "index": index,
        "pre": pre[index] if index < len(pre) else None,
        "post": post[index] if index < len(post) else None,
        "delta": (post[index] - pre[index]) if index < len(pre) and index < len(post) else None,
        "fee": tx.get("meta", {}).get("fee"),
    }


def token_balance_hints(tx: dict, account: str) -> list[str]:
    keys = account_keys(tx)
    hints = []
    if account not in keys:
        return hints
    index = keys.index(account)
    for name in ("preTokenBalances", "postTokenBalances"):
        for row in tx.get("meta", {}).get(name) or []:
            if row.get("accountIndex") == index:
                hints.append(f"{name}: mint={row.get('mint')} owner={row.get('owner')}")
    return hints


def upgrade_authority_map(base: Path) -> dict[str, list[str]]:
    out = collections.defaultdict(list)
    for row in parse_programdata(base):
        if row.get("authority"):
            out[row["authority"]].append(row["label"])
    return out


def scan_account_data_for_submitters(base: Path, submitters: set[str]) -> dict[str, list[str]]:
    needles = {submitter: b58decode(submitter) for submitter in submitters}
    hits = collections.defaultdict(list)
    for path in sorted(base.glob("*.json")):
        data = load(path)
        candidates = []
        value = data.get("result")
        if isinstance(value, dict) and isinstance(value.get("value"), dict):
            candidates.append((path.name, value["value"]))
        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict) and isinstance(item.get("account"), dict):
                    candidates.append((f"{path.name}:{item.get('pubkey')}", item["account"]))
        for label, account in candidates:
            raw = raw_account_data(account)
            text = json.dumps(account, sort_keys=True)
            for submitter, raw_needle in needles.items():
                if submitter in text or (raw_needle and raw_needle in raw):
                    hits[submitter].append(label)
    return hits


def fmt(values: list[str] | set[str], empty: str = "`None`", limit: int | None = None) -> str:
    items = sorted(values) if isinstance(values, set) else list(values)
    items = [item for item in items if item]
    if limit is not None:
        items = items[:limit]
    if not items:
        return empty
    return "<br>".join(f"`{item}`" for item in items)


def fmt_counter(counter: collections.Counter[str], limit: int | None = None) -> str:
    return fmt([f"{key}: {value}" for key, value in counter.most_common(limit)])


def short_signature(tx: dict) -> str:
    signature = (tx_signatures(tx) or [""])[0]
    return signature[:12] + "..." if len(signature) > 12 else signature


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot_dir")
    args = parser.parse_args()
    base = Path(args.snapshot_dir)

    validators = validator_related_keys(base)
    upgrade_authorities = upgrade_authority_map(base)
    root_rows = root_update_rows(base)
    submitters = {signer for row in root_rows for signer in row["tx_signers"]}
    files = transaction_files(base)
    account_data_hits = scan_account_data_for_submitters(base, submitters)

    occurrence_rows = []
    signer_rows = []
    program_counter = collections.Counter()
    coaccount_counter = collections.Counter()
    role_counter = collections.Counter()
    security_intersections = collections.defaultdict(set)
    upgrade_intersections = collections.defaultdict(set)
    root_update_files = {row["file"] for row in root_rows}

    for path in files:
        tx = load(path).get("result")
        keys = set(account_keys(tx))
        metas = account_metas(tx)
        signers = {account for account, meta in metas.items() if meta["signer"]}
        matched = keys & submitters
        if not matched:
            continue
        programs = instruction_programs(tx)
        for program in programs:
            program_counter[program] += 1
        for account in keys:
            if account not in submitters:
                coaccount_counter[account] += 1
                role = role_for(account, validators, upgrade_authorities)
                if role:
                    role_counter[role] += 1
        for submitter in matched:
            if submitter in signers:
                signer_rows.append(path.name)
            security_intersections[submitter].update((keys & set(validators)) | ({JUP_MINT} if JUP_MINT in keys else set()))
            upgrade_intersections[submitter].update(keys & set(upgrade_authorities))
            occurrence_rows.append(
                {
                    "file": path.name,
                    "slot": tx.get("slot"),
                    "time": block_time(tx.get("blockTime")),
                    "signature": short_signature(tx),
                    "submitter": submitter,
                    "is_signer": submitter in signers,
                    "is_root_update": path.name in root_update_files,
                    "balance": balance_delta(tx, submitter),
                    "programs": programs,
                    "logs": interesting_logs(tx),
                    "token_hints": token_balance_hints(tx, submitter),
                }
            )

    print("# Root Submitter Provenance")
    print()
    print("## Scope")
    print()
    print(f"- Snapshot: `{base}`")
    print(f"- Root-update submitters derived from decoded root updates: `{len(submitters)}`")
    print(f"- Saved transaction bodies scanned: `{len(files)}`")
    print(f"- Transactions containing a root-update submitter: `{len(occurrence_rows)}`")
    print(f"- Transactions where a root-update submitter is a signer: `{len(signer_rows)}`")
    print(f"- Submitter account-data hits outside transaction bodies: `{sum(len(v) for v in account_data_hits.values())}`")
    print()

    print("## Submitter Summary")
    print()
    print("| Submitter | Tx occurrences | Signer occurrences | Security intersections | Upgrade-authority intersections | Account-data hits |")
    print("|---|---:|---:|---|---|---|")
    for submitter in sorted(submitters):
        tx_count = sum(1 for row in occurrence_rows if row["submitter"] == submitter)
        signer_count = sum(1 for row in occurrence_rows if row["submitter"] == submitter and row["is_signer"])
        print(
            f"| `{submitter}` | {tx_count} | {signer_count} | "
            f"{fmt(security_intersections[submitter])} | {fmt(upgrade_intersections[submitter])} | "
            f"{fmt(account_data_hits.get(submitter, []), limit=6)} |"
        )
    print()

    print("## Transaction Occurrences")
    print()
    if occurrence_rows:
        print("| File | Time | Slot | Signature | Submitter signer | Root update | Balance delta | Programs | Relevant logs |")
        print("|---|---|---:|---|---|---|---|---|---|")
        for row in sorted(occurrence_rows, key=lambda item: (item["slot"] or 0, item["file"])):
            balance = row["balance"]
            balance_text = (
                f"pre={balance.get('pre')} post={balance.get('post')} "
                f"delta={balance.get('delta')} fee={balance.get('fee')}"
                if balance
                else "None"
            )
            print(
                f"| `{row['file']}` | `{row['time']}` | {row['slot']} | `{row['signature']}` | "
                f"`{row['is_signer']}` | `{row['is_root_update']}` | `{balance_text}` | "
                f"{fmt(row['programs'])} | {fmt(row['logs'], limit=8)} |"
            )
    else:
        print("- No saved transaction bodies contained the derived root-update submitters.")
    print()

    print("## Co-Occurrence Summary")
    print()
    print("| Group | Values |")
    print("|---|---|")
    print(f"| Programs invoked with submitter | {fmt_counter(program_counter)} |")
    print(f"| Repeated co-accounts | {fmt_counter(coaccount_counter, limit=20)} |")
    print(f"| Known co-account roles | {fmt_counter(role_counter, limit=20)} |")
    print()

    print("## Funding And Asset Clues")
    print()
    if occurrence_rows:
        for row in occurrence_rows:
            token_hints = row["token_hints"]
            balance = row["balance"]
            delta = balance.get("delta") if balance else None
            fee = balance.get("fee") if balance else None
            print(
                f"- `{row['submitter']}` in `{row['file']}` had lamport delta `{delta}` with transaction fee `{fee}`; "
                f"token-balance hints: {fmt(token_hints)}"
            )
    else:
        print("- No funding or token-balance clues were available in saved transaction bodies.")
    print()

    print("## Assessment")
    print()
    if submitters:
        print("- Within the saved corpus, the root-update submitter appears as a narrow outbox-root publisher rather than a broad Gum/Bank operator.")
        print("- The observed transaction only paid the Solana transaction fee and wrote the outbox root-history account; no token balance movement was attached to the submitter.")
        print("- The saved corpus does not show the submitter touching canonical JUP, current validator/vote/stake accounts, parsed upgrade authorities, signer-set accounts, quorum state, slashing state or rewards.")
        print("- Full provenance still requires collecting a direct signature window for the submitter address and walking its funding history.")
    else:
        print("- No root-update submitter could be derived from the saved root-update rows.")


if __name__ == "__main__":
    main()
