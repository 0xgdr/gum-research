#!/usr/bin/env python3
"""Collect full ProgramData accounts for all JupNet upgradeable executables."""

from __future__ import annotations

import argparse
import base64
import json
import struct
import time
import urllib.error
import urllib.request
from pathlib import Path


ENDPOINT = "https://mainnet-beta-rpc.jup.net/"
UPGRADEABLE_SCAN = "getProgramAccounts-UpgradeableLoader-slice48.json"
ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def b58encode(data: bytes) -> str:
    number = int.from_bytes(data, "big")
    out = ""
    while number:
        number, rem = divmod(number, 58)
        out = ALPHABET[rem] + out
    return ("1" * (len(data) - len(data.lstrip(b"\0")))) + (out or "")


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


def program_rows(snapshot: Path) -> list[dict]:
    data = json.loads((snapshot / UPGRADEABLE_SCAN).read_text())
    rows = []
    for item in data.get("result") or []:
        account_data = item.get("account", {}).get("data")
        if not isinstance(account_data, list):
            continue
        raw = base64.b64decode(account_data[0])
        if len(raw) < 36 or struct.unpack("<I", raw[:4])[0] != 2:
            continue
        rows.append(
            {
                "program": item["pubkey"],
                "programdata": b58encode(raw[4:36]),
                "program_space": item.get("account", {}).get("space"),
            }
        )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot_dir")
    parser.add_argument("--endpoint", default=ENDPOINT)
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--pause", type=float, default=0.15)
    args = parser.parse_args()

    snapshot = Path(args.snapshot_dir)
    rows = program_rows(snapshot)
    manifest = []
    for row in rows:
        filename = f"jupnet-programdata-{row['program'][:8]}.json"
        try:
            response = rpc(args.endpoint, "getAccountInfo", [row["programdata"], {"encoding": "base64"}], args.timeout)
        except urllib.error.HTTPError as exc:
            response = {"jsonrpc": "2.0", "id": 1, "error": {"message": str(exc)}}
        save(snapshot / filename, response)
        manifest.append({**row, "programdata_file": filename})
        time.sleep(args.pause)

    save(
        snapshot / "jupnet-executable-census-manifest.json",
        {"program_count": len(rows), "programs": manifest},
    )
    print(f"Fetched ProgramData for {len(rows)} JupNet programs")


if __name__ == "__main__":
    main()
