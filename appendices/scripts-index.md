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

### `scripts/compare_validator_security_snapshots.py`

Compares two saved snapshots and emits alert-oriented Markdown.

Example:

```bash
python3 scripts/compare_validator_security_snapshots.py \
  evidence/OLD-live-rpc \
  evidence/NEW-live-rpc
```

### `scripts/run_validator_security_check.py`

Runs the full monitoring workflow: collect a fresh snapshot, generate `analysis.md`, generate `deep-dive.md`, generate `authorization.md`, generate `utility-classification.md`, generate `solana-bank.md`, generate `bank-reverse-engineering.md`, generate `bank-account-graph.md`, and compare against the latest prior snapshot when available.

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
