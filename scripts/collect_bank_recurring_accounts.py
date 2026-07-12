#!/usr/bin/env python3
"""Fetch Solana account state for recurring sampled GUM Bank accounts."""

from __future__ import annotations

import argparse
import collections
import json
import time
import urllib.request
from pathlib import Path


SOLANA_ENDPOINT = "https://api.mainnet-beta.solana.com"
GUM_BANK_PROGRAM = "BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ"
JUP_MINT = "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN"
SYSTEM_PROGRAM = "11111111111111111111111111111111"
SYSVAR_INSTRUCTIONS = "Sysvar1nstructions1111111111111111111111111"
SPL_TOKEN = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
ASSOCIATED_TOKEN = "ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL"
WRAPPED_SOL = "So11111111111111111111111111111111111111112"
USDC = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"

EXCLUDED = {
    GUM_BANK_PROGRAM,
    JUP_MINT,
    SYSTEM_PROGRAM,
    SYSVAR_INSTRUCTIONS,
    SPL_TOKEN,
    ASSOCIATED_TOKEN,
    WRAPPED_SOL,
    USDC,
}


def load(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def rpc(endpoint: str, method: str, params: list | None, timeout: int) -> dict:
    body = {"jsonrpc": "2.0", "id": 1, "method": method}
    if params is not None:
        body["params"] = params
    data = json.dumps(body, separators=(",", ":")).encode()
    req = urllib.request.Request(
        endpoint,
        data=data,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "gum-research-validator-monitor",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as res:
        return json.loads(res.read().decode())


def bank_account_counts(snapshot: Path) -> collections.Counter:
    counts: collections.Counter = collections.Counter()
    for path in sorted(snapshot.glob("solana-mainnet-bank-tx-*.json")):
        tx = load(path).get("result")
        if not tx:
            continue
        for ix in tx.get("transaction", {}).get("message", {}).get("instructions", []):
            if ix.get("programId") != GUM_BANK_PROGRAM:
                continue
            counts.update(ix.get("accounts") or [])
    return counts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot_dir")
    parser.add_argument("--endpoint", default=SOLANA_ENDPOINT)
    parser.add_argument("--min-count", type=int, default=2)
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--pause", type=float, default=0.15)
    args = parser.parse_args()

    snapshot = Path(args.snapshot_dir)
    counts = bank_account_counts(snapshot)
    accounts = [
        account
        for account, count in counts.most_common()
        if count >= args.min_count and account not in EXCLUDED
    ]

    response = rpc(args.endpoint, "getMultipleAccounts", [accounts, {"encoding": "base64"}], args.timeout)
    (snapshot / "solana-mainnet-getMultipleAccounts-BankRecurringAccounts.json").write_text(
        json.dumps(
            {
                "accounts": accounts,
                "counts": {account: counts[account] for account in accounts},
                "response": response,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )
    time.sleep(args.pause)
    print(f"Fetched {len(accounts)} recurring Bank accounts")


if __name__ == "__main__":
    main()
