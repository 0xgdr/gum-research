#!/usr/bin/env python3
"""Hunt for public sources behind an outbox epoch Merkle root."""

from __future__ import annotations

import argparse
import base64
import collections
import datetime as dt
import hashlib
import json
import struct
from pathlib import Path
from typing import Any


ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
JUP_MINT = "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN"
OUTBOX_PROGRAM = "jnoUtncGR9ZCCMixtys6Gzy5coTo6mnmUZuEHRQFTFV"
ROOT_ACCOUNT = "3C1LxtpR3Mh5RQjydfeQdvRaAzpStWM7gBi1XzP9oyGt"


def b58decode(value: str) -> bytes:
    number = 0
    for char in value:
        number = number * 58 + ALPHABET.index(char)
    data = number.to_bytes((number.bit_length() + 7) // 8, "big") if number else b""
    return (b"\0" * (len(value) - len(value.lstrip("1")))) + data


def sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def load(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def block_time(value: int | None) -> str:
    if value is None:
        return "unknown"
    return dt.datetime.fromtimestamp(value, dt.timezone.utc).isoformat()


def parse_update_payload(raw: bytes) -> dict | None:
    if len(raw) != 305:
        return None
    proof_count = struct.unpack("<I", raw[73:77])[0]
    proof_start = 77
    proof_end = proof_start + proof_count * 32
    if proof_end + 68 != len(raw):
        return None
    proof_nodes = [raw[proof_start + index * 32 : proof_start + (index + 1) * 32] for index in range(proof_count)]
    path_bitmap = struct.unpack("<I", raw[proof_end : proof_end + 4])[0]
    leaf_material = raw[proof_end + 4 :]
    current = sha256(b"\x00" + leaf_material)
    for index, sibling in enumerate(proof_nodes):
        sibling_on_left = bool((path_bitmap >> index) & 1)
        left = sibling if sibling_on_left else current
        right = current if sibling_on_left else sibling
        current = sha256(b"\x01" + left + right)
    return {
        "epoch": struct.unpack("<Q", raw[1:9])[0],
        "root": raw[9:41],
        "unknown_32": raw[41:73],
        "proof_count": proof_count,
        "path_bitmap": path_bitmap,
        "leaf_material": leaf_material,
        "leaf_hash": sha256(b"\x00" + leaf_material),
        "recomputed_root": current,
        "merkle_match": current == raw[9:41],
    }


def update_payloads(base: Path) -> list[dict]:
    rows = []
    for path in sorted(base.glob("solana-mainnet-outbox-tx-*.json")):
        tx = load(path).get("result")
        if not tx:
            continue
        for index, ix in enumerate(tx.get("transaction", {}).get("message", {}).get("instructions") or []):
            if ix.get("programId") != OUTBOX_PROGRAM:
                continue
            try:
                raw = b58decode(ix.get("data") or "")
            except ValueError:
                continue
            parsed = parse_update_payload(raw)
            if not parsed:
                continue
            rows.append(
                {
                    "file": path.name,
                    "signature": (tx.get("transaction", {}).get("signatures") or [""])[0],
                    "slot": tx.get("slot"),
                    "block_time": tx.get("blockTime"),
                    "instruction_index": index,
                    "raw": raw,
                    **parsed,
                }
            )
    return rows


def validator_related_targets(base: Path) -> dict[str, str]:
    targets = {}
    votes = (load(base / "getVoteAccounts.json").get("result") or {})
    for row in (votes.get("current") or []) + (votes.get("delinquent") or []):
        targets[f"validator node {row['nodePubkey']}"] = row["nodePubkey"]
        targets[f"vote account {row['votePubkey']}"] = row["votePubkey"]
    for item in load(base / "getProgramAccounts-Stake.json").get("result") or []:
        targets[f"stake account {item['pubkey']}"] = item["pubkey"]
    return targets


def decode_base64(value: str) -> bytes | None:
    try:
        return base64.b64decode(value, validate=True)
    except ValueError:
        return None


def decode_program_data_log(line: str) -> bytes | None:
    prefix = "Program data: "
    if prefix not in line:
        return None
    return decode_base64(line.split(prefix, 1)[1])


def extract_binary_records(path: Path, node: Any, trail: str = "$") -> list[dict]:
    records = []
    if isinstance(node, dict):
        data = node.get("data")
        if isinstance(data, list) and len(data) >= 2 and data[1] == "base64" and isinstance(data[0], str):
            raw = decode_base64(data[0])
            if raw is not None:
                records.append(
                    {
                        "file": path.name,
                        "json_path": f"{trail}.data",
                        "kind": "account-base64",
                        "raw": raw,
                        "owner": node.get("owner"),
                        "space": node.get("space"),
                    }
                )
        if isinstance(data, str) and isinstance(node.get("programId"), str):
            try:
                raw = b58decode(data)
            except ValueError:
                raw = None
            if raw is not None:
                records.append(
                    {
                        "file": path.name,
                        "json_path": f"{trail}.data",
                        "kind": "instruction-base58",
                        "raw": raw,
                        "program_id": node.get("programId"),
                    }
                )
        logs = node.get("logMessages")
        if isinstance(logs, list):
            for index, line in enumerate(logs):
                if not isinstance(line, str):
                    continue
                raw = decode_program_data_log(line)
                if raw is not None:
                    records.append(
                        {
                            "file": path.name,
                            "json_path": f"{trail}.logMessages[{index}]",
                            "kind": "program-data-log",
                            "raw": raw,
                        }
                    )
        for key, value in node.items():
            records.extend(extract_binary_records(path, value, f"{trail}.{key}"))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            records.extend(extract_binary_records(path, value, f"{trail}[{index}]"))
    return records


def all_binary_records(base: Path) -> list[dict]:
    records = []
    for path in sorted(base.glob("*.json")):
        data = load(path)
        records.extend(extract_binary_records(path, data))
    return records


def hex_short(value: bytes, size: int = 16) -> str:
    text = value.hex()
    return text if len(text) <= size * 2 else f"{text[:size * 2]}..."


def fmt_hits(values: list[str], empty: str = "`None`") -> str:
    if not values:
        return empty
    return "<br>".join(f"`{value}`" for value in values)


def target_hits(records: list[dict], targets: dict[str, bytes]) -> dict[str, list[dict]]:
    hits = {name: [] for name in targets}
    for record in records:
        raw = record["raw"]
        for name, target in targets.items():
            if target and target in raw:
                hits[name].append(record)
    return hits


def text_hits(base: Path, labels: dict[str, str]) -> dict[str, list[str]]:
    hits = {label: [] for label in labels}
    for path in sorted(base.glob("*.json")):
        text = path.read_text(errors="ignore")
        for label, needle in labels.items():
            if needle in text:
                hits[label].append(path.name)
    return hits


def co_located_records(records: list[dict], required: bytes, others: dict[str, bytes]) -> list[dict]:
    rows = []
    for record in records:
        raw = record["raw"]
        if required not in raw:
            continue
        found = [label for label, target in others.items() if target in raw]
        if found:
            rows.append({**record, "co_hits": found})
    return rows


def candidate_registry_records(records: list[dict], update: dict, watched: dict[str, bytes]) -> list[dict]:
    epoch_bytes = struct.pack("<Q", update["epoch"])
    rows = []
    for record in records:
        raw = record["raw"]
        signals = []
        if update["root"] in raw:
            signals.append("root")
        if update["leaf_material"] in raw:
            signals.append("candidate aggregate key")
        if update["leaf_hash"] in raw:
            signals.append("leaf hash")
        if update["unknown_32"] in raw:
            signals.append("untyped verifier field")
        if epoch_bytes in raw:
            signals.append(f"epoch {update['epoch']} little-endian")
        security_hits = [label for label, target in watched.items() if target in raw]
        if signals or security_hits:
            rows.append(
                {
                    **record,
                    "signals": signals,
                    "security_hits": security_hits,
                    "sha256": hashlib.sha256(raw).hexdigest(),
                }
            )
    return rows


def classify_record(record: dict) -> str:
    if record.get("program_id") == OUTBOX_PROGRAM:
        return "outbox instruction"
    if record.get("file", "").startswith("solana-mainnet-outbox-tx-"):
        return "outbox transaction"
    if record.get("file") == "solana-mainnet-getProgramAccounts-JupNetOutboxProgram.json":
        return "outbox-owned account state"
    if record.get("file", "").startswith("getProgramAccounts-"):
        return "JupNet account collection"
    if record.get("file", "").startswith("solana-mainnet-getAccountInfo-"):
        return "Solana account/program state"
    return "other saved artifact"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot_dir")
    args = parser.parse_args()
    base = Path(args.snapshot_dir)

    updates = update_payloads(base)
    records = all_binary_records(base)
    validator_targets = validator_related_targets(base)
    watched_text = {"canonical JUP mint": JUP_MINT, **validator_targets}
    watched_raw = {label: b58decode(value) for label, value in watched_text.items()}

    print("# Epoch Security Source Hunt")
    print()
    print("## Scope")
    print()
    print(f"- Snapshot: `{base}`")
    print(f"- Binary records scanned: `{len(records)}`")
    print(f"- Outbox update payloads decoded: `{len(updates)}`")
    print(f"- Watched validator/vote/stake keys: `{len(validator_targets)}`")
    print()

    if not updates:
        print("## Assessment")
        print()
        print("- No decodable outbox root-update payload was available in this snapshot.")
        return

    update = updates[0]
    proof_targets = {
        "epoch root": update["root"],
        "candidate aggregate key material": update["leaf_material"],
        "candidate aggregate-key leaf hash": update["leaf_hash"],
        "untyped 32-byte verifier field": update["unknown_32"],
        "full 305-byte update payload": update["raw"],
    }
    hits = target_hits(records, proof_targets)
    text = text_hits(base, watched_text)
    aggregate_colocations = co_located_records(records, update["leaf_material"], watched_raw)
    root_colocations = co_located_records(records, update["root"], watched_raw)
    candidates = candidate_registry_records(records, update, watched_raw)

    print("## Root Under Test")
    print()
    print(f"- Source transaction file: `{update['file']}`")
    print(f"- Signature: `{update['signature']}`")
    print(f"- Slot: `{update['slot']}`")
    print(f"- Time: `{block_time(update['block_time'])}`")
    print(f"- Epoch/root slot: `{update['epoch']}`")
    print(f"- Root: `{update['root'].hex()}`")
    print(f"- Candidate aggregate-key material: `{update['leaf_material'].hex()}`")
    print(f"- Candidate leaf hash: `{update['leaf_hash'].hex()}`")
    print(f"- Merkle match: `{update['merkle_match']}`")
    print()

    print("## Target Byte Hits")
    print()
    print("| Target | Hits | Hit classes | First hit locations |")
    print("|---|---:|---|---|")
    for name, rows in hits.items():
        classes = collections.Counter(classify_record(row) for row in rows)
        first = [f"{row['file']} {row['json_path']} ({row['kind']}, {len(row['raw'])} bytes)" for row in rows[:6]]
        print(f"| `{name}` | {len(rows)} | {fmt_hits([f'{k}: {v}' for k, v in classes.items()])} | {fmt_hits(first)} |")
    print()

    print("## Watched Security Text Hits")
    print()
    print("| Watched value | Files containing text |")
    print("|---|---:|")
    for label, rows in text.items():
        if label != "canonical JUP mint" and not rows:
            continue
        print(f"| `{label}` | {len(rows)} |")
    print()

    print("## Co-Location Checks")
    print()
    print("| Check | Matching records |")
    print("|---|---:|")
    print(f"| Candidate aggregate key in same binary record as canonical JUP/validator/vote/stake key | {len(aggregate_colocations)} |")
    print(f"| Epoch root in same binary record as canonical JUP/validator/vote/stake key | {len(root_colocations)} |")
    print()
    if aggregate_colocations or root_colocations:
        print("| File | JSON path | Co-located hits |")
        print("|---|---|---|")
        for row in (aggregate_colocations + root_colocations)[:20]:
            print(f"| `{row['file']}` | `{row['json_path']}` | {fmt_hits(row['co_hits'])} |")
        print()

    print("## Candidate Registry Records")
    print()
    print("| File | JSON path | Kind | Size | Signals | Security hits | SHA256 |")
    print("|---|---|---|---:|---|---|---|")
    for row in candidates[:80]:
        print(
            f"| `{row['file']}` | `{row['json_path']}` | `{row['kind']}` | {len(row['raw'])} | "
            f"{fmt_hits(row['signals'])} | {fmt_hits(row['security_hits'])} | `{row['sha256']}` |"
        )
    if not candidates:
        print("| `None` | `None` | `None` | 0 | `None` | `None` | `None` |")
    print()

    print("## Assessment")
    print()
    if hits["candidate aggregate key material"]:
        print("- The candidate aggregate-key material appears in saved public artifacts.")
    else:
        print("- The candidate aggregate-key material was only recoverable from the decoded outbox update transaction payload.")
    if aggregate_colocations or root_colocations:
        print("- At least one saved binary record co-locates root/update material with watched JUP or validator/vote/stake keys; inspect the table above.")
    else:
        print("- No saved binary record co-located the epoch root or candidate aggregate key with canonical JUP, current validator, vote or stake keys.")
    print("- This hunt did not find a public top-half source that maps Dove identities, stake weights or JUP balances into the aggregate-key Merkle tree.")
    print("- The current public evidence still stops at the compact verification boundary: aggregate-key material, Merkle proof, epoch root and BLS verification logs.")


if __name__ == "__main__":
    main()
