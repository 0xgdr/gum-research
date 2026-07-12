#!/usr/bin/env python3
"""Analyze a saved JupNet validator-security snapshot."""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import json
from pathlib import Path


ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
JUP_MINT = "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN"
GUM_BANK = "bk1PDAkbHEBGtVRiM94Lzets8gVFP7FgySyfkAc8MPN"
GUM_BANK_PROGRAM = "BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ"


def b58decode(value: str) -> bytes:
    number = 0
    for char in value:
        number = number * 58 + ALPHABET.index(char)
    data = number.to_bytes((number.bit_length() + 7) // 8, "big") if number else b""
    return (b"\0" * (len(value) - len(value.lstrip("1")))) + data


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def result(base: Path, filename: str):
    path = base / filename
    if not path.exists():
        return None
    return load(path).get("result")


def account_bytes(account_data) -> bytes:
    if isinstance(account_data, list):
        return base64.b64decode(account_data[0])
    if isinstance(account_data, dict) and "parsed" in account_data:
        return json.dumps(account_data["parsed"], sort_keys=True).encode()
    return b""


def account_value(base: Path, filename: str) -> dict | None:
    data = result(base, filename)
    if not data:
        return None
    return data.get("value")


def account_summary(value: dict | None) -> str:
    if not value:
        return "not present"
    return (
        f"present; owner `{value.get('owner')}`; executable `{value.get('executable')}`; "
        f"lamports `{value.get('lamports')}`; space `{value.get('space')}`"
    )


def account_records(base: Path, filename: str) -> list[tuple[str, bytes]]:
    records = []
    for item in result(base, filename) or []:
        records.append((item["pubkey"], account_bytes(item["account"]["data"])))
    return records


def scan(records: list[tuple[str, bytes]], targets: list[tuple[str, str, bytes]]) -> dict:
    hits: dict[str, list[str]] = {name: [] for name, _, _ in targets}
    for pubkey, raw in records:
        for name, text, raw_key in targets:
            if raw_key in raw or text.encode() in raw:
                hits[name].append(pubkey)
    return hits


def scan_exact(records: list[tuple[str, bytes]], target: bytes) -> list[str]:
    return [pubkey for pubkey, raw in records if target in raw]


def block_time(value: int | None) -> str:
    if not value:
        return "unknown"
    return dt.datetime.fromtimestamp(value, dt.timezone.utc).isoformat()


def signature_set(base: Path, filename: str) -> set[str]:
    return {item["signature"] for item in result(base, filename) or []}


def tx_account_keys(tx: dict) -> set[str]:
    keys = set()
    for key in tx.get("transaction", {}).get("message", {}).get("accountKeys", []):
        if isinstance(key, dict):
            keys.add(key["pubkey"])
        elif isinstance(key, str):
            keys.add(key)
    return keys


def sampled_tx_rows(base: Path, prefix: str, validator_related: set[str]) -> list[dict]:
    rows = []
    for path in sorted(base.glob(f"{prefix}-tx-*.json")):
        tx = load(path).get("result")
        if not tx:
            continue
        keys = tx_account_keys(tx)
        logs = tx.get("meta", {}).get("logMessages") or []
        terms = ("jup", "stake", "signer", "quorum", "proof", "hash", "fee", "lock", "burn", "dove", "vote", "validator")
        interesting = [line for line in logs if any(term in line.lower() for term in terms)]
        rows.append(
            {
                "file": path.name,
                "slot": tx.get("slot"),
                "jup_account_hit": JUP_MINT in keys,
                "validator_hits": sorted(keys & validator_related),
                "interesting_logs": interesting,
            }
        )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot_dir")
    args = parser.parse_args()
    base = Path(args.snapshot_dir)

    slot = result(base, "getSlot.json")
    identity = result(base, "getIdentity.json") or {}
    epoch_info = result(base, "getEpochInfo.json") or {}
    cluster = result(base, "getClusterNodes.json") or []
    votes = result(base, "getVoteAccounts.json") or {}
    current_votes = votes.get("current") or []
    delinquent_votes = votes.get("delinquent") or []
    stake_accounts = result(base, "getProgramAccounts-Stake.json") or []
    gum_accounts = account_records(base, "getProgramAccounts-Gum.json")
    openid_accounts = account_records(base, "getProgramAccounts-OpenIDRegistry.json")
    native_loader_accounts = account_records(base, "getProgramAccounts-NativeLoader.json")
    jup_info = result(base, "getAccountInfo-JUPMint.json") or {}
    jup_token_accounts = result(base, "getProgramAccounts-Token-JUPMint.json") or []
    bank_info = account_value(base, "getAccountInfo-GumBank.json")
    bank_program_info = account_value(base, "getAccountInfo-GumBankProgram.json")
    bank_program_accounts = result(base, "getProgramAccounts-GumBankProgram.json") or []
    if not isinstance(bank_program_accounts, list):
        bank_program_accounts = []

    key_targets = []
    for vote in current_votes + delinquent_votes:
        key_targets.append((f"node:{vote['nodePubkey']}", vote["nodePubkey"], b58decode(vote["nodePubkey"])))
        key_targets.append((f"vote:{vote['votePubkey']}", vote["votePubkey"], b58decode(vote["votePubkey"])))
    for account in stake_accounts:
        key_targets.append((f"stake:{account['pubkey']}", account["pubkey"], b58decode(account["pubkey"])))
    validator_related = {
        text
        for name, text, _raw_key in key_targets
        if name.startswith(("node:", "vote:", "stake:"))
    }

    jup_raw = b58decode(JUP_MINT)
    gum_jup_raw_hits = scan_exact(gum_accounts, jup_raw)
    gum_jup_text_hits = scan_exact(gum_accounts, JUP_MINT.encode())
    gum_jup_symbol_hits = scan_exact(gum_accounts, b"JUP")
    openid_jup_raw_hits = scan_exact(openid_accounts, jup_raw)
    openid_jup_text_hits = scan_exact(openid_accounts, JUP_MINT.encode())
    native_jup_raw_hits = scan_exact(native_loader_accounts, jup_raw)
    native_jup_text_hits = scan_exact(native_loader_accounts, JUP_MINT.encode())
    gum_key_hits = {k: v for k, v in scan(gum_accounts, key_targets).items() if v}
    openid_key_hits = {k: v for k, v in scan(openid_accounts, key_targets).items() if v}

    stake_rows = []
    for account in stake_accounts:
        parsed = account["account"]["data"]["parsed"]["info"]
        delegation = parsed["stake"]["delegation"]
        authorized = parsed["meta"]["authorized"]
        stake_rows.append(
            (
                account["pubkey"],
                authorized["staker"],
                authorized["withdrawer"],
                delegation["voter"],
                delegation["stake"],
                delegation["activationEpoch"],
            )
        )

    gum_signatures = signature_set(base, "getSignaturesForAddress-Gum.json")
    bank_signatures = signature_set(base, "getSignaturesForAddress-GumBank.json")
    bank_program_signatures = signature_set(base, "getSignaturesForAddress-GumBankProgram.json")
    bank_program_tx_rows = sampled_tx_rows(base, "bank", validator_related)

    print("# Validator Security Snapshot Analysis")
    print()
    print(f"- Snapshot slot: `{slot}`")
    print(f"- RPC identity: `{identity.get('identity', 'unknown')}`")
    print(f"- Epoch: `{epoch_info.get('epoch', 'unknown')}`")
    print(f"- Cluster nodes: `{len(cluster)}`")
    print(f"- Current vote accounts: `{len(current_votes)}`")
    print(f"- Delinquent vote accounts: `{len(delinquent_votes)}`")
    print(f"- Stake-program accounts: `{len(stake_accounts)}`")
    print(f"- Gum-owned accounts scanned: `{len(gum_accounts)}`")
    print(f"- OpenID-owned accounts scanned: `{len(openid_accounts)}`")
    print(f"- NativeLoader-owned accounts scanned: `{len(native_loader_accounts)}`")
    print()
    print("## Public Registry Bank Lead")
    print()
    print(f"- Registry Bank account: `{GUM_BANK}`")
    print(f"- Registry Bank Program: `{GUM_BANK_PROGRAM}`")
    print(f"- Bank account on configured RPC: {account_summary(bank_info)}")
    print(f"- Bank Program on configured RPC: {account_summary(bank_program_info)}")
    print(f"- Bank Program-owned accounts scanned: `{len(bank_program_accounts)}`")
    print(f"- Recent Bank signatures in window: `{len(bank_signatures)}`")
    print(f"- Recent Bank Program signatures in window: `{len(bank_program_signatures)}`")
    print(f"- Gum/Bank signature overlap in windows: `{len(gum_signatures & bank_signatures)}`")
    print(f"- Gum/Bank Program signature overlap in windows: `{len(gum_signatures & bank_program_signatures)}`")
    print()
    print("## JUP Surface")
    print()
    print(f"- Canonical JUP mint account on JupNet: `{'present' if jup_info.get('value') else 'not present'}`")
    print(f"- SPL token accounts with canonical JUP mint on JupNet: `{len(jup_token_accounts)}`")
    print(f"- Gum accounts containing canonical JUP raw pubkey bytes: `{len(gum_jup_raw_hits)}`")
    print(f"- Gum accounts containing canonical JUP base58 text: `{len(gum_jup_text_hits)}`")
    print(f"- Gum accounts containing `JUP` symbol text: `{len(gum_jup_symbol_hits)}`")
    print(f"- OpenID accounts containing canonical JUP raw pubkey bytes: `{len(openid_jup_raw_hits)}`")
    print(f"- OpenID accounts containing canonical JUP base58 text: `{len(openid_jup_text_hits)}`")
    print(f"- NativeLoader accounts containing canonical JUP raw pubkey bytes: `{len(native_jup_raw_hits)}`")
    print(f"- NativeLoader accounts containing canonical JUP base58 text: `{len(native_jup_text_hits)}`")
    if gum_jup_text_hits:
        print(f"- First Gum JUP text-hit accounts: `{', '.join(gum_jup_text_hits[:10])}`")
    print()
    print("## Validator Key Correlation")
    print()
    print(f"- Gum accounts containing current validator/vote/stake keys: `{sum(len(v) for v in gum_key_hits.values())}`")
    print(f"- OpenID accounts containing current validator/vote/stake keys: `{sum(len(v) for v in openid_key_hits.values())}`")
    print()
    print("## Native Stake Rows")
    print()
    print("| Stake account | Staker | Withdrawer | Vote account | Delegated native stake | Activation epoch |")
    print("|---|---|---|---|---:|---:|")
    for row in stake_rows:
        print("| " + " | ".join(row) + " |")
    print()
    print("## Recent Gum Signatures")
    print()
    print("| Slot | Block time UTC | Error | Signature prefix |")
    print("|---:|---|---|---|")
    for item in result(base, "getSignaturesForAddress-Gum.json") or []:
        print(f"| {item.get('slot')} | {block_time(item.get('blockTime'))} | `{item.get('err')}` | `{item['signature'][:16]}` |")
    print()
    print("## Recent Bank Program Signatures")
    print()
    print("| Slot | Block time UTC | Error | Signature prefix |")
    print("|---:|---|---|---|")
    for item in result(base, "getSignaturesForAddress-GumBankProgram.json") or []:
        print(f"| {item.get('slot')} | {block_time(item.get('blockTime'))} | `{item.get('err')}` | `{item['signature'][:16]}` |")
    print()
    print("## Sample Bank Program Transaction Logs")
    print()
    if bank_program_tx_rows:
        for row in bank_program_tx_rows:
            print(f"### `{row['file']}`")
            print()
            print(f"- Slot: `{row['slot']}`")
            print(f"- Canonical JUP account key hit: `{row['jup_account_hit']}`")
            print(f"- Validator/vote/stake account-key hits: `{len(row['validator_hits'])}`")
            print(f"- Matching log lines: `{len(row['interesting_logs'])}`")
            for line in row["interesting_logs"][:8]:
                print(f"- `{line}`")
            print()
    else:
        print("No sampled Bank Program transactions were available in this snapshot.")
        print()
    print("## Sample Gum Transaction Logs")
    print()
    terms = ("jup", "stake", "signer", "quorum", "fault", "proof", "hash", "claim", "mint", "burn", "dove", "vote")
    for path in sorted(base.glob("tx-*.json")):
        if path.name.endswith("-raw.json"):
            continue
        data = load(path)
        tx = data.get("result")
        if not tx:
            continue
        logs = tx.get("meta", {}).get("logMessages") or []
        interesting = [line for line in logs if any(term in line.lower() for term in terms)]
        print(f"### `{path.name}`")
        print()
        print(f"- Slot: `{tx.get('slot')}`")
        print(f"- Matching log lines: `{len(interesting)}`")
        for line in interesting[:8]:
            print(f"- `{line}`")
        print()


if __name__ == "__main__":
    main()
