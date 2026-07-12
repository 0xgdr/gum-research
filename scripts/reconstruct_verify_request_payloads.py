#!/usr/bin/env python3
"""Reconstruct sampled GUM Bank verify_request payload structure."""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import json
import struct
from pathlib import Path


ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
GUM_BANK_PROGRAM = "BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ"
VERIFY_REQUEST_DISC = "891f2fe4cdea81ed"
JUP_MINT = "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN"
USDC = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
WRAPPED_SOL = "So11111111111111111111111111111111111111112"
BANK_PROGRAM = GUM_BANK_PROGRAM
INBOX_PROGRAM = "JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw"
OUTBOX_PROGRAM = "jnoUtncGR9ZCCMixtys6Gzy5coTo6mnmUZuEHRQFTFV"
OUTBOX_ROOT_ACCOUNT = "3C1LxtpR3Mh5RQjydfeQdvRaAzpStWM7gBi1XzP9oyGt"


WATCHED_KEYS = {
    "canonical JUP mint": JUP_MINT,
    "USDC mint": USDC,
    "wrapped SOL mint": WRAPPED_SOL,
    "Bank Program": BANK_PROGRAM,
    "Inbox Program": INBOX_PROGRAM,
    "Outbox Program": OUTBOX_PROGRAM,
    "Outbox root account": OUTBOX_ROOT_ACCOUNT,
}


def b58decode(value: str) -> bytes:
    number = 0
    for char in value:
        number = number * 58 + ALPHABET.index(char)
    data = number.to_bytes((number.bit_length() + 7) // 8, "big") if number else b""
    return (b"\0" * (len(value) - len(value.lstrip("1")))) + data


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


def validator_related_keys(base: Path) -> dict[str, str]:
    keys = {}
    votes = (load(base / "getVoteAccounts.json").get("result") or {})
    for row in (votes.get("current") or []) + (votes.get("delinquent") or []):
        keys[row["nodePubkey"]] = "validator node"
        keys[row["votePubkey"]] = "vote account"
    for item in load(base / "getProgramAccounts-Stake.json").get("result") or []:
        keys[item["pubkey"]] = "stake account"
    return keys


def verify_rows(base: Path) -> list[dict]:
    rows = []
    watched = dict(WATCHED_KEYS)
    watched.update(validator_related_keys(base))
    for path in sorted(base.glob("solana-mainnet-bank-tx-*.json")):
        tx = load(path).get("result")
        if not tx:
            continue
        message = tx.get("transaction", {}).get("message", {})
        for index, ix in enumerate(message.get("instructions", [])):
            if ix.get("programId") != GUM_BANK_PROGRAM:
                continue
            raw = b58decode(ix.get("data", ""))
            if raw[:8].hex() != VERIFY_REQUEST_DISC:
                continue
            payload = raw[8:]
            key_hits = []
            for label, key in watched.items():
                try:
                    needle = b58decode(key)
                except ValueError:
                    continue
                offsets = []
                start = payload.find(needle)
                while start != -1:
                    offsets.append(start)
                    start = payload.find(needle, start + 1)
                if offsets:
                    key_hits.append((label, key, offsets))
            rows.append(
                {
                    "file": path.name,
                    "slot": tx.get("slot"),
                    "block_time": tx.get("blockTime"),
                    "signature": (tx.get("transaction", {}).get("signatures") or [""])[0],
                    "instruction_index": index,
                    "accounts": ix.get("accounts") or [],
                    "raw": raw,
                    "payload": payload,
                    "key_hits": key_hits,
                }
            )
    return rows


def diff_ranges(payloads: list[bytes]) -> list[tuple[int, int]]:
    if len(payloads) < 2:
        return []
    length = min(len(payload) for payload in payloads)
    diffs = []
    for offset in range(length):
        values = {payload[offset] for payload in payloads}
        if len(values) > 1:
            diffs.append(offset)
    if not diffs:
        return []
    ranges = []
    start = previous = diffs[0]
    for offset in diffs[1:]:
        if offset == previous + 1:
            previous = offset
            continue
        ranges.append((start, previous))
        start = previous = offset
    ranges.append((start, previous))
    return ranges


def outbox_roots(base: Path) -> list[dict]:
    data = load(base / "solana-mainnet-getProgramAccounts-JupNetOutboxProgram.json")
    items = data.get("result") or []
    roots = []
    for item in items:
        raw = b""
        account_data = item.get("account", {}).get("data")
        if isinstance(account_data, list):
            raw = base64.b64decode(account_data[0])
        for offset in range(0, len(raw), 40):
            chunk = raw[offset : offset + 40]
            if len(chunk) < 40:
                continue
            epoch = struct.unpack("<Q", chunk[:8])[0]
            root = chunk[8:40]
            if epoch or root != b"\0" * 32:
                roots.append({"account": item["pubkey"], "offset": offset, "epoch": epoch, "root": root})
    return roots


def proof_tail(payload: bytes) -> dict | None:
    # The samples contain bytes 00 00 00 05 00 00 00 followed by 160 bytes.
    # This permits length=5 as BE u32 at 288 or LE u32 at 291. The latter is
    # also exactly followed by five 32-byte nodes, so record both indicators.
    if len(payload) < 295:
        return None
    length_be_288 = int.from_bytes(payload[288:292], "big") if len(payload) >= 292 else None
    length_le_291 = struct.unpack("<I", payload[291:295])[0] if len(payload) >= 295 else None
    candidate_len = length_le_291 if length_le_291 and len(payload) - 295 == length_le_291 * 32 else length_be_288
    if not candidate_len or len(payload) < 295 + candidate_len * 32:
        return None
    nodes = [payload[295 + i * 32 : 295 + (i + 1) * 32] for i in range(candidate_len)]
    return {
        "length_be_288": length_be_288,
        "length_le_291": length_le_291,
        "node_start": 295,
        "nodes": nodes,
    }


def timestamp_like(payload: bytes, block_time: int | None) -> list[dict]:
    fields = []
    if len(payload) >= 86:
        value = int.from_bytes(payload[82:86], "big")
        if 1_600_000_000 < value < 2_000_000_000:
            fields.append(
                {
                    "offset": 82,
                    "encoding": "u32be",
                    "value": value,
                    "iso": dt.datetime.fromtimestamp(value, dt.timezone.utc).isoformat(),
                    "delta_from_block_time": value - block_time if block_time else None,
                }
            )
    return fields


def sha256_merkle_attempt(leaf: bytes, nodes: list[bytes], root: bytes) -> bool:
    values = {leaf}
    for node in nodes:
        next_values = set()
        for value in values:
            next_values.add(hashlib.sha256(value + node).digest())
            next_values.add(hashlib.sha256(node + value).digest())
        values = next_values
    return root in values


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot_dir")
    args = parser.parse_args()
    base = Path(args.snapshot_dir)
    rows = verify_rows(base)
    roots = outbox_roots(base)
    payloads = [row["payload"] for row in rows]
    ranges = diff_ranges(payloads)

    all_key_hits = [
        (row["file"], label, key, offsets)
        for row in rows
        for label, key, offsets in row["key_hits"]
    ]
    jup_hits = [hit for hit in all_key_hits if hit[1] == "canonical JUP mint"]
    validator_hits = [hit for hit in all_key_hits if hit[1] in {"validator node", "vote account", "stake account"}]

    print("# Verify Request Payload Reconstruction")
    print()
    print("## Scope")
    print()
    print(f"- `verify_request` samples: `{len(rows)}`")
    print(f"- Payload length: `{len(payloads[0]) if payloads else 0}`")
    print(f"- Raw instruction length: `{len(rows[0]['raw']) if rows else 0}`")
    print(f"- Canonical JUP key hits: `{len(jup_hits)}`")
    print(f"- Current JupNet validator/vote/stake key hits: `{len(validator_hits)}`")
    print()
    print("## Samples")
    print()
    print("| File | Slot | Block time | Signature | Accounts |")
    print("|---|---:|---|---|---:|")
    for row in rows:
        block = dt.datetime.fromtimestamp(row["block_time"], dt.timezone.utc).isoformat() if row["block_time"] else "unknown"
        print(f"| `{row['file']}` | {row['slot']} | `{block}` | `{row['signature']}` | {len(row['accounts'])} |")
    print()
    print("## Difference Ranges")
    print()
    if ranges:
        print("| Offset range | Length | Interpretation candidate |")
        print("|---|---:|---|")
        for start, end in ranges:
            length = end - start + 1
            candidate = ""
            if length == 32:
                candidate = "per-message 32-byte hash/key-like field"
            elif not (end < 82 or start > 85):
                candidate = "timestamp-like field"
            elif start >= 255 and length == 32:
                candidate = "per-message 32-byte leaf/hash-like field"
            print(f"| `{start}-{end}` | {length} | {candidate} |")
    else:
        print("- None")
    print()
    print("## Known Pubkey Hits")
    print()
    if all_key_hits:
        print("| File | Label | Pubkey | Payload offsets |")
        print("|---|---|---|---|")
        for filename, label, key, offsets in all_key_hits:
            print(f"| `{filename}` | {label} | `{key}` | `{', '.join(str(offset) for offset in offsets)}` |")
    else:
        print("- None")
    print()
    print("## Timestamp-Like Fields")
    print()
    ts_rows = [(row, field) for row in rows for field in timestamp_like(row["payload"], row["block_time"])]
    if ts_rows:
        print("| File | Offset | Encoding | Value | ISO time | Delta from block time |")
        print("|---|---:|---|---:|---|---:|")
        for row, field in ts_rows:
            print(
                f"| `{row['file']}` | {field['offset']} | `{field['encoding']}` | {field['value']} | "
                f"`{field['iso']}` | {field['delta_from_block_time']} |"
            )
    else:
        print("- None")
    print()
    print("## Merkle Proof Tail")
    print()
    proof_rows = [(row, proof_tail(row["payload"])) for row in rows]
    if proof_rows and all(proof for _row, proof in proof_rows):
        print(f"- Tail node start offset: `{proof_rows[0][1]['node_start']}`")
        print(f"- Length indicators: BE u32 at 288 = `{proof_rows[0][1]['length_be_288']}`, LE u32 at 291 = `{proof_rows[0][1]['length_le_291']}`")
        print()
        print("| Node index | Hex |")
        print("|---:|---|")
        for index, node in enumerate(proof_rows[0][1]["nodes"]):
            print(f"| {index} | `{node.hex()}` |")
        identical = all(proof["nodes"] == proof_rows[0][1]["nodes"] for _row, proof in proof_rows if proof)
        print()
        print(f"- Proof nodes identical across sampled payloads: `{identical}`")
    else:
        print("- No fixed proof tail recognized")
    print()
    print("## Outbox Root Comparison")
    print()
    if roots:
        print("| Epoch | Root | Present in payload | SHA256 proof attempt matched |")
        print("|---:|---|---|---|")
        for root in roots:
            present = any(root["root"] in payload for payload in payloads)
            matched = False
            for row, proof in proof_rows:
                if not proof:
                    continue
                candidates = [
                    row["payload"][46:78],
                    row["payload"][152:184],
                    row["payload"][191:223],
                    row["payload"][223:255],
                    row["payload"][255:287],
                ]
                matched = matched or any(sha256_merkle_attempt(candidate, proof["nodes"], root["root"]) for candidate in candidates)
            print(f"| {root['epoch']} | `{root['root'].hex()}` | `{present}` | `{matched}` |")
    else:
        print("- No outbox roots available")
    print()
    print("## Field Map Candidate")
    print()
    print("| Offset | Length | Observation |")
    print("|---:|---:|---|")
    print("| 0 | 4 | Stable little-endian `179`; likely serialized message/body length or domain field |")
    print("| 4 | 4 | Stable little-endian `1` |")
    print("| 13 | 32 | Embedded Bank Program pubkey |")
    print("| 46 | 32 | Per-message hash/key-like field; differs between samples |")
    print("| 82 | 4 | Big-endian timestamp-like value; equals block time + 56 seconds in both samples |")
    print("| 87 | 32 | Embedded USDC mint pubkey |")
    print("| 148 | 3 | Per-message bytes inside a mostly stable field |")
    print("| 191 | 64 | Stable 64-byte hash/signature-like region across samples |")
    print("| 255 | 32 | Per-message hash/leaf-like field; differs between samples |")
    print("| 291 | 4 | Little-endian proof node count candidate `5` |")
    print("| 295 | 160 | Five 32-byte Merkle proof nodes, identical across samples |")
    print()
    print("## Assessment")
    print()
    print("- `verify_request` carries a Merkle proof-like payload and references the outbox root state account by account meta, not by embedding the root directly.")
    print("- The sampled payloads contain USDC and Bank Program pubkeys, but no canonical JUP mint, current validator/vote/stake keys, inbox program key or outbox program key.")
    print("- The public outbox state provides Merkle roots; sampled `verify_request` payloads provide proof nodes and message/leaf-like fields.")
    print("- BLS signer/quorum material is not obvious in these `verify_request` samples. The BLS path is more likely associated with outbox root updates than per-request proof verification.")


if __name__ == "__main__":
    main()
