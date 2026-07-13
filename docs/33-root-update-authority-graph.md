# Root Update Authority Graph

## Purpose

This pass maps the public authority/control surface around outbox root publication.

It asks:

```text
Who signs or controls updates to the root-history state that Gum/Bank later verifies?
```

Report:

```text
evidence/2026-07-12-bank-live-rpc/root-update-authority-graph.md
```

Script:

```text
scripts/analyze_root_update_authority_graph.py
```

## Scope

| Metric | Value |
|---|---:|
| Outbox history/update transaction files scanned | `120` |
| Decoded root-update transactions | `1` |
| Unique transaction signers on decoded root updates | `1` |
| Unique instruction signers on decoded root updates | `0` |
| Unique instruction writable accounts on decoded root updates | `1` |
| Root-update participants intersecting canonical JUP/current validator/vote/stake keys | `0` |
| Root-update participants intersecting known upgrade authorities | `0` |

## Observed Root Update

| Field | Value |
|---|---|
| File | `solana-mainnet-outbox-tx-3Zjq8FZd.json` |
| Time | `2026-07-12T21:25:50+00:00` |
| Slot | `432511387` |
| Epoch | `271` |
| Transaction signer | `6f5muRjigWVnoQHfXWLeXFfafUqMVJfzoBBJL8Gwquji` |
| Instruction signer | `None` |
| Writable instruction account | `3C1LxtpR3Mh5RQjydfeQdvRaAzpStWM7gBi1XzP9oyGt` |
| Root | `6928957b2ea436bc...` |
| Aggregate-key material | `87e930814a0131f7...` |

The only writable instruction account is the outbox Merkle root-history account.

The transaction logs show:

- `UpdateMerkleRoot invoked`
- `Merkle proof verified`
- `Verifying BLS signature`
- `Signature verified`

## Upgrade Authority Comparison

The parsed upgrade authorities for the Gum/Bank/inbox/outbox surfaces did not appear in the root-update transaction signer, instruction accounts or writable accounts.

Notably, the same authority controls the Solana-side Bank Program ProgramData, inbox helper ProgramData and outbox helper ProgramData:

```text
GRr146QcbpANhTZPCo9QBJa1tP5Fr9B6vfua4zRC5cc3
```

That authority did **not** appear in the decoded root update.

## Interpretation

The public control path currently looks like:

```text
unknown root-update transaction signer
  -> invokes Solana JupNet outbox helper
  -> BLS/Merkle verification succeeds
  -> outbox root-history account is updated
```

This is useful because it separates two authority layers:

- **program governance/upgrade authority**, which can change deployed code;
- **runtime root submitter/operator**, which submits root updates for verification.

In the sampled evidence, these are not the same public account.

## Assessment

This strengthens the boundary map but does not prove JUP utility.

What it confirms:

- root publication is public and verifiable;
- the root-history account is the mutable state touched by `UpdateMerkleRoot`;
- the update is submitted by a single transaction signer in the sampled window;
- BLS/Merkle verification occurs before the root update succeeds.

What it still does not expose:

- Dove signer identities;
- JUP-denominated signer weights;
- validator/vote/stake mappings;
- quorum threshold state;
- slashing or reward state;
- root-builder state.

The best monitoring signal from this pass is change detection:

```text
new root-update signer
new writable root-update account
root-update signer matches upgrade authority
root-update participant matches canonical JUP/current validator/vote/stake key
```
