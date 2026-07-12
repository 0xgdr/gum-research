# Outbox Verifier Payload Field Map

## Scope

- Snapshot: `evidence/2026-07-12-bank-live-rpc`
- Parsed verifier payloads: `22`
- Bank wrapper payloads: `11`
- Inner outbox payloads: `11`
- Known aggregate-key material: `87e930814a0131f70e4b405f4e30ca3e226ad5bee2e5e40d584947d48c4bcceb15f96af18671975c31abc6d2c3ea8230ee775da12cd69b5331e35865ad2c4025`

## Layouts

### Inner Outbox Verifier

| Offset | Length | Field |
|---:|---:|---|
| 0 | 1 | tag, observed `0` |
| 1 | 32 | message hash |
| 33 | 32 | sender/program id candidate |
| 65 | 8 | epoch, little-endian u64 |
| 73 | 64 | aggregate-key material |
| 137 | 32 | compact signature/verifier field |
| 169 | 4 | Merkle path bitmap |
| 173 | 4 | Merkle proof count |
| 177 | 160 | five 32-byte Merkle proof nodes |

### Bank Verify Wrapper

| Offset | Length | Field |
|---:|---:|---|
| 0 | 8 | Bank `verify_request` discriminator |
| 8 | 4 | request/body length |
| 12 | 4 | stable version/flag |
| 21 | 32 | embedded Bank Program id in sampled 463-byte wrappers |
| aggregate_offset - 40 | 32 | message hash candidate |
| aggregate_offset - 8 | 8 | epoch, little-endian u64 |
| aggregate_offset | 64 | aggregate-key material |
| aggregate_offset + 64 | 32 | compact signature/verifier field |
| aggregate_offset + 96 | 4 | Merkle path bitmap |
| aggregate_offset + 100 | 4 | Merkle proof count |
| aggregate_offset + 104 | `32 * count` | Merkle proof nodes |

## Payload Rows

| File | Ix | Kind | Len | Epoch | Sender/program candidate | Root match | JUP key | Validator key | Message hash | Signature field |
|---|---|---|---:|---:|---|---|---|---|---|---|
| `solana-mainnet-outbox-tx-2CzThmfQ.json` | `2` | `bank-verify-wrapper` | 463 | 270 | `None` | `True` | `False` | `False` | `641f6255a3a0935c...` | `8f97485822378ac3...` |
| `solana-mainnet-outbox-tx-2CzThmfQ.json` | `inner:2:0` | `inner-outbox` | 337 | 270 | `GUMebNDCYyF81xjyqaHagbgMQVUTb8fBC9YRh25xSH64` | `True` | `False` | `False` | `32b055164d552c87...` | `8f97485822378ac3...` |
| `solana-mainnet-outbox-tx-2FzPsrQ1.json` | `2` | `bank-verify-wrapper` | 496 | 270 | `None` | `True` | `False` | `False` | `0000000000000000...` | `10f5d0e2cffa806e...` |
| `solana-mainnet-outbox-tx-2FzPsrQ1.json` | `inner:2:0` | `inner-outbox` | 337 | 270 | `GUMebNDCYyF81xjyqaHagbgMQVUTb8fBC9YRh25xSH64` | `True` | `False` | `False` | `d6d0d1507b32fa3f...` | `10f5d0e2cffa806e...` |
| `solana-mainnet-outbox-tx-2NbTujvU.json` | `2` | `bank-verify-wrapper` | 496 | 270 | `None` | `True` | `False` | `False` | `0000000000000000...` | `9bed6a7f2674b11f...` |
| `solana-mainnet-outbox-tx-2NbTujvU.json` | `inner:2:0` | `inner-outbox` | 337 | 270 | `GUMebNDCYyF81xjyqaHagbgMQVUTb8fBC9YRh25xSH64` | `True` | `False` | `False` | `89699934d93c74da...` | `9bed6a7f2674b11f...` |
| `solana-mainnet-outbox-tx-2cMxqNYU.json` | `2` | `bank-verify-wrapper` | 463 | 270 | `None` | `True` | `False` | `False` | `641f6255a3a0935c...` | `802dc88844bb5217...` |
| `solana-mainnet-outbox-tx-2cMxqNYU.json` | `inner:2:0` | `inner-outbox` | 337 | 270 | `GUMebNDCYyF81xjyqaHagbgMQVUTb8fBC9YRh25xSH64` | `True` | `False` | `False` | `47ed7a81396b71e7...` | `802dc88844bb5217...` |
| `solana-mainnet-outbox-tx-34DtKNBj.json` | `2` | `bank-verify-wrapper` | 463 | 270 | `None` | `True` | `False` | `False` | `641f6255a3a0935c...` | `9d6cfea15977349f...` |
| `solana-mainnet-outbox-tx-34DtKNBj.json` | `inner:2:0` | `inner-outbox` | 337 | 270 | `GUMebNDCYyF81xjyqaHagbgMQVUTb8fBC9YRh25xSH64` | `True` | `False` | `False` | `a664eae2ae3116ea...` | `9d6cfea15977349f...` |
| `solana-mainnet-outbox-tx-4ivz1c34.json` | `2` | `bank-verify-wrapper` | 496 | 270 | `None` | `True` | `False` | `False` | `0000000000000000...` | `975e3054da230ebe...` |
| `solana-mainnet-outbox-tx-4ivz1c34.json` | `inner:2:0` | `inner-outbox` | 337 | 270 | `GUMebNDCYyF81xjyqaHagbgMQVUTb8fBC9YRh25xSH64` | `True` | `False` | `False` | `57716856cbcbd100...` | `975e3054da230ebe...` |
| `solana-mainnet-outbox-tx-4u2aHaAt.json` | `2` | `bank-verify-wrapper` | 463 | 270 | `None` | `True` | `False` | `False` | `694fa6e67a508d19...` | `096dc3a5d62eadc2...` |
| `solana-mainnet-outbox-tx-4u2aHaAt.json` | `inner:2:0` | `inner-outbox` | 337 | 270 | `GUMebNDCYyF81xjyqaHagbgMQVUTb8fBC9YRh25xSH64` | `True` | `False` | `False` | `0538b1139c9ab47c...` | `096dc3a5d62eadc2...` |
| `solana-mainnet-outbox-tx-Xdk7KN25.json` | `2` | `bank-verify-wrapper` | 496 | 270 | `None` | `True` | `False` | `False` | `0000000000000000...` | `2cbbb237a8906990...` |
| `solana-mainnet-outbox-tx-Xdk7KN25.json` | `inner:2:0` | `inner-outbox` | 337 | 270 | `GUMebNDCYyF81xjyqaHagbgMQVUTb8fBC9YRh25xSH64` | `True` | `False` | `False` | `f1c1deacea8e71a2...` | `2cbbb237a8906990...` |
| `solana-mainnet-outbox-tx-kHij6H1u.json` | `2` | `bank-verify-wrapper` | 496 | 270 | `None` | `True` | `False` | `False` | `0000000000000000...` | `8044ea7eed3dd9d8...` |
| `solana-mainnet-outbox-tx-kHij6H1u.json` | `inner:2:0` | `inner-outbox` | 337 | 270 | `GUMebNDCYyF81xjyqaHagbgMQVUTb8fBC9YRh25xSH64` | `True` | `False` | `False` | `be6d0b952f5735f6...` | `8044ea7eed3dd9d8...` |
| `solana-mainnet-bank-tx-5EivNpnD.json` | `2` | `bank-verify-wrapper` | 463 | 269 | `None` | `True` | `False` | `False` | `641f6255a3a0935c...` | `9e7d4e0079fa4c05...` |
| `solana-mainnet-bank-tx-5EivNpnD.json` | `inner:2:0` | `inner-outbox` | 337 | 269 | `GUMebNDCYyF81xjyqaHagbgMQVUTb8fBC9YRh25xSH64` | `True` | `False` | `False` | `0289535f32a49bbe...` | `9e7d4e0079fa4c05...` |
| `solana-mainnet-bank-tx-5JQFCWSE.json` | `2` | `bank-verify-wrapper` | 463 | 269 | `None` | `True` | `False` | `False` | `641f6255a3a0935c...` | `284da295e350bc7b...` |
| `solana-mainnet-bank-tx-5JQFCWSE.json` | `inner:2:0` | `inner-outbox` | 337 | 269 | `GUMebNDCYyF81xjyqaHagbgMQVUTb8fBC9YRh25xSH64` | `True` | `False` | `False` | `add2af73f269cc6a...` | `284da295e350bc7b...` |

## Aggregate-Key Groups

| Aggregate key prefix | Count |
|---|---:|
| `87e930814a0131f70e4b405f4e30ca3e...` | 20 |
| `05eebac3af7909fd6e3349703ebbe4c0...` | 2 |

## Proof Invariants

- Bitmap/count groups: `{(18, 5): 20, (5, 5): 2}`
- Recomputed root groups: `{'6928957b2ea436bcc9c44970a0f85364b6f0c8e5e4e886565eea061c9bd8d999': 22}`
- Stored roots available: `{271: '6928957b2ea436bcc9c44970a0f85364b6f0c8e5e4e886565eea061c9bd8d999', 270: '6928957b2ea436bcc9c44970a0f85364b6f0c8e5e4e886565eea061c9bd8d999', 269: '6928957b2ea436bcc9c44970a0f85364b6f0c8e5e4e886565eea061c9bd8d999'}`

## Assessment

- Sampled Bank/outbox verification payloads expose the same aggregate-key material and Merkle proof path used by the root-update reconstruction.
- The inner outbox verifier payload maps closely to the public article's outbox argument list: message hash, sender/program id, epoch, aggregate key, compact signature/verifier field and Merkle proof.
- Every parsed payload recomputes to the stored outbox root for its epoch when the article's `0x00` leaf and `0x01` parent hash formula is used.
- These verifier payloads still do not expose Dove identities, individual BLS keys, JUP balances or stake weights.
