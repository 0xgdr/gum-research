# Outbox Root Update Transactions

## Scope

- Outbox helper program: `jnoUtncGR9ZCCMixtys6Gzy5coTo6mnmUZuEHRQFTFV`
- Transaction files scanned: `20`
- Top-level outbox instructions found: `1`
- Update/BLS candidate instructions: `1`
- Canonical JUP key hits: `0`
- Current JupNet validator/vote/stake key hits: `0`

## Instruction Variants

| Count | Discriminator | Data length | Account count |
|---:|---|---:|---:|
| 1 | `010f010000000000` | 305 | 1 |

## Relevant Logs

- `Program log: UpdateMerkleRoot invoked`: `1`
- `Program log: Merkle proof verified`: `1`
- `Program log: Verifying BLS signature`: `1`
- `Program log: Signature verified`: `1`
- `Program log: advance_epoch_root: dropped root of epoch 268:`: `1`

## Transaction Rows

| File | Slot | Time | Discriminator | Data len | Accounts | Signers | Writable accounts | Key hits | Payload hits | Logs |
|---|---:|---|---|---:|---:|---|---|---|---|---|
| `solana-mainnet-outbox-tx-3Zjq8FZd.json` | 432511387 | `2026-07-12T21:25:50+00:00` | `010f010000000000` | 305 | 1 | `None` | `3C1LxtpR3Mh5RQjydfeQdvRaAzpStWM7gBi1XzP9oyGt` | `Outbox Program: jnoUtncGR9ZCCMixtys6Gzy5coTo6mnmUZuEHRQFTFV`<br>`Outbox root account: 3C1LxtpR3Mh5RQjydfeQdvRaAzpStWM7gBi1XzP9oyGt` | `None` | `Program log: UpdateMerkleRoot invoked`<br>`Program log: Merkle proof verified`<br>`Program log: Verifying BLS signature`<br>`Program log: Signature verified`<br>`Program log: advance_epoch_root: dropped root of epoch 268:` |

## Payload Shape Hints

| Discriminator | Data len | Small aligned u64 candidates |
|---|---:|---|
| `010f010000000000` | 305 | `None` |

## Decoded Update Payload

### `solana-mainnet-outbox-tx-3Zjq8FZd.json`

- Tag byte: `1`
- Epoch/root slot candidate: `271`
- Merkle root: `6928957b2ea436bcc9c44970a0f85364b6f0c8e5e4e886565eea061c9bd8d999`
- Message/leaf candidate: `1936cf6325733174d35ff22f86bebabdf33abd441315398d8d4b61313eda628d`
- Proof node count: `5`
- Tail after proof nodes: `1200000087e930814a0131f70e4b405f4e30ca3e226ad5bee2e5e40d584947d48c4bcceb15f96af18671975c31abc6d2c3ea8230ee775da12cd69b5331e35865ad2c4025`

| Node index | Hex |
|---:|---|
| 0 | `97375839a6a19a2382b9958796df46161a113362aad11143cb547a7867b05fdf` |
| 1 | `d62d10c2522c7d52ec0da4227e3e361067970b648f35d2a746430197e8a1d271` |
| 2 | `7e8cab4245423af57ff7f95f2c46b21c7fbf2b4267ba056ec66abbacbed1f78b` |
| 3 | `2a2271f4288574d17854d87120c1c0cfc6335b8a9f83e85fdb9acd9c1cc3dc7d` |
| 4 | `d90c3226b4e2a82538f6f1fee4d3f4892d319a391d084cf66fbab40a03994a8f` |


## Assessment

- Recent outbox helper transactions include update/BLS log candidates; inspect payload rows above for signer/quorum evidence.
- No scanned outbox transaction exposed canonical Solana JUP key material.
- No scanned outbox transaction exposed current JupNet validator, vote or stake account keys.
- If BLS quorum material is present here, it is not visible as direct JUP, validator/vote/stake account references in the sampled transaction keys or payload bytes.
