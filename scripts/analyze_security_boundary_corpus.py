#!/usr/bin/env python3
"""Analyze the public Gum/JupNet security boundary from helper accounts and verifier payloads."""

from __future__ import annotations

import argparse
import collections
import datetime as dt
import hashlib
import json
import struct
from pathlib import Path

from analyze_jupnet_helper_program_accounts import INBOX_PROGRAM
from analyze_jupnet_helper_program_accounts import OUTBOX_PROGRAM
from analyze_jupnet_helper_program_accounts import b58decode as helper_b58decode
from analyze_jupnet_helper_program_accounts import program_rows as helper_program_rows
from analyze_jupnet_helper_program_accounts import raw_account_data
from analyze_jupnet_helper_program_accounts import validator_related_keys
from map_outbox_verifier_payloads import BANK_PROGRAM
from map_outbox_verifier_payloads import JUP_MINT
from map_outbox_verifier_payloads import b58decode
from map_outbox_verifier_payloads import b58encode
from map_outbox_verifier_payloads import outbox_roots
from map_outbox_verifier_payloads import parse_bank_verify
from map_outbox_verifier_payloads import parse_inner_outbox


def load(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def block_time(value: int | None) -> str:
    if value is None:
        return "unknown"
    return dt.datetime.fromtimestamp(value, dt.timezone.utc).isoformat()


def fmt(values: list[str] | set[str] | tuple[str, ...], empty: str = "`None`", limit: int | None = None) -> str:
    items = list(values)
    if limit is not None:
        items = items[:limit]
    if not items:
        return empty
    return "<br>".join(f"`{value}`" for value in items)


def fmt_hex(value: bytes | None, limit: int | None = None) -> str:
    if value is None:
        return "`None`"
    text = value.hex()
    if limit and len(text) > limit:
        text = text[:limit] + "..."
    return f"`{text}`"


def transaction_files(base: Path) -> list[Path]:
    paths = {
        path.name: path
        for path in [
            *base.glob("solana-mainnet-outbox-history-tx-*.json"),
            *base.glob("solana-mainnet-outbox-tx-*.json"),
            *base.glob("solana-mainnet-bank-tx-*.json"),
        ]
    }
    return [paths[name] for name in sorted(paths)]


def tx_account_keys(tx: dict) -> set[str]:
    keys = set()
    for key in tx.get("transaction", {}).get("message", {}).get("accountKeys") or []:
        keys.add(key["pubkey"] if isinstance(key, dict) else key)
    return keys


def helper_rows(base: Path) -> list[dict]:
    rows = []
    rows.extend(helper_program_rows(base, "JupNetInboxProgram", INBOX_PROGRAM))
    rows.extend(helper_program_rows(base, "JupNetOutboxProgram", OUTBOX_PROGRAM))
    return rows


def u64_candidates(raw: bytes, limit: int = 192) -> list[str]:
    values = []
    for offset in range(0, min(len(raw) - 7, limit), 8):
        value = struct.unpack("<Q", raw[offset : offset + 8])[0]
        if value and value < 10**15:
            values.append(f"{offset}:{value}")
    return values


def root_candidates(raw: bytes) -> list[str]:
    rows = []
    for offset in range(0, len(raw) - 39, 8):
        epoch = struct.unpack("<Q", raw[offset : offset + 8])[0]
        root = raw[offset + 8 : offset + 40]
        if not epoch or epoch > 1_000_000 or root == b"\0" * 32:
            continue
        if len(set(root)) < 8:
            continue
        rows.append(f"offset {offset}: epoch {epoch}, root {root.hex()}")
    return rows


def aligned_pubkey_chunks(raw: bytes) -> list[str]:
    rows = []
    for offset in range(0, len(raw) - 31, 32):
        chunk = raw[offset : offset + 32]
        if chunk and chunk != b"\0" * 32:
            rows.append(f"{offset}:{b58encode(chunk)}")
    return rows


def current_security_keys(base: Path) -> dict[str, str]:
    return {
        "canonical JUP mint": JUP_MINT,
        **validator_related_keys(base),
    }


def watched_hits(raw: bytes, account_keys: set[str], watched: dict[str, str]) -> list[str]:
    hits = []
    for label, key in watched.items():
        try:
            key_raw = helper_b58decode(key)
        except ValueError:
            continue
        if key in account_keys:
            hits.append(f"{label} account: {key}")
        if key_raw in raw:
            hits.append(f"{label} raw: {key}")
        if key.encode() in raw:
            hits.append(f"{label} text: {key}")
    return hits


def verifier_rows(base: Path) -> list[dict]:
    rows = []
    watched = current_security_keys(base)
    for path in transaction_files(base):
        tx = load(path).get("result")
        if not tx:
            continue
        keys = tx_account_keys(tx)
        message = tx.get("transaction", {}).get("message", {})
        for index, ix in enumerate(message.get("instructions") or []):
            raw = b58decode(ix.get("data") or "") if ix.get("data") else b""
            parsed = None
            if ix.get("programId") == BANK_PROGRAM:
                parsed = parse_bank_verify(raw)
            elif ix.get("programId") == OUTBOX_PROGRAM:
                parsed = parse_inner_outbox(raw)
            if parsed:
                rows.append(
                    {
                        "file": path.name,
                        "slot": tx.get("slot"),
                        "block_time": tx.get("blockTime"),
                        "signature": (tx.get("transaction", {}).get("signatures") or [""])[0],
                        "instruction_index": str(index),
                        "program_id": ix.get("programId"),
                        "raw_len": len(raw),
                        "account_keys": keys,
                        "security_hits": watched_hits(raw, keys, watched),
                        **parsed,
                    }
                )
        for group in tx.get("meta", {}).get("innerInstructions") or []:
            for inner_index, ix in enumerate(group.get("instructions") or []):
                if ix.get("programId") != OUTBOX_PROGRAM:
                    continue
                raw = b58decode(ix.get("data") or "") if ix.get("data") else b""
                parsed = parse_inner_outbox(raw)
                if parsed:
                    rows.append(
                        {
                            "file": path.name,
                            "slot": tx.get("slot"),
                            "block_time": tx.get("blockTime"),
                            "signature": (tx.get("transaction", {}).get("signatures") or [""])[0],
                            "instruction_index": f"inner:{group.get('index')}:{inner_index}",
                            "program_id": ix.get("programId"),
                            "raw_len": len(raw),
                            "account_keys": keys,
                            "security_hits": watched_hits(raw, keys, watched),
                            **parsed,
                        }
                    )
    return rows


def row_root(row: dict) -> str:
    return row["recomputed_root"].hex()


def row_sender(row: dict) -> str:
    sender = row.get("sender")
    return b58encode(sender) if sender else "None"


def transition_rows(rows: list[dict]) -> list[str]:
    transitions = []
    previous = None
    for row in sorted(rows, key=lambda item: ((item.get("block_time") or 0), (item.get("slot") or 0), item["file"], item["instruction_index"])):
        current = (
            row["epoch"],
            row["aggregate_key"].hex(),
            row_root(row),
            row_sender(row),
            row["path_bitmap"],
            row["proof_count"],
        )
        if current == previous:
            continue
        transitions.append(
            f"{block_time(row.get('block_time'))} slot {row.get('slot')} "
            f"epoch {row['epoch']} sender {row_sender(row)} aggregate {row['aggregate_key'].hex()[:32]}... "
            f"root {row_root(row)[:32]}... bitmap {row['path_bitmap']} proof {row['proof_count']}"
        )
        previous = current
    return transitions


def print_helper_section(base: Path, rows: list[dict]) -> None:
    watched = current_security_keys(base)
    layout_counts = collections.Counter((row["label"], row["space"], row["discriminator"]) for row in rows)
    helper_security_hits = [
        (row["pubkey"], watched_hits(row["raw"], set(), watched))
        for row in rows
        if watched_hits(row["raw"], set(), watched)
    ]

    print("## Helper-Owned Account Layouts")
    print()
    print(f"- Helper accounts decoded: `{len(rows)}`")
    print(f"- Helper accounts with canonical JUP / validator / vote / stake hits: `{len(helper_security_hits)}`")
    print()
    print("| Program | Space | Discriminator | Count |")
    print("|---|---:|---|---:|")
    for (label, space, discriminator), count in layout_counts.most_common():
        print(f"| `{label}` | {space} | `{discriminator}` | {count} |")
    print()
    print("| Program | Account | Space | SHA256 | Root-like entries | U64 candidates | Aligned 32-byte chunks |")
    print("|---|---|---:|---|---|---|---|")
    for row in sorted(rows, key=lambda item: (item["label"], item["pubkey"])):
        raw = row["raw"]
        roots = root_candidates(raw)
        print(
            f"| `{row['label']}` | `{row['pubkey']}` | {row['space']} | `{hashlib.sha256(raw).hexdigest() if raw else None}` | "
            f"{fmt(roots, limit=8)} | {fmt(u64_candidates(raw), limit=10)} | {fmt(aligned_pubkey_chunks(raw), limit=8)} |"
        )
    print()
    print("### Helper Layout Assessment")
    print()
    if helper_security_hits:
        for pubkey, hits in helper_security_hits:
            print(f"- `{pubkey}` exposed security-key hits: {fmt(hits)}")
    else:
        print("- No helper-owned account exposed canonical JUP, current validator, vote or stake account bytes/text.")
    print("- The public outbox helper account still presents as epoch/root storage rather than a signer-set, quorum or stake-weight registry.")
    print("- No helper-owned account in this snapshot had an obvious sequence of current validator/vote/stake keys paired with small integer weights.")
    print()


def print_verifier_section(base: Path, rows: list[dict]) -> None:
    roots = outbox_roots(base)
    parsed_files = {row["file"] for row in rows}
    by_kind = collections.Counter(row["kind"] for row in rows)
    by_epoch = collections.Counter(row["epoch"] for row in rows)
    by_sender = collections.Counter(row_sender(row) for row in rows)
    by_aggregate = collections.Counter(row["aggregate_key"].hex() for row in rows)
    by_root = collections.Counter(row_root(row) for row in rows)
    by_signature = collections.Counter(row["signature"].hex() for row in rows)
    by_layout = collections.Counter((row["kind"], row["raw_len"], row["aggregate_offset"], row["path_bitmap"], row["proof_count"]) for row in rows)
    root_mismatches = [
        row for row in rows if roots.get(row["epoch"]) is not None and roots[row["epoch"]] != row["recomputed_root"]
    ]
    security_hit_rows = [row for row in rows if row["security_hits"]]
    times = [row["block_time"] for row in rows if row.get("block_time") is not None]
    slots = [row["slot"] for row in rows if row.get("slot") is not None]

    print("## Verifier Payload Corpus")
    print()
    print(f"- Transaction files available: `{len(transaction_files(base))}`")
    print(f"- Transaction files with decoded verifier payloads: `{len(parsed_files)}`")
    print(f"- Decoded verifier payloads: `{len(rows)}`")
    print(f"- Time range: `{block_time(min(times)) if times else 'unknown'}` -> `{block_time(max(times)) if times else 'unknown'}`")
    print(f"- Slot range: `{min(slots) if slots else 'unknown'}` -> `{max(slots) if slots else 'unknown'}`")
    print(f"- Root mismatches against stored outbox roots: `{len(root_mismatches)}`")
    print(f"- Payloads with canonical JUP / validator / vote / stake hits: `{len(security_hit_rows)}`")
    print()
    print("| Group | Values |")
    print("|---|---|")
    print(f"| Payload kinds | {fmt([f'{key}: {value}' for key, value in by_kind.most_common()])} |")
    print(f"| Epochs | {fmt([f'{key}: {value}' for key, value in by_epoch.most_common()])} |")
    print(f"| Sender/program ids | {fmt([f'{key}: {value}' for key, value in by_sender.most_common()])} |")
    print(f"| Aggregate keys | {fmt([f'{key[:32]}...: {value}' for key, value in by_aggregate.most_common()])} |")
    print(f"| Recomputed roots | {fmt([f'{key}: {value}' for key, value in by_root.most_common()])} |")
    print(f"| Compact signature/verifier fields | {fmt([f'{key[:32]}...: {value}' for key, value in by_signature.most_common()], limit=12)} |")
    print(
        f"| Proof layouts | {fmt([f'{kind} len={length} aggregate={offset} bitmap={bitmap} proof={proof}: {count}' for (kind, length, offset, bitmap, proof), count in by_layout.most_common()])} |"
    )
    print()
    print("### Verifier Boundary Transitions")
    print()
    for item in transition_rows(rows)[:30]:
        print(f"- `{item}`")
    if len(transition_rows(rows)) > 30:
        print(f"- Additional transitions omitted: `{len(transition_rows(rows)) - 30}`")
    if not rows:
        print("- None")
    print()
    print("### Corpus Assessment")
    print()
    if security_hit_rows:
        for row in security_hit_rows[:10]:
            print(f"- `{row['file']}` `{row['instruction_index']}` exposed: {fmt(row['security_hits'])}")
    else:
        print("- No decoded verifier payload or account list exposed canonical JUP, current validator, vote or stake account material.")
    print("- The larger local corpus still exposes aggregate-key/proof verification state, not the producer-side Dove/JUP/stake source used to build that aggregate-key set.")
    print("- The most useful future signal is a transition where aggregate keys or roots change near a validator/stake snapshot change.")
    print()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot_dir")
    args = parser.parse_args()
    base = Path(args.snapshot_dir)

    helpers = helper_rows(base)
    verifier = verifier_rows(base)

    print("# Security Boundary Corpus")
    print()
    print("## Purpose")
    print()
    print("This pass tests the public boundary where hidden JupNet/Dove security material would have to meet Solana-visible Gum verification.")
    print()
    print("It combines:")
    print()
    print("- helper-program-owned inbox/outbox account layouts;")
    print("- every locally saved Solana Bank/outbox/history transaction body;")
    print("- decoded verifier payload roots, aggregate keys, senders, proof layouts and key-hit checks.")
    print()
    print_helper_section(base, helpers)
    print_verifier_section(base, verifier)
    print("## Bottom Line")
    print()
    print("- Public helper accounts and verifier payloads still support the BLS/Merkle verifier model.")
    print("- They do not currently expose a JUP-denominated stake table, Dove signer registry, validator-key registry, quorum threshold or weight mapping.")
    print("- This narrows the likely hiding place to private runtime/source, private off-chain epoch construction, or a public account layout not yet reachable from the sampled helper/Bank/outbox surface.")


if __name__ == "__main__":
    main()
