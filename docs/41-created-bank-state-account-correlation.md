# Created Bank State Account Correlation

## Purpose

This pass checks whether current account state reveals the per-message bridge that transaction logs did not expose.

It derives accounts created by sampled `bk1PDA...`, `BankK...` and root-submitter setup transactions, fetches their current Solana account data, and scans those bytes for:

- decoded `bk1PDA...` message hashes;
- decoded withdrawal-request / `jupnet` pubkeys;
- decoded recipients;
- canonical JUP;
- current JupNet validator, vote or stake keys.

Report:

```text
evidence/2026-07-12-bank-live-rpc/created-bank-state-account-correlation.md
```

Scripts:

```text
scripts/collect_created_bank_state_accounts.py
scripts/analyze_created_bank_state_accounts.py
```

## Scope

| Metric | Value |
|---|---:|
| Created accounts fetched | `85` |
| Current accounts missing/closed | `46` |
| Current `bk1PDA...`-owned state accounts | `19` |
| Current `BankK...`-owned state accounts | `18` |
| Current SPL token accounts | `2` |
| Cross-surface high-value hits in current `BankK...` state | `0` |
| Canonical JUP hits | `0` |
| Current validator/vote/stake hits | `0` |

## Findings

The created-account state pass sharpened the boundary.

Current `bk1PDA...` 72-byte request accounts retain decodable request state:

- the `op16...` withdrawal implementation key appears at offset `8`;
- some request / `jupnet` pubkeys appear at offset `40`;
- this confirms that the `bk1PDA...` request state layout is publicly decodable after execution.

Current `BankK...` state did **not** expose the same join:

- no current `BankK...` state account contained decoded `bk1PDA...` message hashes;
- no current `BankK...` state account contained decoded withdrawal-request / `jupnet` pubkeys;
- no current `BankK...` state account contained decoded recipients;
- no fetched created account contained canonical JUP, current validator, vote or stake key material.

Many created accounts are already missing or closed. That is expected for transient request, proof or token accounts and means current account state cannot fully reconstruct transaction-time state.

## Interpretation

This pass confirms one useful thing and one limit.

The useful thing:

```text
bk1PDA 72-byte request accounts retain public request/implementation fields.
```

The limit:

```text
BankK current state does not retain the decoded bk1PDA request/message identifiers.
```

So the missing public join is not in:

- sampled transaction logs;
- sampled `BankK...` raw instruction payloads;
- sampled `BankK...` raw log payloads;
- current `BankK...` state accounts.

That makes the remaining bridge likely one of:

- transient account state that was closed or rewritten after execution;
- a private/off-chain index or executor system;
- a different transaction window not yet sampled;
- an intentionally separate `BankK...` local-id system that does not preserve `bk1PDA...` request identifiers publicly.

## Next Angle

The immediate follow-up decoded the compact 41-byte `BankK...` state accounts:

```text
docs/42-bankk-41-byte-state-layout.md
evidence/2026-07-12-bank-live-rpc/bankk-41-byte-state-layout.md
```

That found a stable Bank-local 32-byte id reused in `BankK...` / `JNiN...` payloads, but still no decoded `bk1PDA...`, verifier/root, JUP or validator/vote/stake match.

The next meaningful public option is historical account-state reconstruction. Standard public RPC does not provide arbitrary historical account bytes, so the practical paths are:

- collect larger paired time windows around same-slot `BankK...` Withdraw and VerifyRequest rows;
- fetch confirmed blocks for narrow slot ranges and reconstruct same-slot transaction groups;
- if available, use an archival/indexer source that preserves account write versions.

Without historical account state, current public evidence now strongly suggests the per-message join is not exposed by the normal Solana RPC surfaces we sampled.
