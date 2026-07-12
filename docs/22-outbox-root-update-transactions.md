# Outbox Root Update Transactions

## Scope

This pass collected recent transactions for the JupNet outbox helper program and looked specifically for root-update and BLS verification evidence.

Generated files:

```text
evidence/2026-07-12-bank-live-rpc/outbox-root-update-transactions.md
evidence/2026-07-12-bank-live-rpc/solana-mainnet-outbox-tx-*.json
```

Scripts:

```text
scripts/collect_outbox_root_update_transactions.py
scripts/analyze_outbox_root_update_transactions.py
```

## Result

Twenty recent outbox helper transactions were fetched. One contained the update/BLS path:

| Field | Value |
|---|---|
| Signature | `3Zjq8FZdd9srj5UbC9FrRrstNB8eSXreTCWTKG7b4ozsZLVHjXoPkcQKK72gTuzLZcLFsV2MebiaMDiCiVKLS4pQ` |
| Slot | `432511387` |
| Time | `2026-07-12T21:25:50Z` |
| Outbox instruction discriminator | `010f010000000000` |
| Data length | `305` |
| Writable account | `3C1LxtpR3Mh5RQjydfeQdvRaAzpStWM7gBi1XzP9oyGt` |

Logs:

```text
UpdateMerkleRoot invoked
Merkle proof verified
Verifying BLS signature
Signature verified
advance_epoch_root: dropped root of epoch 268:
```

## Decoded Payload

The 305-byte update payload decodes as:

| Field | Value |
|---|---|
| Tag byte | `1` |
| Epoch/root slot candidate | `271` |
| Merkle root | `6928957b2ea436bcc9c44970a0f85364b6f0c8e5e4e886565eea061c9bd8d999` |
| Message/leaf candidate | `1936cf6325733174d35ff22f86bebabdf33abd441315398d8d4b61313eda628d` |
| Proof node count | `5` |

The Merkle root matches the public outbox helper state account for epoch `271`.

Follow-up byte-level reconstruction is in:

```text
docs/23-outbox-update-payload-reconstruction.md
evidence/2026-07-12-bank-live-rpc/outbox-update-payload-reconstruction.md
```

That reconstruction proves the final 64-byte field into the emitted root using the public JupNet Merkle formulas: `SHA256(0x00 || candidate_64_bytes)` for the leaf and `SHA256(0x01 || left || right)` for parent nodes.

## Utility/Security Checks

| Check | Result |
|---|---:|
| Canonical Solana JUP key hits | 0 |
| Current JupNet validator/vote/stake key hits | 0 |

## Assessment

This is the strongest public path found so far:

```text
UpdateMerkleRoot
  -> Merkle proof verified
  -> BLS signature verified
  -> epoch 271 root written to outbox state
  -> verify_request later proves inclusion against that root
```

It still does not expose the JUP security layer.

The root-update transaction proves BLS verification is part of the public outbox root update path, but the signer set, quorum threshold and any stake/JUP weighting are not visible as direct account keys or payload pubkeys in this sampled transaction.

The remaining honest conclusion is narrower:

> Public Solana state exposes Merkle-root publication and BLS verification logs, but not the signer-set/quorum source that determines whether JUP secures those roots.
