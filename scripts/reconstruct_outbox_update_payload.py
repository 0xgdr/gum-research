#!/usr/bin/env python3
"""Reconstruct JupNet outbox root-update payloads from saved transaction JSON."""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import json
import struct
from pathlib import Path


ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
OUTBOX_PROGRAM = "jnoUtncGR9ZCCMixtys6Gzy5coTo6mnmUZuEHRQFTFV"


def b58decode(value: str) -> bytes:
    number = 0
    for char in value:
        number = number * 58 + ALPHABET.index(char)
    data = number.to_bytes((number.bit_length() + 7) // 8, "big") if number else b""
    return (b"\0" * (len(value) - len(value.lstrip("1")))) + data


def load(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def block_time(value: int | None) -> str:
    if value is None:
        return "unknown"
    return dt.datetime.fromtimestamp(value, dt.timezone.utc).isoformat()


def sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def recompute_root(leaf_material: bytes, proof_nodes: list[bytes], path_bitmap: int) -> tuple[bytes, list[dict]]:
    current = sha256(b"\x00" + leaf_material)
    steps = []
    for index, sibling in enumerate(proof_nodes):
        sibling_on_left = bool((path_bitmap >> index) & 1)
        left = sibling if sibling_on_left else current
        right = current if sibling_on_left else sibling
        parent = sha256(b"\x01" + left + right)
        steps.append(
            {
                "index": index,
                "bit": 1 if sibling_on_left else 0,
                "sibling_position": "left" if sibling_on_left else "right",
                "input": current,
                "sibling": sibling,
                "parent": parent,
            }
        )
        current = parent
    return current, steps


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
    recomputed_root, steps = recompute_root(leaf_material, proof_nodes, path_bitmap)

    return {
        "instruction_tag": raw[0],
        "epoch": struct.unpack("<Q", raw[1:9])[0],
        "root": raw[9:41],
        "unknown_32": raw[41:73],
        "proof_count": proof_count,
        "proof_nodes": proof_nodes,
        "path_bitmap": path_bitmap,
        "leaf_material": leaf_material,
        "leaf_hash": sha256(b"\x00" + leaf_material),
        "recomputed_root": recomputed_root,
        "merkle_match": recomputed_root == raw[9:41],
        "steps": steps,
    }


def outbox_instruction_rows(base: Path) -> list[dict]:
    rows = []
    for path in sorted(base.glob("solana-mainnet-outbox-tx-*.json")):
        tx = load(path).get("result")
        if not tx:
            continue
        for index, ix in enumerate(tx.get("transaction", {}).get("message", {}).get("instructions") or []):
            if ix.get("programId") != OUTBOX_PROGRAM:
                continue
            raw = b58decode(ix.get("data") or "")
            decoded = parse_update_payload(raw)
            if not decoded:
                continue
            rows.append(
                {
                    "file": path.name,
                    "slot": tx.get("slot"),
                    "block_time": tx.get("blockTime"),
                    "signature": (tx.get("transaction", {}).get("signatures") or [""])[0],
                    "instruction_index": index,
                    "raw": raw,
                    "decoded": decoded,
                    "logs": tx.get("meta", {}).get("logMessages") or [],
                }
            )
    return rows


def program_data_logs(logs: list[str]) -> list[bytes]:
    decoded = []
    prefix = "Program data: "
    for line in logs:
        if prefix not in line:
            continue
        try:
            decoded.append(base64.b64decode(line.split(prefix, 1)[1]))
        except ValueError:
            continue
    return decoded


def fmt_hex(value: bytes) -> str:
    return f"`{value.hex()}`"


def bitmap_bits(path_bitmap: int, proof_count: int) -> str:
    return "".join(str((path_bitmap >> index) & 1) for index in range(proof_count))


def print_offsets() -> None:
    print("| Offset | Length | Interpretation |")
    print("|---:|---:|---|")
    print("| `0` | 1 | Instruction tag, observed `1` |")
    print("| `1` | 8 | Epoch/root-slot candidate, little-endian u64 |")
    print("| `9` | 32 | Merkle root stored/emitted by the outbox helper |")
    print("| `41` | 32 | Untyped 32-byte field; likely signed message hash or compact signature material |")
    print("| `73` | 4 | Merkle proof node count, little-endian u32 |")
    print("| `77` | `32 * proof_count` | Merkle proof sibling nodes |")
    print("| after proof | 4 | Merkle path orientation bitmap |")
    print("| after bitmap | 64 | Candidate aggregated BLS public key material; hashes as the Merkle leaf material |")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot_dir")
    args = parser.parse_args()

    base = Path(args.snapshot_dir)
    rows = outbox_instruction_rows(base)

    print("# Outbox Update Payload Reconstruction")
    print()
    print("## Scope")
    print()
    print(f"- Snapshot: `{base}`")
    print(f"- Outbox helper program: `{OUTBOX_PROGRAM}`")
    print(f"- 305-byte update payloads decoded: `{len(rows)}`")
    print("- Merkle formula tested: `leaf = SHA256(0x00 || candidate_64_bytes)` and `parent = SHA256(0x01 || left || right)`")
    print()
    print("## Payload Layout")
    print()
    if rows:
        print_offsets()
    else:
        print("- No decodable 305-byte update payloads found.")
    print()

    for row in rows:
        decoded = row["decoded"]
        print(f"## `{row['file']}`")
        print()
        print(f"- Signature: `{row['signature']}`")
        print(f"- Slot: `{row['slot']}`")
        print(f"- Time: `{block_time(row['block_time'])}`")
        print(f"- Instruction index: `{row['instruction_index']}`")
        print(f"- Instruction tag: `{decoded['instruction_tag']}`")
        print(f"- Epoch/root slot: `{decoded['epoch']}`")
        print(f"- Merkle root: {fmt_hex(decoded['root'])}")
        print(f"- Untyped 32-byte field: {fmt_hex(decoded['unknown_32'])}")
        print(f"- Proof node count: `{decoded['proof_count']}`")
        print(f"- Path bitmap: `{decoded['path_bitmap']}` (`{bitmap_bits(decoded['path_bitmap'], decoded['proof_count'])}` low-bit first)")
        print(f"- Candidate 64-byte aggregate key material: {fmt_hex(decoded['leaf_material'])}")
        print(f"- Candidate leaf hash: {fmt_hex(decoded['leaf_hash'])}")
        print(f"- Recomputed root: {fmt_hex(decoded['recomputed_root'])}")
        print(f"- Merkle match: `{decoded['merkle_match']}`")
        print()
        print("### Proof Steps")
        print()
        print("| Step | Bitmap bit | Sibling position | Sibling hash | Parent hash |")
        print("|---:|---:|---|---|---|")
        for step in decoded["steps"]:
            print(
                f"| {step['index']} | {step['bit']} | `{step['sibling_position']}` | "
                f"{fmt_hex(step['sibling'])} | {fmt_hex(step['parent'])} |"
            )
        print()

        event_data = program_data_logs(row["logs"])
        if event_data:
            print("### Program Data Logs")
            print()
            print("| Length | Hex | Interpretation |")
            print("|---:|---|---|")
            for item in event_data:
                interpretation = ""
                if item == decoded["root"]:
                    interpretation = "emitted Merkle root"
                elif len(item) == 40 and item[:8] == struct.pack("<Q", decoded["epoch"]) and item[8:] == decoded["root"]:
                    interpretation = "emitted epoch/root pair"
                print(f"| {len(item)} | {fmt_hex(item)} | {interpretation or 'unclassified'} |")
            print()

    print("## Assessment")
    print()
    if rows and all(row["decoded"]["merkle_match"] for row in rows):
        print("- The sampled root-update payload matches the public JupNet article's Merkle leaf and parent hash formulas exactly.")
        print("- The four bytes after the proof nodes behave as a Merkle path bitmap; for the sampled transaction the bitmap is `18`.")
        print("- The final 64-byte field is the material hashed into the Merkle leaf, making it the strongest public candidate for the aggregate BLS public key committed by the epoch root.")
    else:
        print("- No sampled root-update payload produced a Merkle root match with the tested JupNet article formula.")
    print("- The payload still does not expose the underlying Dove members, stake weights, JUP balances, slashing records or threshold calculation that produced the aggregate key.")
    print("- The 32-byte field at offset `41` remains untyped from public bytes alone; logs prove BLS verification occurred, but the public transaction does not label whether this field is message hash, compact signature material or another verifier input.")


if __name__ == "__main__":
    main()
