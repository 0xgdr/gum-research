# Network and Validator Analysis

## Independent chain evidence

The RPC returned an independent slot height and chain identity, demonstrating that JupNet is not merely an RPC proxy to Solana mainnet.

A chain identity was returned:

```text
HbzR4TxZsfiNm3VFkuQVpV6CSzfVU3k2zqh1D2sFRTNn
```

## Validator nodes

`getClusterNodes` returned multiple validator identities with gossip, TVU, TPU, RPC and PubSub endpoints.

Examples included validator identities beginning with:

```text
idtWF336...
idtcqyhG...
idtxyt9...
idtwvwF...
idt4cGQc...
```

Node versions observed included JupNet version strings such as `1.1.5`, `1.1.6` and `1.1.7`.

## Interpretation

This strongly supports a customised Solana-derived validator implementation. The network exposes the expected Solana validator networking surfaces while using JupNet-specific binaries and versioning.

## What this does not prove

The validator list alone does not prove:

- validators are community operated;
- validators are permissionless;
- validators are weighted by JUP;
- validator identities correspond directly to Dove identities described publicly.
