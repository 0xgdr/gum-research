# Gum Omnichain Sender Program

## Scope

- Sender/program id recovered from outbox verifier payloads: `GUMebNDCYyF81xjyqaHagbgMQVUTb8fBC9YRh25xSH64`
- ProgramData derived from program account: `Gi8HgbHnykRiHboqG2VHysti773o8bNSjuFJWpyf4Q89`
- Expected ProgramData: `Gi8HgbHnykRiHboqG2VHysti773o8bNSjuFJWpyf4Q89`

## Account Metadata

| Account | Owner | Executable | Space | SHA256 |
|---|---|---|---:|---|
| Program | `BPFLoaderUpgradeab1e11111111111111111111111` | `True` | 36 | `e8f5cdb9c50f574466d5443fc9c0c8e16ae672eb95bd36c6ae8bcba464858c42` |
| ProgramData | `BPFLoaderUpgradeab1e11111111111111111111111` | `False` | 1140509 | `f4f2dfbe8c379fc1ed7cc97c45184b2849cdc13d0b1aafc0f8302eef2c524240` |

## ProgramData Header

- Deployment slot candidate: `106613674`
- Upgrade authority: `7RrBcJS6vbyMdLoYxQUqiUxD3CYVD55FvsGS5L5rfx2x`
- Executable length: `1140464`
- Executable SHA256: `136c7c999694e1e4999f2c71779564c1b001c2d60bc27bd10e692f4bb66f4734`

## Term Hits

| Term | Count | Examples |
|---|---:|---|
| `gum` | 12 | `programs/gum-omnichain/src/state/withdrawal_request.rs`<br>`programs/gum-omnichain/src/instructions/authorized/admin/register_unified_mint.rs`<br>`programs/gum-omnichain/src/state/deposit_addresses.rs`<br>`programs/gum-omnichain/src/lib.rs` |
| `jup` | 1 | `failed to write whole bufferfailed to fill whole buffera Display implementation returned an error unexpectedlyUnexpected length of inputErrorcalled `Result::unwrap()` on an `Err` valuejupderived_object__inbox_event_authU` |
| `omnichain` | 12 | `programs/gum-omnichain/src/state/withdrawal_request.rs`<br>`programs/gum-omnichain/src/instructions/authorized/admin/register_unified_mint.rs`<br>`programs/gum-omnichain/src/state/deposit_addresses.rs`<br>`programs/gum-omnichain/src/lib.rs` |
| `bls` | 2 | `123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyzprograms/gum-omnichain/src/utils/verification.rsInsufficientBalanceInvalidRequestStatusAccountNotWritablePdaKeyMismatchInvalidAccountMintKeyMismatchInvalidMintFee`<br>`sol_verify_bls_merkle_key` |
| `merkle` | 2 | `123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyzprograms/gum-omnichain/src/utils/verification.rsInsufficientBalanceInvalidRequestStatusAccountNotWritablePdaKeyMismatchInvalidAccountMintKeyMismatchInvalidMintFee`<br>`sol_verify_bls_merkle_key` |
| `proof` | 2 | `AccountNotSignerUnsupportedChainPermissionDeniedoutbox msg_hash BridgedNotLinkedTokenGroupMemberno storage spaceFeeOwnerMismatchAddrNotAvailable right` failed: 0123456789abcdefInvalidProgramIdinvalid SuiPayloadassertion `<br>`123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyzprograms/gum-omnichain/src/utils/verification.rsInsufficientBalanceInvalidRequestStatusAccountNotWritablePdaKeyMismatchInvalidAccountMintKeyMismatchInvalidMintFee` |
| `inbox` | 3 | `src/inbox.rs`<br>`failed to write whole bufferfailed to fill whole buffera Display implementation returned an error unexpectedlyUnexpected length of inputErrorcalled `Result::unwrap()` on an `Err` valuejupderived_object__inbox_event_authU`<br>`InboxEvent serializeinvalid finality thresholdMessage serialize0x` |
| `outbox` | 2 | `AccountNotSignerUnsupportedChainPermissionDeniedoutbox msg_hash BridgedNotLinkedTokenGroupMemberno storage spaceFeeOwnerMismatchAddrNotAvailable right` failed: 0123456789abcdefInvalidProgramIdinvalid SuiPayloadassertion `<br>`123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyzprograms/gum-omnichain/src/utils/verification.rsInsufficientBalanceInvalidRequestStatusAccountNotWritablePdaKeyMismatchInvalidAccountMintKeyMismatchInvalidMintFee` |
| `signature` | 4 | `TryFromIntErrorUnexpected variant index: CustomInvalidArgumentInvalidInstructionDataInvalidAccountDataAccountDataTooSmallInsufficientFundsIncorrectProgramIdMissingRequiredSignatureAccountAlreadyInitializedUninitializedAc`<br>`123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyzprograms/gum-omnichain/src/utils/verification.rsInsufficientBalanceInvalidRequestStatusAccountNotWritablePdaKeyMismatchInvalidAccountMintKeyMismatchInvalidMintFee`<br>`UnexpectedEofTrailingBytesInvalidVarianttype_nametagLengthOverflowlenassertion failed: key_size <= U64::to_usize()assertion failed: output_size <= U64::to_usize()assertion failed: salt.len() <= lengthassertion failed: pe`<br>`The arguments provided to a program instruction were invalidAn instruction's data contents was invalidAn account's data contents was invalidAn account's data was too smallAn account's balance was too small to complete th` |
| `message` | 4 | `src/message.rs`<br>`InboxEvent serializeinvalid finality thresholdMessage serialize0x`<br>`UnexpectedEofTrailingBytesInvalidVarianttype_nametagLengthOverflowlenassertion failed: key_size <= U64::to_usize()assertion failed: output_size <= U64::to_usize()assertion failed: salt.len() <= lengthassertion failed: pe`<br>`123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyzUnable to find a viable program address bump seedcalled `Result::unwrap()` on an `Err` valueUnexpected length of inputUnexpected length of inputWouldBlockpermissi` |
| `withdraw` | 5 | `programs/gum-omnichain/src/state/withdrawal_request.rs`<br>`AccountNotSignerUnsupportedChainPermissionDeniedoutbox msg_hash BridgedNotLinkedTokenGroupMemberno storage spaceFeeOwnerMismatchAddrNotAvailable right` failed: 0123456789abcdefInvalidProgramIdinvalid SuiPayloadassertion `<br>` account was not initialized via update_chain_configrequest_claim msg_hash programs/gum-omnichain/src/instructions/request_claim.rsprograms/gum-omnichain/src/instructions/request_swap.rsprograms/gum-omnichain/src/instruc`<br>`not implemented: signerchain_configadminrent_payerwithholdinguser_tokenevent_authorityprogramoutput_native_mintinput_native_mintfee_multisigfeeassociated_token_programholderholder_bridged_ataholder_unified_atadepositdepo` |
| `deposit` | 6 | `programs/gum-omnichain/src/state/deposit_addresses.rs`<br>`programs/gum-omnichain/src/state/deposit_request.rs`<br>`AccountNotSignerUnsupportedChainPermissionDeniedoutbox msg_hash BridgedNotLinkedTokenGroupMemberno storage spaceFeeOwnerMismatchAddrNotAvailable right` failed: 0123456789abcdefInvalidProgramIdinvalid SuiPayloadassertion `<br>`123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyzprograms/gum-omnichain/src/utils/verification.rsInsufficientBalanceInvalidRequestStatusAccountNotWritablePdaKeyMismatchInvalidAccountMintKeyMismatchInvalidMintFee` |
| `swap` | 12 | `swap`<br>`swap`<br>`swap`<br>`swap` |
| `mint` | 12 | `minty`<br>`minty`<br>`mint`<br>`mintyr` |
| `fee` | 7 | `TryFromIntErrorUnexpected variant index: CustomInvalidArgumentInvalidInstructionDataInvalidAccountDataAccountDataTooSmallInsufficientFundsIncorrectProgramIdMissingRequiredSignatureAccountAlreadyInitializedUninitializedAc`<br>`operatorCpiGuardPermanentDelegateNonTransferableAccountTransferHookTransferHookAccountConfidentialTransferFeeConfigConfidentialTransferFeeAmountMetadataPointerTokenMetadataGroupPointerTokenGroupGroupMemberPointer`<br>`AccountNotSignerUnsupportedChainPermissionDeniedoutbox msg_hash BridgedNotLinkedTokenGroupMemberno storage spaceFeeOwnerMismatchAddrNotAvailable right` failed: 0123456789abcdefInvalidProgramIdinvalid SuiPayloadassertion `<br>` account was not initialized via update_chain_configrequest_claim msg_hash programs/gum-omnichain/src/instructions/request_claim.rsprograms/gum-omnichain/src/instructions/request_swap.rsprograms/gum-omnichain/src/instruc` |

## Watched Key Hits

- Canonical JUP / current validator / vote / stake key hits in executable: `0`

## Assessment

- The outbox verifier sender/program candidate resolves to a live upgradeable JupNet executable.
- Executable strings identify it as `programs/gum-omnichain`, with deposit, withdrawal, swap, mint, inbox, outbox and BLS/Merkle verification surfaces.
- This strengthens the interpretation that sampled verifier payloads are Gum omnichain messages certified through the JupNet outbox verifier.
- The executable string/key scan did not expose a Dove registry, JUP-denominated stake weights, validator mappings, slashing or reward state.
