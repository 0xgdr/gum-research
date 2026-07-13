#!/usr/bin/env python3
"""Analyze current state of Bank/Gum accounts created in sampled transactions."""

from __future__ import annotations

import argparse
import base64
import collections
import hashlib
import json
import struct
from pathlib import Path

from analyze_bank_account_graph import b58decode
from analyze_bank_account_graph import b58encode
from analyze_bank_request_message_correlation import decoded_fields
from analyze_bank_request_message_correlation import load
from analyze_bank_request_message_correlation import manifest_files
from analyze_bank_request_message_correlation import tx_result
from analyze_root_update_authority_graph import JUP_MINT
from analyze_root_update_authority_graph import validator_related_keys


BK1PDA = "bk1PDAkbHEBGtVRiM94Lzets8gVFP7FgySyfkAc8MPN"
BANKK = "BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ"
SPL_TOKEN = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
USDC = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
WRAPPED_SOL = "So11111111111111111111111111111111111111112"


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
        "state": state,
    }


def watched_decoded_fields(base: Path) -> dict[str, dict]:
    watched = {}

    def add_row(surface: str, filename: str, tx: dict) -> None:
        for label, item in decoded_fields(tx).items():
            if label not in {"message_hash", "withdrawal_request_pubkey", "jupnet", "recipient", "mint", "impl program key"}:
                continue
            key = f"{surface}:{filename}:{label}:{item.get('base58') or item.get('hex')}"
            watched[key] = {
                "surface": surface,
                "file": filename,
                "label": label,
                "value": item.get("base58") or item.get("hex"),
                "raw": item.get("bytes") or b"",
            }

    for filename in manifest_files(base, "bank-withdrawal-cohort"):
        tx = tx_result(base, filename)
        if tx:
            add_row("bk1PDA", filename, tx)
    funding_manifest = load(base / "solana-mainnet-root-submitter-funding-history-manifest.json")
    for submitter in funding_manifest.get("submitters") or []:
        for filename in submitter.get("positive_delta_files") or []:
            tx = tx_result(base, filename)
            if tx:
                add_row("root_submitter_setup", filename, tx)
    return watched


def byte_hits(raw: bytes, watched: dict[str, dict]) -> list[str]:
    hits = []
    for item in watched.values():
        needle = item["raw"]
        if not needle:
            continue
        offset = raw.find(needle)
        if offset != -1:
            hits.append(f"{item['surface']} {item['label']} {item['value']} @ {offset}")
    return hits


def known_key_hits(raw: bytes, base: Path) -> list[str]:
    watched = {
        "canonical JUP mint": JUP_MINT,
        "USDC mint": USDC,
        "wrapped SOL mint": WRAPPED_SOL,
        "bk1PDA": BK1PDA,
        "BankK": BANKK,
        "SPL Token": SPL_TOKEN,
    }
    for key, role in validator_related_keys(base).items():
        watched[f"current {role}"] = key
    hits = []
    for label, key in watched.items():
        try:
            needle = b58decode(key)
        except ValueError:
            continue
        if needle and needle in raw:
            hits.append(f"{label}: {key}")
        if key.encode() in raw:
            hits.append(f"{label} text: {key}")
    return hits


def account_rows(base: Path) -> list[dict]:
    data = load(base / "solana-mainnet-getMultipleAccounts-CreatedBankStateAccounts.json")
    accounts = data.get("accounts") or []
    metadata = data.get("metadata") or {}
    values = data.get("values") or []
    watched_fields = watched_decoded_fields(base)
    rows = []
    for account, value in zip(accounts, values):
        raw = raw_account_data(value)
        owner = value.get("owner") if value else None
        token = token_account(raw) if owner == SPL_TOKEN else None
        decoded_hits = byte_hits(raw, watched_fields)
        key_hits = known_key_hits(raw, base)
        if not value:
            classification = "missing-or-closed"
        elif owner == SPL_TOKEN and token:
            classification = "SPL token account"
        elif owner == BK1PDA:
            classification = "bk1PDA-owned state"
        elif owner == BANKK:
            classification = "BankK-owned state"
        else:
            classification = "other"
        rows.append(
            {
                "account": account,
                "value": value,
                "raw": raw,
                "metadata": metadata.get(account) or {},
                "classification": classification,
                "token": token,
                "decoded_hits": decoded_hits,
                "key_hits": key_hits,
                "strings": printable_strings(raw),
                "sha256": hashlib.sha256(raw).hexdigest() if raw else None,
                "anchor_discriminator": raw[:8].hex() if len(raw) >= 8 else None,
            }
        )
    return rows


def fmt(values, empty: str = "`None`", limit: int | None = None) -> str:
    items = sorted(values) if isinstance(values, set) else list(values)
    items = [str(item) for item in items if item]
    if limit is not None:
        items = items[:limit]
    if not items:
        return empty
    return "<br>".join(f"`{item}`" for item in items)


def fmt_counter(counter: collections.Counter, limit: int | None = None) -> str:
    return fmt([f"{key}: {value}" for key, value in counter.most_common(limit)])


def creation_summary(row: dict) -> str:
    meta = row["metadata"]
    pieces = []
    for surface, count in (meta.get("surfaces") or {}).items():
        pieces.append(f"{surface}: {count}")
    for space, count in (meta.get("spaces") or {}).items():
        pieces.append(f"space {space}: {count}")
    return "<br>".join(f"`{piece}`" for piece in pieces) if pieces else "`None`"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot_dir")
    args = parser.parse_args()
    base = Path(args.snapshot_dir)
    rows = account_rows(base)

    class_counts = collections.Counter(row["classification"] for row in rows)
    owner_counts = collections.Counter((row["value"] or {}).get("owner") for row in rows)
    space_counts = collections.Counter((row["value"] or {}).get("space") for row in rows if row["value"])
    decoded_hit_rows = [row for row in rows if row["decoded_hits"]]
    high_value_hits = [
        hit
        for row in rows
        for hit in row["decoded_hits"]
        if any(label in hit for label in ("message_hash", "withdrawal_request_pubkey", "jupnet", "recipient"))
    ]
    bankk_cross_surface_hits = [
        hit
        for row in rows
        for hit in row["decoded_hits"]
        if row["classification"] == "BankK-owned state"
        and any(label in hit for label in ("message_hash", "withdrawal_request_pubkey", "jupnet", "recipient"))
    ]
    bk1_request_state_hits = [
        hit
        for row in rows
        for hit in row["decoded_hits"]
        if row["classification"] == "bk1PDA-owned state"
        and any(label in hit for label in ("withdrawal_request_pubkey", "jupnet", "impl program key"))
    ]
    jup_hits = [hit for row in rows for hit in row["key_hits"] if "canonical JUP" in hit]
    validator_hits = [
        hit
        for row in rows
        for hit in row["key_hits"]
        if any(role in hit for role in ("current validator", "current vote", "current native stake"))
    ]

    print("# Created Bank State Account Correlation")
    print()
    print("## Scope")
    print()
    print(f"- Created accounts fetched: `{len(rows)}`")
    print(f"- Current accounts missing/closed: `{class_counts.get('missing-or-closed', 0)}`")
    print(f"- Accounts with any decoded `bk1PDA...` field bytes: `{len(decoded_hit_rows)}`")
    print(f"- High-value decoded request/message/recipient hits: `{len(high_value_hits)}`")
    print(f"- Cross-surface high-value hits in current `BankK...` state: `{len(bankk_cross_surface_hits)}`")
    print(f"- Decoded request/implementation hits retained in current `bk1PDA...` request state: `{len(bk1_request_state_hits)}`")
    print(f"- Canonical JUP hits: `{len(jup_hits)}`")
    print(f"- Current validator/vote/stake hits: `{len(validator_hits)}`")
    print()

    print("## Current Account Summary")
    print()
    print(f"- Classification: {fmt_counter(class_counts)}")
    print(f"- Owners: {fmt_counter(owner_counts)}")
    print(f"- Current account spaces: {fmt_counter(space_counts)}")
    print()

    print("## Account Rows")
    print()
    print("| Account | Created as | Current owner | Current space | Class | SHA256 | Decoded field hits | Key hits |")
    print("|---|---|---|---:|---|---|---|---|")
    for row in rows:
        value = row["value"] or {}
        print(
            f"| `{row['account']}` | {creation_summary(row)} | `{value.get('owner')}` | "
            f"{value.get('space')} | {row['classification']} | `{row['sha256']}` | "
            f"{fmt(row['decoded_hits'], limit=6)} | {fmt(row['key_hits'], limit=6)} |"
        )
    print()

    print("## Token Accounts")
    print()
    token_rows = [row for row in rows if row["token"]]
    if token_rows:
        print("| Account | Mint | Owner | Amount | Created as |")
        print("|---|---|---|---:|---|")
        for row in token_rows:
            token = row["token"]
            print(
                f"| `{row['account']}` | `{token['mint']}` | `{token['owner']}` | "
                f"{token['amount']} | {creation_summary(row)} |"
            )
    else:
        print("- None")
    print()

    print("## Assessment")
    print()
    if bankk_cross_surface_hits:
        print("- At least one current `BankK...` state account stores high-value decoded request/message/recipient bytes from the `bk1PDA...` surface.")
    else:
        print("- No current `BankK...` state account stores decoded `bk1PDA...` message hashes, withdrawal-request pubkeys, `jupnet` pubkeys or recipients.")
    if bk1_request_state_hits:
        print("- Current `bk1PDA...` 72-byte request accounts do retain the withdrawal implementation key and some request/`jupnet` pubkeys, confirming that request state is publicly decodable on that surface.")
    if jup_hits or validator_hits:
        print("- Watched canonical JUP or current validator/vote/stake material appeared in fetched created account state.")
    else:
        print("- No fetched created account contains canonical JUP or current validator/vote/stake key material.")
    print("- Missing/closed accounts are expected for short-lived request or token accounts; current account state may not preserve all transaction-time state.")
    print("- If the public join exists only in transient account data that is later closed or rewritten, transaction-time account snapshots would be needed to prove it.")


if __name__ == "__main__":
    main()
