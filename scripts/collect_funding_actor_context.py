#!/usr/bin/env python3
"""Collect Solana mainnet context for accounts in root submitter funding events."""

from __future__ import annotations

import argparse
import json
import time
import urllib.error
import urllib.request
from pathlib import Path

from analyze_root_submitter_history import account_keys
from analyze_root_submitter_history import parsed_system_transfers
from analyze_root_submitter_history import programs


SOLANA_ENDPOINT = "https://api.mainnet-beta.solana.com"


def rpc(endpoint: str, method: str, params: list | None, timeout: int) -> dict:
    body = {"jsonrpc": "2.0", "id": 1, "method": method}
    if params is not None:
        body["params"] = params
    data = json.dumps(body, separators=(",", ":")).encode()
    req = urllib.request.Request(
        endpoint,
        data=data,
        headers={"Content-Type": "application/json", "User-Agent": "gum-research-validator-monitor"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as res:
        return json.loads(res.read().decode())


def rpc_with_retries(endpoint: str, method: str, params: list | None, timeout: int, pause: float, retries: int) -> dict:
    last_error = None
    for attempt in range(retries + 1):
        try:
            return rpc(endpoint, method, params, timeout)
        except (urllib.error.HTTPError, urllib.error.URLError) as exc:
            last_error = exc
            if attempt >= retries:
                break
            time.sleep(pause * (2**attempt))
    return {"jsonrpc": "2.0", "id": 1, "error": {"message": str(last_error)}}


def load(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def save(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def funding_manifest(base: Path) -> list[dict]:
    data = load(base / "solana-mainnet-root-submitter-funding-history-manifest.json")
    return data.get("submitters") or []


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


def funding_targets(base: Path) -> tuple[list[str], dict[str, list[str]]]:
    roles: dict[str, set[str]] = {}

    def add(address: str | None, role: str) -> None:
        if not address:
            return
        roles.setdefault(address, set()).add(role)

    for row in funding_manifest(base):
        submitter = row.get("address")
        add(submitter, "root submitter")
        for filename in row.get("positive_delta_files") or []:
            tx = load(base / filename).get("result")
            if not tx:
                continue
            keys = tx.get("transaction", {}).get("message", {}).get("accountKeys") or []
            if keys:
                first = keys[0]
                add(first.get("pubkey") if isinstance(first, dict) else first, "fee payer")
            for key in keys:
                if isinstance(key, dict):
                    if key.get("signer"):
                        add(key.get("pubkey"), "transaction signer")
                    if key.get("writable"):
                        add(key.get("pubkey"), "writable funding-tx account")
            for source in transfer_sources(tx, submitter):
                add(source, "parsed transfer source into root submitter")
            for program in programs(tx):
                add(program, "invoked program")
            for ix in all_instructions(tx):
                if ix.get("programId"):
                    add(ix["programId"], "instruction program")
                for account in ix.get("accounts") or []:
                    add(account, "funding-tx instruction account")

    return sorted(roles), {address: sorted(values) for address, values in roles.items()}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot_dir")
    parser.add_argument("--endpoint", default=SOLANA_ENDPOINT)
    parser.add_argument("--signature-limit", type=int, default=30)
    parser.add_argument("--skip-signatures", action="store_true")
    parser.add_argument(
        "--signature-role",
        action="append",
        help="Only fetch signatures for accounts with this inferred role. Can be repeated.",
    )
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--pause", type=float, default=0.25)
    parser.add_argument("--retries", type=int, default=5)
    args = parser.parse_args()

    base = Path(args.snapshot_dir)
    targets, roles = funding_targets(base)
    account_response = rpc_with_retries(
        args.endpoint,
        "getMultipleAccounts",
        [targets, {"encoding": "base64"}],
        args.timeout,
        args.pause,
        args.retries,
    )
    save(base / "solana-mainnet-getMultipleAccounts-FundingActors.json", {"accounts": targets, "roles": roles, "response": account_response})
    time.sleep(args.pause)

    signature_targets = targets
    if args.signature_role:
        wanted_roles = set(args.signature_role)
        signature_targets = [
            account for account in targets if wanted_roles & set(roles.get(account) or [])
        ]

    signatures = {}
    for account in [] if args.skip_signatures else signature_targets:
        signatures[account] = rpc_with_retries(
            args.endpoint,
            "getSignaturesForAddress",
            [account, {"limit": args.signature_limit}],
            args.timeout,
            args.pause,
            args.retries,
        )
        time.sleep(args.pause)
    save(base / "solana-mainnet-getSignaturesForAddress-FundingActors.json", signatures)

    print(f"Fetched funding actor context for {len(targets)} accounts and signatures for {len(signatures)} accounts")


if __name__ == "__main__":
    main()
