# JupNet Technical Investigation

Independent reverse-engineering research into the JupNet private beta, Gum, Doves, native staking, vote traffic, BLS-related runtime components, OpenID, and the unresolved question of whether JUP currently has protocol utility beyond being a tradable Gum asset.

## Status

**Version:** 1.0  
**State:** Living investigation  
**Primary unresolved question:** Is validator/Dove security weight, protocol access, fee flow, burn/sink behavior, governance control or any other Gum/JupNet utility currently derived from JUP?

## Research focus

This repo is not trying to prove that JUP can be traded on Gum. Treat JUP trading, bridging, transfer, burn/mint routing and asset metadata as background unless the evidence connects JUP to protocol utility.

Utility-relevant evidence includes:

- JUP stake or lock records tied to validators, Doves, signers or operators.
- Signer weights, quorum thresholds or BLS verifier configs denominated in JUP.
- JUP fees, fee sinks, permanent burns or settlement costs required by Gum/JupNet.
- Governance, upgrade, access-control or slashing/reward mechanisms keyed to JUP.
- Validator/Dove registration or onboarding that requires JUP.

## Key conclusions

- JupNet is a customised SVM-based network.
- A live validator set, native vote accounts and native stake accounts were observed.
- Vote traffic was decoded and did not expose BLS signatures directly.
- Public dependency metadata references JupNet-specific BLS, BN254, Merkle and cross-chain crates.
- Gum exposes omnichain message and burn/mint behaviour, but asset flow alone is not utility evidence.
- Public Jupiter registry data exposes Solana-side GUM Bank programs with inbox/outbox message logs.
- Bank account-graph analysis links a repeated account to the Bank Program `__inbox_event_auth` PDA.
- Recurring Bank account-state analysis found USDC/wrapped SOL token accounts and compact Bank state, but no canonical JUP or validator-key hits.
- Bank owner-context analysis ties recurring non-token state to JupNet inbox/outbox helper programs on Solana mainnet.
- Helper-program account enumeration shows public outbox state stores Merkle root history, not visible signer-set or JUP-weight state.
- `verify_request` payload reconstruction shows message/proof data and USDC context, but no JUP, validator keys or visible quorum state.
- JUP appears in Gum asset metadata/flows; this is confirmed but treated as non-decisive noise unless tied to protocol utility.
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
- [`docs/13-utility-evidence-standard.md`](docs/13-utility-evidence-standard.md)
- [`docs/14-public-jupiter-source-audit.md`](docs/14-public-jupiter-source-audit.md)
- [`docs/15-bank-program-followup.md`](docs/15-bank-program-followup.md)
- [`docs/16-bank-program-reverse-engineering.md`](docs/16-bank-program-reverse-engineering.md)
- [`docs/17-bank-account-graph-and-pda-hunt.md`](docs/17-bank-account-graph-and-pda-hunt.md)
- [`docs/18-bank-recurring-account-state.md`](docs/18-bank-recurring-account-state.md)
- [`docs/19-bank-owner-program-context.md`](docs/19-bank-owner-program-context.md)
- [`docs/20-jupnet-helper-program-state.md`](docs/20-jupnet-helper-program-state.md)
- [`docs/21-verify-request-payload-reconstruction.md`](docs/21-verify-request-payload-reconstruction.md)
- [`appendices/rpc-catalogue.md`](appendices/rpc-catalogue.md)
- [`appendices/program-ids.md`](appendices/program-ids.md)
- [`appendices/scripts-index.md`](appendices/scripts-index.md)
- [`appendices/dead-ends.md`](appendices/dead-ends.md)
- [`research/repositories.md`](research/repositories.md)
- [`evidence/2026-07-12-live-rpc/analysis.md`](evidence/2026-07-12-live-rpc/analysis.md)
- [`evidence/2026-07-12-live-rpc/deep-dive.md`](evidence/2026-07-12-live-rpc/deep-dive.md)
- [`evidence/2026-07-12-live-rpc/authorization.md`](evidence/2026-07-12-live-rpc/authorization.md)
- [`evidence/2026-07-12-live-rpc/utility-classification.md`](evidence/2026-07-12-live-rpc/utility-classification.md)
- [`evidence/2026-07-12-bank-live-rpc/solana-bank.md`](evidence/2026-07-12-bank-live-rpc/solana-bank.md)
- [`evidence/2026-07-12-bank-live-rpc/bank-reverse-engineering.md`](evidence/2026-07-12-bank-live-rpc/bank-reverse-engineering.md)
- [`evidence/2026-07-12-bank-live-rpc/bank-account-graph.md`](evidence/2026-07-12-bank-live-rpc/bank-account-graph.md)
- [`evidence/2026-07-12-bank-live-rpc/bank-recurring-account-state.md`](evidence/2026-07-12-bank-live-rpc/bank-recurring-account-state.md)
- [`evidence/2026-07-12-bank-live-rpc/bank-owner-program-context.md`](evidence/2026-07-12-bank-live-rpc/bank-owner-program-context.md)
- [`evidence/2026-07-12-bank-live-rpc/jupnet-helper-program-accounts.md`](evidence/2026-07-12-bank-live-rpc/jupnet-helper-program-accounts.md)
- [`evidence/2026-07-12-bank-live-rpc/verify-request-payload-reconstruction.md`](evidence/2026-07-12-bank-live-rpc/verify-request-payload-reconstruction.md)

## Evidence classifications

- **Confirmed** — directly observed through RPC, transaction data, program state or executable metadata.
- **Strong evidence** — multiple independent observations support the conclusion.
- **Working hypothesis** — plausible but not yet directly verified.
- **Unverified** — claim could not be demonstrated from accessible evidence.
- **Non-decisive asset evidence** — confirms JUP appears in trading, routing, transfer, mint/burn or metadata surfaces, but does not prove protocol utility.

## Important caution

A token `Burn`, `MintTo`, transfer, market route or Gum asset record is not utility evidence by itself. In this repo, those observations are only useful when they reveal JUP-denominated stake, signer weight, fee capture, permanent supply sink, governance control, access control or validator/Dove participation.
