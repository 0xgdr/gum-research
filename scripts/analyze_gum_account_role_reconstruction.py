#!/usr/bin/env python3
"""Reconstruct Gum/Bank account roles from sampled transactions and verifier payloads."""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import struct
from pathlib import Path

from analyze_bank_account_graph import ASSOCIATED_TOKEN
from analyze_bank_account_graph import GUM_BANK
from analyze_bank_account_graph import GUM_BANK_PROGRAM
from analyze_bank_account_graph import JUP_MINT
from analyze_bank_account_graph import SPL_TOKEN
from analyze_bank_account_graph import SYSVAR_INSTRUCTIONS
from analyze_bank_account_graph import SYSTEM_PROGRAM
from analyze_bank_account_graph import USDC
from analyze_bank_account_graph import WRAPPED_SOL
from analyze_bank_account_graph import anchor_discriminator
from analyze_gum_authorization import GUM_PROGRAM
from analyze_gum_authorization import parse_programdata_authority
from map_outbox_verifier_payloads import collect_rows as verifier_payload_rows


ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
GUMEB_PROGRAM = "GUMebNDCYyF81xjyqaHagbgMQVUTb8fBC9YRh25xSH64"
INBOX_PROGRAM = "JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw"
OUTBOX_PROGRAM = "jnoUtncGR9ZCCMixtys6Gzy5coTo6mnmUZuEHRQFTFV"
OUTBOX_ROOT_ACCOUNT = "3C1LxtpR3Mh5RQjydfeQdvRaAzpStWM7gBi1XzP9oyGt"
INBOX_STATE_ACCOUNT = "9DvDdsw38EB3RPChPqHkgBmntFbM5v79QxMyMSbfXWuy"
INBOX_EVENT_AUTH = "EG9fKpmLgkzCYZdj8uNDhHu5xmeXCZakccV6QmUavbzt"

BANK_VARIANTS = (
    "withdraw",
    "sweep",
    "verify_request",
    "rfq_sell_resolve",
    "rfq_sell_commit",
)

KNOWN_ACCOUNTS = {
    GUM_PROGRAM: "JupNet Gum omnichain executable brhPf",
    GUMEB_PROGRAM: "JupNet Gum omnichain executable GUMeb recovered as verifier sender",
    GUM_BANK: "Solana Gum Bank executable",
    GUM_BANK_PROGRAM: "Solana Gum Bank Program executable",
    INBOX_PROGRAM: "JupNet inbox helper program",
    OUTBOX_PROGRAM: "JupNet outbox helper program",
    INBOX_STATE_ACCOUNT: "inbox helper state/counter account",
    OUTBOX_ROOT_ACCOUNT: "outbox Merkle root-history account",
    INBOX_EVENT_AUTH: "Bank __inbox_event_auth PDA",
    JUP_MINT: "canonical Solana JUP mint",
    USDC: "USDC mint",
    WRAPPED_SOL: "wrapped SOL mint",
    SPL_TOKEN: "SPL Token program",
    ASSOCIATED_TOKEN: "Associated Token program",
    SYSTEM_PROGRAM: "system program",
    SYSVAR_INSTRUCTIONS: "instructions sysvar",
}

GUM_POSITION_HINTS = {
    "1202": {
        0: "candidate created/managed account",
        1: "admin/upgrade authority signer",
        2: "Gum-owned config/state account",
        4: "system program",
        6: "candidate chain_config or readonly Gum config",
    },
    "0a": {
        0: "admin/upgrade authority signer",
        1: "Gum-owned config/state account",
        2: "program id self-reference",
    },
    "0184030000781177": {
        0: "admin/upgrade authority signer",
        1: "admin/upgrade authority signer",
        2: "Gum-owned mint/config state",
        13: "candidate chain_config or readonly Gum config",
        14: "token program",
        15: "system program",
        16: "associated token program",
    },
    "0020000000633166": {
        0: "admin/upgrade authority signer",
        1: "secondary signer/payer",
        2: "Gum-owned mint/config state",
        3: "Gum-owned state",
        7: "candidate chain_config or readonly Gum config",
        8: "token program",
        9: "system program",
    },
}

BANK_POSITION_HINTS = {
    "verify_request": {
        0: "payer/signer",
        2: "Bank state/config candidate",
        3: "outbox Merkle root-history account",
        4: "outbox helper program",
        5: "system program",
        6: "instructions sysvar",
        7: "request/account state candidate",
        8: "Bank Program executable",
    },
    "withdraw": {
        0: "payer/signer",
        3: "Bank state/config candidate",
        4: "recipient/authority candidate",
        6: "destination token account",
        9: "source token account",
        10: "token mint",
        11: "token program",
        14: "Bank inbox event authority PDA",
        15: "inbox state/counter account",
        16: "inbox helper program",
        18: "request/account state candidate",
    },
    "sweep": {
        0: "payer/signer",
        4: "Bank state/config candidate",
        6: "destination token account",
        7: "token mint",
        8: "Bank Program executable",
        11: "token program",
        14: "instructions sysvar",
        15: "Bank inbox event authority PDA",
        16: "inbox state/counter account",
        17: "inbox helper program",
        18: "request/account state candidate",
    },
    "rfq_sell_resolve": {
        0: "payer/signer",
        3: "Bank-owned compact state candidate",
        4: "Bank state/config candidate",
        7: "token mint",
        10: "destination/source token account",
        13: "token program",
    },
    "rfq_sell_commit": {
        0: "payer/signer",
        3: "Bank-owned compact state candidate",
        4: "Bank state/config candidate",
        7: "token mint",
        10: "destination/source token account",
        13: "token program",
    },
}


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
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def result(base: Path, filename: str):
    return load(base / filename).get("result")


def account_metas(tx: dict) -> dict[str, dict]:
    metas = {}
    for index, key in enumerate(tx.get("transaction", {}).get("message", {}).get("accountKeys", [])):
        if isinstance(key, dict):
            metas[key["pubkey"]] = {
                "index": index,
                "signer": bool(key.get("signer")),
                "writable": bool(key.get("writable")),
                "source": key.get("source"),
            }
        elif isinstance(key, str):
            metas[key] = {"index": index, "signer": False, "writable": False, "source": "unknown"}
    return metas


def token_hints(tx: dict) -> dict[str, dict]:
    keys = tx.get("transaction", {}).get("message", {}).get("accountKeys", [])
    hints = {}
    for balance_key in ("preTokenBalances", "postTokenBalances"):
        for row in tx.get("meta", {}).get(balance_key) or []:
            index = row.get("accountIndex")
            if not isinstance(index, int) or index >= len(keys):
                continue
            key = keys[index]
            pubkey = key.get("pubkey") if isinstance(key, dict) else key
            if not isinstance(pubkey, str):
                continue
            hints.setdefault(pubkey, {}).update(
                {
                    "mint": row.get("mint"),
                    "owner": row.get("owner"),
                    "token_program": row.get("programId"),
                }
            )
    return hints


def gum_owned_accounts(base: Path) -> set[str]:
    return {item["pubkey"] for item in result(base, "getProgramAccounts-Gum.json") or []}


def validator_related_keys(base: Path) -> set[str]:
    keys = set()
    votes = result(base, "getVoteAccounts.json") or {}
    for vote in (votes.get("current") or []) + (votes.get("delinquent") or []):
        keys.add(vote["nodePubkey"])
        keys.add(vote["votePubkey"])
    for account in result(base, "getProgramAccounts-Stake.json") or []:
        keys.add(account["pubkey"])
    return keys


def role_label(account: str, token_hints: dict[str, dict], gum_owned: set[str], authority: str | None, validators: set[str]) -> str:
    labels = []
    if account in KNOWN_ACCOUNTS:
        labels.append(KNOWN_ACCOUNTS[account])
    if account == authority:
        labels.append("Gum upgrade/admin authority")
    if account in gum_owned:
        labels.append("JupNet Gum-owned account")
    if account in validators:
        labels.append("current JupNet validator/vote/stake key")
    hint = token_hints.get(account)
    if hint:
        labels.append(f"token account mint={hint.get('mint')} owner={hint.get('owner')}")
    return "; ".join(labels)


def fmt(values: list[str] | tuple[str, ...], empty: str = "`None`", limit: int | None = None) -> str:
    items = [value for value in values if value]
    if limit is not None:
        items = items[:limit]
    if not items:
        return empty
    return "<br>".join(f"`{value}`" for value in items)


def fmt_counter(counter: collections.Counter, limit: int | None = None) -> str:
    return fmt([f"{key}: {value}" for key, value in counter.most_common(limit)], limit=limit)


def bank_name_for(raw: bytes) -> str:
    disc = raw[:8].hex()
    lookup = {anchor_discriminator(name): name for name in BANK_VARIANTS}
    return lookup.get(disc, "")


def direct_gum_rows(base: Path) -> list[dict]:
    rows = []
    gum_owned = gum_owned_accounts(base)
    validators = validator_related_keys(base)
    authority = parse_programdata_authority(base)
    for path in sorted(base.glob("tx-*.json")):
        tx = load(path).get("result")
        if not tx:
            continue
        metas = account_metas(tx)
        hints = token_hints(tx)
        for ix_index, ix in enumerate(tx.get("transaction", {}).get("message", {}).get("instructions", [])):
            if ix.get("programId") != GUM_PROGRAM:
                continue
            raw = b58decode(ix.get("data") or "")
            disc = raw[:8].hex()
            accounts = ix.get("accounts") or []
            rows.append(
                {
                    "file": path.name,
                    "slot": tx.get("slot"),
                    "signature": (tx.get("transaction", {}).get("signatures") or [""])[0],
                    "instruction_index": ix_index,
                    "discriminator": disc,
                    "raw_len": len(raw),
                    "accounts": [
                        {
                            "position": position,
                            "account": account,
                            "signer": metas.get(account, {}).get("signer", False),
                            "writable": metas.get(account, {}).get("writable", False),
                            "meta_index": metas.get(account, {}).get("index"),
                            "role": role_label(account, hints, gum_owned, authority, validators),
                            "hint": GUM_POSITION_HINTS.get(disc, {}).get(position, ""),
                        }
                        for position, account in enumerate(accounts)
                    ],
                }
            )
    return rows


def bank_rows(base: Path) -> list[dict]:
    rows = []
    gum_owned = gum_owned_accounts(base)
    validators = validator_related_keys(base)
    authority = parse_programdata_authority(base)
    for path in sorted(base.glob("solana-mainnet-bank-tx-*.json")) + sorted(base.glob("solana-mainnet-outbox-tx-*.json")):
        tx = load(path).get("result")
        if not tx:
            continue
        metas = account_metas(tx)
        hints = token_hints(tx)
        for ix_index, ix in enumerate(tx.get("transaction", {}).get("message", {}).get("instructions", [])):
            if ix.get("programId") != GUM_BANK_PROGRAM:
                continue
            raw = b58decode(ix.get("data") or "")
            name = bank_name_for(raw)
            accounts = ix.get("accounts") or []
            rows.append(
                {
                    "file": path.name,
                    "slot": tx.get("slot"),
                    "signature": (tx.get("transaction", {}).get("signatures") or [""])[0],
                    "instruction_index": ix_index,
                    "name": name or raw[:8].hex(),
                    "discriminator": raw[:8].hex(),
                    "raw_len": len(raw),
                    "accounts": [
                        {
                            "position": position,
                            "account": account,
                            "signer": metas.get(account, {}).get("signer", False),
                            "writable": metas.get(account, {}).get("writable", False),
                            "meta_index": metas.get(account, {}).get("index"),
                            "role": role_label(account, hints, gum_owned, authority, validators),
                            "hint": BANK_POSITION_HINTS.get(name, {}).get(position, ""),
                        }
                        for position, account in enumerate(accounts)
                    ],
                }
            )
    return rows


def position_summary(rows: list[dict], key_name: str) -> dict[tuple[str, int, int], dict]:
    summaries = {}
    for row in rows:
        group = row[key_name]
        key_prefix = (group, row["raw_len"])
        for account in row["accounts"]:
            key = (*key_prefix, account["position"])
            summary = summaries.setdefault(
                key,
                {
                    "count": 0,
                    "accounts": collections.Counter(),
                    "roles": collections.Counter(),
                    "hints": collections.Counter(),
                    "signer": 0,
                    "writable": 0,
                },
            )
            summary["count"] += 1
            summary["accounts"][account["account"]] += 1
            if account["role"]:
                summary["roles"][account["role"]] += 1
            if account["hint"]:
                summary["hints"][account["hint"]] += 1
            if account["signer"]:
                summary["signer"] += 1
            if account["writable"]:
                summary["writable"] += 1
    return summaries


def known_account_table(base: Path, gum_rows: list[dict], bank_rows_: list[dict]) -> collections.Counter[str]:
    counter = collections.Counter()
    for row in gum_rows + bank_rows_:
        for account in row["accounts"]:
            if account["role"] or account["hint"]:
                counter[f"{account['account']} => {account['role'] or account['hint']}"] += 1
    for row in verifier_payload_rows(base):
        if row.get("sender"):
            counter[f"{b58encode(row['sender'])} => verifier payload sender/program id"] += 1
    return counter


def security_hits(base: Path, gum_rows: list[dict], bank_rows_: list[dict]) -> tuple[int, int]:
    validators = validator_related_keys(base)
    jup_hits = 0
    validator_hits = 0
    for row in gum_rows + bank_rows_:
        for account in row["accounts"]:
            if account["account"] == JUP_MINT:
                jup_hits += 1
            if account["account"] in validators:
                validator_hits += 1
    return jup_hits, validator_hits


def print_position_summary(title: str, rows: list[dict], key_name: str, limit_groups: int | None = None) -> None:
    print(f"## {title}")
    print()
    grouped = collections.Counter((row[key_name], row["raw_len"]) for row in rows)
    print("| Variant | Raw len | Samples |")
    print("|---|---:|---:|")
    for (variant, raw_len), count in grouped.most_common():
        print(f"| `{variant}` | {raw_len} | {count} |")
    print()
    summaries = position_summary(rows, key_name)
    printed = 0
    for (variant, raw_len), _count in grouped.most_common():
        if limit_groups is not None and printed >= limit_groups:
            break
        printed += 1
        print(f"### `{variant}` raw len `{raw_len}`")
        print()
        print("| Pos | Signer | Writable | Common accounts | Role labels | Inferred role |")
        print("|---:|---:|---:|---|---|---|")
        for (_variant, _raw_len, position), summary in sorted(summaries.items()):
            if _variant != variant or _raw_len != raw_len:
                continue
            print(
                f"| {position} | {summary['signer']} | {summary['writable']} | "
                f"{fmt_counter(summary['accounts'], limit=4)} | {fmt_counter(summary['roles'], limit=4)} | "
                f"{fmt_counter(summary['hints'], limit=4)} |"
            )
        print()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot_dir")
    args = parser.parse_args()
    base = Path(args.snapshot_dir)

    gum_rows = direct_gum_rows(base)
    bank_rows_ = bank_rows(base)
    known = known_account_table(base, gum_rows, bank_rows_)
    jup_hits, validator_hits = security_hits(base, gum_rows, bank_rows_)
    verifier_senders = collections.Counter()
    for row in verifier_payload_rows(base):
        if row.get("sender"):
            verifier_senders[b58encode(row["sender"])] += 1

    print("# Gum Account Role Reconstruction")
    print()
    print("## Scope")
    print()
    print(f"- Direct JupNet Gum `brhPf...` instructions decoded: `{len(gum_rows)}`")
    print(f"- Direct Solana Bank instructions decoded: `{len(bank_rows_)}`")
    print(f"- Direct sampled top-level `GUMeb...` instructions: `0`")
    verifier_sender_text = ", ".join(f"{key}: {value}" for key, value in verifier_senders.most_common()) or "None"
    print(f"- Inner verifier payload sender/program ids: `{verifier_sender_text}`")
    print(f"- Account-meta canonical JUP hits: `{jup_hits}`")
    print(f"- Account-meta current validator/vote/stake hits: `{validator_hits}`")
    print()
    print("## High-Confidence Account Roles")
    print()
    print("| Account / role | Observations |")
    print("|---|---:|")
    for item, count in known.most_common(40):
        print(f"| `{item}` | {count} |")
    print()
    print_position_summary("Direct JupNet Gum Account Positions", gum_rows, "discriminator")
    print_position_summary("Solana Bank Account Positions", bank_rows_, "name", limit_groups=8)
    print("## Interpretation")
    print()
    print("- `GUMeb...` is not directly invoked in the saved transaction bodies; its role comes from decoded inner outbox verifier payloads, where it is the stable sender/program id.")
    print("- Direct `brhPf...` Gum samples are admin/authority-heavy and mostly touch Gum-owned config/state, Token-2022, system and associated-token surfaces.")
    print("- Direct Solana Bank samples split into asset movement (`withdraw`, `sweep`, RFQ variants) and proof verification (`verify_request`).")
    print("- Bank `verify_request` consistently uses the outbox root-history account and outbox helper program, matching the proof-chain model.")
    print("- The visible account-role surface still does not expose JUP staking, Dove signer weights, validator mappings, quorum state, slashing or rewards.")


if __name__ == "__main__":
    main()
