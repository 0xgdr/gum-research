# Root Submitter Provenance

## Scope

- Snapshot: `evidence/2026-07-12-bank-live-rpc`
- Root-update submitters derived from decoded root updates: `1`
- Saved transaction bodies scanned: `36`
- Transactions containing a root-update submitter: `1`
- Transactions where a root-update submitter is a signer: `1`
- Submitter account-data hits outside transaction bodies: `0`

## Submitter Summary

| Submitter | Tx occurrences | Signer occurrences | Security intersections | Upgrade-authority intersections | Account-data hits |
|---|---:|---:|---|---|---|
| `6f5muRjigWVnoQHfXWLeXFfafUqMVJfzoBBJL8Gwquji` | 1 | 1 | `None` | `None` | `None` |

## Transaction Occurrences

| File | Time | Slot | Signature | Submitter signer | Root update | Balance delta | Programs | Relevant logs |
|---|---|---:|---|---|---|---|---|---|
| `solana-mainnet-outbox-tx-3Zjq8FZd.json` | `2026-07-12T21:25:50+00:00` | 432511387 | `3Zjq8FZdd9sr...` | `True` | `True` | `pre=2127875131 post=2127870131 delta=-5000 fee=5000` | `jnoUtncGR9ZCCMixtys6Gzy5coTo6mnmUZuEHRQFTFV` | `Program log: UpdateMerkleRoot invoked`<br>`Program log: Merkle proof verified`<br>`Program log: Verifying BLS signature`<br>`Program log: Signature verified` |

## Co-Occurrence Summary

| Group | Values |
|---|---|
| Programs invoked with submitter | `jnoUtncGR9ZCCMixtys6Gzy5coTo6mnmUZuEHRQFTFV: 1` |
| Repeated co-accounts | `jnoUtncGR9ZCCMixtys6Gzy5coTo6mnmUZuEHRQFTFV: 1`<br>`3C1LxtpR3Mh5RQjydfeQdvRaAzpStWM7gBi1XzP9oyGt: 1` |
| Known co-account roles | `Solana JupNet outbox helper executable: 1`<br>`outbox Merkle root-history account: 1` |

## Funding And Asset Clues

- `6f5muRjigWVnoQHfXWLeXFfafUqMVJfzoBBJL8Gwquji` in `solana-mainnet-outbox-tx-3Zjq8FZd.json` had lamport delta `-5000` with transaction fee `5000`; token-balance hints: `None`

## Assessment

- Within the saved corpus, the root-update submitter appears as a narrow outbox-root publisher rather than a broad Gum/Bank operator.
- The observed transaction only paid the Solana transaction fee and wrote the outbox root-history account; no token balance movement was attached to the submitter.
- The saved corpus does not show the submitter touching canonical JUP, current validator/vote/stake accounts, parsed upgrade authorities, signer-set accounts, quorum state, slashing state or rewards.
- Full provenance still requires collecting a direct signature window for the submitter address and walking its funding history.
