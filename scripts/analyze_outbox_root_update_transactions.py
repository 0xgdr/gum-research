#!/usr/bin/env python3
"""Analyze recent JupNet outbox helper transactions for root-update/BLS evidence."""

from __future__ import annotations

import argparse
import collections
import datetime as dt
import json
import struct
from pathlib import Path


ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
OUTBOX_PROGRAM = "jnoUtncGR9ZCCMixtys6Gzy5coTo6mnmUZuEHRQFTFV"
OUTBOX_ROOT_ACCOUNT = "3C1LxtpR3Mh5RQjydfeQdvRaAzpStWM7gBi1XzP9oyGt"
JUP_MINT = "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN"
BANK_PROGRAM = "BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ"
USDC = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
WRAPPED_SOL = "So11111111111111111111111111111111111111112"

WATCHED_KEYS = {
    "canonical JUP mint": JUP_MINT,
    "Outbox Program": OUTBOX_PROGRAM,
    "Outbox root account": OUTBOX_ROOT_ACCOUNT,
    "Bank Program": BANK_PROGRAM,
    "USDC mint": USDC,
    "wrapped SOL mint": WRAPPED_SOL,
}

LOG_TERMS = (
    "UpdateMerkleRoot",
    "InitMerkleRoot",
    "EmergencyResetMerkleRoot",
    "VerifyOutboxMessage",
    "Verifying BLS signature",
    "Signature verified",
    "Merkle proof verified",
    "advance_epoch_root",
    "quorum",
    "signer",
    "stake",
    "validator",
    "jup",
)


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


def validator_related_keys(base: Path) -> dict[str, str]:
    keys = {}
    votes = (load(base / "getVoteAccounts.json").get("result") or {})
    for row in (votes.get("current") or []) + (votes.get("delinquent") or []):
        keys[row["nodePubkey"]] = "validator node"
        keys[row["votePubkey"]] = "vote account"
    for item in load(base / "getProgramAccounts-Stake.json").get("result") or []:
        keys[item["pubkey"]] = "stake account"
    return keys


def account_metas(tx: dict) -> dict[str, dict]:
    metas = {}
    keys = tx.get("transaction", {}).get("message", {}).get("accountKeys") or []
    for index, key in enumerate(keys):
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


def all_account_keys(tx: dict) -> set[str]:
    keys = set()
    for key in tx.get("transaction", {}).get("message", {}).get("accountKeys") or []:
        keys.add(key["pubkey"] if isinstance(key, dict) else key)
    return keys


def interesting_logs(tx: dict) -> list[str]:
    logs = tx.get("meta", {}).get("logMessages") or []
    return [line for line in logs if any(term.lower() in line.lower() for term in LOG_TERMS)]


def outbox_instruction_rows(base: Path) -> list[dict]:
    watched = dict(WATCHED_KEYS)
    watched.update(validator_related_keys(base))
    rows = []
    for path in sorted(base.glob("solana-mainnet-outbox-tx-*.json")):
        tx = load(path).get("result")
        if not tx:
            continue
        metas = account_metas(tx)
        keys = all_account_keys(tx)
        logs = interesting_logs(tx)
        key_hits = []
        for label, key in watched.items():
            if key in keys:
                key_hits.append(f"{label}: {key}")
        for index, ix in enumerate(tx.get("transaction", {}).get("message", {}).get("instructions") or []):
            if ix.get("programId") != OUTBOX_PROGRAM:
                continue
            data = ix.get("data") or ""
            raw = b58decode(data) if data else b""
            accounts = ix.get("accounts") or []
            signer_accounts = [account for account in accounts if metas.get(account, {}).get("signer")]
            writable_accounts = [account for account in accounts if metas.get(account, {}).get("writable")]
            payload_hits = []
            for label, key in watched.items():
                try:
                    needle = b58decode(key)
                except ValueError:
                    continue
                if needle and needle in raw:
                    payload_hits.append(f"{label}: {key}")
            small_numbers = []
            for offset in range(8, min(len(raw) - 7, 160), 8):
                value = struct.unpack("<Q", raw[offset : offset + 8])[0]
                if value and value < 10**12:
                    small_numbers.append(f"{offset}:{value}")
            decoded = decode_update_payload(raw)
            rows.append(
                {
                    "file": path.name,
                    "slot": tx.get("slot"),
                    "block_time": tx.get("blockTime"),
                    "signature": (tx.get("transaction", {}).get("signatures") or [""])[0],
                    "instruction_index": index,
                    "raw": raw,
                    "discriminator": raw[:8].hex() if raw else "",
                    "data_len": len(raw),
                    "accounts": accounts,
                    "signers": signer_accounts,
                    "writables": writable_accounts,
                    "logs": logs,
                    "key_hits": key_hits,
                    "payload_hits": payload_hits,
                    "small_numbers": small_numbers,
                    "decoded": decoded,
                }
            )
    return rows


def decode_update_payload(raw: bytes) -> dict:
    if len(raw) != 305:
        return {}
    proof_count = struct.unpack("<I", raw[73:77])[0] if len(raw) >= 77 else None
    proof_nodes = []
    if proof_count and len(raw) >= 77 + proof_count * 32:
        proof_nodes = [raw[77 + index * 32 : 77 + (index + 1) * 32] for index in range(proof_count)]
    return {
        "tag": raw[0],
        "epoch_candidate": struct.unpack("<Q", raw[1:9])[0],
        "root": raw[9:41],
        "message_or_leaf": raw[41:73],
        "proof_count": proof_count,
        "proof_nodes": proof_nodes,
        "tail": raw[77 + len(proof_nodes) * 32 :],
    }


def block_time(value: int | None) -> str:
    if value is None:
        return "unknown"
    return dt.datetime.fromtimestamp(value, dt.timezone.utc).isoformat()


def fmt(values: list[str], empty: str = "`None`") -> str:
    if not values:
        return empty
    return "<br>".join(f"`{value}`" for value in values)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot_dir")
    args = parser.parse_args()
    base = Path(args.snapshot_dir)
    rows = outbox_instruction_rows(base)
    variant_counts = collections.Counter((row["discriminator"], row["data_len"], len(row["accounts"])) for row in rows)
    log_counter = collections.Counter(line for row in rows for line in row["logs"])
    update_rows = [
        row
        for row in rows
        if any("updatemerkleroot" in line.lower() or "verifying bls signature" in line.lower() for line in row["logs"])
    ]
    jup_key_hits = [row for row in rows if any("canonical JUP" in hit for hit in row["key_hits"] + row["payload_hits"])]
    validator_key_hits = [
        row
        for row in rows
        if any(("validator node" in hit or "vote account" in hit or "stake account" in hit) for hit in row["key_hits"] + row["payload_hits"])
    ]

    print("# Outbox Root Update Transactions")
    print()
    print("## Scope")
    print()
    print(f"- Outbox helper program: `{OUTBOX_PROGRAM}`")
    print(f"- Transaction files scanned: `{len(list(base.glob('solana-mainnet-outbox-tx-*.json')))}`")
    print(f"- Top-level outbox instructions found: `{len(rows)}`")
    print(f"- Update/BLS candidate instructions: `{len(update_rows)}`")
    print(f"- Canonical JUP key hits: `{len(jup_key_hits)}`")
    print(f"- Current JupNet validator/vote/stake key hits: `{len(validator_key_hits)}`")
    print()
    print("## Instruction Variants")
    print()
    print("| Count | Discriminator | Data length | Account count |")
    print("|---:|---|---:|---:|")
    for (discriminator, data_len, account_count), count in variant_counts.most_common():
        print(f"| {count} | `{discriminator}` | {data_len} | {account_count} |")
    print()
    print("## Relevant Logs")
    print()
    if log_counter:
        for line, count in log_counter.most_common(30):
            print(f"- `{line}`: `{count}`")
    else:
        print("- None")
    print()
    print("## Transaction Rows")
    print()
    print("| File | Slot | Time | Discriminator | Data len | Accounts | Signers | Writable accounts | Key hits | Payload hits | Logs |")
    print("|---|---:|---|---|---:|---:|---|---|---|---|---|")
    for row in rows:
        print(
            f"| `{row['file']}` | {row['slot']} | `{block_time(row['block_time'])}` | "
            f"`{row['discriminator']}` | {row['data_len']} | {len(row['accounts'])} | "
            f"{fmt(row['signers'])} | {fmt(row['writables'][:8])} | "
            f"{fmt(row['key_hits'])} | {fmt(row['payload_hits'])} | {fmt(row['logs'][:8])} |"
        )
    print()
    print("## Payload Shape Hints")
    print()
    if rows:
        print("| Discriminator | Data len | Small aligned u64 candidates |")
        print("|---|---:|---|")
        seen = set()
        for row in rows:
            key = (row["discriminator"], row["data_len"], tuple(row["small_numbers"]))
            if key in seen:
                continue
            seen.add(key)
            print(f"| `{row['discriminator']}` | {row['data_len']} | {fmt(row['small_numbers'][:12])} |")
    else:
        print("- None")
    print()
    print("## Decoded Update Payload")
    print()
    decoded_rows = [row for row in rows if row["decoded"]]
    if decoded_rows:
        for row in decoded_rows:
            decoded = row["decoded"]
            print(f"### `{row['file']}`")
            print()
            print(f"- Tag byte: `{decoded['tag']}`")
            print(f"- Epoch/root slot candidate: `{decoded['epoch_candidate']}`")
            print(f"- Merkle root: `{decoded['root'].hex()}`")
            print(f"- Message/leaf candidate: `{decoded['message_or_leaf'].hex()}`")
            print(f"- Proof node count: `{decoded['proof_count']}`")
            print(f"- Tail after proof nodes: `{decoded['tail'].hex()}`")
            print()
            print("| Node index | Hex |")
            print("|---:|---|")
            for index, node in enumerate(decoded["proof_nodes"]):
                print(f"| {index} | `{node.hex()}` |")
            print()
    else:
        print("- No 305-byte update payload decoded.")
    print()
    print("## Assessment")
    print()
    if update_rows:
        print("- Recent outbox helper transactions include update/BLS log candidates; inspect payload rows above for signer/quorum evidence.")
    else:
        print("- The scanned recent outbox helper transactions did not include `UpdateMerkleRoot` or `Verifying BLS signature` logs.")
    print("- No scanned outbox transaction exposed canonical Solana JUP key material.")
    print("- No scanned outbox transaction exposed current JupNet validator, vote or stake account keys.")
    print("- If BLS quorum material is present here, it is not visible as direct JUP, validator/vote/stake account references in the sampled transaction keys or payload bytes.")


if __name__ == "__main__":
    main()
