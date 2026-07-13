#!/usr/bin/env python3
"""Analyze BankK local-id lifecycles over a wider transaction window."""

from __future__ import annotations

import argparse
import base64
import collections
from pathlib import Path

from analyze_bank_account_graph import b58encode
from analyze_bank_request_message_correlation import load
from analyze_bank_request_message_correlation import raw_hit_locations
from analyze_bank_request_message_correlation import row_for
from analyze_bank_request_message_correlation import tx_result
from analyze_bankk_41_byte_state import account_values_from_created_state
from analyze_bankk_41_byte_state import account_values_from_recurring_state
from analyze_bankk_41_byte_state import decode_41
from analyze_bankk_41_byte_state import dedupe_rows
from analyze_bankk_41_byte_state import known_key_matches
from analyze_bankk_local_id_lifecycle import BANKK
from analyze_bankk_local_id_lifecycle import INBOX
from analyze_bankk_local_id_lifecycle import OUTBOX
from analyze_bankk_local_id_lifecycle import event_summary
from analyze_bankk_local_id_lifecycle import fmt
from analyze_bankk_local_id_lifecycle import fmt_counter
from analyze_bankk_local_id_lifecycle import parse_program
from analyze_bankk_local_id_lifecycle import phase_for
from analyze_created_bank_state_accounts import raw_account_data
from analyze_root_update_authority_graph import block_time
from analyze_root_update_authority_graph import root_update_rows
from map_outbox_verifier_payloads import outbox_roots
from map_outbox_verifier_payloads import parse_bank_verify


def wide_transaction_rows(base: Path, prefix: str) -> list[dict]:
    manifest = load(base / f"solana-mainnet-{prefix}-manifest.json")
    rows = []
    for filename in manifest.get("transaction_files") or []:
        tx = tx_result(base, filename)
        if tx:
            rows.append(row_for("BankKWide", filename, tx))
    return rows


def wide_created_41_rows(base: Path, state_name: str) -> list[dict]:
    data = load(base / f"solana-mainnet-getMultipleAccounts-{state_name}.json")
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
                    "source": "wide-window-created-current-state",
                    "count": None,
                    "value": value,
                    "raw": raw,
                    "metadata": metadata.get(account) or {},
                }
            )
    return rows


def local_ids(base: Path, state_name: str) -> list[dict]:
    return [
        decode_41(row)
        for row in dedupe_rows(
            account_values_from_created_state(base)
            + account_values_from_recurring_state(base)
            + wide_created_41_rows(base, state_name)
        )
    ]


def payload_candidate_local_ids(rows: list[dict]) -> list[dict]:
    candidates = {}
    for row in rows:
        phase = phase_for(row)
        for blob in row["raw_blobs"]:
            if blob.get("program") != BANKK:
                continue
            offsets = []
            if phase in {"withdraw/inbox", "rfq/inbox", "swap/inbox", "metadata"}:
                offsets.append(("operation-offset-16", 16))
            if phase == "verify-request":
                offsets.append(("verify-offset-54", 54))
            for label, offset in offsets:
                raw = blob["raw"]
                if len(raw) < offset + 32:
                    continue
                embedded = raw[offset : offset + 32]
                if embedded == b"\0" * 32:
                    continue
                key = embedded.hex()
                row_ = candidates.setdefault(
                    key,
                    {
                        "account": f"payload:{b58encode(embedded)}",
                        "source": "wide-window-payload-candidate",
                        "count": 0,
                        "value": None,
                        "raw": b"",
                        "metadata": {},
                        "discriminator": None,
                        "flag": None,
                        "embedded_raw": embedded,
                        "embedded_hex": key,
                        "embedded_pubkey": b58encode(embedded),
                        "sha256": None,
                        "candidate_offsets": collections.Counter(),
                    },
                )
                row_["count"] += 1
                row_["candidate_offsets"][label] += 1
    out = []
    for row in candidates.values():
        row["candidate_offsets"] = dict(row["candidate_offsets"])
        out.append(row)
    return sorted(out, key=lambda item: item["embedded_pubkey"])


def verifier_field_matches_for_rows(rows: list[dict], local_id: dict) -> list[str]:
    embedded = local_id["embedded_raw"]
    hits = []
    for row in rows:
        for blob in row["raw_blobs"]:
            if blob.get("program") != BANKK:
                continue
            parsed = parse_bank_verify(blob["raw"])
            if not parsed:
                continue
            fields = {
                "message_hash": parsed.get("message_hash"),
                "aggregate_key_first32": (parsed.get("aggregate_key") or b"")[:32],
                "aggregate_key_last32": (parsed.get("aggregate_key") or b"")[32:64],
                "signature_field": parsed.get("signature"),
                "recomputed_root": parsed.get("recomputed_root"),
            }
            for index, node in enumerate(parsed.get("proof_nodes") or []):
                fields[f"proof_node_{index}"] = node
            for label, value in fields.items():
                if value and value == embedded:
                    hits.append(f"{row['filename']} {row['signature'][:8]} {label}")
    return sorted(set(hits))


def root_matches(base: Path, local_id: dict) -> list[str]:
    embedded = local_id["embedded_raw"]
    return [f"outbox-root epoch {epoch}" for epoch, root in outbox_roots(base).items() if root == embedded]


def decoded_field_matches(rows: list[dict], local_id: dict) -> list[str]:
    embedded = local_id["embedded_raw"]
    embedded_pubkey = local_id["embedded_pubkey"]
    hits = []
    for row in rows:
        for label, field in row["fields"].items():
            if embedded == field.get("bytes") or embedded_pubkey == field.get("base58"):
                hits.append(f"{row['surface']} {label} {row['signature'][:8]}")
    return sorted(set(hits))


def hit_events(rows: list[dict], local_id: dict) -> list[dict]:
    events = []
    embedded = local_id["embedded_raw"]
    embedded_pubkey = local_id["embedded_pubkey"]
    for row in rows:
        locations = raw_hit_locations(embedded, row)
        key_roles = []
        if embedded_pubkey in row["keys"]:
            key_roles.append("account-key")
        if embedded_pubkey == row["fee_payer"]:
            key_roles.append("fee-payer")
        if embedded_pubkey in row["signers"]:
            key_roles.append("signer")
        transfer_roles = []
        for transfer in row["token_transfers"]:
            for role in ("source", "destination", "authority"):
                if embedded_pubkey == transfer.get(role):
                    transfer_roles.append(f"token-{role}:{transfer.get('mint')}")
        decoded_fields = []
        for label, field in row["fields"].items():
            if embedded == field.get("bytes") or embedded_pubkey == field.get("base58"):
                decoded_fields.append(label)
        if not (locations or key_roles or transfer_roles or decoded_fields):
            continue
        events.append(
            {
                "surface": row["surface"],
                "file": row["filename"],
                "signature": row["signature"],
                "slot": row["slot"],
                "time": row["time"],
                "phase": phase_for(row),
                "instructions": row["instructions"],
                "submit_inbox": row["submit_inbox"],
                "verify_outbox": row["verify_outbox"],
                "signature_verified": row["signature_verified"],
                "locations": locations,
                "programs": sorted({parse_program(location) for location in locations}),
                "key_roles": key_roles,
                "transfer_roles": transfer_roles,
                "decoded_fields": decoded_fields,
            }
        )
    return sorted(events, key=lambda item: ((item["slot"] or 0), item["signature"], item["phase"]))


def lifecycle_rows(base: Path, prefix: str, state_name: str) -> tuple[list[dict], list[dict]]:
    tx_rows = wide_transaction_rows(base, prefix)
    roots = root_update_rows(base)
    roots_by_slot = collections.defaultdict(list)
    for row in roots:
        roots_by_slot[row["slot"]].append(row)

    local_id_rows = dedupe_rows(local_ids(base, state_name) + payload_candidate_local_ids(tx_rows))
    output = []
    for local_id in local_id_rows:
        events = hit_events(tx_rows, local_id)
        phase_counts = collections.Counter(event["phase"] for event in events)
        payload_programs = collections.Counter(program for event in events for program in event["programs"])
        slots_by_phase: dict[str, set[int]] = collections.defaultdict(set)
        for event in events:
            if event["slot"] is not None:
                slots_by_phase[event["phase"]].add(event["slot"])
        operation_slots = set().union(
            slots_by_phase.get("withdraw/inbox", set()),
            slots_by_phase.get("rfq/inbox", set()),
            slots_by_phase.get("swap/inbox", set()),
            slots_by_phase.get("metadata", set()),
        )
        verify_slots = slots_by_phase.get("verify-request", set())
        event_slots = [event["slot"] for event in events if event["slot"] is not None]
        root_deltas = []
        for slot in event_slots:
            for root in roots:
                if root["slot"] is not None:
                    root_deltas.append(abs(root["slot"] - slot))
        verifier_matches = verifier_field_matches_for_rows(tx_rows, local_id) + root_matches(base, local_id)
        output.append(
            {
                **local_id,
                "events": events,
                "phase_counts": phase_counts,
                "payload_programs": payload_programs,
                "same_slot_operation_verify": sorted(operation_slots & verify_slots),
                "root_update_same_slots": sorted(set(slot for slot in event_slots if slot in roots_by_slot)),
                "closest_root_update_slot_delta": min(root_deltas) if root_deltas else None,
                "decoded_request_matches": decoded_field_matches(tx_rows, local_id),
                "verifier_matches": sorted(set(verifier_matches)),
                "known_key_matches": known_key_matches(base, local_id["embedded_pubkey"], local_id["embedded_raw"]),
            }
        )
    return output, tx_rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot_dir")
    parser.add_argument("--input-prefix", default="bank-program-wide-window")
    parser.add_argument("--state-name", default="BankKWideWindowCreatedAccounts")
    args = parser.parse_args()
    base = Path(args.snapshot_dir)
    rows, tx_rows = lifecycle_rows(base, args.input_prefix, args.state_name)
    slots = sorted({row["slot"] for row in tx_rows if row["slot"] is not None})

    ids_with_events = [row for row in rows if row["events"]]
    ids_with_bank_payload = [row for row in rows if row["payload_programs"].get(BANKK)]
    ids_with_inbox_payload = [row for row in rows if row["payload_programs"].get(INBOX)]
    ids_with_outbox_payload = [row for row in rows if row["payload_programs"].get(OUTBOX)]
    ids_with_verify = [row for row in rows if row["phase_counts"].get("verify-request")]
    ids_with_operation_and_verify = [
        row
        for row in rows
        if row["phase_counts"].get("verify-request")
        and any(row["phase_counts"].get(phase) for phase in ("withdraw/inbox", "rfq/inbox", "swap/inbox"))
    ]
    ids_with_same_slot_operation_verify = [row for row in rows if row["same_slot_operation_verify"]]
    decoded_request_hits = [row for row in rows if row["decoded_request_matches"]]
    verifier_hits = [row for row in rows if row["verifier_matches"]]
    security_hits = [row for row in rows if row["known_key_matches"]]
    root_same_slot_hits = [row for row in rows if row["root_update_same_slots"]]

    print("# BankK Wide Window Local ID Lifecycle")
    print()
    print("## Scope")
    print()
    print(f"- Input prefix: `{args.input_prefix}`")
    print(f"- Transactions analyzed: `{len(tx_rows)}`")
    print(f"- Slot range: `{slots[0] if slots else None}` to `{slots[-1] if slots else None}`")
    print(f"- Slot span: `{(slots[-1] - slots[0]) if len(slots) > 1 else 0}`")
    print(f"- Local ids analyzed: `{len(rows)}`")
    print(f"- Payload-derived local ids: `{sum(1 for row in rows if row['source'] == 'wide-window-payload-candidate')}`")
    print(f"- Local ids with sampled lifecycle events: `{len(ids_with_events)}`")
    print(f"- Local ids seen in `BankK...` raw payloads: `{len(ids_with_bank_payload)}`")
    print(f"- Local ids seen in `JNiN...` inbox raw payloads: `{len(ids_with_inbox_payload)}`")
    print(f"- Local ids seen in `jnoUtn...` outbox raw payloads: `{len(ids_with_outbox_payload)}`")
    print(f"- Local ids seen in `VerifyRequest` rows: `{len(ids_with_verify)}`")
    print(f"- Local ids with operation + verify lifecycle evidence: `{len(ids_with_operation_and_verify)}`")
    print(f"- Local ids with same-slot operation + verify evidence: `{len(ids_with_same_slot_operation_verify)}`")
    print(f"- Local ids matching decoded request fields in this window: `{len(decoded_request_hits)}`")
    print(f"- Local ids matching verifier/root fields in this window: `{len(verifier_hits)}`")
    print(f"- Local ids matching canonical JUP / validator / vote / stake keys: `{len(security_hits)}`")
    print(f"- Local ids sharing a slot with root updates: `{len(root_same_slot_hits)}`")
    print()

    print("## Lifecycle Rows")
    print()
    print("| State account/source | Local id | Candidate offsets | Phases | Payload programs | Same-slot operation/verify | Closest root-update slot delta | Decoded request hits | Verifier/root hits | Security hits | Events |")
    print("|---|---|---|---|---|---|---:|---|---|---|---|")
    for row in rows:
        print(
            f"| `{row['account']}` | `{row['embedded_pubkey']}` | {fmt_counter(collections.Counter(row.get('candidate_offsets') or {}))} | "
            f"{fmt_counter(row['phase_counts'])} | "
            f"{fmt_counter(row['payload_programs'])} | {fmt(row['same_slot_operation_verify'])} | "
            f"{row['closest_root_update_slot_delta']} | {fmt(row['decoded_request_matches'], limit=4)} | "
            f"{fmt(row['verifier_matches'], limit=4)} | {fmt(row['known_key_matches'], limit=4)} | "
            f"{fmt(event_summary(row['events']), limit=8)} |"
        )
    print()

    print("## Root Update Context")
    print()
    roots = root_update_rows(base)
    if roots:
        print("| Time | Slot | File | Epoch | Signers |")
        print("|---|---:|---|---:|---|")
        for row in roots:
            print(
                f"| `{block_time(row['block_time'])}` | {row['slot']} | `{row['file']}` | "
                f"{row['epoch']} | {fmt(sorted(row['tx_signers']))} |"
            )
    else:
        print("- No decoded root-update rows in snapshot.")
    print()

    print("## Assessment")
    print()
    if ids_with_operation_and_verify:
        print("- The wider window still shows Bank-local ids bridging operation payloads and `VerifyRequest` payloads.")
    else:
        print("- The wider window did not show operation + `VerifyRequest` lifecycle pairings for recovered local ids.")
    if ids_with_outbox_payload or verifier_hits or root_same_slot_hits:
        print("- At least one local id reached an outbox/root-adjacent surface; inspect rows above.")
    else:
        print("- No local id reached `jnoUtn...` outbox payloads, verifier/root fields or sampled root-update slots.")
    if decoded_request_hits or security_hits:
        print("- At least one local id matched decoded request or JUP/validator/stake material; inspect rows above.")
    else:
        print("- No local id matched decoded request fields, canonical JUP or current validator/vote/stake keys.")


if __name__ == "__main__":
    main()
