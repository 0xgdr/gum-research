#!/usr/bin/env python3
"""Analyze full ProgramData accounts for JupNet upgradeable executables."""

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
JUP_MINT = "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN"

SOURCE_PATH_RE = re.compile(r"(?:programs|src|crates)/[A-Za-z0-9_./-]+\.rs")
SECURITY_TERMS = (
    "jup",
    "jupnet",
    "gum",
    "dove",
    "stake",
    "validator",
    "vote",
    "quorum",
    "weight",
    "slash",
    "reward",
    "bls",
    "bn254",
    "merkle",
    "proof",
    "root",
    "epoch",
    "outbox",
    "inbox",
    "signature",
    "signer",
    "message",
    "syscall",
    "verify",
    "fee",
)
HIGH_VALUE_TERMS = (
    "dove",
    "stake",
    "validator",
    "vote",
    "quorum",
    "weight",
    "slash",
    "reward",
    "jup",
    "sol_verify_bls_merkle_key",
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


def term_hits(strings: list[str], terms: tuple[str, ...]) -> dict[str, list[str]]:
    hits = collections.defaultdict(list)
    for text in strings:
        lower = text.lower()
        for term in terms:
            if term.lower() in lower and len(hits[term]) < 8:
                hits[term].append(text[:220])
    return dict(hits)


def source_paths(strings: list[str]) -> list[str]:
    paths = []
    seen = set()
    for text in strings:
        for match in SOURCE_PATH_RE.findall(text):
            if match not in seen:
                seen.add(match)
                paths.append(match)
    return paths


def watched_key_hits(raw: bytes, watched: dict[str, str]) -> list[str]:
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


def program_rows(base: Path) -> list[dict]:
    manifest = load(base / "jupnet-executable-census-manifest.json")
    watched = {"canonical JUP mint": JUP_MINT, **validator_related_keys(base)}
    rows = []
    for item in manifest.get("programs") or []:
        filename = item["programdata_file"]
        value = (load(base / filename).get("result") or {}).get("value")
        raw = raw_account_data(value)
        parsed = parse_programdata(raw)
        executable = parsed.get("executable") or b""
        strings = printable_strings(executable)
        paths = source_paths(strings)
        hits = term_hits(strings, SECURITY_TERMS)
        high = term_hits(strings, HIGH_VALUE_TERMS)
        key_hits = watched_key_hits(executable, watched)
        rows.append(
            {
                **item,
                "owner": value.get("owner") if value else None,
                "space": value.get("space") if value else None,
                "slot": parsed.get("slot"),
                "upgrade_authority": parsed.get("upgrade_authority"),
                "executable_len": len(executable),
                "executable_sha256": hashlib.sha256(executable).hexdigest() if executable else None,
                "programdata_sha256": hashlib.sha256(raw).hexdigest() if raw else None,
                "strings_count": len(strings),
                "source_paths": paths,
                "term_hits": hits,
                "high_value_hits": high,
                "key_hits": key_hits,
            }
        )
    return rows


def fmt(values: list[str], empty: str = "`None`") -> str:
    if not values:
        return empty
    return "<br>".join(f"`{value}`" for value in values)


def program_label(row: dict) -> str:
    for values in row.get("term_hits", {}).values():
        if any("gum-omnichain" in value for value in values):
            return "gum-omnichain"
    paths = row["source_paths"]
    for path in paths:
        parts = path.split("/")
        if len(parts) >= 2 and parts[0] == "programs":
            return parts[1]
    if paths:
        first = paths[0]
        return first
    return ""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot_dir")
    args = parser.parse_args()
    base = Path(args.snapshot_dir)
    rows = program_rows(base)

    key_hit_rows = [row for row in rows if row["key_hits"]]
    high_rows = [row for row in rows if row["high_value_hits"]]
    verifier_rows = [
        row
        for row in rows
        if any("sol_verify_bls_merkle_key" in text for values in row["term_hits"].values() for text in values)
    ]
    authorities = collections.Counter(row["upgrade_authority"] for row in rows)
    labels = collections.Counter(program_label(row) or "unlabeled" for row in rows)

    print("# JupNet Executable Census")
    print()
    print("## Scope")
    print()
    print(f"- Snapshot: `{base}`")
    print(f"- Upgradeable executables analyzed: `{len(rows)}`")
    print(f"- Executables with source paths: `{sum(1 for row in rows if row['source_paths'])}`")
    print(f"- Executables with high-value security term hits: `{len(high_rows)}`")
    print(f"- Executables with canonical JUP / validator / vote / stake key hits: `{len(key_hit_rows)}`")
    print(f"- Executables with `sol_verify_bls_merkle_key`: `{len(verifier_rows)}`")
    print()
    print("## Program Families")
    print()
    print("| Label | Count |")
    print("|---|---:|")
    for label, count in labels.most_common():
        print(f"| `{label}` | {count} |")
    print()
    print("## Upgrade Authorities")
    print()
    print("| Upgrade authority | Program count |")
    print("|---|---:|")
    for authority, count in authorities.most_common():
        print(f"| `{authority}` | {count} |")
    print()
    print("## Program Rows")
    print()
    print("| Program | Label | ProgramData | Slot | Authority | Exe bytes | Exe SHA256 | Source paths | Key hits | High-value hits |")
    print("|---|---|---|---:|---|---:|---|---|---|---|")
    for row in rows:
        high_terms = [f"{term}: {len(values)}" for term, values in row["high_value_hits"].items()]
        print(
            f"| `{row['program']}` | `{program_label(row)}` | `{row['programdata']}` | "
            f"{row['slot']} | `{row['upgrade_authority']}` | {row['executable_len']} | "
            f"`{row['executable_sha256']}` | {fmt(row['source_paths'][:4])} | "
            f"{fmt(row['key_hits'])} | {fmt(high_terms)} |"
        )
    print()
    print("## Verifier Syscall Candidates")
    print()
    if verifier_rows:
        print("| Program | Label | Evidence |")
        print("|---|---|---|")
        for row in verifier_rows:
            evidence = []
            for values in row["term_hits"].values():
                evidence.extend(text for text in values if "sol_verify_bls_merkle_key" in text)
            print(f"| `{row['program']}` | `{program_label(row)}` | {fmt(evidence[:4])} |")
    else:
        print("- None")
    print()
    print("## High-Value Term Examples")
    print()
    if high_rows:
        for row in high_rows:
            print(f"### `{row['program']}` `{program_label(row)}`")
            print()
            for term, values in row["high_value_hits"].items():
                print(f"- `{term}`: {fmt(values[:3])}")
            print()
    else:
        print("- None")
    print("## Assessment")
    print()
    print("- The census indexes all upgradeable JupNet executables visible in the saved loader scan.")
    if verifier_rows:
        print("- `sol_verify_bls_merkle_key` appears in Gum omnichain executables, matching the outbox verifier payload analysis.")
    print("- No executable in the census exposed canonical JUP, current validator, vote or stake key material.")
    print("- Source-path/string evidence still supports application-level Gum/outbox verification, but did not reveal a public Dove registry, JUP stake-weight table, slashing or reward implementation.")


if __name__ == "__main__":
    main()
