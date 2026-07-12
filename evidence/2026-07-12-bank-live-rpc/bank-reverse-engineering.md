# Solana Bank Reverse Engineering

## Instruction Variant Groups

- Sampled transactions scanned: `8`
- Distinct top-level Bank instruction variants: `5`

| Count | Discriminator | Data length | Account count | Likely Anchor name | Files | Mints | Logs |
|---:|---|---:|---:|---|---|---|---|
| 2 | `2817eaaf0e3d9ab1` | 52 | 20 | `sweep` | `solana-mainnet-bank-tx-3eTXuSzv.json, solana-mainnet-bank-tx-3tunHccR.json` | `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` 4 | `Program log: Instruction: Sweep` 2<br>`Program log: SubmitInboxMessageWithFinality invoked` 2 |
| 2 | `891f2fe4cdea81ed` | 463 | 9 | `verify_request` | `solana-mainnet-bank-tx-5EivNpnD.json, solana-mainnet-bank-tx-5JQFCWSE.json` |  | `Program log: Instruction: VerifyRequest` 2<br>`Program log: VerifyOutboxMessage invoked` 2<br>`Program log: Outbox verification passed` 2 |
| 2 | `b712469c946da122` | 8 | 20 | `withdraw` | `solana-mainnet-bank-tx-22PTevP3.json, solana-mainnet-bank-tx-2CnrMhsF.json` | `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` 6 | `Program log: Instruction: Withdraw` 2<br>`Program log: Withdrawal processed` 2<br>`Program log: SubmitInboxMessageWithFinality invoked` 2 |
| 1 | `14a2fae36fc17bec` | 17 | 21 | `rfq_sell_resolve` | `solana-mainnet-bank-tx-2uNAiE4g.json` | `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` 1 | `Program log: Instruction: RfqSellResolve` 1<br>`Program log: SubmitInboxMessageWithFinality invoked` 1 |
| 1 | `9ce6d1a96eebde14` | 8 | 18 | `rfq_sell_commit` | `solana-mainnet-bank-tx-5yxi7NH.json` | `So11111111111111111111111111111111111111112` 2<br>`EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` 1 | `Program log: Instruction: RfqSellCommit` 1 |

## Variant Account Roles

### `2817eaaf0e3d9ab1` length `52` accounts `20`

- Signer accounts: `JUPW3tHBxmNRzVnLmTyYUsUDB6izZSEtupY6znBC5mo`
- Writable accounts: `JUPW3tHBxmNRzVnLmTyYUsUDB6izZSEtupY6znBC5mo, C8VeT16ySsyMW9xijjmYgvw83FfvEZVJawn5jgpzcf1X, 9DvDdsw38EB3RPChPqHkgBmntFbM5v79QxMyMSbfXWuy, ECho1E2CXg3smpWVqjwpLpgv2A2KzKUeqXuTg9XyBr8R, HPRQqnbrjnP8m5yu1ZG3sN4c16n7ne17iXuuCE2ACgU5, 63S6bZgc9Gky6uFv5g2FyNhwgqKZFKTr22gyT8nowz9b, FZNvPAp875kXHS6Vpu2zJkLfZxp4QCEquTjdfYgXAeGB`
- Readonly accounts: `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ, HVKuqyK6wjexdVJAUARiGdQTdGBBWhdYyhCZGFXh9d4s, 2sbhRE62pbi3sLo9CtjM7nYzUynEV4oBAPrGmQPrhnfF, EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v, 5x38Kp4hvdomTCnCrAny4UtMUt5rQBdB6px2K1Ui45Wq, TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA, ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL, 11111111111111111111111111111111, Sysvar1nstructions1111111111111111111111111, EG9fKpmLgkzCYZdj8uNDhHu5xmeXCZakccV6QmUavbzt, JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw, 2x4wPZePCbq2W9tFfP2bagXjXnysdqNWQWMtwGMoyPFv, gum1UnP99NnohRt3YcdkA4PGubCYvtWiH8mgjT2KhXH, 4rAgpDkj9iB2cN6BXdQu8Q26RKQaPuZSsDGcQHjCaqz7`

### `891f2fe4cdea81ed` length `463` accounts `9`

- Signer accounts: `JUPW3tHBxmNRzVnLmTyYUsUDB6izZSEtupY6znBC5mo`
- Writable accounts: `JUPW3tHBxmNRzVnLmTyYUsUDB6izZSEtupY6znBC5mo, 7SnRzKKo8QonsMUb1wYCQoqCsLq2njp41yS33gJsVfp8, Cei4rumgr8ePPdNCMim7yo4C6idaMNv3N8P3qqQbbjyf`
- Readonly accounts: `HVKuqyK6wjexdVJAUARiGdQTdGBBWhdYyhCZGFXh9d4s, 3C1LxtpR3Mh5RQjydfeQdvRaAzpStWM7gBi1XzP9oyGt, jnoUtncGR9ZCCMixtys6Gzy5coTo6mnmUZuEHRQFTFV, 11111111111111111111111111111111, Sysvar1nstructions1111111111111111111111111, 2x4wPZePCbq2W9tFfP2bagXjXnysdqNWQWMtwGMoyPFv, BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ`

### `b712469c946da122` length `8` accounts `20`

- Signer accounts: `JUPW3tHBxmNRzVnLmTyYUsUDB6izZSEtupY6znBC5mo`
- Writable accounts: `JUPW3tHBxmNRzVnLmTyYUsUDB6izZSEtupY6znBC5mo, 7jqXWdiyYkY9XUStYhbGzSgn1VCr9tMF4LNCK52oG76U, 5RD1PyMjzgo3gMCToQTnqk44L99kQZ3MnGnRzxMwRwLj, C8VeT16ySsyMW9xijjmYgvw83FfvEZVJawn5jgpzcf1X, 9DvDdsw38EB3RPChPqHkgBmntFbM5v79QxMyMSbfXWuy, 7SnRzKKo8QonsMUb1wYCQoqCsLq2njp41yS33gJsVfp8, 8NiTpug6V5SeWN42wwTGqUcKM3y6dCnRR6ouV7sf4Kak, Cei4rumgr8ePPdNCMim7yo4C6idaMNv3N8P3qqQbbjyf, ESLg5R1Ry4LXSfxh67BUPusKHeHGpaJWHGjTGeg6oYGE`
- Readonly accounts: `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ, HVKuqyK6wjexdVJAUARiGdQTdGBBWhdYyhCZGFXh9d4s, 2sbhRE62pbi3sLo9CtjM7nYzUynEV4oBAPrGmQPrhnfF, EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v, TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA, ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL, 11111111111111111111111111111111, EG9fKpmLgkzCYZdj8uNDhHu5xmeXCZakccV6QmUavbzt, JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw, 2x4wPZePCbq2W9tFfP2bagXjXnysdqNWQWMtwGMoyPFv`

### `14a2fae36fc17bec` length `17` accounts `21`

- Signer accounts: `rfQMFpNueeNufBW4byyEAhvL4To4tCsVBVagcEWG8ea`
- Writable accounts: `rfQMFpNueeNufBW4byyEAhvL4To4tCsVBVagcEWG8ea, H5Y5aLdTQXRWJ6kitWeUkHyAEVLPPfChgSxhUBVxZ3D2, 4s3gnkf1R2UzAWbfvVowfaW7VdLDNSQhmwjYcSnMYwmT, GqpFMhoHzfhUnM65kvCRkzozm4c72A9TpNZzt9D69z88, C8VeT16ySsyMW9xijjmYgvw83FfvEZVJawn5jgpzcf1X, 5DtSBy1imR7W2Zbdt9Z1gfRPVmVZyTVorvi562SZ7bvd, 9DvDdsw38EB3RPChPqHkgBmntFbM5v79QxMyMSbfXWuy`
- Readonly accounts: `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ, TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA, HVKuqyK6wjexdVJAUARiGdQTdGBBWhdYyhCZGFXh9d4s, 2sbhRE62pbi3sLo9CtjM7nYzUynEV4oBAPrGmQPrhnfF, So11111111111111111111111111111111111111112, EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v, 5x38Kp4hvdomTCnCrAny4UtMUt5rQBdB6px2K1Ui45Wq, EG9fKpmLgkzCYZdj8uNDhHu5xmeXCZakccV6QmUavbzt, JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw, 2x4wPZePCbq2W9tFfP2bagXjXnysdqNWQWMtwGMoyPFv`

### `9ce6d1a96eebde14` length `8` accounts `18`

- Signer accounts: `rfQMFpNueeNufBW4byyEAhvL4To4tCsVBVagcEWG8ea`
- Writable accounts: `rfQMFpNueeNufBW4byyEAhvL4To4tCsVBVagcEWG8ea, 4s3gnkf1R2UzAWbfvVowfaW7VdLDNSQhmwjYcSnMYwmT, GqpFMhoHzfhUnM65kvCRkzozm4c72A9TpNZzt9D69z88, C8VeT16ySsyMW9xijjmYgvw83FfvEZVJawn5jgpzcf1X, DnM9teVNbi4Cebkqtar3sVJs9LcZWSrV8DhwQzPpSeqM, 5DtSBy1imR7W2Zbdt9Z1gfRPVmVZyTVorvi562SZ7bvd`
- Readonly accounts: `TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA, BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ, H5Y5aLdTQXRWJ6kitWeUkHyAEVLPPfChgSxhUBVxZ3D2, HVKuqyK6wjexdVJAUARiGdQTdGBBWhdYyhCZGFXh9d4s, 2sbhRE62pbi3sLo9CtjM7nYzUynEV4oBAPrGmQPrhnfF, So11111111111111111111111111111111111111112, EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v, ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL, 11111111111111111111111111111111, 2x4wPZePCbq2W9tFfP2bagXjXnysdqNWQWMtwGMoyPFv`

## Parsed Token Mints Across Samples

- `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v`: `12`
- `So11111111111111111111111111111111111111112`: `2`

## ProgramData Binary String Scan

### Bank

- Present: `True`
- Owner: `BPFLoaderUpgradeab1e11111111111111111111111`
- Account space: `602517`
- Deployment slot: `425956918`
- Upgrade authority: `F5p1mBd6C3v6NB2oLGM9bLKmtHQ53RMsYKeGPPg4s113`
- Executable byte length: `602472`
- Executable SHA256: `44b58a16d622d80648022be699cff39762aa3d3110b80491add9c6372f48315c`
- Printable strings extracted: `314`

| Term | Hit count | Sample strings |
|---|---:|---|
| `proof` | 5 | `internal error: entered unreachable codefailed to fill whole buffer()a Display implementation returned an error unexpectedly/Users/runner/work/platform-tools/platform-tools/out/rust/library/alloc/src/string.rsInvalid bool representation: Er`<br>`mintmerkle_proof_hashes_bufferprograms/bank/src/instructions/create_or_append_request_buffer.rsprograms/bank/src/instructions/invalidate_request.rs`<br>`invalidate_requestSignature verifiedrequestunique request account data writtencalled `Result::unwrap()` on an `Err` valueprograms/bank/src/instructions/request.rsvaultjupnet valid_till impl program key message_hash programs/bank/src/instruc`<br>`AccountNotSignerPermissionDeniedUnexpiredRequestsrc/primitive.rsAddrNotAvailable right` failed: 0123456789abcdefInvalidProgramIdInvalidMerkleProofInvalidEpochMerkleRootNotFoundBankDisabledInvalidAccountNoReturnDataInvalidReturnDataUniqueReq`<br>`programs/bank/src/lib.rsInstruction: IdlCreateAccountanchor:idlInstruction: IdlResizeAccountdata_len should always be >= the current account spaceInstruction: IdlCloseAccountInstruction: IdlCreateBufferInstruction: IdlWriteInstruction: IdlS` |
| `signer` | 3 | `rNd0A signer constraint was violatedInstruction: WithdrawBankToAdminAn owner constraint was violatedProgramError caused by account: src/de/mod.rs`<br>`ConstraintHasOneConstraintSignerassertion `left ) when slicing `InvalidSignaturerange end index . Error Number: `<br>`AccountNotSignerPermissionDeniedUnexpiredRequestsrc/primitive.rsAddrNotAvailable right` failed: 0123456789abcdefInvalidProgramIdInvalidMerkleProofInvalidEpochMerkleRootNotFoundBankDisabledInvalidAccountNoReturnDataInvalidReturnDataUniqueReq` |
| `merkle` | 5 | `internal error: entered unreachable codefailed to fill whole buffer()a Display implementation returned an error unexpectedly/Users/runner/work/platform-tools/platform-tools/out/rust/library/alloc/src/string.rsInvalid bool representation: Er`<br>`mintmerkle_proof_hashes_bufferprograms/bank/src/instructions/create_or_append_request_buffer.rsprograms/bank/src/instructions/invalidate_request.rs`<br>`invalidate_requestSignature verifiedrequestunique request account data writtencalled `Result::unwrap()` on an `Err` valueprograms/bank/src/instructions/request.rsvaultjupnet valid_till impl program key message_hash programs/bank/src/instruc`<br>`AccountNotSignerPermissionDeniedUnexpiredRequestsrc/primitive.rsAddrNotAvailable right` failed: 0123456789abcdefInvalidProgramIdInvalidMerkleProofInvalidEpochMerkleRootNotFoundBankDisabledInvalidAccountNoReturnDataInvalidReturnDataUniqueReq`<br>`programs/bank/src/lib.rsInstruction: IdlCreateAccountanchor:idlInstruction: IdlResizeAccountdata_len should always be >= the current account spaceInstruction: IdlCloseAccountInstruction: IdlCreateBufferInstruction: IdlWriteInstruction: IdlS` |
| `jup` | 1 | `invalidate_requestSignature verifiedrequestunique request account data writtencalled `Result::unwrap()` on an `Err` valueprograms/bank/src/instructions/request.rsvaultjupnet valid_till impl program key message_hash programs/bank/src/instruc` |
| `fee` | 1 | `src/state.rssrc/barret.rsassertion failed: divisor.leading_zeros() == 0LayoutErrormid > lensrc/add.rssrc/buffer.rsinternal error: entered unreachable codesrc/repr.rssrc/math.rsassertion failed: capacity > 0 && capacity <= Self::MAX_CAPACITY` |
| `authority` | 4 | `internal error: entered unreachable codefailed to fill whole buffer()a Display implementation returned an error unexpectedly/Users/runner/work/platform-tools/platform-tools/out/rust/library/alloc/src/string.rsInvalid bool representation: Er`<br>`AccountNotSignerPermissionDeniedUnexpiredRequestsrc/primitive.rsAddrNotAvailable right` failed: 0123456789abcdefInvalidProgramIdInvalidMerkleProofInvalidEpochMerkleRootNotFoundBankDisabledInvalidAccountNoReturnDataInvalidReturnDataUniqueReq`<br>`programs/bank/src/lib.rsInstruction: IdlCreateAccountanchor:idlInstruction: IdlResizeAccountdata_len should always be >= the current account spaceInstruction: IdlCloseAccountInstruction: IdlCreateBufferInstruction: IdlWriteInstruction: IdlS`<br>`src/state.rssrc/barret.rsassertion failed: divisor.leading_zeros() == 0LayoutErrormid > lensrc/add.rssrc/buffer.rsinternal error: entered unreachable codesrc/repr.rssrc/math.rsassertion failed: capacity > 0 && capacity <= Self::MAX_CAPACITY` |

### Bank Program

- Present: `True`
- Owner: `BPFLoaderUpgradeab1e11111111111111111111111`
- Account space: `795965`
- Deployment slot: `432453318`
- Upgrade authority: `GRr146QcbpANhTZPCo9QBJa1tP5Fr9B6vfua4zRC5cc3`
- Executable byte length: `795920`
- Executable SHA256: `e12d39ee6591d6c9e58460f1ada4addb5bed76cedbc703284ce7bfcd4c60744d`
- Printable strings extracted: `895`

| Term | Hit count | Sample strings |
|---|---:|---|
| `Outbox verification passed` | 1 | `swap_authorityprograms/bank/src/instructions/sweep.rsjupOutbox verification passed` |
| `Withdrawal processed` | 1 | `AccountNotSignerPermissionDeniedAddrNotAvailable0123456789abcdefverified_messageDataTypeMismatchInvalidProgramIdtemp_vaultWithdrawal processedprograms/bank/src/instructions/withdraw.rsprograms/bank/src/state/mod.rsprograms/bank/src/utils/mo` |
| `inbox` | 5 | `programs/bank/src/utils/inbox.rs
`<br>`src/inbox.rs`<br>`__inbox_event_authfailed to fill whole bufferfailed to write whole buffera Display implementation returned an error unexpectedlyUnexpected length of inputInvalid bool representation: ErrorUnexpectedEofTrailingBytesInvalidVarianttype_nametag`<br>`AccountNotSignerPermissionDeniedAddrNotAvailable0123456789abcdefverified_messageDataTypeMismatchInvalidProgramIdtemp_vaultWithdrawal processedprograms/bank/src/instructions/withdraw.rsprograms/bank/src/state/mod.rsprograms/bank/src/utils/mo`<br>`Unable to find a viable program address bump seedUnable to find a viable program address bump seedJUPNET_INBOX__inbox_event_authmerkle_root_stateborsh serializationa Display implementation returned an error unexpectedlyErrorCustomInvalidArg` |
| `outbox` | 3 | `src/outbox.rs`<br>`swap_authorityprograms/bank/src/instructions/sweep.rsjupOutbox verification passed`<br>`AccountNotSignerPermissionDeniedAddrNotAvailable0123456789abcdefverified_messageDataTypeMismatchInvalidProgramIdtemp_vaultWithdrawal processedprograms/bank/src/instructions/withdraw.rsprograms/bank/src/state/mod.rsprograms/bank/src/utils/mo` |
| `signer` | 3 | `}A signer constraint was violatedAn owner constraint was violatedFailed to serialize wire payload`<br>`ConstraintHasOneConstraintSigner) when slicing `range end index . Error Number: `<br>`AccountNotSignerPermissionDeniedAddrNotAvailable0123456789abcdefverified_messageDataTypeMismatchInvalidProgramIdtemp_vaultWithdrawal processedprograms/bank/src/instructions/withdraw.rsprograms/bank/src/state/mod.rsprograms/bank/src/utils/mo` |
| `merkle` | 1 | `Unable to find a viable program address bump seedUnable to find a viable program address bump seedJUPNET_INBOX__inbox_event_authmerkle_root_stateborsh serializationa Display implementation returned an error unexpectedlyErrorCustomInvalidArg` |
| `jup` | 4 | `jupn`<br>`swap_authorityprograms/bank/src/instructions/sweep.rsjupOutbox verification passed`<br>`AccountNotSignerPermissionDeniedAddrNotAvailable0123456789abcdefverified_messageDataTypeMismatchInvalidProgramIdtemp_vaultWithdrawal processedprograms/bank/src/instructions/withdraw.rsprograms/bank/src/state/mod.rsprograms/bank/src/utils/mo`<br>`Unable to find a viable program address bump seedUnable to find a viable program address bump seedJUPNET_INBOX__inbox_event_authmerkle_root_stateborsh serializationa Display implementation returned an error unexpectedlyErrorCustomInvalidArg` |
| `fee` | 3 | `src/extension/transfer_fee/instruction.rs`<br>`AccountNotSignerPermissionDeniedAddrNotAvailable0123456789abcdefverified_messageDataTypeMismatchInvalidProgramIdtemp_vaultWithdrawal processedprograms/bank/src/instructions/withdraw.rsprograms/bank/src/state/mod.rsprograms/bank/src/utils/mo`<br>`Unable to find a viable program address bump seedUnable to find a viable program address bump seedJUPNET_INBOX__inbox_event_authmerkle_root_stateborsh serializationa Display implementation returned an error unexpectedlyErrorCustomInvalidArg` |
| `authority` | 5 | `truncated on char boundary__event_authority`<br>`swap_authorityprograms/bank/src/instructions/sweep.rsjupOutbox verification passed`<br>`AccountNotSignerPermissionDeniedAddrNotAvailable0123456789abcdefverified_messageDataTypeMismatchInvalidProgramIdtemp_vaultWithdrawal processedprograms/bank/src/instructions/withdraw.rsprograms/bank/src/state/mod.rsprograms/bank/src/utils/mo`<br>`Unable to find a viable program address bump seedUnable to find a viable program address bump seedJUPNET_INBOX__inbox_event_authmerkle_root_stateborsh serializationa Display implementation returned an error unexpectedlyErrorCustomInvalidArg`<br>`The arguments provided to a program instruction were invalidAn instruction's data contents was invalidAn account's data contents was invalidAn account's data was too smallAn account's balance was too small to complete the instructionThe acc` |

## Utility Assessment

- The sampled Bank Program transactions group into a small number of instruction variants with Anchor-style logging.
- Inbox/outbox strings are present in sampled transaction logs and binary strings.
- Canonical JUP was not observed as a parsed token mint in the sampled transactions.
- Binary string hits are clues only; they do not prove JUP-denominated stake, signer weight, quorum, fees or validator security.
