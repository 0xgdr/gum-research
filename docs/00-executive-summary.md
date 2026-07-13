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
- Root-update authority graphing found the decoded root update was submitted by one unknown transaction signer, wrote only the outbox root-history account, and had zero overlap with parsed Gum/Bank/inbox/outbox upgrade authorities or canonical JUP/current validator/vote/stake keys.
- Root submitter provenance found that signer only once in the saved transaction corpus, as the outbox root-update signer/payer, with only a 5000 lamport fee delta and no token-balance movement or JUP/validator/stake overlap.
- Direct root submitter history fetched 30 recent transactions for `6f5mu...`; all 30 were outbox `UpdateMerkleRoot` calls, invoked only `jnoUtn...`, paid only transaction fees, and exposed no JUP, validator/vote/stake, token-balance or upgrade-authority intersections.
- Root submitter funding-history analysis found one older positive funding/setup event for `6f5mu...`; the transaction flowed through the Solana-side Gum Bank request path, invoked an inner withdrawal program, emitted `jupnet`, `message_hash` and `Signature verified` logs, and still exposed no canonical JUP or validator/vote/stake security source.
- Security boundary corpus analysis decoded 42 verifier payloads across 128 local Bank/outbox/history transaction files and found zero canonical JUP/current validator/vote/stake key hits, zero root mismatches and no visible signer-set/quorum/weight state in helper-owned accounts.
- Private runtime fingerprint analysis found `jupnet_bn254` and `jupnet_crosschain_hash` in one public Gum omnichain ProgramData binary, while still finding zero Dove/stake-weight/quorum/root-builder producer terms.
- Gum omnichain binary-role analysis shows `brhPf...` is the richer/full verifier candidate with BN254, cross-chain-hash and alt-BN128 BLS symbols, while `GUMeb...` is the recovered outbox verifier sender/program id.
- Gum account-role reconstruction found no direct sampled top-level `GUMeb...` calls; the visible public roles split across `brhPf...` admin/config transactions, Solana Bank request/asset operations and outbox proof verification.
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
- **Root-update authority graph:** the public update path resolves to a transaction signer/payer submitting an outbox helper update that writes the root-history account after BLS/Merkle verification; the sampled signer is not a known parsed upgrade authority and does not intersect canonical JUP or current validator/vote/stake keys.
- **Root submitter provenance:** within the saved corpus, the root-update signer appears as a narrow outbox-root publisher rather than a broad Gum/Bank operator; full provenance still requires direct address-history collection.
- **Root submitter direct history:** the direct 30-transaction signature window shows a dedicated automated root publisher pattern, with regular `UpdateMerkleRoot` calls and no observed token or security-state intersections.
- **Root submitter funding history:** paging further back finds the setup/funding event for `6f5mu...` inside a Gum Bank request/withdrawal flow, linking the public root publisher to Gum/JupNet operations while still leaving the Dove/JUP/stake producer side hidden.
- **Security boundary corpus:** the helper accounts and wider verifier corpus strengthen the public BLS/Merkle verifier model, but still stop at the aggregate-key inclusion boundary rather than exposing the Dove/JUP/stake producer side.
- **Private runtime fingerprints:** public Gum omnichain executable bytes expose JupNet-specific BN254 and cross-chain hash crate fingerprints, but not the private root-builder, Dove registry or JUP stake-weight implementation.
- **Gum binary roles:** `brhPf...` carries the strongest public crypto/verifier linkage; `GUMeb...` carries the sender/application role seen in verifier payloads.
- **Account roles:** sampled account metas expose application/config/request/proof roles, not JUP staking, Dove weights, validator mappings or quorum state.
- **JUP utility/security:** described publicly for Dove security, but not independently verifiable from the beta artifacts inspected.

This does not disprove the intended JUP security model. It establishes an evidence boundary: the implementation is either private, off-chain, not yet activated, or not publicly exposed in the beta.
