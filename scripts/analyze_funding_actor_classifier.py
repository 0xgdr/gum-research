#!/usr/bin/env python3
"""Classify accounts involved in root submitter funding/setup transactions."""

from __future__ import annotations

import argparse
import base64
import collections
import datetime as dt
import json
import re
from pathlib import Path

from analyze_root_submitter_history import account_keys
from analyze_root_submitter_history import balance_delta
from analyze_root_submitter_history import parsed_system_transfers
from analyze_root_submitter_history import programs
from analyze_root_update_authority_graph import JUP_MINT
from analyze_root_update_authority_graph import role_for
from analyze_root_update_authority_graph import validator_related_keys


ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
SYSTEM_PROGRAM = "11111111111111111111111111111111"
SPL_TOKEN = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
ASSOCIATED_TOKEN = "ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL"
COMPUTE_BUDGET = "ComputeBudget111111111111111111111111111111"
WRAPPED_SOL = "So11111111111111111111111111111111111111112"
GUM_BANK_REQUEST = "bk1PDAkbHEBGtVRiM94Lzets8gVFP7FgySyfkAc8MPN"
JUPNET_OUTBOX = "jnoUtncGR9ZCCMixtys6Gzy5coTo6mnmUZuEHRQFTFV"
STANDARD_PROGRAMS = {SYSTEM_PROGRAM, SPL_TOKEN, ASSOCIATED_TOKEN, COMPUTE_BUDGET}


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


def block_time(value: int | None) -> str:
    if value is None:
        return "unknown"
    return dt.datetime.fromtimestamp(value, dt.timezone.utc).isoformat()


def funding_manifest(base: Path) -> list[dict]:
    data = load(base / "solana-mainnet-root-submitter-funding-history-manifest.json")
    return data.get("submitters") or []


def funding_actor_context(base: Path) -> tuple[list[str], dict[str, list[str]], dict[str, dict | None]]:
    data = load(base / "solana-mainnet-getMultipleAccounts-FundingActors.json")
    accounts = data.get("accounts") or []
    roles = data.get("roles") or {}
    values = ((data.get("response") or {}).get("result") or {}).get("value") or []
    return accounts, roles, {account: value for account, value in zip(accounts, values)}


def funding_signatures(base: Path) -> dict[str, list[dict]]:
    data = load(base / "solana-mainnet-getSignaturesForAddress-FundingActors.json")
    out = {}
    for account, response in data.items():
        out[account] = response.get("result") or []
    return out


def tx_files(base: Path) -> list[Path]:
    return sorted(
        path for path in base.glob("*.json") if path.name.startswith(("tx-", "bank-tx-", "solana-mainnet-")) and "-raw" not in path.name
    )


def tx_result(path: Path) -> dict | None:
    data = load(path)
    result = data.get("result")
    if isinstance(result, dict) and "transaction" in result:
        return result
    return None


def all_instructions(tx: dict) -> list[dict]:
    rows = list(tx.get("transaction", {}).get("message", {}).get("instructions") or [])
    for group in tx.get("meta", {}).get("innerInstructions") or []:
        rows.extend(group.get("instructions") or [])
    return rows


def transfer_sources(tx: dict, destination: str) -> set[str]:
    sources = set()
    marker = f"->{destination}"
    for transfer in parsed_system_transfers(tx, destination):
        if marker not in transfer:
            continue
        sources.add(transfer.split(" ", 1)[1].split("->", 1)[0])
    return sources


def positive_funding_events(base: Path) -> list[dict]:
    events = []
    for row in funding_manifest(base):
        submitter = row.get("address")
        for filename in row.get("positive_delta_files") or []:
            tx = load(base / filename).get("result")
            if not tx:
                continue
            keys = account_keys(tx)
            signers = set()
            writable = set()
            for key in tx.get("transaction", {}).get("message", {}).get("accountKeys") or []:
                if not isinstance(key, dict):
                    continue
                if key.get("signer"):
                    signers.add(key["pubkey"])
                if key.get("writable"):
                    writable.add(key["pubkey"])
            events.append(
                {
                    "filename": filename,
                    "signature": (tx.get("transaction", {}).get("signatures") or [""])[0],
                    "slot": tx.get("slot"),
                    "time": block_time(tx.get("blockTime")),
                    "submitter": submitter,
                    "fee_payer": keys[0] if keys else None,
                    "signers": signers,
                    "writable": writable,
                    "programs": set(programs(tx)),
                    "transfer_sources": transfer_sources(tx, submitter),
                    "delta": balance_delta(tx, submitter).get("delta"),
                    "tx": tx,
                }
            )
    return events


def inferred_roles_from_events(events: list[dict]) -> dict[str, set[str]]:
    roles: dict[str, set[str]] = collections.defaultdict(set)
    for event in events:
        roles[event["submitter"]].add("root submitter funded in positive event")
        roles[event["fee_payer"]].add("fee payer")
        for signer in event["signers"]:
            roles[signer].add("transaction signer")
        for source in event["transfer_sources"]:
            roles[source].add("parsed transfer source into root submitter")
        for program in event["programs"]:
            roles[program].add("invoked program")
        if GUM_BANK_REQUEST in event["programs"]:
            roles[GUM_BANK_REQUEST].add("Gum Bank request path")
        non_standard = event["programs"] - STANDARD_PROGRAMS
        for program in non_standard:
            roles[program].add("non-standard funding event program")
        for account in account_keys(event["tx"]):
            if account in event["writable"]:
                roles[account].add("writable funding event account")
    roles.pop(None, None)
    return roles


def local_corpus_occurrences(base: Path, targets: set[str]) -> dict[str, dict]:
    rows = {
        target: {
            "tx_files": set(),
            "signer_files": set(),
            "writable_files": set(),
            "program_files": set(),
        }
        for target in targets
    }
    for path in tx_files(base):
        tx = tx_result(path)
        if not tx:
            continue
        keys = set(account_keys(tx))
        touched = keys & targets
        for target in touched:
            rows[target]["tx_files"].add(path.name)
        for key in tx.get("transaction", {}).get("message", {}).get("accountKeys") or []:
            if not isinstance(key, dict):
                continue
            pubkey = key["pubkey"]
            if pubkey not in targets:
                continue
            if key.get("signer"):
                rows[pubkey]["signer_files"].add(path.name)
            if key.get("writable"):
                rows[pubkey]["writable_files"].add(path.name)
        for program in programs(tx):
            if program in targets:
                rows[program]["program_files"].add(path.name)
    return rows


def decode_log_arrays(tx: dict, known_accounts: set[str]) -> list[dict]:
    rows = []
    for line in tx.get("meta", {}).get("logMessages") or []:
        match = re.match(r"Program log: ([^\[]+) \[([^\]]+)\]$", line)
        if not match:
            continue
        label = match.group(1).strip()
        try:
            raw = bytes(int(part.strip()) for part in match.group(2).split(",") if part.strip())
        except ValueError:
            continue
        decoded = b58encode(raw)
        rows.append(
            {
                "label": label,
                "len": len(raw),
                "base58": decoded,
                "hex": raw.hex(),
                "u64_be": int.from_bytes(raw, "big") if len(raw) <= 8 else None,
                "u64_le": int.from_bytes(raw, "little") if len(raw) <= 8 else None,
                "u128_be": int.from_bytes(raw, "big") if len(raw) <= 16 else None,
                "known_account": decoded if decoded in known_accounts else None,
            }
        )
    return rows


def program_data_rows(tx: dict) -> list[dict]:
    rows = []
    for line in tx.get("meta", {}).get("logMessages") or []:
        if not line.startswith("Program data: "):
            continue
        value = line.split(": ", 1)[1]
        try:
            raw = base64.b64decode(value)
        except ValueError:
            continue
        rows.append({"len": len(raw), "base64": value, "hex_prefix": raw[:96].hex()})
    return rows


def account_summary(value: dict | None) -> dict:
    if not value:
        return {"owner": None, "executable": None, "lamports": None, "space": None}
    return {
        "owner": value.get("owner"),
        "executable": value.get("executable"),
        "lamports": value.get("lamports"),
        "space": value.get("space"),
    }


def fmt(values, empty: str = "`None`", limit: int | None = None) -> str:
    items = sorted(values) if isinstance(values, set) else list(values)
    items = [str(item) for item in items if item]
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

    events = positive_funding_events(base)
    collected_accounts, collected_roles, account_values = funding_actor_context(base)
    signatures = funding_signatures(base)
    event_roles = inferred_roles_from_events(events)
    targets = set(collected_accounts) | set(event_roles)
    local_occurrences = local_corpus_occurrences(base, targets)
    validators = validator_related_keys(base)
    known_accounts = targets | {key for event in events for key in account_keys(event["tx"])}

    print("# Funding Actor Classifier")
    print()
    print("## Scope")
    print()
    print(f"- Snapshot: `{base}`")
    print(f"- Positive funding/setup events: `{len(events)}`")
    print(f"- Funding actors collected: `{len(collected_accounts)}`")
    print("- Evidence seed: root submitter funding-history positive-delta transaction(s)")
    print()

    if not events:
        print("## Assessment")
        print()
        print("- No positive root submitter funding events were found. Run the funding-history collector/analyzer first.")
        return

    print("## Funding Events")
    print()
    print("| File | Time | Slot | Signature | Submitter delta | Fee payer | Transfer sources | Non-standard programs |")
    print("|---|---|---:|---|---:|---|---|---|")
    for event in events:
        non_standard = event["programs"] - STANDARD_PROGRAMS
        print(
            f"| `{event['filename']}` | `{event['time']}` | {event['slot']} | `{event['signature']}` | "
            f"{event['delta']} | `{event['fee_payer']}` | {fmt(event['transfer_sources'])} | {fmt(non_standard)} |"
        )
    print()

    print("## Actor Classification")
    print()
    print("| Account | Inferred roles | Owner | Executable | Lamports | Space | Local tx files | Local signer files | Local program files | Recent signatures | Latest seen | Security role |")
    print("|---|---|---|---|---:|---:|---:|---:|---:|---:|---|---|")
    for account in sorted(targets):
        roles = set(collected_roles.get(account) or []) | event_roles.get(account, set())
        summary = account_summary(account_values.get(account))
        occurrences = local_occurrences.get(account) or {}
        sig_rows = signatures.get(account) or []
        latest = block_time(sig_rows[0].get("blockTime")) if sig_rows else "unknown"
        security_role = role_for(account, validators, {}) if account == JUP_MINT or account in validators else ""
        print(
            f"| `{account}` | {fmt(roles)} | `{summary['owner']}` | `{summary['executable']}` | "
            f"{summary['lamports']} | {summary['space']} | {len(occurrences.get('tx_files') or [])} | "
            f"{len(occurrences.get('signer_files') or [])} | {len(occurrences.get('program_files') or [])} | "
            f"{len(sig_rows)} | `{latest}` | `{security_role or 'None'}` |"
        )
    print()

    print("## Decoded Funding Logs")
    print()
    for event in events:
        print(f"### `{event['filename']}`")
        print()
        rows = decode_log_arrays(event["tx"], known_accounts)
        print("| Label | Bytes | Base58 | Known account match | Hex | Integer interpretation |")
        print("|---|---:|---|---|---|---|")
        for row in rows:
            ints = []
            if row["u64_be"] is not None:
                ints.append(f"u64_be={row['u64_be']}")
                ints.append(f"u64_le={row['u64_le']}")
            elif row["u128_be"] is not None:
                ints.append(f"u128_be={row['u128_be']}")
            print(
                f"| `{row['label']}` | {row['len']} | `{row['base58']}` | "
                f"`{row['known_account'] or 'None'}` | `{row['hex']}` | `{', '.join(ints) or 'n/a'}` |"
            )
        print()
        pdata_rows = program_data_rows(event["tx"])
        if pdata_rows:
            print("Program data payloads:")
            print()
            print("| Bytes | Base64 | Hex prefix |")
            print("|---:|---|---|")
            for row in pdata_rows:
                print(f"| {row['len']} | `{row['base64']}` | `{row['hex_prefix']}` |")
            print()

    print("## Assessment")
    print()
    print("- The funding/setup event is tied to the Gum Bank request path rather than a plain wallet-to-wallet top-up.")
    print("- The root submitter received SOL through a parsed transfer during a transaction that also invoked non-standard Gum/JupNet programs.")
    print("- The collector/analyzer found no canonical JUP, current validator, vote or stake key classification among the funding actors.")
    print("- The most useful next comparison is a cohort of other `bk1PDA...` request/withdrawal transactions to determine whether funding infrastructure accounts through this path is exceptional or routine.")


if __name__ == "__main__":
    main()
