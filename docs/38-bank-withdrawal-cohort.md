# Bank Withdrawal Cohort

## Purpose

This pass tests whether the root submitter setup transaction is exceptional or part of a broader `bk1PDA...` Gum Bank withdrawal pattern.

Report:

```text
evidence/2026-07-12-bank-live-rpc/bank-withdrawal-cohort.md
```

Scripts:

```text
scripts/collect_bank_withdrawal_cohort.py
scripts/analyze_bank_withdrawal_cohort.py
```

## Scope

| Metric | Value |
|---|---:|
| Target program/address | `bk1PDAkbHEBGtVRiM94Lzets8gVFP7FgySyfkAc8MPN` |
| Cohort transaction bodies fetched | `50` |
| Cohort transactions with `Instruction: Request` and `Instruction: Withdraw` | `18` |
| Root submitter setup comparison events | `1` |
| Decoded withdrawal-like rows including setup comparison | `19` |
| Unique decoded recipients | `15` |
| Canonical JUP / validator / vote / stake intersections | `0` |

## Findings

The root submitter setup transaction does **not** use a one-off withdrawal implementation.

Across the decoded withdrawal-like rows:

- `op16NNe3ZDePmRze6ySKvZzKgT1D2duqSWg9b1rfCnR` appears as the implementation program in all `19` decoded rows;
- `JUPW3tHBxmNRzVnLmTyYUsUDB6izZSEtupY6znBC5mo` signs and pays all `50` fetched cohort transactions, and also signs/pays the root-submitter setup comparison transaction;
- the root submitter `6f5mu...` appears as one decoded recipient among many recipients, not as the only recipient observed through this path;
- the cohort does not expose canonical JUP, current validators, vote accounts or stake accounts.

## What Is Distinct About The Root Submitter Setup

The regular decoded cohort withdrawals used USDC:

```text
EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v
```

The root submitter setup comparison used wrapped SOL:

```text
So11111111111111111111111111111111111111112
```

That means the setup event is operationally connected to the same `bk1PDA... -> op16...` withdrawal machinery, but it is still distinguishable by mint and recipient.

## Interpretation

The current model becomes:

```text
JUPW3... operational signer/fee payer
  -> bk1PDA... Gum Bank request path
  -> op16... withdrawal implementation
  -> normal decoded recipients, mostly USDC in the sampled cohort
  -> one observed setup comparison recipient: 6f5mu... with wrapped SOL
```

This weakens the idea that the root submitter was funded through a bespoke one-off program path. It strengthens the idea that Jupiter/Gum infrastructure uses a common `JUPW3...`-signed Bank withdrawal system, and that the root publisher was funded through that system.

It still does not prove JUP utility or Dove security. No decoded cohort row exposed JUP-denominated staking, validator/vote/stake linkage, quorum weights, signer-set records, slashing, rewards, governance or access control.

## Next Angle

The next useful expansion is to compare the two Solana-side withdrawal surfaces:

- `bk1PDA...` Request/Withdraw rows, which include the root-submitter setup event;
- `BankK...` Withdraw rows already seen in sampled Bank Program transactions.

That comparison should answer whether these are two layers of the same withdrawal pipeline, and whether the `JUPW3...` signer consistently controls both surfaces.
