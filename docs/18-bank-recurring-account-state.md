# Bank Recurring Account State

## Scope

This pass fetched full Solana mainnet account state for recurring accounts observed in sampled Bank Program instructions.

Generated files:

```text
evidence/2026-07-12-bank-live-rpc/solana-mainnet-getMultipleAccounts-BankRecurringAccounts.json
evidence/2026-07-12-bank-live-rpc/bank-recurring-account-state.md
```

Scripts:

```text
scripts/collect_bank_recurring_accounts.py
scripts/analyze_bank_recurring_accounts.py
```

## Result

The collector fetched 20 recurring Bank instruction accounts.

Classification:

| Class | Count |
|---|---:|
| missing | 6 |
| other account | 5 |
| SPL token account | 4 |
| system account | 3 |
| Bank Program-owned state | 2 |

Negative utility/security checks:

| Check | Result |
|---|---:|
| Canonical JUP raw pubkey bytes | 0 accounts |
| Canonical JUP base58 text | 0 accounts |
| Current JupNet validator/vote/stake key hits | 0 accounts |

## Token Accounts

The recurring SPL token accounts were USDC and wrapped SOL accounts:

- USDC mint: `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v`
- wrapped SOL mint: `So11111111111111111111111111111111111111112`

No recurring SPL token account used the canonical Solana JUP mint.

## Bank-Owned State

Two recurring accounts were owned by the Bank Program:

| Account | Space | Discriminator | Compact fields |
|---|---:|---|---|
| `HVKuqyK6wjexdVJAUARiGdQTdGBBWhdYyhCZGFXh9d4s` | 9 | `10a97e6323a949c8` | `byte_8=1` |
| `4s3gnkf1R2UzAWbfvVowfaW7VdLDNSQhmwjYcSnMYwmT` | 41 | `d201f3aeaed73c91` | `byte_8=1`, `pubkey_9_40=5Tv692BDJinbjR6Beb2K9bGmxnbQeFaGb1rJqCs2y3Q6` |

These look like compact Bank state/config records, not token custody accounts or obvious validator-security registries. Their layouts are still not fully identified.

## Assessment

This pass reduces the chance that obvious JUP utility is hidden in the high-frequency sampled Bank accounts.

It does not rule out JUP utility elsewhere:

- the sample window is still small;
- missing accounts may be transient PDAs closed after instruction execution;
- security state could live in less frequent accounts, off-chain services, private runtime code, or accounts not touched by the sampled Bank paths.

The best next target is to fetch account history and owner/program context for:

- `JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw`
- `jnoUtncGR9ZCCMixtys6Gzy5coTo6mnmUZuEHRQFTFV`
- `5Tv692BDJinbjR6Beb2K9bGmxnbQeFaGb1rJqCs2y3Q6`

Those keys may explain the non-token owner programs and the embedded pubkey in the 41-byte Bank-owned state record.
