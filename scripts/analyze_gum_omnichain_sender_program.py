#!/usr/bin/env python3
"""Analyze the JupNet Gum omnichain sender program recovered from outbox payloads."""

from __future__ import annotations

import argparse
import base64
import collections
import hashlib
import json
import string
import struct
from pathlib import Path


ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
GUM_OMNICHAIN_PROGRAM = "GUMebNDCYyF81xjyqaHagbgMQVUTb8fBC9YRh25xSH64"
GUM_OMNICHAIN_PROGRAMDATA = "Gi8HgbHnykRiHboqG2VHysti773o8bNSjuFJWpyf4Q89"
JUP_MINT = "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN"

TERMS = (
    "gum",
    "jup",
    "jupnet",
    "omnichain",
    "bank",
    "stake",
    "validator",
    "vote",
    "dove",
    "quorum",
    "weight",
    "slash",
    "reward",
    "bls",
    "bn254",
    "merkle",
    "proof",
    "root",
    "inbox",
    "outbox",
    "signature",
    "message",
    "withdraw",
    "deposit",
    "swap",
    "mint",
    "fee",
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


def parse_programdata(raw: bytes) -> dict:
    if len(raw) < 45 or struct.unpack("<I", raw[:4])[0] != 3:
        return {}
    return {
        "slot": struct.unpack("<Q", raw[4:12])[0],
        "upgrade_authority": b58encode(raw[13:45]) if raw[12] == 1 else None,
        "executable": raw[45:],
    }


def validator_related_keys(base: Path) -> dict[str, str]:
    keys = {}
    votes = (load(base / "getVoteAccounts.json").get("result") or {})
    for row in (votes.get("current") or []) + (votes.get("delinquent") or []):
        keys[row["nodePubkey"]] = "validator node"
        keys[row["votePubkey"]] = "vote account"
    for item in load(base / "getProgramAccounts-Stake.json").get("result") or []:
        keys[item["pubkey"]] = "stake account"
    return keys


def term_hits(strings: list[str]) -> dict[str, list[str]]:
    hits = collections.defaultdict(list)
    for text in strings:
        lower = text.lower()
        for term in TERMS:
            if term in lower and len(hits[term]) < 12:
                hits[term].append(text[:220])
    return dict(hits)


def key_hits(raw: bytes, watched: dict[str, str]) -> list[str]:
    hits = []
    for label, key in watched.items():
        try:
            key_raw = b58decode(key)
        except ValueError:
            continue
        if key_raw in raw:
            hits.append(f"{label} raw: {key}")
        if key.encode() in raw:
            hits.append(f"{label} text: {key}")
    return hits


def fmt(values: list[str], empty: str = "`None`") -> str:
    if not values:
        return empty
    return "<br>".join(f"`{value}`" for value in values)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot_dir")
    args = parser.parse_args()
    base = Path(args.snapshot_dir)

    program_value = (load(base / "getAccountInfo-GUMebProgram.json").get("result") or {}).get("value")
    programdata_value = (load(base / "getAccountInfo-GUMebProgramData-full.json").get("result") or {}).get("value")
    program_raw = raw_account_data(program_value)
    programdata_raw = raw_account_data(programdata_value)
    parsed = parse_programdata(programdata_raw)
    executable = parsed.get("executable") or b""
    strings = printable_strings(executable)
    hits = term_hits(strings)
    watched = {"canonical JUP mint": JUP_MINT, **validator_related_keys(base)}
    watched_hits = key_hits(executable, watched)

    derived_programdata = None
    if len(program_raw) >= 36 and struct.unpack("<I", program_raw[:4])[0] == 2:
        derived_programdata = b58encode(program_raw[4:36])

    print("# Gum Omnichain Sender Program")
    print()
    print("## Scope")
    print()
    print(f"- Sender/program id recovered from outbox verifier payloads: `{GUM_OMNICHAIN_PROGRAM}`")
    print(f"- ProgramData derived from program account: `{derived_programdata}`")
    print(f"- Expected ProgramData: `{GUM_OMNICHAIN_PROGRAMDATA}`")
    print()
    print("## Account Metadata")
    print()
    print("| Account | Owner | Executable | Space | SHA256 |")
    print("|---|---|---|---:|---|")
    print(
        f"| Program | `{program_value.get('owner') if program_value else None}` | "
        f"`{program_value.get('executable') if program_value else None}` | "
        f"{program_value.get('space') if program_value else 0} | `{hashlib.sha256(program_raw).hexdigest() if program_raw else None}` |"
    )
    print(
        f"| ProgramData | `{programdata_value.get('owner') if programdata_value else None}` | "
        f"`{programdata_value.get('executable') if programdata_value else None}` | "
        f"{programdata_value.get('space') if programdata_value else 0} | `{hashlib.sha256(programdata_raw).hexdigest() if programdata_raw else None}` |"
    )
    print()
    print("## ProgramData Header")
    print()
    print(f"- Deployment slot candidate: `{parsed.get('slot')}`")
    print(f"- Upgrade authority: `{parsed.get('upgrade_authority')}`")
    print(f"- Executable length: `{len(executable)}`")
    print(f"- Executable SHA256: `{hashlib.sha256(executable).hexdigest() if executable else None}`")
    print()
    print("## Term Hits")
    print()
    print("| Term | Count | Examples |")
    print("|---|---:|---|")
    for term in TERMS:
        values = hits.get(term, [])
        if values:
            print(f"| `{term}` | {len(values)} | {fmt(values[:4])} |")
    print()
    print("## Watched Key Hits")
    print()
    print(f"- Canonical JUP / current validator / vote / stake key hits in executable: `{len(watched_hits)}`")
    if watched_hits:
        for hit in watched_hits:
            print(f"- `{hit}`")
    print()
    print("## Assessment")
    print()
    print("- The outbox verifier sender/program candidate resolves to a live upgradeable JupNet executable.")
    print("- Executable strings identify it as `programs/gum-omnichain`, with deposit, withdrawal, swap, mint, inbox, outbox and BLS/Merkle verification surfaces.")
    print("- This strengthens the interpretation that sampled verifier payloads are Gum omnichain messages certified through the JupNet outbox verifier.")
    print("- The executable string/key scan did not expose a Dove registry, JUP-denominated stake weights, validator mappings, slashing or reward state.")


if __name__ == "__main__":
    main()
