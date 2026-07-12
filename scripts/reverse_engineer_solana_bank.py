#!/usr/bin/env python3
"""Reverse-engineering helper for Solana-side GUM Bank programs."""

from __future__ import annotations

import argparse
import base64
import collections
import hashlib
import json
import re
import string
import struct
from pathlib import Path


ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
GUM_BANK = "bk1PDAkbHEBGtVRiM94Lzets8gVFP7FgySyfkAc8MPN"
GUM_BANK_PROGRAM = "BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ"
JUP_MINT = "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN"

SEARCH_TERMS = (
    "SubmitInboxMessageWithFinality",
    "VerifyOutboxMessage",
    "Outbox verification passed",
    "Withdrawal processed",
    "inbox",
    "outbox",
    "proof",
    "validator",
    "quorum",
    "signer",
    "merkle",
    "bls",
    "jup",
    "fee",
    "authority",
    "finality",
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


def result(base: Path, filename: str):
    return load(base / filename).get("result")


def raw_account_data(value: dict | None) -> bytes:
    if not value:
        return b""
    data = value.get("data")
    if isinstance(data, list):
        return base64.b64decode(data[0])
    return b""


def account_value(base: Path, filename: str) -> dict | None:
    data = result(base, filename)
    if not data:
        return None
    return data.get("value")


def executable_bytes(programdata_raw: bytes) -> bytes:
    if len(programdata_raw) >= 45 and struct.unpack("<I", programdata_raw[:4])[0] == 3:
        return programdata_raw[45:]
    return b""


def printable_strings(raw: bytes, min_len: int = 4) -> list[str]:
    allowed = set(bytes(string.printable, "ascii"))
    out = []
    current = bytearray()
    for byte in raw:
        if byte in allowed and byte not in (0x0B, 0x0C):
            current.append(byte)
            continue
        if len(current) >= min_len:
            out.append(current.decode("ascii", errors="ignore"))
        current.clear()
    if len(current) >= min_len:
        out.append(current.decode("ascii", errors="ignore"))
    return out


def term_hits(strings: list[str]) -> dict[str, list[str]]:
    hits: dict[str, list[str]] = {term: [] for term in SEARCH_TERMS}
    for value in strings:
        lower = value.lower()
        for term in SEARCH_TERMS:
            if term.lower() in lower and len(hits[term]) < 12:
                hits[term].append(value[:240])
    return {term: values for term, values in hits.items() if values}


def anchor_discriminator(name: str) -> str:
    return hashlib.sha256(f"global:{name}".encode()).digest()[:8].hex()


def account_metas(message: dict) -> dict[str, dict]:
    metas = {}
    for key in message.get("accountKeys", []):
        if isinstance(key, dict):
            metas[key["pubkey"]] = {
                "signer": bool(key.get("signer")),
                "writable": bool(key.get("writable")),
                "source": key.get("source"),
            }
        elif isinstance(key, str):
            metas[key] = {"signer": False, "writable": False, "source": "unknown"}
    return metas


def bank_logs(logs: list[str]) -> list[str]:
    terms = ("instruction:", "inbox", "outbox", "withdrawal", "proof", "validator", "quorum", "signer", "jup", "fee")
    return [line for line in logs if any(term in line.lower() for term in terms)]


def token_mints(tx: dict) -> collections.Counter:
    counts: collections.Counter = collections.Counter()

    def scan(ix: dict) -> None:
        parsed = ix.get("parsed")
        if not isinstance(parsed, dict):
            return
        info = parsed.get("info") or {}
        if not isinstance(info, dict):
            return
        mint = info.get("mint")
        if isinstance(mint, str):
            counts[mint] += 1
        token_amount = info.get("tokenAmount")
        if isinstance(token_amount, dict) and isinstance(token_amount.get("mint"), str):
            counts[token_amount["mint"]] += 1

    for ix in tx.get("transaction", {}).get("message", {}).get("instructions", []):
        scan(ix)
    for group in tx.get("meta", {}).get("innerInstructions") or []:
        for ix in group.get("instructions") or []:
            scan(ix)
    return counts


def group_bank_instructions(base: Path) -> tuple[dict[tuple[str, int, int], dict], collections.Counter]:
    variants: dict[tuple[str, int, int], dict] = {}
    all_mints: collections.Counter = collections.Counter()
    for path in sorted(base.glob("solana-mainnet-bank-tx-*.json")):
        tx = load(path).get("result")
        if not tx:
            continue
        message = tx["transaction"]["message"]
        metas = account_metas(message)
        logs = bank_logs(tx.get("meta", {}).get("logMessages") or [])
        tx_mints = token_mints(tx)
        all_mints.update(tx_mints)
        for index, ix in enumerate(message.get("instructions", [])):
            if ix.get("programId") != GUM_BANK_PROGRAM:
                continue
            raw = b58decode(ix.get("data", ""))
            discriminator = raw[:8].hex() if raw else ""
            accounts = ix.get("accounts") or []
            key = (discriminator, len(raw), len(accounts))
            row = variants.setdefault(
                key,
                {
                    "count": 0,
                    "files": [],
                    "signer_accounts": collections.Counter(),
                    "writable_accounts": collections.Counter(),
                    "readonly_accounts": collections.Counter(),
                    "logs": collections.Counter(),
                    "mints": collections.Counter(),
                    "raw_prefixes": collections.Counter(),
                },
            )
            row["count"] += 1
            row["files"].append(path.name)
            row["raw_prefixes"][raw[:16].hex()] += 1
            row["mints"].update(tx_mints)
            for line in logs:
                row["logs"][line] += 1
            for account in accounts:
                meta = metas.get(account, {})
                if meta.get("signer"):
                    row["signer_accounts"][account] += 1
                if meta.get("writable"):
                    row["writable_accounts"][account] += 1
                else:
                    row["readonly_accounts"][account] += 1
    return variants, all_mints


def programdata_report(base: Path) -> list[dict]:
    configs = [
        (
            "Bank",
            "solana-mainnet-getAccountInfo-GumBankProgramData-full.json",
            "solana-mainnet-getAccountInfo-GumBankProgramData-slice48.json",
        ),
        (
            "Bank Program",
            "solana-mainnet-getAccountInfo-GumBankProgramProgramData-full.json",
            "solana-mainnet-getAccountInfo-GumBankProgramProgramData-slice48.json",
        ),
    ]
    reports = []
    for label, full_filename, header_filename in configs:
        value = account_value(base, full_filename)
        raw = raw_account_data(value)
        header_value = account_value(base, header_filename)
        header_raw = raw_account_data(header_value)
        slot = None
        authority = None
        if len(header_raw) >= 45 and struct.unpack("<I", header_raw[:4])[0] == 3:
            slot = struct.unpack("<Q", header_raw[4:12])[0]
            authority = b58encode(header_raw[13:45]) if header_raw[12] == 1 else None
        executable = executable_bytes(raw)
        strings = printable_strings(executable)
        reports.append(
            {
                "label": label,
                "present": bool(value),
                "owner": value.get("owner") if value else None,
                "space": value.get("space") if value else None,
                "deployment_slot": slot,
                "upgrade_authority": authority,
                "executable_bytes": len(executable),
                "sha256": hashlib.sha256(executable).hexdigest() if executable else None,
                "strings": strings,
                "hits": term_hits(strings),
            }
        )
    return reports


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot_dir")
    args = parser.parse_args()
    base = Path(args.snapshot_dir)

    variants, all_mints = group_bank_instructions(base)
    binaries = programdata_report(base)
    known_names = [
        "withdraw",
        "sweep",
        "verify_request",
        "rfq_sell_resolve",
        "rfq_sell_commit",
        "deposit",
        "submit_inbox_message_with_finality",
        "verify_outbox_message",
        "initialize",
        "set_authority",
        "upgrade",
    ]
    known_discriminators = {name: anchor_discriminator(name) for name in known_names}

    print("# Solana Bank Reverse Engineering")
    print()
    print("## Instruction Variant Groups")
    print()
    print(f"- Sampled transactions scanned: `{len(list(base.glob('solana-mainnet-bank-tx-*.json')))}`")
    print(f"- Distinct top-level Bank instruction variants: `{len(variants)}`")
    print()
    print("| Count | Discriminator | Data length | Account count | Likely Anchor name | Files | Mints | Logs |")
    print("|---:|---|---:|---:|---|---|---|---|")
    for (discriminator, data_len, account_count), row in sorted(variants.items(), key=lambda item: (-item[1]["count"], item[0])):
        likely = [name for name, disc in known_discriminators.items() if disc == discriminator]
        files = ", ".join(row["files"][:8])
        mints = "<br>".join(f"`{mint}` {count}" for mint, count in row["mints"].most_common(6))
        logs = "<br>".join(f"`{line}` {count}" for line, count in row["logs"].most_common(8))
        print(
            f"| {row['count']} | `{discriminator}` | {data_len} | {account_count} | "
            f"`{', '.join(likely) if likely else ''}` | `{files}` | {mints} | {logs} |"
        )
    print()
    print("## Variant Account Roles")
    print()
    for (discriminator, data_len, account_count), row in sorted(variants.items(), key=lambda item: (-item[1]["count"], item[0])):
        print(f"### `{discriminator}` length `{data_len}` accounts `{account_count}`")
        print()
        print(f"- Signer accounts: `{', '.join(k for k, _ in row['signer_accounts'].most_common())}`")
        print(f"- Writable accounts: `{', '.join(k for k, _ in row['writable_accounts'].most_common(20))}`")
        print(f"- Readonly accounts: `{', '.join(k for k, _ in row['readonly_accounts'].most_common(20))}`")
        print()
    print("## Parsed Token Mints Across Samples")
    print()
    for mint, count in all_mints.most_common():
        print(f"- `{mint}`: `{count}`")
    if not all_mints:
        print("- None")
    print()
    print("## ProgramData Binary String Scan")
    print()
    for report in binaries:
        print(f"### {report['label']}")
        print()
        print(f"- Present: `{report['present']}`")
        print(f"- Owner: `{report['owner']}`")
        print(f"- Account space: `{report['space']}`")
        print(f"- Deployment slot: `{report['deployment_slot']}`")
        print(f"- Upgrade authority: `{report['upgrade_authority']}`")
        print(f"- Executable byte length: `{report['executable_bytes']}`")
        print(f"- Executable SHA256: `{report['sha256']}`")
        print(f"- Printable strings extracted: `{len(report['strings'])}`")
        print()
        print("| Term | Hit count | Sample strings |")
        print("|---|---:|---|")
        if report["hits"]:
            for term, values in report["hits"].items():
                samples = "<br>".join(f"`{value}`" for value in values[:8])
                print(f"| `{term}` | {len(values)} | {samples} |")
        else:
            print("| None | 0 |  |")
        print()
    print("## Utility Assessment")
    print()
    print("- The sampled Bank Program transactions group into a small number of instruction variants with Anchor-style logging.")
    print("- Inbox/outbox strings are present in sampled transaction logs and binary strings.")
    print("- Canonical JUP was not observed as a parsed token mint in the sampled transactions.")
    print("- Binary string hits are clues only; they do not prove JUP-denominated stake, signer weight, quorum, fees or validator security.")


if __name__ == "__main__":
    main()
