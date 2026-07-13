#!/usr/bin/env python3
"""Analyze historical JupNet outbox root-update transactions."""

from __future__ import annotations

import argparse
import collections
import datetime as dt
import hashlib
import json
import struct
from pathlib import Path


ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
OUTBOX_PROGRAM = "jnoUtncGR9ZCCMixtys6Gzy5coTo6mnmUZuEHRQFTFV"
JUP_MINT = "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN"


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


def sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def block_time(value: int | None) -> str:
    if value is None:
        return "unknown"
    return dt.datetime.fromtimestamp(value, dt.timezone.utc).isoformat()


def recompute_root(aggregate_key: bytes, proof_nodes: list[bytes], path_bitmap: int) -> bytes:
    current = sha256(b"\x00" + aggregate_key)
    for index, sibling in enumerate(proof_nodes):
        sibling_on_left = bool((path_bitmap >> index) & 1)
        left = sibling if sibling_on_left else current
        right = current if sibling_on_left else sibling
        current = sha256(b"\x01" + left + right)
    return current


def decode_update_payload(raw: bytes) -> dict | None:
    if len(raw) != 305:
        return None
    proof_count = struct.unpack("<I", raw[73:77])[0]
    proof_start = 77
    proof_end = proof_start + proof_count * 32
    if proof_count == 0 or proof_end + 68 != len(raw):
        return None
    proof_nodes = [raw[proof_start + index * 32 : proof_start + (index + 1) * 32] for index in range(proof_count)]
    path_bitmap = struct.unpack("<I", raw[proof_end : proof_end + 4])[0]
    aggregate_key = raw[proof_end + 4 :]
    recomputed = recompute_root(aggregate_key, proof_nodes, path_bitmap)
    return {
        "tag": raw[0],
        "epoch": struct.unpack("<Q", raw[1:9])[0],
        "root": raw[9:41],
        "compact_verifier_field": raw[41:73],
        "proof_count": proof_count,
        "proof_nodes": proof_nodes,
        "path_bitmap": path_bitmap,
        "aggregate_key": aggregate_key,
        "leaf_hash": sha256(b"\x00" + aggregate_key),
        "recomputed_root": recomputed,
        "root_match": recomputed == raw[9:41],
    }


def decode_inner_verifier(raw: bytes) -> dict | None:
    # Inner VerifyOutboxMessage payload shape established in the field-map pass.
    if len(raw) != 337:
        return None
    proof_count = struct.unpack("<I", raw[173:177])[0]
    if proof_count == 0 or 177 + proof_count * 32 != len(raw):
        return None
    aggregate_key = raw[73:137]
    proof_nodes = [raw[177 + index * 32 : 177 + (index + 1) * 32] for index in range(proof_count)]
    path_bitmap = struct.unpack("<I", raw[169:173])[0]
    return {
        "epoch": struct.unpack("<Q", raw[65:73])[0],
        "aggregate_key": aggregate_key,
        "signature_field": raw[137:169],
        "path_bitmap": path_bitmap,
        "proof_count": proof_count,
        "root": recompute_root(aggregate_key, proof_nodes, path_bitmap),
    }


def all_account_keys(tx: dict) -> set[str]:
    keys = set()
    for key in tx.get("transaction", {}).get("message", {}).get("accountKeys") or []:
        keys.add(key["pubkey"] if isinstance(key, dict) else key)
    return keys


def validator_related_keys(base: Path) -> dict[str, str]:
    keys = {}
    votes = (load(base / "getVoteAccounts.json").get("result") or {})
    for row in (votes.get("current") or []) + (votes.get("delinquent") or []):
        keys[row["nodePubkey"]] = "validator node"
        keys[row["votePubkey"]] = "vote account"
    for item in load(base / "getProgramAccounts-Stake.json").get("result") or []:
        keys[item["pubkey"]] = "stake account"
    return keys


def transaction_files(base: Path) -> list[Path]:
    paths = {
        path.name: path
        for path in [
            *base.glob("solana-mainnet-outbox-history-tx-*.json"),
            *base.glob("solana-mainnet-outbox-tx-*.json"),
        ]
    }
    return [paths[name] for name in sorted(paths)]


def history_rows(base: Path) -> tuple[list[dict], list[dict]]:
    update_rows = []
    verifier_rows = []
    watched = {"canonical JUP mint": JUP_MINT, **validator_related_keys(base)}
    watched_raw = {}
    for label, value in watched.items():
        try:
            watched_raw[label] = b58decode(value)
        except ValueError:
            continue
    for path in transaction_files(base):
        tx = load(path).get("result")
        if not tx:
            continue
        keys = all_account_keys(tx)
        key_hits = [label for label, value in watched.items() if value in keys]
        logs = tx.get("meta", {}).get("logMessages") or []
        update_logs = [line for line in logs if "UpdateMerkleRoot" in line or "Signature verified" in line or "advance_epoch_root" in line]
        message = tx.get("transaction", {}).get("message", {})
        for index, ix in enumerate(message.get("instructions") or []):
            if ix.get("programId") != OUTBOX_PROGRAM:
                continue
            raw = b58decode(ix.get("data") or "") if ix.get("data") else b""
            payload_hits = [label for label, needle in watched_raw.items() if needle in raw]
            update = decode_update_payload(raw)
            if update:
                update_rows.append(
                    {
                        "file": path.name,
                        "slot": tx.get("slot"),
                        "block_time": tx.get("blockTime"),
                        "signature": (tx.get("transaction", {}).get("signatures") or [""])[0],
                        "instruction_index": index,
                        "raw": raw,
                        "logs": update_logs,
                        "key_hits": key_hits,
                        "payload_hits": payload_hits,
                        **update,
                    }
                )
            verifier = decode_inner_verifier(raw)
            if verifier:
                verifier_rows.append(
                    {
                        "file": path.name,
                        "slot": tx.get("slot"),
                        "block_time": tx.get("blockTime"),
                        "signature": (tx.get("transaction", {}).get("signatures") or [""])[0],
                        "instruction_index": index,
                        "key_hits": key_hits,
                        "payload_hits": payload_hits,
                        **verifier,
                    }
                )
        for group in tx.get("meta", {}).get("innerInstructions") or []:
            for inner_index, ix in enumerate(group.get("instructions") or []):
                if ix.get("programId") != OUTBOX_PROGRAM:
                    continue
                raw = b58decode(ix.get("data") or "") if ix.get("data") else b""
                payload_hits = [label for label, needle in watched_raw.items() if needle in raw]
                verifier = decode_inner_verifier(raw)
                if verifier:
                    verifier_rows.append(
                        {
                            "file": path.name,
                            "slot": tx.get("slot"),
                            "block_time": tx.get("blockTime"),
                            "signature": (tx.get("transaction", {}).get("signatures") or [""])[0],
                            "instruction_index": f"inner:{group.get('index')}:{inner_index}",
                            "key_hits": key_hits,
                            "payload_hits": payload_hits,
                            **verifier,
                        }
                    )
    return update_rows, verifier_rows


def current_validator_summary(base: Path) -> dict:
    votes = (load(base / "getVoteAccounts.json").get("result") or {})
    current_votes = votes.get("current") or []
    stake_accounts = load(base / "getProgramAccounts-Stake.json").get("result") or []
    stakes = []
    for account in stake_accounts:
        try:
            stakes.append(int(account["account"]["data"]["parsed"]["info"]["stake"]["delegation"]["stake"]))
        except (KeyError, TypeError, ValueError):
            continue
    return {
        "current_vote_accounts": len(current_votes),
        "stake_accounts": len(stake_accounts),
        "unique_delegated_stakes": sorted(set(stakes)),
    }


def fmt_hex(value: bytes, limit: int | None = None) -> str:
    text = value.hex()
    if limit and len(text) > limit:
        text = text[:limit] + "..."
    return f"`{text}`"


def fmt(values: list[str], empty: str = "`None`") -> str:
    if not values:
        return empty
    return "<br>".join(f"`{value}`" for value in values)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot_dir")
    args = parser.parse_args()
    base = Path(args.snapshot_dir)

    update_rows, verifier_rows = history_rows(base)
    files = transaction_files(base)
    root_counter = collections.Counter(row["root"].hex() for row in update_rows)
    aggregate_counter = collections.Counter(row["aggregate_key"].hex() for row in update_rows)
    compact_counter = collections.Counter(row["compact_verifier_field"].hex() for row in update_rows)
    verifier_aggregate_counter = collections.Counter(row["aggregate_key"].hex() for row in verifier_rows)
    verifier_root_counter = collections.Counter(row["root"].hex() for row in verifier_rows)
    validator_summary = current_validator_summary(base)
    any_security_hits = [row for row in update_rows + verifier_rows if row["key_hits"] or row["payload_hits"]]

    print("# Outbox Root History Analysis")
    print()
    print("## Scope")
    print()
    print(f"- Snapshot: `{base}`")
    print(f"- Transaction files scanned: `{len(files)}`")
    print(f"- Root-update payloads decoded: `{len(update_rows)}`")
    print(f"- Inner verifier payloads decoded: `{len(verifier_rows)}`")
    print(f"- Current vote accounts in snapshot: `{validator_summary['current_vote_accounts']}`")
    print(f"- Current stake accounts in snapshot: `{validator_summary['stake_accounts']}`")
    print(f"- Current unique delegated native stake values: `{validator_summary['unique_delegated_stakes']}`")
    print(f"- Root/update or verifier rows with canonical JUP / validator / vote / stake key hits: `{len(any_security_hits)}`")
    print()

    print("## Root Update Timeline")
    print()
    if update_rows:
        print("| Time | Slot | Epoch | Root | Aggregate key | Compact verifier field | Bitmap | Proof nodes | Root match | Key hits |")
        print("|---|---:|---:|---|---|---|---:|---:|---|---|")
        for row in sorted(update_rows, key=lambda item: (item["slot"] or 0, item["signature"])):
            print(
                f"| `{block_time(row['block_time'])}` | {row['slot']} | {row['epoch']} | "
                f"{fmt_hex(row['root'], 16)} | {fmt_hex(row['aggregate_key'], 16)} | "
                f"{fmt_hex(row['compact_verifier_field'], 16)} | {row['path_bitmap']} | {row['proof_count']} | "
                f"`{row['root_match']}` | {fmt(row['key_hits'] + row['payload_hits'])} |"
            )
    else:
        print("- No root-update payloads decoded.")
    print()

    print("## Root Update Groups")
    print()
    print("| Group | Unique count | Values |")
    print("|---|---:|---|")
    print(f"| Roots | {len(root_counter)} | {fmt([f'{value}: {count}' for value, count in root_counter.items()])} |")
    print(f"| Aggregate keys | {len(aggregate_counter)} | {fmt([f'{value[:32]}...: {count}' for value, count in aggregate_counter.items()])} |")
    print(f"| Compact verifier fields | {len(compact_counter)} | {fmt([f'{value[:32]}...: {count}' for value, count in compact_counter.items()])} |")
    print()

    print("## Verifier Context Groups")
    print()
    print("| Group | Unique count | Values |")
    print("|---|---:|---|")
    print(f"| Verifier recomputed roots | {len(verifier_root_counter)} | {fmt([f'{value}: {count}' for value, count in verifier_root_counter.items()])} |")
    print(f"| Verifier aggregate keys | {len(verifier_aggregate_counter)} | {fmt([f'{value[:32]}...: {count}' for value, count in verifier_aggregate_counter.items()])} |")
    print()

    print("## Change Signals")
    print()
    if len(root_counter) > 1 or len(aggregate_counter) > 1 or len(compact_counter) > 1:
        print("- Root-update material changed within the fetched history window.")
    elif update_rows:
        print("- Root-update material was stable within the fetched history window.")
    else:
        print("- No root-update material was available to compare.")
    if len(verifier_aggregate_counter) > 1:
        print("- Verifier aggregate-key material changed within ordinary verification payloads.")
    elif verifier_rows:
        print("- Verifier aggregate-key material was stable within ordinary verification payloads.")
    else:
        print("- No ordinary verifier payloads were decoded.")
    if any_security_hits:
        print("- At least one decoded row exposed watched JUP/validator/vote/stake key material.")
    else:
        print("- No decoded root-update or verifier row exposed canonical JUP, current validator, vote or stake keys.")
    print()

    print("## Assessment")
    print()
    print("- This history pass compares public root/update proof material over a wider outbox transaction window.")
    print("- It can identify changes in epoch root, aggregate key, compact verifier field and proof path, but it only correlates against the current validator/stake snapshot unless older validator snapshots are supplied separately.")
    print("- A stable root/aggregate-key history does not disprove JUP utility, but it gives no public evidence of live stake-weight churn.")
    print("- A future change that introduces JUP/validator/stake key material or root/key changes around validator/stake changes would be a high-value signal.")


if __name__ == "__main__":
    main()
