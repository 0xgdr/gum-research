# Utility Evidence Standard

## Purpose

This repo is focused on one detective question:

```text
What, if anything, does JUP do for Gum/JupNet beyond being a tradable asset?
```

JUP trading on Gum is treated as already established background. It is not the target.

## Not Utility Evidence

The following are noise unless they connect to a protocol mechanism:

- JUP can be traded on Gum.
- JUP appears as a supported asset.
- JUP appears as base58 text in asset metadata.
- A JUP transfer appears in a Gum route.
- A JUP burn is paired with a mint in an omnichain flow.
- A token account, associated token account or mint appears in a trade path.
- A transaction log mentions asset movement without showing who controls security or settlement.

These observations may help map Gum, but they do not answer whether JUP has protocol utility.

## Utility Evidence

The following would be utility-relevant:

- JUP stake, lock or escrow accounts tied to validators, Doves, signers or operators.
- JUP-denominated signer weights.
- A quorum threshold calculated from JUP balances or delegated JUP.
- BLS/verifier config that maps signers to JUP weights.
- Validator or Dove registration requiring JUP.
- Slashing, rewards or penalties denominated in JUP.
- Gum/JupNet fees paid in JUP.
- A permanent protocol-level JUP burn or fee sink, not merely a bridge burn paired with a mint.
- Governance, upgrade authority or access-control rules keyed to JUP.
- Runtime or validator code using JUP for security, fee or access decisions.

## Classification Rules

### Confirmed Utility

Use only when public evidence directly links JUP to a protocol mechanism such as staking, weights, fees, access control, governance, slashing, rewards or permanent supply sinks.

### Strong Utility Evidence

Use when multiple independent observations point to the same JUP utility mechanism but one decisive artifact is still missing.

### Non-Decisive Asset Evidence

Use for trade, transfer, mint, burn, route, asset metadata or token-account evidence that shows JUP is supported by Gum but does not show why the protocol needs JUP.

### Not Observed

Use when a targeted scan finds no public evidence of the utility mechanism being tested.

## Current Working Boundary

As of the 2026-07-12 snapshot:

- JUP asset metadata in Gum is confirmed.
- The 127 Gum JUP text-hit accounts are classified as non-decisive asset metadata or route config.
- JUP as native validator stake is not observed.
- JUP-denominated Dove or signer weights are not observed.
- JUP-weighted quorum enforcement is not observed.
- JUP fee, sink, governance, slashing or reward utility is not observed.

The highest-value next evidence would be a signer/validator/Dove registry, verifier config, staking/lock account, fee account or source code path that uses JUP for protocol decisions.
