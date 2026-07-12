# Bank Account Graph and PDA Hunt

## Scope

This follow-up pushes the Solana-side Bank investigation from instruction grouping into account-graph and PDA analysis.

Generated report:

```text
evidence/2026-07-12-bank-live-rpc/bank-account-graph.md
```

Generator:

```text
scripts/analyze_bank_account_graph.py
```

## What Changed

The new script analyzes sampled `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ` transactions for:

- global account frequency across Bank instructions;
- signer and writable account appearances;
- strong account co-occurrence edges;
- positional account layouts by Bank instruction variant;
- SPL token account hints from pre/post token balances;
- payload string and aligned integer candidates;
- embedded known pubkeys in instruction payloads;
- bounded PDA seed matches for Bank-related string seeds.

## New Findings

The strongest new positive finding is a PDA hit:

| Program | Seed | Derived observed account |
|---|---|---|
| `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ` | `__inbox_event_auth` | `EG9fKpmLgkzCYZdj8uNDhHu5xmeXCZakccV6QmUavbzt` |

This connects one repeated Bank instruction account to the inbox-event authority string recovered from the executable binary.

Other useful observations:

- `sweep` payloads include the strings `USD Coin` and `USDC`.
- `verify_request` payloads embed the Bank Program id and the USDC mint.
- Sampled Bank instructions still contain zero canonical Solana JUP mint account hits.
- The bounded PDA search did not find a simple canonical JUP-derived PDA, `JUPNET_INBOX` PDA, or `merkle_root_state` PDA among observed Bank instruction accounts.

## Assessment

This makes the cross-chain messaging interpretation stronger. We now have a transaction-level account matched to a binary-discovered inbox authority seed.

It still does not prove JUP validator-security utility:

- the only token mints identified in sampled Bank paths remain USDC and wrapped SOL;
- the observed PDA hit is an inbox/event authority, not a JUP stake, fee, quorum, signer-weight or validator registry account;
- no canonical JUP mint or JUP-derived PDA appeared in the sampled Bank instruction accounts.

## Next Decisive Work

The next useful escalation is a wider sample window and an account-owner fetch for the recurring unknown accounts:

- `HVKuqyK6wjexdVJAUARiGdQTdGBBWhdYyhCZGFXh9d4s`
- `2x4wPZePCbq2W9tFfP2bagXjXnysdqNWQWMtwGMoyPFv`
- `2sbhRE62pbi3sLo9CtjM7nYzUynEV4oBAPrGmQPrhnfF`
- `EG9fKpmLgkzCYZdj8uNDhHu5xmeXCZakccV6QmUavbzt`
- `9DvDdsw38EB3RPChPqHkgBmntFbM5v79QxMyMSbfXWuy`
- `JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw`

If those accounts decode into verifier, root, signer-set, route-config or authority state, they may expose the security model without the private source repository.
