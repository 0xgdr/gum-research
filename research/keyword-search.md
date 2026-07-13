# Public Code-Search Matrix

## Search scope

Initial searches were run across the public `jup-ag` GitHub organisation.

## Search groups

### Product and network names

```text
gum
jupnet
dove
```

### Messaging and verification

```text
proof_hash
msg_hash
inbox
outbox
request_claim
quorum
committee
```

### Cryptography

```text
bls
bn254
alt_bn128
merkle
aggregate signature
```

### Validator and stake terminology

```text
stake_weight
validator
vote
observer
```

## Initial results

| Query | Result |
|---|---|
| `jupnet` | `jup-ag/platform-list/src/platforms/gum.ts`; historical `vote-meta` files |
| `gum` | Many noisy substring matches; one high-signal exact platform definition in `platform-list` |
| `Dove` | Multiple `jupusd-program` files related to a Doves price oracle |
| `jupnet-svm` | No public result under `jup-ag` |
| combined BLS/BN254/Merkle terms | No direct public result in the initial search |
| combined proof/inbox/outbox terms | No direct public result in the initial search |

## Search-quality warning

The term `gum` is extremely noisy because it appears inside words such as `Bubblegum`. Results must be filtered for exact Gum/JupNet context.

The term `Dove` is also ambiguous. The `jupusd-program` result is currently classified as unrelated to JupNet validators because it deserialises an `AgPriceFeed` and treats Doves as one price-oracle type alongside Pyth and Switchboard.

## Next search passes

1. Search exact strings and known addresses from `platform-list`.
2. Search commit history, deleted files and pull requests for `gum`, `jupnet`, `BankK1Y...` and `bk1PDA...`.
3. Inspect forks and dependency lockfiles rather than repository names alone.
4. Search for known runtime crate names individually.
5. Track future changes to `platform-list/src/platforms/gum.ts`.
