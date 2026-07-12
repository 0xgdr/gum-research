#!/usr/bin/env python3
"""Collect recent JupNet outbox helper transactions for root-update analysis."""

from __future__ import annotations

import argparse
import json
import time
import urllib.error
import urllib.request
from pathlib import Path


SOLANA_ENDPOINT = "https://api.mainnet-beta.solana.com"


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
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--pause", type=float, default=0.15)
    args = parser.parse_args()

    snapshot = Path(args.snapshot_dir)
    sigs = load(snapshot / "solana-mainnet-getSignaturesForAddress-JupNetOutboxProgram.json").get("result") or []
    fetched = []
    for item in sigs[: args.limit]:
        signature = item["signature"]
        params = [signature, {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 0}]
        try:
            tx = rpc(args.endpoint, "getTransaction", params, args.timeout)
        except urllib.error.HTTPError as exc:
            tx = {"jsonrpc": "2.0", "id": 1, "error": {"message": str(exc)}}
        filename = f"solana-mainnet-outbox-tx-{signature[:8]}.json"
        save(snapshot / filename, tx)
        fetched.append(filename)
        time.sleep(args.pause)

    save(
        snapshot / "solana-mainnet-outbox-root-update-transaction-files.json",
        {"transaction_files": fetched, "source_signature_count": len(sigs), "fetched": len(fetched)},
    )
    print(f"Fetched {len(fetched)} outbox helper transactions")


if __name__ == "__main__":
    main()
