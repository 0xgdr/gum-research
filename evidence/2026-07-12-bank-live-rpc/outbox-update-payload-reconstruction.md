# Outbox Update Payload Reconstruction

## Scope

- Snapshot: `evidence/2026-07-12-bank-live-rpc`
- Outbox helper program: `jnoUtncGR9ZCCMixtys6Gzy5coTo6mnmUZuEHRQFTFV`
- 305-byte update payloads decoded: `1`
- Merkle formula tested: `leaf = SHA256(0x00 || candidate_64_bytes)` and `parent = SHA256(0x01 || left || right)`

## Payload Layout

| Offset | Length | Interpretation |
|---:|---:|---|
| `0` | 1 | Instruction tag, observed `1` |
| `1` | 8 | Epoch/root-slot candidate, little-endian u64 |
| `9` | 32 | Merkle root stored/emitted by the outbox helper |
| `41` | 32 | Untyped 32-byte field; likely signed message hash or compact signature material |
| `73` | 4 | Merkle proof node count, little-endian u32 |
| `77` | `32 * proof_count` | Merkle proof sibling nodes |
| after proof | 4 | Merkle path orientation bitmap |
| after bitmap | 64 | Candidate aggregated BLS public key material; hashes as the Merkle leaf material |

## `solana-mainnet-outbox-tx-3Zjq8FZd.json`

- Signature: `3Zjq8FZdd9srj5UbC9FrRrstNB8eSXreTCWTKG7b4ozsZLVHjXoPkcQKK72gTuzLZcLFsV2MebiaMDiCiVKLS4pQ`
- Slot: `432511387`
- Time: `2026-07-12T21:25:50+00:00`
- Instruction index: `0`
- Instruction tag: `1`
- Epoch/root slot: `271`
- Merkle root: `6928957b2ea436bcc9c44970a0f85364b6f0c8e5e4e886565eea061c9bd8d999`
- Untyped 32-byte field: `1936cf6325733174d35ff22f86bebabdf33abd441315398d8d4b61313eda628d`
- Proof node count: `5`
- Path bitmap: `18` (`01001` low-bit first)
- Candidate 64-byte aggregate key material: `87e930814a0131f70e4b405f4e30ca3e226ad5bee2e5e40d584947d48c4bcceb15f96af18671975c31abc6d2c3ea8230ee775da12cd69b5331e35865ad2c4025`
- Candidate leaf hash: `549627c9007f9bde82667fab9390ede2ff81307d18b4b391beda278f8bb48e44`
- Recomputed root: `6928957b2ea436bcc9c44970a0f85364b6f0c8e5e4e886565eea061c9bd8d999`
- Merkle match: `True`

### Proof Steps

| Step | Bitmap bit | Sibling position | Sibling hash | Parent hash |
|---:|---:|---|---|---|
| 0 | 0 | `right` | `97375839a6a19a2382b9958796df46161a113362aad11143cb547a7867b05fdf` | `8cfde994b0413475650295e927aef81c4166b363e306ea8498a0cfb06934ca7c` |
| 1 | 1 | `left` | `d62d10c2522c7d52ec0da4227e3e361067970b648f35d2a746430197e8a1d271` | `1f43f02444f54e5106de382694b7a24220ed57ac5ab33b4d1a5218088d8ced0c` |
| 2 | 0 | `right` | `7e8cab4245423af57ff7f95f2c46b21c7fbf2b4267ba056ec66abbacbed1f78b` | `35de069953a4ef3ca12a38375447245db9c631418d581a5478ac1a587834b156` |
| 3 | 0 | `right` | `2a2271f4288574d17854d87120c1c0cfc6335b8a9f83e85fdb9acd9c1cc3dc7d` | `7174f3a341a14f01b9ee061c268f2ac78803eae3248fb67b5968be592e1b91fe` |
| 4 | 1 | `left` | `d90c3226b4e2a82538f6f1fee4d3f4892d319a391d084cf66fbab40a03994a8f` | `6928957b2ea436bcc9c44970a0f85364b6f0c8e5e4e886565eea061c9bd8d999` |

### Program Data Logs

| Length | Hex | Interpretation |
|---:|---|---|
| 32 | `6928957b2ea436bcc9c44970a0f85364b6f0c8e5e4e886565eea061c9bd8d999` | emitted Merkle root |
| 40 | `0f010000000000006928957b2ea436bcc9c44970a0f85364b6f0c8e5e4e886565eea061c9bd8d999` | emitted epoch/root pair |

## Assessment

- The sampled root-update payload matches the public JupNet article's Merkle leaf and parent hash formulas exactly.
- The four bytes after the proof nodes behave as a Merkle path bitmap; for the sampled transaction the bitmap is `18`.
- The final 64-byte field is the material hashed into the Merkle leaf, making it the strongest public candidate for the aggregate BLS public key committed by the epoch root.
- The payload still does not expose the underlying Dove members, stake weights, JUP balances, slashing records or threshold calculation that produced the aggregate key.
- The 32-byte field at offset `41` remains untyped from public bytes alone; logs prove BLS verification occurred, but the public transaction does not label whether this field is message hash, compact signature material or another verifier input.
