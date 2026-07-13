#!/usr/bin/env python3
"""Build an authority/control graph around public outbox root updates."""

from __future__ import annotations

import argparse
import base64
import collections
import datetime as dt
import json
import struct
from pathlib import Path

from analyze_outbox_root_history import OUTBOX_PROGRAM
from analyze_outbox_root_history import decode_update_payload
from analyze_outbox_root_history import transaction_files


JUP_MINT = "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN"
GUM_PROGRAM = "brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1"
GUMEB_PROGRAM = "GUMebNDCYyF81xjyqaHagbgMQVUTb8fBC9YRh25xSH64"
BANK_PROGRAM = "BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ"
INBOX_PROGRAM = "JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw"
OUTBOX_ROOT_ACCOUNT = "3C1LxtpR3Mh5RQjydfeQdvRaAzpStWM7gBi1XzP9oyGt"
SYSTEM_PROGRAM = "11111111111111111111111111111111"
COMPUTE_BUDGET = "ComputeBudget111111111111111111111111111111"
SYSVAR_INSTRUCTIONS = "Sysvar1nstructions1111111111111111111111111"
UPGRADEABLE_LOADER = "BPFLoaderUpgradeab1e11111111111111111111111"

PROGRAMDATA_FILES = {
    "JupNet Gum brhPf ProgramData": "getAccountInfo-GumProgramData-slice48.json",
    "JupNet Gum GUMeb ProgramData": "getAccountInfo-GUMebProgramData-full.json",
    "Solana Bank ProgramData": "solana-mainnet-getAccountInfo-GumBankProgramData-full.json",
    "Solana Bank Program ProgramData": "solana-mainnet-getAccountInfo-GumBankProgramProgramData-full.json",
    "Solana Inbox helper ProgramData": "solana-mainnet-getAccountInfo-OwnerProgramData-JNiN12VC.json",
    "Solana Outbox helper ProgramData": "solana-mainnet-getAccountInfo-OwnerProgramData-jnoUtncG.json",
}

KNOWN_ROLES = {
    JUP_MINT: "canonical Solana JUP mint",
    GUM_PROGRAM: "JupNet Gum brhPf executable",
    GUMEB_PROGRAM: "JupNet Gum GUMeb executable",
    BANK_PROGRAM: "Solana Gum Bank executable",
    INBOX_PROGRAM: "Solana JupNet inbox helper executable",
    OUTBOX_PROGRAM: "Solana JupNet outbox helper executable",
    OUTBOX_ROOT_ACCOUNT: "outbox Merkle root-history account",
    SYSTEM_PROGRAM: "system program",
    COMPUTE_BUDGET: "compute budget program",
    SYSVAR_INSTRUCTIONS: "instructions sysvar",
    UPGRADEABLE_LOADER: "BPF upgradeable loader",
}


def load(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def raw_account_data(account: dict | None) -> bytes:
    if not account:
        return b""
    data = account.get("data")
    if isinstance(data, list) and data:
        return base64.b64decode(data[0])
    return b""


def b58encode(data: bytes) -> str:
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    number = int.from_bytes(data, "big")
    out = ""
    while number:
        number, rem = divmod(number, 58)
        out = alphabet[rem] + out
    return ("1" * (len(data) - len(data.lstrip(b"\0")))) + (out or "")


def result(base: Path, filename: str):
    return load(base / filename).get("result")


def block_time(value: int | None) -> str:
    if value is None:
        return "unknown"
    return dt.datetime.fromtimestamp(value, dt.timezone.utc).isoformat()


def account_metas(tx: dict) -> dict[str, dict]:
    metas = {}
    for index, key in enumerate(tx.get("transaction", {}).get("message", {}).get("accountKeys") or []):
        if isinstance(key, dict):
            metas[key["pubkey"]] = {
                "index": index,
                "signer": bool(key.get("signer")),
                "writable": bool(key.get("writable")),
                "source": key.get("source"),
            }
        elif isinstance(key, str):
            metas[key] = {"index": index, "signer": False, "writable": False, "source": "unknown"}
    return metas


def validator_related_keys(base: Path) -> dict[str, str]:
    keys = {}
    votes = result(base, "getVoteAccounts.json") or {}
    for row in (votes.get("current") or []) + (votes.get("delinquent") or []):
        keys[row["nodePubkey"]] = "current validator identity"
        keys[row["votePubkey"]] = "current vote account"
    for account in result(base, "getProgramAccounts-Stake.json") or []:
        keys[account["pubkey"]] = "current native stake account"
    return keys


def parse_programdata(base: Path) -> list[dict]:
    rows = []
    seen = set()
    for label, filename in PROGRAMDATA_FILES.items():
        data = result(base, filename)
        value = data.get("value") if isinstance(data, dict) else None
        raw = raw_account_data(value)
        if not raw or len(raw) < 45:
            continue
        tag = struct.unpack("<I", raw[:4])[0]
        if tag != 3:
            continue
        slot = struct.unpack("<Q", raw[4:12])[0]
        authority = b58encode(raw[13:45]) if raw[12] == 1 else None
        key = (label, authority, slot)
        if key in seen:
            continue
        seen.add(key)
        rows.append(
            {
                "label": label,
                "filename": filename,
                "owner": value.get("owner"),
                "slot": slot,
                "authority": authority,
            }
        )
    return rows


def role_for(pubkey: str, validators: dict[str, str], upgrade_authorities: dict[str, list[str]]) -> str:
    roles = []
    if pubkey in KNOWN_ROLES:
        roles.append(KNOWN_ROLES[pubkey])
    if pubkey in validators:
        roles.append(validators[pubkey])
    for label in upgrade_authorities.get(pubkey, []):
        roles.append(f"upgrade authority for {label}")
    return "; ".join(roles)


def root_update_rows(base: Path) -> list[dict]:
    rows = []
    for path in transaction_files(base):
        tx = load(path).get("result")
        if not tx:
            continue
        metas = account_metas(tx)
        message = tx.get("transaction", {}).get("message", {})
        tx_signers = [account for account, meta in metas.items() if meta["signer"]]
        tx_writables = [account for account, meta in metas.items() if meta["writable"]]
        logs = tx.get("meta", {}).get("logMessages") or []
        update_logs = [
            line
            for line in logs
            if any(term in line for term in ("UpdateMerkleRoot", "Merkle proof verified", "Verifying BLS signature", "Signature verified"))
        ]
        for instruction_index, ix in enumerate(message.get("instructions") or []):
            if ix.get("programId") != OUTBOX_PROGRAM:
                continue
            raw = decode_instruction_data(ix.get("data") or "")
            decoded = decode_update_payload(raw)
            if not decoded:
                continue
            accounts = ix.get("accounts") or []
            rows.append(
                {
                    "file": path.name,
                    "slot": tx.get("slot"),
                    "block_time": tx.get("blockTime"),
                    "signature": (tx.get("transaction", {}).get("signatures") or [""])[0],
                    "instruction_index": instruction_index,
                    "accounts": accounts,
                    "instruction_signers": [account for account in accounts if metas.get(account, {}).get("signer")],
                    "instruction_writables": [account for account in accounts if metas.get(account, {}).get("writable")],
                    "tx_signers": tx_signers,
                    "tx_writables": tx_writables,
                    "logs": update_logs,
                    **decoded,
                }
            )
    return rows


def decode_instruction_data(value: str) -> bytes:
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    number = 0
    for char in value:
        number = number * 58 + alphabet.index(char)
    data = number.to_bytes((number.bit_length() + 7) // 8, "big") if number else b""
    return (b"\0" * (len(value) - len(value.lstrip("1")))) + data


def short(value: bytes | str, chars: int = 16) -> str:
    text = value.hex() if isinstance(value, bytes) else value
    if len(text) <= chars:
        return text
    return text[:chars] + "..."


def fmt(values: list[str], empty: str = "`None`", limit: int | None = None) -> str:
    items = [value for value in values if value]
    if limit is not None:
        items = items[:limit]
    if not items:
        return empty
    return "<br>".join(f"`{value}`" for value in items)


def fmt_counter(counter: collections.Counter[str], limit: int | None = None) -> str:
    return fmt([f"{key}: {value}" for key, value in counter.most_common(limit)])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot_dir")
    args = parser.parse_args()
    base = Path(args.snapshot_dir)

    validators = validator_related_keys(base)
    programdata = parse_programdata(base)
    upgrade_authorities = collections.defaultdict(list)
    for row in programdata:
        if row["authority"]:
            upgrade_authorities[row["authority"]].append(row["label"])

    rows = root_update_rows(base)
    signer_counter = collections.Counter(signer for row in rows for signer in row["tx_signers"])
    ix_signer_counter = collections.Counter(signer for row in rows for signer in row["instruction_signers"])
    writable_counter = collections.Counter(account for row in rows for account in row["instruction_writables"])
    account_counter = collections.Counter(account for row in rows for account in row["accounts"])
    participant_counter = collections.Counter()
    for row in rows:
        participant_counter.update(set([*row["accounts"], *row["tx_signers"], *row["tx_writables"]]))
    log_counter = collections.Counter(line for row in rows for line in row["logs"])
    root_counter = collections.Counter(row["root"].hex() for row in rows)
    aggregate_counter = collections.Counter(row["aggregate_key"].hex() for row in rows)
    security_accounts = {
        account: role_for(account, validators, upgrade_authorities)
        for row in rows
        for account in [*row["accounts"], *row["tx_signers"], *row["tx_writables"]]
        if account == JUP_MINT or account in validators
    }
    authority_intersections = {
        account: role_for(account, validators, upgrade_authorities)
        for row in rows
        for account in [*row["accounts"], *row["tx_signers"], *row["tx_writables"]]
        if account in upgrade_authorities
    }

    print("# Root Update Authority Graph")
    print()
    print("## Scope")
    print()
    print(f"- Snapshot: `{base}`")
    print(f"- Outbox helper program: `{OUTBOX_PROGRAM}`")
    print(f"- Outbox root-history account: `{OUTBOX_ROOT_ACCOUNT}`")
    print(f"- Transaction files scanned: `{len(transaction_files(base))}`")
    print(f"- Decoded root-update transactions: `{len(rows)}`")
    print(f"- Unique transaction signers on root updates: `{len(signer_counter)}`")
    print(f"- Unique instruction signers on root updates: `{len(ix_signer_counter)}`")
    print(f"- Unique instruction writable accounts on root updates: `{len(writable_counter)}`")
    print(f"- Root-update accounts intersecting canonical JUP/current validator/vote/stake keys: `{len(security_accounts)}`")
    print(f"- Root-update accounts intersecting known upgrade authorities: `{len(authority_intersections)}`")
    print()

    print("## Control Graph")
    print()
    print("| Edge | Evidence |")
    print("|---|---|")
    print(f"| `root-update tx signer -> {OUTBOX_PROGRAM}` | {fmt_counter(signer_counter)} |")
    print(f"| `instruction signer -> UpdateMerkleRoot` | {fmt_counter(ix_signer_counter)} |")
    print(f"| `UpdateMerkleRoot -> writable accounts` | {fmt_counter(writable_counter)} |")
    print(f"| `UpdateMerkleRoot -> root values` | {fmt_counter(collections.Counter(short(root) for root in root_counter))} |")
    print(f"| `UpdateMerkleRoot -> aggregate-key material` | {fmt_counter(collections.Counter(short(key) for key in aggregate_counter))} |")
    print()

    print("## Root Update Rows")
    print()
    if rows:
        print("| Time | Slot | File | Epoch | Root | Aggregate key | Tx signers | Instruction signers | Instruction writable accounts | Logs |")
        print("|---|---:|---|---:|---|---|---|---|---|---|")
        for row in sorted(rows, key=lambda item: (item["slot"] or 0, item["signature"])):
            print(
                f"| `{block_time(row['block_time'])}` | {row['slot']} | `{row['file']}` | {row['epoch']} | "
                f"`{short(row['root'])}` | `{short(row['aggregate_key'])}` | "
                f"{fmt(row['tx_signers'])} | {fmt(row['instruction_signers'])} | "
                f"{fmt(row['instruction_writables'])} | {fmt(row['logs'], limit=6)} |"
            )
    else:
        print("- No root-update payloads decoded.")
    print()

    print("## Root Update Participant Roles")
    print()
    print("| Account | Count | Role |")
    print("|---|---:|---|")
    for account, count in participant_counter.most_common(30):
        print(f"| `{account}` | {count} | `{role_for(account, validators, upgrade_authorities) or 'unknown'}` |")
    print()

    print("## Program Upgrade Authorities")
    print()
    print("| ProgramData surface | Deployment slot | Upgrade authority | Authority appears in root updates |")
    print("|---|---:|---|---|")
    for row in programdata:
        authority = row["authority"] or "None"
        appears = authority in authority_intersections if authority != "None" else False
        print(f"| `{row['label']}` | {row['slot']} | `{authority}` | `{appears}` |")
    print()

    print("## Security Intersections")
    print()
    if security_accounts:
        print("| Account | Role |")
        print("|---|---|")
        for account, role in sorted(security_accounts.items()):
            print(f"| `{account}` | `{role}` |")
    else:
        print("- No root-update account, signer or writable account intersected the canonical JUP mint or current validator/vote/stake key sets.")
    print()
    if authority_intersections:
        print("- At least one root-update account also appears as a known program upgrade authority.")
    else:
        print("- No root-update account, signer or writable account matched the parsed upgrade authorities for the Gum/Bank/inbox/outbox surfaces.")
    print()

    print("## Root Update Logs")
    print()
    if log_counter:
        for line, count in log_counter.most_common():
            print(f"- `{line}`: `{count}`")
    else:
        print("- None")
    print()

    print("## Assessment")
    print()
    print("- Public root-update submission currently resolves to the transaction signer/payer around the Solana outbox helper, plus the helper program's BLS/Merkle verification path.")
    print("- The sampled root update exposes the aggregate-key inclusion boundary, but not the producer-side Dove/JUP/stake mapping that created or weighted that aggregate key.")
    print("- The signer/control graph should be monitored for new signers, writable accounts, upgrade-authority overlap or any direct intersection with canonical JUP/current validator/vote/stake keys.")


if __name__ == "__main__":
    main()
