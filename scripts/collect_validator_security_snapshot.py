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
SOLANA_ENDPOINT = "https://api.mainnet-beta.solana.com"
ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
JUP_MINT = "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN"
GUM_PROGRAM = "brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1"
GUM_BANK = "bk1PDAkbHEBGtVRiM94Lzets8gVFP7FgySyfkAc8MPN"
GUM_BANK_PROGRAM = "BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ"
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


def collect_programdata(
    endpoint: str,
    out: Path,
    program_id: str,
    filename_prefix: str,
    timeout: int,
    pause: float,
) -> tuple[str | None, str | None]:
    program = json.loads((out / f"getAccountInfo-{filename_prefix}Program.json").read_text())
    program_value = (program.get("result") or {}).get("value")
    if not program_value or not isinstance(program_value.get("data"), list):
        return None, None

    import base64
    import struct

    raw = base64.b64decode(program_value["data"][0])
    if len(raw) < 36 or struct.unpack("<I", raw[:4])[0] != 2:
        return None, None

    programdata = b58encode(raw[4:36])
    params = [programdata, {"encoding": "base64"}]
    full_programdata_response = rpc(endpoint, "getAccountInfo", params, timeout)
    save(out / f"solana-mainnet-getAccountInfo-{output_prefix}ProgramData-full.json", full_programdata_response)
    time.sleep(pause)

    params = [programdata, {"encoding": "base64", "dataSlice": {"offset": 0, "length": 48}}]
    programdata_response = rpc(endpoint, "getAccountInfo", params, timeout)
    save(out / f"getAccountInfo-{filename_prefix}ProgramData-slice48.json", programdata_response)
    time.sleep(pause)

    programdata_value = (programdata_response.get("result") or {}).get("value")
    if not programdata_value or not isinstance(programdata_value.get("data"), list):
        return programdata, None

    header = base64.b64decode(programdata_value["data"][0])
    if len(header) < 45 or struct.unpack("<I", header[:4])[0] != 3 or header[12] != 1:
        return programdata, None

    authority = b58encode(header[13:45])
    params = [authority, {"encoding": "base64"}]
    save(out / f"getAccountInfo-{filename_prefix}UpgradeAuthority.json", rpc(endpoint, "getAccountInfo", params, timeout))
    time.sleep(pause)
    return programdata, authority


def collect_programdata_from_account_file(
    endpoint: str,
    out: Path,
    account_filename: str,
    output_prefix: str,
    timeout: int,
    pause: float,
) -> tuple[str | None, str | None]:
    program = json.loads((out / account_filename).read_text())
    program_value = (program.get("result") or {}).get("value")
    if not program_value or not isinstance(program_value.get("data"), list):
        return None, None

    import base64
    import struct

    raw = base64.b64decode(program_value["data"][0])
    if len(raw) < 36 or struct.unpack("<I", raw[:4])[0] != 2:
        return None, None

    programdata = b58encode(raw[4:36])
    params = [programdata, {"encoding": "base64", "dataSlice": {"offset": 0, "length": 48}}]
    programdata_response = rpc(endpoint, "getAccountInfo", params, timeout)
    save(out / f"solana-mainnet-getAccountInfo-{output_prefix}ProgramData-slice48.json", programdata_response)
    time.sleep(pause)

    programdata_value = (programdata_response.get("result") or {}).get("value")
    if not programdata_value or not isinstance(programdata_value.get("data"), list):
        return programdata, None

    header = base64.b64decode(programdata_value["data"][0])
    if len(header) < 45 or struct.unpack("<I", header[:4])[0] != 3 or header[12] != 1:
        return programdata, None

    authority = b58encode(header[13:45])
    params = [authority, {"encoding": "base64"}]
    save(out / f"solana-mainnet-getAccountInfo-{output_prefix}UpgradeAuthority.json", rpc(endpoint, "getAccountInfo", params, timeout))
    time.sleep(pause)
    return programdata, authority


def collect_solana_bank(args: argparse.Namespace, out: Path) -> None:
    if not args.solana_endpoint:
        return

    calls = [
        (
            "getAccountInfo",
            "solana-mainnet-getAccountInfo-GumBank.json",
            [GUM_BANK, {"encoding": "base64"}],
        ),
        (
            "getAccountInfo",
            "solana-mainnet-getAccountInfo-GumBankProgram.json",
            [GUM_BANK_PROGRAM, {"encoding": "base64"}],
        ),
        (
            "getSignaturesForAddress",
            "solana-mainnet-getSignaturesForAddress-GumBank.json",
            [GUM_BANK, {"limit": args.signature_limit}],
        ),
        (
            "getSignaturesForAddress",
            "solana-mainnet-getSignaturesForAddress-GumBankProgram.json",
            [GUM_BANK_PROGRAM, {"limit": args.signature_limit}],
        ),
    ]
    for method, filename, params in calls:
        try:
            save(out / filename, rpc(args.solana_endpoint, method, params, args.timeout))
        except urllib.error.HTTPError as exc:
            save(out / filename, {"jsonrpc": "2.0", "id": 1, "error": {"message": str(exc)}})
        time.sleep(args.pause)

    for account_filename, output_prefix in [
        ("solana-mainnet-getAccountInfo-GumBank.json", "GumBank"),
        ("solana-mainnet-getAccountInfo-GumBankProgram.json", "GumBankProgram"),
    ]:
        try:
            collect_programdata_from_account_file(
                args.solana_endpoint,
                out,
                account_filename,
                output_prefix,
                args.timeout,
                args.pause,
            )
        except urllib.error.HTTPError as exc:
            save(
                out / f"solana-mainnet-getAccountInfo-{output_prefix}ProgramData-slice48.json",
                {"jsonrpc": "2.0", "id": 1, "error": {"message": str(exc)}},
            )
            time.sleep(args.pause)

    bank_sigs = json.loads((out / "solana-mainnet-getSignaturesForAddress-GumBankProgram.json").read_text()).get("result") or []
    for item in bank_sigs[: args.transaction_limit]:
        sig = item["signature"]
        params = [sig, {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 0}]
        try:
            data = rpc(args.solana_endpoint, "getTransaction", params, args.timeout)
        except urllib.error.HTTPError as exc:
            data = {"jsonrpc": "2.0", "id": 1, "error": {"message": str(exc)}}
        save(out / f"solana-mainnet-bank-tx-{sig[:8]}.json", data)
        time.sleep(args.pause)


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
            "getAccountInfo-GumBank.json",
            [GUM_BANK, {"encoding": "base64"}],
        ),
        (
            "getAccountInfo",
            "getAccountInfo-GumBankProgram.json",
            [GUM_BANK_PROGRAM, {"encoding": "base64"}],
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
            "getSignaturesForAddress",
            "getSignaturesForAddress-GumBank.json",
            [GUM_BANK, {"limit": args.signature_limit}],
        ),
        (
            "getSignaturesForAddress",
            "getSignaturesForAddress-GumBankProgram.json",
            [GUM_BANK_PROGRAM, {"limit": args.signature_limit}],
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

    collect_programdata(args.endpoint, out, GUM_PROGRAM, "Gum", args.timeout, args.pause)
    bank_programdata, _bank_authority = collect_programdata(
        args.endpoint,
        out,
        GUM_BANK_PROGRAM,
        "GumBank",
        args.timeout,
        args.pause,
    )

    bank_program_info = json.loads((out / "getAccountInfo-GumBankProgram.json").read_text())
    bank_program_value = (bank_program_info.get("result") or {}).get("value")
    if bank_program_value:
        try:
            params = [GUM_BANK_PROGRAM, {"encoding": "base64"}]
            save(out / "getProgramAccounts-GumBankProgram.json", rpc(args.endpoint, "getProgramAccounts", params, args.timeout))
            time.sleep(args.pause)
        except urllib.error.HTTPError as exc:
            save(
                out / "getProgramAccounts-GumBankProgram.json",
                {"jsonrpc": "2.0", "id": 1, "error": {"message": str(exc)}},
            )
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

    bank_sigs_path = out / "getSignaturesForAddress-GumBankProgram.json"
    bank_sigs = json.loads(bank_sigs_path.read_text()).get("result") or []
    for item in bank_sigs[: args.transaction_limit]:
        sig = item["signature"]
        params = [sig, {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 0}]
        try:
            data = rpc(args.endpoint, "getTransaction", params, args.timeout)
        except urllib.error.HTTPError as exc:
            data = {"jsonrpc": "2.0", "id": 1, "error": {"message": str(exc)}}
        save(out / f"bank-tx-{sig[:8]}.json", data)
        time.sleep(args.pause)

    collect_solana_bank(args, out)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--endpoint", default=ENDPOINT)
    parser.add_argument("--solana-endpoint", default=SOLANA_ENDPOINT)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--signature-limit", type=int, default=20)
    parser.add_argument("--transaction-limit", type=int, default=8)
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--pause", type=float, default=0.15)
    collect(parser.parse_args())


if __name__ == "__main__":
    main()
