# Jupiter Public Repository Archaeology

## Purpose

This index records public Jupiter repositories and files that are potentially relevant to Gum, JupNet, Doves, cross-chain verification, BLS, BN254, Merkle proofs, inbox/outbox messaging and JUP staking.

## High-signal repositories

| Repository | Relevance | Current finding |
|---|---|---|
| `jup-ag/platform-list` | High | Contains an explicit `GUM` platform entry and identifies the Solana-side Bank and Bank Program addresses. |
| `jup-ag/jupusd-program` | Medium | Contains a type named `DovesOracle`, but source inspection shows this is a price-oracle integration rather than evidence of JupNet Dove validators. |
| `jup-ag/vote-meta` | Low/unknown | Search results mention `jupnet` in historical governance metadata files. These require contextual review and are not protocol source. |
| `jup-ag/jupiter-amm-implementation` | Low | Search matches for `Dove` appear in generated/interface data and currently provide no evidence of JupNet validator logic. |

## Confirmed Gum source clue

The strongest direct public Gum reference found so far is:

```text
jup-ag/platform-list/src/platforms/gum.ts
```

It defines:

```text
Platform ID: gum
Platform name: GUM
Parent: Jupiter
Service: Global Deposit
Bank account: bk1PDAkbHEBGtVRiM94Lzets8gVFP7FgySyfkAc8MPN
Bank Program: BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ
Network: Solana
```

This is important because it gives two concrete Solana-side addresses for continued investigation.

## Negative result

No public repository named `gum` was found under `jup-ag` in the initial repository-name search.

No public `jupnet-svm` source was found under `jup-ag`. The previously identified `jupnet/jupnet-svm` reference remains a private-source boundary.

## Interpretation discipline

A repository or symbol containing the word `Doves` must not automatically be treated as JupNet Dove-validator evidence. For example, `jupusd-program` uses a `Doves` oracle alongside Pyth and Switchboard. That is an oracle provider integration, not validator-staking logic.
