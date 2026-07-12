#!/usr/bin/env python3
"""Collect, analyze, deep-dive, and compare a fresh validator-security snapshot."""

from __future__ import annotations

import argparse
import datetime as dt
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_DIR = ROOT / "evidence"


def run(command: list[str], stdout_path: Path | None = None) -> None:
    if stdout_path:
        with stdout_path.open("w") as handle:
            subprocess.run(command, cwd=ROOT, check=True, stdout=handle)
    else:
        subprocess.run(command, cwd=ROOT, check=True)


def snapshot_dirs() -> list[Path]:
    if not EVIDENCE_DIR.exists():
        return []
    return sorted(path for path in EVIDENCE_DIR.iterdir() if path.is_dir() and path.name.endswith("-live-rpc"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", help="Snapshot directory to create.")
    parser.add_argument("--compare-to", help="Previous snapshot directory. Defaults to latest existing snapshot.")
    parser.add_argument("--signature-limit", type=int, default=20)
    parser.add_argument("--transaction-limit", type=int, default=8)
    args = parser.parse_args()

    existing = snapshot_dirs()
    if args.output_dir:
        out = Path(args.output_dir)
        if not out.is_absolute():
            out = ROOT / out
    else:
        stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d-%H%M")
        out = EVIDENCE_DIR / f"{stamp}-live-rpc"

    if args.compare_to:
        previous = Path(args.compare_to)
        if not previous.is_absolute():
            previous = ROOT / previous
    else:
        previous = existing[-1] if existing else None

    run(
        [
            sys.executable,
            "scripts/collect_validator_security_snapshot.py",
            "--output-dir",
            str(out),
            "--signature-limit",
            str(args.signature_limit),
            "--transaction-limit",
            str(args.transaction_limit),
        ]
    )
    run([sys.executable, "scripts/collect_bank_recurring_accounts.py", str(out)])
    run([sys.executable, "scripts/collect_bank_owner_context.py", str(out)])
    run([sys.executable, "scripts/collect_jupnet_helper_program_accounts.py", str(out)])
    run([sys.executable, "scripts/analyze_validator_security_snapshot.py", str(out)], out / "analysis.md")
    run([sys.executable, "scripts/deep_dive_validator_security_snapshot.py", str(out)], out / "deep-dive.md")
    run([sys.executable, "scripts/analyze_gum_authorization.py", str(out)], out / "authorization.md")
    run([sys.executable, "scripts/classify_gum_utility_surfaces.py", str(out)], out / "utility-classification.md")
    run([sys.executable, "scripts/analyze_solana_bank_surface.py", str(out)], out / "solana-bank.md")
    run([sys.executable, "scripts/reverse_engineer_solana_bank.py", str(out)], out / "bank-reverse-engineering.md")
    run([sys.executable, "scripts/analyze_bank_account_graph.py", str(out)], out / "bank-account-graph.md")
    run([sys.executable, "scripts/analyze_bank_recurring_accounts.py", str(out)], out / "bank-recurring-account-state.md")
    run([sys.executable, "scripts/analyze_bank_owner_context.py", str(out)], out / "bank-owner-program-context.md")
    run([sys.executable, "scripts/analyze_jupnet_helper_program_accounts.py", str(out)], out / "jupnet-helper-program-accounts.md")
    run([sys.executable, "scripts/reconstruct_verify_request_payloads.py", str(out)], out / "verify-request-payload-reconstruction.md")
    if previous:
        run([sys.executable, "scripts/compare_validator_security_snapshots.py", str(previous), str(out)], out / "diff.md")

    print(f"Snapshot: {out}")
    print(f"Analysis: {out / 'analysis.md'}")
    print(f"Deep dive: {out / 'deep-dive.md'}")
    print(f"Authorization: {out / 'authorization.md'}")
    print(f"Utility classification: {out / 'utility-classification.md'}")
    print(f"Solana Bank surface: {out / 'solana-bank.md'}")
    print(f"Bank reverse engineering: {out / 'bank-reverse-engineering.md'}")
    print(f"Bank account graph: {out / 'bank-account-graph.md'}")
    print(f"Bank recurring account state: {out / 'bank-recurring-account-state.md'}")
    print(f"Bank owner program context: {out / 'bank-owner-program-context.md'}")
    print(f"JupNet helper program accounts: {out / 'jupnet-helper-program-accounts.md'}")
    print(f"Verify request payload reconstruction: {out / 'verify-request-payload-reconstruction.md'}")
    if previous:
        print(f"Compared against: {previous}")
        print(f"Diff: {out / 'diff.md'}")
    else:
        print("Compared against: none")


if __name__ == "__main__":
    main()
