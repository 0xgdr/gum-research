# Funding Actor Classifier

## Purpose

This pass classifies the accounts around the positive root-submitter funding/setup transaction instead of treating the event as a single opaque transfer.

Report:

```text
evidence/2026-07-12-bank-live-rpc/funding-actor-classifier.md
```

Scripts:

```text
scripts/collect_funding_actor_context.py
scripts/analyze_funding_actor_classifier.py
```

## Main Finding

The positive root-submitter funding event is a Gum Bank request/withdrawal flow that credits the root publisher, not a plain standalone transfer.

The funding transaction:

- used `JUPW3tHBxmNRzVnLmTyYUsUDB6izZSEtupY6znBC5mo` as fee payer and signer;
- credited `6f5muRjigWVnoQHfXWLeXFfafUqMVJfzoBBJL8Gwquji` by `2132273211` lamports;
- included parsed transfer source `7r3RH97CtnYvoUTG18pH3y8c47K7XtTVwzuDifgjiTMM`;
- invoked non-standard programs `bk1PDA...` and `op16...`;
- logged `Instruction: Request`, `Instruction: Withdraw`, `jupnet`, `message_hash` and `Signature verified`;
- wrote request-account data.

## Account Classification

| Account | Observed role | Owner / state |
|---|---|---|
| `6f5muRjigWVnoQHfXWLeXFfafUqMVJfzoBBJL8Gwquji` | Funded root submitter; later regular outbox root publisher | System-owned wallet, non-executable, current lamports `2127865131` |
| `JUPW3tHBxmNRzVnLmTyYUsUDB6izZSEtupY6znBC5mo` | Funding transaction fee payer and signer | System-owned wallet, non-executable, current lamports `4053384455` |
| `7r3RH97CtnYvoUTG18pH3y8c47K7XtTVwzuDifgjiTMM` | Parsed transfer source into root submitter | No current account returned by RPC |
| `bk1PDAkbHEBGtVRiM94Lzets8gVFP7FgySyfkAc8MPN` | Gum Bank request path program | Upgradeable executable |
| `op16NNe3ZDePmRze6ySKvZzKgT1D2duqSWg9b1rfCnR` | Inner withdrawal implementation program | Upgradeable executable |
| `DyEnjnLsr56cwJ4FK38xKw3YyjQ5BgHTq1dgwYMjRCxQ` | Funding-event writable account | Owned by `bk1PDA...`, 72 bytes |
| `VUMS4yy6oKWw4zqHHn9o9moDbaPuRmB7a6fGB7sNVXT` | Funding-event writable/account-meta participant | Owned by `bk1PDA...`, 9 bytes |
| `zVFYUJR5N4jnbxcSQFznjD5hjEmVbjSb9aiVLS4zQHh` | Funding-event account-meta participant | Owned by `bk1PDA...`, 328 bytes |

The local corpus also shows:

- `6f5mu...` appears in `260` local transaction files and is signer in `259`, consistent with the later root-publisher loop;
- `JUPW3...` appears in `26` local transaction files and is signer in all `26`, making it an operational fee-payer/signer candidate rather than a one-off passive account;
- `7r3...`, `bk1PDA...` and `op16...` each appear once in the local corpus because the current saved corpus is centered on the root-submitter funding event rather than a broad Bank withdrawal cohort.

## Decoded Logs

The byte-array logs decode cleanly:

| Log label | Decoded value |
|---|---|
| `recipient` | `6f5muRjigWVnoQHfXWLeXFfafUqMVJfzoBBJL8Gwquji` |
| `mint` | `So11111111111111111111111111111111111111112` |
| `amount 0` | `2132273211` |
| `impl program key` | `op16NNe3ZDePmRze6ySKvZzKgT1D2duqSWg9b1rfCnR` |
| `valid_till` | `1773755762`, about 60 seconds after the transaction block time |
| `withdrawal_request_pubkey` / `jupnet` | same 32-byte value, `Eveu6MH3DxUaH5ZTHBU8BdxjiBcmKJ91wVi6tqjvWBY8` |

This confirms that the Bank withdrawal/request payload names the root submitter as recipient and names `op16...` as the implementation program.

## Utility/Security Implication

This improves our understanding of the operational path:

```text
JUPW3... signer
  -> Gum Bank request program bk1PDA...
  -> withdraw implementation op16...
  -> wrapped SOL withdrawal/request
  -> recipient 6f5mu...
  -> later outbox UpdateMerkleRoot publisher
```

It still does not expose:

- canonical JUP utility;
- Dove identities;
- validator/vote/stake linkage;
- signer-set or quorum state;
- JUP-denominated weight, rewards, slashing, fees or access control.

## Next Angle

The next useful step is a **Bank withdrawal cohort**:

- collect recent `bk1PDA...` request/withdrawal transactions;
- identify how often `op16...` appears;
- decode recipients, mints, amounts and request pubkeys;
- compare recipients against known infrastructure accounts such as `6f5mu...`;
- determine whether funding a root publisher through this path is exceptional or just normal Gum withdrawal behavior.
