# BankK 41-Byte State Layout

This pass decodes the compact `41`-byte `BankK...` state accounts observed in the created-account and recurring-account evidence.

Evidence report:

```text
evidence/2026-07-12-bank-live-rpc/bankk-41-byte-state-layout.md
```

## Result

The sampled layout is stable:

| Offset | Length | Field | Observed |
|---:|---:|---|---|
| 0 | 8 | account discriminator | `d201f3aeaed73c91` in all 19 rows |
| 8 | 1 | status/version flag | `1` in all 19 rows |
| 9 | 32 | Bank-local id/pubkey candidate | unique per account |

## Correlation

| Test | Result |
|---|---:|
| 41-byte `BankK...` accounts analyzed | `19` |
| Unique embedded 32-byte values | `19` |
| Embedded values with any sampled transaction hit | `18` |
| Embedded values seen as sampled account keys | `1` |
| Embedded values seen in sampled `BankK...` / `JNiN...` raw payloads | `18` |
| Embedded values matching decoded `bk1PDA...` request fields | `0` |
| Embedded values matching verifier payload or outbox-root fields | `0` |
| Embedded values matching canonical JUP / current validator / vote / stake keys | `0` |

## Interpretation

The 32-byte field is not arbitrary account padding. In 18 of 19 analyzed rows it reappears in sampled `BankK...` instruction payloads and `JNiN...` inbox-helper payload/log material. That makes it a Bank-local message/state identifier.

This is meaningful progress because it explains what the live 41-byte accounts are retaining:

- a stable account type discriminator;
- a one-byte state/version flag;
- a per-message or per-operation Bank-local id.

It also narrows what the 41-byte layout is not exposing:

- no decoded `bk1PDA...` request pubkey;
- no decoded `bk1PDA...` `jupnet` pubkey;
- no decoded `bk1PDA...` message hash;
- no verifier message hash, aggregate-key half, compact verifier field, proof node or stored outbox root;
- no canonical JUP mint;
- no current validator, vote or stake key.

## Research Impact

This strengthens the current model:

```text
bk1PDA request state
  -> public decoded withdrawal/request fields

BankK 41-byte state
  -> compact Bank-local id
  -> reused in BankK/JNiN inbox payloads

outbox verifier/root state
  -> separate proof/root material
```

The public surfaces are connected operationally, but the missing bridge from decoded `bk1PDA...` request fields to verifier/security producer state is still not public in this sample.

## Next Useful Angle

The immediate follow-up traced those local ids across sampled transaction lifecycles:

```text
docs/43-bankk-local-id-lifecycle.md
evidence/2026-07-12-bank-live-rpc/bankk-local-id-lifecycle.md
```

That found 18 local ids with operation + `VerifyRequest` lifecycle evidence, including 12 same-slot operation/verify pairings, while still finding zero decoded `bk1PDA...`, verifier/root, JUP or validator/vote/stake matches.

The next broader expansion is transaction-time reconstruction around a larger paired window:

- collect more `BankK...` Withdraw/RFQ/Sweep rows;
- map every 41-byte embedded id to its corresponding `VerifyRequest` payload;
- check whether each id eventually links to an outbox message hash or root update;
- alert if any embedded id begins matching JUP, validator, vote, stake, signer-set, quorum or fee/reward fields.
