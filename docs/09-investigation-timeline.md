# Investigation Timeline

## Phase 1 — RPC discovery

- Connected to the private-beta RPC.
- Confirmed live slot progression.
- Retrieved chain identity.
- Enumerated validator nodes.

## Phase 2 — Native consensus surface

- Queried stake-program accounts.
- Identified delegated native stake.
- Mapped stake accounts to vote accounts.
- Distinguished native stake from SPL JUP staking.

## Phase 3 — Program and registry mapping

- Enumerated OpenID Registry accounts.
- Decoded binary and printable metadata.
- Determined OpenID was primarily identity-oriented.

## Phase 4 — Gum and JUP

- Located canonical JUP mint in Gum state.
- Traced JUP transfer/burn/mint activity.
- Identified proof/inbox/outbox message logs.
- Separated “JUP used by Gum” from “JUP secures Gum.”

## Phase 5 — Vote decoding

- Captured recent vote transactions.
- Corrected raw-instruction program-index decoding.
- Analysed fixed-format vote payloads.
- Found no direct BLS aggregate signature payload.

## Phase 6 — Runtime and dependencies

- Enumerated NativeLoader programs.
- Found JupNet-labelled loader strings.
- Searched public repositories.
- Located JupNet-specific cryptographic crates in lockfiles.
- Identified inaccessible private `jupnet-svm` source reference.

## Phase 7 — Executable scan

- Dumped upgradeable and legacy program binaries.
- Extracted strings.
- Classified application programs.
- Found no clearly labelled on-chain Dove/JUP consensus coordinator.

## Phase 8 — Evidence boundary

- Tested local cache/artifact possibilities.
- Determined further local-file hunting was low-value.
- Concluded validator-side/private implementation is the main unresolved boundary.
