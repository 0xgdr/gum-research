# Withdrawal Surface Comparison

## Purpose

This pass compares two Solana-side Gum withdrawal surfaces:

- `bk1PDA...`, the request/withdrawal path that funded the root submitter setup transaction;
- `BankK...`, the public Bank Program path that emits `Withdraw`, `Sweep`, `VerifyRequest`, inbox and outbox logs.

Report:

```text
evidence/2026-07-12-bank-live-rpc/withdrawal-surface-comparison.md
```

Scripts:

```text
scripts/collect_bank_withdrawal_cohort.py
scripts/analyze_withdrawal_surface_comparison.py
```

## Scope

| Metric | Value |
|---|---:|
| `bk1PDA...` cohort transaction bodies | `50` |
| `BankK...` cohort transaction bodies | `50` |
| Root submitter setup comparison transactions | `1` |
| Total transactions compared | `101` |
| `bk1PDA...` decoded Request/Withdraw rows | `18` |
| `BankK...` VerifyRequest rows | `18` |
| `BankK...` SubmitInbox rows | `27` |
| Canonical JUP / validator / vote / stake intersections | `0` |

## Findings

The two surfaces look connected, but they expose different layers of the system.

`bk1PDA...` is the most useful path for decoded withdrawal payloads. In the sampled set it shows `Request`/`Withdraw` rows, decoded recipients, decoded mint/amount fields and the reused implementation program:

```text
op16NNe3ZDePmRze6ySKvZzKgT1D2duqSWg9b1rfCnR
```

`BankK...` is the more public Bank Program layer. In the sampled set it shows `Withdraw`, `Sweep`, RFQ rows, `VerifyRequest`, inbox submission and outbox verification. It invokes:

```text
JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw
jnoUtncGR9ZCCMixtys6Gzy5coTo6mnmUZuEHRQFTFV
```

Those are the inferred JupNet inbox and outbox helper programs.

Both sampled surfaces are commonly signed/paid by:

```text
JUPW3tHBxmNRzVnLmTyYUsUDB6izZSEtupY6znBC5mo
```

In the `BankK...` sample, `JUPW3...` signed/paid 40 of 50 transactions. A second fee payer/signer, `rfQMF...`, paid the other 10 sampled rows. So `JUPW3...` is a strong operational signer, but not the only observed signer on the public Bank Program surface.

## Interpretation

The current map is now:

```text
JUPW3... operational signer/fee payer
  -> bk1PDA... request/withdrawal surface
     -> op16... withdrawal implementation
     -> decoded recipients/mints/amounts

JUPW3... and rfQ... operational signers/fee payers
  -> BankK... public Bank Program surface
     -> JNiN... inbox helper
     -> jnoUtn... outbox helper
     -> Withdraw / Sweep / RFQ / VerifyRequest rows
```

This is meaningful progress because it separates asset-withdrawal implementation evidence from inbox/outbox message verification evidence. The root submitter setup is not just an isolated funding oddity: it shares the same `bk1PDA... -> op16...` withdrawal machinery as normal decoded withdrawals, while the live `BankK...` path shows the surrounding inbox/outbox layer.

It still does not prove JUP utility. The comparison found no canonical JUP mint, current validator, vote account or stake account intersections, and no visible Dove registry, signer weights, quorum table, slashing, rewards, JUP fee sink or JUP-denominated access-control record.

## Next Angle

The strongest remaining public angle is to watch for changes in the relationship between:

- `JUPW3...` and other operational signers;
- `bk1PDA...`, `op16...`, `BankK...`, `JNiN...` and `jnoUtn...`;
- mints used by root-submitter setup versus normal withdrawals;
- any future appearance of canonical JUP or current validator/vote/stake keys in either surface.

This comparison is now part of the monitor so future checks can alert if the withdrawal/security boundary changes.

The direct per-message correlation follow-up is documented in:

```text
docs/40-bank-request-message-correlation.md
evidence/2026-07-12-bank-live-rpc/bank-request-message-correlation.md
```
