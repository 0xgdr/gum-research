#!/usr/bin/env python3
"""Analyze older root submitter transactions for funding provenance."""

from __future__ import annotations

import argparse
import collections
import json
from pathlib import Path

from analyze_root_submitter_history import account_keys
from analyze_root_submitter_history import balance_delta
from analyze_root_submitter_history import logs
from analyze_root_submitter_history import parsed_system_transfers
from analyze_root_submitter_history import programs
from analyze_root_submitter_history import token_hints
from analyze_root_update_authority_graph import JUP_MINT
from analyze_root_update_authority_graph import block_time
from analyze_root_update_authority_graph import parse_programdata
from analyze_root_update_authority_graph import role_for
from analyze_root_update_authority_graph import validator_related_keys


def load(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def manifest_rows(base: Path) -> list[dict]:
    manifest = load(base / "solana-mainnet-root-submitter-funding-history-manifest.json")
    return manifest.get("submitters") or []


def upgrade_authorities(base: Path) -> dict[str, list[str]]:
    out = collections.defaultdict(list)
    for row in parse_programdata(base):
        if row.get("authority"):
            out[row["authority"]].append(row["label"])
    return out


def transfer_sources(transfers: list[str], destination: str) -> list[str]:
    sources = []
    marker = f"->{destination}"
    for transfer in transfers:
        if marker not in transfer:
            continue
        left = transfer.split(" ", 1)[1].split("->", 1)[0]
        if left:
            sources.append(left)
    return sources


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

    print("# Root Submitter Funding History")
    print()
    print("## Scope")
    print()
    print(f"- Snapshot: `{base}`")
    print(f"- Submitters with funding-history collection: `{len(manifests)}`")
    print(f"- Manifest: `solana-mainnet-root-submitter-funding-history-manifest.json`")
    print()

    if not manifests:
        print("## Assessment")
        print()
        print("- No funding-history manifest was found. Run `scripts/collect_root_submitter_funding_history.py` first.")
        return

    total_fetched = 0
    total_positive = 0
    all_sources = collections.Counter()
    all_programs = collections.Counter()
    all_security_hits = set()
    all_authority_hits = set()

    print("## Collection Summary")
    print()
    print("| Submitter | Before signature | Signatures | Fetched txs | Positive-delta txs |")
    print("|---|---|---:|---:|---:|")
    for row in manifests:
        print(
            f"| `{row['address']}` | `{row.get('before') or 'None'}` | {row.get('signature_count')} | "
            f"{row.get('fetched')} | {len(row.get('positive_delta_files') or [])} |"
        )
    print()

    for row in manifests:
        submitter = row["address"]
        print(f"## Submitter `{submitter}`")
        print()
        print("| File | Time | Slot | Delta | Programs | Transfers involving submitter | Security hits | Authority hits | Logs |")
        print("|---|---|---:|---:|---|---|---|---|---|")
        positive_rows = []
        negative_rows = []
        transfer_source_counter = collections.Counter()
        program_counter = collections.Counter()
        token_hint_rows = []
        security_hits = set()
        authority_hits = set()
        for filename in row.get("transaction_files") or []:
            tx = load(base / filename).get("result")
            if not tx:
                continue
            total_fetched += 1
            keys = set(account_keys(tx))
            tx_programs = programs(tx)
            program_counter.update(tx_programs)
            all_programs.update(tx_programs)
            transfers = parsed_system_transfers(tx, submitter)
            sources = transfer_sources(transfers, submitter)
            transfer_source_counter.update(sources)
            all_sources.update(sources)
            hints = token_hints(tx, submitter)
            if hints:
                token_hint_rows.append(filename)
            tx_security_hits = (keys & set(validators)) | ({JUP_MINT} if JUP_MINT in keys else set())
            tx_authority_hits = keys & set(authorities)
            security_hits.update(tx_security_hits)
            authority_hits.update(tx_authority_hits)
            all_security_hits.update(tx_security_hits)
            all_authority_hits.update(tx_authority_hits)
            delta = balance_delta(tx, submitter)
            value = delta.get("delta")
            if value is not None and value > 0:
                positive_rows.append((filename, value))
                total_positive += 1
            if value is not None and value < 0:
                negative_rows.append((filename, value))
            print(
                f"| `{filename}` | `{block_time(tx.get('blockTime'))}` | {tx.get('slot')} | "
                f"`{value}` | {fmt(tx_programs, limit=6)} | {fmt(transfers, limit=6)} | "
                f"{fmt([f'{key} => {role_for(key, validators, authorities)}' for key in tx_security_hits])} | "
                f"{fmt([f'{key} => {role_for(key, validators, authorities)}' for key in tx_authority_hits])} | "
                f"{fmt(logs(tx), limit=6)} |"
            )
        print()
        print("### Funding Aggregates")
        print()
        print("| Group | Values |")
        print("|---|---|")
        print(f"| Positive lamport deltas | {fmt([f'{name}: {delta}' for name, delta in positive_rows], limit=20)} |")
        print(f"| Negative lamport deltas | {fmt([f'{name}: {delta}' for name, delta in negative_rows], limit=20)} |")
        print(f"| Transfer sources into submitter | {fmt_counter(transfer_source_counter, limit=20)} |")
        print(f"| Programs | {fmt_counter(program_counter, limit=20)} |")
        print(f"| Token-balance hint files | {fmt(token_hint_rows, limit=20)} |")
        print(f"| Security intersections | {fmt([f'{key} => {role_for(key, validators, authorities)}' for key in security_hits])} |")
        print(f"| Upgrade-authority intersections | {fmt([f'{key} => {role_for(key, validators, authorities)}' for key in authority_hits])} |")
        print()

    print("## Cross-Submitter Assessment")
    print()
    print(f"- Funding-history transaction bodies analyzed: `{total_fetched}`")
    print(f"- Positive lamport-delta transactions found: `{total_positive}`")
    print(f"- Transfer source accounts into submitters: `{len(all_sources)}`")
    print(f"- Programs invoked across funding history: {fmt_counter(all_programs)}")
    print(f"- Canonical JUP / current validator / vote / stake intersections: `{len(all_security_hits)}`")
    print(f"- Parsed upgrade-authority intersections: `{len(all_authority_hits)}`")
    print()
    if total_positive:
        print("- At least one possible funding transaction was found in the fetched window.")
    else:
        print("- No positive funding transaction was found in the fetched window; the submitter was already funded before this older page window or funding used a pattern not captured as a positive lamport delta.")
    if all_security_hits or all_authority_hits:
        print("- Funding-history rows exposed at least one watched security or upgrade-authority intersection.")
    else:
        print("- Funding-history rows did not expose canonical JUP, current validator/vote/stake keys or parsed upgrade authorities.")


if __name__ == "__main__":
    main()
