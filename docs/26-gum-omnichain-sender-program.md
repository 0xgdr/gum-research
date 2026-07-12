# Gum Omnichain Sender Program

## Purpose

The outbox verifier field map recovered a stable sender/program id from inner outbox verifier payloads:

```text
GUMebNDCYyF81xjyqaHagbgMQVUTb8fBC9YRh25xSH64
```

This pass follows that lead on JupNet.

Report:

```text
evidence/2026-07-12-bank-live-rpc/gum-omnichain-sender-program.md
```

Scripts:

```text
scripts/collect_gum_omnichain_sender_program.py
scripts/analyze_gum_omnichain_sender_program.py
```

## Account Metadata

| Field | Value |
|---|---|
| Program | `GUMebNDCYyF81xjyqaHagbgMQVUTb8fBC9YRh25xSH64` |
| ProgramData | `Gi8HgbHnykRiHboqG2VHysti773o8bNSjuFJWpyf4Q89` |
| ProgramData deployment slot | `106613674` |
| Upgrade authority | `7RrBcJS6vbyMdLoYxQUqiUxD3CYVD55FvsGS5L5rfx2x` |
| Executable length | `1140464` |
| Executable SHA256 | `136c7c999694e1e4999f2c71779564c1b001c2d60bc27bd10e692f4bb66f4734` |

## String Evidence

The executable contains clear source-path and verifier strings:

```text
programs/gum-omnichain/src/lib.rs
programs/gum-omnichain/src/state/withdrawal_request.rs
programs/gum-omnichain/src/state/deposit_request.rs
programs/gum-omnichain/src/state/swap_request.rs
programs/gum-omnichain/src/utils/verification.rs
sol_verify_bls_merkle_key
outbox msg_hash
__inbox_event_auth
```

It also exposes application surfaces for deposit, withdrawal, swap, mint, inbox, outbox, message and fee handling.

## What This Proves

The sampled outbox verifier payloads are not generic proof traffic. Their sender/program id resolves to a live JupNet executable identified by strings as Gum omnichain.

That strengthens this path:

```text
Gum omnichain program
  -> outbox message hash
  -> outbox verifier payload
  -> aggregate-key Merkle proof
  -> stored epoch root
```

## What It Does Not Prove

The executable scan found:

| Check | Result |
|---|---:|
| Canonical JUP / current validator / vote / stake key hits | `0` |
| Dove registry strings | not observed |
| JUP-denominated stake-weight strings | not observed |
| Slashing/reward state strings | not observed |
| Validator mapping strings | not observed |

So this is strong Gum omnichain application evidence, but still not proof that JUP secures the Dove verifier set.

## Current Interpretation

The public pieces now look like:

```text
Gum omnichain application
  -> JupNet outbox verifier
  -> aggregate BLS/Merkle proof
  -> epoch root
```

The missing piece remains:

```text
JUP stake / lock / slash state
  -> Dove weights
  -> aggregate-key set
  -> epoch root
```
