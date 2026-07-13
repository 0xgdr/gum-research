#!/usr/bin/env python3
"""Collect older Solana mainnet transactions for root submitter funding analysis."""

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


def rpc_with_retries(endpoint: str, method: str, params: list | None, timeout: int, pause: float, retries: int) -> dict:
    last_error = None
    for attempt in range(retries + 1):
        try:
            return rpc(endpoint, method, params, timeout)
        except (urllib.error.HTTPError, urllib.error.URLError) as exc:
            last_error = exc
            if attempt >= retries:
                break
            time.sleep(pause * (2 ** attempt))
    return {"jsonrpc": "2.0", "id": 1, "error": {"message": str(last_error)}}


def load(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def save(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def account_keys(tx: dict) -> list[str]:
    keys = []
    for key in tx.get("transaction", {}).get("message", {}).get("accountKeys") or []:
        keys.append(key["pubkey"] if isinstance(key, dict) else key)
    return keys


def lamport_delta(tx: dict, address: str) -> int | None:
    keys = account_keys(tx)
    if address not in keys:
        return None
    index = keys.index(address)
    pre = tx.get("meta", {}).get("preBalances") or []
    post = tx.get("meta", {}).get("postBalances") or []
    if index >= len(pre) or index >= len(post):
        return None
    return post[index] - pre[index]


def derived_submitters(snapshot: Path) -> list[str]:
    return sorted({signer for row in root_update_rows(snapshot) for signer in row["tx_signers"]})


def existing_history_before(snapshot: Path, submitter: str) -> str | None:
    short = submitter[:8]
    data = load(snapshot / f"solana-mainnet-root-submitter-{short}-signatures.json")
    rows = data.get("result") or []
    if rows:
        return rows[-1].get("signature")
    return None


def existing_funding_before(snapshot: Path, submitter: str) -> str | None:
    short = submitter[:8]
    data = load(snapshot / f"solana-mainnet-root-submitter-funding-{short}-signatures.json")
    rows = data.get("result") or []
    if rows:
        return rows[-1].get("signature")
    return None


def collect_signatures(
    endpoint: str,
    address: str,
    limit: int,
    page_size: int,
    timeout: int,
    pause: float,
    before: str | None,
) -> list[dict]:
    rows = []
    cursor = before
    while len(rows) < limit:
        remaining = min(page_size, limit - len(rows))
        params = [address, {"limit": remaining}]
        if cursor:
            params[1]["before"] = cursor
        response = rpc_with_retries(endpoint, "getSignaturesForAddress", params, timeout, pause, retries=3)
        batch = response.get("result") or []
        if not batch:
            break
        rows.extend(batch)
        cursor = batch[-1]["signature"]
        time.sleep(pause)
        if len(batch) < remaining:
            break
    return rows


def existing_signature_rows(snapshot: Path, submitter: str) -> list[dict]:
    short = submitter[:8]
    data = load(snapshot / f"solana-mainnet-root-submitter-funding-{short}-signatures.json")
    return data.get("result") or []


def existing_manifest_row(snapshot: Path, submitter: str) -> dict:
    manifest = load(snapshot / "solana-mainnet-root-submitter-funding-history-manifest.json")
    for row in manifest.get("submitters") or []:
        if row.get("address") == submitter:
            return row
    return {}


def is_error_file(path: Path) -> bool:
    data = load(path)
    return bool(data.get("error")) or data.get("result") is None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot_dir")
    parser.add_argument("--endpoint", default=SOLANA_ENDPOINT)
    parser.add_argument("--submitter", action="append", help="Root submitter address to collect. Defaults to decoded submitters.")
    parser.add_argument("--signature-limit", type=int, default=200)
    parser.add_argument("--page-size", type=int, default=100)
    parser.add_argument("--transaction-limit", type=int, default=200)
    parser.add_argument("--stop-after-positive", type=int, default=1)
    parser.add_argument("--retry-errors-only", action="store_true")
    parser.add_argument("--continue-existing-funding", action="store_true")
    parser.add_argument("--from-latest", action="store_true", help="Start from the latest signature instead of after existing direct-history window.")
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--pause", type=float, default=0.15)
    parser.add_argument("--retries", type=int, default=5)
    args = parser.parse_args()

    snapshot = Path(args.snapshot_dir)
    submitters = sorted(set(args.submitter or derived_submitters(snapshot)))
    manifest = {
        "endpoint": args.endpoint,
        "signature_limit": args.signature_limit,
        "transaction_limit": args.transaction_limit,
        "stop_after_positive": args.stop_after_positive,
        "submitters": [],
    }

    for submitter in submitters:
        short = submitter[:8]
        if args.from_latest:
            before = None
        elif args.continue_existing_funding:
            before = existing_funding_before(snapshot, submitter) or existing_history_before(snapshot, submitter)
        else:
            before = existing_history_before(snapshot, submitter)
        previous_row = existing_manifest_row(snapshot, submitter) if args.continue_existing_funding else {}
        previous_signatures = existing_signature_rows(snapshot, submitter) if args.continue_existing_funding else []
        previous_files = list(previous_row.get("transaction_files") or [])
        previous_positive_files = list(previous_row.get("positive_delta_files") or [])
        if args.retry_errors_only:
            signatures = existing_signature_rows(snapshot, submitter)
            fetch_items = signatures[: args.transaction_limit]
        else:
            new_signatures = collect_signatures(args.endpoint, submitter, args.signature_limit, args.page_size, args.timeout, args.pause, before)
            signatures = [*previous_signatures, *new_signatures]
            fetch_items = new_signatures[: args.transaction_limit]
        signature_file = f"solana-mainnet-root-submitter-funding-{short}-signatures.json"
        if not args.retry_errors_only:
            save(snapshot / signature_file, {"address": submitter, "before": before, "result": signatures})

        fetched = previous_files if args.continue_existing_funding and not args.retry_errors_only else []
        positive_delta_files = previous_positive_files if args.continue_existing_funding and not args.retry_errors_only else []
        for item in fetch_items:
            signature = item["signature"]
            params = [signature, {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 0}]
            filename = f"solana-mainnet-root-submitter-funding-{short}-tx-{signature[:8]}.json"
            if args.retry_errors_only and (snapshot / filename).exists() and not is_error_file(snapshot / filename):
                fetched.append(filename)
                continue
            tx = rpc_with_retries(args.endpoint, "getTransaction", params, args.timeout, args.pause, args.retries)
            save(snapshot / filename, tx)
            fetched.append(filename)
            delta = lamport_delta(tx.get("result") or {}, submitter)
            if delta is not None and delta > 0:
                positive_delta_files.append(filename)
                if len(positive_delta_files) >= args.stop_after_positive:
                    break
            time.sleep(args.pause)

        manifest["submitters"].append(
            {
                "address": submitter,
                "before": before,
                "signature_file": signature_file,
                "signature_count": len(signatures),
                "fetched": len(fetched),
                "positive_delta_files": positive_delta_files,
                "transaction_files": fetched,
            }
        )

    save(snapshot / "solana-mainnet-root-submitter-funding-history-manifest.json", manifest)
    print(f"Fetched root submitter funding history for {len(submitters)} submitter(s)")


if __name__ == "__main__":
    main()
