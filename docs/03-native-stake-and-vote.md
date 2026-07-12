# Native Stake and Vote Analysis

## Native stake accounts

Standard stake-program accounts were found under:

```text
Stake11111111111111111111111111111111111111
```

Observed delegated stake accounts held approximately:

```text
999,999,997,717,120 delegated lamports
```

with total account balances around:

```text
1,000,000,000,000,000 lamports
```

Each stake account delegated to a native vote account.

## Plain-language interpretation

These are **native chain stake accounts**, analogous to SOL stake accounts on Solana. They are not SPL-token accounts holding the JUP mint.

Therefore:

- native staking exists;
- native staking contributes to ordinary validator participation;
- this does not by itself prove that JUP is the economic security asset.

## Vote transaction analysis

Recent vote transactions were captured and decoded.

Observed properties:

- standard Vote Program ID;
- compact fixed-format vote payloads;
- no visible 48-byte/96-byte BLS key/signature payloads;
- no obvious committee bitmap;
- no extra on-chain quorum-certificate accounts.

## Corrected conclusion

Earlier empty vote-instruction results were caused by reading raw JSON instructions as though they had direct `programId` fields. After decoding `programIdIndex`, vote instructions were recovered.

The corrected analysis still did not reveal BLS signatures directly inside ordinary vote transactions.

## Likely separation

A plausible architecture is:

```text
Tower/SVM vote traffic
        +
separate BLS checkpoint/cross-chain signing
```

This remains a hypothesis until validator-side implementation is available.
