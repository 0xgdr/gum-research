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
- `outbox-root-history.md`
- `root-update-authority-graph.md`
- `root-submitter-provenance.md`
- `root-submitter-history.md`
- `epoch-security-source-hunt.md`
- `outbox-verifier-payload-field-map.md`
- `security-boundary-corpus.md`
- `private-runtime-fingerprints.md`
- `gum-omnichain-binary-roles.md`
- `gum-account-role-reconstruction.md`
- `gum-omnichain-sender-program.md`
- `jupnet-executable-census.md`
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

Collect and analyze a wider outbox root history:

```bash
python3 scripts/collect_outbox_root_history.py \
  evidence/YYYY-MM-DD-HHMM-live-rpc

python3 scripts/analyze_outbox_root_history.py \
  evidence/YYYY-MM-DD-HHMM-live-rpc \
  > evidence/YYYY-MM-DD-HHMM-live-rpc/outbox-root-history.md
```

Build the root-update authority graph:

```bash
python3 scripts/analyze_root_update_authority_graph.py \
  evidence/YYYY-MM-DD-HHMM-live-rpc \
  > evidence/YYYY-MM-DD-HHMM-live-rpc/root-update-authority-graph.md
```

Trace root-update submitters through the saved corpus:

```bash
python3 scripts/collect_root_submitter_history.py \
  evidence/YYYY-MM-DD-HHMM-live-rpc

python3 scripts/analyze_root_submitter_provenance.py \
  evidence/YYYY-MM-DD-HHMM-live-rpc \
  > evidence/YYYY-MM-DD-HHMM-live-rpc/root-submitter-provenance.md

python3 scripts/analyze_root_submitter_history.py \
  evidence/YYYY-MM-DD-HHMM-live-rpc \
  > evidence/YYYY-MM-DD-HHMM-live-rpc/root-submitter-history.md
```

Hunt for epoch security source material:

```bash
python3 scripts/hunt_epoch_security_sources.py \
  evidence/YYYY-MM-DD-HHMM-live-rpc \
  > evidence/YYYY-MM-DD-HHMM-live-rpc/epoch-security-source-hunt.md
```

Map outbox verifier payload fields:

```bash
python3 scripts/map_outbox_verifier_payloads.py \
  evidence/YYYY-MM-DD-HHMM-live-rpc \
  > evidence/YYYY-MM-DD-HHMM-live-rpc/outbox-verifier-payload-field-map.md
```

Analyze the helper-account and verifier-payload security boundary corpus:

```bash
python3 scripts/analyze_security_boundary_corpus.py \
  evidence/YYYY-MM-DD-HHMM-live-rpc \
  > evidence/YYYY-MM-DD-HHMM-live-rpc/security-boundary-corpus.md
```

Hunt for private runtime fingerprints in saved artifacts:

```bash
python3 scripts/analyze_private_runtime_fingerprints.py \
  evidence/YYYY-MM-DD-HHMM-live-rpc \
  > evidence/YYYY-MM-DD-HHMM-live-rpc/private-runtime-fingerprints.md
```

Compare Gum omnichain binary roles:

```bash
python3 scripts/analyze_gum_omnichain_binary_roles.py \
  evidence/YYYY-MM-DD-HHMM-live-rpc \
  > evidence/YYYY-MM-DD-HHMM-live-rpc/gum-omnichain-binary-roles.md
```

Reconstruct Gum and Bank account roles:

```bash
python3 scripts/analyze_gum_account_role_reconstruction.py \
  evidence/YYYY-MM-DD-HHMM-live-rpc \
  > evidence/YYYY-MM-DD-HHMM-live-rpc/gum-account-role-reconstruction.md
```

Collect and analyze the recovered Gum omnichain sender program:

```bash
python3 scripts/collect_gum_omnichain_sender_program.py \
  evidence/YYYY-MM-DD-HHMM-live-rpc

python3 scripts/analyze_gum_omnichain_sender_program.py \
  evidence/YYYY-MM-DD-HHMM-live-rpc \
  > evidence/YYYY-MM-DD-HHMM-live-rpc/gum-omnichain-sender-program.md
```

Collect and analyze all visible JupNet upgradeable executables:

```bash
python3 scripts/collect_jupnet_executable_census.py \
  evidence/YYYY-MM-DD-HHMM-live-rpc

python3 scripts/analyze_jupnet_executable_census.py \
  evidence/YYYY-MM-DD-HHMM-live-rpc \
  > evidence/YYYY-MM-DD-HHMM-live-rpc/jupnet-executable-census.md
```

Compare two snapshots:

```bash
python3 scripts/compare_validator_security_snapshots.py \
  evidence/OLD-live-rpc \
  evidence/NEW-live-rpc \
  > evidence/NEW-live-rpc/diff.md
```

The diff now promotes the proof-chain surfaces into alerts: outbox root-history roots, aggregate keys, compact verifier fields, root-update signers, root-update writable accounts, root-submitter provenance changes, root-submitter direct-history changes, root-submitter funding-history changes, verifier aggregate-key sets, sender/program ids, verifier payload layouts, JupNet executable hashes, upgrade authorities, `sol_verify_bls_merkle_key` consumers and executable key-hit rows.

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
- outbox root-history analysis observes root-update root/key changes, new proof shapes, or any canonical JUP / validator / vote / stake key material;
- root-update authority graph finds a new root-update signer, new writable root-update account, upgrade-authority overlap, or canonical JUP / validator / vote / stake key intersection;
- root-submitter provenance shows the root submitter appearing in non-root Gum/Bank flows, touching canonical JUP / validator / vote / stake keys, matching upgrade authorities, or showing token-balance movement tied to utility/security flows;
- root-submitter direct history shows a new invoked program, positive funding delta, token-balance movement, non-root behavior, or canonical JUP / validator / vote / stake / upgrade-authority intersection;
- root-submitter funding history shows a new funding source, Bank request file, positive funding transaction, token-balance hint, new invoked program, or canonical JUP / validator / vote / stake / upgrade-authority intersection;
- epoch security-source hunting finds candidate aggregate-key or epoch-root material co-located with canonical JUP, validator, vote or stake keys;
- outbox verifier payloads stop matching the mapped field layout, introduce new sender/program ids, or expose canonical JUP / validator / vote / stake key material;
- security boundary corpus analysis finds helper-owned signer-set/quorum/weight state, root mismatches, new verifier sender/program ids, new proof layouts, or canonical JUP / validator / vote / stake material;
- private runtime fingerprint analysis finds new private JupNet crate names, Dove/stake-weight/quorum/root-builder terms, or loses existing BN254/cross-chain-hash/verifier fingerprints;
- Gum omnichain binary-role analysis changes the `brhPf...` / `GUMeb...` verifier split, adds producer/security terms, or loses existing BN254/cross-chain-hash/verifier symbols;
- Gum account-role reconstruction finds direct `GUMeb...` top-level instructions, canonical JUP account metas, validator/vote/stake account metas, or new signer-set/quorum/weight role candidates;
- Gum omnichain ProgramData hash, deployment slot, upgrade authority, BLS/Merkle strings or utility/security key hits change;
- JupNet executable census finds new programs, ProgramData hash changes, new `sol_verify_bls_merkle_key` consumers, or any canonical JUP / validator / vote / stake / Dove-weight source material;
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
