# Private Runtime Fingerprints

## Purpose

This pass searches saved public artifacts for strings that connect the visible Gum/JupNet verifier layer to private runtime, Dove, stake-weight or quorum implementation details.

Report:

```text
evidence/2026-07-12-bank-live-rpc/private-runtime-fingerprints.md
```

Script:

```text
scripts/analyze_private_runtime_fingerprints.py
```

## Scope

| Metric | Value |
|---|---:|
| JSON artifacts scanned | `204` |
| Decoded/text blobs scanned | `3418` |
| Private runtime dependency terms with hits | `2` |
| Security producer terms with hits | `0` |
| Public verifier terms with hits | `10` |
| JupNet/Gum source paths recovered | `24` |

## New Positive Finding

Two private-runtime dependency fingerprints were visible in the public `brhPf...` Gum omnichain ProgramData executable:

| Term | Artifact |
|---|---|
| `jupnet_bn254` | `jupnet-programdata-brhPfKEx.json` |
| `jupnet_crosschain_hash` | `jupnet-programdata-brhPfKEx.json` |

This is stronger than generic BLS/Merkle strings. It links one public Gum omnichain binary to JupNet-specific cryptographic/cross-chain crates.

The same binary also exposes:

```text
jupnet_alt_bn128_bls
sol_verify_bls_merkle_key
```

## Negative Producer Result

The scan did not find public hits for:

- `jupnet-svm`;
- `jupnet-vote`;
- `jupnet-vote-program`;
- `jupnet-bls-sdk`;
- `jupnet-merkle-tree`;
- `jupnet-define-syscall`;
- `dove`;
- `validator_set`;
- `stake_weight`;
- `vote_weight`;
- `signer_set`;
- `quorum`;
- `root_builder`;
- `aggregate_key_set`;
- `slashing`;
- `reward`.

## Interpretation

This improves the implementation map:

```text
Gum omnichain executable
  -> JupNet BN254 / cross-chain hash crates
  -> BLS/Merkle verifier syscall
  -> public outbox root verification
```

It still does not expose:

```text
Dove signer registry
JUP stake-weight table
quorum threshold calculation
root-builder implementation
```

## Assessment

The public executable evidence now ties Gum omnichain more tightly to JupNet-specific cryptographic libraries. It does not prove JUP-denominated security.

The likely split remains:

- public application/verifier side: Gum, Bank, inbox/outbox, BN254/BLS/Merkle/cross-chain hash;
- hidden producer side: Dove set, JUP stake weights, quorum and epoch-root construction.
