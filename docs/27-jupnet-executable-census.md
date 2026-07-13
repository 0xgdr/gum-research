# JupNet Executable Census

## Purpose

The remaining proof target is the missing upper half of the security path:

```text
JUP stake / Dove identity / stake weight
  -> aggregate BLS key set
  -> Merkle root
```

This pass fetched and analyzed full ProgramData for every upgradeable JupNet executable visible in the saved loader scan.

Report:

```text
evidence/2026-07-12-bank-live-rpc/jupnet-executable-census.md
```

Scripts:

```text
scripts/collect_jupnet_executable_census.py
scripts/analyze_jupnet_executable_census.py
```

## Scope

| Metric | Value |
|---|---:|
| Upgradeable JupNet executables analyzed | `23` |
| Executables with source-path strings | `22` |
| Executables with high-value security term hits | `5` |
| Executables with canonical JUP / validator / vote / stake key hits | `0` |
| Executables with `sol_verify_bls_merkle_key` | `2` |

## Main Finding

The verifier syscall string appears in two Gum omnichain executables:

| Program | ProgramData | Evidence |
|---|---|---|
| `brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1` | `BW7ncAFAX1jjhZU6X5AS8JrkAqr8njfUNQxkuPtUQXjv` | `sol_verify_bls_merkle_key`; `gum-omnichain/src/instructions/complete_withdrawal.rs`; `jupnet_alt_bn128_bls` |
| `GUMebNDCYyF81xjyqaHagbgMQVUTb8fBC9YRh25xSH64` | `Gi8HgbHnykRiHboqG2VHysti773o8bNSjuFJWpyf4Q89` | `sol_verify_bls_merkle_key`; `programs/gum-omnichain` strings |

This strengthens the model that BLS/Merkle verification is consumed by Gum application programs through a JupNet verifier syscall/runtime interface.

## Negative Result

Across the executable census:

```text
canonical JUP key hits: 0
current validator key hits: 0
current vote account key hits: 0
current stake account key hits: 0
```

The census did not expose:

- a Dove registry;
- a public JUP stake-weight table;
- a root-builder implementation;
- slashing or reward state tied to JUP;
- a validator-to-BLS-key mapping.

## Interpretation

The public JupNet executable set confirms the consumer side of the proof:

```text
Gum application programs
  -> sol_verify_bls_merkle_key
  -> aggregate-key Merkle proof
  -> stored epoch root
```

It still does not expose the producer side:

```text
Dove set + JUP/stake weights
  -> aggregate keys
  -> epoch Merkle root
```

That producer side is still most likely inside private runtime/root-builder infrastructure or private `jupnet-svm` components rather than public JupNet program accounts.
