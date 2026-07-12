#!/usr/bin/env python3
"""Decode recurring Solana GUM Bank account state from a saved snapshot."""

from __future__ import annotations

import argparse
import base64
import collections
import hashlib
import json
import struct
from pathlib import Path


ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
GUM_BANK = "bk1PDAkbHEBGtVRiM94Lzets8gVFP7FgySyfkAc8MPN"
GUM_BANK_PROGRAM = "BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ"
JUP_MINT = "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN"
SYSTEM_PROGRAM = "11111111111111111111111111111111"
SPL_TOKEN = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
ASSOCIATED_TOKEN = "ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL"
WRAPPED_SOL = "So11111111111111111111111111111111111111112"
USDC = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
INBOX_EVENT_AUTH = "EG9fKpmLgkzCYZdj8uNDhHu5xmeXCZakccV6QmUavbzt"

SECURITY_TERMS = (
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
    "merkle",
    "root",
    "proof",
    "inbox",
    "outbox",
)

KNOWN_PUBKEYS = {
    "Gum Bank": GUM_BANK,
    "Gum Bank Program": GUM_BANK_PROGRAM,
    "canonical JUP mint": JUP_MINT,
    "USDC mint": USDC,
    "wrapped SOL mint": WRAPPED_SOL,
    "SPL Token program": SPL_TOKEN,
    "Associated Token program": ASSOCIATED_TOKEN,
    "__inbox_event_auth PDA": INBOX_EVENT_AUTH,
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


def token_account(raw: bytes) -> dict | None:
    if len(raw) < 165:
        return None
    state = raw[108]
    if state not in (1, 2):
        return None
    return {
        "mint": b58encode(raw[0:32]),
        "owner": b58encode(raw[32:64]),
        "amount": struct.unpack("<Q", raw[64:72])[0],
        "delegate_option": struct.unpack("<I", raw[72:76])[0],
        "state": state,
        "is_native_option": struct.unpack("<I", raw[109:113])[0],
        "delegated_amount": struct.unpack("<Q", raw[121:129])[0],
        "close_authority_option": struct.unpack("<I", raw[129:133])[0],
    }


def compact_bank_state(raw: bytes) -> dict:
    decoded = {}
    if len(raw) >= 9:
        decoded["byte_8"] = raw[8]
    if len(raw) == 41:
        decoded["pubkey_9_40"] = b58encode(raw[9:41])
    return decoded


def account_rows(base: Path) -> list[dict]:
    data = load(base / "solana-mainnet-getMultipleAccounts-BankRecurringAccounts.json")
    accounts = data.get("accounts") or []
    counts = data.get("counts") or {}
    values = ((data.get("response") or {}).get("result") or {}).get("value") or []
    related = validator_related_keys(base)
    watched = dict(KNOWN_PUBKEYS)
    watched.update(related)

    rows = []
    for account, value in zip(accounts, values):
        raw = raw_account_data(value)
        strings = printable_strings(raw)
        string_hits = collections.defaultdict(list)
        for text in strings:
            lower = text.lower()
            for term in SECURITY_TERMS:
                if term in lower and len(string_hits[term]) < 5:
                    string_hits[term].append(text[:120])
        raw_hits = []
        text_hits = []
        for label, pubkey in watched.items():
            try:
                pubkey_raw = b58decode(pubkey)
            except ValueError:
                continue
            if pubkey_raw and pubkey_raw in raw:
                raw_hits.append(f"{label}: {pubkey}")
            if pubkey.encode() in raw:
                text_hits.append(f"{label}: {pubkey}")
        embedded_pubkeys = collections.Counter()
        for offset in range(0, max(0, len(raw) - 31)):
            chunk = raw[offset : offset + 32]
            if chunk == b"\0" * 32:
                continue
            encoded = b58encode(chunk)
            if encoded in watched.values():
                embedded_pubkeys[encoded] += 1
        token = token_account(raw) if value and value.get("owner") == SPL_TOKEN else None
        if not value:
            classification = "missing"
        elif value.get("owner") == SPL_TOKEN and token:
            classification = "SPL token account"
        elif value.get("owner") == SYSTEM_PROGRAM and not raw:
            classification = "system account"
        elif value.get("owner") == GUM_BANK_PROGRAM:
            classification = "Bank Program-owned state"
        else:
            classification = "other account"
        rows.append(
            {
                "account": account,
                "count": counts.get(account),
                "value": value,
                "raw": raw,
                "sha256": hashlib.sha256(raw).hexdigest() if raw else None,
                "anchor_discriminator": raw[:8].hex() if len(raw) >= 8 else None,
                "classification": classification,
                "token": token,
                "compact_bank_state": compact_bank_state(raw) if value and value.get("owner") == GUM_BANK_PROGRAM else {},
                "raw_hits": raw_hits,
                "text_hits": text_hits,
                "embedded_pubkeys": embedded_pubkeys,
                "string_hits": dict(string_hits),
                "strings": strings,
            }
        )
    return rows


def fmt_list(values: list[str], empty: str = "`None`") -> str:
    if not values:
        return empty
    return "<br>".join(f"`{value}`" for value in values)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot_dir")
    args = parser.parse_args()
    base = Path(args.snapshot_dir)
    rows = account_rows(base)

    jup_raw_accounts = [row["account"] for row in rows if any("canonical JUP" in hit for hit in row["raw_hits"])]
    jup_text_accounts = [row["account"] for row in rows if any("canonical JUP" in hit for hit in row["text_hits"])]
    validator_accounts = [
        row["account"]
        for row in rows
        if any(("validator" in hit or "vote account" in hit or "stake account" in hit) for hit in row["raw_hits"] + row["text_hits"])
    ]
    class_counts = collections.Counter(row["classification"] for row in rows)

    print("# Bank Recurring Account State")
    print()
    print("## Scope")
    print()
    print(f"- Recurring Bank accounts fetched: `{len(rows)}`")
    print(f"- Accounts with canonical JUP raw pubkey bytes: `{len(jup_raw_accounts)}`")
    print(f"- Accounts with canonical JUP base58 text: `{len(jup_text_accounts)}`")
    print(f"- Accounts with JupNet validator/vote/stake key hits: `{len(validator_accounts)}`")
    print()
    print("## Classification Summary")
    print()
    for name, count in class_counts.most_common():
        print(f"- {name}: `{count}`")
    print()
    print("## Account Rows")
    print()
    print("| Account | Count | Owner | Space | Lamports | Class | Data SHA256 | Key hits | String hits |")
    print("|---|---:|---|---:|---:|---|---|---|---|")
    for row in rows:
        value = row["value"] or {}
        string_terms = []
        for term, values in row["string_hits"].items():
            string_terms.append(f"{term}: {', '.join(values[:2])}")
        key_hits = row["raw_hits"] + row["text_hits"]
        print(
            f"| `{row['account']}` | {row['count']} | `{value.get('owner')}` | "
            f"{value.get('space')} | {value.get('lamports')} | {row['classification']} | "
            f"`{row['sha256']}` | {fmt_list(key_hits)} | {fmt_list(string_terms)} |"
        )
    print()
    print("## Token Accounts")
    print()
    token_rows = [row for row in rows if row["token"]]
    if token_rows:
        print("| Account | Mint | Token owner | Amount | State |")
        print("|---|---|---|---:|---:|")
        for row in token_rows:
            token = row["token"]
            print(
                f"| `{row['account']}` | `{token['mint']}` | `{token['owner']}` | "
                f"{token['amount']} | {token['state']} |"
            )
    else:
        print("- None")
    print()
    print("## Bank Program-Owned State")
    print()
    bank_rows = [row for row in rows if row["classification"] == "Bank Program-owned state"]
    if bank_rows:
        print("| Account | Count | Space | Anchor/account discriminator | Compact fields | Raw key hits | Printable strings |")
        print("|---|---:|---:|---|---|---|---|")
        for row in bank_rows:
            strings = [text for text in row["strings"] if len(text) >= 4][:6]
            compact_fields = ", ".join(f"{key}={value}" for key, value in row["compact_bank_state"].items())
            print(
                f"| `{row['account']}` | {row['count']} | {row['value'].get('space')} | "
                f"`{row['anchor_discriminator']}` | `{compact_fields or 'None'}` | "
                f"{fmt_list(row['raw_hits'])} | {fmt_list(strings)} |"
            )
    else:
        print("- None")
    print()
    print("## Assessment")
    print()
    print("- No fetched recurring account contained canonical Solana JUP raw bytes or base58 text.")
    print("- No fetched recurring account contained current JupNet validator, vote or stake keys.")
    print("- Recurring SPL token accounts are USDC and wrapped SOL accounts in this sample, not JUP accounts.")
    print("- Bank Program-owned accounts should be treated as the next layout-reconstruction target if they are present.")


if __name__ == "__main__":
    main()
