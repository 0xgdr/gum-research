# Gum Omnichain Binary Role Map

## Purpose

This pass compares the two Gum omnichain executables that consume BLS/Merkle verification surfaces, with special focus on the `brhPf...` binary that leaks JupNet-specific BN254 and cross-chain hash symbols.

## Executable Metadata

| Program | Label | Slot | Authority | Exe bytes | Exe SHA256 | Strings | Source paths |
|---|---|---:|---|---:|---|---:|---:|
| `brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1` | `legacy/full Gum omnichain verifier candidate` | 8167938 | `E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9` | 810928 | `4acf794fb915287f0bbefcf013aa706244047da5ba54c6735ef2c6f81ab94400` | 6350 | 58 |
| `GUMebNDCYyF81xjyqaHagbgMQVUTb8fBC9YRh25xSH64` | `recovered outbox sender Gum omnichain` | 106613674 | `7RrBcJS6vbyMdLoYxQUqiUxD3CYVD55FvsGS5L5rfx2x` | 1140464 | `136c7c999694e1e4999f2c71779564c1b001c2d60bc27bd10e692f4bb66f4734` | 1008 | 91 |

## Feature Matrix

| Feature | `brhPfKEx...` | `GUMebNDC...` |
|---|---:|---:|
| `sol_verify_bls_merkle_key` | 2 | 1 |
| `jupnet_alt_bn128_bls` | 6 | 0 |
| `jupnet_bn254` | 4 | 0 |
| `jupnet_crosschain_hash` | 2 | 0 |
| `jupnet_svm` | 0 | 0 |
| `jupnet_vote` | 0 | 0 |
| `jupnet_bls` | 0 | 0 |
| `jupnet_merkle` | 0 | 0 |
| `verify_signature` | 1 | 0 |
| `aggregate` | 0 | 2 |
| `proof_hash` | 1 | 1 |
| `inbox_hash` | 1 | 0 |
| `outbound_hash` | 2 | 1 |
| `root` | 0 | 0 |
| `epoch` | 1 | 1 |
| `chain_config` | 6 | 5 |
| `fee` | 4 | 6 |
| `stake` | 0 | 0 |
| `validator` | 0 | 0 |
| `vote` | 0 | 0 |
| `dove` | 0 | 0 |
| `quorum` | 0 | 0 |
| `weight` | 0 | 0 |
| `signer` | 0 | 4 |
| `slash` | 0 | 0 |
| `reward` | 0 | 0 |

## Source Path Families

| Program | Families | Instruction paths | State paths | Utils paths |
|---|---|---|---|---|
| `brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1` | `other: 39`<br>`instructions: 11`<br>`utils: 4`<br>`state: 3`<br>`lib: 1` | `src/instructions/complete_claim.rs`<br>`src/instructions/complete_swap.rs`<br>`src/instructions/complete_withdrawal.rs`<br>`src/instructions/deposit.rs`<br>`src/instructions/request_swap.rs`<br>`src/instructions/request_withdrawal.rs`<br>`src/instructions/update_chain_config.rs`<br>`src/instructions/account_burned_amount.rs`<br>`src/instructions/initialize.rs`<br>`src/instructions/initialize_deposit_addresses.rs`<br>`src/instructions/register_sui_sweep_account.rs` | `src/state/account/request_swap.rs`<br>`src/state/account/request_withdrawal.rs`<br>`src/state/account/initialize.rs` | `src/utils/address.rs`<br>`src/utils/init_mint_account.rs`<br>`src/utils/initialize_unified_usd_mint.rs`<br>`src/utils/mint.rs` |
| `GUMebNDCYyF81xjyqaHagbgMQVUTb8fBC9YRh25xSH64` | `other: 62`<br>`instructions: 15`<br>`state: 6`<br>`utils: 5`<br>`lib: 2`<br>`events: 1` | `programs/gum-omnichain/src/instructions/authorized/admin/register_unified_mint.rs`<br>`programs/gum-omnichain/src/instructions/authorized/admin/update_managed_mint_metadata.rs`<br>`programs/gum-omnichain/src/instructions/authorized/admin/bind_unified_mint.rs`<br>`programs/gum-omnichain/src/instructions/authorized/admin/unbind_unified_mint.rs`<br>`programs/gum-omnichain/src/instructions/authorized/admin/update_chain_config.rs`<br>`programs/gum-omnichain/src/instructions/authorized/operator/register_bridged_mint.rs`<br>`programs/gum-omnichain/src/instructions/authorized/operator/request_discounted_swap.rs`<br>`programs/gum-omnichain/src/instructions/complete_claim.rs`<br>`programs/gum-omnichain/src/instructions/complete_swap.rs`<br>`programs/gum-omnichain/src/instructions/convert_managed_mint.rs`<br>`programs/gum-omnichain/src/instructions/deposit.rs`<br>`programs/gum-omnichain/src/instructions/request_claim.rs` | `programs/gum-omnichain/src/state/withdrawal_request.rs`<br>`programs/gum-omnichain/src/state/deposit_addresses.rs`<br>`programs/gum-omnichain/src/state/deposit_request.rs`<br>`programs/gum-omnichain/src/state/chain_config.rs`<br>`programs/gum-omnichain/src/state/managed_mint.rs`<br>`programs/gum-omnichain/src/state/swap_request.rs` | `programs/gum-omnichain/src/utils/initialize_bridged_mint.rs`<br>`programs/gum-omnichain/src/utils/fee.rs`<br>`programs/gum-omnichain/src/utils/mint.rs`<br>`programs/gum-omnichain/src/utils/swap.rs`<br>`programs/gum-omnichain/src/utils/verification.rs` |

## Runtime Symbols And Syscalls

| Program | JupNet symbols | Solana/JupNet syscalls | Instruction markers |
|---|---|---|---|
| `brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1` | `jupnet_alt_bn128_bls: 5`<br>`jupnet_program_error: 4`<br>`jupnet_program_pack: 2`<br>`jupnet_target_token_mint: 1`<br>`jupnet_bn254: 1`<br>`jupnet_program: 1`<br>`jupnet_serialize_utils: 1`<br>`jupnet_rent: 1`<br>`jupnet_crosschain_hash: 1`<br>`jupnet_cpi: 1`<br>`jupnet_account_info: 1`<br>`jupnet_epoch_schedule: 1`<br>`jupnet_instruction: 1`<br>`jupnet_pubkey: 1`<br>`jupnet_sha256_hasher: 1`<br>`jupnet_atomic_u64: 1` | `sol_sha256: 2`<br>`sol_invoke_signed_c: 2`<br>`sol_log_: 2`<br>`sol_try_find_program_address: 2`<br>`sol_create_program_address: 2`<br>`sol_alt_bn128_compression: 2`<br>`sol_alt_bn128_group_op: 2`<br>`sol_verify_bls_merkle_key: 2`<br>`sol_keccak256: 2`<br>`sol_log_data: 2`<br>`sol_get_clock_sysvar: 2`<br>`sol_get_rent_sysvar: 2`<br>`sol_dispatch_outbound_hash: 2`<br>`sol_memset_: 2`<br>`sol_memcpy_: 2`<br>`sol_memmove_: 2` | `None` |
| `GUMebNDCYyF81xjyqaHagbgMQVUTb8fBC9YRh25xSH64` | `None` | `sol_log_: 1`<br>`sol_sha256: 1`<br>`sol_alt_bn128_compression: 1`<br>`sol_alt_bn128_group_op: 1`<br>`sol_keccak256: 1`<br>`sol_try_find_program_address: 1`<br>`sol_memcpy_: 1`<br>`sol_verify_bls_merkle_key: 1`<br>`sol_get_clock_sysvar: 1`<br>`sol_get_rent_sysvar: 1`<br>`sol_dispatch_outbound_hash: 1`<br>`sol_invoke_signed_rust: 1`<br>`sol_memset_: 1`<br>`sol_create_program_address: 1`<br>`sol_log_pubkey: 1`<br>`sol_memmove_: 1` | `Instruction: RegisterBridgedMint`<br>`Instruction: IdlCreateAccountanchor` |

## Unique Gum Omnichain Paths

### Only `brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1`

`src/barret.rs`<br>`src/escape.rs`<br>`src/fmt/num.rs`<br>`src/instructions/account_burned_amount.rs`<br>`src/instructions/complete_claim.rs`<br>`src/instructions/complete_swap.rs`<br>`src/instructions/complete_withdrawal.rs`<br>`src/instructions/deposit.rs`<br>`src/instructions/initialize.rs`<br>`src/instructions/initialize_deposit_addresses.rs`<br>`src/instructions/register_sui_sweep_account.rs`<br>`src/instructions/request_swap.rs`<br>`src/instructions/request_withdrawal.rs`<br>`src/instructions/update_chain_config.rs`<br>`src/mint.rs`<br>`src/mul/mod.rs`<br>`src/parse.rs`<br>`src/pubkey.rs`<br>`src/raw_vec.rs`<br>`src/state/account/initialize.rs`<br>`src/state/account/request_swap.rs`<br>`src/state/account/request_withdrawal.rs`<br>`src/unicode/unicode_data.rs`<br>`src/utils.rs`<br>`src/utils/address.rs`<br>`src/utils/init_mint_account.rs`<br>`src/utils/initialize_unified_usd_mint.rs`<br>`src/utils/mint.rs`

### Only `GUMebNDCYyF81xjyqaHagbgMQVUTb8fBC9YRh25xSH64`

`programs/gum-omnichain/src/events.rs`<br>`programs/gum-omnichain/src/instructions/authorized/admin/bind_unified_mint.rs`<br>`programs/gum-omnichain/src/instructions/authorized/admin/register_unified_mint.rs`<br>`programs/gum-omnichain/src/instructions/authorized/admin/unbind_unified_mint.rs`<br>`programs/gum-omnichain/src/instructions/authorized/admin/update_chain_config.rs`<br>`programs/gum-omnichain/src/instructions/authorized/admin/update_managed_mint_metadata.rs`<br>`programs/gum-omnichain/src/instructions/authorized/operator/register_bridged_mint.rs`<br>`programs/gum-omnichain/src/instructions/authorized/operator/request_discounted_swap.rs`<br>`programs/gum-omnichain/src/instructions/complete_claim.rs`<br>`programs/gum-omnichain/src/instructions/complete_swap.rs`<br>`programs/gum-omnichain/src/instructions/convert_managed_mint.rs`<br>`programs/gum-omnichain/src/instructions/deposit.rs`<br>`programs/gum-omnichain/src/instructions/initialize_deposit_addresses.rs`<br>`programs/gum-omnichain/src/instructions/request_claim.rs`<br>`programs/gum-omnichain/src/instructions/request_swap.rs`<br>`programs/gum-omnichain/src/instructions/request_withdrawal.rs`<br>`programs/gum-omnichain/src/lib.rs`<br>`programs/gum-omnichain/src/state/chain_config.rs`<br>`programs/gum-omnichain/src/state/deposit_addresses.rs`<br>`programs/gum-omnichain/src/state/deposit_request.rs`<br>`programs/gum-omnichain/src/state/managed_mint.rs`<br>`programs/gum-omnichain/src/state/swap_request.rs`<br>`programs/gum-omnichain/src/state/withdrawal_request.rs`<br>`programs/gum-omnichain/src/utils/fee.rs`<br>`programs/gum-omnichain/src/utils/initialize_bridged_mint.rs`<br>`programs/gum-omnichain/src/utils/mint.rs`<br>`programs/gum-omnichain/src/utils/swap.rs`<br>`programs/gum-omnichain/src/utils/verification.rs`<br>`src/action.rs`<br>`src/barrett.rs`<br>`src/bpf_writer.rs`<br>`src/clone.rs`<br>`src/collections/btree/navigate.rs`<br>`src/common.rs`<br>`src/extension/mod.rs`<br>`src/inbox.rs`<br>`src/internal.rs`<br>`src/io/mod.rs`<br>`src/iter/traits/accum.rs`<br>`src/iter/traits/iterator.rs`

## High-Value Contexts

### `sol_verify_bls_merkle_key`

- `brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1`: `ol_try_find_program_address.sol_create_program_address.abort.sol_alt_bn128_compression.sol_alt_bn128_group_op.sol_verify_bls_merkle_key.sol_keccak256.sol_log_data.sol_get_clock_sysvar.sol_get_rent_sysvar.sol_dispatch_outbound_hash.sol_memset_.so`<br>`erHex$u20$for$u20$u64$GT$3fmt17hdc601a14ed977194E._ZN4core9panicking19assert_failed_inner17hc8b328755bf6e166E.sol_verify_bls_merkle_key.sol_keccak256.sol_log_data.sol_get_clock_sysvar.sol_get_rent_sysvar._ZN4core3fmt9Formatter12debug_struct17h94`
- `GUMebNDCYyF81xjyqaHagbgMQVUTb8fBC9YRh25xSH64`: `ha256.sol_alt_bn128_compression.sol_alt_bn128_group_op.sol_keccak256.sol_try_find_program_address.sol_memcpy_.sol_verify_bls_merkle_key.sol_get_clock_sysvar.sol_get_rent_sysvar.sol_dispatch_outbound_hash.sol_invoke_signed_rust.sol_memset_.sol_cr`

### `jupnet_alt_bn128_bls`

- `brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1`: `LT$S$GT$6unpack17he82adcd1e95ef7c7E.LBB4_2.LBB4_3.LBB4_14.LBB4_15.LBB4_11.LBB4_6.LBB4_12.LBB4_10.LBB4_13._ZN20jupnet_alt_bn128_bls8g2_point7G2Point16verify_signature17he7f0aeba795deafbE.LBB5_4.LBB5_6.LBB5_22.LBB5_8.LBB5_15.LBB5_10.LBB5_12.L`<br>`BB13_63.LBB13_65.LBB13_67.LBB13_69..L__unnamed_36..L__unnamed_40..L__unnamed_42..L__unnamed_43..L__unnamed_47.jupnet_alt_bn128_bls.1fda9e82f93c5a14-cgu.0.LBB0_2.LBB0_3.LBB8_2.LBB8_3.jupnet_bn254.20303437e8480312-cgu.0.LBB4_2.LBB4_3.LBB6_2.L`<br>`ken_2022..state..Account$u20$as$u20$jupnet_program_pack..Pack$GT$17unpack_from_slice17h730db0924c1d2403E._ZN20jupnet_alt_bn128_bls9constants7MODULUS17hd80f9abebdae7623E._ZN9dashu_int3cmp12cmp_in_place17h711ebe649cd5f633E._ZN63_$LT$dashu_int`<br>`sha256._ZN9dashu_int7convert39_$LT$impl$u20$dashu_int..repr..Repr$GT$13from_be_bytes17h8668f505e85fc5b2E._ZN20jupnet_alt_bn128_bls7schemes17sha256_normalized17NORMALIZE_MODULUS17h881e59f175cca333E._ZN121_$LT$jupnet_alt_bn128_bls..g1_point..`

### `jupnet_bn254`

- `brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1`: `amed_42..L__unnamed_43..L__unnamed_47.jupnet_alt_bn128_bls.1fda9e82f93c5a14-cgu.0.LBB0_2.LBB0_3.LBB8_2.LBB8_3.jupnet_bn254.20303437e8480312-cgu.0.LBB4_2.LBB4_3.LBB6_2.LBB6_3.LBB10_4.LBB10_3.jupnet_program.db3e8d18072e4750-cgu.0.LBB1`<br>`3E._ZN4core5slice29_$LT$impl$u20$$u5b$T$u5d$$GT$15copy_from_slice17len_mismatch_fail17h99a18f7a481ed80cE._ZN12jupnet_bn25411compression11target_arch23alt_bn128_g1_decompress17h0a587d2fd479188cE._ZN9dashu_int4repr4Repr11from_buffer17`<br>`sedPoint$u20$as$u20$jupnet_alt_bn128_bls..schemes..traits..BLSSignature$GT$8to_bytes17ha596896296d6c64dE._ZN12jupnet_bn25411target_arch17alt_bn128_pairing17h3dedef49273ea399E._ZN79_$LT$hex..BytesToHexChars$u20$as$u20$core..iter..tra`<br>`1ec62114643631E.__divdi3.__ashlti3.__lshrti3.__adddf3._ZN4core6option13expect_failed17h7e4de16c9a498fceE._ZN12jupnet_bn25411compression11target_arch23alt_bn128_g2_decompress17haaa94e9f9579a872E.sol_alt_bn128_compression.sol_alt_bn12`

### `jupnet_crosschain_hash`

- `brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1`: `lake3.7c2a17b7fc91c27d-cgu.0.jupnet_serialize_utils.3494eb35fefd573e-cgu.0.jupnet_rent.5752aa8b34e6f920-cgu.0.jupnet_crosschain_hash.bfffe4da37cf68a5-cgu.0.log.d6e5e5d0f7cecb40-cgu.0.jupnet_cpi.81cb33522d75a01a-cgu.0.jupnet_account_info.f314a`<br>`N13gum_omnichain5state7account13request_claim20RequestClaimAccounts15verify_and_load17h44094d56b99a8503E._ZN22jupnet_crosschain_hash24dispatch_crosschain_hash17h712bd4dca0ac7c3cE._ZN13gum_omnichain12instructions12request_swap11RequestSwap20pr`

### `verify_signature`

- `brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1`: `4_2.LBB4_3.LBB4_14.LBB4_15.LBB4_11.LBB4_6.LBB4_12.LBB4_10.LBB4_13._ZN20jupnet_alt_bn128_bls8g2_point7G2Point16verify_signature17he7f0aeba795deafbE.LBB5_4.LBB5_6.LBB5_22.LBB5_8.LBB5_15.LBB5_10.LBB5_12.LBB5_14.LBB5_2.LBB5_23.LBB5_17.LBB5_`

### `aggregate`

- `GUMebNDCYyF81xjyqaHagbgMQVUTb8fBC9YRh25xSH64`: `n id does not match the chain id stored on the requestChain extra payload does not match the supplied chain idAggregate BLS public key failed merkle key validation or G2 decodingAggregate BLS signature verification failedmin_fina`<br>`yload does not match the supplied chain idAggregate BLS public key failed merkle key validation or G2 decodingAggregate BLS signature verification failedmin_finality_threshold must be FINALITY_THRESHOLD_CONFIRMED or FINALITY_THRE`

### `proof_hash`

- `brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1`: `ckdeadlockamount: operator__inbox_event_authgum-omnichain/src/instructions/complete_claim.rsinbox_hash INBOUNDproof_hash target_token_address: swap_data.chain_id: jupnet_target_token_mint: complete_claim_account.mint.key(): Invali`
- `GUMebNDCYyF81xjyqaHagbgMQVUTb8fBC9YRh25xSH64`: `hain/src/instructions/convert_managed_mint.rsprograms/gum-omnichain/src/instructions/deposit.rsdeposit: noop, proof_hash already processedChainConfig has an unrecognized chain_id ... account was not initialized via update_chain_co`

### `inbox_hash`

- `brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1`: `tes withdrewDeadlockdeadlockamount: operator__inbox_event_authgum-omnichain/src/instructions/complete_claim.rsinbox_hash INBOUNDproof_hash target_token_address: swap_data.chain_id: jupnet_target_token_mint: complete_claim_account.`

### `outbound_hash`

- `brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1`: `op.sol_verify_bls_merkle_key.sol_keccak256.sol_log_data.sol_get_clock_sysvar.sol_get_rent_sysvar.sol_dispatch_outbound_hash.sol_memset_.sol_memcpy_.sol_memmove_.sol_memcmp_.............................................................`<br>`ugStruct5field17h0a26c85d244f0399E._ZN4core3fmt8builders11DebugStruct6finish17h06042bf63596cf75E.sol_dispatch_outbound_hash.sol_memset_._ZN60_$LT$std..io..error..Error$u20$as$u20$core..fmt..Display$GT$3fmt17h3844085053c5a93dE._ZN66_$`
- `GUMebNDCYyF81xjyqaHagbgMQVUTb8fBC9YRh25xSH64`: `d_program_address.sol_memcpy_.sol_verify_bls_merkle_key.sol_get_clock_sysvar.sol_get_rent_sysvar.sol_dispatch_outbound_hash.sol_invoke_signed_rust.sol_memset_.sol_create_program_address.sol_log_pubkey.sol_memmove_.sol_memcmp_........`

### `epoch`

- `brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1`: `et_cpi.81cb33522d75a01a-cgu.0.jupnet_account_info.f314a31ea0384b65-cgu.0.keccak.28945af00f0457d2-cgu.0.jupnet_epoch_schedule.4dc1f98b63052dc0-cgu.0.jupnet_program_error.49c24c6fe2651ffe-cgu.0.LBB5_5.LBB5_4.jupnet_instruction.`
- `GUMebNDCYyF81xjyqaHagbgMQVUTb8fBC9YRh25xSH64`: `.........\... .e>...Instruction: RegisterBridgedMint..U*$L.... ..'rL...M.w...{.A...}dispatching invalidate in epoch G./... <..qh.j..]X...EP.).1.rNd0A signer constraint was violatedInstruction: RegisterUnifiedMintassertion fai`

### `chain_config`

- `brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1`: `accountsgum-omnichain/src/instructions/request_withdrawal.rsfee_amount: gum-omnichain/src/instructions/update_chain_config.rsgum-omnichain/src/instructions/account_burned_amount.rsAdding chain metadata - verify & load startAdding ch`<br>`ied and loadedVerifying swap_request PDAVerifying input_unified_mint_map PDAVerifying input_mint PDAVerifying chain_config PDAgum-omnichain/src/state/account/request_swap.rsPassed unified mint map PDA checkPassed withdrawal request`<br>`0_6.LBB140_18.LBB140_9.LBB140_11.LBB140_13.LBB140_15.LBB140_17._ZN112_$LT$gum_omnichain..instructions..update_chain_config..ChainExtraArgs$u20$as$u20$borsh..de..BorshDeserialize$GT$18deserialize_reader17hea27d876b4e85c67E.LBB141_19.`<br>`t..Display$u20$for$u20$ethnum..uint..U256$GT$3fmt17h03786988159342feE._ZN13gum_omnichain12instructions18reset_chain_config16ResetChainConfig26process_reset_chain_config17h42534c6627f74fa7E._ZN13gum_omnichain5state7account18reset_cha`
- `GUMebNDCYyF81xjyqaHagbgMQVUTb8fBC9YRh25xSH64`: `-omnichain/src/instructions/authorized/admin/update_managed_mint_metadata.rs.programs/gum-omnichain/src/state/chain_config.rs.src/primitive.rs.src/mul/ntt/crt.rs./home/runner/work/platform-tools/platform-tools/out/rust/library/core/`<br>`horized/admin/unbind_unified_mint.rsunified-toprograms/gum-omnichain/src/instructions/authorized/admin/update_chain_config.rschain-programs/gum-omnichain/src/instructions/authorized/admin/update_managed_mint_metadata.rsprograms/gum-`<br>`oof_hash already processedChainConfig has an unrecognized chain_id ... account was not initialized via update_chain_configrequest_claim msg_hash programs/gum-omnichain/src/instructions/request_claim.rsprograms/gum-omnichain/src/inst`<br>`/request_swap.rsprograms/gum-omnichain/src/instructions/request_withdrawal.rsprograms/gum-omnichain/src/state/chain_config.rsprograms/gum-omnichain/src/state/managed_mint.rsprograms/gum-omnichain/src/utils/fee.rs.......programs/gum-`

### `fee`

- `brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1`: `0Processing request withdrawalVerified and loaded accountsgum-omnichain/src/instructions/request_withdrawal.rsfee_amount: gum-omnichain/src/instructions/update_chain_config.rsgum-omnichain/src/instructions/account_burned_am`<br>`t15mint_via_minter17hb202bde639dd8258E._ZN13gum_omnichain12instructions13complete_swap12CompleteSwap18compute_fee_amount17h0d3e5cfedb318d42E._ZN13gum_omnichain12instructions21account_burned_amount19AccountBurnedAmount18dedu`<br>`ain5utils7address14decode_address17h401f962ffb635a55E._ZN13gum_omnichain12instructions12request_swap18compute_fee_amount17hd50b59bd07d40dbbE._ZN6ethnum4uint4U25612from_str_hex17haf96754421910999E._ZN13gum_omnichain12instruc`<br>`._ZN6ethnum4uint3fmt67_$LT$impl$u20$core..fmt..Display$u20$for$u20$ethnum..uint..U256$GT$3fmt17h03786988159342feE._ZN13gum_omnichain12instructions18reset_chain_config16ResetChainConfig26process_reset_chain_config17h42534c66`
- `GUMebNDCYyF81xjyqaHagbgMQVUTb8fBC9YRh25xSH64`: `nfidentialTransfersDisabledInvalid Option representation: . The first byte must be 0 or 1UninitializedTransferFeeConfigTransferFeeAmountMintCloseAuthorityConfidentialTransferMintConfidentialTransferAccountDefaultAccountStat`<br>`rsDisabledInvalid Option representation: . The first byte must be 0 or 1UninitializedTransferFeeConfigTransferFeeAmountMintCloseAuthorityConfidentialTransferMintConfidentialTransferAccountDefaultAccountStateImmutableOwnerMe`<br>`.>..operatorCpiGuardPermanentDelegateNonTransferableAccountTransferHookTransferHookAccountConfidentialTransferFeeConfigConfidentialTransferFeeAmountMetadataPointerTokenMetadataGroupPointerTokenGroupGroupMemberPointer....Con`<br>`DelegateNonTransferableAccountTransferHookTransferHookAccountConfidentialTransferFeeConfigConfidentialTransferFeeAmountMetadataPointerTokenMetadataGroupPointerTokenGroupGroupMemberPointer....ConstraintHasOneConstraintSigner`

### `signer`

- `GUMebNDCYyF81xjyqaHagbgMQVUTb8fBC9YRh25xSH64`: `rBridgedMint..U*$L.... ..'rL...M.w...{.A...}dispatching invalidate in epoch G./... <..qh.j..]X...EP.).1.rNd0A signer constraint was violatedInstruction: RegisterUnifiedMintassertion failed: out.len() >= nAn owner constraint wa`<br>`ferFeeAmountMetadataPointerTokenMetadataGroupPointerTokenGroupGroupMemberPointer....ConstraintHasOneConstraintSignerconnection resetassertion `left ) when slicing `DerivedObjectKeyentity not foundhost unreachableinvalid filena`<br>`tKeyentity not foundhost unreachableinvalid filenamerange end index . Error Number: ................AccountNotSignerUnsupportedChainPermissionDeniedoutbox msg_hash BridgedNotLinkedTokenGroupMemberno storage spaceFeeOwnerMismat`<br>`harge_out fee math but not availablepayerunified_mintbridged_minttoken_programsystem_program.not implemented: signerchain_configadminrent_payerwithholdinguser_tokenevent_authorityprogramoutput_native_mintinput_native_mintfee_m`

## Assessment

- `brhPf...` is the richer/full Gum omnichain verifier candidate: it contains `jupnet_bn254`, `jupnet_crosschain_hash`, `jupnet_alt_bn128_bls`, `verify_signature`, `proof_hash`, `inbox_hash`, Gum instruction/state paths and `sol_verify_bls_merkle_key`.
- `GUMeb...` is the recovered sender/program id from verifier payloads. It contains Gum omnichain state/instruction paths and `sol_verify_bls_merkle_key`, but did not expose the same private BN254/cross-chain hash crate symbols in this snapshot.
- Producer/security terms in `brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1`: `None`
- Producer/security terms in `GUMebNDCYyF81xjyqaHagbgMQVUTb8fBC9YRh25xSH64`: `None`
- The comparison clarifies the public application/verifier split, but still does not expose a Dove registry, JUP stake-weight table, quorum calculation or root-builder implementation.
