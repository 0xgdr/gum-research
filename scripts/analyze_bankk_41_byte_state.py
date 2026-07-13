#!/usr/bin/env python3
"""Decode and correlate 41-byte BankK-owned state accounts."""

from __future__ import annotations

import argparse
import base64
import collections
import hashlib
import json
from pathlib import Path

from analyze_bank_account_graph import b58decode
from analyze_bank_account_graph import b58encode
from analyze_bank_request_message_correlation import load
from analyze_bank_request_message_correlation import raw_hit_locations
from analyze_bank_request_message_correlation import rows as correlation_rows
from analyze_created_bank_state_accounts import BANKK
from analyze_created_bank_state_accounts import raw_account_data
from analyze_root_update_authority_graph import JUP_MINT
from analyze_root_update_authority_graph import validator_related_keys
from map_outbox_verifier_payloads import collect_rows as verifier_payload_rows
from map_outbox_verifier_payloads import outbox_roots


BANKK_41_DISCRIMINATOR = "d201f3aeaed73c91"
KNOWN_PROGRAMS = {
    "Bank Program": BANKK,
    "canonical JUP mint": JUP_MINT,
    "Jupiter v6 aggregator": "JUP6LkbZbjS1jKKwapdHNy74zcZ3tLUZoi5QNyVTaV4",
    "observed Bank signer/payer": "JUPW3tHBxmNRzVnLmTyYUsUDB6izZSEtupY6znBC5mo",
    "JupNet inbox helper": "JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw",
    "JupNet outbox helper": "jnoUtncGR9ZCCMixtys6Gzy5coTo6mnmUZuEHRQFTFV",
    "SPL Token": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA",
    "System Program": "11111111111111111111111111111111",
}


def account_values_from_created_state(base: Path) -> list[dict]:
    data = load(base / "solana-mainnet-getMultipleAccounts-CreatedBankStateAccounts.json")
    accounts = data.get("accounts") or []
    values = data.get("values") or []
    metadata = data.get("metadata") or {}
    rows = []
    for account, value in zip(accounts, values):
        if not value:
            continue
        raw = raw_account_data(value)
        if value.get("owner") == BANKK and len(raw) == 41:
            rows.append(
                {
                    "account": account,
                    "source": "created-account-current-state",
                    "count": None,
                    "value": value,
                    "raw": raw,
                    "metadata": metadata.get(account) or {},
                }
            )
    return rows


def account_values_from_recurring_state(base: Path) -> list[dict]:
    data = load(base / "solana-mainnet-getMultipleAccounts-BankRecurringAccounts.json")
    accounts = data.get("accounts") or []
    values = ((data.get("response") or {}).get("result") or {}).get("value") or []
    counts = data.get("counts") or {}
    rows = []
    for account, value in zip(accounts, values):
        if not value:
            continue
        raw = raw_account_data(value)
        if value.get("owner") == BANKK and len(raw) == 41:
            rows.append(
                {
                    "account": account,
                    "source": "recurring-account-current-state",
                    "count": counts.get(account),
                    "value": value,
                    "raw": raw,
                    "metadata": {},
                }
            )
    return rows


def decode_41(row: dict) -> dict:
    raw = row["raw"]
    embedded = raw[9:41]
    return {
        **row,
        "discriminator": raw[:8].hex(),
        "flag": raw[8],
        "embedded_raw": embedded,
        "embedded_hex": embedded.hex(),
        "embedded_pubkey": b58encode(embedded),
        "sha256": hashlib.sha256(raw).hexdigest(),
    }


def dedupe_rows(rows: list[dict]) -> list[dict]:
    by_account = {}
    for row in rows:
        existing = by_account.get(row["account"])
        if not existing:
            by_account[row["account"]] = row
            continue
        existing["source"] = f"{existing['source']}+{row['source']}"
        if row.get("count"):
            existing["count"] = row["count"]
    return sorted(by_account.values(), key=lambda item: item["account"])


def creation_summary(row: dict) -> str:
    metadata = row.get("metadata") or {}
    pieces = []
    for surface, count in (metadata.get("surfaces") or {}).items():
        pieces.append(f"{surface}: {count}")
    for space, count in (metadata.get("spaces") or {}).items():
        pieces.append(f"space {space}: {count}")
    if row.get("count") is not None:
        pieces.append(f"recurring count: {row['count']}")
    return "<br>".join(f"`{piece}`" for piece in pieces) if pieces else "`None`"


def known_key_matches(base: Path, embedded_pubkey: str, embedded_raw: bytes) -> list[str]:
    watched = dict(KNOWN_PROGRAMS)
    for key, role in validator_related_keys(base).items():
        watched[f"current {role}"] = key
    hits = []
    for label, key in watched.items():
        if embedded_pubkey == key:
            hits.append(f"{label}: exact pubkey")
            continue
        try:
            if embedded_raw == b58decode(key):
                hits.append(f"{label}: exact raw key")
        except ValueError:
            pass
    return hits


def transaction_matches(base: Path, decoded: dict) -> list[str]:
    matches = []
    embedded_pubkey = decoded["embedded_pubkey"]
    embedded_raw = decoded["embedded_raw"]
    for row in correlation_rows(base):
        instructions = ",".join(row["instructions"]) or "unknown"
        if embedded_pubkey in row["keys"]:
            matches.append(f"{row['surface']} {instructions} account-key {row['signature'][:8]}")
        if embedded_pubkey == row["fee_payer"]:
            matches.append(f"{row['surface']} {instructions} fee-payer {row['signature'][:8]}")
        if embedded_pubkey in row["signers"]:
            matches.append(f"{row['surface']} {instructions} signer {row['signature'][:8]}")
        for transfer in row["token_transfers"]:
            for role in ("source", "destination", "authority"):
                if embedded_pubkey == transfer.get(role):
                    mint = transfer.get("mint")
                    matches.append(f"{row['surface']} {instructions} token-{role} {mint} {row['signature'][:8]}")
        for label, field in row["fields"].items():
            if embedded_pubkey == field.get("base58") or embedded_raw == field.get("bytes"):
                matches.append(f"{row['surface']} {instructions} decoded-field {label} {row['signature'][:8]}")
        for location in raw_hit_locations(embedded_raw, row):
            matches.append(f"{row['surface']} {instructions} raw-payload {location} {row['signature'][:8]}")
    return sorted(set(matches))


def verifier_matches(base: Path, decoded: dict) -> list[str]:
    matches = []
    embedded = decoded["embedded_raw"]
    embedded_pubkey = decoded["embedded_pubkey"]
    roots = outbox_roots(base)
    for epoch, root in roots.items():
        if embedded == root:
            matches.append(f"outbox-root epoch {epoch}")
    for row in verifier_payload_rows(base):
        fields = {
            "message_hash": row.get("message_hash"),
            "sender": row.get("sender"),
            "aggregate_key_first32": (row.get("aggregate_key") or b"")[:32],
            "aggregate_key_last32": (row.get("aggregate_key") or b"")[32:64],
            "signature_field": row.get("signature"),
            "recomputed_root": row.get("recomputed_root"),
        }
        for index, node in enumerate(row.get("proof_nodes") or []):
            fields[f"proof_node_{index}"] = node
        for label, value in fields.items():
            if value and embedded == value:
                matches.append(f"{row['kind']} {label} {row['signature'][:8]}")
        if embedded_pubkey in row.get("account_keys", set()):
            matches.append(f"{row['kind']} account-key {row['signature'][:8]}")
    return sorted(set(matches))


def decoded_request_field_matches(base: Path, decoded: dict) -> list[str]:
    matches = []
    embedded = decoded["embedded_raw"]
    embedded_pubkey = decoded["embedded_pubkey"]
    for row in correlation_rows(base):
        for label, field in row["fields"].items():
            if embedded == field.get("bytes") or embedded_pubkey == field.get("base58"):
                matches.append(f"{row['surface']} {label} {row['signature'][:8]}")
    return sorted(set(matches))


def fmt(values, empty: str = "`None`", limit: int | None = None) -> str:
    items = list(values)
    if limit is not None:
        items = items[:limit]
    if not items:
        return empty
    return "<br>".join(f"`{item}`" for item in items)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot_dir")
    args = parser.parse_args()
    base = Path(args.snapshot_dir)

    decoded = [
        decode_41(row)
        for row in dedupe_rows(account_values_from_created_state(base) + account_values_from_recurring_state(base))
    ]
    for row in decoded:
        row["known_key_matches"] = known_key_matches(base, row["embedded_pubkey"], row["embedded_raw"])
        row["transaction_matches"] = transaction_matches(base, row)
        row["verifier_matches"] = verifier_matches(base, row)
        row["decoded_request_matches"] = decoded_request_field_matches(base, row)

    discriminator_counts = collections.Counter(row["discriminator"] for row in decoded)
    flag_counts = collections.Counter(row["flag"] for row in decoded)
    embedded_counter = collections.Counter(row["embedded_pubkey"] for row in decoded)
    transaction_hit_rows = [row for row in decoded if row["transaction_matches"]]
    account_key_hit_rows = [
        row for row in decoded if any("account-key" in hit for hit in row["transaction_matches"])
    ]
    raw_payload_hit_rows = [
        row for row in decoded if any("raw-payload" in hit for hit in row["transaction_matches"])
    ]
    verifier_hit_rows = [row for row in decoded if row["verifier_matches"]]
    decoded_request_hit_rows = [row for row in decoded if row["decoded_request_matches"]]
    security_hit_rows = [row for row in decoded if row["known_key_matches"]]

    print("# BankK 41-Byte State Layout")
    print()
    print("## Scope")
    print()
    print(f"- 41-byte `BankK...` accounts analyzed: `{len(decoded)}`")
    print(f"- Unique embedded 32-byte values: `{len(embedded_counter)}`")
    print(f"- Discriminator groups: `{dict(discriminator_counts)}`")
    print(f"- Flag byte groups: `{dict(flag_counts)}`")
    print(f"- Embedded values with any sampled transaction hit: `{len(transaction_hit_rows)}`")
    print(f"- Embedded values seen as sampled transaction account keys: `{len(account_key_hit_rows)}`")
    print(f"- Embedded values seen in sampled Bank/inbox raw payloads: `{len(raw_payload_hit_rows)}`")
    print(f"- Embedded values matching decoded `bk1PDA...` request fields: `{len(decoded_request_hit_rows)}`")
    print(f"- Embedded values matching verifier payload/root fields: `{len(verifier_hit_rows)}`")
    print(f"- Embedded values matching canonical JUP / current validator / vote / stake keys: `{len(security_hit_rows)}`")
    print()

    print("## Layout")
    print()
    print("| Offset | Length | Field | Observed |")
    print("|---:|---:|---|---|")
    print(f"| 0 | 8 | account discriminator | `{dict(discriminator_counts)}` |")
    print(f"| 8 | 1 | status/version flag | `{dict(flag_counts)}` |")
    print("| 9 | 32 | embedded id/pubkey candidate | unique per account in this sample |")
    print()

    print("## Account Rows")
    print()
    print("| Account | Source | Created as | Discriminator | Flag | Embedded 32-byte value | Embedded as pubkey | Tx/raw matches | Verifier/root matches | Known security-key matches |")
    print("|---|---|---|---|---:|---|---|---|---|---|")
    for row in decoded:
        print(
            f"| `{row['account']}` | `{row['source']}` | {creation_summary(row)} | "
            f"`{row['discriminator']}` | {row['flag']} | `{row['embedded_hex']}` | "
            f"`{row['embedded_pubkey']}` | {fmt(row['transaction_matches'], limit=5)} | "
            f"{fmt(row['verifier_matches'], limit=5)} | {fmt(row['known_key_matches'], limit=5)} |"
        )
    print()

    print("## Embedded Value Groups")
    print()
    print("| Embedded pubkey interpretation | Count |")
    print("|---|---:|")
    for value, count in embedded_counter.most_common():
        print(f"| `{value}` | {count} |")
    print()

    print("## Assessment")
    print()
    if decoded and set(discriminator_counts) == {BANKK_41_DISCRIMINATOR} and set(flag_counts) == {1}:
        print("- The sampled 41-byte `BankK...` state has a stable compact layout: 8-byte discriminator, one flag byte set to `1`, then one 32-byte value.")
    if raw_payload_hit_rows:
        print("- The 32-byte field is a Bank-local message/state identifier in this sample: it is retained in current 41-byte state and reappears in sampled `BankK...` and `JNiN...` inbox instruction/log payloads.")
    elif transaction_hit_rows:
        print("- The 32-byte field reappears somewhere in sampled Bank transactions, but not in the verifier/root fields checked here.")
    else:
        print("- The 32-byte field did not appear in sampled transaction account keys or raw payloads.")
    if decoded_request_hit_rows or verifier_hit_rows:
        print("- At least one 32-byte field matched a decoded request, verifier payload or outbox-root field; inspect rows above.")
    else:
        print("- The 32-byte field did not match decoded `bk1PDA...` request fields, verifier message hashes, aggregate-key halves, compact verifier fields, proof nodes or stored outbox roots.")
    if security_hit_rows:
        print("- At least one 41-byte state value matched watched JUP or validator/vote/stake material.")
    else:
        print("- No 41-byte state value matched canonical JUP or current validator/vote/stake keys.")
    print("- This makes the 41-byte layout useful for Bank-local account linkage, but it does not expose the missing Gum security/staking source in the current public sample.")


if __name__ == "__main__":
    main()
