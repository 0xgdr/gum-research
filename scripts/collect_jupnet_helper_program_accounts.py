#!/usr/bin/env python3
"""Collect accounts owned by inferred Solana-side JupNet inbox/outbox helper programs."""

from __future__ import annotations

import argparse
import json
import time
import urllib.error
import urllib.request
from pathlib import Path


SOLANA_ENDPOINT = "https://api.mainnet-beta.solana.com"
INBOX_PROGRAM = "JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw"
OUTBOX_PROGRAM = "jnoUtncGR9ZCCMixtys6Gzy5coTo6mnmUZuEHRQFTFV"


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


def save(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def collect_program_accounts(endpoint: str, out: Path, label: str, program: str, timeout: int, pause: float) -> None:
    try:
        response = rpc(endpoint, "getProgramAccounts", [program, {"encoding": "base64"}], timeout)
    except urllib.error.HTTPError as exc:
        response = {"jsonrpc": "2.0", "id": 1, "error": {"message": str(exc)}}
    save(out / f"solana-mainnet-getProgramAccounts-{label}.json", response)
    time.sleep(pause)

    try:
        sigs = rpc(endpoint, "getSignaturesForAddress", [program, {"limit": 20}], timeout)
    except urllib.error.HTTPError as exc:
        sigs = {"jsonrpc": "2.0", "id": 1, "error": {"message": str(exc)}}
    save(out / f"solana-mainnet-getSignaturesForAddress-{label}.json", sigs)
    time.sleep(pause)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot_dir")
    parser.add_argument("--endpoint", default=SOLANA_ENDPOINT)
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--pause", type=float, default=0.15)
    args = parser.parse_args()

    out = Path(args.snapshot_dir)
    collect_program_accounts(args.endpoint, out, "JupNetInboxProgram", INBOX_PROGRAM, args.timeout, args.pause)
    collect_program_accounts(args.endpoint, out, "JupNetOutboxProgram", OUTBOX_PROGRAM, args.timeout, args.pause)
    print("Fetched JupNet inbox/outbox helper program accounts")


if __name__ == "__main__":
    main()
