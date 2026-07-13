# Bank Request / Message Correlation

## Purpose

This pass tests whether a decoded `bk1PDA... -> op16...` withdrawal request can be linked to a sampled `BankK...` inbox/outbox row by exact request account, message hash, recipient, token movement or raw payload bytes.

Report:

```text
evidence/2026-07-12-bank-live-rpc/bank-request-message-correlation.md
```

Script:

```text
scripts/analyze_bank_request_message_correlation.py
```

## Scope

| Metric | Value |
|---|---:|
| `bk1PDA...` rows loaded | `50` |
| Root submitter setup rows loaded | `1` |
| `BankK...` rows loaded | `50` |
| Decoded `bk1PDA...` / setup request rows | `19` |
| `BankK...` Withdraw rows | `11` |
| `BankK...` VerifyRequest rows | `18` |
| Canonical JUP / validator / vote / stake intersections | `0` |

## Findings

No per-message bridge was found between the sampled windows.

The analyzer checked whether decoded `bk1PDA...` fields appeared in sampled `BankK...` account keys, instruction data, inner instruction data, `Program data:` logs or `Program return:` blobs.

Results:

| Correlation test | Result |
|---|---:|
| Exact high-value request/message/recipient hits | `0` |
| Exact `message_hash` hits | `0` |
| Exact withdrawal-request / `jupnet` pubkey hits | `0` |
| Exact recipient pubkey hits | `0` |
| Token near-matches between decoded `bk1PDA...` withdrawals and `BankK...` Withdraw transfers | `0` |

The analyzer did find common mint/context bytes, mostly expected USDC/context reuse, but those are not enough to prove a specific request moved through both surfaces.

## Role Map

The two surfaces expose different public layouts:

- decoded `bk1PDA...` request rows create `bk1PDA...` request accounts with `72` bytes of space;
- `BankK...` Withdraw rows create `BankK...` state accounts with `41` bytes of space;
- `BankK...` VerifyRequest rows create `BankK...` state accounts with `223` or `256` bytes of space;
- `BankK...` Withdraw/Sweep/RFQ-style rows submit inbox messages through `JNiN...`;
- `BankK...` VerifyRequest rows verify outbox messages through `jnoUtn...`.

This supports the idea that `bk1PDA...` and `BankK...` are related Gum/JupNet operational surfaces but not directly joinable by public per-message identifiers in the sampled corpus.

## Interpretation

This is a useful negative result. It means the evidence has moved from:

```text
These surfaces share signer/program behavior.
```

to:

```text
The sampled public data does not expose a direct per-message join between these surfaces.
```

That sharpens the boundary. We can see the decoded withdrawal request on `bk1PDA...`, and we can see the public inbox/outbox behavior on `BankK...`, but the bridge between those two surfaces is not visible as a reused message hash, request pubkey, recipient account or exact token movement in this sampled window.

It still does not prove JUP utility. No canonical JUP mint, current validator, vote account, stake account, Dove registry, signer weight, quorum, reward, slashing or JUP fee/sink evidence appeared.

## Next Angle

The next public angle is to fetch the Bank-owned state accounts created by the `BankK...` rows and inspect their current raw contents:

- `41`-byte accounts from Withdraw/Swap/Route-style inbox submissions;
- `223`/`256`-byte accounts from VerifyRequest/outbox verification;
- `72`-byte `bk1PDA...` request accounts from decoded request rows.

If those accounts store message hashes or request ids after execution, account-state comparison may expose the join that transaction logs do not.
