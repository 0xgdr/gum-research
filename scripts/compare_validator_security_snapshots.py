#!/usr/bin/env python3
"""Compare two JupNet validator-security snapshots and emit alert-oriented Markdown."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import re
import struct
from pathlib import Path

from analyze_jupnet_executable_census import program_label as census_program_label
from analyze_jupnet_executable_census import program_rows as census_program_rows
from analyze_outbox_root_history import history_rows as outbox_history_rows
from analyze_outbox_root_history import transaction_files as outbox_history_transaction_files
from analyze_root_update_authority_graph import parse_programdata as root_update_programdata
from analyze_root_update_authority_graph import root_update_rows as root_update_authority_rows
from map_outbox_verifier_payloads import collect_rows as verifier_payload_rows
from map_outbox_verifier_payloads import outbox_roots as verifier_stored_roots


ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
JUP_MINT = "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN"
GUM_PROGRAM = "brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1"
GUM_BANK = "bk1PDAkbHEBGtVRiM94Lzets8gVFP7FgySyfkAc8MPN"
GUM_BANK_PROGRAM = "BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ"


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


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def result(base: Path, filename: str):
    return load_json(base / filename).get("result")


def raw_account_data(account: dict) -> bytes:
    data = account.get("data")
    if isinstance(data, list):
        return base64.b64decode(data[0])
    if isinstance(data, dict) and isinstance(data.get("parsed"), dict):
        return json.dumps(data["parsed"], sort_keys=True).encode()
    return b""


def account_records(base: Path, filename: str) -> list[tuple[str, bytes]]:
    records = []
    for item in result(base, filename) or []:
        records.append((item["pubkey"], raw_account_data(item["account"])))
    return records


def count_hits(records: list[tuple[str, bytes]], target: bytes) -> int:
    return sum(1 for _pubkey, raw in records if target in raw)


def parse_programdata(base: Path, program_filename: str, programdata_filename: str) -> tuple[str | None, int | None, str | None]:
    program = result(base, program_filename)
    programdata = None
    if program and program.get("value"):
        raw = raw_account_data(program["value"])
        if len(raw) >= 36 and struct.unpack("<I", raw[:4])[0] == 2:
            programdata = b58encode(raw[4:36])

    deployment_slot = None
    authority = None
    data = result(base, programdata_filename)
    if data and data.get("value"):
        raw = raw_account_data(data["value"])
        if len(raw) >= 45 and struct.unpack("<I", raw[:4])[0] == 3:
            deployment_slot = struct.unpack("<Q", raw[4:12])[0]
            authority = b58encode(raw[13:45]) if raw[12] == 1 else None
    return programdata, deployment_slot, authority


def account_value(base: Path, filename: str) -> dict | None:
    data = result(base, filename)
    if not data:
        return None
    return data.get("value")


def account_hash(value: dict | None) -> str | None:
    if not value:
        return None
    return hashlib.sha256(raw_account_data(value)).hexdigest()


def signature_set(base: Path, filename: str) -> set[str]:
    return {item["signature"] for item in result(base, filename) or []}


def validator_sets(base: Path) -> tuple[set[str], set[str], dict[str, int]]:
    votes = result(base, "getVoteAccounts.json") or {}
    nodes = set()
    vote_accounts = set()
    stakes = {}
    for vote in (votes.get("current") or []) + (votes.get("delinquent") or []):
        nodes.add(vote["nodePubkey"])
        vote_accounts.add(vote["votePubkey"])
        stakes[vote["votePubkey"]] = int(vote.get("activatedStake") or 0)
    return nodes, vote_accounts, stakes


def stake_accounts(base: Path) -> set[str]:
    return {item["pubkey"] for item in result(base, "getProgramAccounts-Stake.json") or []}


def validator_related_keys(base: Path) -> set[str]:
    nodes, votes, _stakes = validator_sets(base)
    return nodes | votes | stake_accounts(base)


def tx_rows(base: Path, authority: str | None, validator_related: set[str]) -> tuple[set[str], int, int]:
    signatures = set()
    authority_signed = 0
    validator_hits = 0
    for path in sorted(base.glob("tx-*.json")):
        if path.name.endswith("-raw.json"):
            continue
        data = load_json(path)
        tx = data.get("result")
        if not tx:
            continue
        for sig in tx.get("transaction", {}).get("signatures", []):
            signatures.add(sig)
        signers = set()
        account_keys = set()
        for key in tx["transaction"]["message"].get("accountKeys", []):
            if isinstance(key, dict):
                account_keys.add(key["pubkey"])
                if key.get("signer"):
                    signers.add(key["pubkey"])
            elif isinstance(key, str):
                account_keys.add(key)
        if authority and authority in signers:
            authority_signed += 1
        validator_hits += len(account_keys & validator_related)
    return signatures, authority_signed, validator_hits


def bank_tx_metrics(base: Path, validator_related: set[str]) -> dict:
    tx_signatures = set()
    validator_hits = 0
    jup_account_hits = 0
    watched_hits = 0
    watched = {GUM_PROGRAM, GUM_BANK, GUM_BANK_PROGRAM, JUP_MINT}
    for path in sorted(base.glob("bank-tx-*.json")):
        tx = load_json(path).get("result")
        if not tx:
            continue
        for sig in tx.get("transaction", {}).get("signatures", []):
            tx_signatures.add(sig)
        keys = set()
        for key in tx["transaction"]["message"].get("accountKeys", []):
            if isinstance(key, dict):
                keys.add(key["pubkey"])
            elif isinstance(key, str):
                keys.add(key)
        validator_hits += len(keys & validator_related)
        if JUP_MINT in keys:
            jup_account_hits += 1
        watched_hits += len(keys & watched)
    return {
        "bank_sample_tx_signatures": tx_signatures,
        "bank_sample_tx_validator_hits": validator_hits,
        "bank_sample_tx_jup_account_hits": jup_account_hits,
        "bank_sample_tx_watched_hits": watched_hits,
    }


def solana_bank_tx_metrics(base: Path) -> dict:
    tx_signatures = set()
    jup_account_hits = 0
    inbox_outbox_log_hits = 0
    watched_hits = 0
    watched = {GUM_PROGRAM, GUM_BANK, GUM_BANK_PROGRAM, JUP_MINT}
    for path in sorted(base.glob("solana-mainnet-bank-tx-*.json")):
        tx = load_json(path).get("result")
        if not tx:
            continue
        for sig in tx.get("transaction", {}).get("signatures", []):
            tx_signatures.add(sig)
        keys = set()
        for key in tx["transaction"]["message"].get("accountKeys", []):
            if isinstance(key, dict):
                keys.add(key["pubkey"])
            elif isinstance(key, str):
                keys.add(key)
        if JUP_MINT in keys:
            jup_account_hits += 1
        watched_hits += len(keys & watched)
        logs = tx.get("meta", {}).get("logMessages") or []
        inbox_outbox_log_hits += sum(1 for line in logs if "inbox" in line.lower() or "outbox" in line.lower())
    return {
        "solana_bank_sample_tx_signatures": tx_signatures,
        "solana_bank_sample_tx_jup_account_hits": jup_account_hits,
        "solana_bank_sample_tx_watched_hits": watched_hits,
        "solana_bank_inbox_outbox_log_hits": inbox_outbox_log_hits,
    }


def bank_account_graph_metrics(base: Path) -> dict:
    path = base / "bank-account-graph.md"
    if not path.exists():
        return {
            "bank_graph_present": False,
            "bank_graph_jup_account_hits": None,
            "bank_graph_pda_matches": set(),
        }
    text = path.read_text()
    jup_hits = None
    match = re.search(r"Bank instructions with canonical Solana JUP mint account: `(\d+)`", text)
    if match:
        jup_hits = int(match.group(1))
    pda_matches = set()
    for program, seeds, account in re.findall(r"\| `([^`]+)` \| `([^`]+)` \| `([^`]+)` \|", text):
        if program == "Program" or account == "Derived observed account":
            continue
        pda_matches.add(f"{program} | {seeds} | {account}")
    return {
        "bank_graph_present": True,
        "bank_graph_jup_account_hits": jup_hits,
        "bank_graph_pda_matches": pda_matches,
    }


def bank_recurring_account_metrics(base: Path) -> dict:
    path = base / "bank-recurring-account-state.md"
    if not path.exists():
        return {
            "bank_recurring_present": False,
            "bank_recurring_jup_raw_hits": None,
            "bank_recurring_jup_text_hits": None,
            "bank_recurring_validator_hits": None,
            "bank_recurring_bank_owned_state": None,
        }
    text = path.read_text()

    def number(pattern: str) -> int | None:
        match = re.search(pattern, text)
        return int(match.group(1)) if match else None

    return {
        "bank_recurring_present": True,
        "bank_recurring_jup_raw_hits": number(r"Accounts with canonical JUP raw pubkey bytes: `(\d+)`"),
        "bank_recurring_jup_text_hits": number(r"Accounts with canonical JUP base58 text: `(\d+)`"),
        "bank_recurring_validator_hits": number(r"Accounts with JupNet validator/vote/stake key hits: `(\d+)`"),
        "bank_recurring_bank_owned_state": number(r"Bank Program-owned state: `(\d+)`"),
    }


def bank_owner_context_metrics(base: Path) -> dict:
    path = base / "bank-owner-program-context.md"
    if not path.exists():
        return {
            "bank_owner_context_present": False,
            "bank_owner_context_jup_hits": None,
            "bank_owner_context_validator_hits": None,
            "bank_owner_context_programdata_count": None,
            "bank_owner_context_programdata_set": set(),
        }
    text = path.read_text()

    def number(pattern: str) -> int | None:
        match = re.search(pattern, text)
        return int(match.group(1)) if match else None

    programdata_set = set()
    for program, programdata, _slot, authority, _bytes, sha256 in re.findall(
        r"\| `([^`]+)` \| `([^`]+)` \| ([0-9A-Za-z]+) \| `([^`]+)` \| ([0-9]+) \| `([^`]+)` \|",
        text,
    ):
        if program == "Program":
            continue
        programdata_set.add(f"{program} | {programdata} | {authority} | {sha256}")

    return {
        "bank_owner_context_present": True,
        "bank_owner_context_jup_hits": number(r"Accounts with canonical JUP key hits: `(\d+)`"),
        "bank_owner_context_validator_hits": number(r"Accounts with current JupNet validator/vote/stake key hits: `(\d+)`"),
        "bank_owner_context_programdata_count": number(r"Upgradeable owner programs with ProgramData: `(\d+)`"),
        "bank_owner_context_programdata_set": programdata_set,
    }


def helper_program_account_metrics(base: Path) -> dict:
    path = base / "jupnet-helper-program-accounts.md"
    if not path.exists():
        return {
            "helper_program_accounts_present": False,
            "helper_inbox_accounts": None,
            "helper_outbox_accounts": None,
            "helper_jup_hits": None,
            "helper_validator_hits": None,
        }
    text = path.read_text()

    def number(pattern: str) -> int | None:
        match = re.search(pattern, text)
        return int(match.group(1)) if match else None

    return {
        "helper_program_accounts_present": True,
        "helper_inbox_accounts": number(r"Inbox-owned accounts fetched: `(\d+)`"),
        "helper_outbox_accounts": number(r"Outbox-owned accounts fetched: `(\d+)`"),
        "helper_jup_hits": number(r"Accounts with canonical JUP hits: `(\d+)`"),
        "helper_validator_hits": number(r"Accounts with current JupNet validator/vote/stake key hits: `(\d+)`"),
    }


def verify_request_payload_metrics(base: Path) -> dict:
    path = base / "verify-request-payload-reconstruction.md"
    if not path.exists():
        return {
            "verify_request_report_present": False,
            "verify_request_samples": None,
            "verify_request_jup_hits": None,
            "verify_request_validator_hits": None,
            "verify_request_proof_nodes": None,
        }
    text = path.read_text()

    def number(pattern: str) -> int | None:
        match = re.search(pattern, text)
        return int(match.group(1)) if match else None

    proof_nodes = len(re.findall(r"^\| [0-9]+ \| `[0-9a-f]{64}` \|$", text, flags=re.MULTILINE))
    return {
        "verify_request_report_present": True,
        "verify_request_samples": number(r"`verify_request` samples: `(\d+)`"),
        "verify_request_jup_hits": number(r"Canonical JUP key hits: `(\d+)`"),
        "verify_request_validator_hits": number(r"Current JupNet validator/vote/stake key hits: `(\d+)`"),
        "verify_request_proof_nodes": proof_nodes,
    }


def outbox_root_update_metrics(base: Path) -> dict:
    path = base / "outbox-root-update-transactions.md"
    if not path.exists():
        return {
            "outbox_root_update_report_present": False,
            "outbox_root_update_candidates": None,
            "outbox_root_update_jup_hits": None,
            "outbox_root_update_validator_hits": None,
        }
    text = path.read_text()

    def number(pattern: str) -> int | None:
        match = re.search(pattern, text)
        return int(match.group(1)) if match else None

    return {
        "outbox_root_update_report_present": True,
        "outbox_root_update_candidates": number(r"Update/BLS candidate instructions: `(\d+)`"),
        "outbox_root_update_jup_hits": number(r"Canonical JUP key hits: `(\d+)`"),
        "outbox_root_update_validator_hits": number(r"Current JupNet validator/vote/stake key hits: `(\d+)`"),
    }


def private_runtime_fingerprint_metrics(base: Path) -> dict:
    path = base / "private-runtime-fingerprints.md"
    if not path.exists():
        return {
            "private_runtime_fingerprints_present": False,
            "private_runtime_dependency_terms_with_hits": None,
            "private_runtime_security_producer_terms_with_hits": None,
            "private_runtime_public_verifier_terms_with_hits": None,
            "private_runtime_source_paths_recovered": None,
            "private_runtime_dependency_hit_terms": set(),
            "private_runtime_security_producer_hit_terms": set(),
            "private_runtime_public_verifier_hit_terms": set(),
        }
    text = path.read_text()

    def number(pattern: str) -> int | None:
        match = re.search(pattern, text)
        return int(match.group(1)) if match else None

    def section(title: str) -> str:
        match = re.search(rf"## {re.escape(title)}\n\n(.*?)(?=\n## |\Z)", text, flags=re.S)
        return match.group(1) if match else ""

    def hit_terms(title: str) -> set[str]:
        terms = set()
        for term, count in re.findall(r"\| `([^`]+)` \| ([0-9]+) \|", section(title)):
            if int(count) > 0:
                terms.add(term)
        return terms

    return {
        "private_runtime_fingerprints_present": True,
        "private_runtime_dependency_terms_with_hits": number(r"Private runtime dependency terms with hits: `(\d+)`"),
        "private_runtime_security_producer_terms_with_hits": number(r"Security producer terms with hits: `(\d+)`"),
        "private_runtime_public_verifier_terms_with_hits": number(r"Public verifier terms with hits: `(\d+)`"),
        "private_runtime_source_paths_recovered": number(r"JupNet/Gum source paths recovered: `(\d+)`"),
        "private_runtime_dependency_hit_terms": hit_terms("Private Runtime Dependency Terms"),
        "private_runtime_security_producer_hit_terms": hit_terms("Security Producer Terms"),
        "private_runtime_public_verifier_hit_terms": hit_terms("Public Verifier Terms"),
    }


def outbox_root_history_metrics(base: Path) -> dict:
    files = outbox_history_transaction_files(base)
    update_rows, verifier_rows = outbox_history_rows(base)
    rows = update_rows + verifier_rows
    security_hit_rows = sum(1 for row in rows if row.get("key_hits") or row.get("payload_hits"))
    latest = max(
        update_rows,
        key=lambda row: ((row.get("block_time") or 0), (row.get("slot") or 0), str(row.get("signature") or "")),
        default=None,
    )
    return {
        "outbox_root_history_present": bool(files or (base / "outbox-root-history.md").exists()),
        "outbox_root_history_tx_files": len(files),
        "outbox_root_history_updates": len(update_rows),
        "outbox_root_history_verifiers": len(verifier_rows),
        "outbox_root_history_security_hit_rows": security_hit_rows,
        "outbox_root_history_latest_update": (
            f"epoch {latest['epoch']} root {latest['root'].hex()} "
            f"aggregate {latest['aggregate_key'].hex()} compact {latest['compact_verifier_field'].hex()}"
            if latest
            else None
        ),
        "outbox_root_history_epochs": {str(row["epoch"]) for row in update_rows},
        "outbox_root_history_roots": {row["root"].hex() for row in update_rows},
        "outbox_root_history_aggregate_keys": {row["aggregate_key"].hex() for row in update_rows},
        "outbox_root_history_compact_fields": {row["compact_verifier_field"].hex() for row in update_rows},
        "outbox_root_history_verifier_roots": {row["root"].hex() for row in verifier_rows},
        "outbox_root_history_verifier_aggregate_keys": {row["aggregate_key"].hex() for row in verifier_rows},
    }


def root_update_authority_graph_metrics(base: Path, validator_related: set[str]) -> dict:
    rows = root_update_authority_rows(base)
    tx_signers = {signer for row in rows for signer in row["tx_signers"]}
    instruction_signers = {signer for row in rows for signer in row["instruction_signers"]}
    writable_accounts = {account for row in rows for account in row["instruction_writables"]}
    participants = set()
    for row in rows:
        participants.update(row["accounts"])
        participants.update(row["tx_signers"])
        participants.update(row["tx_writables"])
    upgrade_authorities = {row["authority"] for row in root_update_programdata(base) if row.get("authority")}
    security_intersections = (participants & validator_related) | ({JUP_MINT} if JUP_MINT in participants else set())
    upgrade_intersections = participants & upgrade_authorities
    return {
        "root_update_authority_present": bool(rows or (base / "root-update-authority-graph.md").exists()),
        "root_update_authority_updates": len(rows),
        "root_update_authority_tx_signers": tx_signers,
        "root_update_authority_instruction_signers": instruction_signers,
        "root_update_authority_writable_accounts": writable_accounts,
        "root_update_authority_security_intersections": security_intersections,
        "root_update_authority_upgrade_intersections": upgrade_intersections,
        "root_update_authority_tx_signer_count": len(tx_signers),
        "root_update_authority_instruction_signer_count": len(instruction_signers),
        "root_update_authority_writable_account_count": len(writable_accounts),
        "root_update_authority_security_intersection_count": len(security_intersections),
        "root_update_authority_upgrade_intersection_count": len(upgrade_intersections),
    }


def all_saved_transaction_files(base: Path) -> list[Path]:
    paths = []
    for path in sorted(base.glob("*.json")):
        tx = load_json(path).get("result")
        if isinstance(tx, dict) and isinstance(tx.get("transaction"), dict):
            paths.append(path)
    return paths


def transaction_account_keys(tx: dict) -> set[str]:
    keys = set()
    for key in tx.get("transaction", {}).get("message", {}).get("accountKeys") or []:
        keys.add(key["pubkey"] if isinstance(key, dict) else key)
    return keys


def transaction_signers(tx: dict) -> set[str]:
    signers = set()
    for key in tx.get("transaction", {}).get("message", {}).get("accountKeys") or []:
        if isinstance(key, dict) and key.get("signer"):
            signers.add(key["pubkey"])
    return signers


def root_submitter_provenance_metrics(base: Path, validator_related: set[str]) -> dict:
    root_rows = root_update_authority_rows(base)
    submitters = {signer for row in root_rows for signer in row["tx_signers"]}
    upgrade_authorities = {row["authority"] for row in root_update_programdata(base) if row.get("authority")}
    occurrence_files = set()
    signer_files = set()
    programs = set()
    security_intersections = set()
    upgrade_intersections = set()
    for path in all_saved_transaction_files(base):
        tx = load_json(path).get("result")
        keys = transaction_account_keys(tx)
        matched = keys & submitters
        if not matched:
            continue
        occurrence_files.add(path.name)
        signers = transaction_signers(tx)
        if signers & submitters:
            signer_files.add(path.name)
        security_intersections.update((keys & validator_related) | ({JUP_MINT} if JUP_MINT in keys else set()))
        upgrade_intersections.update(keys & upgrade_authorities)
        for ix in tx.get("transaction", {}).get("message", {}).get("instructions") or []:
            if ix.get("programId"):
                programs.add(ix["programId"])
        for group in tx.get("meta", {}).get("innerInstructions") or []:
            for ix in group.get("instructions") or []:
                if ix.get("programId"):
                    programs.add(ix["programId"])
    return {
        "root_submitter_provenance_present": bool(submitters or (base / "root-submitter-provenance.md").exists()),
        "root_submitter_count": len(submitters),
        "root_submitter_occurrence_tx_count": len(occurrence_files),
        "root_submitter_signer_tx_count": len(signer_files),
        "root_submitter_security_intersection_count": len(security_intersections),
        "root_submitter_upgrade_intersection_count": len(upgrade_intersections),
        "root_submitters": submitters,
        "root_submitter_occurrence_files": occurrence_files,
        "root_submitter_signer_files": signer_files,
        "root_submitter_programs": programs,
        "root_submitter_security_intersections": security_intersections,
        "root_submitter_upgrade_intersections": upgrade_intersections,
    }


def outbox_verifier_payload_map_metrics(base: Path) -> dict:
    rows = verifier_payload_rows(base)
    roots = verifier_stored_roots(base)
    related = validator_related_keys(base)
    validator_keys = set(related)
    jup_raw = b58decode(JUP_MINT)

    jup_hits = 0
    validator_hits = 0
    root_mismatches = 0
    senders = set()
    for row in rows:
        raw_blob = b"".join([row["message_hash"], row["aggregate_key"], row["signature"], *row["proof_nodes"]])
        if jup_raw in raw_blob or JUP_MINT in row["account_keys"]:
            jup_hits += 1
        if row["account_keys"] & validator_keys:
            validator_hits += 1
        expected = roots.get(row["epoch"])
        if expected and row["recomputed_root"] != expected:
            root_mismatches += 1
        if row.get("sender"):
            senders.add(b58encode(row["sender"]))

    return {
        "outbox_verifier_map_present": bool(rows or (base / "outbox-verifier-payload-field-map.md").exists()),
        "outbox_verifier_map_payloads": len(rows),
        "outbox_verifier_map_bank_wrappers": sum(1 for row in rows if row["kind"] == "bank-verify-wrapper"),
        "outbox_verifier_map_inner_payloads": sum(1 for row in rows if row["kind"] == "inner-outbox"),
        "outbox_verifier_map_jup_hits": jup_hits,
        "outbox_verifier_map_validator_hits": validator_hits,
        "outbox_verifier_map_root_mismatches": root_mismatches,
        "outbox_verifier_map_senders": senders,
        "outbox_verifier_map_aggregate_keys": {row["aggregate_key"].hex() for row in rows},
        "outbox_verifier_map_roots": {row["recomputed_root"].hex() for row in rows},
        "outbox_verifier_map_layouts": {
            f"{row['kind']} | len {row['raw_len']} | aggregate {row['aggregate_offset']} | "
            f"bitmap {row['path_bitmap']} | proof {row['proof_count']}"
            for row in rows
        },
    }


def jupnet_executable_census_metrics(base: Path) -> dict:
    rows = census_program_rows(base)
    verifier_rows = [
        row
        for row in rows
        if any("sol_verify_bls_merkle_key" in text for values in row["term_hits"].values() for text in values)
    ]
    key_hit_rows = [row for row in rows if row["key_hits"]]
    high_rows = [row for row in rows if row["high_value_hits"]]

    def record(row: dict) -> str:
        return (
            f"{row['program']} | {census_program_label(row) or 'unlabeled'} | "
            f"{row['programdata']} | slot {row['slot']} | authority {row['upgrade_authority']} | "
            f"exe {row['executable_sha256']} | programdata {row['programdata_sha256']}"
        )

    def high_value_record(row: dict) -> str:
        terms = ",".join(sorted(row["high_value_hits"]))
        return f"{row['program']} | {census_program_label(row) or 'unlabeled'} | {terms}"

    return {
        "jupnet_executable_census_present": bool(rows or (base / "jupnet-executable-census.md").exists()),
        "jupnet_executable_count": len(rows),
        "jupnet_executable_source_path_count": sum(1 for row in rows if row["source_paths"]),
        "jupnet_executable_high_value_count": len(high_rows),
        "jupnet_executable_key_hit_count": len(key_hit_rows),
        "jupnet_executable_verifier_count": len(verifier_rows),
        "jupnet_executable_records": {record(row) for row in rows},
        "jupnet_executable_verifier_records": {record(row) for row in verifier_rows},
        "jupnet_executable_key_hit_records": {record(row) for row in key_hit_rows},
        "jupnet_executable_high_value_records": {high_value_record(row) for row in high_rows},
        "jupnet_executable_authority_records": {
            f"{row['program']} | {row['upgrade_authority']}" for row in rows
        },
    }


def snapshot_metrics(base: Path) -> dict:
    jup_raw = b58decode(JUP_MINT)
    gum_records = account_records(base, "getProgramAccounts-Gum.json")
    openid_records = account_records(base, "getProgramAccounts-OpenIDRegistry.json")
    programdata, deployment_slot, authority = parse_programdata(
        base,
        "getAccountInfo-GumProgram.json",
        "getAccountInfo-GumProgramData-slice48.json",
    )
    bank_programdata, bank_deployment_slot, bank_authority = parse_programdata(
        base,
        "getAccountInfo-GumBankProgram.json",
        "getAccountInfo-GumBankProgramData-slice48.json",
    )
    solana_bank_programdata, solana_bank_deployment_slot, solana_bank_authority = parse_programdata(
        base,
        "solana-mainnet-getAccountInfo-GumBank.json",
        "solana-mainnet-getAccountInfo-GumBankProgramData-slice48.json",
    )
    solana_bank_program_programdata, solana_bank_program_deployment_slot, solana_bank_program_authority = parse_programdata(
        base,
        "solana-mainnet-getAccountInfo-GumBankProgram.json",
        "solana-mainnet-getAccountInfo-GumBankProgramProgramData-slice48.json",
    )
    related = validator_related_keys(base)
    tx_sigs, authority_signed, tx_validator_hits = tx_rows(base, authority, related)
    bank_tx = bank_tx_metrics(base, related)
    solana_bank_tx = solana_bank_tx_metrics(base)
    bank_graph = bank_account_graph_metrics(base)
    bank_recurring = bank_recurring_account_metrics(base)
    bank_owner_context = bank_owner_context_metrics(base)
    helper_program_accounts = helper_program_account_metrics(base)
    verify_request_payload = verify_request_payload_metrics(base)
    outbox_root_update = outbox_root_update_metrics(base)
    private_runtime_fingerprints = private_runtime_fingerprint_metrics(base)
    outbox_root_history = outbox_root_history_metrics(base)
    root_update_authority_graph = root_update_authority_graph_metrics(base, related)
    root_submitter_provenance = root_submitter_provenance_metrics(base, related)
    outbox_verifier_payload_map = outbox_verifier_payload_map_metrics(base)
    jupnet_executable_census = jupnet_executable_census_metrics(base)
    gum_validator_hits = 0
    openid_validator_hits = 0
    for _name, raw in gum_records:
        gum_validator_hits += sum(1 for key in related if b58decode(key) in raw or key.encode() in raw)
    for _name, raw in openid_records:
        openid_validator_hits += sum(1 for key in related if b58decode(key) in raw or key.encode() in raw)

    nodes, votes, stakes = validator_sets(base)
    jup_info = result(base, "getAccountInfo-JUPMint.json") or {}
    token_accounts = result(base, "getProgramAccounts-Token-JUPMint.json") or []
    signatures = result(base, "getSignaturesForAddress-Gum.json") or []
    gum_signature_set = {item["signature"] for item in signatures}
    bank_signature_set = signature_set(base, "getSignaturesForAddress-GumBank.json")
    bank_program_signature_set = signature_set(base, "getSignaturesForAddress-GumBankProgram.json")
    bank_info = account_value(base, "getAccountInfo-GumBank.json")
    bank_program_info = account_value(base, "getAccountInfo-GumBankProgram.json")
    solana_bank_info = account_value(base, "solana-mainnet-getAccountInfo-GumBank.json")
    solana_bank_program_info = account_value(base, "solana-mainnet-getAccountInfo-GumBankProgram.json")
    bank_program_accounts = result(base, "getProgramAccounts-GumBankProgram.json") or []
    if not isinstance(bank_program_accounts, list):
        bank_program_accounts = []

    return {
        "slot": result(base, "getSlot.json"),
        "epoch": (result(base, "getEpochInfo.json") or {}).get("epoch"),
        "rpc_identity": (result(base, "getIdentity.json") or {}).get("identity"),
        "node_keys": nodes,
        "vote_keys": votes,
        "vote_stakes": stakes,
        "stake_accounts": stake_accounts(base),
        "gum_accounts": len(gum_records),
        "gum_jup_raw_hits": count_hits(gum_records, jup_raw),
        "gum_jup_text_hits": count_hits(gum_records, JUP_MINT.encode()),
        "openid_jup_raw_hits": count_hits(openid_records, jup_raw),
        "openid_jup_text_hits": count_hits(openid_records, JUP_MINT.encode()),
        "gum_validator_hits": gum_validator_hits,
        "openid_validator_hits": openid_validator_hits,
        "jup_mint_present": bool(jup_info.get("value")),
        "jup_token_accounts": len(token_accounts),
        "gum_programdata": programdata,
        "gum_deployment_slot": deployment_slot,
        "gum_upgrade_authority": authority,
        "gum_signature_count": len(signatures),
        "gum_signature_set": gum_signature_set,
        "sample_tx_signatures": tx_sigs,
        "sample_tx_authority_signed": authority_signed,
        "sample_tx_validator_hits": tx_validator_hits,
        "bank_present": bool(bank_info),
        "bank_owner": bank_info.get("owner") if bank_info else None,
        "bank_executable": bank_info.get("executable") if bank_info else None,
        "bank_data_hash": account_hash(bank_info),
        "bank_program_present": bool(bank_program_info),
        "bank_program_owner": bank_program_info.get("owner") if bank_program_info else None,
        "bank_program_executable": bank_program_info.get("executable") if bank_program_info else None,
        "bank_program_data_hash": account_hash(bank_program_info),
        "bank_programdata": bank_programdata,
        "bank_deployment_slot": bank_deployment_slot,
        "bank_upgrade_authority": bank_authority,
        "bank_program_owned_accounts": len(bank_program_accounts),
        "bank_signature_count": len(bank_signature_set),
        "bank_program_signature_count": len(bank_program_signature_set),
        "gum_bank_signature_overlap": len(gum_signature_set & bank_signature_set),
        "gum_bank_program_signature_overlap": len(gum_signature_set & bank_program_signature_set),
        "bank_signature_set": bank_signature_set,
        "bank_program_signature_set": bank_program_signature_set,
        **bank_tx,
        "solana_bank_present": bool(solana_bank_info),
        "solana_bank_owner": solana_bank_info.get("owner") if solana_bank_info else None,
        "solana_bank_executable": solana_bank_info.get("executable") if solana_bank_info else None,
        "solana_bank_data_hash": account_hash(solana_bank_info),
        "solana_bank_program_present": bool(solana_bank_program_info),
        "solana_bank_program_owner": solana_bank_program_info.get("owner") if solana_bank_program_info else None,
        "solana_bank_program_executable": solana_bank_program_info.get("executable") if solana_bank_program_info else None,
        "solana_bank_program_data_hash": account_hash(solana_bank_program_info),
        "solana_bank_programdata": solana_bank_programdata,
        "solana_bank_deployment_slot": solana_bank_deployment_slot,
        "solana_bank_upgrade_authority": solana_bank_authority,
        "solana_bank_program_programdata": solana_bank_program_programdata,
        "solana_bank_program_deployment_slot": solana_bank_program_deployment_slot,
        "solana_bank_program_upgrade_authority": solana_bank_program_authority,
        **solana_bank_tx,
        **bank_graph,
        **bank_recurring,
        **bank_owner_context,
        **helper_program_accounts,
        **verify_request_payload,
        **outbox_root_update,
        **private_runtime_fingerprints,
        **outbox_root_history,
        **root_update_authority_graph,
        **root_submitter_provenance,
        **outbox_verifier_payload_map,
        **jupnet_executable_census,
    }


def delta_line(label: str, old, new) -> str | None:
    if old == new:
        return None
    return f"- {label}: `{old}` -> `{new}`"


def set_delta(label: str, old: set[str], new: set[str]) -> list[str]:
    lines = []
    added = sorted(new - old)
    removed = sorted(old - new)
    if added:
        lines.append(f"- {label} added: `{', '.join(added)}`")
    if removed:
        lines.append(f"- {label} removed: `{', '.join(removed)}`")
    return lines


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("old_snapshot")
    parser.add_argument("new_snapshot")
    args = parser.parse_args()

    old_base = Path(args.old_snapshot)
    new_base = Path(args.new_snapshot)
    old = snapshot_metrics(old_base)
    new = snapshot_metrics(new_base)

    alerts = []
    info = []

    watched_scalars = [
        ("RPC identity", "rpc_identity"),
        ("Gum account count", "gum_accounts"),
        ("Gum raw JUP pubkey hits", "gum_jup_raw_hits"),
        ("Gum JUP text hits", "gum_jup_text_hits"),
        ("OpenID raw JUP pubkey hits", "openid_jup_raw_hits"),
        ("OpenID JUP text hits", "openid_jup_text_hits"),
        ("JUP mint present on JupNet", "jup_mint_present"),
        ("JUP token accounts on JupNet", "jup_token_accounts"),
        ("Gum ProgramData", "gum_programdata"),
        ("Gum deployment slot", "gum_deployment_slot"),
        ("Gum upgrade authority", "gum_upgrade_authority"),
        ("Gum validator-key hits", "gum_validator_hits"),
        ("OpenID validator-key hits", "openid_validator_hits"),
        ("Sample tx validator-key hits", "sample_tx_validator_hits"),
        ("Bank account present", "bank_present"),
        ("Bank account owner", "bank_owner"),
        ("Bank account executable", "bank_executable"),
        ("Bank account data hash", "bank_data_hash"),
        ("Bank Program present", "bank_program_present"),
        ("Bank Program owner", "bank_program_owner"),
        ("Bank Program executable", "bank_program_executable"),
        ("Bank Program data hash", "bank_program_data_hash"),
        ("Bank ProgramData", "bank_programdata"),
        ("Bank deployment slot", "bank_deployment_slot"),
        ("Bank upgrade authority", "bank_upgrade_authority"),
        ("Bank Program-owned account count", "bank_program_owned_accounts"),
        ("Gum/Bank signature overlap", "gum_bank_signature_overlap"),
        ("Gum/Bank Program signature overlap", "gum_bank_program_signature_overlap"),
        ("Sample Bank tx validator-key hits", "bank_sample_tx_validator_hits"),
        ("Sample Bank tx canonical JUP account hits", "bank_sample_tx_jup_account_hits"),
        ("Sample Bank tx watched Gum/Bank/JUP account hits", "bank_sample_tx_watched_hits"),
        ("Solana Bank present", "solana_bank_present"),
        ("Solana Bank owner", "solana_bank_owner"),
        ("Solana Bank executable", "solana_bank_executable"),
        ("Solana Bank data hash", "solana_bank_data_hash"),
        ("Solana Bank Program present", "solana_bank_program_present"),
        ("Solana Bank Program owner", "solana_bank_program_owner"),
        ("Solana Bank Program executable", "solana_bank_program_executable"),
        ("Solana Bank Program data hash", "solana_bank_program_data_hash"),
        ("Solana Bank ProgramData", "solana_bank_programdata"),
        ("Solana Bank deployment slot", "solana_bank_deployment_slot"),
        ("Solana Bank upgrade authority", "solana_bank_upgrade_authority"),
        ("Solana Bank Program ProgramData", "solana_bank_program_programdata"),
        ("Solana Bank Program deployment slot", "solana_bank_program_deployment_slot"),
        ("Solana Bank Program upgrade authority", "solana_bank_program_upgrade_authority"),
        ("Sample Solana Bank tx canonical JUP account hits", "solana_bank_sample_tx_jup_account_hits"),
        ("Sample Solana Bank tx watched Gum/Bank/JUP account hits", "solana_bank_sample_tx_watched_hits"),
        ("Sample Solana Bank inbox/outbox log hits", "solana_bank_inbox_outbox_log_hits"),
        ("Bank account graph present", "bank_graph_present"),
        ("Bank account graph canonical JUP account hits", "bank_graph_jup_account_hits"),
        ("Bank recurring account report present", "bank_recurring_present"),
        ("Bank recurring account JUP raw hits", "bank_recurring_jup_raw_hits"),
        ("Bank recurring account JUP text hits", "bank_recurring_jup_text_hits"),
        ("Bank recurring account validator-key hits", "bank_recurring_validator_hits"),
        ("Bank recurring Bank-owned state count", "bank_recurring_bank_owned_state"),
        ("Bank owner context report present", "bank_owner_context_present"),
        ("Bank owner context JUP key hits", "bank_owner_context_jup_hits"),
        ("Bank owner context validator-key hits", "bank_owner_context_validator_hits"),
        ("Bank owner context ProgramData count", "bank_owner_context_programdata_count"),
        ("JupNet helper account report present", "helper_program_accounts_present"),
        ("JupNet inbox-owned account count", "helper_inbox_accounts"),
        ("JupNet outbox-owned account count", "helper_outbox_accounts"),
        ("JupNet helper account JUP hits", "helper_jup_hits"),
        ("JupNet helper account validator-key hits", "helper_validator_hits"),
        ("Verify request report present", "verify_request_report_present"),
        ("Verify request sample count", "verify_request_samples"),
        ("Verify request JUP key hits", "verify_request_jup_hits"),
        ("Verify request validator-key hits", "verify_request_validator_hits"),
        ("Verify request proof node count", "verify_request_proof_nodes"),
        ("Outbox root update report present", "outbox_root_update_report_present"),
        ("Outbox root update/BLS candidate count", "outbox_root_update_candidates"),
        ("Outbox root update JUP key hits", "outbox_root_update_jup_hits"),
        ("Outbox root update validator-key hits", "outbox_root_update_validator_hits"),
        ("Private runtime fingerprint report present", "private_runtime_fingerprints_present"),
        ("Private runtime dependency terms with hits", "private_runtime_dependency_terms_with_hits"),
        ("Private runtime security-producer terms with hits", "private_runtime_security_producer_terms_with_hits"),
        ("Private runtime public-verifier terms with hits", "private_runtime_public_verifier_terms_with_hits"),
        ("Private runtime source paths recovered", "private_runtime_source_paths_recovered"),
        ("Outbox root history report present", "outbox_root_history_present"),
        ("Outbox root history transaction files", "outbox_root_history_tx_files"),
        ("Outbox root history update payloads", "outbox_root_history_updates"),
        ("Outbox root history verifier payloads", "outbox_root_history_verifiers"),
        ("Outbox root history security-hit rows", "outbox_root_history_security_hit_rows"),
        ("Outbox root history latest update", "outbox_root_history_latest_update"),
        ("Root update authority graph present", "root_update_authority_present"),
        ("Root update authority update count", "root_update_authority_updates"),
        ("Root update authority tx signer count", "root_update_authority_tx_signer_count"),
        ("Root update authority instruction signer count", "root_update_authority_instruction_signer_count"),
        ("Root update authority writable account count", "root_update_authority_writable_account_count"),
        ("Root update authority security-intersection count", "root_update_authority_security_intersection_count"),
        ("Root update authority upgrade-intersection count", "root_update_authority_upgrade_intersection_count"),
        ("Root submitter provenance report present", "root_submitter_provenance_present"),
        ("Root submitter count", "root_submitter_count"),
        ("Root submitter transaction occurrences", "root_submitter_occurrence_tx_count"),
        ("Root submitter signer transaction occurrences", "root_submitter_signer_tx_count"),
        ("Root submitter security-intersection count", "root_submitter_security_intersection_count"),
        ("Root submitter upgrade-intersection count", "root_submitter_upgrade_intersection_count"),
        ("Outbox verifier field-map report present", "outbox_verifier_map_present"),
        ("Outbox verifier field-map payloads", "outbox_verifier_map_payloads"),
        ("Outbox verifier field-map Bank wrappers", "outbox_verifier_map_bank_wrappers"),
        ("Outbox verifier field-map inner payloads", "outbox_verifier_map_inner_payloads"),
        ("Outbox verifier field-map JUP-hit payloads", "outbox_verifier_map_jup_hits"),
        ("Outbox verifier field-map validator-hit payloads", "outbox_verifier_map_validator_hits"),
        ("Outbox verifier field-map root mismatches", "outbox_verifier_map_root_mismatches"),
        ("JupNet executable census report present", "jupnet_executable_census_present"),
        ("JupNet executable count", "jupnet_executable_count"),
        ("JupNet executable source-path count", "jupnet_executable_source_path_count"),
        ("JupNet executable high-value term count", "jupnet_executable_high_value_count"),
        ("JupNet executable key-hit count", "jupnet_executable_key_hit_count"),
        ("JupNet executable verifier-syscall count", "jupnet_executable_verifier_count"),
    ]
    for label, key in watched_scalars:
        line = delta_line(label, old.get(key), new.get(key))
        if not line:
            continue
        if key in {
            "gum_jup_raw_hits",
            "openid_jup_raw_hits",
            "jup_mint_present",
            "jup_token_accounts",
            "gum_programdata",
            "gum_deployment_slot",
            "gum_upgrade_authority",
            "gum_validator_hits",
            "openid_validator_hits",
            "sample_tx_validator_hits",
            "bank_present",
            "bank_owner",
            "bank_executable",
            "bank_data_hash",
            "bank_program_present",
            "bank_program_owner",
            "bank_program_executable",
            "bank_program_data_hash",
            "bank_programdata",
            "bank_deployment_slot",
            "bank_upgrade_authority",
            "gum_bank_signature_overlap",
            "gum_bank_program_signature_overlap",
            "bank_sample_tx_validator_hits",
            "bank_sample_tx_jup_account_hits",
            "bank_sample_tx_watched_hits",
            "solana_bank_present",
            "solana_bank_owner",
            "solana_bank_executable",
            "solana_bank_data_hash",
            "solana_bank_program_present",
            "solana_bank_program_owner",
            "solana_bank_program_executable",
            "solana_bank_program_data_hash",
            "solana_bank_programdata",
            "solana_bank_deployment_slot",
            "solana_bank_upgrade_authority",
            "solana_bank_program_programdata",
            "solana_bank_program_deployment_slot",
            "solana_bank_program_upgrade_authority",
            "solana_bank_sample_tx_jup_account_hits",
            "solana_bank_sample_tx_watched_hits",
            "solana_bank_inbox_outbox_log_hits",
            "bank_graph_present",
            "bank_graph_jup_account_hits",
            "bank_recurring_present",
            "bank_recurring_jup_raw_hits",
            "bank_recurring_jup_text_hits",
            "bank_recurring_validator_hits",
            "bank_recurring_bank_owned_state",
            "bank_owner_context_present",
            "bank_owner_context_jup_hits",
            "bank_owner_context_validator_hits",
            "bank_owner_context_programdata_count",
            "helper_program_accounts_present",
            "helper_inbox_accounts",
            "helper_outbox_accounts",
            "helper_jup_hits",
            "helper_validator_hits",
            "verify_request_report_present",
            "verify_request_samples",
            "verify_request_jup_hits",
            "verify_request_validator_hits",
            "verify_request_proof_nodes",
            "outbox_root_update_report_present",
            "outbox_root_update_candidates",
            "outbox_root_update_jup_hits",
            "outbox_root_update_validator_hits",
            "private_runtime_fingerprints_present",
            "private_runtime_dependency_terms_with_hits",
            "private_runtime_security_producer_terms_with_hits",
            "private_runtime_public_verifier_terms_with_hits",
            "private_runtime_source_paths_recovered",
            "outbox_root_history_present",
            "outbox_root_history_tx_files",
            "outbox_root_history_updates",
            "outbox_root_history_verifiers",
            "outbox_root_history_security_hit_rows",
            "outbox_root_history_latest_update",
            "root_update_authority_present",
            "root_update_authority_updates",
            "root_update_authority_tx_signer_count",
            "root_update_authority_instruction_signer_count",
            "root_update_authority_writable_account_count",
            "root_update_authority_security_intersection_count",
            "root_update_authority_upgrade_intersection_count",
            "root_submitter_provenance_present",
            "root_submitter_count",
            "root_submitter_occurrence_tx_count",
            "root_submitter_signer_tx_count",
            "root_submitter_security_intersection_count",
            "root_submitter_upgrade_intersection_count",
            "outbox_verifier_map_present",
            "outbox_verifier_map_payloads",
            "outbox_verifier_map_bank_wrappers",
            "outbox_verifier_map_inner_payloads",
            "outbox_verifier_map_jup_hits",
            "outbox_verifier_map_validator_hits",
            "outbox_verifier_map_root_mismatches",
            "jupnet_executable_census_present",
            "jupnet_executable_count",
            "jupnet_executable_source_path_count",
            "jupnet_executable_high_value_count",
            "jupnet_executable_key_hit_count",
            "jupnet_executable_verifier_count",
        }:
            alerts.append(line)
        else:
            info.append(line)

    alerts.extend(set_delta("Validator node", old["node_keys"], new["node_keys"]))
    alerts.extend(set_delta("Vote account", old["vote_keys"], new["vote_keys"]))
    alerts.extend(set_delta("Stake account", old["stake_accounts"], new["stake_accounts"]))
    alerts.extend(set_delta("Bank account graph PDA match", old["bank_graph_pda_matches"], new["bank_graph_pda_matches"]))
    alerts.extend(
        set_delta(
            "Bank owner context ProgramData",
            old["bank_owner_context_programdata_set"],
            new["bank_owner_context_programdata_set"],
        )
    )
    alerts.extend(set_delta("Outbox root-history epoch", old["outbox_root_history_epochs"], new["outbox_root_history_epochs"]))
    alerts.extend(set_delta("Outbox root-history root", old["outbox_root_history_roots"], new["outbox_root_history_roots"]))
    alerts.extend(
        set_delta(
            "Outbox root-history aggregate key",
            old["outbox_root_history_aggregate_keys"],
            new["outbox_root_history_aggregate_keys"],
        )
    )
    alerts.extend(
        set_delta(
            "Outbox root-history compact verifier field",
            old["outbox_root_history_compact_fields"],
            new["outbox_root_history_compact_fields"],
        )
    )
    alerts.extend(
        set_delta(
            "Outbox verifier recomputed root",
            old["outbox_root_history_verifier_roots"],
            new["outbox_root_history_verifier_roots"],
        )
    )
    alerts.extend(
        set_delta(
            "Outbox verifier aggregate key",
            old["outbox_root_history_verifier_aggregate_keys"],
            new["outbox_root_history_verifier_aggregate_keys"],
        )
    )
    alerts.extend(set_delta("Root update tx signer", old["root_update_authority_tx_signers"], new["root_update_authority_tx_signers"]))
    alerts.extend(
        set_delta(
            "Root update instruction signer",
            old["root_update_authority_instruction_signers"],
            new["root_update_authority_instruction_signers"],
        )
    )
    alerts.extend(
        set_delta(
            "Root update writable account",
            old["root_update_authority_writable_accounts"],
            new["root_update_authority_writable_accounts"],
        )
    )
    alerts.extend(
        set_delta(
            "Root update JUP/validator/vote/stake intersection",
            old["root_update_authority_security_intersections"],
            new["root_update_authority_security_intersections"],
        )
    )
    alerts.extend(
        set_delta(
            "Root update upgrade-authority intersection",
            old["root_update_authority_upgrade_intersections"],
            new["root_update_authority_upgrade_intersections"],
        )
    )
    alerts.extend(set_delta("Root submitter", old["root_submitters"], new["root_submitters"]))
    alerts.extend(set_delta("Root submitter occurrence file", old["root_submitter_occurrence_files"], new["root_submitter_occurrence_files"]))
    alerts.extend(set_delta("Root submitter signer file", old["root_submitter_signer_files"], new["root_submitter_signer_files"]))
    alerts.extend(set_delta("Root submitter invoked program", old["root_submitter_programs"], new["root_submitter_programs"]))
    alerts.extend(
        set_delta(
            "Root submitter JUP/validator/vote/stake intersection",
            old["root_submitter_security_intersections"],
            new["root_submitter_security_intersections"],
        )
    )
    alerts.extend(
        set_delta(
            "Root submitter upgrade-authority intersection",
            old["root_submitter_upgrade_intersections"],
            new["root_submitter_upgrade_intersections"],
        )
    )
    alerts.extend(set_delta("Outbox verifier sender/program", old["outbox_verifier_map_senders"], new["outbox_verifier_map_senders"]))
    alerts.extend(set_delta("Outbox verifier field-map aggregate key", old["outbox_verifier_map_aggregate_keys"], new["outbox_verifier_map_aggregate_keys"]))
    alerts.extend(set_delta("Outbox verifier field-map root", old["outbox_verifier_map_roots"], new["outbox_verifier_map_roots"]))
    alerts.extend(set_delta("Outbox verifier field-map layout", old["outbox_verifier_map_layouts"], new["outbox_verifier_map_layouts"]))
    alerts.extend(set_delta("Private runtime dependency hit term", old["private_runtime_dependency_hit_terms"], new["private_runtime_dependency_hit_terms"]))
    alerts.extend(
        set_delta(
            "Private runtime security-producer hit term",
            old["private_runtime_security_producer_hit_terms"],
            new["private_runtime_security_producer_hit_terms"],
        )
    )
    alerts.extend(set_delta("Private runtime public-verifier hit term", old["private_runtime_public_verifier_hit_terms"], new["private_runtime_public_verifier_hit_terms"]))
    alerts.extend(set_delta("JupNet executable", old["jupnet_executable_records"], new["jupnet_executable_records"]))
    alerts.extend(
        set_delta(
            "JupNet executable verifier-syscall consumer",
            old["jupnet_executable_verifier_records"],
            new["jupnet_executable_verifier_records"],
        )
    )
    alerts.extend(set_delta("JupNet executable key-hit row", old["jupnet_executable_key_hit_records"], new["jupnet_executable_key_hit_records"]))
    alerts.extend(set_delta("JupNet executable high-value row", old["jupnet_executable_high_value_records"], new["jupnet_executable_high_value_records"]))
    alerts.extend(set_delta("JupNet executable authority", old["jupnet_executable_authority_records"], new["jupnet_executable_authority_records"]))

    new_gum_sigs = sorted(new["gum_signature_set"] - old["gum_signature_set"])
    if new_gum_sigs:
        alerts.append(f"- New Gum signatures in signature window: `{len(new_gum_sigs)}`")
    new_sample_txs = sorted(new["sample_tx_signatures"] - old["sample_tx_signatures"])
    if new_sample_txs:
        alerts.append(f"- New sampled Gum transaction bodies: `{len(new_sample_txs)}`")
    new_bank_program_sigs = sorted(new["bank_program_signature_set"] - old["bank_program_signature_set"])
    if new_bank_program_sigs:
        alerts.append(f"- New Bank Program signatures in signature window: `{len(new_bank_program_sigs)}`")
    new_bank_sample_txs = sorted(new["bank_sample_tx_signatures"] - old["bank_sample_tx_signatures"])
    if new_bank_sample_txs:
        alerts.append(f"- New sampled Bank Program transaction bodies: `{len(new_bank_sample_txs)}`")
    new_solana_bank_sample_txs = sorted(
        new["solana_bank_sample_tx_signatures"] - old["solana_bank_sample_tx_signatures"]
    )
    if new_solana_bank_sample_txs:
        alerts.append(f"- New sampled Solana Bank Program transaction bodies: `{len(new_solana_bank_sample_txs)}`")

    print("# Validator Security Snapshot Diff")
    print()
    print(f"- Old snapshot: `{old_base}`")
    print(f"- New snapshot: `{new_base}`")
    print(f"- Old slot: `{old.get('slot')}`")
    print(f"- New slot: `{new.get('slot')}`")
    print()
    print("## Alerts")
    print()
    if alerts:
        for line in alerts:
            print(line)
    else:
        print("- No watched security-surface changes detected.")
    print()
    print("## Informational Deltas")
    print()
    if info:
        for line in info:
            print(line)
    else:
        print("- No informational deltas detected.")
    print()
    print("## Current Snapshot Summary")
    print()
    print(f"- Validators: `{len(new['node_keys'])}`")
    print(f"- Vote accounts: `{len(new['vote_keys'])}`")
    print(f"- Stake accounts: `{len(new['stake_accounts'])}`")
    print(f"- Gum JUP raw pubkey hits: `{new['gum_jup_raw_hits']}`")
    print(f"- Gum JUP text hits: `{new['gum_jup_text_hits']}`")
    print(f"- JUP token accounts on JupNet: `{new['jup_token_accounts']}`")
    print(f"- Gum upgrade authority: `{new['gum_upgrade_authority']}`")
    print(f"- Sample tx validator-key hits: `{new['sample_tx_validator_hits']}`")
    print(f"- Outbox root-history update payloads: `{new['outbox_root_history_updates']}`")
    print(f"- Outbox root-history security-hit rows: `{new['outbox_root_history_security_hit_rows']}`")
    print(f"- Root update tx signers: `{new['root_update_authority_tx_signer_count']}`")
    print(f"- Root update writable accounts: `{new['root_update_authority_writable_account_count']}`")
    print(f"- Root update security intersections: `{new['root_update_authority_security_intersection_count']}`")
    print(f"- Root update upgrade-authority intersections: `{new['root_update_authority_upgrade_intersection_count']}`")
    print(f"- Root submitters: `{new['root_submitter_count']}`")
    print(f"- Root submitter tx occurrences: `{new['root_submitter_occurrence_tx_count']}`")
    print(f"- Root submitter security intersections: `{new['root_submitter_security_intersection_count']}`")
    print(f"- Outbox verifier field-map sender/programs: `{len(new['outbox_verifier_map_senders'])}`")
    print(f"- JupNet executable verifier-syscall consumers: `{new['jupnet_executable_verifier_count']}`")
    print(f"- JupNet executable key-hit rows: `{new['jupnet_executable_key_hit_count']}`")
    print(f"- Private runtime dependency terms with hits: `{new['private_runtime_dependency_terms_with_hits']}`")
    print(f"- Private runtime security-producer terms with hits: `{new['private_runtime_security_producer_terms_with_hits']}`")


if __name__ == "__main__":
    main()
