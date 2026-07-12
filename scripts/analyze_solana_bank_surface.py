#!/usr/bin/env python3
"""Analyze Solana mainnet Bank program evidence from a saved snapshot."""

from __future__ import annotations

import argparse
import base64
import collections
import datetime as dt
import json
import struct
from pathlib import Path


ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
JUP_MINT = "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN"
GUM_PROGRAM = "brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1"
GUM_BANK = "bk1PDAkbHEBGtVRiM94Lzets8gVFP7FgySyfkAc8MPN"
GUM_BANK_PROGRAM = "BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ"


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


def parse_program_account(value: dict | None) -> str | None:
    raw = raw_account_data(value)
    if len(raw) >= 36 and struct.unpack("<I", raw[:4])[0] == 2:
        return b58encode(raw[4:36])
    return None


def parse_programdata(value: dict | None) -> tuple[int | None, str | None]:
    raw = raw_account_data(value)
    if len(raw) >= 45 and struct.unpack("<I", raw[:4])[0] == 3:
        slot = struct.unpack("<Q", raw[4:12])[0]
        authority = b58encode(raw[13:45]) if raw[12] == 1 else None
        return slot, authority
    return None, None


def block_time(value: int | None) -> str:
    if value is None:
        return "unknown"
    return dt.datetime.fromtimestamp(value, dt.timezone.utc).isoformat()


def tx_account_keys(tx: dict) -> tuple[set[str], list[str]]:
    keys = set()
    signers = []
    for key in tx.get("transaction", {}).get("message", {}).get("accountKeys", []):
        if isinstance(key, dict):
            keys.add(key["pubkey"])
            if key.get("signer"):
                signers.append(key["pubkey"])
        elif isinstance(key, str):
            keys.add(key)
    return keys, signers


def scan_instruction(ix: dict, program_counts: collections.Counter, mint_counts: collections.Counter) -> None:
    program_id = ix.get("programId")
    if program_id:
        program_counts[program_id] += 1
    parsed = ix.get("parsed")
    if not isinstance(parsed, dict):
        return
    info = parsed.get("info") or {}
    if not isinstance(info, dict):
        return
    mint = info.get("mint")
    if isinstance(mint, str):
        mint_counts[mint] += 1
    token_amount = info.get("tokenAmount")
    if isinstance(token_amount, dict) and isinstance(token_amount.get("mint"), str):
        mint_counts[token_amount["mint"]] += 1


def tx_rows(base: Path) -> tuple[list[dict], collections.Counter, collections.Counter, collections.Counter]:
    rows = []
    program_counts: collections.Counter = collections.Counter()
    mint_counts: collections.Counter = collections.Counter()
    signer_counts: collections.Counter = collections.Counter()
    terms = (
        "jup",
        "stake",
        "signer",
        "quorum",
        "proof",
        "hash",
        "fee",
        "lock",
        "burn",
        "dove",
        "vote",
        "validator",
        "inbox",
        "outbox",
        "authority",
    )
    watched = {GUM_PROGRAM, GUM_BANK, GUM_BANK_PROGRAM, JUP_MINT}
    for path in sorted(base.glob("solana-mainnet-bank-tx-*.json")):
        data = load(path)
        tx = data.get("result")
        if not tx:
            rows.append({"file": path.name, "error": data.get("error") or "no result"})
            continue
        keys, signers = tx_account_keys(tx)
        for signer in signers:
            signer_counts[signer] += 1
        for ix in tx["transaction"]["message"].get("instructions", []):
            scan_instruction(ix, program_counts, mint_counts)
        for group in tx.get("meta", {}).get("innerInstructions") or []:
            for ix in group.get("instructions") or []:
                scan_instruction(ix, program_counts, mint_counts)
        logs = tx.get("meta", {}).get("logMessages") or []
        interesting_logs = [line for line in logs if any(term in line.lower() for term in terms)]
        rows.append(
            {
                "file": path.name,
                "slot": tx.get("slot"),
                "signers": signers,
                "watched_hits": sorted(keys & watched),
                "canonical_jup_account_hit": JUP_MINT in keys,
                "interesting_logs": interesting_logs,
            }
        )
    return rows, program_counts, mint_counts, signer_counts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot_dir")
    args = parser.parse_args()
    base = Path(args.snapshot_dir)

    bank = account_value(base, "solana-mainnet-getAccountInfo-GumBank.json")
    bank_program = account_value(base, "solana-mainnet-getAccountInfo-GumBankProgram.json")
    bank_programdata = parse_program_account(bank)
    bank_program_programdata = parse_program_account(bank_program)
    bank_slot, bank_authority = parse_programdata(
        account_value(base, "solana-mainnet-getAccountInfo-GumBankProgramData-slice48.json")
    )
    bank_program_slot, bank_program_authority = parse_programdata(
        account_value(base, "solana-mainnet-getAccountInfo-GumBankProgramProgramData-slice48.json")
    )
    bank_sigs = result(base, "solana-mainnet-getSignaturesForAddress-GumBank.json") or []
    bank_program_sigs = result(base, "solana-mainnet-getSignaturesForAddress-GumBankProgram.json") or []
    rows, program_counts, mint_counts, signer_counts = tx_rows(base)

    print("# Solana Mainnet Bank Surface")
    print()
    print("## Account Surface")
    print()
    print(f"- Bank account: `{GUM_BANK}`")
    print(f"- Bank account present on Solana mainnet: `{bool(bank)}`")
    if bank:
        print(f"- Bank owner: `{bank.get('owner')}`")
        print(f"- Bank executable: `{bank.get('executable')}`")
        print(f"- Bank data space: `{bank.get('space')}`")
        print(f"- Bank ProgramData: `{bank_programdata}`")
        print(f"- Bank ProgramData deployment slot: `{bank_slot}`")
        print(f"- Bank upgrade authority: `{bank_authority}`")
    print(f"- Bank Program account: `{GUM_BANK_PROGRAM}`")
    print(f"- Bank Program present on Solana mainnet: `{bool(bank_program)}`")
    if bank_program:
        print(f"- Bank Program owner: `{bank_program.get('owner')}`")
        print(f"- Bank Program executable: `{bank_program.get('executable')}`")
        print(f"- Bank Program data space: `{bank_program.get('space')}`")
        print(f"- Bank Program ProgramData: `{bank_program_programdata}`")
        print(f"- Bank ProgramData deployment slot: `{bank_program_slot}`")
        print(f"- Bank Program upgrade authority: `{bank_program_authority}`")
    print()
    print("## Signature Surface")
    print()
    print(f"- Recent Bank signatures in window: `{len(bank_sigs)}`")
    print(f"- Recent Bank Program signatures in window: `{len(bank_program_sigs)}`")
    if bank_program_sigs:
        print(f"- Latest Bank Program signature time: `{block_time(bank_program_sigs[0].get('blockTime'))}`")
        print(f"- Latest Bank Program slot: `{bank_program_sigs[0].get('slot')}`")
    print()
    print("## Sample Transaction Summary")
    print()
    print(f"- Sampled Bank Program transactions: `{len(rows)}`")
    print(f"- Sampled transactions with canonical JUP account key: `{sum(1 for row in rows if row.get('canonical_jup_account_hit'))}`")
    print()
    print("### Signers")
    print()
    for signer, count in signer_counts.most_common():
        print(f"- `{signer}`: `{count}`")
    if not signer_counts:
        print("- None")
    print()
    print("### Invoked Programs")
    print()
    for program, count in program_counts.most_common(20):
        print(f"- `{program}`: `{count}`")
    if not program_counts:
        print("- None")
    print()
    print("### Parsed Token Mints")
    print()
    for mint, count in mint_counts.most_common(20):
        print(f"- `{mint}`: `{count}`")
    if not mint_counts:
        print("- None")
    print()
    print("### Transaction Rows")
    print()
    print("| File | Slot | Signers | Watched hits | Canonical JUP key | Interesting logs |")
    print("|---|---:|---|---|---|---|")
    for row in rows:
        if row.get("error"):
            print(f"| `{row['file']}` |  |  |  |  | `{row['error']}` |")
            continue
        logs = "<br>".join(f"`{line}`" for line in row["interesting_logs"][:8])
        print(
            f"| `{row['file']}` | {row['slot']} | `{', '.join(row['signers'])}` | "
            f"`{', '.join(row['watched_hits'])}` | `{row['canonical_jup_account_hit']}` | {logs} |"
        )
    print()
    print("## Utility Assessment")
    print()
    print("- The Solana-side Bank Program exposes inbox/outbox message handling in sampled logs.")
    print("- Sampled transactions did not include the canonical Solana JUP mint as an account key.")
    print("- The observed token mints were USDC and wrapped SOL, so these samples do not show JUP-denominated utility.")
    print("- This is a strong cross-chain message-passing lead, but not validator/Dove security proof by itself.")


if __name__ == "__main__":
    main()
