# Security Boundary Corpus

## Purpose

This pass pushes reverse engineering at the boundary where hidden JupNet/Dove security material would have to meet public Gum verification.

Report:

```text
evidence/2026-07-12-bank-live-rpc/security-boundary-corpus.md
```

Script:

```text
scripts/analyze_security_boundary_corpus.py
```

## Scope

| Metric | Value |
|---|---:|
| Helper-owned accounts decoded | `2` |
| Local transaction files scanned | `128` |
| Transaction files with decoded verifier payloads | `21` |
| Decoded verifier payloads | `42` |
| Root mismatches against stored outbox roots | `0` |
| Canonical JUP / validator / vote / stake hits | `0` |

## Helper Account Result

The public helper-owned accounts are:

| Program | Account | Space | Decoded shape |
|---|---|---:|---|
| JupNet inbox helper | `9DvDdsw38EB3RPChPqHkgBmntFbM5v79QxMyMSbfXWuy` | `64` | compact counter/state candidate |
| JupNet outbox helper | `3C1LxtpR3Mh5RQjydfeQdvRaAzpStWM7gBi1XzP9oyGt` | `320` | epoch/root history |

The outbox account decodes as epoch/root entries for epochs `271`, `270` and `269`, all currently pointing at:

```text
6928957b2ea436bcc9c44970a0f85364b6f0c8e5e4e886565eea061c9bd8d999
```

No helper-owned account exposed:

- canonical JUP key material;
- current JupNet validator keys;
- vote account keys;
- stake account keys;
- obvious signer-set, quorum or weight records.

## Verifier Corpus Result

The corpus combined locally saved Solana Bank transactions, direct outbox transactions and wider outbox-history transactions.

| Signal | Result |
|---|---|
| Payload kinds | `21` Bank wrappers, `21` inner outbox payloads |
| Epochs | `269`, `270` |
| Inner sender/program id | `GUMebNDCYyF81xjyqaHagbgMQVUTb8fBC9YRh25xSH64` |
| Aggregate keys | `3` observed values |
| Recomputed roots | `1` observed value |
| Root mismatches | `0` |
| JUP/validator/vote/stake hits | `0` |

The three observed aggregate-key values all recompute into the same stored outbox root. That strengthens the model that these payloads are aggregate-key inclusion proofs into a compact epoch root.

## Interpretation

This pass improves our understanding of the public verifier boundary:

```text
Gum message
  -> sender/program id
  -> aggregate-key material
  -> Merkle proof
  -> stored outbox epoch root
```

It still does not reveal the producer side:

```text
Dove signer set / JUP stake weights / quorum rules
  -> aggregate-key set
  -> epoch root
```

## Assessment

The best remaining public evidence path is time correlation. If future snapshots show root or aggregate-key changes near validator, vote, stake, ProgramData or authority changes, that would be meaningful circumstantial evidence.

If no such correlation appears across repeated snapshots, the public evidence remains limited to application-level BLS/Merkle verification, not JUP-denominated security.
