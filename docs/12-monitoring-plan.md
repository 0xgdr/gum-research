# Monitoring Plan

Use this workflow to check whether new public evidence appears for JUP protocol utility. Trading support is treated as noise unless it connects to staking, signer weights, quorum, fees, governance, access control, slashing, rewards or permanent protocol burns/sinks.

## One-Command Check

Run:

```bash
python3 scripts/run_validator_security_check.py
```

The script creates a new directory under:

```text
evidence/YYYY-MM-DD-HHMM-live-rpc/
```

It writes:

- `analysis.md`
- `deep-dive.md`
- `authorization.md`
- `utility-classification.md`
- `solana-bank.md`
- `bank-reverse-engineering.md`
- `bank-account-graph.md`
- `bank-recurring-account-state.md`
- `bank-owner-program-context.md`
- `jupnet-helper-program-accounts.md`
- `verify-request-payload-reconstruction.md`
- `outbox-root-update-transactions.md`
- `outbox-update-payload-reconstruction.md`
- `diff.md` when a previous snapshot exists

## Manual Workflow

Collect a snapshot:

```bash
python3 scripts/collect_validator_security_snapshot.py \
  --output-dir evidence/YYYY-MM-DD-HHMM-live-rpc
```

Generate analysis:

```bash
python3 scripts/analyze_validator_security_snapshot.py \
  evidence/YYYY-MM-DD-HHMM-live-rpc \
  > evidence/YYYY-MM-DD-HHMM-live-rpc/analysis.md
```

Generate deep-dive output:

```bash
python3 scripts/deep_dive_validator_security_snapshot.py \
  evidence/YYYY-MM-DD-HHMM-live-rpc \
  > evidence/YYYY-MM-DD-HHMM-live-rpc/deep-dive.md
```

Generate Gum authorization output:

```bash
python3 scripts/analyze_gum_authorization.py \
  evidence/YYYY-MM-DD-HHMM-live-rpc \
  > evidence/YYYY-MM-DD-HHMM-live-rpc/authorization.md
```

Generate utility classification output:

```bash
python3 scripts/classify_gum_utility_surfaces.py \
  evidence/YYYY-MM-DD-HHMM-live-rpc \
  > evidence/YYYY-MM-DD-HHMM-live-rpc/utility-classification.md
```

Generate Solana Bank surface output:

```bash
python3 scripts/analyze_solana_bank_surface.py \
  evidence/YYYY-MM-DD-HHMM-live-rpc \
  > evidence/YYYY-MM-DD-HHMM-live-rpc/solana-bank.md
```

Generate Bank reverse-engineering output:

```bash
python3 scripts/reverse_engineer_solana_bank.py \
  evidence/YYYY-MM-DD-HHMM-live-rpc \
  > evidence/YYYY-MM-DD-HHMM-live-rpc/bank-reverse-engineering.md
```

Generate Bank account-graph and PDA-hunt output:

```bash
python3 scripts/analyze_bank_account_graph.py \
  evidence/YYYY-MM-DD-HHMM-live-rpc \
  > evidence/YYYY-MM-DD-HHMM-live-rpc/bank-account-graph.md
```

Fetch and analyze recurring Bank account state:

```bash
python3 scripts/collect_bank_recurring_accounts.py \
  evidence/YYYY-MM-DD-HHMM-live-rpc

python3 scripts/analyze_bank_recurring_accounts.py \
  evidence/YYYY-MM-DD-HHMM-live-rpc \
  > evidence/YYYY-MM-DD-HHMM-live-rpc/bank-recurring-account-state.md
```

Fetch and analyze Bank owner-program context:

```bash
python3 scripts/collect_bank_owner_context.py \
  evidence/YYYY-MM-DD-HHMM-live-rpc

python3 scripts/analyze_bank_owner_context.py \
  evidence/YYYY-MM-DD-HHMM-live-rpc \
  > evidence/YYYY-MM-DD-HHMM-live-rpc/bank-owner-program-context.md
```

Fetch and analyze JupNet helper-program-owned accounts:

```bash
python3 scripts/collect_jupnet_helper_program_accounts.py \
  evidence/YYYY-MM-DD-HHMM-live-rpc

python3 scripts/analyze_jupnet_helper_program_accounts.py \
  evidence/YYYY-MM-DD-HHMM-live-rpc \
  > evidence/YYYY-MM-DD-HHMM-live-rpc/jupnet-helper-program-accounts.md
```

Reconstruct sampled `verify_request` payloads:

```bash
python3 scripts/reconstruct_verify_request_payloads.py \
  evidence/YYYY-MM-DD-HHMM-live-rpc \
  > evidence/YYYY-MM-DD-HHMM-live-rpc/verify-request-payload-reconstruction.md
```

Collect and analyze outbox root-update transactions:

```bash
python3 scripts/collect_outbox_root_update_transactions.py \
  evidence/YYYY-MM-DD-HHMM-live-rpc

python3 scripts/analyze_outbox_root_update_transactions.py \
  evidence/YYYY-MM-DD-HHMM-live-rpc \
  > evidence/YYYY-MM-DD-HHMM-live-rpc/outbox-root-update-transactions.md
```

Reconstruct outbox update payload proofs:

```bash
python3 scripts/reconstruct_outbox_update_payload.py \
  evidence/YYYY-MM-DD-HHMM-live-rpc \
  > evidence/YYYY-MM-DD-HHMM-live-rpc/outbox-update-payload-reconstruction.md
```

Compare two snapshots:

```bash
python3 scripts/compare_validator_security_snapshots.py \
  evidence/OLD-live-rpc \
  evidence/NEW-live-rpc \
  > evidence/NEW-live-rpc/diff.md
```

## Alert Conditions

Treat these as high-value changes:

- canonical JUP mint appears as a JupNet account;
- JupNet SPL token accounts appear for canonical JUP;
- Gum or OpenID account data starts containing raw canonical JUP pubkey bytes;
- Gum or OpenID account data starts containing current validator, vote or stake account keys;
- JUP appears in fee, reward, slashing, governance, access-control or permanent burn/sink accounts;
- Gum ProgramData account changes;
- Gum deployment slot changes;
- Gum upgrade authority changes;
- public `jup-ag/platform-list` GUM bank addresses or services change;
- Solana Bank or Bank Program account info, ProgramData or upgrade authority changes;
- Solana Bank Program transactions start touching canonical JUP;
- Solana Bank Program instruction variants or binary string hits change;
- Solana Bank account graph starts exposing canonical JUP-derived PDAs or JUP token accounts;
- Solana Bank PDA matches change for inbox, outbox, Merkle, signer-set or authority seeds;
- recurring Bank account state starts exposing canonical JUP, validator/vote/stake keys, or new Bank-owned state layouts;
- Bank owner helper programs, ProgramData hashes, upgrade authorities, JUP key hits or validator-key hits change;
- JupNet helper-program-owned account counts, Merkle roots, JUP hits or validator-key hits change;
- `verify_request` payloads start exposing canonical JUP, validator/vote/stake keys, different proof shape, signer-set, quorum or BLS material;
- outbox root-update transactions start exposing canonical JUP, validator/vote/stake keys, signer-set, quorum, weight or fee material;
- outbox update payload reconstruction stops matching the `0x00` leaf / `0x01` parent Merkle formula, changes aggregate-key material length, or adds new labelled Dove/JUP/stake fields;
- Solana Bank Program logs add validator, quorum, stake, signer, BLS or JUP fee/sink terms;
- current validator set, vote accounts or stake accounts change;
- sampled Gum transactions start containing current validator, vote or stake account keys;
- new Gum signatures appear after the existing May 2026 signature window.

Do not alert on JUP trading or asset metadata alone.

## How To Ask For A Check

Ask:

```text
Run the validator security monitor.
```

The expected action is to run `scripts/run_validator_security_check.py`, inspect the generated `diff.md`, and summarize only meaningful alerts.
