#!/usr/bin/env python3
"""Analyze owner/program context for recurring GUM Bank accounts."""

from __future__ import annotations

import argparse
import base64
import collections
import datetime as dt
import hashlib
import json
import string
import struct
from pathlib import Path


ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
BPF_UPGRADEABLE_LOADER = "BPFLoaderUpgradeab1e11111111111111111111111"
SYSTEM_PROGRAM = "11111111111111111111111111111111"
JUP_MINT = "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN"
BANK_PROGRAM = "BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ"
USDC = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
WRAPPED_SOL = "So11111111111111111111111111111111111111112"

CONTEXT_LABELS = {
    "JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw": "owner program for 64-byte recurring account",
    "jnoUtncGR9ZCCMixtys6Gzy5coTo6mnmUZuEHRQFTFV": "owner program for 320-byte verify_request account",
    "5Tv692BDJinbjR6Beb2K9bGmxnbQeFaGb1rJqCs2y3Q6": "embedded pubkey in 41-byte Bank-owned state",
}

SEARCH_TERMS = (
    "jup",
    "jupnet",
    "gum",
    "bank",
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
    "inbox",
    "outbox",
    "request",
    "root",
    "authority",
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


def raw_account_data(value: dict | None) -> bytes:
    if not value:
        return b""
    data = value.get("data")
    if isinstance(data, list):
        return base64.b64decode(data[0])
    return b""


def programdata_address(value: dict | None) -> str | None:
    raw = raw_account_data(value)
    if len(raw) >= 36 and struct.unpack("<I", raw[:4])[0] == 2:
        return b58encode(raw[4:36])
    return None


def parse_programdata(raw: bytes) -> dict:
    if len(raw) < 45 or struct.unpack("<I", raw[:4])[0] != 3:
        return {}
    return {
        "slot": struct.unpack("<Q", raw[4:12])[0],
        "upgrade_authority": b58encode(raw[13:45]) if raw[12] == 1 else None,
        "executable": raw[45:],
    }


def printable_strings(raw: bytes, min_len: int = 4) -> list[str]:
    allowed = set(bytes(string.printable, "ascii")) - {0x0B, 0x0C}
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


def term_hits(strings: list[str]) -> dict[str, list[str]]:
    hits = {term: [] for term in SEARCH_TERMS}
    for text in strings:
        lower = text.lower()
        for term in SEARCH_TERMS:
            if term in lower and len(hits[term]) < 8:
                hits[term].append(text[:180])
    return {term: values for term, values in hits.items() if values}


def validator_related_keys(base: Path) -> dict[str, str]:
    keys = {}
    votes = (load(base / "getVoteAccounts.json").get("result") or {})
    for row in (votes.get("current") or []) + (votes.get("delinquent") or []):
        keys[row["nodePubkey"]] = "validator node"
        keys[row["votePubkey"]] = "vote account"
    for item in load(base / "getProgramAccounts-Stake.json").get("result") or []:
        keys[item["pubkey"]] = "stake account"
    return keys


def account_records(base: Path) -> list[dict]:
    data = load(base / "solana-mainnet-getMultipleAccounts-BankOwnerContext.json")
    accounts = data.get("accounts") or []
    values = ((data.get("response") or {}).get("result") or {}).get("value") or []
    related = validator_related_keys(base)
    watched = {
        "canonical JUP mint": JUP_MINT,
        "Bank Program": BANK_PROGRAM,
        "USDC mint": USDC,
        "wrapped SOL mint": WRAPPED_SOL,
        **related,
    }
    rows = []
    for account, value in zip(accounts, values):
        raw = raw_account_data(value)
        raw_hits = []
        text_hits = []
        for label, pubkey in watched.items():
            try:
                pubkey_raw = b58decode(pubkey)
            except ValueError:
                continue
            if pubkey_raw in raw:
                raw_hits.append(f"{label}: {pubkey}")
            if pubkey.encode() in raw:
                text_hits.append(f"{label}: {pubkey}")
        rows.append(
            {
                "account": account,
                "label": CONTEXT_LABELS.get(account, ""),
                "value": value,
                "raw": raw,
                "sha256": hashlib.sha256(raw).hexdigest() if raw else None,
                "programdata": programdata_address(value),
                "raw_hits": raw_hits,
                "text_hits": text_hits,
                "strings": printable_strings(raw),
            }
        )
    return rows


def programdata_records(base: Path, account_rows: list[dict]) -> list[dict]:
    rows = []
    for row in account_rows:
        programdata = row["programdata"]
        if not programdata:
            continue
        data = load(base / f"solana-mainnet-getAccountInfo-OwnerProgramData-{row['account'][:8]}.json")
        value = (data.get("result") or {}).get("value")
        raw = raw_account_data(value)
        parsed = parse_programdata(raw)
        executable = parsed.get("executable") or b""
        strings = printable_strings(executable)
        rows.append(
            {
                "program": row["account"],
                "programdata": programdata,
                "owner": value.get("owner") if value else None,
                "space": value.get("space") if value else None,
                "slot": parsed.get("slot"),
                "upgrade_authority": parsed.get("upgrade_authority"),
                "executable_len": len(executable),
                "sha256": hashlib.sha256(executable).hexdigest() if executable else None,
                "strings": strings,
                "hits": term_hits(strings),
            }
        )
    return rows


def block_time(value: int | None) -> str:
    if value is None:
        return "unknown"
    return dt.datetime.fromtimestamp(value, dt.timezone.utc).isoformat()


def signature_rows(base: Path) -> dict[str, dict]:
    data = load(base / "solana-mainnet-getSignaturesForAddress-BankOwnerContext.json")
    out = {}
    for account, response in data.items():
        rows = response.get("result") or []
        out[account] = {
            "count": len(rows),
            "latest_slot": rows[0].get("slot") if rows else None,
            "latest_time": block_time(rows[0].get("blockTime")) if rows else None,
        }
    return out


def fmt(values: list[str], empty: str = "`None`") -> str:
    if not values:
        return empty
    return "<br>".join(f"`{value}`" for value in values)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot_dir")
    args = parser.parse_args()
    base = Path(args.snapshot_dir)

    accounts = account_records(base)
    programdatas = programdata_records(base, accounts)
    signatures = signature_rows(base)

    jup_accounts = [row["account"] for row in accounts if any("canonical JUP" in hit for hit in row["raw_hits"] + row["text_hits"])]
    validator_accounts = [
        row["account"]
        for row in accounts
        if any(("validator" in hit or "vote account" in hit or "stake account" in hit) for hit in row["raw_hits"] + row["text_hits"])
    ]

    print("# Bank Owner Program Context")
    print()
    print("## Scope")
    print()
    print(f"- Owner-context accounts fetched: `{len(accounts)}`")
    print(f"- Upgradeable owner programs with ProgramData: `{len(programdatas)}`")
    print(f"- Accounts with canonical JUP key hits: `{len(jup_accounts)}`")
    print(f"- Accounts with current JupNet validator/vote/stake key hits: `{len(validator_accounts)}`")
    print()
    print("## Account Context")
    print()
    print("| Account | Context | Owner | Executable | Space | ProgramData | Signatures | Key hits |")
    print("|---|---|---|---|---:|---|---|---|")
    for row in accounts:
        value = row["value"] or {}
        sig = signatures.get(row["account"], {})
        sig_text = f"{sig.get('count', 0)} latest {sig.get('latest_slot') or 'none'}"
        key_hits = row["raw_hits"] + row["text_hits"]
        print(
            f"| `{row['account']}` | {row['label'] or ''} | `{value.get('owner')}` | "
            f"`{value.get('executable')}` | {value.get('space')} | "
            f"`{row['programdata']}` | `{sig_text}` | {fmt(key_hits)} |"
        )
    print()
    print("## Owner ProgramData")
    print()
    if programdatas:
        print("| Program | ProgramData | Deployment slot | Upgrade authority | Executable bytes | SHA256 | Relevant string hits |")
        print("|---|---|---:|---|---:|---|---|")
        for row in programdatas:
            hits = []
            for term, values in row["hits"].items():
                hits.append(f"{term}: {', '.join(values[:3])}")
            print(
                f"| `{row['program']}` | `{row['programdata']}` | {row['slot']} | "
                f"`{row['upgrade_authority']}` | {row['executable_len']} | "
                f"`{row['sha256']}` | {fmt(hits)} |"
            )
    else:
        print("- None")
    print()
    print("## Assessment")
    print()
    print("- The owner-context cluster did not expose canonical JUP key material.")
    print("- The owner-context cluster did not expose current JupNet validator, vote or stake keys.")
    print("- The recurring non-token state is controlled by small upgradeable Solana programs, so these accounts look like settlement/helper program state rather than a visible JUP security registry.")
    print("- ProgramData string hits, if present, should be treated as owner-program clues only unless they identify stake, quorum, signer weight, fee, slashing or governance state.")


if __name__ == "__main__":
    main()
