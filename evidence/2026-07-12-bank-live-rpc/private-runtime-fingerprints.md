# Private Runtime Fingerprint Hunt

## Purpose

This pass searches saved public artifacts for strings that would connect the visible Gum/JupNet verifier layer to private runtime, Dove, stake-weight or quorum implementation details.

It scans decoded account data, ProgramData executable bytes, transaction instruction bytes and JSON/log text from the snapshot.

## Scope

- Snapshot: `evidence/2026-07-12-bank-live-rpc`
- JSON artifacts scanned: `204`
- Decoded/text blobs scanned: `3418`
- Private runtime dependency terms with hits: `2`
- Security producer terms with hits: `0`
- Public verifier terms with hits: `10`
- JupNet/Gum source paths recovered: `24`

## Private Runtime Dependency Terms

| Term | Hit count | Artifacts |
|---|---:|---|
| `jupnet-svm` | 0 | `None` |
| `jupnet_svm` | 0 | `None` |
| `jupnet-vote` | 0 | `None` |
| `jupnet_vote` | 0 | `None` |
| `jupnet-vote-program` | 0 | `None` |
| `jupnet_vote_program` | 0 | `None` |
| `jupnet-bls-sdk` | 0 | `None` |
| `jupnet_bls_sdk` | 0 | `None` |
| `jupnet-bn254` | 0 | `None` |
| `jupnet_bn254` | 1 | `jupnet-programdata-brhPfKEx.json | $.result.value.data[base64]` |
| `jupnet-merkle-tree` | 0 | `None` |
| `jupnet_merkle_tree` | 0 | `None` |
| `jupnet-crosschain-hash` | 0 | `None` |
| `jupnet_crosschain_hash` | 1 | `jupnet-programdata-brhPfKEx.json | $.result.value.data[base64]` |
| `jupnet-define-syscall` | 0 | `None` |
| `jupnet_define_syscall` | 0 | `None` |

## Security Producer Terms

| Term | Hit count | Artifacts |
|---|---:|---|
| `dove` | 0 | `None` |
| `doves` | 0 | `None` |
| `validator_set` | 0 | `None` |
| `validator set` | 0 | `None` |
| `stake_weight` | 0 | `None` |
| `stake weight` | 0 | `None` |
| `vote_weight` | 0 | `None` |
| `vote weight` | 0 | `None` |
| `signer_set` | 0 | `None` |
| `signer set` | 0 | `None` |
| `quorum` | 0 | `None` |
| `root_builder` | 0 | `None` |
| `root builder` | 0 | `None` |
| `aggregate_key_set` | 0 | `None` |
| `aggregate key set` | 0 | `None` |
| `slashing` | 0 | `None` |
| `slash` | 0 | `None` |
| `reward` | 0 | `None` |

## Public Verifier Terms

| Term | Hit count | Artifacts |
|---|---:|---|
| `sol_verify_bls_merkle_key` | 3 | `getAccountInfo-GUMebProgramData-full.json | $.result.value.data[base64]`<br>`jupnet-programdata-GUMebNDC.json | $.result.value.data[base64]`<br>`jupnet-programdata-brhPfKEx.json | $.result.value.data[base64]` |
| `jupnet_alt_bn128_bls` | 1 | `jupnet-programdata-brhPfKEx.json | $.result.value.data[base64]` |
| `programs/jupnet-inbox-program` | 1 | `solana-mainnet-getAccountInfo-OwnerProgramData-JNiN12VC.json | $.result.value.data[base64]` |
| `programs/jupnet-outbox-program` | 1 | `solana-mainnet-getAccountInfo-OwnerProgramData-jnoUtncG.json | $.result.value.data[base64]` |
| `programs/gum-omnichain` | 2 | `getAccountInfo-GUMebProgramData-full.json | $.result.value.data[base64]`<br>`jupnet-programdata-GUMebNDC.json | $.result.value.data[base64]` |
| `verifyoutboxmessage` | 22 | `solana-mainnet-bank-tx-5EivNpnD.json | json-text`<br>`solana-mainnet-bank-tx-5JQFCWSE.json | json-text`<br>`solana-mainnet-getAccountInfo-OwnerProgramData-jnoUtncG.json | $.result.value.data[base64]`<br>`solana-mainnet-outbox-history-tx-1mim5qob.json | json-text`<br>`solana-mainnet-outbox-history-tx-39oSPwzK.json | json-text`<br>`solana-mainnet-outbox-history-tx-3AWbovCV.json | json-text`<br>`solana-mainnet-outbox-history-tx-3g4Rr5eJ.json | json-text`<br>`solana-mainnet-outbox-history-tx-3pchZaxG.json | json-text`<br>`solana-mainnet-outbox-history-tx-3ruC8wFv.json | json-text`<br>`solana-mainnet-outbox-history-tx-4ei1NQTh.json | json-text` |
| `updatemerkleroot` | 3 | `solana-mainnet-getAccountInfo-GumBankProgramData-full.json | $.result.value.data[base64]`<br>`solana-mainnet-getAccountInfo-OwnerProgramData-jnoUtncG.json | $.result.value.data[base64]`<br>`solana-mainnet-outbox-tx-3Zjq8FZd.json | json-text` |
| `merkle proof verified` | 3 | `solana-mainnet-getAccountInfo-GumBankProgramData-full.json | $.result.value.data[base64]`<br>`solana-mainnet-getAccountInfo-OwnerProgramData-jnoUtncG.json | $.result.value.data[base64]`<br>`solana-mainnet-outbox-tx-3Zjq8FZd.json | json-text` |
| `verifying bls signature` | 2 | `solana-mainnet-getAccountInfo-OwnerProgramData-jnoUtncG.json | $.result.value.data[base64]`<br>`solana-mainnet-outbox-tx-3Zjq8FZd.json | json-text` |
| `signature verified` | 3 | `solana-mainnet-getAccountInfo-GumBankProgramData-full.json | $.result.value.data[base64]`<br>`solana-mainnet-getAccountInfo-OwnerProgramData-jnoUtncG.json | $.result.value.data[base64]`<br>`solana-mainnet-outbox-tx-3Zjq8FZd.json | json-text` |

## JupNet/Gum Source Paths

| Source path | Artifact references |
|---|---|
| `programs/gum-omnichain/src/events.rs` | `getAccountInfo-GUMebProgramData-full.json | $.result.value.data[base64]`<br>`jupnet-programdata-GUMebNDC.json | $.result.value.data[base64]` |
| `programs/gum-omnichain/src/instructions/authorized/admin/bind_unified_mint.rsprograms/gum-omnichain/src/instructions/authorized/admin/register_unified_mint.rsprograms/gum-omnichain/src/instructions/authorized/admin/unbind_unified_mint.rsunified-toprograms/gum-omnichain/src/instructions/authorized/admin/update_chain_config.rschain-programs/gum-omnichain/src/instructions/authorized/admin/update_managed_mint_metadata.rsprograms/gum-omnichain/src/instructions/authorized/operator/register_bridged_mint.rsprograms/gum-omnichain/src/instructions/authorized/operator/request_discounted_swap.rswithdrawal_requestswap_requestprograms/gum-omnichain/src/instructions/complete_claim.rs__event_authorityprograms/gum-omnichain/src/instructions/complete_swap.rsprograms/gum-omnichain/src/instructions/convert_managed_mint.rsprograms/gum-omnichain/src/instructions/deposit.rs` | `getAccountInfo-GUMebProgramData-full.json | $.result.value.data[base64]`<br>`jupnet-programdata-GUMebNDC.json | $.result.value.data[base64]` |
| `programs/gum-omnichain/src/instructions/authorized/admin/register_unified_mint.rs` | `getAccountInfo-GUMebProgramData-full.json | $.result.value.data[base64]`<br>`jupnet-programdata-GUMebNDC.json | $.result.value.data[base64]` |
| `programs/gum-omnichain/src/instructions/authorized/admin/update_managed_mint_metadata.rs` | `getAccountInfo-GUMebProgramData-full.json | $.result.value.data[base64]`<br>`jupnet-programdata-GUMebNDC.json | $.result.value.data[base64]` |
| `programs/gum-omnichain/src/instructions/initialize_deposit_addresses.rsinput_tokenprograms/gum-omnichain/src/state/deposit_addresses.rsprograms/gum-omnichain/src/state/deposit_request.rsprograms/gum-omnichain/src/state/swap_request.rsprograms/gum-omnichain/src/state/withdrawal_request.rs` | `getAccountInfo-GUMebProgramData-full.json | $.result.value.data[base64]`<br>`jupnet-programdata-GUMebNDC.json | $.result.value.data[base64]` |
| `programs/gum-omnichain/src/instructions/request_claim.rsprograms/gum-omnichain/src/instructions/request_swap.rsprograms/gum-omnichain/src/instructions/request_withdrawal.rsprograms/gum-omnichain/src/state/chain_config.rsprograms/gum-omnichain/src/state/managed_mint.rsprograms/gum-omnichain/src/utils/fee.rs` | `getAccountInfo-GUMebProgramData-full.json | $.result.value.data[base64]`<br>`jupnet-programdata-GUMebNDC.json | $.result.value.data[base64]` |
| `programs/gum-omnichain/src/lib.rs` | `getAccountInfo-GUMebProgramData-full.json | $.result.value.data[base64]`<br>`jupnet-programdata-GUMebNDC.json | $.result.value.data[base64]` |
| `programs/gum-omnichain/src/state/chain_config.rs` | `getAccountInfo-GUMebProgramData-full.json | $.result.value.data[base64]`<br>`jupnet-programdata-GUMebNDC.json | $.result.value.data[base64]` |
| `programs/gum-omnichain/src/state/deposit_addresses.rs` | `getAccountInfo-GUMebProgramData-full.json | $.result.value.data[base64]`<br>`jupnet-programdata-GUMebNDC.json | $.result.value.data[base64]` |
| `programs/gum-omnichain/src/state/deposit_request.rs` | `getAccountInfo-GUMebProgramData-full.json | $.result.value.data[base64]`<br>`jupnet-programdata-GUMebNDC.json | $.result.value.data[base64]` |
| `programs/gum-omnichain/src/state/managed_mint.rs` | `getAccountInfo-GUMebProgramData-full.json | $.result.value.data[base64]`<br>`jupnet-programdata-GUMebNDC.json | $.result.value.data[base64]` |
| `programs/gum-omnichain/src/state/swap_request.rs` | `getAccountInfo-GUMebProgramData-full.json | $.result.value.data[base64]`<br>`jupnet-programdata-GUMebNDC.json | $.result.value.data[base64]` |
| `programs/gum-omnichain/src/state/withdrawal_request.rs` | `getAccountInfo-GUMebProgramData-full.json | $.result.value.data[base64]`<br>`jupnet-programdata-GUMebNDC.json | $.result.value.data[base64]` |
| `programs/gum-omnichain/src/utils/initialize_bridged_mint.rs` | `getAccountInfo-GUMebProgramData-full.json | $.result.value.data[base64]`<br>`jupnet-programdata-GUMebNDC.json | $.result.value.data[base64]` |
| `programs/gum-omnichain/src/utils/mint.rsprograms/gum-omnichain/src/utils/swap.rs` | `getAccountInfo-GUMebProgramData-full.json | $.result.value.data[base64]`<br>`jupnet-programdata-GUMebNDC.json | $.result.value.data[base64]` |
| `programs/gum-omnichain/src/utils/verification.rs` | `getAccountInfo-GUMebProgramData-full.json | $.result.value.data[base64]`<br>`jupnet-programdata-GUMebNDC.json | $.result.value.data[base64]` |
| `programs/jupnet-inbox-program/src/inbox_events.rs` | `solana-mainnet-getAccountInfo-OwnerProgramData-JNiN12VC.json | $.result.value.data[base64]` |
| `programs/jupnet-inbox-program/src/instructions/emit.rs` | `solana-mainnet-getAccountInfo-OwnerProgramData-JNiN12VC.json | $.result.value.data[base64]` |
| `programs/jupnet-outbox-program/src/instructions/emergency_reset_merkle_root.rs` | `solana-mainnet-getAccountInfo-OwnerProgramData-jnoUtncG.json | $.result.value.data[base64]` |
| `programs/jupnet-outbox-program/src/state.rs` | `solana-mainnet-getAccountInfo-OwnerProgramData-jnoUtncG.json | $.result.value.data[base64]` |
| `src/instructions/initialize.rsgum-omnichain/src/instructions/initialize_deposit_addresses.rsdeposit_addresses3d602d80600a3d3981f3363d3d373d3d3d363d735af43d82803e903d91602b57fd5bf3jupsweep_account_createdgum-omnichain/src/instructions/register_sui_sweep_account.rs` | `jupnet-programdata-brhPfKEx.json | $.result.value.data[base64]` |
| `src/instructions/update_chain_config.rsgum-omnichain/src/instructions/account_burned_amount.rs` | `jupnet-programdata-brhPfKEx.json | $.result.value.data[base64]` |
| `src/state/account/request_withdrawal.rsgum-omnichain/src/state/account/initialize.rs` | `jupnet-programdata-brhPfKEx.json | $.result.value.data[base64]` |
| `src/utils/init_mint_account.rsgum-omnichain/src/utils/initialize_unified_usd_mint.rsgum-omnichain/src/utils/mint.rs` | `jupnet-programdata-brhPfKEx.json | $.result.value.data[base64]` |

## Private Runtime Context Examples

### `jupnet_bn254`

- `jupnet-programdata-brhPfKEx.json` `$.result.value.data[base64]`: `43..L__unnamed_47.jupnet_alt_bn128_bls.1fda9e82f93c5a14-cgu.0.LBB0_2.LBB0_3.LBB8_2.LBB8_3.jupnet_bn254.20303437e8480312-cgu.0.LBB4_2.LBB4_3.LBB6_2.LBB6_3.LBB10_4.LBB10_3.jupnet_program.db3e8d1`

### `jupnet_crosschain_hash`

- `jupnet-programdata-brhPfKEx.json` `$.result.value.data[base64]`: `7d-cgu.0.jupnet_serialize_utils.3494eb35fefd573e-cgu.0.jupnet_rent.5752aa8b34e6f920-cgu.0.jupnet_crosschain_hash.bfffe4da37cf68a5-cgu.0.log.d6e5e5d0f7cecb40-cgu.0.jupnet_cpi.81cb33522d75a01a-cgu.0.jupne`

## Security Producer Context Examples

- None

## Public Verifier Context Examples

### `sol_verify_bls_merkle_key`

- `getAccountInfo-GUMebProgramData-full.json` `$.result.value.data[base64]`: `compression.sol_alt_bn128_group_op.sol_keccak256.sol_try_find_program_address.sol_memcpy_.sol_verify_bls_merkle_key.sol_get_clock_sysvar.sol_get_rent_sysvar.sol_dispatch_outbound_hash.sol_invoke_signed_rus`
- `jupnet-programdata-GUMebNDC.json` `$.result.value.data[base64]`: `compression.sol_alt_bn128_group_op.sol_keccak256.sol_try_find_program_address.sol_memcpy_.sol_verify_bls_merkle_key.sol_get_clock_sysvar.sol_get_rent_sysvar.sol_dispatch_outbound_hash.sol_invoke_signed_rus`
- `jupnet-programdata-brhPfKEx.json` `$.result.value.data[base64]`: `address.sol_create_program_address.abort.sol_alt_bn128_compression.sol_alt_bn128_group_op.sol_verify_bls_merkle_key.sol_keccak256.sol_log_data.sol_get_clock_sysvar.sol_get_rent_sysvar.sol_dispatch_outbound`

### `jupnet_alt_bn128_bls`

- `jupnet-programdata-brhPfKEx.json` `$.result.value.data[base64]`: `2adcd1e95ef7c7E.LBB4_2.LBB4_3.LBB4_14.LBB4_15.LBB4_11.LBB4_6.LBB4_12.LBB4_10.LBB4_13._ZN20jupnet_alt_bn128_bls8g2_point7G2Point16verify_signature17he7f0aeba795deafbE.LBB5_4.LBB5_6.LBB5_22.LBB5_8.LBB5_`

### `programs/jupnet-inbox-program`

- `solana-mainnet-getAccountInfo-OwnerProgramData-JNiN12VC.json` `$.result.value.data[base64]`: `............t.(Vc.i.^..^...Km\sU[!....failed to write whole buffer()src/entrypoint/mod.rs.programs/jupnet-inbox-program/src/instructions/emit.rs.library/core/src/unicode/printable.rs./home/runner/work/platform`

### `programs/jupnet-outbox-program`

- `solana-mainnet-getAccountInfo-OwnerProgramData-jnoUtncG.json` `$.result.value.data[base64]`: `atform-tools/platform-tools/out/rust/library/alloc/src/boxed/convert.rs.src/div/simple.rs.programs/jupnet-outbox-program/src/state.rs.library/core/src/unicode/printable.rs.programs/jupnet-outbox-program/src/ins`

### `programs/gum-omnichain`

- `getAccountInfo-GUMebProgramData-full.json` `$.result.value.data[base64]`: `c/lib.rs.src/div/divide_conquer.rs.src/reduced.rs.src/mul/karatsuba.rs.src/mul/ntt/mod.rs.programs/gum-omnichain/src/state/withdrawal_request.rs.src/mul/simple.rs.src/shift.rs.library/alloc/src/fmt.rs./`
- `jupnet-programdata-GUMebNDC.json` `$.result.value.data[base64]`: `c/lib.rs.src/div/divide_conquer.rs.src/reduced.rs.src/mul/karatsuba.rs.src/mul/ntt/mod.rs.programs/gum-omnichain/src/state/withdrawal_request.rs.src/mul/simple.rs.src/shift.rs.library/alloc/src/fmt.rs./`

### `verifyoutboxmessage`

- `solana-mainnet-bank-tx-5EivNpnD.json` `json-text`: `fyRequest","Program jnoUtncGR9ZCCMixtys6Gzy5coTo6mnmUZuEHRQFTFV invoke [2]","Program log: VerifyOutboxMessage invoked","Program jnoUtncGR9ZCCMixtys6Gzy5coTo6mnmUZuEHRQFTFV consumed 68649 of 97866 com`
- `solana-mainnet-bank-tx-5JQFCWSE.json` `json-text`: `fyRequest","Program jnoUtncGR9ZCCMixtys6Gzy5coTo6mnmUZuEHRQFTFV invoke [2]","Program log: VerifyOutboxMessage invoked","Program jnoUtncGR9ZCCMixtys6Gzy5coTo6mnmUZuEHRQFTFV consumed 71367 of 102084 co`
- `solana-mainnet-getAccountInfo-OwnerProgramData-jnoUtncG.json` `$.result.value.data[base64]`: `ate.UpdateMerkleRoot invokedMerkle proof verifiedVerifying BLS signatureSignature verifiedVerifyOutboxMessage invokedadvance_epoch_root: dropped root of epoch :OUTBOX............ (bytes OUTBOUNDMERKL`
- `solana-mainnet-outbox-history-tx-1mim5qob.json` `json-text`: `"Program jnoUtncGR9ZCCMixtys6Gzy5coTo6mnmUZuEHRQFTFV invoke [2]", "Program log: VerifyOutboxMessage invoked", "Program jnoUtncGR9ZCCMixtys6Gzy5coTo6mnmUZuEHRQFTFV consumed 73996 of`
- `solana-mainnet-outbox-history-tx-39oSPwzK.json` `json-text`: `"Program jnoUtncGR9ZCCMixtys6Gzy5coTo6mnmUZuEHRQFTFV invoke [2]", "Program log: VerifyOutboxMessage invoked", "Program jnoUtncGR9ZCCMixtys6Gzy5coTo6mnmUZuEHRQFTFV consumed 68647 of`
- `solana-mainnet-outbox-history-tx-3AWbovCV.json` `json-text`: `"Program jnoUtncGR9ZCCMixtys6Gzy5coTo6mnmUZuEHRQFTFV invoke [2]", "Program log: VerifyOutboxMessage invoked", "Program jnoUtncGR9ZCCMixtys6Gzy5coTo6mnmUZuEHRQFTFV consumed 68647 of`

### `updatemerkleroot`

- `solana-mainnet-getAccountInfo-GumBankProgramData-full.json` `$.result.value.data[base64]`: `orityInstruction: IdlSetBufferInstruction: EnableBankInstruction: DisableBankInstruction: UpdateMerkleRootStateInstruction: SetMerkleRootStateInstruction: CreateOrAppendRequestBufferInstruction: C`
- `solana-mainnet-getAccountInfo-OwnerProgramData-jnoUtncG.json` `$.result.value.data[base64]`: `ertion failed: src_len <= self.capacity - self.lenInitMerkleRoot invokedmerkle_root_state.UpdateMerkleRoot invokedMerkle proof verifiedVerifying BLS signatureSignature verifiedVerifyOutboxMessage`
- `solana-mainnet-outbox-tx-3Zjq8FZd.json` `json-text`: `"Program jnoUtncGR9ZCCMixtys6Gzy5coTo6mnmUZuEHRQFTFV invoke [1]", "Program log: UpdateMerkleRoot invoked", "Program log: Merkle proof verified", "Program log: Verifying B`

### `merkle proof verified`

- `solana-mainnet-getAccountInfo-GumBankProgramData-full.json` `$.result.value.data[base64]`: `_bank_state.rsprograms/bank/src/instructions/update_merkle_root_state.rsupdate_merkle_rootMerkle proof verifiedMessage hash: programs/bank/src/instructions/withdraw_bank_to_admin.rsprograms/bank/src/in`
- `solana-mainnet-getAccountInfo-OwnerProgramData-jnoUtncG.json` `$.result.value.data[base64]`: `= self.capacity - self.lenInitMerkleRoot invokedmerkle_root_state.UpdateMerkleRoot invokedMerkle proof verifiedVerifying BLS signatureSignature verifiedVerifyOutboxMessage invokedadvance_epoch_root: dr`
- `solana-mainnet-outbox-tx-3Zjq8FZd.json` `json-text`: `QFTFV invoke [1]", "Program log: UpdateMerkleRoot invoked", "Program log: Merkle proof verified", "Program log: Verifying BLS signature", "Program log: Signature verifie`

### `verifying bls signature`

- `solana-mainnet-getAccountInfo-OwnerProgramData-jnoUtncG.json` `$.result.value.data[base64]`: `f.lenInitMerkleRoot invokedmerkle_root_state.UpdateMerkleRoot invokedMerkle proof verifiedVerifying BLS signatureSignature verifiedVerifyOutboxMessage invokedadvance_epoch_root: dropped root of epoch :OU`
- `solana-mainnet-outbox-tx-3Zjq8FZd.json` `json-text`: `eMerkleRoot invoked", "Program log: Merkle proof verified", "Program log: Verifying BLS signature", "Program log: Signature verified", "Program log: advance_epoch_root: dr`

### `signature verified`

- `solana-mainnet-getAccountInfo-GumBankProgramData-full.json` `$.result.value.data[base64]`: `NotFoundTimedOut.Fb.:.{......... (bytes ....q..~..z_> R.Deadlock..~c#.I.invalidate_requestSignature verifiedrequestunique request account data writtencalled `Result::unwrap()` on an `Err` valueprogr`
- `solana-mainnet-getAccountInfo-OwnerProgramData-jnoUtncG.json` `$.result.value.data[base64]`: `okedmerkle_root_state.UpdateMerkleRoot invokedMerkle proof verifiedVerifying BLS signatureSignature verifiedVerifyOutboxMessage invokedadvance_epoch_root: dropped root of epoch :OUTBOX............ (`
- `solana-mainnet-outbox-tx-3Zjq8FZd.json` `json-text`: `le proof verified", "Program log: Verifying BLS signature", "Program log: Signature verified", "Program log: advance_epoch_root: dropped root of epoch 268:", "Program`

## Assessment

- Private runtime dependency terms were visible in public artifacts: `jupnet_bn254, jupnet_crosschain_hash`.
- Public verifier fingerprints remain visible in Gum/Bank/helper binaries and logs, especially BLS/Merkle/outbox strings.
- Security producer terms were either absent or appeared as generic application/staking strings, not as a Dove/JUP stake-weight implementation.
- This supports the current boundary model: public artifacts expose verifier consumption, while the root-builder, Dove set and JUP-weight source remain outside the observed public surface.
