# Root Submitter Direct History

## Purpose

This pass collects a direct Solana mainnet signature window for the root-update submitter and analyzes whether it does anything beyond outbox root publication.

Report:

```text
evidence/2026-07-12-bank-live-rpc/root-submitter-history.md
```

Collection manifest:

```text
evidence/2026-07-12-bank-live-rpc/solana-mainnet-root-submitter-history-manifest.json
```

Scripts:

```text
scripts/collect_root_submitter_history.py
scripts/analyze_root_submitter_history.py
```

## Scope

| Metric | Value |
|---|---:|
| Root submitters collected | `1` |
| Signatures fetched | `30` |
| Transaction bodies fetched | `30` |
| Date window | `2026-06-30T19:44:46+00:00` to `2026-07-13T07:47:25+00:00` |
| Programs invoked | `1` |
| Root-update transactions | `30` |
| Canonical JUP / validator / vote / stake intersections | `0` |
| Parsed upgrade-authority intersections | `0` |

## Submitter

```text
6f5muRjigWVnoQHfXWLeXFfafUqMVJfzoBBJL8Gwquji
```

Current account state from Solana mainnet:

| Field | Value |
|---|---|
| Owner | `11111111111111111111111111111111` |
| Executable | `False` |
| Space | `0` |
| Lamports | `2127865131` |

## Pattern

Every fetched transaction:

- is signed by `6f5mu...`;
- invokes only the JupNet outbox helper program;
- logs `UpdateMerkleRoot invoked`;
- logs `Merkle proof verified`;
- logs `Verifying BLS signature`;
- logs `Signature verified`;
- has lamport delta `-5000`;
- has transaction fee `5000`;
- has no token-balance hints.

The fetched pattern is:

```text
6f5mu...
  -> signs/pays scheduled root-update transactions
  -> invokes jnoUtn... outbox helper
  -> pays only transaction fee
  -> no visible token movement
```

## Interpretation

This materially improves the provenance picture.

The submitter is not just a one-off root-update payer. Across the fetched window, it behaves like a dedicated root publisher for the JupNet outbox helper.

The cadence is regular, with one root update roughly every ten hours in the fetched window. That suggests an automated publisher process rather than manual ad hoc operation.

## Negative Findings

The direct signature window did not expose:

- canonical JUP;
- current validator identities;
- current vote accounts;
- current native stake accounts;
- parsed Gum/Bank/inbox/outbox upgrade authorities;
- token balance movement;
- funding source transactions;
- signer-set accounts;
- quorum state;
- slashing or reward state.

## Assessment

This strengthens the operational model:

```text
private/off-chain root builder or operator
  -> dedicated Solana submitter wallet
  -> outbox helper UpdateMerkleRoot
  -> public BLS/Merkle verification
  -> root-history account update
```

It still does not expose the producer side:

```text
Dove/JUP/stake signer set
  -> aggregate key
  -> root submitted by 6f5mu...
```

The next expansion was completed in [`docs/36-root-submitter-funding-history.md`](docs/36-root-submitter-funding-history.md). It found one older funding/setup event tied to a Gum Bank request/withdrawal flow, but still no JUP, validator, vote or stake security-source exposure.
