#!/usr/bin/env python3
"""Search saved public artifacts for private JupNet runtime/security fingerprints."""

from __future__ import annotations

import argparse
import base64
import collections
import json
import re
import string
from pathlib import Path
from typing import Any


ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

PRIVATE_RUNTIME_TERMS = (
    "jupnet-svm",
    "jupnet_svm",
    "jupnet-vote",
    "jupnet_vote",
    "jupnet-vote-program",
    "jupnet_vote_program",
    "jupnet-bls-sdk",
    "jupnet_bls_sdk",
    "jupnet-bn254",
    "jupnet_bn254",
    "jupnet-merkle-tree",
    "jupnet_merkle_tree",
    "jupnet-crosschain-hash",
    "jupnet_crosschain_hash",
    "jupnet-define-syscall",
    "jupnet_define_syscall",
)

SECURITY_PRODUCER_TERMS = (
    "dove",
    "doves",
    "validator_set",
    "validator set",
    "stake_weight",
    "stake weight",
    "vote_weight",
    "vote weight",
    "signer_set",
    "signer set",
    "quorum",
    "root_builder",
    "root builder",
    "aggregate_key_set",
    "aggregate key set",
    "slashing",
    "slash",
    "reward",
)

PUBLIC_VERIFIER_TERMS = (
    "sol_verify_bls_merkle_key",
    "jupnet_alt_bn128_bls",
    "programs/jupnet-inbox-program",
    "programs/jupnet-outbox-program",
    "programs/gum-omnichain",
    "verifyoutboxmessage",
    "updatemerkleroot",
    "merkle proof verified",
    "verifying bls signature",
    "signature verified",
)

ALL_TERMS = PRIVATE_RUNTIME_TERMS + SECURITY_PRODUCER_TERMS + PUBLIC_VERIFIER_TERMS
SOURCE_PATH_RE = re.compile(rb"(?:programs|src|crates)/[A-Za-z0-9_./-]+\.rs")


def b58decode(value: str) -> bytes:
    number = 0
    for char in value:
        number = number * 58 + ALPHABET.index(char)
    data = number.to_bytes((number.bit_length() + 7) // 8, "big") if number else b""
    return (b"\0" * (len(value) - len(value.lstrip("1")))) + data


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text())
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None


def account_data_from_node(node: Any) -> bytes | None:
    if not isinstance(node, dict):
        return None
    data = node.get("data")
    if isinstance(data, list) and data and isinstance(data[0], str):
        try:
            return base64.b64decode(data[0])
        except (ValueError, TypeError):
            return None
    return None


def walk_json(node: Any, path: str = "$") -> list[tuple[str, Any]]:
    rows = [(path, node)]
    if isinstance(node, dict):
        for key, value in node.items():
            rows.extend(walk_json(value, f"{path}.{key}"))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            rows.extend(walk_json(value, f"{path}[{index}]"))
    return rows


def instruction_data_blobs(data: Any) -> list[tuple[str, bytes]]:
    blobs = []
    for node_path, node in walk_json(data):
        if not isinstance(node, dict):
            continue
        raw = node.get("data")
        if not isinstance(raw, str) or not raw:
            continue
        program_id = node.get("programId") or node.get("program")
        if not program_id:
            continue
        try:
            decoded = b58decode(raw)
        except ValueError:
            continue
        if decoded:
            blobs.append((f"{node_path}.data", decoded))
    return blobs


def artifact_blobs(path: Path) -> list[tuple[str, bytes]]:
    data = load_json(path)
    text = path.read_bytes()
    blobs = [("json-text", text)]
    if data is None:
        return blobs
    for node_path, node in walk_json(data):
        raw = account_data_from_node(node)
        if raw:
            blobs.append((f"{node_path}.data[base64]", raw))
    blobs.extend(instruction_data_blobs(data))
    return blobs


def context(raw: bytes, term: bytes, width: int = 90) -> str:
    lower = raw.lower()
    index = lower.find(term.lower())
    if index == -1:
        return ""
    start = max(0, index - width)
    end = min(len(raw), index + len(term) + width)
    snippet = raw[start:end]
    allowed = set(bytes(string.printable, "ascii")) - {0x0B, 0x0C}
    cleaned = "".join(chr(byte) if byte in allowed else "." for byte in snippet)
    return " ".join(cleaned.split())


def source_paths(raw: bytes) -> set[str]:
    return {match.decode("ascii", errors="ignore") for match in SOURCE_PATH_RE.findall(raw)}


def scan(base: Path) -> dict:
    term_hits = collections.defaultdict(list)
    source_hit_rows = collections.defaultdict(set)
    files_scanned = 0
    blobs_scanned = 0

    for path in sorted(base.glob("*.json")):
        files_scanned += 1
        blobs = artifact_blobs(path)
        blobs_scanned += len(blobs)
        for blob_label, raw in blobs:
            lower = raw.lower()
            for source_path in source_paths(raw):
                source_hit_rows[source_path].add(f"{path.name} | {blob_label}")
            for term in ALL_TERMS:
                if blob_label == "json-text" and term not in PUBLIC_VERIFIER_TERMS:
                    continue
                needle = term.encode()
                if needle.lower() not in lower:
                    continue
                term_hits[term].append(
                    {
                        "file": path.name,
                        "blob": blob_label,
                        "context": context(raw, needle),
                    }
                )

    return {
        "files_scanned": files_scanned,
        "blobs_scanned": blobs_scanned,
        "term_hits": dict(term_hits),
        "source_hit_rows": {key: sorted(value) for key, value in source_hit_rows.items()},
    }


def fmt(values: list[str], empty: str = "`None`", limit: int | None = None) -> str:
    if limit is not None:
        values = values[:limit]
    if not values:
        return empty
    return "<br>".join(f"`{value}`" for value in values)


def print_term_table(title: str, terms: tuple[str, ...], hits: dict[str, list[dict]]) -> None:
    print(f"## {title}")
    print()
    print("| Term | Hit count | Artifacts |")
    print("|---|---:|---|")
    for term in terms:
        rows = hits.get(term, [])
        artifacts = sorted({f"{row['file']} | {row['blob']}" for row in rows})
        print(f"| `{term}` | {len(rows)} | {fmt(artifacts, limit=10)} |")
    print()


def print_context_examples(title: str, terms: tuple[str, ...], hits: dict[str, list[dict]]) -> None:
    print(f"## {title}")
    print()
    emitted = False
    for term in terms:
        rows = hits.get(term, [])
        if not rows:
            continue
        emitted = True
        print(f"### `{term}`")
        print()
        seen = set()
        for row in rows:
            key = (row["file"], row["blob"], row["context"])
            if key in seen:
                continue
            seen.add(key)
            print(f"- `{row['file']}` `{row['blob']}`: `{row['context'][:240]}`")
            if len(seen) >= 6:
                break
        print()
    if not emitted:
        print("- None")
        print()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot_dir")
    args = parser.parse_args()
    base = Path(args.snapshot_dir)
    result = scan(base)
    hits = result["term_hits"]

    private_hit_terms = [term for term in PRIVATE_RUNTIME_TERMS if hits.get(term)]
    producer_hit_terms = [term for term in SECURITY_PRODUCER_TERMS if hits.get(term)]
    verifier_hit_terms = [term for term in PUBLIC_VERIFIER_TERMS if hits.get(term)]
    source_rows = result["source_hit_rows"]
    private_source_paths = sorted(
        path for path in source_rows if "jupnet" in path.lower() or "gum-omnichain" in path.lower()
    )

    print("# Private Runtime Fingerprint Hunt")
    print()
    print("## Purpose")
    print()
    print("This pass searches saved public artifacts for strings that would connect the visible Gum/JupNet verifier layer to private runtime, Dove, stake-weight or quorum implementation details.")
    print()
    print("It scans decoded account data, ProgramData executable bytes, transaction instruction bytes and JSON/log text from the snapshot.")
    print()
    print("## Scope")
    print()
    print(f"- Snapshot: `{base}`")
    print(f"- JSON artifacts scanned: `{result['files_scanned']}`")
    print(f"- Decoded/text blobs scanned: `{result['blobs_scanned']}`")
    print(f"- Private runtime dependency terms with hits: `{len(private_hit_terms)}`")
    print(f"- Security producer terms with hits: `{len(producer_hit_terms)}`")
    print(f"- Public verifier terms with hits: `{len(verifier_hit_terms)}`")
    print(f"- JupNet/Gum source paths recovered: `{len(private_source_paths)}`")
    print()

    print_term_table("Private Runtime Dependency Terms", PRIVATE_RUNTIME_TERMS, hits)
    print_term_table("Security Producer Terms", SECURITY_PRODUCER_TERMS, hits)
    print_term_table("Public Verifier Terms", PUBLIC_VERIFIER_TERMS, hits)

    print("## JupNet/Gum Source Paths")
    print()
    if private_source_paths:
        print("| Source path | Artifact references |")
        print("|---|---|")
        for path in private_source_paths:
            print(f"| `{path}` | {fmt(source_rows[path], limit=8)} |")
    else:
        print("- None")
    print()

    print_context_examples("Private Runtime Context Examples", PRIVATE_RUNTIME_TERMS, hits)
    print_context_examples("Security Producer Context Examples", SECURITY_PRODUCER_TERMS, hits)
    print_context_examples("Public Verifier Context Examples", PUBLIC_VERIFIER_TERMS, hits)

    print("## Assessment")
    print()
    if private_hit_terms:
        print(f"- Private runtime dependency terms were visible in public artifacts: `{', '.join(private_hit_terms)}`.")
    else:
        print("- No exact private runtime dependency terms such as `jupnet-svm`, `jupnet-vote`, `jupnet-bls-sdk`, `jupnet-bn254`, `jupnet-merkle-tree`, `jupnet-crosschain-hash` or `jupnet-define-syscall` appeared in the saved public artifacts.")
    print("- Public verifier fingerprints remain visible in Gum/Bank/helper binaries and logs, especially BLS/Merkle/outbox strings.")
    print("- Security producer terms were either absent or appeared as generic application/staking strings, not as a Dove/JUP stake-weight implementation.")
    print("- This supports the current boundary model: public artifacts expose verifier consumption, while the root-builder, Dove set and JUP-weight source remain outside the observed public surface.")


if __name__ == "__main__":
    main()
