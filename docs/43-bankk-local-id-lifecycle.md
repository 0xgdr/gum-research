# BankK Local ID Lifecycle

This pass follows the 32-byte local ids recovered from compact `BankK...` 41-byte state accounts across the sampled Bank transaction corpus.

Evidence report:

```text
evidence/2026-07-12-bank-live-rpc/bankk-local-id-lifecycle.md
```

## Result

| Test | Result |
|---|---:|
| 41-byte local ids analyzed | `19` |
| Local ids with sampled lifecycle events | `18` |
| Local ids seen in `BankK...` raw payloads | `18` |
| Local ids seen in `JNiN...` inbox raw payloads | `18` |
| Local ids seen in `jnoUtn...` outbox raw payloads | `0` |
| Local ids seen in `VerifyRequest` rows | `18` |
| Local ids with operation + verify lifecycle evidence | `18` |
| Local ids with same-slot operation + verify evidence | `12` |
| Local ids matching decoded `bk1PDA...` request fields | `0` |
| Local ids matching verifier/root fields | `0` |
| Local ids matching canonical JUP / current validator / vote / stake keys | `0` |
| Local ids sharing a slot with root updates | `0` |

## What This Adds

The previous 41-byte layout pass showed that each compact `BankK...` account stores a stable 32-byte Bank-local id.

This lifecycle pass shows what that id does:

```text
BankK 41-byte state
  -> BankK operation payload
  -> JNiN inbox-helper payload/log material
  -> BankK VerifyRequest payload
```

That is the strongest public per-operation linkage found so far on the `BankK...` side.

## Boundary

The lifecycle still stops before the security producer layer:

- no local id matched decoded `bk1PDA...` request pubkeys, `jupnet` pubkeys, recipients or message hashes;
- no local id matched verifier message hashes, aggregate-key halves, compact verifier fields, proof nodes or stored outbox roots;
- no local id matched canonical JUP;
- no local id matched current validator, vote or stake accounts;
- no local id shared a slot with the sampled root-update transaction.

## Interpretation

This confirms that `BankK...` exposes its own public operation lifecycle. It does not expose the missing bridge from decoded `bk1PDA...` withdrawal requests into Dove/JUP/stake security material.

The current model becomes:

```text
bk1PDA request surface
  -> decoded withdrawal/request fields

BankK local-id lifecycle
  -> operation/inbox/verify handle

outbox root/security boundary
  -> aggregate-key and Merkle proof material

Dove/JUP/stake producer source
  -> still not public in this sample
```

## Next Useful Angle

The next meaningful extension is a larger paired `BankK...` window:

- collect more `BankK...` transactions across contiguous slots;
- rebuild the same lifecycle table over a wider window;
- check whether local ids ever persist into outbox-helper payloads or root-update-adjacent slots;
- alert if a local id starts matching decoded `bk1PDA...`, verifier/root, canonical JUP, validator, vote or stake material.
