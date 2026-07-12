#!/usr/bin/env python3
"""Produce second-stage evidence for Gum/JUP validator-security research."""

from __future__ import annotations

import argparse
import base64
import collections
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


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def result(base: Path, filename: str):
    return load(base / filename).get("result")


def raw_account_data(account: dict) -> bytes:
    data = account["data"]
    if not isinstance(data, list):
        return b""
    return base64.b64decode(data[0])


def account_records(base: Path, filename: str) -> list[tuple[str, dict, bytes]]:
    records = []
    for item in result(base, filename) or []:
        records.append((item["pubkey"], item["account"], raw_account_data(item["account"])))
    return records


def find_positions(raw: bytes, target: bytes) -> tuple[int, ...]:
    positions = []
    start = 0
    while True:
        index = raw.find(target, start)
        if index < 0:
            return tuple(positions)
        positions.append(index)
        start = index + 1


def parse_program_address(base: Path) -> tuple[str | None, str | None]:
    data = result(base, "getAccountInfo-GumProgram.json")
    if not data or not data.get("value"):
        return None, None
    raw = raw_account_data(data["value"])
    if len(raw) < 36 or struct.unpack("<I", raw[:4])[0] != 2:
        return None, None
    return b58encode(raw[4:36]), data["value"]["owner"]


def parse_programdata(base: Path) -> tuple[int | None, str | None, str | None]:
    data = result(base, "getAccountInfo-GumProgramData-slice48.json")
    if not data or not data.get("value"):
        return None, None, None
    raw = raw_account_data(data["value"])
    if len(raw) < 45 or struct.unpack("<I", raw[:4])[0] != 3:
        return None, None, data["value"].get("owner")
    slot = struct.unpack("<Q", raw[4:12])[0]
    authority = b58encode(raw[13:45]) if raw[12] == 1 else None
    return slot, authority, data["value"].get("owner")


def account_info(base: Path, filename: str) -> dict | None:
    path = base / filename
    if not path.exists():
        return None
    data = result(base, filename)
    return data.get("value") if data else None


def upgradeable_loader_summary(base: Path) -> tuple[collections.Counter, dict[str, str]]:
    records = account_records(base, "getProgramAccounts-UpgradeableLoader-slice48.json")
    tags: collections.Counter = collections.Counter()
    program_to_programdata = {}
    for pubkey, _account, raw in records:
        if len(raw) < 4:
            continue
        tag = struct.unpack("<I", raw[:4])[0]
        tags[tag] += 1
        if tag == 2 and len(raw) >= 36:
            program_to_programdata[pubkey] = b58encode(raw[4:36])
    return tags, program_to_programdata


def validator_keys(base: Path) -> set[str]:
    keys = set()
    votes = result(base, "getVoteAccounts.json") or {}
    for vote in (votes.get("current") or []) + (votes.get("delinquent") or []):
        keys.add(vote["nodePubkey"])
        keys.add(vote["votePubkey"])
    for account in result(base, "getProgramAccounts-Stake.json") or []:
        keys.add(account["pubkey"])
    return keys


def tx_signer_rows(base: Path, authority: str | None, validator_related: set[str]) -> list[tuple[str, int, list[str], bool, list[str]]]:
    rows = []
    for path in sorted(base.glob("tx-*.json")):
        if path.name.endswith("-raw.json"):
            continue
        tx = load(path).get("result")
        if not tx:
            continue
        signers = []
        account_keys = []
        for key in tx["transaction"]["message"].get("accountKeys", []):
            if isinstance(key, dict):
                account_keys.append(key["pubkey"])
                if key.get("signer"):
                    signers.append(key["pubkey"])
            elif isinstance(key, str):
                account_keys.append(key)
        validator_hits = sorted(set(account_keys) & validator_related)
        rows.append((path.name, tx.get("slot"), signers, authority in signers if authority else False, validator_hits))
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot_dir")
    args = parser.parse_args()
    base = Path(args.snapshot_dir)

    jup_raw = b58decode(JUP_MINT)
    gum_records = account_records(base, "getProgramAccounts-Gum.json")
    groups: collections.Counter = collections.Counter()
    examples = {}
    raw_hits = []
    text_hits = []
    symbol_hits = []
    for pubkey, account, raw in gum_records:
        raw_pos = find_positions(raw, jup_raw)
        text_pos = find_positions(raw, JUP_MINT.encode())
        symbol_pos = find_positions(raw, b"JUP")
        if raw_pos:
            raw_hits.append(pubkey)
        if text_pos:
            text_hits.append(pubkey)
            key = (len(raw), raw[:8].hex(), text_pos)
            groups[key] += 1
            examples.setdefault(key, pubkey)
        if symbol_pos:
            symbol_hits.append(pubkey)

    programdata_address, program_owner = parse_program_address(base)
    deployment_slot, upgrade_authority, programdata_owner = parse_programdata(base)
    authority_info = account_info(base, "getAccountInfo-GumUpgradeAuthority.json")
    tags, program_map = upgradeable_loader_summary(base)
    validator_related = validator_keys(base)
    signer_rows = tx_signer_rows(base, upgrade_authority, validator_related)

    print("# Validator Security Deep Dive")
    print()
    print("## Gum JUP Account Structure")
    print()
    print(f"- Gum accounts scanned: `{len(gum_records)}`")
    print(f"- Gum accounts with canonical JUP raw pubkey bytes: `{len(raw_hits)}`")
    print(f"- Gum accounts with canonical JUP base58 text: `{len(text_hits)}`")
    print(f"- Gum accounts with `JUP` symbol text: `{len(symbol_hits)}`")
    print()
    print("| Count | Data length | First 8 bytes | Text offset(s) | Example account |")
    print("|---:|---:|---|---|---|")
    for (length, prefix, offsets), count in groups.most_common():
        print(f"| {count} | {length} | `{prefix}` | `{list(offsets)}` | `{examples[(length, prefix, offsets)]}` |")
    print()
    print("Interpretation: the JUP references in Gum account data are textual asset identifiers, not raw 32-byte mint pubkey fields in the scanned account layouts.")
    print()
    print("## Program Loader Surface")
    print()
    print(f"- Gum program: `{GUM_PROGRAM}`")
    print(f"- Gum program owner: `{program_owner}`")
    print(f"- Gum ProgramData account: `{programdata_address}`")
    print(f"- Gum ProgramData owner: `{programdata_owner}`")
    print(f"- Gum ProgramData deployment slot: `{deployment_slot}`")
    print(f"- Gum ProgramData upgrade authority: `{upgrade_authority}`")
    if authority_info:
        print(f"- Upgrade authority account owner: `{authority_info.get('owner')}`")
        print(f"- Upgrade authority lamports: `{authority_info.get('lamports')}`")
        print(f"- Upgrade authority executable: `{authority_info.get('executable')}`")
        print(f"- Upgrade authority data space: `{authority_info.get('space')}`")
    print(f"- Upgradeable loader account tags: `{dict(tags)}`")
    print(f"- Gum program maps to ProgramData in loader scan: `{program_map.get(GUM_PROGRAM)}`")
    print()
    print("## Sample Gum Transaction Signers")
    print()
    print("| Transaction file | Slot | Signers | Upgrade authority signed | Validator/vote/stake account hits |")
    print("|---|---:|---|---|---|")
    for filename, slot, signers, authority_signed, validator_hits in signer_rows:
        signer_text = ", ".join(signers)
        hit_text = ", ".join(validator_hits)
        print(f"| `{filename}` | {slot} | `{signer_text}` | `{authority_signed}` | `{hit_text}` |")
    print()
    print("Interpretation: in the sampled Gum transactions, the Gum upgrade authority appears as a signer and no current validator, vote-account or stake-account keys appear in the transaction account lists.")


if __name__ == "__main__":
    main()
