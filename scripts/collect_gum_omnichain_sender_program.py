#!/usr/bin/env python3
"""Collect the JupNet Gum omnichain sender program and ProgramData accounts."""

from __future__ import annotations

import argparse
import json
import urllib.request
from pathlib import Path


ENDPOINT = "https://mainnet-beta-rpc.jup.net/"
GUM_OMNICHAIN_PROGRAM = "GUMebNDCYyF81xjyqaHagbgMQVUTb8fBC9YRh25xSH64"
GUM_OMNICHAIN_PROGRAMDATA = "Gi8HgbHnykRiHboqG2VHysti773o8bNSjuFJWpyf4Q89"


def rpc(endpoint: str, method: str, params: list, timeout: int) -> dict:
    body = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params}
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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot_dir")
    parser.add_argument("--endpoint", default=ENDPOINT)
    parser.add_argument("--timeout", type=int, default=30)
    args = parser.parse_args()
    base = Path(args.snapshot_dir)
    base.mkdir(parents=True, exist_ok=True)

    save(
        base / "getAccountInfo-GUMebProgram.json",
        rpc(args.endpoint, "getAccountInfo", [GUM_OMNICHAIN_PROGRAM, {"encoding": "base64"}], args.timeout),
    )
    save(
        base / "getAccountInfo-GUMebProgramData-full.json",
        rpc(args.endpoint, "getAccountInfo", [GUM_OMNICHAIN_PROGRAMDATA, {"encoding": "base64"}], args.timeout),
    )


if __name__ == "__main__":
    main()
