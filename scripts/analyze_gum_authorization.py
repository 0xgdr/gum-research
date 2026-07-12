#!/usr/bin/env python3
"""Analyze Gum transaction authorization surfaces from a saved JupNet snapshot."""

from __future__ import annotations

import argparse
import collections
import json
import struct
import base64
from pathlib import Path


ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
GUM_PROGRAM = "brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1"
SYSTEM_PROGRAM = "11111111111111111111111111111111"
COMPUTE_BUDGET = "ComputeBudget111111111111111111111111111111"
ASSOCIATED_TOKEN = "ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL"


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
    data = account.get("data")
    if isinstance(data, list):
        return base64.b64decode(data[0])
    return b""


def gum_owned_accounts(base: Path) -> set[str]:
    return {item["pubkey"] for item in result(base, "getProgramAccounts-Gum.json") or []}


def token_mints_from_instruction(ix: dict) -> list[str]:
    parsed = ix.get("parsed")
    if not isinstance(parsed, dict):
        return []
    info = parsed.get("info") or {}
    mints = []
    if isinstance(info, dict):
        mint = info.get("mint")
        if isinstance(mint, str):
            mints.append(mint)
        token_amount = info.get("tokenAmount")
        if isinstance(token_amount, dict) and isinstance(token_amount.get("mint"), str):
            mints.append(token_amount["mint"])
    return mints


def parse_programdata_authority(base: Path) -> str | None:
    data = result(base, "getAccountInfo-GumProgramData-slice48.json")
    if not data or not data.get("value"):
        return None
    raw = raw_account_data(data["value"])
    if len(raw) < 45 or struct.unpack("<I", raw[:4])[0] != 3 or raw[12] != 1:
        return None
    return b58encode(raw[13:45])


def validator_key_sets(base: Path) -> dict[str, set[str]]:
    nodes = set()
    vote_accounts = set()
    stake_accounts = set()
    votes = result(base, "getVoteAccounts.json") or {}
    for vote in (votes.get("current") or []) + (votes.get("delinquent") or []):
        nodes.add(vote["nodePubkey"])
        vote_accounts.add(vote["votePubkey"])
    for account in result(base, "getProgramAccounts-Stake.json") or []:
        stake_accounts.add(account["pubkey"])
    return {
        "validator_identity": nodes,
        "vote_account": vote_accounts,
        "stake_account": stake_accounts,
    }


def role_for(pubkey: str, authority: str | None, gum_owned: set[str], validators: dict[str, set[str]]) -> str:
    roles = []
    if pubkey == authority:
        roles.append("gum_upgrade_authority")
    if pubkey == GUM_PROGRAM:
        roles.append("gum_program")
    if pubkey == SYSTEM_PROGRAM:
        roles.append("system_program")
    if pubkey == COMPUTE_BUDGET:
        roles.append("compute_budget")
    if pubkey == ASSOCIATED_TOKEN:
        roles.append("associated_token_program")
    if pubkey in gum_owned:
        roles.append("gum_owned_account")
    for name, keys in validators.items():
        if pubkey in keys:
            roles.append(name)
    return ",".join(roles)


def tx_files(base: Path) -> list[Path]:
    return [
        path
        for path in sorted(base.glob("tx-*.json"))
        if not path.name.endswith("-raw.json")
    ]


def account_meta(message: dict) -> dict[str, dict]:
    metas = {}
    for key in message.get("accountKeys", []):
        if isinstance(key, dict):
            metas[key["pubkey"]] = {
                "signer": bool(key.get("signer")),
                "writable": bool(key.get("writable")),
                "source": key.get("source"),
            }
        elif isinstance(key, str):
            metas[key] = {"signer": False, "writable": False, "source": "unknown"}
    return metas


def instruction_program_id(ix: dict) -> str | None:
    return ix.get("programId")


def gum_instructions(message: dict) -> list[tuple[int, dict]]:
    return [
        (index, ix)
        for index, ix in enumerate(message.get("instructions", []))
        if instruction_program_id(ix) == GUM_PROGRAM
    ]


def inner_instructions(meta: dict) -> list[dict]:
    out = []
    for group in meta.get("innerInstructions") or []:
        for ix in group.get("instructions") or []:
            out.append(ix)
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot_dir")
    args = parser.parse_args()
    base = Path(args.snapshot_dir)

    authority = parse_programdata_authority(base)
    gum_owned = gum_owned_accounts(base)
    validators = validator_key_sets(base)
    all_validator_keys = set().union(*validators.values())

    signer_counts: collections.Counter[str] = collections.Counter()
    writable_counts: collections.Counter[str] = collections.Counter()
    account_counts: collections.Counter[str] = collections.Counter()
    program_counts: collections.Counter[str] = collections.Counter()
    discriminator_counts: collections.Counter[str] = collections.Counter()
    data_len_counts: collections.Counter[int] = collections.Counter()
    token_mints: collections.Counter[str] = collections.Counter()
    gum_account_role_counts: collections.Counter[str] = collections.Counter()
    tx_rows = []

    for path in tx_files(base):
        data = load(path)
        tx = data.get("result")
        if not tx:
            continue
        message = tx["transaction"]["message"]
        meta = tx.get("meta") or {}
        metas = account_meta(message)
        tx_signers = [key for key, value in metas.items() if value["signer"]]
        tx_writable = [key for key, value in metas.items() if value["writable"]]
        for signer in tx_signers:
            signer_counts[signer] += 1
        for writable in tx_writable:
            writable_counts[writable] += 1
        for key in metas:
            account_counts[key] += 1

        top_programs = []
        for ix in message.get("instructions", []):
            program_id = instruction_program_id(ix)
            if program_id:
                top_programs.append(program_id)
                program_counts[program_id] += 1
            for mint in token_mints_from_instruction(ix):
                token_mints[mint] += 1

        inner_programs = []
        for ix in inner_instructions(meta):
            program_id = instruction_program_id(ix)
            if program_id:
                inner_programs.append(program_id)
                program_counts[program_id] += 1
            for mint in token_mints_from_instruction(ix):
                token_mints[mint] += 1

        gum_ix_rows = []
        for index, ix in gum_instructions(message):
            raw = b58decode(ix.get("data", ""))
            discriminator = raw[:8].hex()
            discriminator_counts[discriminator] += 1
            data_len_counts[len(raw)] += 1
            accounts = ix.get("accounts") or []
            account_roles = []
            for account in accounts:
                role = role_for(account, authority, gum_owned, validators)
                if role:
                    gum_account_role_counts[role] += 1
                account_roles.append(
                    {
                        "account": account,
                        "signer": metas.get(account, {}).get("signer", False),
                        "writable": metas.get(account, {}).get("writable", False),
                        "role": role,
                    }
                )
            gum_ix_rows.append((index, len(raw), discriminator, account_roles))

        validator_hits = sorted(set(metas) & all_validator_keys)
        tx_rows.append(
            {
                "file": path.name,
                "slot": tx.get("slot"),
                "signers": tx_signers,
                "writable_count": len(tx_writable),
                "top_programs": top_programs,
                "inner_programs": inner_programs,
                "validator_hits": validator_hits,
                "gum_ix_rows": gum_ix_rows,
            }
        )

    print("# Gum Authorization Analysis")
    print()
    print("## Summary")
    print()
    print(f"- Gum upgrade authority: `{authority}`")
    print(f"- Parsed Gum transaction files analyzed: `{len(tx_rows)}`")
    print(f"- Unique signers: `{len(signer_counts)}`")
    print(f"- Unique writable accounts: `{len(writable_counts)}`")
    print(f"- Unique transaction accounts: `{len(account_counts)}`")
    print(f"- Validator/vote/stake account hits across transactions: `{sum(len(row['validator_hits']) for row in tx_rows)}`")
    print()
    print("## Signers")
    print()
    print("| Signer | Count | Role |")
    print("|---|---:|---|")
    for signer, count in signer_counts.most_common():
        print(f"| `{signer}` | {count} | `{role_for(signer, authority, gum_owned, validators)}` |")
    print()
    print("## Gum Instruction Data")
    print()
    print("| First 8 bytes | Count |")
    print("|---|---:|")
    for discriminator, count in discriminator_counts.most_common():
        print(f"| `{discriminator}` | {count} |")
    print()
    print("| Data length | Count |")
    print("|---:|---:|")
    for length, count in data_len_counts.most_common():
        print(f"| {length} | {count} |")
    print()
    print("## Invoked Programs")
    print()
    print("| Program | Count |")
    print("|---|---:|")
    for program, count in program_counts.most_common():
        print(f"| `{program}` | {count} |")
    print()
    print("## Token Mints Touched")
    print()
    if token_mints:
        print("| Mint | Count |")
        print("|---|---:|")
        for mint, count in token_mints.most_common():
            print(f"| `{mint}` | {count} |")
    else:
        print("- No parsed token mints found.")
    print()
    print("## Repeated Writable Accounts")
    print()
    print("| Account | Writable tx count | Role |")
    print("|---|---:|---|")
    for account, count in writable_counts.most_common(25):
        print(f"| `{account}` | {count} | `{role_for(account, authority, gum_owned, validators)}` |")
    print()
    print("## Per-Transaction Authorization Surface")
    print()
    print("| File | Slot | Signers | Writable accounts | Top-level programs | Inner programs | Validator/vote/stake hits |")
    print("|---|---:|---|---:|---|---|---|")
    for row in tx_rows:
        print(
            "| "
            + " | ".join(
                [
                    f"`{row['file']}`",
                    str(row["slot"]),
                    f"`{', '.join(row['signers'])}`",
                    str(row["writable_count"]),
                    f"`{', '.join(row['top_programs'])}`",
                    f"`{', '.join(row['inner_programs'])}`",
                    f"`{', '.join(row['validator_hits'])}`",
                ]
            )
            + " |"
        )
    print()
    print("## Gum Instruction Accounts")
    print()
    for row in tx_rows:
        print(f"### `{row['file']}`")
        print()
        if not row["gum_ix_rows"]:
            print("- No Gum instruction found.")
            print()
            continue
        for index, length, discriminator, accounts in row["gum_ix_rows"]:
            print(f"- Instruction index: `{index}`")
            print(f"- Data length: `{length}`")
            print(f"- First 8 bytes: `{discriminator}`")
            print()
            print("| Position | Account | Signer | Writable | Role |")
            print("|---:|---|---|---|---|")
            for position, account in enumerate(accounts):
                print(
                    f"| {position} | `{account['account']}` | `{account['signer']}` | "
                    f"`{account['writable']}` | `{account['role']}` |"
                )
            print()
    print("## Interpretation")
    print()
    print("- The sampled Gum transactions are enough to identify the public authorization surface for those flows, but not enough to prove every Gum instruction variant.")
    print("- If validator or Dove security is enforced privately or through hashed/encrypted state, this transaction-level scan will not expose it directly.")
    print("- Public evidence for validator/Dove participation would become stronger if validator, vote, stake, signer-set, quorum, or weight accounts appeared in these account lists or verifier/config account layouts.")


if __name__ == "__main__":
    main()
