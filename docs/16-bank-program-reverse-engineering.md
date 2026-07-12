# Bank Program Reverse Engineering

## Scope

This follow-up groups sampled Solana mainnet Bank Program instructions and scans the deployed executable bytes for useful strings.

Inputs:

- 8 sampled `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ` transactions.
- Full ProgramData for `bk1PDAkbHEBGtVRiM94Lzets8gVFP7FgySyfkAc8MPN`.
- Full ProgramData for `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ`.

Generated report:

```text
evidence/2026-07-12-bank-live-rpc/bank-reverse-engineering.md
```

## Instruction Variants

Five top-level Bank Program instruction variants were observed in the sampled transactions.

| Discriminator | Likely Anchor name | Data length | Account count | Evidence |
|---|---|---:|---:|---|
| `b712469c946da122` | `withdraw` | 8 | 20 | `Instruction: Withdraw`; `Withdrawal processed`; inbox submission |
| `2817eaaf0e3d9ab1` | `sweep` | 52 | 20 | `Instruction: Sweep`; inbox submission |
| `891f2fe4cdea81ed` | `verify_request` | 463 | 9 | `Instruction: VerifyRequest`; outbox verification |
| `14a2fae36fc17bec` | `rfq_sell_resolve` | 17 | 21 | `Instruction: RfqSellResolve`; inbox submission |
| `9ce6d1a96eebde14` | `rfq_sell_commit` | 8 | 18 | `Instruction: RfqSellCommit` |

Observed parsed token mints across the sampled transactions:

- USDC: `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v`
- Wrapped SOL: `So11111111111111111111111111111111111111112`

Canonical Solana JUP was not observed as a parsed token mint in these samples.

## Binary Strings

The executable string scan exposed useful internal names and source-path clues.

Bank ProgramData:

- executable SHA256: `44b58a16d622d80648022be699cff39762aa3d3110b80491add9c6372f48315c`
- source-path strings include:
  - `programs/bank/src/instructions/create_or_append_request_buffer.rs`
  - `programs/bank/src/instructions/invalidate_request.rs`
  - `programs/bank/src/instructions/request.rs`
  - `programs/bank/src/lib.rs`
- utility-relevant string terms include `merkle`, `proof`, `signer`, `jupnet`, `message_hash`, `valid_till`, `InvalidMerkleProof`, `InvalidEpochMerkleRootNotFound`, `BankDisabled`.

Bank Program ProgramData:

- executable SHA256: `e12d39ee6591d6c9e58460f1ada4addb5bed76cedbc703284ce7bfcd4c60744d`
- source-path strings include:
  - `programs/bank/src/instructions/sweep.rs`
  - `programs/bank/src/instructions/withdraw.rs`
  - `programs/bank/src/state/mod.rs`
  - `programs/bank/src/utils/inbox.rs`
  - `src/inbox.rs`
  - `src/outbox.rs`
- utility-relevant string terms include `JUPNET_INBOX`, `__inbox_event_auth`, `merkle_root_state`, `Outbox verification passed`, `Withdrawal processed`, `swap_authority`.

## Assessment

This is stronger than generic routing evidence. The Solana-side Bank programs visibly implement request, inbox, outbox, Merkle/proof and message-hash machinery.

It is still not proof that JUP secures the validator or Dove layer:

- no canonical JUP mint was observed in sampled Bank Program token flow;
- no JUP-denominated signer weight, validator stake, quorum threshold, slashing, reward or fee mechanism was observed;
- binary `jup`/`jupnet` string hits identify JupNet integration context, not token utility by themselves.

Follow-up account-graph work found that the repeated account `EG9fKpmLgkzCYZdj8uNDhHu5xmeXCZakccV6QmUavbzt` is the Bank Program PDA for `__inbox_event_auth`. That supports the inbox-event authority interpretation, but still does not expose a JUP stake, fee, quorum, signer-weight or validator-security account.

The next decisive target is broader account-owner/layout reconstruction for the recurring unknown Bank accounts, especially verifier, root, signer-set and authority candidates.
