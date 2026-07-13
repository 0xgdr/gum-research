# Gum Omnichain Binary Roles

## Purpose

This pass compares the two Gum omnichain executables that consume BLS/Merkle verification surfaces:

- `brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1`;
- `GUMebNDCYyF81xjyqaHagbgMQVUTb8fBC9YRh25xSH64`.

Report:

```text
evidence/2026-07-12-bank-live-rpc/gum-omnichain-binary-roles.md
```

Script:

```text
scripts/analyze_gum_omnichain_binary_roles.py
```

## Metadata

| Program | Role interpretation | Executable bytes | Source paths | Key private/verifier signals |
|---|---|---:|---:|---|
| `brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1` | richer/full Gum omnichain verifier candidate | `810928` | `58` | `jupnet_bn254`, `jupnet_crosschain_hash`, `jupnet_alt_bn128_bls`, `verify_signature`, `sol_verify_bls_merkle_key` |
| `GUMebNDCYyF81xjyqaHagbgMQVUTb8fBC9YRh25xSH64` | recovered outbox sender/program id | `1140464` | `91` | `sol_verify_bls_merkle_key`, Gum omnichain instruction/state paths |

## Feature Comparison

| Feature | `brhPf...` | `GUMeb...` |
|---|---:|---:|
| `sol_verify_bls_merkle_key` | `2` | `1` |
| `jupnet_alt_bn128_bls` | `6` | `0` |
| `jupnet_bn254` | `4` | `0` |
| `jupnet_crosschain_hash` | `2` | `0` |
| `verify_signature` | `1` | `0` |
| `proof_hash` | `1` | `1` |
| `inbox_hash` | `1` | `0` |
| `outbound_hash` | `2` | `1` |
| `chain_config` | `6` | `5` |
| `fee` | `4` | `6` |
| `stake` / `validator` / `vote` / `dove` / `quorum` / `weight` | `0` | `0` |

## Interpretation

The role split now looks like:

```text
brhPf...
  -> older/richer Gum omnichain verifier candidate
  -> JupNet BN254 and cross-chain-hash symbols
  -> alt_bn128 BLS signature verification
  -> proof_hash / inbox_hash / outbound hash surfaces

GUMeb...
  -> recovered sender/program id in verifier payloads
  -> Gum omnichain request/deposit/swap/withdraw state and instruction paths
  -> BLS/Merkle verifier syscall consumer
```

This explains why the private runtime fingerprint pass found BN254 and cross-chain-hash symbols in `brhPf...` but not in `GUMeb...`.

## Security Producer Result

Neither Gum omnichain executable exposed:

- Dove registry strings;
- JUP stake-weight tables;
- validator/vote/stake key mappings;
- quorum threshold calculation;
- slashing or reward machinery;
- root-builder implementation.

## Assessment

This is meaningful reverse engineering progress because it clarifies the public application/verifier split:

```text
Gum application programs
  -> JupNet-specific crypto/verifier utilities
  -> public outbox root verification
```

The missing piece remains the producer side:

```text
Dove/JUP/stake state
  -> aggregate key set
  -> epoch root
```
