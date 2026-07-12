# Scope and Methodology

## Scope

The investigation focused on architecture and security, not trading performance or token-price forecasting.

Primary questions:

1. Is JupNet an independent chain or an application layer?
2. Are Doves equivalent to native validators?
3. What role does native stake play?
4. Where is BLS used?
5. Does Gum consume, bridge or permanently burn JUP?
6. Can JUP-weighted security be proven from the beta?

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
