#!/usr/bin/env python3
"""Fetch current account state for Bank/Gum accounts created in sampled transactions."""

from __future__ import annotations

import argparse
import collections
import json
import time
import urllib.error
import urllib.request
from pathlib import Path

from analyze_bank_request_message_correlation import created_accounts
from analyze_bank_request_message_correlation import instruction_names
from analyze_bank_request_message_correlation import load
from analyze_bank_request_message_correlation import manifest_files
from analyze_bank_request_message_correlation import tx_result


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


def save(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def transaction_sources(base: Path) -> list[tuple[str, str, dict]]:
    rows = []
    for prefix, surface in (
        ("bank-withdrawal-cohort", "bk1PDA"),
        ("bank-program-withdrawal-cohort", "BankK"),
    ):
        for filename in manifest_files(base, prefix):
            tx = tx_result(base, filename)
            if tx:
                rows.append((surface, filename, tx))

    funding_manifest = load(base / "solana-mainnet-root-submitter-funding-history-manifest.json")
    for submitter in funding_manifest.get("submitters") or []:
        for filename in submitter.get("positive_delta_files") or []:
            tx = tx_result(base, filename)
            if tx:
                rows.append(("root_submitter_setup", filename, tx))
    return rows


def created_account_manifest(base: Path) -> tuple[list[str], dict[str, dict]]:
    accounts: dict[str, dict] = {}
    for surface, filename, tx in transaction_sources(base):
        logs = tx.get("meta", {}).get("logMessages") or []
        instructions = instruction_names(logs)
        signature = (tx.get("transaction", {}).get("signatures") or [""])[0]
        for item in created_accounts(tx):
            account = item.get("account")
            if not account:
                continue
            row = accounts.setdefault(
                account,
                {
                    "account": account,
                    "created_by": [],
                    "owners": collections.Counter(),
                    "spaces": collections.Counter(),
                    "sources": collections.Counter(),
                    "lamports": collections.Counter(),
                    "surfaces": collections.Counter(),
                    "instructions": collections.Counter(),
                },
            )
            row["created_by"].append(
                {
                    "surface": surface,
                    "file": filename,
                    "signature": signature,
                    "slot": tx.get("slot"),
                    "block_time": tx.get("blockTime"),
                    "owner": item.get("owner"),
                    "space": item.get("space"),
                    "source": item.get("source"),
                    "lamports": item.get("lamports"),
                    "instructions": instructions,
                }
            )
            row["owners"][item.get("owner")] += 1
            row["spaces"][str(item.get("space"))] += 1
            row["sources"][item.get("source")] += 1
            row["lamports"][str(item.get("lamports"))] += 1
            row["surfaces"][surface] += 1
            row["instructions"].update(instructions)

    serializable = {}
    for account, row in accounts.items():
        serializable[account] = {
            **row,
            "owners": dict(row["owners"]),
            "spaces": dict(row["spaces"]),
            "sources": dict(row["sources"]),
            "lamports": dict(row["lamports"]),
            "surfaces": dict(row["surfaces"]),
            "instructions": dict(row["instructions"]),
        }
    return sorted(accounts), serializable


def chunks(items: list[str], size: int) -> list[list[str]]:
    return [items[index : index + size] for index in range(0, len(items), size)]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot_dir")
    parser.add_argument("--endpoint", default=SOLANA_ENDPOINT)
    parser.add_argument("--batch-size", type=int, default=100)
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--pause", type=float, default=0.25)
    parser.add_argument("--retries", type=int, default=5)
    args = parser.parse_args()

    base = Path(args.snapshot_dir)
    accounts, metadata = created_account_manifest(base)
    responses = []
    values = []
    for batch in chunks(accounts, args.batch_size):
        response = rpc_with_retries(
            args.endpoint,
            "getMultipleAccounts",
            [batch, {"encoding": "base64"}],
            args.timeout,
            args.pause,
            args.retries,
        )
        responses.append({"accounts": batch, "response": response})
        result_values = ((response.get("result") or {}).get("value") or [])
        values.extend(result_values)
        time.sleep(args.pause)

    save(
        base / "solana-mainnet-getMultipleAccounts-CreatedBankStateAccounts.json",
        {
            "accounts": accounts,
            "metadata": metadata,
            "responses": responses,
            "values": values,
        },
    )
    print(f"Fetched current account state for {len(accounts)} created Bank/Gum state accounts")


if __name__ == "__main__":
    main()
