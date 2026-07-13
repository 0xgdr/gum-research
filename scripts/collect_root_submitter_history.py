#!/usr/bin/env python3
"""Collect Solana mainnet history for decoded outbox root-update submitters."""

from __future__ import annotations

import argparse
import json
import time
import urllib.error
import urllib.request
from pathlib import Path

from analyze_root_update_authority_graph import root_update_rows


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


def save(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def collect_signatures(endpoint: str, address: str, limit: int, page_size: int, timeout: int, pause: float) -> list[dict]:
    rows = []
    before = None
    while len(rows) < limit:
        remaining = min(page_size, limit - len(rows))
        params = [address, {"limit": remaining}]
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


def derived_submitters(snapshot: Path) -> list[str]:
    submitters = sorted({signer for row in root_update_rows(snapshot) for signer in row["tx_signers"]})
    return submitters


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot_dir")
    parser.add_argument("--endpoint", default=SOLANA_ENDPOINT)
    parser.add_argument("--submitter", action="append", help="Root submitter address to collect. Defaults to decoded submitters.")
    parser.add_argument("--signature-limit", type=int, default=50)
    parser.add_argument("--page-size", type=int, default=50)
    parser.add_argument("--transaction-limit", type=int, default=50)
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--pause", type=float, default=0.15)
    args = parser.parse_args()

    snapshot = Path(args.snapshot_dir)
    submitters = sorted(set(args.submitter or derived_submitters(snapshot)))
    manifest = {"endpoint": args.endpoint, "submitters": [], "signature_limit": args.signature_limit}

    for submitter in submitters:
        short = submitter[:8]
        signatures = collect_signatures(args.endpoint, submitter, args.signature_limit, args.page_size, args.timeout, args.pause)
        signature_file = f"solana-mainnet-root-submitter-{short}-signatures.json"
        save(snapshot / signature_file, {"address": submitter, "result": signatures})

        fetched = []
        account_info = rpc(args.endpoint, "getAccountInfo", [submitter, {"encoding": "jsonParsed"}], args.timeout)
        account_file = f"solana-mainnet-root-submitter-{short}-account.json"
        save(snapshot / account_file, account_info)
        time.sleep(args.pause)

        for item in signatures[: args.transaction_limit]:
            signature = item["signature"]
            params = [signature, {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 0}]
            try:
                tx = rpc(args.endpoint, "getTransaction", params, args.timeout)
            except urllib.error.HTTPError as exc:
                tx = {"jsonrpc": "2.0", "id": 1, "error": {"message": str(exc)}}
            filename = f"solana-mainnet-root-submitter-{short}-tx-{signature[:8]}.json"
            save(snapshot / filename, tx)
            fetched.append(filename)
            time.sleep(args.pause)

        manifest["submitters"].append(
            {
                "address": submitter,
                "signature_file": signature_file,
                "account_file": account_file,
                "signature_count": len(signatures),
                "fetched": len(fetched),
                "transaction_files": fetched,
            }
        )

    save(snapshot / "solana-mainnet-root-submitter-history-manifest.json", manifest)
    print(f"Fetched root submitter history for {len(submitters)} submitter(s)")


if __name__ == "__main__":
    main()
