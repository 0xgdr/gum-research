#!/usr/bin/env python3
"""Trace BankK 41-byte local ids across sampled transaction lifecycles."""

from __future__ import annotations

import argparse
import collections
from pathlib import Path

from analyze_bank_request_message_correlation import raw_hit_locations
from analyze_bank_request_message_correlation import rows as correlation_rows
from analyze_bankk_41_byte_state import account_values_from_created_state
from analyze_bankk_41_byte_state import account_values_from_recurring_state
from analyze_bankk_41_byte_state import decode_41
from analyze_bankk_41_byte_state import decoded_request_field_matches
from analyze_bankk_41_byte_state import dedupe_rows
from analyze_bankk_41_byte_state import known_key_matches
from analyze_bankk_41_byte_state import verifier_matches
from analyze_root_update_authority_graph import block_time
from analyze_root_update_authority_graph import root_update_rows


BANKK = "BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ"
INBOX = "JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw"
OUTBOX = "jnoUtncGR9ZCCMixtys6Gzy5coTo6mnmUZuEHRQFTFV"


def bankk_local_ids(base: Path) -> list[dict]:
    return [
        decode_41(row)
        for row in dedupe_rows(account_values_from_created_state(base) + account_values_from_recurring_state(base))
    ]


def phase_for(row: dict) -> str:
    instructions = set(row["instructions"])
    if "VerifyRequest" in instructions:
        return "verify-request"
    if instructions & {"Withdraw", "Sweep", "TransferChecked"}:
        return "withdraw/inbox"
    if any(name.startswith("Rfq") for name in instructions):
        return "rfq/inbox"
    if instructions & {"Swap", "RouteV2"}:
        return "swap/inbox"
    if "CacheTokenMetadata" in instructions:
        return "metadata"
    return "other"


def parse_program(location: str) -> str:
    parts = location.split(":")
    return parts[1] if len(parts) > 1 else "unknown"


def hit_events(base: Path, local_id: dict) -> list[dict]:
    events = []
    embedded = local_id["embedded_raw"]
    embedded_pubkey = local_id["embedded_pubkey"]
    for row in correlation_rows(base):
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


def lifecycle_rows(base: Path) -> list[dict]:
    root_rows = root_update_rows(base)
    roots_by_slot = collections.defaultdict(list)
    for row in root_rows:
        roots_by_slot[row["slot"]].append(row)

    rows = []
    for local_id in bankk_local_ids(base):
        events = hit_events(base, local_id)
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
        same_slot_operation_verify = operation_slots & verify_slots
        root_update_same_slots = sorted(set(event["slot"] for event in events if event["slot"] in roots_by_slot))
        all_event_slots = [event["slot"] for event in events if event["slot"] is not None]
        root_slot_deltas = []
        for event_slot in all_event_slots:
            for root_row in root_rows:
                if root_row["slot"] is not None:
                    root_slot_deltas.append(abs(root_row["slot"] - event_slot))
        rows.append(
            {
                **local_id,
                "events": events,
                "phase_counts": phase_counts,
                "payload_programs": payload_programs,
                "same_slot_operation_verify": sorted(same_slot_operation_verify),
                "root_update_same_slots": root_update_same_slots,
                "closest_root_update_slot_delta": min(root_slot_deltas) if root_slot_deltas else None,
                "decoded_request_matches": decoded_request_field_matches(base, local_id),
                "verifier_matches": verifier_matches(base, local_id),
                "known_key_matches": known_key_matches(base, local_id["embedded_pubkey"], local_id["embedded_raw"]),
            }
        )
    return rows


def fmt(values, empty: str = "`None`", limit: int | None = None) -> str:
    items = [str(value) for value in values if value is not None and value != ""]
    if limit is not None:
        items = items[:limit]
    if not items:
        return empty
    return "<br>".join(f"`{item}`" for item in items)


def fmt_counter(counter: collections.Counter) -> str:
    return fmt([f"{key}: {value}" for key, value in counter.most_common()])


def event_summary(events: list[dict], limit: int = 8) -> list[str]:
    rows = []
    for event in events[:limit]:
        instructions = ",".join(event["instructions"]) or "unknown"
        programs = ",".join(event["programs"]) or "none"
        rows.append(
            f"{event['slot']} {event['phase']} {instructions} {programs} "
            f"{event['signature'][:8]} locations={len(event['locations'])}"
        )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot_dir")
    args = parser.parse_args()
    base = Path(args.snapshot_dir)
    rows = lifecycle_rows(base)

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

    print("# BankK Local ID Lifecycle")
    print()
    print("## Scope")
    print()
    print(f"- 41-byte local ids analyzed: `{len(rows)}`")
    print(f"- Local ids with sampled lifecycle events: `{len(ids_with_events)}`")
    print(f"- Local ids seen in `BankK...` raw payloads: `{len(ids_with_bank_payload)}`")
    print(f"- Local ids seen in `JNiN...` inbox raw payloads: `{len(ids_with_inbox_payload)}`")
    print(f"- Local ids seen in `jnoUtn...` outbox raw payloads: `{len(ids_with_outbox_payload)}`")
    print(f"- Local ids seen in `VerifyRequest` rows: `{len(ids_with_verify)}`")
    print(f"- Local ids with operation + verify lifecycle evidence: `{len(ids_with_operation_and_verify)}`")
    print(f"- Local ids with same-slot operation + verify evidence: `{len(ids_with_same_slot_operation_verify)}`")
    print(f"- Local ids matching decoded `bk1PDA...` request fields: `{len(decoded_request_hits)}`")
    print(f"- Local ids matching verifier/root fields: `{len(verifier_hits)}`")
    print(f"- Local ids matching canonical JUP / validator / vote / stake keys: `{len(security_hits)}`")
    print(f"- Local ids sharing a slot with root updates: `{len(root_same_slot_hits)}`")
    print()

    print("## Lifecycle Rows")
    print()
    print("| State account | Local id | Phases | Payload programs | Same-slot operation/verify | Closest root-update slot delta | Decoded request hits | Verifier/root hits | Security hits | Events |")
    print("|---|---|---|---|---|---:|---|---|---|---|")
    for row in rows:
        print(
            f"| `{row['account']}` | `{row['embedded_pubkey']}` | {fmt_counter(row['phase_counts'])} | "
            f"{fmt_counter(row['payload_programs'])} | {fmt(row['same_slot_operation_verify'])} | "
            f"{row['closest_root_update_slot_delta']} | {fmt(row['decoded_request_matches'], limit=4)} | "
            f"{fmt(row['verifier_matches'], limit=4)} | {fmt(row['known_key_matches'], limit=4)} | "
            f"{fmt(event_summary(row['events']), limit=8)} |"
        )
    print()

    print("## Same-Slot Operation And Verify")
    print()
    if ids_with_same_slot_operation_verify:
        print("| Local id | Slots |")
        print("|---|---|")
        for row in ids_with_same_slot_operation_verify:
            print(f"| `{row['embedded_pubkey']}` | {fmt(row['same_slot_operation_verify'])} |")
    else:
        print("- None")
    print()

    print("## Root Update Context")
    print()
    root_rows = root_update_rows(base)
    if root_rows:
        print("| Time | Slot | File | Epoch | Signers |")
        print("|---|---:|---|---:|---|")
        for row in root_rows:
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
        print("- Most sampled local ids bridge Bank operation payloads and `VerifyRequest` payloads, so the 32-byte value is a useful Bank-local lifecycle handle.")
    else:
        print("- No local id bridged operation and `VerifyRequest` payloads in this sample.")
    if ids_with_same_slot_operation_verify:
        print("- Some local ids have same-slot operation and verification evidence, which is the strongest public timing link in this pass.")
    else:
        print("- No local id had same-slot operation and verification evidence in the saved sample.")
    if verifier_hits or decoded_request_hits or security_hits:
        print("- At least one local id crossed into decoded request, verifier/root, JUP or validator/stake material; inspect the rows above.")
    else:
        print("- No local id crossed into decoded `bk1PDA...` request fields, verifier/root fields, canonical JUP or current validator/vote/stake keys.")
    print("- The public lifecycle currently stops at a Bank-local operation/verify handle; it does not expose the Dove/JUP/stake producer side.")


if __name__ == "__main__":
    main()
