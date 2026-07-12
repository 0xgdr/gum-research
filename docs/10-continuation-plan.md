# Continuation Plan

## Highest-value triggers

Resume investigation when any of the following appears:

1. Public validator/Dove software.
2. Community Dove onboarding documentation.
3. JUP staking contracts or registry accounts on JupNet.
4. Governance proposal defining Dove economics.
5. Public technical specification for cross-chain quorum proofs.
6. New Gum program deployment or upgrade.
7. Observable JUP utility mechanism such as staking, signer weights, fees, access control, governance, slashing, rewards or a permanent protocol burn/sink.
8. Public Jupiter source for Gum, Dove, JupNet validator software or JUP-weighted security.

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

### JUP utility flows

For each JUP-related transaction, ignore ordinary trading/routing unless it exposes utility. Capture:

- capture signature, slot and amount;
- capture Gum message/proof hash;
- identify whether JUP is paying fees, being locked, being staked, being burned as a protocol sink, governing access or affecting signer/validator weight;
- locate destination mint only when needed to rule out bridge-neutral accounting;
- compare canonical supply snapshots only when testing a permanent burn/sink claim.

## Avoid repeating low-value work

Unless new evidence appears, do not prioritise:

- random full-disk searches;
- Cargo cache searches on machines that never built the private dependencies;
- re-enumerating unchanged programs without binary hash comparison;
- assuming every burn is deflationary;
- treating JUP trading on Gum as utility evidence;
- treating native stake as JUP stake.

## Best next proof target

The decisive artifact would be one of:

- a validator configuration schema containing JUP stake weights;
- a public Dove registration transaction;
- an account mapping validator identity to JUP stake;
- code calculating a two-thirds threshold from JUP-denominated weights;
- a fee, burn/sink, governance, reward, slashing or access-control mechanism that requires JUP.
- public source that maps Gum/JupNet validators, Doves, signers or Omnipair/Gum authorities to JUP stake, fees, governance or security weights.
