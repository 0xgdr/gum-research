# Outbox Update Payload Reconstruction

## Why this pass mattered

The previous outbox-root update pass proved that a public Solana transaction logged:

```text
UpdateMerkleRoot invoked
Merkle proof verified
Verifying BLS signature
Signature verified
```

That was useful, but still log-level evidence. This pass checks whether the transaction bytes themselves match the public JupNet article's stated Merkle construction:

```text
https://blog.blockmagnates.com/jupnet-a-crosschain-decentralized-network-6cd2ee835cf2
```

```text
leaf   = SHA256(0x00 || aggregated_pubkey)
parent = SHA256(0x01 || left_child || right_child)
```

## Result

The sampled `UpdateMerkleRoot` payload matches that Merkle construction exactly.

Report:

```text
evidence/2026-07-12-bank-live-rpc/outbox-update-payload-reconstruction.md
```

Script:

```text
scripts/reconstruct_outbox_update_payload.py
```

## Decoded transaction

| Field | Value |
|---|---|
| Signature | `3Zjq8FZdd9srj5UbC9FrRrstNB8eSXreTCWTKG7b4ozsZLVHjXoPkcQKK72gTuzLZcLFsV2MebiaMDiCiVKLS4pQ` |
| Slot | `432511387` |
| Time | `2026-07-12T21:25:50Z` |
| Epoch/root slot | `271` |
| Merkle root | `6928957b2ea436bcc9c44970a0f85364b6f0c8e5e4e886565eea061c9bd8d999` |
| Proof nodes | `5` |
| Path bitmap | `18` |
| Merkle match | `true` |

## Reconstructed payload layout

| Offset | Length | Interpretation |
|---:|---:|---|
| `0` | 1 | Instruction tag, observed `1` |
| `1` | 8 | Epoch/root-slot candidate, little-endian u64 |
| `9` | 32 | Merkle root stored/emitted by the outbox helper |
| `41` | 32 | Untyped verifier field; likely signed message hash or compact signature material |
| `73` | 4 | Merkle proof node count |
| `77` | `32 * proof_count` | Merkle proof sibling nodes |
| after proof | 4 | Merkle path orientation bitmap |
| after bitmap | 64 | Candidate aggregated BLS public key material |

The final 64-byte field hashes as:

```text
SHA256(0x00 || candidate_64_bytes)
```

Using the five proof nodes and the path bitmap `18`, the script reconstructs:

```text
6928957b2ea436bcc9c44970a0f85364b6f0c8e5e4e886565eea061c9bd8d999
```

That is the same root emitted in the program logs and stored in the outbox helper root-history account.

## What this teaches

This is now stronger than "we saw BLS/Merkle strings" or "the logs mention BLS." The public transaction bytes line up with the described JupNet verifier design:

```text
candidate aggregate key
  -> SHA256(0x00 || key)
  -> Merkle proof with SHA256(0x01 || left || right)
  -> epoch root
  -> BLS verification log path
  -> root stored for later verify_request proofs
```

It also explains why the validator-security layer is hard to inspect publicly. The public outbox program does not need the full Dove set, every Dove public key, individual signatures, individual stake accounts or JUP balances. It only needs:

- an aggregate key;
- an aggregate signature or compact verifier input;
- a Merkle proof that the aggregate key is in the epoch root;
- the stored root for that epoch.

The expensive or sensitive part is pushed behind the root:

```text
Dove set + stake weights + valid supermajority combinations
  -> aggregate BLS public keys
  -> Merkle tree
  -> one public epoch root
```

That is a compact verification boundary, and it is also the visibility boundary for this investigation.

## Comparison to the public article

The byte-level match is strong for the article's technical messaging claims:

| Article claim | Public evidence |
|---|---|
| Aggregated BLS public keys are committed into a Merkle tree | Strong match: a 64-byte field hashes as leaf material under the article's `0x00` formula |
| Merkle parents use `SHA256(0x01 || left || right)` | Confirmed for the sampled transaction |
| Outbox/root verification checks Merkle proof and BLS signature | Confirmed by logs and payload reconstruction |
| Epoch roots are updated by signed root-update messages | Strong match: epoch/root pair emitted and root stored |
| Doves are weighted by staked tokens/JUP | Still not visible in public transaction bytes |
| Slashing/reward/validator economics are enforced on-chain | Still not observed |

## Utility conclusion

This pass moves the investigation forward meaningfully, but it does not prove JUP utility.

It proves that the public Solana outbox helper is implementing the kind of BLS/Merkle compact verifier described for JupNet. It also shows why JUP utility is difficult to prove from the outbox alone: if JUP is used, it is likely consumed during private/off-chain epoch tree construction or inside private JupNet validator/runtime code, not exposed as Solana account metas in each proof.

The next evidence target is therefore not ordinary Gum trading or Bank token flow. It is any public artifact that links the epoch Merkle root construction to:

- Dove identities;
- stake weights;
- the staking token denomination;
- slashing/reward state;
- the private `jupnet-svm` runtime or associated BLS/Merkle crates.
