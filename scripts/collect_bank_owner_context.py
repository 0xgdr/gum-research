#!/usr/bin/env python3
"""Collect owner/program context for non-token recurring GUM Bank accounts."""

from __future__ import annotations

import argparse
import base64
import json
import struct
import time
import urllib.error
import urllib.request
from pathlib import Path


SOLANA_ENDPOINT = "https://api.mainnet-beta.solana.com"
ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
BPF_UPGRADEABLE_LOADER = "BPFLoaderUpgradeab1e11111111111111111111111"
SYSTEM_PROGRAM = "11111111111111111111111111111111"
SPL_TOKEN = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
BANK_PROGRAM = "BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ"
METAPLEX_TOKEN_METADATA = "metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s"

EXTRA_TARGETS = {
    "JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw",
    "jnoUtncGR9ZCCMixtys6Gzy5coTo6mnmUZuEHRQFTFV",
    "5Tv692BDJinbjR6Beb2K9bGmxnbQeFaGb1rJqCs2y3Q6",
}


def b58encode(data: bytes) -> str:
    number = int.from_bytes(data, "big")
    out = ""
    while number:
        number, rem = divmod(number, 58)
        out = ALPHABET[rem] + out
    return ("1" * (len(data) - len(data.lstrip(b"\0")))) + (out or "")


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


def raw_account_data(value: dict | None) -> bytes:
    if not value:
        return b""
    data = value.get("data")
    if isinstance(data, list):
        return base64.b64decode(data[0])
    return b""


def programdata_address(value: dict | None) -> str | None:
    raw = raw_account_data(value)
    if len(raw) >= 36 and struct.unpack("<I", raw[:4])[0] == 2:
        return b58encode(raw[4:36])
    return None


def recurring_targets(snapshot: Path) -> set[str]:
    data = load(snapshot / "solana-mainnet-getMultipleAccounts-BankRecurringAccounts.json")
    accounts = data.get("accounts") or []
    values = ((data.get("response") or {}).get("result") or {}).get("value") or []
    targets = set(EXTRA_TARGETS)
    ignored_owners = {
        SYSTEM_PROGRAM,
        SPL_TOKEN,
        BANK_PROGRAM,
        METAPLEX_TOKEN_METADATA,
        BPF_UPGRADEABLE_LOADER,
        None,
    }
    for account, value in zip(accounts, values):
        if not value:
            targets.add(account)
            continue
        owner = value.get("owner")
        if owner not in ignored_owners:
            targets.add(owner)
            targets.add(account)
        if owner == BPF_UPGRADEABLE_LOADER:
            targets.add(account)
    return targets


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot_dir")
    parser.add_argument("--endpoint", default=SOLANA_ENDPOINT)
    parser.add_argument("--signature-limit", type=int, default=20)
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--pause", type=float, default=0.15)
    args = parser.parse_args()

    snapshot = Path(args.snapshot_dir)
    targets = sorted(recurring_targets(snapshot))
    account_response = rpc(args.endpoint, "getMultipleAccounts", [targets, {"encoding": "base64"}], args.timeout)
    save(
        snapshot / "solana-mainnet-getMultipleAccounts-BankOwnerContext.json",
        {"accounts": targets, "response": account_response},
    )
    time.sleep(args.pause)

    values = (account_response.get("result") or {}).get("value") or []
    programdata_targets = {}
    for account, value in zip(targets, values):
        pda = programdata_address(value)
        if pda:
            programdata_targets[account] = pda

    for program, programdata in programdata_targets.items():
        try:
            save(
                snapshot / f"solana-mainnet-getAccountInfo-OwnerProgramData-{program[:8]}.json",
                rpc(args.endpoint, "getAccountInfo", [programdata, {"encoding": "base64"}], args.timeout),
            )
        except urllib.error.HTTPError as exc:
            save(
                snapshot / f"solana-mainnet-getAccountInfo-OwnerProgramData-{program[:8]}.json",
                {"jsonrpc": "2.0", "id": 1, "error": {"message": str(exc)}},
            )
        time.sleep(args.pause)

    signatures = {}
    for account in targets:
        try:
            signatures[account] = rpc(
                args.endpoint,
                "getSignaturesForAddress",
                [account, {"limit": args.signature_limit}],
                args.timeout,
            )
        except urllib.error.HTTPError as exc:
            signatures[account] = {"jsonrpc": "2.0", "id": 1, "error": {"message": str(exc)}}
        time.sleep(args.pause)
    save(snapshot / "solana-mainnet-getSignaturesForAddress-BankOwnerContext.json", signatures)
    print(f"Fetched owner context for {len(targets)} accounts and {len(programdata_targets)} programdata accounts")


if __name__ == "__main__":
    main()
