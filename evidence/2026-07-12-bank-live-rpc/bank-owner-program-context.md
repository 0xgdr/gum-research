# Bank Owner Program Context

## Scope

- Owner-context accounts fetched: `11`
- Upgradeable owner programs with ProgramData: `2`
- Accounts with canonical JUP key hits: `0`
- Accounts with current JupNet validator/vote/stake key hits: `0`

## Account Context

| Account | Context | Owner | Executable | Space | ProgramData | Signatures | Key hits |
|---|---|---|---|---:|---|---|---|
| `2sbhRE62pbi3sLo9CtjM7nYzUynEV4oBAPrGmQPrhnfF` |  | `None` | `None` | None | `None` | `20 latest 432509988` | `None` |
| `2x4wPZePCbq2W9tFfP2bagXjXnysdqNWQWMtwGMoyPFv` |  | `None` | `None` | None | `None` | `20 latest 432509988` | `None` |
| `3C1LxtpR3Mh5RQjydfeQdvRaAzpStWM7gBi1XzP9oyGt` |  | `jnoUtncGR9ZCCMixtys6Gzy5coTo6mnmUZuEHRQFTFV` | `False` | 320 | `None` | `20 latest 432509927` | `None` |
| `5Tv692BDJinbjR6Beb2K9bGmxnbQeFaGb1rJqCs2y3Q6` | embedded pubkey in 41-byte Bank-owned state | `None` | `None` | None | `None` | `0 latest none` | `None` |
| `7SnRzKKo8QonsMUb1wYCQoqCsLq2njp41yS33gJsVfp8` |  | `None` | `None` | None | `None` | `2 latest 432481982` | `None` |
| `9DvDdsw38EB3RPChPqHkgBmntFbM5v79QxMyMSbfXWuy` |  | `JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw` | `False` | 64 | `None` | `20 latest 432509988` | `None` |
| `Cei4rumgr8ePPdNCMim7yo4C6idaMNv3N8P3qqQbbjyf` |  | `None` | `None` | None | `None` | `2 latest 432481451` | `None` |
| `EG9fKpmLgkzCYZdj8uNDhHu5xmeXCZakccV6QmUavbzt` |  | `None` | `None` | None | `None` | `20 latest 432509988` | `None` |
| `H5Y5aLdTQXRWJ6kitWeUkHyAEVLPPfChgSxhUBVxZ3D2` |  | `None` | `None` | None | `None` | `3 latest 432481423` | `None` |
| `JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw` | owner program for 64-byte recurring account | `BPFLoaderUpgradeab1e11111111111111111111111` | `True` | 36 | `6fBvinpo8Ub7TVpUeTPpPiGMryL432i8N9Z3n3aH2KVT` | `20 latest 432509988` | `None` |
| `jnoUtncGR9ZCCMixtys6Gzy5coTo6mnmUZuEHRQFTFV` | owner program for 320-byte verify_request account | `BPFLoaderUpgradeab1e11111111111111111111111` | `True` | 36 | `D6xAx2iTMXP5hg8DeKPDgTw8exLs8MNpYEsmLg89pAsT` | `0 latest none` | `None` |

## Owner ProgramData

| Program | ProgramData | Deployment slot | Upgrade authority | Executable bytes | SHA256 | Relevant string hits |
|---|---|---:|---|---:|---|---|
| `JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw` | `6fBvinpo8Ub7TVpUeTPpPiGMryL432i8N9Z3n3aH2KVT` | 416240879 | `GRr146QcbpANhTZPCo9QBJa1tP5Fr9B6vfua4zRC5cc3` | 60000 | `8f7265a388f02f0ac21638d4f0ea4b59576f9da8b1c2ecbb56501087369c02b7` | `jup: programs/jupnet-inbox-program/src/instructions/emit.rs, programs/jupnet-inbox-program/src/inbox_events.rs, called `Result::unwrap()` on an `Err` valueEmit invokedSubmitInboxMessage invokedSubmitInboxMessageWithFinality invokedJUPNET_INBOX`<br>`jupnet: programs/jupnet-inbox-program/src/instructions/emit.rs, programs/jupnet-inbox-program/src/inbox_events.rs, called `Result::unwrap()` on an `Err` valueEmit invokedSubmitInboxMessage invokedSubmitInboxMessageWithFinality invokedJUPNET_INBOX`<br>`gum: ) when slicing `range end index PermissionDeniedAddrNotAvailable0123456789abcdefNotFoundTimedOut (bytes DeadlockcodeKindkind <=     WouldBlockOsmessageErrorCustomerrorConnectionRef`<br>`inbox: programs/jupnet-inbox-program/src/instructions/emit.rs, programs/jupnet-inbox-program/src/inbox_events.rs, called `Result::unwrap()` on an `Err` valueEmit invokedSubmitInboxMessage invokedSubmitInboxMessageWithFinality invokedJUPNET_INBOX` |
| `jnoUtncGR9ZCCMixtys6Gzy5coTo6mnmUZuEHRQFTFV` | `D6xAx2iTMXP5hg8DeKPDgTw8exLs8MNpYEsmLg89pAsT` | 431537850 | `GRr146QcbpANhTZPCo9QBJa1tP5Fr9B6vfua4zRC5cc3` | 149816 | `c438a773de1e9edc6cc36f98ad214724ee0753db5b6be71e6c4cceacac2c18f2` | `jup: programs/jupnet-outbox-program/src/state.rs, programs/jupnet-outbox-program/src/instructions/emergency_reset_merkle_root.rs`<br>`jupnet: programs/jupnet-outbox-program/src/state.rs, programs/jupnet-outbox-program/src/instructions/emergency_reset_merkle_root.rs`<br>`bls: UpdateMerkleRoot invokedMerkle proof verifiedVerifying BLS signatureSignature verifiedVerifyOutboxMessage invokedadvance_epoch_root: dropped root of epoch :OUTBOX`<br>`merkle: programs/jupnet-outbox-program/src/instructions/emergency_reset_merkle_root.rs, rNd0EmergencyResetMerkleRoot invoked, internal error: entered unreachable codefailed to fill whole bufferNot all bytes readassertion failed: src_len <= self.capacity - self.lenInitMerkleRoot invokedmerkle_root_state`<br>`proof: UpdateMerkleRoot invokedMerkle proof verifiedVerifying BLS signatureSignature verifiedVerifyOutboxMessage invokedadvance_epoch_root: dropped root of epoch :OUTBOX`<br>`outbox: programs/jupnet-outbox-program/src/state.rs, programs/jupnet-outbox-program/src/instructions/emergency_reset_merkle_root.rs, UpdateMerkleRoot invokedMerkle proof verifiedVerifying BLS signatureSignature verifiedVerifyOutboxMessage invokedadvance_epoch_root: dropped root of epoch :OUTBOX`<br>`root: programs/jupnet-outbox-program/src/instructions/emergency_reset_merkle_root.rs, rNd0EmergencyResetMerkleRoot invoked, internal error: entered unreachable codefailed to fill whole bufferNot all bytes readassertion failed: src_len <= self.capacity - self.lenInitMerkleRoot invokedmerkle_root_state` |

## Assessment

- The owner-context cluster did not expose canonical JUP key material.
- The owner-context cluster did not expose current JupNet validator, vote or stake keys.
- The recurring non-token state is controlled by small upgradeable Solana programs, so these accounts look like settlement/helper program state rather than a visible JUP security registry.
- ProgramData string hits, if present, should be treated as owner-program clues only unless they identify stake, quorum, signer weight, fee, slashing or governance state.
