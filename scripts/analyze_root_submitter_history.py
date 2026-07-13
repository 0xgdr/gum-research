#!/usr/bin/env python3
"""Analyze direct Solana history collected for root-update submitters."""

from __future__ import annotations

import argparse
import collections
import datetime as dt
import json
from pathlib import Path

from analyze_root_update_authority_graph import JUP_MINT
from analyze_root_update_authority_graph import OUTBOX_PROGRAM
from analyze_root_update_authority_graph import OUTBOX_ROOT_ACCOUNT
from analyze_root_update_authority_graph import block_time
from analyze_root_update_authority_graph import parse_programdata
from analyze_root_update_authority_graph import role_for
from analyze_root_update_authority_graph import validator_related_keys


INTERESTING_LOG_TERMS = (
    "UpdateMerkleRoot",
    "VerifyOutboxMessage",
    "SubmitInboxMessage",
    "Verifying BLS signature",
    "Signature verified",
    "Merkle proof verified",
    "Outbox verification passed",
    "inbox",
    "outbox",
    "jup",
    "stake",
    "validator",
    "quorum",
    "signer",
    "weight",
)


def load(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def account_keys(tx: dict) -> list[str]:
    keys = []
    for key in tx.get("transaction", {}).get("message", {}).get("accountKeys") or []:
        keys.append(key["pubkey"] if isinstance(key, dict) else key)
    return keys


def signers(tx: dict) -> set[str]:
    out = set()
    for key in tx.get("transaction", {}).get("message", {}).get("accountKeys") or []:
        if isinstance(key, dict) and key.get("signer"):
            out.add(key["pubkey"])
    return out


def programs(tx: dict) -> list[str]:
    out = []
    for ix in tx.get("transaction", {}).get("message", {}).get("instructions") or []:
        if ix.get("programId"):
            out.append(ix["programId"])
    for group in tx.get("meta", {}).get("innerInstructions") or []:
        for ix in group.get("instructions") or []:
            if ix.get("programId"):
                out.append(ix["programId"])
    return out


def logs(tx: dict) -> list[str]:
    rows = tx.get("meta", {}).get("logMessages") or []
    return [line for line in rows if any(term.lower() in line.lower() for term in INTERESTING_LOG_TERMS)]


def balance_delta(tx: dict, address: str) -> dict:
    keys = account_keys(tx)
    if address not in keys:
        return {}
    index = keys.index(address)
    pre = tx.get("meta", {}).get("preBalances") or []
    post = tx.get("meta", {}).get("postBalances") or []
    return {
        "index": index,
        "pre": pre[index] if index < len(pre) else None,
        "post": post[index] if index < len(post) else None,
        "delta": (post[index] - pre[index]) if index < len(pre) and index < len(post) else None,
        "fee": tx.get("meta", {}).get("fee"),
    }


def parsed_system_transfers(tx: dict, address: str) -> list[str]:
    transfers = []
    instructions = list(tx.get("transaction", {}).get("message", {}).get("instructions") or [])
    for group in tx.get("meta", {}).get("innerInstructions") or []:
        instructions.extend(group.get("instructions") or [])
    for ix in instructions:
        parsed = ix.get("parsed")
        if not isinstance(parsed, dict):
            continue
        if parsed.get("type") not in {"transfer", "transferChecked"}:
            continue
        info = parsed.get("info") or {}
        source = info.get("source") or info.get("authority")
        destination = info.get("destination")
        lamports = info.get("lamports")
        amount = info.get("amount")
        mint = info.get("mint")
        if address in {source, destination, info.get("owner")}:
            value = lamports if lamports is not None else amount
            suffix = f" mint={mint}" if mint else ""
            transfers.append(f"{parsed.get('type')} {source}->{destination} value={value}{suffix}")
    return transfers


def token_hints(tx: dict, address: str) -> list[str]:
    hints = []
    keys = account_keys(tx)
    for name in ("preTokenBalances", "postTokenBalances"):
        for row in tx.get("meta", {}).get(name) or []:
            owner = row.get("owner")
            account_index = row.get("accountIndex")
            account = keys[account_index] if isinstance(account_index, int) and account_index < len(keys) else None
            if address in {owner, account}:
                hints.append(f"{name}: account={account} mint={row.get('mint')} owner={owner}")
    return hints


def upgrade_authorities(base: Path) -> dict[str, list[str]]:
    out = collections.defaultdict(list)
    for row in parse_programdata(base):
        if row.get("authority"):
            out[row["authority"]].append(row["label"])
    return out


def manifest_rows(base: Path) -> list[dict]:
    manifest = load(base / "solana-mainnet-root-submitter-history-manifest.json")
    return manifest.get("submitters") or []


def tx_file_rows(base: Path, manifest_row: dict) -> list[tuple[Path, dict]]:
    rows = []
    for filename in manifest_row.get("transaction_files") or []:
        path = base / filename
        tx = load(path).get("result")
        if tx:
            rows.append((path, tx))
    return rows


def fmt(values, empty: str = "`None`", limit: int | None = None) -> str:
    items = sorted(values) if isinstance(values, set) else list(values)
    items = [str(item) for item in items if item]
    if limit is not None:
        items = items[:limit]
    if not items:
        return empty
    return "<br>".join(f"`{item}`" for item in items)


def fmt_counter(counter: collections.Counter[str], limit: int | None = None) -> str:
    return fmt([f"{key}: {value}" for key, value in counter.most_common(limit)])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot_dir")
    args = parser.parse_args()
    base = Path(args.snapshot_dir)

    validators = validator_related_keys(base)
    authorities = upgrade_authorities(base)
    manifests = manifest_rows(base)

    print("# Root Submitter Direct History")
    print()
    print("## Scope")
    print()
    print(f"- Snapshot: `{base}`")
    print(f"- Submitters with collected history: `{len(manifests)}`")
    print(f"- Manifest: `solana-mainnet-root-submitter-history-manifest.json`")
    print()

    if not manifests:
        print("## Assessment")
        print()
        print("- No direct submitter history manifest was found. Run `scripts/collect_root_submitter_history.py` first.")
        return

    total_txs = 0
    all_security_hits = set()
    all_authority_hits = set()
    all_programs = collections.Counter()
    all_submitter_occurrences = collections.Counter()

    print("## Submitter Summary")
    print()
    print("| Submitter | Signatures | Fetched txs | Account lamports | Owner | Executable |")
    print("|---|---:|---:|---:|---|---|")
    for row in manifests:
        account_value = (load(base / row.get("account_file", "")).get("result") or {}).get("value") or {}
        print(
            f"| `{row['address']}` | {row.get('signature_count')} | {row.get('fetched')} | "
            f"{account_value.get('lamports')} | `{account_value.get('owner')}` | `{account_value.get('executable')}` |"
        )
    print()

    for row in manifests:
        address = row["address"]
        rows = tx_file_rows(base, row)
        total_txs += len(rows)
        print(f"## Submitter `{address}`")
        print()
        print("| File | Time | Slot | Signer | Root update | Lamport delta | Programs | Security hits | Authority hits | Transfers | Logs |")
        print("|---|---|---:|---|---|---|---|---|---|---|---|")
        program_counter = collections.Counter()
        transfer_counter = collections.Counter()
        positive_deltas = []
        negative_deltas = []
        security_hits = set()
        authority_hits = set()
        for path, tx in sorted(rows, key=lambda item: ((item[1].get("slot") or 0), item[0].name)):
            keys = set(account_keys(tx))
            tx_programs = programs(tx)
            for program in tx_programs:
                program_counter[program] += 1
                all_programs[program] += 1
            tx_security_hits = (keys & set(validators)) | ({JUP_MINT} if JUP_MINT in keys else set())
            tx_authority_hits = keys & set(authorities)
            security_hits.update(tx_security_hits)
            authority_hits.update(tx_authority_hits)
            all_security_hits.update(tx_security_hits)
            all_authority_hits.update(tx_authority_hits)
            delta = balance_delta(tx, address)
            if delta.get("delta", 0) > 0:
                positive_deltas.append((path.name, delta["delta"]))
            if delta.get("delta", 0) < 0:
                negative_deltas.append((path.name, delta["delta"]))
            transfers = parsed_system_transfers(tx, address)
            for transfer in transfers:
                transfer_counter[transfer] += 1
            root_update = OUTBOX_PROGRAM in tx_programs and OUTBOX_ROOT_ACCOUNT in keys and any("UpdateMerkleRoot" in line for line in logs(tx))
            all_submitter_occurrences[address] += 1
            print(
                f"| `{path.name}` | `{block_time(tx.get('blockTime'))}` | {tx.get('slot')} | "
                f"`{address in signers(tx)}` | `{root_update}` | "
                f"`{delta.get('delta')} fee={delta.get('fee')}` | {fmt(tx_programs, limit=6)} | "
                f"{fmt([f'{key} => {role_for(key, validators, authorities)}' for key in tx_security_hits])} | "
                f"{fmt([f'{key} => {role_for(key, validators, authorities)}' for key in tx_authority_hits])} | "
                f"{fmt(transfers, limit=4)} | {fmt(logs(tx), limit=6)} |"
            )
        print()
        print("### Submitter Aggregates")
        print()
        print("| Group | Values |")
        print("|---|---|")
        print(f"| Programs | {fmt_counter(program_counter)} |")
        print(f"| Positive lamport deltas | {fmt([f'{name}: {delta}' for name, delta in positive_deltas])} |")
        print(f"| Negative lamport deltas | {fmt([f'{name}: {delta}' for name, delta in negative_deltas], limit=20)} |")
        print(f"| Transfers involving submitter | {fmt_counter(transfer_counter, limit=20)} |")
        print(f"| Token-balance hints | {fmt([hint for _path, tx in rows for hint in token_hints(tx, address)], limit=20)} |")
        print(f"| Security intersections | {fmt([f'{key} => {role_for(key, validators, authorities)}' for key in security_hits])} |")
        print(f"| Upgrade-authority intersections | {fmt([f'{key} => {role_for(key, validators, authorities)}' for key in authority_hits])} |")
        print()

    print("## Cross-Submitter Assessment")
    print()
    print(f"- Transaction bodies analyzed: `{total_txs}`")
    print(f"- Unique submitters observed in direct history: `{len(all_submitter_occurrences)}`")
    print(f"- Programs invoked across submitter history: {fmt_counter(all_programs)}")
    print(f"- Canonical JUP / current validator / vote / stake intersections: `{len(all_security_hits)}`")
    print(f"- Parsed upgrade-authority intersections: `{len(all_authority_hits)}`")
    print()
    if all_security_hits or all_authority_hits:
        print("- Direct submitter history exposed at least one watched security or upgrade-authority intersection.")
    else:
        print("- Direct submitter history did not expose canonical JUP, current validator/vote/stake keys or parsed upgrade authorities.")
    print("- Funding attribution depends on whether positive lamport deltas or transfer-source rows are present in the fetched signature window.")


if __name__ == "__main__":
    main()
