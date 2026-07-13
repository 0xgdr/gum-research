# Root Submitter Funding History

## Purpose

This pass pages further back through the root-update submitter's Solana mainnet history to find the funding or setup event behind the dedicated outbox root publisher.

Report:

```text
evidence/2026-07-12-bank-live-rpc/root-submitter-funding-history.md
```

Collection manifest:

```text
evidence/2026-07-12-bank-live-rpc/solana-mainnet-root-submitter-funding-history-manifest.json
```

Scripts:

```text
scripts/collect_root_submitter_funding_history.py
scripts/analyze_root_submitter_funding_history.py
```

## Scope

| Metric | Value |
|---|---:|
| Root submitters collected | `1` |
| Transaction bodies fetched | `229` |
| Positive lamport-delta transactions | `1` |
| Date window | `2026-03-17T13:55:02+00:00` to `2026-06-30T09:29:39+00:00` |
| Transfer sources into submitter | `1` |
| Canonical JUP / validator / vote / stake intersections | `0` |
| Parsed upgrade-authority intersections | `0` |

## Positive Funding Event

| Field | Value |
|---|---|
| File | `solana-mainnet-root-submitter-funding-6f5muRji-tx-3tT26UGo.json` |
| Signature | `3tT26UGoe2Vdeg4drULx3jbwZQe9uzMDW1xwuoB33opzfs9SXdmiWMRcCWXXKsPtwd9v2qCCV63Pt2qWGfh8iBX3` |
| Time | `2026-03-17T13:55:02+00:00` |
| Slot | `407026644` |
| Root submitter | `6f5muRjigWVnoQHfXWLeXFfafUqMVJfzoBBJL8Gwquji` |
| Submitter lamport delta | `+2132273211` |
| Parsed transfer source into submitter | `7r3RH97CtnYvoUTG18pH3y8c47K7XtTVwzuDifgjiTMM` |
| Fee payer / signer | `JUPW3tHBxmNRzVnLmTyYUsUDB6izZSEtupY6znBC5mo` |
| Bank request program | `bk1PDAkbHEBGtVRiM94Lzets8gVFP7FgySyfkAc8MPN` |
| Inner withdraw program | `op16NNe3ZDePmRze6ySKvZzKgT1D2duqSWg9b1rfCnR` |

## Why This Matters

This is the first concrete provenance link behind the public root publisher.

The funding event is not a simple isolated SOL transfer. The transaction:

- creates associated token accounts;
- invokes the Solana-side Gum Bank request program `bk1PDA...`;
- invokes `op16...` with an `Instruction: Withdraw` log;
- credits the root submitter with `2132273211` lamports;
- emits `jupnet [...]`, `message_hash [...]` and `Signature verified` logs;
- writes unique request-account data.

That ties the root submitter's setup/funding event to the same Gum/Bank/JupNet operational surface already seen in the inbox/outbox evidence. It makes the submitter look like infrastructure created through a Gum Bank withdrawal/request workflow, not a random externally funded wallet.

## What It Does Not Prove

This still does not prove JUP utility or JUP-backed validator security.

The funding-history window did not expose:

- canonical JUP mint/account usage;
- current JupNet validator identities;
- current vote accounts;
- current native stake accounts;
- parsed Gum/Bank/inbox/outbox upgrade authorities;
- Dove identities;
- signer-set accounts;
- JUP-denominated weights;
- quorum calculation;
- slashing, rewards, governance or access-control state.

The evidence therefore improves operational attribution but does not cross the utility/security proof threshold.

## Updated Model

```text
Gum/Bank/JupNet request or withdrawal flow
  -> funds/sets up 6f5mu... root submitter
  -> 6f5mu... later publishes regular outbox UpdateMerkleRoot transactions
  -> public helper verifies BLS/Merkle proof
  -> root-history account is updated
```

The missing part remains:

```text
Dove/JUP/stake-weight source
  -> aggregate key or signer set
  -> root builder
  -> public root submitter
```

## Follow-Up

The funding actor classification follow-up is documented in [`docs/37-funding-actor-classifier.md`](docs/37-funding-actor-classifier.md). It decodes the funding payload and classifies `JUPW3...`, `7r3...`, `bk1PDA...`, `op16...` and the Bank-owned request accounts.

The next meaningful investigation target is now a wider Bank withdrawal cohort: compare other `bk1PDA...` request/withdrawal transactions against this root-submitter setup event to see whether infrastructure funding through this path is exceptional or routine.
