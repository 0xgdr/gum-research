#!/usr/bin/env python3
"""Collect a bounded JupNet RPC snapshot for validator-security research."""

from __future__ import annotations

import argparse
import json
import time
import urllib.error
import urllib.request
from pathlib import Path


ENDPOINT = "https://mainnet-beta-rpc.jup.net/"
ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
JUP_MINT = "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN"
GUM_PROGRAM = "brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1"
OPENID_REGISTRY = "Jupnetopen1DRegistry11111111111111111111111"
STAKE_PROGRAM = "Stake11111111111111111111111111111111111111"
NATIVE_LOADER = "NativeLoader1111111111111111111111111111111"
TOKEN_PROGRAM = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
BPF_UPGRADEABLE_LOADER = "BPFLoaderUpgradeab1e11111111111111111111111"
BPF_LEGACY_LOADER = "BPFLoader2111111111111111111111111111111111"
REPEATED_GUM_PATH_ACCOUNTS = [
    "ESUtymMEp6NULmLBcREaumM87TRpgt5R4eNYVrKjCKQq",
    "76WKTLzujFUnj7TyB7CqLywPE3YZQf4Fmxj9SwcFAJrY",
    "Hso4y8rKEXUUvMbxnyDmjCxA7yk1wbVsZNHSGXcDEUyU",
    "GZF3sfYF27BU83fd5BPgB419SZiLLZPty3qL6465JTp6",
    "Fh54LKACZCzo3GzDcxoPQomTZamBsFy6XLbj15zJP1WH",
    "A5ER4hbDN82jEnf986kZzuJzMzsyw1DRqodnone5yJWo",
    "94oZZEp1p1Vwuvc7axgeaRSU4Mk9diugqzjxpz1dnSZv",
    "FCNefQTEYCsPyQA64hdCpekucCDJFPHm2qfwg8F61jgc",
]


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
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as res:
        return json.loads(res.read().decode())


def save(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def collect(args: argparse.Namespace) -> None:
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)

    calls = [
        ("getSlot", "getSlot.json", None),
        ("getIdentity", "getIdentity.json", None),
        ("getEpochInfo", "getEpochInfo.json", None),
        ("getClusterNodes", "getClusterNodes.json", None),
        ("getVoteAccounts", "getVoteAccounts.json", None),
        (
            "getProgramAccounts",
            "getProgramAccounts-Stake.json",
            [STAKE_PROGRAM, {"encoding": "jsonParsed"}],
        ),
        (
            "getProgramAccounts",
            "getProgramAccounts-OpenIDRegistry.json",
            [OPENID_REGISTRY, {"encoding": "base64"}],
        ),
        (
            "getProgramAccounts",
            "getProgramAccounts-Gum.json",
            [GUM_PROGRAM, {"encoding": "base64"}],
        ),
        (
            "getProgramAccounts",
            "getProgramAccounts-NativeLoader.json",
            [NATIVE_LOADER, {"encoding": "base64"}],
        ),
        (
            "getProgramAccounts",
            "getProgramAccounts-UpgradeableLoader-slice48.json",
            [BPF_UPGRADEABLE_LOADER, {"encoding": "base64", "dataSlice": {"offset": 0, "length": 48}}],
        ),
        (
            "getProgramAccounts",
            "getProgramAccounts-LegacyBPFLoader-slice40.json",
            [BPF_LEGACY_LOADER, {"encoding": "base64", "dataSlice": {"offset": 0, "length": 40}}],
        ),
        (
            "getAccountInfo",
            "getAccountInfo-GumProgram.json",
            [GUM_PROGRAM, {"encoding": "base64"}],
        ),
        (
            "getAccountInfo",
            "getAccountInfo-JUPMint.json",
            [JUP_MINT, {"encoding": "jsonParsed"}],
        ),
        (
            "getProgramAccounts",
            "getProgramAccounts-Token-JUPMint.json",
            [
                TOKEN_PROGRAM,
                {
                    "encoding": "jsonParsed",
                    "filters": [{"memcmp": {"offset": 0, "bytes": JUP_MINT}}],
                },
            ],
        ),
        (
            "getSignaturesForAddress",
            "getSignaturesForAddress-Gum.json",
            [GUM_PROGRAM, {"limit": args.signature_limit}],
        ),
        (
            "getMultipleAccounts",
            "getMultipleAccounts-RepeatedGumPathAccounts.json",
            [REPEATED_GUM_PATH_ACCOUNTS, {"encoding": "base64"}],
        ),
    ]

    for method, filename, params in calls:
        save(out / filename, rpc(args.endpoint, method, params, args.timeout))
        time.sleep(args.pause)

    gum_program = json.loads((out / "getAccountInfo-GumProgram.json").read_text())
    gum_value = (gum_program.get("result") or {}).get("value")
    if gum_value and isinstance(gum_value.get("data"), list):
        import base64
        import struct

        raw = base64.b64decode(gum_value["data"][0])
        if len(raw) >= 36 and struct.unpack("<I", raw[:4])[0] == 2:
            programdata = b58encode(raw[4:36])
            params = [programdata, {"encoding": "base64", "dataSlice": {"offset": 0, "length": 48}}]
            programdata_response = rpc(args.endpoint, "getAccountInfo", params, args.timeout)
            save(out / "getAccountInfo-GumProgramData-slice48.json", programdata_response)
            time.sleep(args.pause)
            programdata_value = (programdata_response.get("result") or {}).get("value")
            if programdata_value and isinstance(programdata_value.get("data"), list):
                header = base64.b64decode(programdata_value["data"][0])
                if len(header) >= 45 and struct.unpack("<I", header[:4])[0] == 3 and header[12] == 1:
                    authority = b58encode(header[13:45])
                    params = [authority, {"encoding": "base64"}]
                    save(out / "getAccountInfo-GumUpgradeAuthority.json", rpc(args.endpoint, "getAccountInfo", params, args.timeout))
                    time.sleep(args.pause)

    sigs_path = out / "getSignaturesForAddress-Gum.json"
    sigs = json.loads(sigs_path.read_text()).get("result") or []
    for item in sigs[: args.transaction_limit]:
        sig = item["signature"]
        params = [sig, {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 0}]
        try:
            data = rpc(args.endpoint, "getTransaction", params, args.timeout)
        except urllib.error.HTTPError as exc:
            data = {"jsonrpc": "2.0", "id": 1, "error": {"message": str(exc)}}
        save(out / f"tx-{sig[:8]}.json", data)
        time.sleep(args.pause)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--endpoint", default=ENDPOINT)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--signature-limit", type=int, default=20)
    parser.add_argument("--transaction-limit", type=int, default=8)
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--pause", type=float, default=0.15)
    collect(parser.parse_args())


if __name__ == "__main__":
    main()
