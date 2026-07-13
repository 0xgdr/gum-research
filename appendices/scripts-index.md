# Scripts Index

Scripts developed or discussed during the investigation included:

- validator/native-program inspection;
- stake account enumeration;
- vote transaction capture;
- corrected raw vote decoding;
- OpenID Registry decoding;
- executable program dumping;
- binary string extraction;
- JUP-in-Gum tracing;
- public dependency/lockfile analysis.

## Added reproducibility scripts

### `scripts/collect_validator_security_snapshot.py`

Collects a bounded live JupNet RPC snapshot for validator-security research.

Example:

```bash
python3 scripts/collect_validator_security_snapshot.py \
  --output-dir evidence/YYYY-MM-DD-live-rpc
```

### `scripts/analyze_validator_security_snapshot.py`

Analyzes a saved snapshot for:

- canonical JUP mint references;
- validator identity key references;
- vote account key references;
- stake account key references;
- native stake distribution;
- recent Gum transaction log terms.

Example:

```bash
python3 scripts/analyze_validator_security_snapshot.py \
  evidence/YYYY-MM-DD-live-rpc
```

### `scripts/deep_dive_validator_security_snapshot.py`

Performs second-stage analysis for:

- Gum account groups containing canonical JUP base58 text;
- absence/presence of raw canonical JUP pubkey bytes;
- Gum ProgramData address, deployment slot and upgrade authority;
- sampled Gum transaction signers;
- validator/vote/stake account hits in sampled Gum transactions.

Example:

```bash
python3 scripts/deep_dive_validator_security_snapshot.py \
  evidence/YYYY-MM-DD-live-rpc
```

### `scripts/analyze_gum_authorization.py`

Analyzes sampled Gum transactions like a Solana program/operator review:

- signers and writable accounts;
- Gum instruction data lengths and first eight bytes;
- invoked top-level and inner programs;
- parsed token mints touched;
- repeated config-like accounts;
- validator/vote/stake account hits;
- full Gum instruction account metas with signer/writable roles.

Example:

```bash
python3 scripts/analyze_gum_authorization.py \
  evidence/YYYY-MM-DD-live-rpc
```

### `scripts/classify_gum_utility_surfaces.py`

Classifies Gum JUP metadata accounts, repeated Gum path accounts and sampled Gum instruction variants as utility evidence or non-decisive asset evidence.

Example:

```bash
python3 scripts/classify_gum_utility_surfaces.py \
  evidence/YYYY-MM-DD-live-rpc
```

### `scripts/analyze_solana_bank_surface.py`

Analyzes Solana mainnet Bank evidence captured by the snapshot collector, including account presence, ProgramData, upgrade authority, recent signatures, sampled transaction signers, invoked programs, parsed token mints and inbox/outbox log terms.

Example:

```bash
python3 scripts/analyze_solana_bank_surface.py \
  evidence/YYYY-MM-DD-live-rpc
```

### `scripts/reverse_engineer_solana_bank.py`

Groups sampled Solana Bank Program instructions by discriminator, data length and account roles, then scans full Bank ProgramData executable bytes for request, inbox, outbox, Merkle, JupNet and JUP-related strings.

Example:

```bash
python3 scripts/reverse_engineer_solana_bank.py \
  evidence/YYYY-MM-DD-live-rpc
```

### `scripts/analyze_bank_account_graph.py`

Builds a sampled Solana Bank account graph and PDA hunt:

- account frequency and co-occurrence edges;
- positional account layouts per instruction variant;
- token account hints from pre/post token balances;
- payload string, aligned integer and embedded-pubkey candidates;
- bounded PDA seed matches for Bank, inbox, outbox, Merkle, authority and JUP-related seeds.

Example:

```bash
python3 scripts/analyze_bank_account_graph.py \
  evidence/YYYY-MM-DD-live-rpc
```

### `scripts/collect_bank_recurring_accounts.py`

Fetches Solana mainnet account state for accounts that recur in sampled Bank Program instructions. The target list is derived from the saved sampled transaction bodies and excludes obvious program/mint accounts.

Example:

```bash
python3 scripts/collect_bank_recurring_accounts.py \
  evidence/YYYY-MM-DD-live-rpc
```

### `scripts/analyze_bank_recurring_accounts.py`

Classifies fetched recurring Bank accounts as system accounts, SPL token accounts, Bank Program-owned state, missing/transient accounts or other accounts. It scans raw account data for canonical JUP, current JupNet validator/vote/stake keys, known Bank pubkeys and utility/security terms.

Example:

```bash
python3 scripts/analyze_bank_recurring_accounts.py \
  evidence/YYYY-MM-DD-live-rpc
```

### `scripts/collect_bank_owner_context.py`

Fetches Solana mainnet owner/program context for recurring Bank accounts, including owner programs, their ProgramData accounts where applicable, and bounded signature windows for the context cluster.

Example:

```bash
python3 scripts/collect_bank_owner_context.py \
  evidence/YYYY-MM-DD-live-rpc
```

### `scripts/analyze_bank_owner_context.py`

Analyzes the owner/program context cluster for recurring Bank state. It identifies upgradeable owner programs, ProgramData deployment slots, upgrade authorities, executable hashes, inbox/outbox/Merkle/BLS string hits, canonical JUP hits and validator/vote/stake key hits.

Example:

```bash
python3 scripts/analyze_bank_owner_context.py \
  evidence/YYYY-MM-DD-live-rpc
```

### `scripts/collect_jupnet_helper_program_accounts.py`

Fetches all accounts owned by the inferred Solana-side JupNet inbox and outbox helper programs, plus bounded signature windows for those program IDs.

Example:

```bash
python3 scripts/collect_jupnet_helper_program_accounts.py \
  evidence/YYYY-MM-DD-live-rpc
```

### `scripts/analyze_jupnet_helper_program_accounts.py`

Groups helper-program-owned accounts by layout, scans for canonical JUP and validator/vote/stake keys, and decodes the public outbox state as Merkle root history when present.

Example:

```bash
python3 scripts/analyze_jupnet_helper_program_accounts.py \
  evidence/YYYY-MM-DD-live-rpc
```

### `scripts/reconstruct_verify_request_payloads.py`

Reconstructs sampled Bank Program `verify_request` instruction payloads, including difference ranges, known pubkey hits, timestamp-like fields, Merkle proof tail extraction, outbox-root comparison and JUP/validator-key checks.

Example:

```bash
python3 scripts/reconstruct_verify_request_payloads.py \
  evidence/YYYY-MM-DD-live-rpc
```

### `scripts/collect_outbox_root_update_transactions.py`

Fetches recent transaction bodies for signatures involving the inferred JupNet outbox helper program.

Example:

```bash
python3 scripts/collect_outbox_root_update_transactions.py \
  evidence/YYYY-MM-DD-live-rpc
```

### `scripts/analyze_outbox_root_update_transactions.py`

Scans recent outbox helper transactions for `UpdateMerkleRoot`, Merkle proof and BLS verification logs, then decodes the 305-byte root-update payload when present and checks account keys/payload bytes for canonical JUP and current JupNet validator/vote/stake keys.

Example:

```bash
python3 scripts/analyze_outbox_root_update_transactions.py \
  evidence/YYYY-MM-DD-live-rpc
```

### `scripts/collect_outbox_root_history.py`

Pages a wider Solana mainnet signature window for the JupNet outbox helper program and fetches parsed transaction bodies into `solana-mainnet-outbox-history-tx-*.json`.

Example:

```bash
python3 scripts/collect_outbox_root_history.py \
  evidence/YYYY-MM-DD-live-rpc
```

### `scripts/analyze_outbox_root_history.py`

Analyzes all saved outbox history/update transaction files. It decodes root-update payloads and inner verifier payloads, recomputes Merkle roots, groups aggregate-key/root/compact-verifier-field values and checks decoded rows for canonical JUP plus current validator/vote/stake keys.

Example:

```bash
python3 scripts/analyze_outbox_root_history.py \
  evidence/YYYY-MM-DD-live-rpc
```

### `scripts/analyze_root_update_authority_graph.py`

Builds a public authority/control graph around decoded outbox root updates. It reports root-update transaction signers, instruction signers, writable root-history accounts, parsed ProgramData upgrade authorities and intersections with canonical JUP or current validator/vote/stake keys.

Example:

```bash
python3 scripts/analyze_root_update_authority_graph.py \
  evidence/YYYY-MM-DD-live-rpc
```

### `scripts/analyze_root_submitter_provenance.py`

Traces root-update submitter accounts through the saved transaction corpus. It reports submitter occurrences, signer occurrences, invoked programs, co-accounts, lamport deltas, token-balance hints, account-data hits and intersections with canonical JUP, validator/vote/stake keys or parsed upgrade authorities.

Example:

```bash
python3 scripts/analyze_root_submitter_provenance.py \
  evidence/YYYY-MM-DD-live-rpc
```

### `scripts/reconstruct_outbox_update_payload.py`

Reconstructs sampled 305-byte outbox `UpdateMerkleRoot` payloads. It parses the epoch/root fields, proof nodes, path bitmap and final 64-byte candidate aggregate-key material, then recomputes the Merkle root using the public JupNet article's `0x00` leaf and `0x01` parent hash formulas.

Example:

```bash
python3 scripts/reconstruct_outbox_update_payload.py \
  evidence/YYYY-MM-DD-live-rpc
```

### `scripts/hunt_epoch_security_sources.py`

Scans a saved snapshot for the missing source behind an outbox epoch root. It extracts binary account, instruction and program-log records, then searches for the epoch root, candidate aggregate-key material, aggregate-key leaf hash, canonical JUP mint and current JupNet validator/vote/stake keys. It reports whether root/update material co-locates with JUP or validator-security keys.

Example:

```bash
python3 scripts/hunt_epoch_security_sources.py \
  evidence/YYYY-MM-DD-live-rpc
```

### `scripts/map_outbox_verifier_payloads.py`

Maps sampled Bank/outbox verifier payloads around aggregate-key proof material. It parses message hash, sender/program id, epoch, aggregate-key material, compact signature/verifier field, path bitmap and Merkle proof nodes, then recomputes the stored outbox root for each parsed payload.

Example:

```bash
python3 scripts/map_outbox_verifier_payloads.py \
  evidence/YYYY-MM-DD-live-rpc
```

### `scripts/collect_gum_omnichain_sender_program.py`

Fetches the JupNet `GUMeb...` sender program and its ProgramData account after the outbox verifier field map identifies it as the stable sender/program id.

Example:

```bash
python3 scripts/collect_gum_omnichain_sender_program.py \
  evidence/YYYY-MM-DD-live-rpc
```

### `scripts/analyze_gum_omnichain_sender_program.py`

Analyzes the fetched Gum omnichain sender program. It parses upgradeable-loader metadata, extracts executable strings, reports Gum/inbox/outbox/BLS/Merkle terms and scans for canonical JUP plus current validator/vote/stake key material.

Example:

```bash
python3 scripts/analyze_gum_omnichain_sender_program.py \
  evidence/YYYY-MM-DD-live-rpc
```

### `scripts/collect_jupnet_executable_census.py`

Derives all visible JupNet upgradeable executable ProgramData addresses from `getProgramAccounts-UpgradeableLoader-slice48.json`, then fetches each full ProgramData account and writes `jupnet-executable-census-manifest.json`.

Example:

```bash
python3 scripts/collect_jupnet_executable_census.py \
  evidence/YYYY-MM-DD-live-rpc
```

### `scripts/analyze_jupnet_executable_census.py`

Analyzes the fetched JupNet executable census. It parses ProgramData headers, extracts executable hashes, source-path strings, verifier/syscall terms and canonical JUP/current validator/vote/stake key hits.

Example:

```bash
python3 scripts/analyze_jupnet_executable_census.py \
  evidence/YYYY-MM-DD-live-rpc
```

### `scripts/compare_validator_security_snapshots.py`

Compares two saved snapshots and emits alert-oriented Markdown. The comparator tracks the original Gum/Bank/JUP surfaces plus the newer proof-chain evidence: outbox root-history roots, aggregate keys, compact verifier fields, root-update signers, root-update writable accounts, root-submitter provenance changes, verifier sender/program ids, verifier payload layouts, private runtime fingerprints, JupNet executable hashes, upgrade authorities, `sol_verify_bls_merkle_key` consumers and executable key-hit rows.

Example:

```bash
python3 scripts/compare_validator_security_snapshots.py \
  evidence/OLD-live-rpc \
  evidence/NEW-live-rpc
```

### `scripts/analyze_security_boundary_corpus.py`

Combines helper-program-owned inbox/outbox account layout analysis with every locally saved Solana Bank/outbox/history transaction body. It decodes verifier payload roots, aggregate keys, sender/program ids, compact verifier fields, proof layouts, root mismatches and canonical JUP/current validator/vote/stake key hits.

Example:

```bash
python3 scripts/analyze_security_boundary_corpus.py \
  evidence/YYYY-MM-DD-live-rpc
```

### `scripts/analyze_private_runtime_fingerprints.py`

Scans saved public artifacts for exact private JupNet runtime/security fingerprints. It searches decoded account data, ProgramData executable bytes, transaction instruction bytes and JSON/log text for private dependency names, Dove/stake-weight/quorum/root-builder terms and public verifier strings.

Example:

```bash
python3 scripts/analyze_private_runtime_fingerprints.py \
  evidence/YYYY-MM-DD-live-rpc
```

### `scripts/analyze_gum_omnichain_binary_roles.py`

Compares the `brhPf...` and `GUMeb...` Gum omnichain executables. It extracts metadata, source-path families, JupNet symbols, Solana/JupNet syscalls, instruction markers and high-value contexts around verifier, BN254, cross-chain hash, proof, chain config, fee and producer/security terms.

Example:

```bash
python3 scripts/analyze_gum_omnichain_binary_roles.py \
  evidence/YYYY-MM-DD-live-rpc
```

### `scripts/analyze_gum_account_role_reconstruction.py`

Reconstructs Gum and Bank account roles from sampled transaction account metas, token balance hints, known helper accounts and decoded verifier payloads. It separates direct `brhPf...` Gum transactions, direct Solana Bank instructions and inferred `GUMeb...` verifier sender evidence.

Example:

```bash
python3 scripts/analyze_gum_account_role_reconstruction.py \
  evidence/YYYY-MM-DD-live-rpc
```

### `scripts/run_validator_security_check.py`

Runs the full monitoring workflow: collect a fresh snapshot, fetch recurring Bank account state, fetch owner-program context, fetch JupNet helper-program-owned accounts, fetch outbox root-update transactions, fetch wider outbox root history, fetch the Gum omnichain sender program, fetch all visible JupNet executable ProgramData accounts, generate `analysis.md`, generate `deep-dive.md`, generate `authorization.md`, generate `utility-classification.md`, generate `solana-bank.md`, generate `bank-reverse-engineering.md`, generate `bank-account-graph.md`, generate `bank-recurring-account-state.md`, generate `bank-owner-program-context.md`, generate `jupnet-helper-program-accounts.md`, generate `verify-request-payload-reconstruction.md`, generate `outbox-root-update-transactions.md`, generate `outbox-update-payload-reconstruction.md`, generate `outbox-root-history.md`, generate `root-update-authority-graph.md`, generate `root-submitter-provenance.md`, generate `epoch-security-source-hunt.md`, generate `outbox-verifier-payload-field-map.md`, generate `security-boundary-corpus.md`, generate `private-runtime-fingerprints.md`, generate `gum-omnichain-binary-roles.md`, generate `gum-account-role-reconstruction.md`, generate `gum-omnichain-sender-program.md`, generate `jupnet-executable-census.md`, and compare against the latest prior snapshot when available.

Example:

```bash
python3 scripts/run_validator_security_check.py
```

### `scripts/crawl_jup_ag_public_repos.py`

Enumerates public repositories under `jup-ag`, shallow-clones each repository into a temporary directory, scans bounded text files for Gum/JupNet utility clue terms and writes markdown/JSON results under `research/`.

Example:

```bash
python3 scripts/crawl_jup_ag_public_repos.py
```

## Reproducibility note

The original scripts were developed iteratively. Before publishing them as production tooling:

1. consolidate duplicated RPC helpers;
2. add rate limiting and retries;
3. persist raw responses;
4. record generated timestamps and RPC versions;
5. hash every downloaded binary;
6. distinguish parsed-instruction and compiled-instruction formats;
7. add tests for base58 and account-index decoding.
