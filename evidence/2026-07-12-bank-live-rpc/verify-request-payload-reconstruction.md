# Verify Request Payload Reconstruction

## Scope

- `verify_request` samples: `2`
- Payload length: `455`
- Raw instruction length: `463`
- Canonical JUP key hits: `0`
- Current JupNet validator/vote/stake key hits: `0`

## Samples

| File | Slot | Block time | Signature | Accounts |
|---|---:|---|---|---:|
| `solana-mainnet-bank-tx-5EivNpnD.json` | 432481982 | `2026-07-12T18:04:26+00:00` | `5EivNpnDvdiVqnTrhgjeZ3sGuNBu4GBbYUJbWWYAgHATtR3ytX8aZQAN4CZYJrPRdQjiYKRybZxc4gdRy2CuDhYf` | 9 |
| `solana-mainnet-bank-tx-5JQFCWSE.json` | 432481451 | `2026-07-12T18:00:48+00:00` | `5JQFCWSE3Ld7d4Ker6DaVYY1uGcJ29zPiosd9GxwFUXNLd3Gewe5vMMj9phH1ntQVtZbuU5MsZsUhJDew4EST5c4` | 9 |

## Difference Ranges

| Offset range | Length | Interpretation candidate |
|---|---:|---|
| `46-77` | 32 | per-message 32-byte hash/key-like field |
| `84-85` | 2 | timestamp-like field |
| `148-150` | 3 |  |
| `255-286` | 32 | per-message 32-byte hash/key-like field |

## Known Pubkey Hits

| File | Label | Pubkey | Payload offsets |
|---|---|---|---|
| `solana-mainnet-bank-tx-5EivNpnD.json` | USDC mint | `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` | `87` |
| `solana-mainnet-bank-tx-5EivNpnD.json` | Bank Program | `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ` | `13` |
| `solana-mainnet-bank-tx-5JQFCWSE.json` | USDC mint | `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` | `87` |
| `solana-mainnet-bank-tx-5JQFCWSE.json` | Bank Program | `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ` | `13` |

## Timestamp-Like Fields

| File | Offset | Encoding | Value | ISO time | Delta from block time |
|---|---:|---|---:|---|---:|
| `solana-mainnet-bank-tx-5EivNpnD.json` | 82 | `u32be` | 1783879522 | `2026-07-12T18:05:22+00:00` | 56 |
| `solana-mainnet-bank-tx-5JQFCWSE.json` | 82 | `u32be` | 1783879304 | `2026-07-12T18:01:44+00:00` | 56 |

## Merkle Proof Tail

- Tail node start offset: `295`
- Length indicators: BE u32 at 288 = `5`, LE u32 at 291 = `5`

| Node index | Hex |
|---:|---|
| 0 | `97375839a6a19a2382b9958796df46161a113362aad11143cb547a7867b05fdf` |
| 1 | `d62d10c2522c7d52ec0da4227e3e361067970b648f35d2a746430197e8a1d271` |
| 2 | `7e8cab4245423af57ff7f95f2c46b21c7fbf2b4267ba056ec66abbacbed1f78b` |
| 3 | `2a2271f4288574d17854d87120c1c0cfc6335b8a9f83e85fdb9acd9c1cc3dc7d` |
| 4 | `d90c3226b4e2a82538f6f1fee4d3f4892d319a391d084cf66fbab40a03994a8f` |

- Proof nodes identical across sampled payloads: `True`

## Outbox Root Comparison

| Epoch | Root | Present in payload | SHA256 proof attempt matched |
|---:|---|---|---|
| 271 | `6928957b2ea436bcc9c44970a0f85364b6f0c8e5e4e886565eea061c9bd8d999` | `False` | `False` |
| 270 | `6928957b2ea436bcc9c44970a0f85364b6f0c8e5e4e886565eea061c9bd8d999` | `False` | `False` |
| 269 | `6928957b2ea436bcc9c44970a0f85364b6f0c8e5e4e886565eea061c9bd8d999` | `False` | `False` |

## Field Map Candidate

| Offset | Length | Observation |
|---:|---:|---|
| 0 | 4 | Stable little-endian `179`; likely serialized message/body length or domain field |
| 4 | 4 | Stable little-endian `1` |
| 13 | 32 | Embedded Bank Program pubkey |
| 46 | 32 | Per-message hash/key-like field; differs between samples |
| 82 | 4 | Big-endian timestamp-like value; equals block time + 56 seconds in both samples |
| 87 | 32 | Embedded USDC mint pubkey |
| 148 | 3 | Per-message bytes inside a mostly stable field |
| 191 | 64 | Stable 64-byte hash/signature-like region across samples |
| 255 | 32 | Per-message hash/leaf-like field; differs between samples |
| 291 | 4 | Little-endian proof node count candidate `5` |
| 295 | 160 | Five 32-byte Merkle proof nodes, identical across samples |

## Assessment

- `verify_request` carries a Merkle proof-like payload and references the outbox root state account by account meta, not by embedding the root directly.
- The sampled payloads contain USDC and Bank Program pubkeys, but no canonical JUP mint, current validator/vote/stake keys, inbox program key or outbox program key.
- The public outbox state provides Merkle roots; sampled `verify_request` payloads provide proof nodes and message/leaf-like fields.
- BLS signer/quorum material is not obvious in these `verify_request` samples. The BLS path is more likely associated with outbox root updates than per-request proof verification.
