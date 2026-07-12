# Gum and JUP Asset Flows

## Gum state

The canonical JUP mint was found in Gum-related state:

```text
JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN
```

This confirms that JUP is configured as a supported asset in the omnichain system.

## Observed transaction flow

A traced flow included:

```text
TransferChecked
Burn
MintTo
```

The transferred and burned JUP amounts matched at token precision in the inspected example.

Logs also included message-oriented fields such as:

```text
outbox msg_hash
request_claim
proof_hash
inbox_hash
```

## Interpretation

The strongest interpretation is a cross-chain burn/mint or unified-asset flow.

This proves JUP is used by Gum as an asset.

It does **not** prove the burn is permanently deflationary.

## Permanent burn test

For a burn to be counted as permanent, investigators should verify:

1. The JUP mint burned.
2. The amount and decimals.
3. The associated Gum message hash.
4. Whether a corresponding representation was minted on JupNet or another chain.
5. Whether canonical total supply decreased.
6. Whether any reverse settlement later reissued the amount.

## Price relevance

A bridge burn paired with a destination mint is supply-neutral across the system.

A permanent, unmatched burn reduces system-wide supply and may be price-supportive if demand remains unchanged or rises.
