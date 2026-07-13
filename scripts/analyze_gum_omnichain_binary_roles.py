#!/usr/bin/env python3
"""Compare Gum omnichain executables and map their verifier/runtime roles."""

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

TARGETS = (
    {
        "program": "brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1",
        "programdata": "BW7ncAFAX1jjhZU6X5AS8JrkAqr8njfUNQxkuPtUQXjv",
        "file": "jupnet-programdata-brhPfKEx.json",
        "label": "legacy/full Gum omnichain verifier candidate",
    },
    {
        "program": "GUMebNDCYyF81xjyqaHagbgMQVUTb8fBC9YRh25xSH64",
        "programdata": "Gi8HgbHnykRiHboqG2VHysti773o8bNSjuFJWpyf4Q89",
        "file": "jupnet-programdata-GUMebNDC.json",
        "label": "recovered outbox sender Gum omnichain",
    },
)

WATCH_TERMS = (
    "sol_verify_bls_merkle_key",
    "jupnet_alt_bn128_bls",
    "jupnet_bn254",
    "jupnet_crosschain_hash",
    "jupnet_svm",
    "jupnet_vote",
    "jupnet_bls",
    "jupnet_merkle",
    "verify_signature",
    "aggregate",
    "proof_hash",
    "inbox_hash",
    "outbound_hash",
    "root",
    "epoch",
    "chain_config",
    "fee",
    "stake",
    "validator",
    "vote",
    "dove",
    "quorum",
    "weight",
    "signer",
    "slash",
    "reward",
)

PRIVATE_PRODUCER_TERMS = (
    "jupnet_svm",
    "jupnet_vote",
    "jupnet_bls",
    "jupnet_merkle",
    "stake_weight",
    "validator_set",
    "signer_set",
    "root_builder",
    "aggregate_key_set",
    "dove",
    "quorum",
)

SOURCE_PATH_RE = re.compile(r"((?:programs|src|crates)/[A-Za-z0-9_./-]+?\.rs)")
JUPNET_SYMBOL_RE = re.compile(r"\bjupnet_[A-Za-z0-9_]+\b")
SOL_SYSCALL_RE = re.compile(r"\bsol_[A-Za-z0-9_]+\b")
INSTRUCTION_RE = re.compile(r"\bInstruction: ?[A-Za-z0-9_]+")


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


def clean(value: str) -> str:
    return " ".join(value.replace("|", "/").split())


def contexts(raw: bytes, term: str, width: int = 110) -> list[str]:
    lower = raw.lower()
    needle = term.lower().encode()
    out = []
    start = 0
    allowed = set(bytes(string.printable, "ascii")) - {0x0B, 0x0C}
    while True:
        index = lower.find(needle, start)
        if index == -1:
            break
        left = max(0, index - width)
        right = min(len(raw), index + len(needle) + width)
        snippet = raw[left:right]
        text = "".join(chr(byte) if byte in allowed else "." for byte in snippet)
        out.append(clean(text)[:260])
        start = index + len(needle)
        if len(out) >= 6:
            break
    return out


def source_paths(strings: list[str]) -> list[str]:
    paths = []
    seen = set()
    for text in strings:
        for match in SOURCE_PATH_RE.findall(text):
            if match not in seen:
                seen.add(match)
                paths.append(match)
    return paths


def path_family(path: str) -> str:
    if "/instructions/" in path:
        return "instructions"
    if "/state/" in path:
        return "state"
    if "/utils/" in path:
        return "utils"
    if path.endswith("/events.rs") or path.endswith("events.rs"):
        return "events"
    if path.endswith("/lib.rs") or path.endswith("lib.rs"):
        return "lib"
    return "other"


def symbol_counts(strings: list[str], pattern: re.Pattern[str]) -> collections.Counter[str]:
    counter: collections.Counter[str] = collections.Counter()
    for text in strings:
        for match in pattern.findall(text):
            counter[match] += 1
    return counter


def instruction_strings(strings: list[str]) -> list[str]:
    values = []
    seen = set()
    for text in strings:
        for match in INSTRUCTION_RE.findall(text):
            if match not in seen:
                seen.add(match)
                values.append(match)
    return values


def analyze_target(base: Path, target: dict) -> dict:
    value = (load(base / target["file"]).get("result") or {}).get("value")
    raw = raw_account_data(value)
    parsed = parse_programdata(raw)
    executable = parsed.get("executable") or b""
    strings = printable_strings(executable)
    paths = source_paths(strings)
    term_contexts = {term: contexts(executable, term) for term in WATCH_TERMS}
    return {
        **target,
        "owner": value.get("owner") if value else None,
        "space": value.get("space") if value else None,
        "slot": parsed.get("slot"),
        "upgrade_authority": parsed.get("upgrade_authority"),
        "programdata_sha256": hashlib.sha256(raw).hexdigest() if raw else None,
        "executable_len": len(executable),
        "executable_sha256": hashlib.sha256(executable).hexdigest() if executable else None,
        "string_count": len(strings),
        "source_paths": paths,
        "path_families": collections.Counter(path_family(path) for path in paths),
        "jupnet_symbols": symbol_counts(strings, JUPNET_SYMBOL_RE),
        "sol_syscalls": symbol_counts(strings, SOL_SYSCALL_RE),
        "instruction_strings": instruction_strings(strings),
        "term_counts": {term: len(values) for term, values in term_contexts.items()},
        "term_contexts": term_contexts,
    }


def fmt(values: list[str] | tuple[str, ...], empty: str = "`None`", limit: int | None = None) -> str:
    items = list(values)
    if limit is not None:
        items = items[:limit]
    if not items:
        return empty
    return "<br>".join(f"`{clean(str(value))}`" for value in items)


def fmt_counter(counter: collections.Counter[str], limit: int | None = None) -> str:
    return fmt([f"{key}: {value}" for key, value in counter.most_common(limit)], limit=limit)


def print_metadata(rows: list[dict]) -> None:
    print("## Executable Metadata")
    print()
    print("| Program | Label | Slot | Authority | Exe bytes | Exe SHA256 | Strings | Source paths |")
    print("|---|---|---:|---|---:|---|---:|---:|")
    for row in rows:
        print(
            f"| `{row['program']}` | `{row['label']}` | {row['slot']} | `{row['upgrade_authority']}` | "
            f"{row['executable_len']} | `{row['executable_sha256']}` | {row['string_count']} | {len(row['source_paths'])} |"
        )
    print()


def print_feature_matrix(rows: list[dict]) -> None:
    print("## Feature Matrix")
    print()
    print("| Feature | " + " | ".join(f"`{row['program'][:8]}...`" for row in rows) + " |")
    print("|---|" + "---:|" * len(rows))
    for term in WATCH_TERMS:
        print("| `" + term + "` | " + " | ".join(str(row["term_counts"].get(term, 0)) for row in rows) + " |")
    print()


def print_paths(rows: list[dict]) -> None:
    print("## Source Path Families")
    print()
    print("| Program | Families | Instruction paths | State paths | Utils paths |")
    print("|---|---|---|---|---|")
    for row in rows:
        instructions = [path for path in row["source_paths"] if path_family(path) == "instructions"]
        state = [path for path in row["source_paths"] if path_family(path) == "state"]
        utils = [path for path in row["source_paths"] if path_family(path) == "utils"]
        print(
            f"| `{row['program']}` | {fmt_counter(row['path_families'])} | "
            f"{fmt(instructions, limit=12)} | {fmt(state, limit=12)} | {fmt(utils, limit=12)} |"
        )
    print()


def print_symbols(rows: list[dict]) -> None:
    print("## Runtime Symbols And Syscalls")
    print()
    print("| Program | JupNet symbols | Solana/JupNet syscalls | Instruction markers |")
    print("|---|---|---|---|")
    for row in rows:
        print(
            f"| `{row['program']}` | {fmt_counter(row['jupnet_symbols'], limit=16)} | "
            f"{fmt_counter(row['sol_syscalls'], limit=16)} | {fmt(row['instruction_strings'], limit=16)} |"
        )
    print()


def print_unique_paths(rows: list[dict]) -> None:
    print("## Unique Gum Omnichain Paths")
    print()
    if len(rows) != 2:
        print("- Unique path comparison expects exactly two targets.")
        print()
        return
    left, right = rows
    left_paths = set(left["source_paths"])
    right_paths = set(right["source_paths"])
    print(f"### Only `{left['program']}`")
    print()
    print(fmt(sorted(left_paths - right_paths), limit=40))
    print()
    print(f"### Only `{right['program']}`")
    print()
    print(fmt(sorted(right_paths - left_paths), limit=40))
    print()


def print_contexts(rows: list[dict]) -> None:
    print("## High-Value Contexts")
    print()
    for term in WATCH_TERMS:
        if not any(row["term_contexts"].get(term) for row in rows):
            continue
        print(f"### `{term}`")
        print()
        for row in rows:
            values = row["term_contexts"].get(term) or []
            if values:
                print(f"- `{row['program']}`: {fmt(values, limit=4)}")
        print()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot_dir")
    args = parser.parse_args()
    base = Path(args.snapshot_dir)
    rows = [analyze_target(base, target) for target in TARGETS]
    producer_hits = {
        row["program"]: [term for term in PRIVATE_PRODUCER_TERMS if row["term_counts"].get(term)]
        for row in rows
    }

    print("# Gum Omnichain Binary Role Map")
    print()
    print("## Purpose")
    print()
    print("This pass compares the two Gum omnichain executables that consume BLS/Merkle verification surfaces, with special focus on the `brhPf...` binary that leaks JupNet-specific BN254 and cross-chain hash symbols.")
    print()
    print_metadata(rows)
    print_feature_matrix(rows)
    print_paths(rows)
    print_symbols(rows)
    print_unique_paths(rows)
    print_contexts(rows)
    print("## Assessment")
    print()
    print("- `brhPf...` is the richer/full Gum omnichain verifier candidate: it contains `jupnet_bn254`, `jupnet_crosschain_hash`, `jupnet_alt_bn128_bls`, `verify_signature`, `proof_hash`, `inbox_hash`, Gum instruction/state paths and `sol_verify_bls_merkle_key`.")
    print("- `GUMeb...` is the recovered sender/program id from verifier payloads. It contains Gum omnichain state/instruction paths and `sol_verify_bls_merkle_key`, but did not expose the same private BN254/cross-chain hash crate symbols in this snapshot.")
    for program, hits in producer_hits.items():
        print(f"- Producer/security terms in `{program}`: {fmt(hits)}")
    print("- The comparison clarifies the public application/verifier split, but still does not expose a Dove registry, JUP stake-weight table, quorum calculation or root-builder implementation.")


if __name__ == "__main__":
    main()
