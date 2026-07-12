#!/usr/bin/env python3
"""Analyze accounts owned by inferred Solana-side JupNet inbox/outbox helper programs."""

from __future__ import annotations

import argparse
import base64
import collections
import hashlib
import json
import struct
from pathlib import Path


ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
JUP_MINT = "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN"
BANK_PROGRAM = "BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ"
INBOX_PROGRAM = "JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw"
OUTBOX_PROGRAM = "jnoUtncGR9ZCCMixtys6Gzy5coTo6mnmUZuEHRQFTFV"
USDC = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
WRAPPED_SOL = "So11111111111111111111111111111111111111112"

SEARCH_TERMS = (
    "jup",
    "stake",
    "validator",
    "vote",
    "quorum",
    "signer",
    "weight",
    "fee",
    "reward",
    "slash",
    "bls",
    "bn254",
    "merkle",
    "proof",
    "root",
    "epoch",
    "authority",
    "inbox",
    "outbox",
)


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


def raw_account_data(account: dict | None) -> bytes:
    if not account:
        return b""
    data = account.get("data")
    if isinstance(data, list):
        return base64.b64decode(data[0])
    return b""


def printable_strings(raw: bytes, min_len: int = 4) -> list[str]:
    allowed = set(range(0x20, 0x7F))
    out = []
    current = bytearray()
    for byte in raw:
        if byte in allowed:
            current.append(byte)
            continue
        if len(current) >= min_len:
            out.append(current.decode("ascii", errors="ignore"))
        current.clear()
    if len(current) >= min_len:
        out.append(current.decode("ascii", errors="ignore"))
    return out


def validator_related_keys(base: Path) -> dict[str, str]:
    keys = {}
    votes = (load(base / "getVoteAccounts.json").get("result") or {})
    for row in (votes.get("current") or []) + (votes.get("delinquent") or []):
        keys[row["nodePubkey"]] = "validator node"
        keys[row["votePubkey"]] = "vote account"
    for item in load(base / "getProgramAccounts-Stake.json").get("result") or []:
        keys[item["pubkey"]] = "stake account"
    return keys


def program_rows(base: Path, label: str, program: str) -> list[dict]:
    data = load(base / f"solana-mainnet-getProgramAccounts-{label}.json")
    items = data.get("result") or []
    related = validator_related_keys(base)
    watched = {
        "canonical JUP mint": JUP_MINT,
        "Bank Program": BANK_PROGRAM,
        "Inbox Program": INBOX_PROGRAM,
        "Outbox Program": OUTBOX_PROGRAM,
        "USDC mint": USDC,
        "wrapped SOL mint": WRAPPED_SOL,
        **related,
    }
    rows = []
    for item in items:
        pubkey = item["pubkey"]
        account = item["account"]
        raw = raw_account_data(account)
        strings = printable_strings(raw)
        term_hits = collections.defaultdict(list)
        for text in strings:
            lower = text.lower()
            for term in SEARCH_TERMS:
                if term in lower and len(term_hits[term]) < 4:
                    term_hits[term].append(text[:140])
        key_hits = []
        for name, key in watched.items():
            try:
                key_raw = b58decode(key)
            except ValueError:
                continue
            if key_raw in raw or key.encode() in raw:
                key_hits.append(f"{name}: {key}")
        likely_pubkeys = []
        for offset in range(8, max(8, len(raw) - 31), 32):
            chunk = raw[offset : offset + 32]
            if chunk and chunk != b"\0" * 32:
                likely_pubkeys.append(f"{offset}:{b58encode(chunk)}")
        small_numbers = []
        for offset in range(8, min(len(raw) - 7, 128), 8):
            value = struct.unpack("<Q", raw[offset : offset + 8])[0]
            if value and value < 10**12:
                small_numbers.append(f"{offset}:{value}")
        root_entries = []
        if label == "JupNetOutboxProgram" and len(raw) % 40 == 0:
            for offset in range(0, len(raw), 40):
                epoch = struct.unpack("<Q", raw[offset : offset + 8])[0]
                root = raw[offset + 8 : offset + 40]
                if epoch or root != b"\0" * 32:
                    root_entries.append(f"offset {offset}: epoch {epoch}, root {root.hex()}")
        inbox_counter = None
        if label == "JupNetInboxProgram" and len(raw) >= 8:
            inbox_counter = struct.unpack("<Q", raw[:8])[0]
        rows.append(
            {
                "program": program,
                "label": label,
                "pubkey": pubkey,
                "owner": account.get("owner"),
                "space": account.get("space"),
                "lamports": account.get("lamports"),
                "raw": raw,
                "sha256": hashlib.sha256(raw).hexdigest() if raw else None,
                "discriminator": raw[:8].hex() if len(raw) >= 8 else None,
                "key_hits": key_hits,
                "term_hits": dict(term_hits),
                "strings": strings,
                "likely_pubkeys": likely_pubkeys,
                "small_numbers": small_numbers,
                "root_entries": root_entries,
                "inbox_counter": inbox_counter,
            }
        )
    return rows


def signature_count(base: Path, label: str) -> int:
    data = load(base / f"solana-mainnet-getSignaturesForAddress-{label}.json")
    return len(data.get("result") or [])


def fmt(values: list[str], empty: str = "`None`") -> str:
    if not values:
        return empty
    return "<br>".join(f"`{value}`" for value in values)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot_dir")
    args = parser.parse_args()
    base = Path(args.snapshot_dir)

    rows = []
    rows.extend(program_rows(base, "JupNetInboxProgram", INBOX_PROGRAM))
    rows.extend(program_rows(base, "JupNetOutboxProgram", OUTBOX_PROGRAM))

    jup_hits = [row for row in rows if any("canonical JUP" in hit for hit in row["key_hits"])]
    validator_hits = [
        row
        for row in rows
        if any(("validator node" in hit or "vote account" in hit or "stake account" in hit) for hit in row["key_hits"])
    ]
    class_counts = collections.Counter((row["label"], row["space"], row["discriminator"]) for row in rows)

    print("# JupNet Helper Program Accounts")
    print()
    print("## Scope")
    print()
    print(f"- Inbox helper program: `{INBOX_PROGRAM}`")
    print(f"- Outbox helper program: `{OUTBOX_PROGRAM}`")
    print(f"- Inbox-owned accounts fetched: `{sum(1 for row in rows if row['label'] == 'JupNetInboxProgram')}`")
    print(f"- Outbox-owned accounts fetched: `{sum(1 for row in rows if row['label'] == 'JupNetOutboxProgram')}`")
    print(f"- Inbox program signature-window count: `{signature_count(base, 'JupNetInboxProgram')}`")
    print(f"- Outbox program signature-window count: `{signature_count(base, 'JupNetOutboxProgram')}`")
    print(f"- Accounts with canonical JUP hits: `{len(jup_hits)}`")
    print(f"- Accounts with current JupNet validator/vote/stake key hits: `{len(validator_hits)}`")
    print()
    print("## Layout Groups")
    print()
    print("| Program | Space | Discriminator | Count |")
    print("|---|---:|---|---:|")
    for (label, space, discriminator), count in class_counts.most_common():
        print(f"| `{label}` | {space} | `{discriminator}` | {count} |")
    print()
    print("## Account Rows")
    print()
    print("| Program | Account | Space | Discriminator | SHA256 | Key hits | Term hits | Likely pubkey chunks | Small numbers |")
    print("|---|---|---:|---|---|---|---|---|---|")
    for row in sorted(rows, key=lambda item: (item["label"], item["space"] or 0, item["pubkey"])):
        term_hits = []
        for term, values in row["term_hits"].items():
            term_hits.append(f"{term}: {', '.join(values[:2])}")
        print(
            f"| `{row['label']}` | `{row['pubkey']}` | {row['space']} | "
            f"`{row['discriminator']}` | `{row['sha256']}` | "
            f"{fmt(row['key_hits'])} | {fmt(term_hits)} | "
            f"{fmt(row['likely_pubkeys'][:8])} | {fmt(row['small_numbers'][:8])} |"
        )
    print()
    print("## Decoded State Hints")
    print()
    for row in sorted(rows, key=lambda item: item["label"]):
        if row["inbox_counter"] is not None:
            print(f"- `{row['pubkey']}` inbox counter/value candidate: `{row['inbox_counter']}`")
        if row["root_entries"]:
            print(f"- `{row['pubkey']}` outbox Merkle root entries:")
            for entry in row["root_entries"]:
                print(f"  - `{entry}`")
    if not any(row["root_entries"] or row["inbox_counter"] is not None for row in rows):
        print("- None")
    print()
    print("## Assessment")
    print()
    print("- Helper-program-owned accounts did not expose canonical Solana JUP key material in this snapshot.")
    print("- Helper-program-owned accounts did not expose current JupNet validator, vote or stake account keys in this snapshot.")
    print("- The outbox-owned account decodes as Merkle root history, not an obvious signer-set, quorum or stake-weight registry.")
    print("- If signer-set or quorum state is public, it is not obvious from direct key hits or helper-program-owned account layouts in this snapshot.")


if __name__ == "__main__":
    main()
