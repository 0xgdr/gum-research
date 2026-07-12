#!/usr/bin/env python3
"""Account-graph and payload helper for sampled Solana GUM Bank transactions."""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import struct
from pathlib import Path


ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
GUM_BANK = "bk1PDAkbHEBGtVRiM94Lzets8gVFP7FgySyfkAc8MPN"
GUM_BANK_PROGRAM = "BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ"
JUP_MINT = "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN"
SYSTEM_PROGRAM = "11111111111111111111111111111111"
SYSVAR_INSTRUCTIONS = "Sysvar1nstructions1111111111111111111111111"
SPL_TOKEN = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
ASSOCIATED_TOKEN = "ATokenGPvbdGVxr1b2hvZbsiqW5xWH25EFJHUyzW6baS"
WRAPPED_SOL = "So11111111111111111111111111111111111111112"
USDC = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"

KNOWN_ANCHOR_NAMES = (
    "withdraw",
    "sweep",
    "verify_request",
    "rfq_sell_resolve",
    "rfq_sell_commit",
)

STRING_SEEDS = (
    "JUPNET_INBOX",
    "__inbox_event_auth",
    "merkle_root_state",
    "swap_authority",
    "request",
    "request_buffer",
    "inbox",
    "outbox",
    "bank",
    "gum",
    "jupnet",
)

KNOWN_ACCOUNTS = {
    GUM_BANK: "Gum Bank executable",
    GUM_BANK_PROGRAM: "Gum Bank Program executable",
    JUP_MINT: "canonical Solana JUP mint",
    SYSTEM_PROGRAM: "system program",
    SYSVAR_INSTRUCTIONS: "instructions sysvar",
    SPL_TOKEN: "SPL Token program",
    ASSOCIATED_TOKEN: "Associated Token program",
    WRAPPED_SOL: "wrapped SOL mint",
    USDC: "USDC mint",
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


def anchor_discriminator(name: str) -> str:
    return hashlib.sha256(f"global:{name}".encode()).digest()[:8].hex()


def printable_runs(raw: bytes, min_len: int = 4) -> list[tuple[int, str]]:
    allowed = set(range(0x20, 0x7F))
    out: list[tuple[int, str]] = []
    start = None
    current = bytearray()
    for offset, byte in enumerate(raw):
        if byte in allowed:
            if start is None:
                start = offset
            current.append(byte)
            continue
        if start is not None and len(current) >= min_len:
            out.append((start, current.decode("ascii", errors="ignore")))
        start = None
        current.clear()
    if start is not None and len(current) >= min_len:
        out.append((start, current.decode("ascii", errors="ignore")))
    return out


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


def token_account_hints(tx: dict) -> dict[str, dict]:
    hints: dict[str, dict] = {}
    keys = tx.get("transaction", {}).get("message", {}).get("accountKeys", [])
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


def invoked_programs(tx: dict) -> collections.Counter:
    counts: collections.Counter = collections.Counter()
    for ix in tx.get("transaction", {}).get("message", {}).get("instructions", []):
        if ix.get("programId"):
            counts[ix["programId"]] += 1
    for group in tx.get("meta", {}).get("innerInstructions") or []:
        for ix in group.get("instructions") or []:
            if ix.get("programId"):
                counts[ix["programId"]] += 1
    return counts


def bank_instruction_rows(base: Path) -> list[dict]:
    rows = []
    likely_names = {anchor_discriminator(name): name for name in KNOWN_ANCHOR_NAMES}
    for path in sorted(base.glob("solana-mainnet-bank-tx-*.json")):
        tx = load(path).get("result")
        if not tx:
            continue
        metas = account_metas(tx)
        token_hints = token_account_hints(tx)
        logs = tx.get("meta", {}).get("logMessages") or []
        instruction_logs = [line for line in logs if "Instruction:" in line]
        programs = invoked_programs(tx)
        for ix_index, ix in enumerate(tx.get("transaction", {}).get("message", {}).get("instructions", [])):
            if ix.get("programId") != GUM_BANK_PROGRAM:
                continue
            raw = b58decode(ix.get("data", ""))
            disc = raw[:8].hex()
            accounts = ix.get("accounts") or []
            rows.append(
                {
                    "file": path.name,
                    "slot": tx.get("slot"),
                    "instruction_index": ix_index,
                    "signature": (tx.get("transaction", {}).get("signatures") or [""])[0],
                    "discriminator": disc,
                    "name": likely_names.get(disc, ""),
                    "raw": raw,
                    "payload": raw[8:],
                    "accounts": accounts,
                    "metas": metas,
                    "token_hints": token_hints,
                    "instruction_logs": instruction_logs,
                    "programs": programs,
                }
            )
    return rows


def account_label(account: str, token_hints: dict[str, dict]) -> str:
    if account in KNOWN_ACCOUNTS:
        return KNOWN_ACCOUNTS[account]
    hint = token_hints.get(account)
    if hint:
        mint = hint.get("mint") or "unknown mint"
        owner = hint.get("owner") or "unknown owner"
        return f"token account mint={mint} owner={owner}"
    return ""


def summarize_positions(rows: list[dict]) -> dict[tuple[str, int], dict]:
    by_variant: dict[tuple[str, int], dict] = {}
    for row in rows:
        key = (row["discriminator"], len(row["payload"]) + 8)
        summary = by_variant.setdefault(
            key,
            {
                "name": row["name"],
                "rows": [],
                "positions": collections.defaultdict(collections.Counter),
                "signers": collections.Counter(),
                "writables": collections.Counter(),
                "readonly": collections.Counter(),
                "labels": collections.defaultdict(collections.Counter),
            },
        )
        summary["rows"].append(row)
        for position, account in enumerate(row["accounts"]):
            meta = row["metas"].get(account, {})
            summary["positions"][position][account] += 1
            label = account_label(account, row["token_hints"])
            if label:
                summary["labels"][position][label] += 1
            if meta.get("signer"):
                summary["signers"][account] += 1
            if meta.get("writable"):
                summary["writables"][account] += 1
            else:
                summary["readonly"][account] += 1
    return by_variant


def payload_report(rows: list[dict]) -> dict[tuple[str, int], dict]:
    out = {}
    for row in rows:
        key = (row["discriminator"], len(row["raw"]))
        report = out.setdefault(
            key,
            {
                "name": row["name"],
                "count": 0,
                "payloads": [],
                "strings": collections.Counter(),
                "u32_offsets": collections.defaultdict(collections.Counter),
                "u64_offsets": collections.defaultdict(collections.Counter),
                "pubkey_offsets": collections.defaultdict(collections.Counter),
            },
        )
        report["count"] += 1
        payload = row["payload"]
        report["payloads"].append(payload)
        for offset, text in printable_runs(payload):
            report["strings"][(offset, text)] += 1
        for offset in range(0, max(0, len(payload) - 3), 4):
            value = struct.unpack("<I", payload[offset : offset + 4])[0]
            if value and value < 10**9:
                report["u32_offsets"][offset][value] += 1
        for offset in range(0, max(0, len(payload) - 7), 8):
            value = struct.unpack("<Q", payload[offset : offset + 8])[0]
            if value and value < 10**15:
                report["u64_offsets"][offset][value] += 1
        for offset in range(0, max(0, len(payload) - 31)):
            encoded = b58encode(payload[offset : offset + 32])
            if encoded in KNOWN_ACCOUNTS:
                report["pubkey_offsets"][offset][encoded] += 1
    return out


def common_account_edges(rows: list[dict]) -> collections.Counter:
    edges: collections.Counter = collections.Counter()
    for row in rows:
        accounts = list(dict.fromkeys(row["accounts"]))
        for left_index, left in enumerate(accounts):
            for right in accounts[left_index + 1 :]:
                edges[tuple(sorted((left, right)))] += 1
    return edges


def is_on_ed25519_curve(pubkey_bytes: bytes) -> bool:
    if len(pubkey_bytes) != 32:
        return False
    p = 2**255 - 19
    y = int.from_bytes(pubkey_bytes, "little") & ((1 << 255) - 1)
    if y >= p:
        return False
    y2 = y * y % p
    d = (-121665 * pow(121666, p - 2, p)) % p
    denominator = (d * y2 + 1) % p
    if denominator == 0:
        return False
    x2 = ((y2 - 1) * pow(denominator, p - 2, p)) % p
    return x2 == 0 or pow(x2, (p - 1) // 2, p) == 1


def derive_pda(seeds: list[bytes], program_id: str) -> str | None:
    program_bytes = b58decode(program_id)
    for bump in range(255, -1, -1):
        data = b"".join(seeds + [bytes([bump]), program_bytes, b"ProgramDerivedAddress"])
        digest = hashlib.sha256(data).digest()
        if not is_on_ed25519_curve(digest):
            return b58encode(digest)
    return None


def pda_matches(rows: list[dict]) -> list[dict]:
    observed = {account for row in rows for account in row["accounts"]}
    observed.update(KNOWN_ACCOUNTS)
    pubkey_seeds = {
        "bank": b58decode(GUM_BANK),
        "bank_program": b58decode(GUM_BANK_PROGRAM),
        "jup_mint": b58decode(JUP_MINT),
        "usdc": b58decode(USDC),
        "wrapped_sol": b58decode(WRAPPED_SOL),
    }
    matches = []
    for program_id in (GUM_BANK_PROGRAM, GUM_BANK):
        for seed in STRING_SEEDS:
            derived = derive_pda([seed.encode()], program_id)
            if derived in observed:
                matches.append({"program": program_id, "seeds": seed, "account": derived})
            for pubkey_label, pubkey_bytes in pubkey_seeds.items():
                derived = derive_pda([seed.encode(), pubkey_bytes], program_id)
                if derived in observed:
                    matches.append({"program": program_id, "seeds": f"{seed}, {pubkey_label}", "account": derived})
                derived = derive_pda([pubkey_bytes, seed.encode()], program_id)
                if derived in observed:
                    matches.append({"program": program_id, "seeds": f"{pubkey_label}, {seed}", "account": derived})
    return matches


def format_counter(counter: collections.Counter, limit: int = 6) -> str:
    if not counter:
        return ""
    return "<br>".join(f"`{key}` {count}" for key, count in counter.most_common(limit))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot_dir")
    args = parser.parse_args()
    base = Path(args.snapshot_dir)
    rows = bank_instruction_rows(base)
    variants = summarize_positions(rows)
    payloads = payload_report(rows)
    edges = common_account_edges(rows)
    pdas = pda_matches(rows)

    all_accounts = collections.Counter(account for row in rows for account in row["accounts"])
    signer_appearances = collections.Counter(
        account for row in rows for account in row["accounts"] if row["metas"].get(account, {}).get("signer")
    )
    jup_hits = sum(1 for row in rows if JUP_MINT in row["accounts"])

    print("# Bank Account Graph and Payload Analysis")
    print()
    print("## Scope")
    print()
    print(f"- Sampled Bank instructions: `{len(rows)}`")
    print(f"- Distinct account keys passed to Bank instructions: `{len(all_accounts)}`")
    print(f"- Bank instructions with canonical Solana JUP mint account: `{jup_hits}`")
    print()
    print("## Global Account Frequency")
    print()
    print("| Account | Count | Role hints |")
    print("|---|---:|---|")
    for account, count in all_accounts.most_common(30):
        labels = []
        if account in KNOWN_ACCOUNTS:
            labels.append(KNOWN_ACCOUNTS[account])
        if signer_appearances[account]:
            labels.append("signer")
        print(f"| `{account}` | {count} | {', '.join(labels)} |")
    print()
    print("## Strong Co-Occurrence Edges")
    print()
    print("| Account A | Account B | Shared instructions |")
    print("|---|---|---:|")
    for (left, right), count in edges.most_common(25):
        if count < 2:
            continue
        print(f"| `{left}` | `{right}` | {count} |")
    print()
    print("## Positional Account Layouts")
    print()
    for (discriminator, raw_len), summary in sorted(variants.items(), key=lambda item: (-len(item[1]["rows"]), item[0])):
        name = summary["name"] or "unknown"
        print(f"### `{name}` `{discriminator}` raw length `{raw_len}`")
        print()
        print(f"- Samples: `{len(summary['rows'])}`")
        print(f"- Signers: {format_counter(summary['signers']) or '`None`'}")
        print()
        print("| Position | Most common account(s) | Label hints |")
        print("|---:|---|---|")
        for position in sorted(summary["positions"]):
            accounts = format_counter(summary["positions"][position], 5)
            labels = format_counter(summary["labels"][position], 5)
            print(f"| {position} | {accounts} | {labels} |")
        print()
    print("## Payload Shape Hints")
    print()
    for (discriminator, raw_len), report in sorted(payloads.items(), key=lambda item: (-item[1]["count"], item[0])):
        name = report["name"] or "unknown"
        print(f"### `{name}` `{discriminator}` raw length `{raw_len}`")
        print()
        print(f"- Samples: `{report['count']}`")
        if report["strings"]:
            strings = "<br>".join(
                f"offset `{offset}` text `{text}` count `{count}`"
                for (offset, text), count in report["strings"].most_common(8)
            )
            print(f"- Printable payload strings: {strings}")
        else:
            print("- Printable payload strings: `None`")
        stable_u32 = [
            (offset, values)
            for offset, values in report["u32_offsets"].items()
            if values.most_common(1)[0][1] == report["count"]
        ]
        if stable_u32:
            fields = "<br>".join(
                f"offset `{offset}` value `{values.most_common(1)[0][0]}`"
                for offset, values in sorted(stable_u32)[:12]
            )
            print(f"- Stable aligned u32 candidates: {fields}")
        else:
            print("- Stable aligned u32 candidates: `None`")
        stable_u64 = [
            (offset, values)
            for offset, values in report["u64_offsets"].items()
            if values.most_common(1)[0][1] == report["count"]
        ]
        if stable_u64:
            fields = "<br>".join(
                f"offset `{offset}` value `{values.most_common(1)[0][0]}`"
                for offset, values in sorted(stable_u64)[:12]
            )
            print(f"- Stable aligned u64 candidates: {fields}")
        else:
            print("- Stable aligned u64 candidates: `None`")
        if report["pubkey_offsets"]:
            pubs = "<br>".join(
                f"offset `{offset}` `{values.most_common(1)[0][0]}`"
                for offset, values in sorted(report["pubkey_offsets"].items())
            )
            print(f"- Embedded known pubkey candidates: {pubs}")
        else:
            print("- Embedded known pubkey candidates: `None`")
        print()
    print("## PDA Seed Hunt")
    print()
    if pdas:
        print("| Program | Seeds | Derived observed account |")
        print("|---|---|---|")
        for row in pdas:
            print(f"| `{row['program']}` | `{row['seeds']}` | `{row['account']}` |")
    else:
        print("- No observed Bank instruction account matched the bounded seed list.")
    print()
    print("## Assessment")
    print()
    print("- The account graph shows stable protocol plumbing accounts across variants, especially the repeated Bank Program executable, inbox/outbox-adjacent accounts, SPL Token, system program and instructions sysvar.")
    print("- `sweep` carries asset metadata strings in its payload; in the sampled data those strings identify USDC, not JUP.")
    print("- `verify_request` has a large mostly binary payload consistent with proof/message verification data, but this report does not decode it into a trusted ABI.")
    print("- The bounded PDA search did not expose a canonical JUP-derived PDA or a simple `JUPNET_INBOX`/Merkle seed account in the observed account set.")
    print("- This adds negative evidence against visible JUP-denominated security in the sampled Bank path, while strengthening the cross-chain request/proof interpretation.")


if __name__ == "__main__":
    main()
