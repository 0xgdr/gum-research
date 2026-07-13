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
10. Crawl public Jupiter repositories and follow the `jup-ag/platform-list` GUM Bank lead.

## Confirmed

- JupNet is a live, independent SVM-derived chain.
- It has a native validator set.
- Validators have native vote accounts.
- Native stake accounts are delegated to vote accounts.
- Gum implements cross-chain message and asset flows.
- Public Jupiter registry data points to Solana-side GUM Bank programs.
- Solana-side Bank Program samples expose inbox/outbox message handling.
- Solana-side Bank account analysis derives a repeated `__inbox_event_auth` PDA.
- Recurring Solana-side Bank account state shows USDC/wrapped SOL token accounts and compact Bank state, but no canonical JUP or validator-key hits.
- Owner-context analysis ties recurring non-token Bank state to JupNet inbox and outbox helper programs on Solana mainnet.
- Helper-program account enumeration shows the public outbox account stores Merkle root history, not visible signer-set or JUP-weight state.
- `verify_request` payload reconstruction shows Merkle proof data and USDC context, but no visible JUP or validator-security fields.
- Outbox root-update transaction analysis confirms public BLS signature verification during Merkle-root publication.
- Outbox update payload reconstruction confirms the sampled root-update transaction bytes reproduce the public JupNet article's Merkle leaf and parent hash formulas.
- Epoch security-source hunting finds the same candidate aggregate-key material in multiple verification payloads, but not co-located with JUP, validator, vote or stake keys.
- Outbox verifier payload mapping matches the public article's field shape: message hash, sender/program id, epoch, aggregate-key material, compact signature/verifier field and Merkle proof.
- The recovered sender/program id resolves to JupNet `gum-omnichain`, which exposes deposit, withdrawal, swap, inbox/outbox and BLS/Merkle verification strings.
- JupNet executable census found `sol_verify_bls_merkle_key` in two Gum omnichain executables, but did not expose Dove/JUP/stake-weight source material.
- Outbox root-history analysis found one decoded root update and 19 decoded verifier payloads across 120 local outbox transaction files, with no canonical JUP or validator/vote/stake key exposure.
- Security boundary corpus analysis decoded 42 verifier payloads across 128 local Bank/outbox/history transaction files and found zero canonical JUP/current validator/vote/stake key hits, zero root mismatches and no visible signer-set/quorum/weight state in helper-owned accounts.
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
- Canonical JUP usage in sampled Solana-side Bank Program transactions.

## Current assessment

The strongest current model is:

- **SVM consensus layer:** native validators, vote accounts and native stake.
- **Cross-chain security layer:** custom BLS/Merkle machinery, likely implemented in validator/runtime software or private infrastructure.
- **Solana-side Bank layer:** public registry-linked executable programs that handle inbox/outbox message flow, observed with USDC/wrapped SOL but not canonical JUP in the sampled transactions.
- **Bank account graph:** one repeated account matches the Bank Program `__inbox_event_auth` PDA, strengthening the inbox/event-authority interpretation.
- **Recurring Bank state:** high-frequency Bank accounts include compact Bank-owned records and USDC/wrapped SOL token accounts, with no observed canonical JUP state.
- **Owner helper programs:** recurring non-token Bank state is linked to upgradeable JupNet inbox/outbox programs with Merkle/BLS/outbox verification strings.
- **Helper program state:** the outbox helper owns one 320-byte Merkle-root-history account; the signer-set/quorum source is not visible there.
- **Per-request verification:** sampled `verify_request` payloads carry proof/message fields against outbox roots, with no observed JUP or validator-key material.
- **Root publication:** sampled `UpdateMerkleRoot` logs show Merkle proof verification and BLS signature verification before an outbox root is stored.
- **Root-update payload:** the sampled 305-byte update payload proves a 64-byte candidate aggregate key into the epoch root using `SHA256(0x00 || key)` leaves and `SHA256(0x01 || left || right)` parents.
- **Epoch source hunt:** scanning 3153 saved binary records found the candidate aggregate key in repeated verification payloads, but found zero co-location with canonical JUP or current validator/vote/stake keys.
- **Verifier payloads:** 21 sampled Bank/outbox verifier payloads map to the article's outbox argument shape and recompute to the stored outbox root.
- **Gum omnichain sender:** the verifier sender/program id is a live upgradeable JupNet program with `programs/gum-omnichain` strings and `sol_verify_bls_merkle_key`.
- **Executable census:** all 23 visible JupNet upgradeable executables were fetched; two Gum omnichain binaries contain `sol_verify_bls_merkle_key`, and zero expose canonical JUP or current validator/vote/stake keys.
- **Root history:** a widened outbox history window found one root update and 19 verifier payloads; verifier aggregate keys varied, but every decoded verifier root landed on the same stored root and no decoded row exposed JUP or validator/stake key material.
- **Security boundary corpus:** the helper accounts and wider verifier corpus strengthen the public BLS/Merkle verifier model, but still stop at the aggregate-key inclusion boundary rather than exposing the Dove/JUP/stake producer side.
- **JUP utility/security:** described publicly for Dove security, but not independently verifiable from the beta artifacts inspected.

This does not disprove the intended JUP security model. It establishes an evidence boundary: the implementation is either private, off-chain, not yet activated, or not publicly exposed in the beta.
