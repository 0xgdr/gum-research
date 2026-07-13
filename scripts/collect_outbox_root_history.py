#!/usr/bin/env python3
"""Collect a wider Solana mainnet history for the JupNet outbox helper program."""

from __future__ import annotations

import argparse
import json
import time
import urllib.error
import urllib.request
from pathlib import Path


SOLANA_ENDPOINT = "https://api.mainnet-beta.solana.com"
OUTBOX_PROGRAM = "jnoUtncGR9ZCCMixtys6Gzy5coTo6mnmUZuEHRQFTFV"


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


def save(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def collect_signatures(endpoint: str, limit: int, page_size: int, timeout: int, pause: float) -> list[dict]:
    rows = []
    before = None
    while len(rows) < limit:
        remaining = min(page_size, limit - len(rows))
        params = [OUTBOX_PROGRAM, {"limit": remaining}]
        if before:
            params[1]["before"] = before
        response = rpc(endpoint, "getSignaturesForAddress", params, timeout)
        batch = response.get("result") or []
        if not batch:
            break
        rows.extend(batch)
        before = batch[-1]["signature"]
        time.sleep(pause)
        if len(batch) < remaining:
            break
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot_dir")
    parser.add_argument("--endpoint", default=SOLANA_ENDPOINT)
    parser.add_argument("--signature-limit", type=int, default=100)
    parser.add_argument("--page-size", type=int, default=100)
    parser.add_argument("--transaction-limit", type=int, default=100)
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--pause", type=float, default=0.15)
    args = parser.parse_args()

    snapshot = Path(args.snapshot_dir)
    signatures = collect_signatures(args.endpoint, args.signature_limit, args.page_size, args.timeout, args.pause)
    save(snapshot / "solana-mainnet-outbox-history-signatures.json", {"result": signatures})

    fetched = []
    for item in signatures[: args.transaction_limit]:
        signature = item["signature"]
        params = [signature, {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 0}]
        try:
            tx = rpc(args.endpoint, "getTransaction", params, args.timeout)
        except urllib.error.HTTPError as exc:
            tx = {"jsonrpc": "2.0", "id": 1, "error": {"message": str(exc)}}
        filename = f"solana-mainnet-outbox-history-tx-{signature[:8]}.json"
        save(snapshot / filename, tx)
        fetched.append(filename)
        time.sleep(args.pause)

    save(
        snapshot / "solana-mainnet-outbox-root-history-transaction-files.json",
        {
            "program": OUTBOX_PROGRAM,
            "signature_count": len(signatures),
            "fetched": len(fetched),
            "transaction_files": fetched,
        },
    )
    print(f"Fetched {len(fetched)} outbox history transactions from {len(signatures)} signatures")


if __name__ == "__main__":
    main()
