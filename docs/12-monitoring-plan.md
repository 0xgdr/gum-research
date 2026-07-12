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
