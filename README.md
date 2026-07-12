# JupNet Technical Investigation

Independent reverse-engineering research into the JupNet private beta, Gum, Doves, native staking, vote traffic, BLS-related runtime components, OpenID, and the unresolved question of whether JUP currently provides stake-weighted economic security.

## Status

**Version:** 1.0  
**State:** Living investigation  
**Primary unresolved question:** Is validator/Dove security weight currently derived from JUP stake?

## Key conclusions

- JupNet is a customised SVM-based network.
- A live validator set, native vote accounts and native stake accounts were observed.
- Vote traffic was decoded and did not expose BLS signatures directly.
- Public dependency metadata references JupNet-specific BLS, BN254, Merkle and cross-chain crates.
- Gum exposes omnichain message and burn/mint behaviour.
- JUP is integrated into Gum asset flows.
- Public evidence does not currently prove that JUP stake determines validator or Dove voting weight.

## Repository map

- [`docs/00-executive-summary.md`](docs/00-executive-summary.md)
- [`docs/01-scope-and-methodology.md`](docs/01-scope-and-methodology.md)
- [`docs/02-network-and-validators.md`](docs/02-network-and-validators.md)
- [`docs/03-native-stake-and-vote.md`](docs/03-native-stake-and-vote.md)
- [`docs/04-runtime-and-cryptography.md`](docs/04-runtime-and-cryptography.md)
- [`docs/05-gum-and-jup-flows.md`](docs/05-gum-and-jup-flows.md)
- [`docs/06-openid-and-application-programs.md`](docs/06-openid-and-application-programs.md)
- [`docs/07-security-model-assessment.md`](docs/07-security-model-assessment.md)
- [`docs/08-evidence-matrix.md`](docs/08-evidence-matrix.md)
- [`docs/09-investigation-timeline.md`](docs/09-investigation-timeline.md)
- [`docs/10-continuation-plan.md`](docs/10-continuation-plan.md)
- [`docs/11-validator-security-layer-followup.md`](docs/11-validator-security-layer-followup.md)
- [`docs/12-monitoring-plan.md`](docs/12-monitoring-plan.md)
- [`appendices/rpc-catalogue.md`](appendices/rpc-catalogue.md)
- [`appendices/program-ids.md`](appendices/program-ids.md)
- [`appendices/scripts-index.md`](appendices/scripts-index.md)
- [`appendices/dead-ends.md`](appendices/dead-ends.md)
- [`evidence/2026-07-12-live-rpc/analysis.md`](evidence/2026-07-12-live-rpc/analysis.md)
- [`evidence/2026-07-12-live-rpc/deep-dive.md`](evidence/2026-07-12-live-rpc/deep-dive.md)

## Evidence classifications

- **Confirmed** — directly observed through RPC, transaction data, program state or executable metadata.
- **Strong evidence** — multiple independent observations support the conclusion.
- **Working hypothesis** — plausible but not yet directly verified.
- **Unverified** — claim could not be demonstrated from accessible evidence.

## Important caution

A token `Burn` instruction is not automatically deflationary. In an omnichain design, a burn may be paired with a mint elsewhere. Permanent supply reduction requires matching source burns, destination mints and canonical supply changes.
