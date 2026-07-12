#!/usr/bin/env python3
"""Compare two JupNet validator-security snapshots and emit alert-oriented Markdown."""

from __future__ import annotations

import argparse
import base64
import json
import struct
from pathlib import Path


ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
JUP_MINT = "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN"
GUM_PROGRAM = "brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1"


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


def parse_gum_programdata(base: Path) -> tuple[str | None, int | None, str | None]:
    program = result(base, "getAccountInfo-GumProgram.json")
    programdata = None
    if program and program.get("value"):
        raw = raw_account_data(program["value"])
        if len(raw) >= 36 and struct.unpack("<I", raw[:4])[0] == 2:
            programdata = b58encode(raw[4:36])

    deployment_slot = None
    authority = None
    data = result(base, "getAccountInfo-GumProgramData-slice48.json")
    if data and data.get("value"):
        raw = raw_account_data(data["value"])
        if len(raw) >= 45 and struct.unpack("<I", raw[:4])[0] == 3:
            deployment_slot = struct.unpack("<Q", raw[4:12])[0]
            authority = b58encode(raw[13:45]) if raw[12] == 1 else None
    return programdata, deployment_slot, authority


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


def snapshot_metrics(base: Path) -> dict:
    jup_raw = b58decode(JUP_MINT)
    gum_records = account_records(base, "getProgramAccounts-Gum.json")
    openid_records = account_records(base, "getProgramAccounts-OpenIDRegistry.json")
    programdata, deployment_slot, authority = parse_gum_programdata(base)
    related = validator_related_keys(base)
    tx_sigs, authority_signed, tx_validator_hits = tx_rows(base, authority, related)
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
        "gum_signature_set": {item["signature"] for item in signatures},
        "sample_tx_signatures": tx_sigs,
        "sample_tx_authority_signed": authority_signed,
        "sample_tx_validator_hits": tx_validator_hits,
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
        }:
            alerts.append(line)
        else:
            info.append(line)

    alerts.extend(set_delta("Validator node", old["node_keys"], new["node_keys"]))
    alerts.extend(set_delta("Vote account", old["vote_keys"], new["vote_keys"]))
    alerts.extend(set_delta("Stake account", old["stake_accounts"], new["stake_accounts"]))

    new_gum_sigs = sorted(new["gum_signature_set"] - old["gum_signature_set"])
    if new_gum_sigs:
        alerts.append(f"- New Gum signatures in signature window: `{len(new_gum_sigs)}`")
    new_sample_txs = sorted(new["sample_tx_signatures"] - old["sample_tx_signatures"])
    if new_sample_txs:
        alerts.append(f"- New sampled Gum transaction bodies: `{len(new_sample_txs)}`")

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


if __name__ == "__main__":
    main()
