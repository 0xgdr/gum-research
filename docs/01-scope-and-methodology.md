# Scope and Methodology

## Scope

The investigation focused on JUP protocol utility, architecture and security, not trading support, trading performance or token-price forecasting.

JUP trading on Gum is treated as background. It is only relevant when a transaction or account exposes JUP-denominated security, signer weights, fees, access control, governance, permanent burns/sinks, rewards, slashing or validator/Dove participation.

Primary questions:

1. Is JupNet an independent chain or an application layer?
2. Are Doves equivalent to native validators?
3. What role does native stake play?
4. Where is BLS used?
5. Does Gum require, consume, sink or permanently burn JUP for protocol operation rather than ordinary asset routing?
6. Can JUP-weighted security or any other JUP utility be proven from the beta?

## Methods

### RPC interrogation

The live endpoint used during the investigation was:

```text
https://mainnet-beta-rpc.jup.net/
```

Standard Solana-style JSON-RPC methods were used, including:

- `getSlot`
- `getIdentity`
- `getClusterNodes`
- `getProgramAccounts`
- `getAccountInfo`
- `getSignaturesForAddress`
- `getTransaction`

### Transaction analysis

Transactions were fetched in both parsed and raw JSON encodings. Instruction decoding was corrected to account for raw `programIdIndex` references.

### Program analysis

Upgradeable and legacy BPF executables were enumerated. Upgradeable ProgramData accounts were fetched and binaries dumped for string inspection.

### Dependency analysis

Public repository lockfiles were searched for JupNet-specific crates and source references.

### Confidence discipline

Negative findings are expressed as “not observed” or “not verified,” not as proof of absence.
