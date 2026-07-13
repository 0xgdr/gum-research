# Root Update Authority Graph

## Scope

- Snapshot: `evidence/2026-07-12-bank-live-rpc`
- Outbox helper program: `jnoUtncGR9ZCCMixtys6Gzy5coTo6mnmUZuEHRQFTFV`
- Outbox root-history account: `3C1LxtpR3Mh5RQjydfeQdvRaAzpStWM7gBi1XzP9oyGt`
- Transaction files scanned: `120`
- Decoded root-update transactions: `1`
- Unique transaction signers on root updates: `1`
- Unique instruction signers on root updates: `0`
- Unique instruction writable accounts on root updates: `1`
- Root-update accounts intersecting canonical JUP/current validator/vote/stake keys: `0`
- Root-update accounts intersecting known upgrade authorities: `0`

## Control Graph

| Edge | Evidence |
|---|---|
| `root-update tx signer -> jnoUtncGR9ZCCMixtys6Gzy5coTo6mnmUZuEHRQFTFV` | `6f5muRjigWVnoQHfXWLeXFfafUqMVJfzoBBJL8Gwquji: 1` |
| `instruction signer -> UpdateMerkleRoot` | `None` |
| `UpdateMerkleRoot -> writable accounts` | `3C1LxtpR3Mh5RQjydfeQdvRaAzpStWM7gBi1XzP9oyGt: 1` |
| `UpdateMerkleRoot -> root values` | `6928957b2ea436bc...: 1` |
| `UpdateMerkleRoot -> aggregate-key material` | `87e930814a0131f7...: 1` |

## Root Update Rows

| Time | Slot | File | Epoch | Root | Aggregate key | Tx signers | Instruction signers | Instruction writable accounts | Logs |
|---|---:|---|---:|---|---|---|---|---|---|
| `2026-07-12T21:25:50+00:00` | 432511387 | `solana-mainnet-outbox-tx-3Zjq8FZd.json` | 271 | `6928957b2ea436bc...` | `87e930814a0131f7...` | `6f5muRjigWVnoQHfXWLeXFfafUqMVJfzoBBJL8Gwquji` | `None` | `3C1LxtpR3Mh5RQjydfeQdvRaAzpStWM7gBi1XzP9oyGt` | `Program log: UpdateMerkleRoot invoked`<br>`Program log: Merkle proof verified`<br>`Program log: Verifying BLS signature`<br>`Program log: Signature verified` |

## Root Update Participant Roles

| Account | Count | Role |
|---|---:|---|
| `6f5muRjigWVnoQHfXWLeXFfafUqMVJfzoBBJL8Gwquji` | 1 | `unknown` |
| `3C1LxtpR3Mh5RQjydfeQdvRaAzpStWM7gBi1XzP9oyGt` | 1 | `outbox Merkle root-history account` |

## Program Upgrade Authorities

| ProgramData surface | Deployment slot | Upgrade authority | Authority appears in root updates |
|---|---:|---|---|
| `JupNet Gum brhPf ProgramData` | 8167938 | `E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9` | `False` |
| `JupNet Gum GUMeb ProgramData` | 106613674 | `7RrBcJS6vbyMdLoYxQUqiUxD3CYVD55FvsGS5L5rfx2x` | `False` |
| `Solana Bank ProgramData` | 425956918 | `F5p1mBd6C3v6NB2oLGM9bLKmtHQ53RMsYKeGPPg4s113` | `False` |
| `Solana Bank Program ProgramData` | 432453318 | `GRr146QcbpANhTZPCo9QBJa1tP5Fr9B6vfua4zRC5cc3` | `False` |
| `Solana Inbox helper ProgramData` | 416240879 | `GRr146QcbpANhTZPCo9QBJa1tP5Fr9B6vfua4zRC5cc3` | `False` |
| `Solana Outbox helper ProgramData` | 431537850 | `GRr146QcbpANhTZPCo9QBJa1tP5Fr9B6vfua4zRC5cc3` | `False` |

## Security Intersections

- No root-update account, signer or writable account intersected the canonical JUP mint or current validator/vote/stake key sets.

- No root-update account, signer or writable account matched the parsed upgrade authorities for the Gum/Bank/inbox/outbox surfaces.

## Root Update Logs

- `Program log: UpdateMerkleRoot invoked`: `1`
- `Program log: Merkle proof verified`: `1`
- `Program log: Verifying BLS signature`: `1`
- `Program log: Signature verified`: `1`

## Assessment

- Public root-update submission currently resolves to the transaction signer/payer around the Solana outbox helper, plus the helper program's BLS/Merkle verification path.
- The sampled root update exposes the aggregate-key inclusion boundary, but not the producer-side Dove/JUP/stake mapping that created or weighted that aggregate key.
- The signer/control graph should be monitored for new signers, writable accounts, upgrade-authority overlap or any direct intersection with canonical JUP/current validator/vote/stake keys.
