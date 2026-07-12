# Continuation Plan

## Highest-value triggers

Resume investigation when any of the following appears:

1. Public validator/Dove software.
2. Community Dove onboarding documentation.
3. JUP staking contracts or registry accounts on JupNet.
4. Governance proposal defining Dove economics.
5. Public technical specification for cross-chain quorum proofs.
6. New Gum program deployment or upgrade.
7. Observable permanent-burn mechanism.

## Recommended live monitoring

### Validator set

Periodically snapshot:

- validator identity;
- software version;
- RPC/gossip endpoints;
- vote account;
- native stake;
- activation/deactivation epochs.

### Program upgrades

Monitor ProgramData:

- deployment slot;
- binary hash;
- upgrade authority;
- string/symbol diffs.

### JUP flows

For each JUP burn:

- capture signature, slot and amount;
- capture Gum message/proof hash;
- locate destination mint;
- classify as bridge-neutral or permanent;
- compare canonical supply snapshots.

## Avoid repeating low-value work

Unless new evidence appears, do not prioritise:

- random full-disk searches;
- Cargo cache searches on machines that never built the private dependencies;
- re-enumerating unchanged programs without binary hash comparison;
- assuming every burn is deflationary;
- treating native stake as JUP stake.

## Best next proof target

The decisive artifact would be one of:

- a validator configuration schema containing JUP stake weights;
- a public Dove registration transaction;
- an account mapping validator identity to JUP stake;
- code calculating a two-thirds threshold from JUP-denominated weights.
