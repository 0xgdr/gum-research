# Bank Owner Program Context

## Scope

This pass followed the owner/program context around non-token recurring Bank accounts, especially:

- `JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw`
- `jnoUtncGR9ZCCMixtys6Gzy5coTo6mnmUZuEHRQFTFV`
- `5Tv692BDJinbjR6Beb2K9bGmxnbQeFaGb1rJqCs2y3Q6`

Generated files:

```text
evidence/2026-07-12-bank-live-rpc/solana-mainnet-getMultipleAccounts-BankOwnerContext.json
evidence/2026-07-12-bank-live-rpc/solana-mainnet-getSignaturesForAddress-BankOwnerContext.json
evidence/2026-07-12-bank-live-rpc/bank-owner-program-context.md
```

Scripts:

```text
scripts/collect_bank_owner_context.py
scripts/analyze_bank_owner_context.py
```

## Main Finding

Two recurring non-token account owners are upgradeable Solana programs with clear JupNet inbox/outbox binary strings.

| Program | Role evidence | ProgramData | Upgrade authority |
|---|---|---|---|
| `JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw` | `programs/jupnet-inbox-program`, `SubmitInboxMessage`, `JUPNET_INBOX` | `6fBvinpo8Ub7TVpUeTPpPiGMryL432i8N9Z3n3aH2KVT` | `GRr146QcbpANhTZPCo9QBJa1tP5Fr9B6vfua4zRC5cc3` |
| `jnoUtncGR9ZCCMixtys6Gzy5coTo6mnmUZuEHRQFTFV` | `programs/jupnet-outbox-program`, `VerifyOutboxMessage`, `Verifying BLS signature`, `merkle_root_state` | `D6xAx2iTMXP5hg8DeKPDgTw8exLs8MNpYEsmLg89pAsT` | `GRr146QcbpANhTZPCo9QBJa1tP5Fr9B6vfua4zRC5cc3` |

This is meaningful progress. It ties the sampled Bank transactions to explicit JupNet inbox and outbox helper programs on Solana mainnet.

## Negative Checks

The owner-context cluster did not expose:

- canonical Solana JUP key material;
- current JupNet validator/vote/stake keys;
- visible JUP stake, JUP signer weight, JUP quorum, JUP fee, JUP slashing or JUP governance state.

## Interpretation

The public Bank path now looks like this:

```text
Bank Program
  -> JupNet inbox helper program
  -> JupNet outbox helper program
  -> Merkle/BLS verification plumbing
  -> USDC/wrapped SOL settlement accounts in sampled flows
```

That is stronger than generic routing evidence. We can now identify concrete Solana programs for the inbox and outbox sides of the Bank flow.

It still does not prove JUP validator-security utility. The evidence continues to point to cross-chain verification and settlement plumbing, while the JUP security layer remains private, off-chain, inactive, or elsewhere.

## Next Target

The highest-value next target is the outbox program's state account:

```text
3C1LxtpR3Mh5RQjydfeQdvRaAzpStWM7gBi1XzP9oyGt
```

It is owned by the inferred JupNet outbox program and has 320 bytes of state. If any public Solana-side account is likely to expose Merkle root, BLS verifier, signer-set or epoch state, this is now the best candidate.
