# Gum Account Role Reconstruction

## Purpose

This pass reconstructs Gum and Bank account roles from sampled transaction account metas, token balance hints, known helper accounts and decoded verifier payloads.

Report:

```text
evidence/2026-07-12-bank-live-rpc/gum-account-role-reconstruction.md
```

Script:

```text
scripts/analyze_gum_account_role_reconstruction.py
```

## Scope

| Metric | Value |
|---|---:|
| Direct JupNet Gum `brhPf...` instructions decoded | `8` |
| Direct Solana Bank instructions decoded | `17` |
| Direct sampled top-level `GUMeb...` instructions | `0` |
| Inner verifier payloads with `GUMeb...` sender/program id | `11` |
| Account-meta canonical JUP hits | `0` |
| Account-meta current validator/vote/stake hits | `0` |

## Role Map

| Surface | Role evidence |
|---|---|
| `brhPf...` | Direct JupNet Gum transaction program; sampled instructions are admin/authority-heavy and touch Gum-owned config/state, Token-2022, system and associated-token surfaces |
| `GUMeb...` | Not directly invoked in saved transaction bodies; stable sender/program id recovered from inner outbox verifier payloads |
| Solana Bank `verify_request` | Consistently passes the outbox Merkle root-history account and outbox helper program |
| Solana Bank asset movement | `withdraw`, `sweep` and RFQ variants touch USDC/wrapped SOL token accounts, Bank state/config candidates and inbox helper accounts |

## High-Confidence Accounts

| Account | Role |
|---|---|
| `3C1LxtpR3Mh5RQjydfeQdvRaAzpStWM7gBi1XzP9oyGt` | outbox Merkle root-history account |
| `jnoUtncGR9ZCCMixtys6Gzy5coTo6mnmUZuEHRQFTFV` | JupNet outbox helper program |
| `9DvDdsw38EB3RPChPqHkgBmntFbM5v79QxMyMSbfXWuy` | inbox helper state/counter account |
| `EG9fKpmLgkzCYZdj8uNDhHu5xmeXCZakccV6QmUavbzt` | Bank `__inbox_event_auth` PDA |
| `HVKuqyK6wjexdVJAUARiGdQTdGBBWhdYyhCZGFXh9d4s` | recurring Bank state/config candidate |
| `2x4wPZePCbq2W9tFfP2bagXjXnysdqNWQWMtwGMoyPFv` | recurring request/account state candidate |
| `Hso4y8rKEXUUvMbxnyDmjCxA7yk1wbVsZNHSGXcDEUyU` | recurring Gum-owned config candidate |

## Interpretation

The public role map now looks like:

```text
brhPf...
  -> direct JupNet Gum admin/config and asset-side operations

GUMeb...
  -> Gum sender/program id inside outbox verifier payloads

Solana Bank verify_request
  -> request/account state
  -> outbox root-history account
  -> outbox helper verifier program
```

This improves our understanding of how the public pieces line up, but the role surface still does not expose:

- JUP staking;
- Dove signer weights;
- validator/vote/stake mappings;
- quorum state;
- slashing or reward state;
- root-builder state.

## Assessment

This pass narrows the visible account model to application/config/request/proof-verification roles. It does not move the producer side into public view.

The unresolved boundary remains:

```text
Dove/JUP/stake producer state
  -> aggregate key set
  -> public outbox root
```
