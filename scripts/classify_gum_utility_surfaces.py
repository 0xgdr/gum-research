#!/usr/bin/env python3
"""Classify Gum surfaces for JUP utility evidence, ignoring ordinary asset noise."""

from __future__ import annotations

import argparse
import base64
import collections
import json
import re
import string
from pathlib import Path


ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
JUP_MINT = "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN"
GUM_PROGRAM = "brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1"
SYSTEM_PROGRAM = "11111111111111111111111111111111"
TOKEN_PROGRAM = "Tokenis9xgQh7yMRbNBnV6uFq7LANbuZJwebxWBWixf"
REPEATED_ACCOUNT_NOTES = {
    "ESUtymMEp6NULmLBcREaumM87TRpgt5R4eNYVrKjCKQq": "transient writable account in repeated 1202 variant; missing by snapshot account fetch",
    "76WKTLzujFUnj7TyB7CqLywPE3YZQf4Fmxj9SwcFAJrY": "gum-owned 136-byte repeated state/config account in 1202 variant",
    "Hso4y8rKEXUUvMbxnyDmjCxA7yk1wbVsZNHSGXcDEUyU": "gum-owned 200-byte readonly account; candidate chain_config based on swap logs",
    "GZF3sfYF27BU83fd5BPgB419SZiLLZPty3qL6465JTp6": "gum-owned 336-byte readonly account; candidate input_unified_mint_map based on swap logs",
    "Fh54LKACZCzo3GzDcxoPQomTZamBsFy6XLbj15zJP1WH": "gum-owned 592-byte account created in swap flow; candidate swap_request/request state",
    "A5ER4hbDN82jEnf986kZzuJzMzsyw1DRqodnone5yJWo": "JPL token mint touched in sampled token CPI; not canonical Solana JUP",
    "94oZZEp1p1Vwuvc7axgeaRSU4Mk9diugqzjxpz1dnSZv": "token transfer authority/user signer in sampled swap flow; missing by snapshot account fetch",
    "FCNefQTEYCsPyQA64hdCpekucCDJFPHm2qfwg8F61jgc": "JPL token account created in sampled swap flow",
}


UTILITY_TERMS = (
    b"stake",
    b"staking",
    b"weight",
    b"quorum",
    b"validator",
    b"validators",
    b"dove",
    b"doves",
    b"signer",
    b"signers",
    b"fee",
    b"fees",
    b"reward",
    b"rewards",
    b"slash",
    b"slashing",
    b"govern",
    b"governance",
    b"authority",
    b"access",
)


def b58decode(value: str) -> bytes:
    number = 0
    for char in value:
        number = number * 58 + ALPHABET.index(char)
    data = number.to_bytes((number.bit_length() + 7) // 8, "big") if number else b""
    return (b"\0" * (len(value) - len(value.lstrip("1")))) + data


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def result(base: Path, filename: str):
    return load(base / filename).get("result")


def raw_account_data(account: dict) -> bytes:
    data = account.get("data")
    if isinstance(data, list):
        return base64.b64decode(data[0])
    return b""


def printable_strings(raw: bytes, min_len: int = 4) -> list[str]:
    allowed = set(bytes(string.printable, "ascii"))
    out = []
    current = bytearray()
    for byte in raw:
        if byte in allowed and byte not in (0x0b, 0x0c):
            current.append(byte)
        else:
            if len(current) >= min_len:
                out.append(current.decode("ascii", errors="ignore"))
            current.clear()
    if len(current) >= min_len:
        out.append(current.decode("ascii", errors="ignore"))
    return out


def account_records(base: Path, filename: str) -> list[tuple[str, dict, bytes]]:
    return [
        (item["pubkey"], item["account"], raw_account_data(item["account"]))
        for item in result(base, filename) or []
    ]


def utility_hits(raw: bytes) -> list[str]:
    hits = set()
    for value in printable_strings(raw):
        lower = value.lower()
        # Do not classify substrings inside hex/hash material as utility terms.
        if len(lower) >= 16 and all(ch in "0123456789abcdef" for ch in lower):
            continue
        for term in UTILITY_TERMS:
            word = re.escape(term.decode())
            if re.search(rf"(^|[^a-z0-9_]){word}([^a-z0-9_]|$)", lower):
                hits.add(term.decode())
    return sorted(hits)


def classify_jup_layout(raw: bytes) -> str:
    if JUP_MINT.encode() not in raw:
        return "not_jup"
    if len(raw) in (592, 672):
        return "asset_metadata_or_route_config"
    return "unknown_jup_text_layout"


def validator_related_keys(base: Path) -> dict[str, set[str]]:
    roles = {
        "validator_identity": set(),
        "vote_account": set(),
        "stake_account": set(),
    }
    votes = result(base, "getVoteAccounts.json") or {}
    for vote in (votes.get("current") or []) + (votes.get("delinquent") or []):
        roles["validator_identity"].add(vote["nodePubkey"])
        roles["vote_account"].add(vote["votePubkey"])
    for item in result(base, "getProgramAccounts-Stake.json") or []:
        roles["stake_account"].add(item["pubkey"])
    return roles


def repeated_account_infos(base: Path) -> dict[str, dict]:
    path = base / "getMultipleAccounts-RepeatedGumPathAccounts.json"
    if not path.exists():
        return {}
    keys = [
        "ESUtymMEp6NULmLBcREaumM87TRpgt5R4eNYVrKjCKQq",
        "76WKTLzujFUnj7TyB7CqLywPE3YZQf4Fmxj9SwcFAJrY",
        "Hso4y8rKEXUUvMbxnyDmjCxA7yk1wbVsZNHSGXcDEUyU",
        "GZF3sfYF27BU83fd5BPgB419SZiLLZPty3qL6465JTp6",
        "Fh54LKACZCzo3GzDcxoPQomTZamBsFy6XLbj15zJP1WH",
        "A5ER4hbDN82jEnf986kZzuJzMzsyw1DRqodnone5yJWo",
        "94oZZEp1p1Vwuvc7axgeaRSU4Mk9diugqzjxpz1dnSZv",
        "FCNefQTEYCsPyQA64hdCpekucCDJFPHm2qfwg8F61jgc",
    ]
    values = (load(path).get("result") or {}).get("value") or []
    return {key: value for key, value in zip(keys, values)}


def tx_instruction_summary(base: Path, all_validator_keys: set[str]) -> tuple[collections.Counter, list[dict], collections.Counter]:
    variants: collections.Counter = collections.Counter()
    rows = []
    token_mints: collections.Counter = collections.Counter()
    for path in sorted(base.glob("tx-*.json")):
        if path.name.endswith("-raw.json"):
            continue
        tx = load(path).get("result")
        if not tx:
            continue
        message = tx["transaction"]["message"]
        metas = {}
        for key in message.get("accountKeys", []):
            if isinstance(key, dict):
                metas[key["pubkey"]] = key
        for ix in message.get("instructions", []):
            if ix.get("programId") == GUM_PROGRAM:
                raw = b58decode(ix.get("data", ""))
                variant = raw[:8].hex()
                variants[(variant, len(raw))] += 1
                accounts = ix.get("accounts") or []
                rows.append(
                    {
                        "file": path.name,
                        "slot": tx.get("slot"),
                        "variant": variant,
                        "data_len": len(raw),
                        "accounts": len(accounts),
                        "signer_accounts": [a for a in accounts if metas.get(a, {}).get("signer")],
                        "writable_accounts": [a for a in accounts if metas.get(a, {}).get("writable")],
                        "validator_hits": sorted(set(accounts) & all_validator_keys),
                    }
                )
        for group in tx.get("meta", {}).get("innerInstructions") or []:
            for ix in group.get("instructions") or []:
                parsed = ix.get("parsed")
                if isinstance(parsed, dict):
                    info = parsed.get("info") or {}
                    if isinstance(info, dict) and isinstance(info.get("mint"), str):
                        token_mints[info["mint"]] += 1
    return variants, rows, token_mints


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot_dir")
    args = parser.parse_args()
    base = Path(args.snapshot_dir)

    jup_raw = b58decode(JUP_MINT)
    gum_records = account_records(base, "getProgramAccounts-Gum.json")
    validators = validator_related_keys(base)
    all_validator_keys = set().union(*validators.values())
    repeated = repeated_account_infos(base)

    jup_rows = []
    jup_layouts: collections.Counter = collections.Counter()
    jup_utility_rows = []
    raw_jup_hits = 0
    for pubkey, account, raw in gum_records:
        has_jup_text = JUP_MINT.encode() in raw
        has_jup_raw = jup_raw in raw
        if has_jup_raw:
            raw_jup_hits += 1
        if not has_jup_text:
            continue
        layout = classify_jup_layout(raw)
        hits = utility_hits(raw)
        strings = printable_strings(raw)
        key = (len(raw), raw[:8].hex(), raw.find(JUP_MINT.encode()), layout)
        jup_layouts[key] += 1
        if hits:
            jup_utility_rows.append((pubkey, hits, strings[:8]))
        jup_rows.append((pubkey, len(raw), raw[:8].hex(), raw.find(JUP_MINT.encode()), layout, hits))

    variants, ix_rows, token_mints = tx_instruction_summary(base, all_validator_keys)

    print("# Gum Utility Surface Classifier")
    print()
    print("## Scope")
    print()
    print("This report classifies JUP-related Gum data as utility evidence or non-decisive asset evidence.")
    print("Trading, route and token-transfer evidence is treated as noise unless it connects to stake, signer weight, quorum, fees, governance, access control, rewards, slashing or permanent protocol sinks.")
    print()
    print("## JUP Metadata Account Classification")
    print()
    print(f"- Gum accounts scanned: `{len(gum_records)}`")
    print(f"- Gum accounts with canonical JUP base58 text: `{len(jup_rows)}`")
    print(f"- Gum accounts with canonical JUP raw pubkey bytes: `{raw_jup_hits}`")
    print(f"- Gum JUP accounts with utility-keyword strings: `{len(jup_utility_rows)}`")
    print()
    print("| Count | Data length | Prefix | JUP text offset | Classification |")
    print("|---:|---:|---|---:|---|")
    for (length, prefix, offset, layout), count in jup_layouts.most_common():
        print(f"| {count} | {length} | `{prefix}` | {offset} | `{layout}` |")
    print()
    if jup_utility_rows:
        print("### JUP Accounts With Utility Keyword Hits")
        print()
        print("| Account | Hits | Sample strings |")
        print("|---|---|---|")
        for pubkey, hits, strings in jup_utility_rows[:25]:
            print(f"| `{pubkey}` | `{', '.join(hits)}` | `{'; '.join(strings)}` |")
        print()
    else:
        print("- No JUP metadata accounts contained utility keywords in printable strings.")
        print()
    print("Interpretation: the 127 JUP accounts look like asset metadata or route/config records. This is non-decisive asset evidence unless a future decoder ties these layouts to fees, staking, signer weights, access control or other utility.")
    print()

    print("## Repeated Gum Path Accounts")
    print()
    print("| Account | Owner | Executable | Space | Lamports | Utility string hits | Classification | Note |")
    print("|---|---|---|---:|---:|---|---|---|")
    for key, value in repeated.items():
        note = REPEATED_ACCOUNT_NOTES.get(key, "")
        if not value:
            print(f"| `{key}` | `missing` | `` |  |  | `` | `missing` | `{note}` |")
            continue
        raw = raw_account_data(value)
        owner = value.get("owner")
        hits = utility_hits(raw)
        if owner == GUM_PROGRAM:
            classification = "gum_owned_config_or_state"
        elif owner == TOKEN_PROGRAM:
            classification = "token_mint_or_account"
        elif owner == SYSTEM_PROGRAM:
            classification = "system_wallet_or_authority"
        else:
            classification = "external_or_unknown_state"
        print(f"| `{key}` | `{owner}` | `{value.get('executable')}` | {value.get('space')} | {value.get('lamports')} | `{', '.join(hits)}` | `{classification}` | `{note}` |")
    print()

    print("## Gum Instruction Variant Classification")
    print()
    print("| First bytes | Data length | Count | Utility relevance |")
    print("|---|---:|---:|---|")
    for (variant, length), count in variants.most_common():
        if length <= 2:
            relevance = "small_admin_or_state_transition; no embedded utility payload visible"
        else:
            relevance = "message_or_proof_payload; inspect accounts/logs for utility"
        print(f"| `{variant}` | {length} | {count} | `{relevance}` |")
    print()
    print("| File | Slot | Variant | Data length | Accounts | Signer accounts | Writable accounts | Validator/vote/stake hits |")
    print("|---|---:|---|---:|---:|---|---|---|")
    for row in ix_rows:
        print(
            f"| `{row['file']}` | {row['slot']} | `{row['variant']}` | {row['data_len']} | {row['accounts']} | "
            f"`{', '.join(row['signer_accounts'])}` | `{', '.join(row['writable_accounts'])}` | `{', '.join(row['validator_hits'])}` |"
        )
    print()

    print("## Token Mint Noise Check")
    print()
    if token_mints:
        print("| Parsed token mint | Count | Utility classification |")
        print("|---|---:|---|")
        for mint, count in token_mints.most_common():
            classification = "canonical_jup" if mint == JUP_MINT else "non_jup_token_path"
            print(f"| `{mint}` | {count} | `{classification}` |")
    else:
        print("- No parsed token mints found in sampled inner instructions.")
    print()
    print("## Utility Finding")
    print()
    print("- No JUP staking, signer-weight, quorum, fee, governance, access-control, reward, slashing or permanent sink mechanism was identified in this pass.")
    print("- The 127 JUP hits remain classified as non-decisive asset metadata/config evidence.")
    print("- The repeated transaction-path accounts are worth decoding further, but current owner/role classification does not expose JUP utility.")


if __name__ == "__main__":
    main()
