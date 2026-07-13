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
    parser.add_argument("--funding-signature-limit", type=int, default=300)
    parser.add_argument("--funding-transaction-limit", type=int, default=300)
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
    run([sys.executable, "scripts/collect_outbox_root_update_transactions.py", str(out)])
    run([sys.executable, "scripts/collect_outbox_root_history.py", str(out)])
    run([sys.executable, "scripts/collect_gum_omnichain_sender_program.py", str(out)])
    run([sys.executable, "scripts/collect_jupnet_executable_census.py", str(out)])
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
    run([sys.executable, "scripts/analyze_outbox_root_update_transactions.py", str(out)], out / "outbox-root-update-transactions.md")
    run([sys.executable, "scripts/reconstruct_outbox_update_payload.py", str(out)], out / "outbox-update-payload-reconstruction.md")
    run([sys.executable, "scripts/analyze_outbox_root_history.py", str(out)], out / "outbox-root-history.md")
    run([sys.executable, "scripts/analyze_root_update_authority_graph.py", str(out)], out / "root-update-authority-graph.md")
    run(
        [
            sys.executable,
            "scripts/collect_root_submitter_history.py",
            str(out),
            "--signature-limit",
            str(args.signature_limit),
            "--transaction-limit",
            str(args.transaction_limit),
        ]
    )
    run([sys.executable, "scripts/analyze_root_submitter_provenance.py", str(out)], out / "root-submitter-provenance.md")
    run([sys.executable, "scripts/analyze_root_submitter_history.py", str(out)], out / "root-submitter-history.md")
    run(
        [
            sys.executable,
            "scripts/collect_root_submitter_funding_history.py",
            str(out),
            "--signature-limit",
            str(args.funding_signature_limit),
            "--transaction-limit",
            str(args.funding_transaction_limit),
            "--stop-after-positive",
            "1",
            "--pause",
            "0.35",
            "--retries",
            "6",
        ]
    )
    run([sys.executable, "scripts/analyze_root_submitter_funding_history.py", str(out)], out / "root-submitter-funding-history.md")
    run(
        [
            sys.executable,
            "scripts/collect_funding_actor_context.py",
            str(out),
            "--signature-limit",
            "20",
            "--signature-role",
            "fee payer",
            "--signature-role",
            "root submitter",
            "--signature-role",
            "parsed transfer source into root submitter",
            "--signature-role",
            "non-standard funding event program",
            "--pause",
            "0.35",
            "--retries",
            "4",
        ]
    )
    run([sys.executable, "scripts/analyze_funding_actor_classifier.py", str(out)], out / "funding-actor-classifier.md")
    run([sys.executable, "scripts/hunt_epoch_security_sources.py", str(out)], out / "epoch-security-source-hunt.md")
    run([sys.executable, "scripts/map_outbox_verifier_payloads.py", str(out)], out / "outbox-verifier-payload-field-map.md")
    run([sys.executable, "scripts/analyze_security_boundary_corpus.py", str(out)], out / "security-boundary-corpus.md")
    run([sys.executable, "scripts/analyze_private_runtime_fingerprints.py", str(out)], out / "private-runtime-fingerprints.md")
    run([sys.executable, "scripts/analyze_gum_omnichain_binary_roles.py", str(out)], out / "gum-omnichain-binary-roles.md")
    run([sys.executable, "scripts/analyze_gum_account_role_reconstruction.py", str(out)], out / "gum-account-role-reconstruction.md")
    run([sys.executable, "scripts/analyze_gum_omnichain_sender_program.py", str(out)], out / "gum-omnichain-sender-program.md")
    run([sys.executable, "scripts/analyze_jupnet_executable_census.py", str(out)], out / "jupnet-executable-census.md")
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
    print(f"Outbox root update transactions: {out / 'outbox-root-update-transactions.md'}")
    print(f"Outbox update payload reconstruction: {out / 'outbox-update-payload-reconstruction.md'}")
    print(f"Outbox root history: {out / 'outbox-root-history.md'}")
    print(f"Root update authority graph: {out / 'root-update-authority-graph.md'}")
    print(f"Root submitter provenance: {out / 'root-submitter-provenance.md'}")
    print(f"Root submitter direct history: {out / 'root-submitter-history.md'}")
    print(f"Root submitter funding history: {out / 'root-submitter-funding-history.md'}")
    print(f"Funding actor classifier: {out / 'funding-actor-classifier.md'}")
    print(f"Epoch security source hunt: {out / 'epoch-security-source-hunt.md'}")
    print(f"Outbox verifier payload field map: {out / 'outbox-verifier-payload-field-map.md'}")
    print(f"Security boundary corpus: {out / 'security-boundary-corpus.md'}")
    print(f"Private runtime fingerprints: {out / 'private-runtime-fingerprints.md'}")
    print(f"Gum omnichain binary roles: {out / 'gum-omnichain-binary-roles.md'}")
    print(f"Gum account role reconstruction: {out / 'gum-account-role-reconstruction.md'}")
    print(f"Gum omnichain sender program: {out / 'gum-omnichain-sender-program.md'}")
    print(f"JupNet executable census: {out / 'jupnet-executable-census.md'}")
    if previous:
        print(f"Compared against: {previous}")
        print(f"Diff: {out / 'diff.md'}")
    else:
        print("Compared against: none")


if __name__ == "__main__":
    main()
