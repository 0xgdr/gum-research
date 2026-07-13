# Root Submitter Provenance

## Purpose

This pass follows the public root-update submitter through the locally saved transaction corpus.

It asks:

```text
Is the root-update submitter a broad Gum/Bank operator, or only visible as a narrow outbox-root publisher?
```

Report:

```text
evidence/2026-07-12-bank-live-rpc/root-submitter-provenance.md
```

Script:

```text
scripts/analyze_root_submitter_provenance.py
```

## Scope

| Metric | Value |
|---|---:|
| Root-update submitters derived from decoded updates | `1` |
| Saved transaction bodies scanned | `36` |
| Transactions containing the submitter | `1` |
| Transactions where the submitter is a signer | `1` |
| Submitter account-data hits outside transaction bodies | `0` |

## Submitter

```text
6f5muRjigWVnoQHfXWLeXFfafUqMVJfzoBBJL8Gwquji
```

The submitter appears in one saved transaction:

| Field | Value |
|---|---|
| File | `solana-mainnet-outbox-tx-3Zjq8FZd.json` |
| Time | `2026-07-12T21:25:50+00:00` |
| Slot | `432511387` |
| Role | root-update transaction signer/payer |
| Program invoked | `jnoUtncGR9ZCCMixtys6Gzy5coTo6mnmUZuEHRQFTFV` |
| Writable state | `3C1LxtpR3Mh5RQjydfeQdvRaAzpStWM7gBi1XzP9oyGt` |
| Lamport delta | `-5000` |
| Transaction fee | `5000` |
| Token-balance hints | `None` |

## Interpretation

Within the saved corpus, the root-update submitter looks like a narrow outbox-root publisher:

```text
6f5mu...
  -> signs/pays one root-update transaction
  -> invokes the Solana JupNet outbox helper
  -> writes the outbox root-history account
```

It does not appear in the sampled Gum, Bank, verifier or helper-account state outside that transaction.

## Negative Findings

The saved corpus does not show the submitter touching:

- canonical JUP;
- current validator identities;
- current vote accounts;
- current native stake accounts;
- parsed Gum/Bank/inbox/outbox upgrade authorities;
- signer-set accounts;
- quorum state;
- slashing or reward state.

## Assessment

This is helpful, but still bounded.

It reduces one possible explanation: the visible root-update signer is not obviously the same as the broader public Gum/Bank operator accounts in the saved evidence.

It does **not** prove who controls the signer or whether it is one of several rotating root publishers. The follow-up direct-history and funding-history walks are now documented in [`docs/35-root-submitter-direct-history.md`](docs/35-root-submitter-direct-history.md) and [`docs/36-root-submitter-funding-history.md`](docs/36-root-submitter-funding-history.md).
