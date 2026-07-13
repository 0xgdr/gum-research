#!/usr/bin/env python3
"""Collect a Solana mainnet transaction cohort for the bk1PDA Gum Bank path."""

from __future__ import annotations

import argparse
import json
import time
import urllib.error
import urllib.request
from pathlib import Path


SOLANA_ENDPOINT = "https://api.mainnet-beta.solana.com"
GUM_BANK_REQUEST = "bk1PDAkbHEBGtVRiM94Lzets8gVFP7FgySyfkAc8MPN"


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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot_dir")
    parser.add_argument("--endpoint", default=SOLANA_ENDPOINT)
    parser.add_argument("--address", default=GUM_BANK_REQUEST)
    parser.add_argument("--signature-limit", type=int, default=100)
    parser.add_argument("--transaction-limit", type=int, default=100)
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--pause", type=float, default=0.35)
    parser.add_argument("--retries", type=int, default=5)
    args = parser.parse_args()

    base = Path(args.snapshot_dir)
    signatures = rpc_with_retries(
        args.endpoint,
        "getSignaturesForAddress",
        [args.address, {"limit": args.signature_limit}],
        args.timeout,
        args.pause,
        args.retries,
    )
    signature_file = "solana-mainnet-bank-withdrawal-cohort-signatures.json"
    save(base / signature_file, {"address": args.address, "response": signatures})
    rows = signatures.get("result") or []
    time.sleep(args.pause)

    tx_files = []
    for item in rows[: args.transaction_limit]:
        signature = item["signature"]
        filename = f"solana-mainnet-bank-withdrawal-cohort-tx-{signature[:8]}.json"
        tx = rpc_with_retries(
            args.endpoint,
            "getTransaction",
            [signature, {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 0}],
            args.timeout,
            args.pause,
            args.retries,
        )
        save(base / filename, tx)
        tx_files.append(filename)
        time.sleep(args.pause)

    save(
        base / "solana-mainnet-bank-withdrawal-cohort-manifest.json",
        {
            "address": args.address,
            "signature_file": signature_file,
            "signature_count": len(rows),
            "transaction_count": len(tx_files),
            "transaction_files": tx_files,
        },
    )
    print(f"Fetched {len(tx_files)} transactions for {args.address}")


if __name__ == "__main__":
    main()
