# Executive Summary

This investigation began with a narrow question: **does JUP secure JupNet/Gum through Dove staking?**

Public material had described Doves as full-node operators that stake JUP and accept cross-chain messages when signatures representing at least two-thirds of staked JUP are present. The private beta provided enough access to interrogate the live chain, but not the validator source.

The investigation therefore proceeded from observable evidence:

1. Connect to the JupNet RPC.
2. Enumerate validators and network contact information.
3. Inspect native vote and stake accounts.
4. Decode recent vote transactions.
5. Enumerate program-owned accounts and deployed executables.
6. Decode OpenID Registry state.
7. Trace Gum-related JUP transactions only to separate asset support from utility.
8. Inspect executable strings and public dependency metadata.
9. Compare observed implementation with the published security model.

## Confirmed

- JupNet is a live, independent SVM-derived chain.
- It has a native validator set.
- Validators have native vote accounts.
- Native stake accounts are delegated to vote accounts.
- Gum implements cross-chain message and asset flows.
- JUP appears in Gum state and transaction flows as an asset.
- JUP burn and mint operations were observed in omnichain activity, but these are non-decisive unless tied to protocol utility.
- Public dependency metadata points to JupNet-specific BLS, BN254, Merkle and syscall components.

## Not confirmed

- A public Dove registry.
- Public JUP staking on JupNet.
- A validator-to-JUP-wallet mapping.
- Stake weights derived from JUP.
- A two-thirds-of-staked-JUP quorum visible on-chain.
- BLS aggregate signatures embedded directly in ordinary vote transactions.
- JUP-denominated fees, governance, access control, rewards, slashing or permanent protocol sinks.

## Current assessment

The strongest current model is:

- **SVM consensus layer:** native validators, vote accounts and native stake.
- **Cross-chain security layer:** custom BLS/Merkle machinery, likely implemented in validator/runtime software or private infrastructure.
- **JUP utility/security:** described publicly for Dove security, but not independently verifiable from the beta artifacts inspected.

This does not disprove the intended JUP security model. It establishes an evidence boundary: the implementation is either private, off-chain, not yet activated, or not publicly exposed in the beta.
