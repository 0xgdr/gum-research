# Security Model Assessment

## Published model under investigation

The public model described Doves as full nodes that stake JUP and accept cross-chain messages once signatures representing at least two-thirds of staked JUP are present.

## Evidence supporting parts of the model

- Full validator nodes exist.
- Custom BLS-related components exist.
- Gum uses proof/message/inbox/outbox mechanics.
- Cross-chain verification infrastructure is clearly present.

## Missing proof

No public evidence was found for:

- JUP stake positions associated with validators;
- public Dove onboarding;
- JUP-weighted committee records;
- two-thirds stake calculations;
- slashing or rewards tied to JUP;
- validator-to-Solana-JUP-wallet mappings.

## Most plausible current explanations

### A. Private implementation

The validator software contains JUP-weighting configuration not exposed on-chain.

### B. Off-chain committee state

A private service or committee registry supplies stake weights and signer keys.

### C. Intended future architecture

The article describes the target system while the current private beta uses a team-controlled or equal-weight validator set.

### D. Hybrid design

Native stake secures the SVM chain, while JUP stake separately secures cross-chain messages.

## Current judgement

The investigation cannot responsibly select one explanation as proven.

The evidence is most consistent with a private or not-yet-public implementation boundary.
