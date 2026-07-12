# Verify Request Payload Reconstruction

## Scope

This pass reconstructs the sampled Bank Program `verify_request` instruction payloads.

Generated report:

```text
evidence/2026-07-12-bank-live-rpc/verify-request-payload-reconstruction.md
```

Script:

```text
scripts/reconstruct_verify_request_payloads.py
```

## Result

Two sampled `verify_request` instructions were decoded.

| Property | Value |
|---|---:|
| Raw instruction length | 463 bytes |
| Payload length after discriminator | 455 bytes |
| Canonical JUP key hits | 0 |
| Current JupNet validator/vote/stake key hits | 0 |

Known embedded pubkeys:

| Offset | Pubkey |
|---:|---|
| 13 | Bank Program `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ` |
| 87 | USDC mint `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` |

## Merkle Proof Tail

The payload tail contains a proof-like structure:

- proof node count candidate: `5`;
- proof node start offset: `295`;
- proof data length: `160` bytes;
- proof node size: `32` bytes;
- proof nodes are identical across the two sampled payloads.

The outbox Merkle root itself is not embedded directly in the payload. It is supplied through the outbox root state account:

```text
3C1LxtpR3Mh5RQjydfeQdvRaAzpStWM7gBi1XzP9oyGt
```

## Timestamp-Like Field

A big-endian timestamp-like field appears at payload offset `82`.

In both samples it equals the transaction block time plus 56 seconds:

| Sample | Block time | Offset 82 value | Delta |
|---|---|---|---:|
| `5EivNpnD` | `2026-07-12T18:04:26Z` | `2026-07-12T18:05:22Z` | 56 seconds |
| `5JQFCWSE` | `2026-07-12T18:00:48Z` | `2026-07-12T18:01:44Z` | 56 seconds |

This may be an expiry/finality/validity field.

## Assessment

This pass makes the public verification path clearer:

```text
verify_request payload
  -> message/leaf-like fields
  -> timestamp-like validity field
  -> USDC mint
  -> five-node Merkle proof
  -> outbox root state account
```

It does not expose JUP utility/security:

- no canonical JUP mint in the payload;
- no current JupNet validator/vote/stake keys in the payload;
- no obvious signer-set, quorum table or stake-weight field;
- no obvious BLS public key or signature set in the sampled payloads.

The likely interpretation is that `verify_request` proves inclusion against an already-published outbox root. The BLS signer/quorum process appears more likely to happen when the outbox root is updated, not when each request is verified.

## Next Target

The next decisive public target is the transaction path for outbox root updates, especially instructions that log:

```text
UpdateMerkleRoot invoked
Verifying BLS signature
Signature verified
```

If public evidence of signer set, quorum or JUP weighting exists, those update-root transactions are now a better target than `verify_request`.
