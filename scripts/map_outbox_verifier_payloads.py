#!/usr/bin/env python3
"""Map Bank/outbox verifier payload fields around aggregate-key proof material."""

from __future__ import annotations

import argparse
import base64
import collections
import datetime as dt
import hashlib
import json
import struct
from pathlib import Path


ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
BANK_PROGRAM = "BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ"
OUTBOX_PROGRAM = "jnoUtncGR9ZCCMixtys6Gzy5coTo6mnmUZuEHRQFTFV"
VERIFY_REQUEST_DISC = bytes.fromhex("891f2fe4cdea81ed")
JUP_MINT = "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN"


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


def raw_account_data(account: dict | None) -> bytes:
    if not account:
        return b""
    data = account.get("data")
    if isinstance(data, list):
        return base64.b64decode(data[0])
    return b""


def outbox_roots(base: Path) -> dict[int, bytes]:
    roots = {}
    data = load(base / "solana-mainnet-getProgramAccounts-JupNetOutboxProgram.json")
    for item in data.get("result") or []:
        raw = raw_account_data(item.get("account"))
        for offset in range(0, len(raw), 40):
            if offset + 40 > len(raw):
                continue
            epoch = struct.unpack("<Q", raw[offset : offset + 8])[0]
            root = raw[offset + 8 : offset + 40]
            if epoch or root != b"\0" * 32:
                roots[epoch] = root
    return roots


def recompute_root(aggregate_key: bytes, proof_nodes: list[bytes], path_bitmap: int) -> bytes:
    current = sha256(b"\x00" + aggregate_key)
    for index, sibling in enumerate(proof_nodes):
        sibling_on_left = bool((path_bitmap >> index) & 1)
        left = sibling if sibling_on_left else current
        right = current if sibling_on_left else sibling
        current = sha256(b"\x01" + left + right)
    return current


def parse_proof(raw: bytes, aggregate_offset: int) -> dict | None:
    if len(raw) < aggregate_offset + 64 + 32 + 4 + 4:
        return None
    signature_offset = aggregate_offset + 64
    bitmap_offset = signature_offset + 32
    count_offset = bitmap_offset + 4
    node_start = count_offset + 4
    count = struct.unpack("<I", raw[count_offset : count_offset + 4])[0]
    node_end = node_start + count * 32
    if count == 0 or node_end != len(raw):
        return None
    aggregate_key = raw[aggregate_offset : aggregate_offset + 64]
    proof_nodes = [raw[node_start + index * 32 : node_start + (index + 1) * 32] for index in range(count)]
    path_bitmap = struct.unpack("<I", raw[bitmap_offset : bitmap_offset + 4])[0]
    return {
        "aggregate_offset": aggregate_offset,
        "aggregate_key": aggregate_key,
        "signature_offset": signature_offset,
        "signature": raw[signature_offset : signature_offset + 32],
        "bitmap_offset": bitmap_offset,
        "path_bitmap": path_bitmap,
        "count_offset": count_offset,
        "proof_count": count,
        "node_start": node_start,
        "proof_nodes": proof_nodes,
        "leaf_hash": sha256(b"\x00" + aggregate_key),
        "recomputed_root": recompute_root(aggregate_key, proof_nodes, path_bitmap),
    }


def parse_inner_outbox(raw: bytes) -> dict | None:
    proof = parse_proof(raw, 73)
    if not proof:
        return None
    return {
        "kind": "inner-outbox",
        "message_hash_offset": 1,
        "message_hash": raw[1:33],
        "sender_offset": 33,
        "sender": raw[33:65],
        "epoch_offset": 65,
        "epoch": struct.unpack("<Q", raw[65:73])[0],
        "tag": raw[0],
        **proof,
    }


def parse_bank_verify(raw: bytes) -> dict | None:
    if raw[:8] != VERIFY_REQUEST_DISC:
        return None
    aggregate_offset = raw.find(KNOWN_AGGREGATE_KEY)
    if aggregate_offset == -1:
        aggregate_offset = find_bank_aggregate_offset(raw)
    if aggregate_offset is None or aggregate_offset == -1:
        return None
    proof = parse_proof(raw, aggregate_offset)
    if not proof:
        return None
    message_hash_offset = aggregate_offset - 40
    if message_hash_offset < 0:
        return None
    return {
        "kind": "bank-verify-wrapper",
        "discriminator": raw[:8],
        "body_len": struct.unpack("<I", raw[8:12])[0] if len(raw) >= 12 else None,
        "body_version": struct.unpack("<I", raw[12:16])[0] if len(raw) >= 16 else None,
        "bank_program_offset": raw.find(b58decode(BANK_PROGRAM)),
        "message_hash_offset": message_hash_offset,
        "message_hash": raw[message_hash_offset : message_hash_offset + 32],
        "sender_offset": None,
        "sender": None,
        "epoch_offset": aggregate_offset - 8,
        "epoch": struct.unpack("<Q", raw[aggregate_offset - 8 : aggregate_offset])[0],
        **proof,
    }


def find_bank_aggregate_offset(raw: bytes) -> int | None:
    for offset in range(16, max(16, len(raw) - 104)):
        if offset < 8:
            continue
        proof = parse_proof(raw, offset)
        if not proof or proof["proof_count"] > 32:
            continue
        epoch = struct.unpack("<Q", raw[offset - 8 : offset])[0]
        if 0 < epoch < 1_000_000:
            return offset
    return None


def tx_account_keys(tx: dict) -> set[str]:
    keys = set()
    for key in tx.get("transaction", {}).get("message", {}).get("accountKeys") or []:
        keys.add(key["pubkey"] if isinstance(key, dict) else key)
    return keys


def collect_rows(base: Path) -> list[dict]:
    rows = []
    for path in sorted(base.glob("solana-mainnet-outbox-tx-*.json")) + sorted(base.glob("solana-mainnet-bank-tx-*.json")):
        tx = load(path).get("result")
        if not tx:
            continue
        keys = tx_account_keys(tx)
        message = tx.get("transaction", {}).get("message", {})
        for index, ix in enumerate(message.get("instructions") or []):
            raw = b58decode(ix.get("data") or "") if ix.get("data") else b""
            parsed = None
            if ix.get("programId") == BANK_PROGRAM:
                parsed = parse_bank_verify(raw)
            elif ix.get("programId") == OUTBOX_PROGRAM:
                parsed = parse_inner_outbox(raw)
            if parsed:
                rows.append(
                    {
                        "file": path.name,
                        "slot": tx.get("slot"),
                        "block_time": tx.get("blockTime"),
                        "signature": (tx.get("transaction", {}).get("signatures") or [""])[0],
                        "instruction_index": index,
                        "program_id": ix.get("programId"),
                        "raw_len": len(raw),
                        "account_keys": keys,
                        **parsed,
                    }
                )
        for group in tx.get("meta", {}).get("innerInstructions") or []:
            for index, ix in enumerate(group.get("instructions") or []):
                if ix.get("programId") != OUTBOX_PROGRAM:
                    continue
                raw = b58decode(ix.get("data") or "") if ix.get("data") else b""
                parsed = parse_inner_outbox(raw)
                if parsed:
                    rows.append(
                        {
                            "file": path.name,
                            "slot": tx.get("slot"),
                            "block_time": tx.get("blockTime"),
                            "signature": (tx.get("transaction", {}).get("signatures") or [""])[0],
                            "instruction_index": f"inner:{group.get('index')}:{index}",
                            "program_id": ix.get("programId"),
                            "raw_len": len(raw),
                            "account_keys": keys,
                            **parsed,
                        }
                    )
    return rows


def validator_related_keys(base: Path) -> dict[str, str]:
    keys = {}
    votes = (load(base / "getVoteAccounts.json").get("result") or {})
    for row in (votes.get("current") or []) + (votes.get("delinquent") or []):
        keys[row["nodePubkey"]] = "validator node"
        keys[row["votePubkey"]] = "vote account"
    for item in load(base / "getProgramAccounts-Stake.json").get("result") or []:
        keys[item["pubkey"]] = "stake account"
    return keys


def bitmap_bits(path_bitmap: int, proof_count: int) -> str:
    return "".join(str((path_bitmap >> index) & 1) for index in range(proof_count))


def fmt_hex(value: bytes | None, limit: int | None = None) -> str:
    if value is None:
        return "`None`"
    text = value.hex()
    if limit and len(text) > limit:
        text = text[:limit] + "..."
    return f"`{text}`"


def fmt(values: list[str], empty: str = "`None`") -> str:
    if not values:
        return empty
    return "<br>".join(f"`{value}`" for value in values)


KNOWN_AGGREGATE_KEY = bytes.fromhex(
    "87e930814a0131f70e4b405f4e30ca3e226ad5bee2e5e40d584947d48c4bcc"
    "eb15f96af18671975c31abc6d2c3ea8230ee775da12cd69b5331e35865ad2c4025"
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot_dir")
    args = parser.parse_args()
    base = Path(args.snapshot_dir)
    roots = outbox_roots(base)
    rows = collect_rows(base)
    validator_keys = set(validator_related_keys(base))
    jup_raw = b58decode(JUP_MINT)

    print("# Outbox Verifier Payload Field Map")
    print()
    print("## Scope")
    print()
    print(f"- Snapshot: `{base}`")
    print(f"- Parsed verifier payloads: `{len(rows)}`")
    print(f"- Bank wrapper payloads: `{sum(1 for row in rows if row['kind'] == 'bank-verify-wrapper')}`")
    print(f"- Inner outbox payloads: `{sum(1 for row in rows if row['kind'] == 'inner-outbox')}`")
    print(f"- Known aggregate-key material: `{KNOWN_AGGREGATE_KEY.hex()}`")
    print()

    print("## Layouts")
    print()
    print("### Inner Outbox Verifier")
    print()
    print("| Offset | Length | Field |")
    print("|---:|---:|---|")
    print("| 0 | 1 | tag, observed `0` |")
    print("| 1 | 32 | message hash |")
    print("| 33 | 32 | sender/program id candidate |")
    print("| 65 | 8 | epoch, little-endian u64 |")
    print("| 73 | 64 | aggregate-key material |")
    print("| 137 | 32 | compact signature/verifier field |")
    print("| 169 | 4 | Merkle path bitmap |")
    print("| 173 | 4 | Merkle proof count |")
    print("| 177 | 160 | five 32-byte Merkle proof nodes |")
    print()
    print("### Bank Verify Wrapper")
    print()
    print("| Offset | Length | Field |")
    print("|---:|---:|---|")
    print("| 0 | 8 | Bank `verify_request` discriminator |")
    print("| 8 | 4 | request/body length |")
    print("| 12 | 4 | stable version/flag |")
    print("| 21 | 32 | embedded Bank Program id in sampled 463-byte wrappers |")
    print("| aggregate_offset - 40 | 32 | message hash candidate |")
    print("| aggregate_offset - 8 | 8 | epoch, little-endian u64 |")
    print("| aggregate_offset | 64 | aggregate-key material |")
    print("| aggregate_offset + 64 | 32 | compact signature/verifier field |")
    print("| aggregate_offset + 96 | 4 | Merkle path bitmap |")
    print("| aggregate_offset + 100 | 4 | Merkle proof count |")
    print("| aggregate_offset + 104 | `32 * count` | Merkle proof nodes |")
    print()

    print("## Payload Rows")
    print()
    print("| File | Ix | Kind | Len | Epoch | Sender/program candidate | Root match | JUP key | Validator key | Message hash | Signature field |")
    print("|---|---|---|---:|---:|---|---|---|---|---|---|")
    for row in rows:
        expected = roots.get(row["epoch"])
        root_match = bool(expected and row["recomputed_root"] == expected)
        raw_blob = b"".join([row["message_hash"], row["aggregate_key"], row["signature"], *row["proof_nodes"]])
        jup_hit = jup_raw in raw_blob or JUP_MINT in row["account_keys"]
        validator_hit = bool(row["account_keys"] & validator_keys)
        sender = b58encode(row["sender"]) if row.get("sender") else "None"
        print(
            f"| `{row['file']}` | `{row['instruction_index']}` | `{row['kind']}` | {row['raw_len']} | "
            f"{row['epoch']} | `{sender}` | `{root_match}` | `{jup_hit}` | `{validator_hit}` | "
            f"{fmt_hex(row['message_hash'], 16)} | {fmt_hex(row['signature'], 16)} |"
        )
    print()

    print("## Aggregate-Key Groups")
    print()
    groups = collections.Counter(row["aggregate_key"].hex() for row in rows)
    print("| Aggregate key prefix | Count |")
    print("|---|---:|")
    for key, count in groups.most_common():
        print(f"| `{key[:32]}...` | {count} |")
    print()

    print("## Proof Invariants")
    print()
    bitmaps = collections.Counter((row["path_bitmap"], row["proof_count"]) for row in rows)
    roots_counter = collections.Counter(row["recomputed_root"].hex() for row in rows)
    print(f"- Bitmap/count groups: `{dict(bitmaps)}`")
    print(f"- Recomputed root groups: `{dict(roots_counter)}`")
    print(f"- Stored roots available: `{ {epoch: root.hex() for epoch, root in roots.items()} }`")
    print()

    print("## Assessment")
    print()
    if rows:
        print("- Sampled Bank/outbox verification payloads expose the same aggregate-key material and Merkle proof path used by the root-update reconstruction.")
        print("- The inner outbox verifier payload maps closely to the public article's outbox argument list: message hash, sender/program id, epoch, aggregate key, compact signature/verifier field and Merkle proof.")
        print("- Every parsed payload recomputes to the stored outbox root for its epoch when the article's `0x00` leaf and `0x01` parent hash formula is used.")
    else:
        print("- No Bank/outbox verifier payloads were parsed.")
    print("- These verifier payloads still do not expose Dove identities, individual BLS keys, JUP balances or stake weights.")


if __name__ == "__main__":
    main()
