# Epoch Security Source Hunt

## Purpose

The proof target is:

```text
JUP stake/lock
  -> Dove identity
  -> Dove BLS public key
  -> stake weight / threshold
  -> aggregate BLS public key
  -> Merkle leaf
  -> epoch root
  -> public outbox verification
```

Earlier passes proved the lower half:

```text
candidate aggregate key
  -> SHA256(0x00 || key)
  -> Merkle proof
  -> epoch root
  -> BLS verification logs
```

This pass hunted for the missing upper half by scanning saved account and transaction artifacts for the epoch root, candidate aggregate key, leaf hash, canonical JUP mint, and current JupNet validator/vote/stake keys.

Report:

```text
evidence/2026-07-12-bank-live-rpc/epoch-security-source-hunt.md
```

Script:

```text
scripts/hunt_epoch_security_sources.py
```

## Root Under Test

| Field | Value |
|---|---|
| Outbox update transaction | `3Zjq8FZdd9srj5UbC9FrRrstNB8eSXreTCWTKG7b4ozsZLVHjXoPkcQKK72gTuzLZcLFsV2MebiaMDiCiVKLS4pQ` |
| Slot | `432511387` |
| Time | `2026-07-12T21:25:50Z` |
| Epoch/root slot | `271` |
| Root | `6928957b2ea436bcc9c44970a0f85364b6f0c8e5e4e886565eea061c9bd8d999` |
| Candidate aggregate-key material | `87e930814a0131f70e4b405f4e30ca3e226ad5bee2e5e40d584947d48c4bcceb15f96af18671975c31abc6d2c3ea8230ee775da12cd69b5331e35865ad2c4025` |
| Candidate leaf hash | `549627c9007f9bde82667fab9390ede2ff81307d18b4b391beda278f8bb48e44` |

## Results

The hunt scanned `3153` binary records extracted from the saved snapshot.

| Target | Hits | Interpretation |
|---|---:|---|
| Epoch root | `6` | Found in the outbox root-history account, root-update logs and root-update payload |
| Candidate aggregate-key material | `21` | Found in root update and repeated outbox/Bank verification payloads |
| Candidate aggregate-key leaf hash | `0` | The leaf hash is recomputed, not obviously stored |
| Untyped 32-byte verifier field | `1` | Only found in the root-update payload |
| Full 305-byte update payload | `1` | Only found in the root-update instruction |

The most useful new observation is that the candidate aggregate-key material appears in multiple verification payloads, not only in the epoch-root update. That means the public verifier path is reusing the same aggregate key material across ordinary outbox/Bank message verification.

## Co-Location Checks

| Check | Result |
|---|---:|
| Candidate aggregate key in the same binary record as canonical JUP / validator / vote / stake key | `0` |
| Epoch root in the same binary record as canonical JUP / validator / vote / stake key | `0` |

This is the key negative result.

The aggregate-key material is public enough to verify messages, but it is not co-located with public JUP, validator, vote or stake keys in the saved artifacts. That makes it unlikely that the ordinary Solana outbox/Bank transaction payloads themselves expose the staking source.

## What This Proves

This pass strengthens the verified public path:

```text
one 64-byte aggregate-key candidate
  -> appears in multiple verification payloads
  -> hashes into an epoch Merkle root
  -> root is stored in the outbox root-history account
  -> Bank/outbox verification consumes that proof boundary
```

It also shows why the missing proof remains missing:

```text
Dove set + JUP/stake weights + threshold rule
  -> aggregate-key construction
```

That construction is not present in the public artifacts scanned here.

## What Still Would Prove JUP Utility

Any of the following would move this from plausible architecture to proven JUP utility:

- a public epoch registry that maps Dove identities to BLS keys and JUP-denominated weights;
- a staking/slashing/reward account that links JUP balances to Dove eligibility;
- source or build metadata showing `JUP stake -> signer weight -> aggregate BLS key -> epoch root`;
- a root-generation witness that lets us recompute epoch `271` from public Dove keys and JUP weights.

## Current Conclusion

We have stronger evidence that JupNet's public Solana verifier works as described: aggregate-key material, Merkle proof, epoch root and BLS verification.

We still do not have public proof that JUP determines the Dove security weight behind that aggregate key.
