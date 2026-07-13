# JupNet Executable Census

## Scope

- Snapshot: `evidence/2026-07-12-bank-live-rpc`
- Upgradeable executables analyzed: `23`
- Executables with source paths: `22`
- Executables with high-value security term hits: `5`
- Executables with canonical JUP / validator / vote / stake key hits: `0`
- Executables with `sol_verify_bls_merkle_key`: `2`

## Program Families

| Label | Count |
|---|---:|
| `src/pubkey.rs` | 5 |
| `gum-omnichain` | 3 |
| `src/de/mod.rs` | 2 |
| `jtx` | 2 |
| `src/pubkey.rssrc/de/mod.rs` | 2 |
| `src/token_account.rssrc/mint.rs` | 1 |
| `poker-staking` | 1 |
| `src/sysvar/mod.rs` | 1 |
| `src/string.rssrc/de/mod.rs` | 1 |
| `verifier` | 1 |
| `jtx-oracle` | 1 |
| `src/extension/mod.rs` | 1 |
| `src/raw_vec.rs` | 1 |
| `unlabeled` | 1 |

## Upgrade Authorities

| Upgrade authority | Program count |
|---|---:|
| `6DeGq3woXEK2tj9L8Zxc8vYP9ZvKgkuMkmqdZu35yJRF` | 6 |
| `ac5p9DKWSSZiF3en6VrNA1PfcsMjqjx3FWyMqq8s2oB` | 3 |
| `DVGrECNZgUJoeByis3jPR7ta2iHuRD8WnWa2Bmco7C9c` | 3 |
| `BssAxGv8zAoYkTb459m9fUitH1cHZdZXtPCsLdE71R1r` | 2 |
| `GK77eaTmYeEkFvqVXYYybmfDhzXSK1i7tnxtKF8btQPc` | 2 |
| `pokxBYD7NN7esG7MYycJjPkTkQYY1RmGb1kpDDeVLKc` | 1 |
| `E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9` | 1 |
| `67wipeYHcBA97pfkfNRPdYasxLfZHwYVkLr5mAVeGFf8` | 1 |
| `4mt4vDw3YMzD5ZUvQHmvKVLjAPoje2GoHZBAsmrZYZBj` | 1 |
| `7P2Jw9iN2iqE2QXxdSnaGoh7Qj7ib5gLRGkaWwgaVbuf` | 1 |
| `7RrBcJS6vbyMdLoYxQUqiUxD3CYVD55FvsGS5L5rfx2x` | 1 |
| `None` | 1 |

## Program Rows

| Program | Label | ProgramData | Slot | Authority | Exe bytes | Exe SHA256 | Source paths | Key hits | High-value hits |
|---|---|---|---:|---|---:|---|---|---|---|
| `JupnetUser111111111111111111111111111111111` | `src/de/mod.rs` | `3brU5Pg72UVjZWvB4NdQJGRQiSLfi6GQ7v2HqU9SPFCx` | 0 | `ac5p9DKWSSZiF3en6VrNA1PfcsMjqjx3FWyMqq8s2oB` | 153344 | `9c48dd0e70c40e86f845cc5945c6ee361b9888a576b712059f22f469f29caa7e` | `src/de/mod.rs`<br>`src/iter/traits/iterator.rs/home/runner/work/platform-tools/platform-tools/out/rust/library/core/src/slice/sort/stable/quicksort.rs`<br>`src/slice.rs`<br>`src/collections/btree/node.rs/home/runner/work/platform-tools/platform-tools/out/rust/library/alloc/src/collections/btree/navigate.rs` | `None` | `None` |
| `Jupnetopen1DRegistry11111111111111111111111` | `src/de/mod.rs` | `E2guMYDzcBgpLqWHebw3DaJWGKJDBpZp17gaQqtV36KL` | 76538464 | `ac5p9DKWSSZiF3en6VrNA1PfcsMjqjx3FWyMqq8s2oB` | 136024 | `0e997c179fe8aa70d358e44c94c1ef06e169018f7443acb77d5b95f4152a29cb` | `src/de/mod.rs`<br>`src/string.rs`<br>`src/processor.rsprogram/openid-registry/src/utils.rs`<br>`src/lib.rs` | `None` | `None` |
| `MagiCFLC56sJYawfhuJQhfveDfQY96AjUft2sk3TssA` | `src/token_account.rssrc/mint.rs` | `C2eUfWuyT3S3tSKhyaJKDQ2pbtAnzHE4op6isk2CYgCf` | 5960226 | `BssAxGv8zAoYkTb459m9fUitH1cHZdZXtPCsLdE71R1r` | 94448 | `f1f22532d5877dcd427287783991ba99b263d55bcf48b104c8089e3d6e94b0c5` | `src/token_account.rssrc/mint.rs`<br>`src/instructions/claim.rssrc/instructions/clawback.rssrc/instructions/expire.rs`<br>`src/pubkey.rs`<br>`src/state.rssrc/lib.rs` | `None` | `None` |
| `PoKERjpvXZBFhLF1zQUNxCFUszYBNHAvBCXX6UKXpT6` | `poker-staking` | `9EBhYAxrhd79xb8EqoMnD7tcBGtWExA8TWoKqbXVhBzM` | 61412713 | `pokxBYD7NN7esG7MYycJjPkTkQYY1RmGb1kpDDeVLKc` | 222808 | `3f275408c58703188428e934676cfb29b5b6dc2a80b879f80d3fe38023499b9b` | `src/math.rs`<br>`src/int/ops.rssrc/uint/ops.rs`<br>`src/internal.rs/home/runner/work/platform-tools/platform-tools/out/rust/library/core/src/slice/iter.rssrc/entrypoint/mod.rssrc/sysvars/rent.rs`<br>`programs/poker-staking/src/instructions/player_claim_winnings.rs` | `None` | `stake: 2` |
| `Tokenis9xgQh7yMRbNBnV6uFq7LANbuZJwebxWBWixf` | `src/sysvar/mod.rs` | `2uYJvtVYZ7JGJdsyhFZdDHyDSCfuakgHYAPEGZyVp8tk` | 0 | `ac5p9DKWSSZiF3en6VrNA1PfcsMjqjx3FWyMqq8s2oB` | 470216 | `5e734f26a0d66143e7dc6b6b2595557b1c44ce8d45153cf0c3f7b46653e3a6e5` | `src/sysvar/mod.rs`<br>`src/string.rs`<br>`src/str/pattern.rs`<br>`src/extension/cpi_guard/processor.rs` | `None` | `jup: 3` |
| `brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1` | `gum-omnichain` | `BW7ncAFAX1jjhZU6X5AS8JrkAqr8njfUNQxkuPtUQXjv` | 8167938 | `E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9` | 810928 | `4acf794fb915287f0bbefcf013aa706244047da5ba54c6735ef2c6f81ab94400` | `src/slice/iter.rs`<br>`src/schemes/sha256_normalized.rs`<br>`src/pubkey.rs`<br>`src/mint.rsshared-lib/src/utils.rs` | `None` | `jup: 8`<br>`sol_verify_bls_merkle_key: 2` |
| `jtxQHH3ysuWRETjaynai3jowPztq2LBJApVFcEv4Wmg` | `jtx` | `AQTRmjfy8C4MCdiL5ANSVvoJKP61cvewacqWN5ZNDKMR` | 106610202 | `DVGrECNZgUJoeByis3jPR7ta2iHuRD8WnWa2Bmco7C9c` | 1435288 | `59b685690a04c003f2c1dfb562f2e2c31b4eb10d34d1ecb1694aa3e0fdcb1471` | `programs/jtx/src/state/trading_account/open_orders.rs`<br>`src/lib.rs`<br>`programs/jtx/src/processor/cancel_order.rs`<br>`programs/jtx/src/processor/place_order.rs` | `None` | `None` |
| `morcJ52h6fKAEm4KdLvDFYzC67Fou8YyZBvURjBVUts` | `src/string.rssrc/de/mod.rs` | `5SoPuxu6KhvaCyV352fQLDLAP7NrVqETASaYtjvapSZL` | 15219852 | `GK77eaTmYeEkFvqVXYYybmfDhzXSK1i7tnxtKF8btQPc` | 50768 | `6215c525b6b57d136a241bc1a3139a6c66a1541a16bbd95d5fed3c5a35a6f14f` | `src/string.rssrc/de/mod.rs`<br>`src/pubkey.rsprograms/mock-oracle/src/processor.rs`<br>`src/raw_vec.rslibrary/core/src/fmt/mod.rs`<br>`src/fmt/num.rs` | `None` | `None` |
| `udpZn12nNpW1LyEjDSdjXtH4quYqbJinFWBHDrRVDRp` | `gum-omnichain` | `8VMfvubChGyXyf1pBBxVfjssHK76fdzcJ7cJB9eMRWag` | 97651144 | `67wipeYHcBA97pfkfNRPdYasxLfZHwYVkLr5mAVeGFf8` | 126776 | `e78753887d5340c0d4682082b1575d5f0d0c648fe3b87b83399c901602fa8526` | `src/fmt.rs`<br>`src/pubkey.rs`<br>`src/string.rs`<br>`src/raw_vec/mod.rs` | `None` | `None` |
| `2ZisfjpHB1sjvhPLMBuAjegRY1hiakqenw1BwrBN1MhQ` | `src/pubkey.rssrc/de/mod.rs` | `F3cnRt5iGAjhrMG4PEKFyDBsU5oBahYqgTBAmV3Fqx5p` | 50334402 | `4mt4vDw3YMzD5ZUvQHmvKVLjAPoje2GoHZBAsmrZYZBj` | 112080 | `0c55171e0182a24cf672e2cf74b6182fb006ffad3fc22ce8f752536ca41b155b` | `src/pubkey.rssrc/de/mod.rs`<br>`src/state/account/mint_checks.rs`<br>`src/state.rs`<br>`src/raw_vec.rs` | `None` | `None` |
| `3UmdTSD7SYocc1FCvjAfxYsLAvMVFU8BFQQmhjrW1Z9d` | `src/pubkey.rs` | `AsQk1DvPS8oFpQVHS3Y52iUENKdWLctcSM196nTtyr7d` | 44543890 | `6DeGq3woXEK2tj9L8Zxc8vYP9ZvKgkuMkmqdZu35yJRF` | 118656 | `e169554b4f6e0ea3105dc3de0410ab1b7ac5c5cec931360da658780d3562dbdc` | `src/pubkey.rs`<br>`src/mint.rs`<br>`src/state/account/mint_checks.rs`<br>`src/state.rs` | `None` | `None` |
| `5C5ZEsDUKUH5dwHyzDtdEb7bcviYoqB4rBf9rkLj5AKm` | `src/pubkey.rs` | `EK64n7pPGRxbxsRduCQwLefibTwqHwePXN8JSUy7Frkj` | 10030291 | `6DeGq3woXEK2tj9L8Zxc8vYP9ZvKgkuMkmqdZu35yJRF` | 116064 | `c664ea3c08e4a0471ce9f3b49cddc33e54af9f493386a45cb0e0aa910c85d34f` | `src/pubkey.rs`<br>`src/mint.rs`<br>`src/state/account/mint_checks.rs`<br>`src/state.rs` | `None` | `None` |
| `5JX82h3HJSamWJVC6Zg2iSPSFwhpZj9h3KBXQPPuDwVn` | `src/pubkey.rs` | `AHpmurTZENhZ4Lk8NooL9yGm8Q9pnkoYziHpvSseLzBH` | 9562815 | `6DeGq3woXEK2tj9L8Zxc8vYP9ZvKgkuMkmqdZu35yJRF` | 116064 | `1e299face5c500341062d3e5eb27958684bea30d0e4baf36fb7faf2611c59105` | `src/pubkey.rs`<br>`src/mint.rs`<br>`src/state/account/mint_checks.rs`<br>`src/state.rs` | `None` | `None` |
| `5p9pJmtfFt6wkceFJHF4Q1uaQA7Venc5knFq2zeDT7kd` | `src/pubkey.rssrc/de/mod.rs` | `HzxAJKJMc8M12z8yPvUcKEZUYvWQ5PPBB2hebbqh1ieF` | 48386458 | `6DeGq3woXEK2tj9L8Zxc8vYP9ZvKgkuMkmqdZu35yJRF` | 110120 | `b11ef536488a899e23904289c20692f1f3a5da7305903cd5ef196edaa4a5a14b` | `src/pubkey.rssrc/de/mod.rs`<br>`src/state/account/mint_checks.rs`<br>`src/state.rs`<br>`src/raw_vec.rs` | `None` | `None` |
| `7KhNwmEmfhBjQwnD6QTi5ek8jFZ8WrP8KMYWmPQgYUn9` | `verifier` | `D3ZjC6F3z1s3Fk88MzvuUM37hkYBnKQ9srwCFHekcq7a` | 86581887 | `DVGrECNZgUJoeByis3jPR7ta2iHuRD8WnWa2Bmco7C9c` | 389024 | `05414985b4d538e37fc08ade90484faf2e5dc2c4de14e907fe408acdddd141a3` | `src/accounts/account_loader.rs`<br>`src/fmt/mod.rs`<br>`src/accounts/program.rssrc/de/mod.rs`<br>`src/string.rs/Users/dmitri/work/git/platform-tools/out/rust/library/core/src/num/mod.rs/Users/dmitri/work/git/platform-tools/out/rust/library/core/src/slice/sort.rs` | `None` | `None` |
| `8SJbxjZWNTTQtWnoqpRGCY2xLRZ4N97Qs7hWHjGhZEQg` | `jtx-oracle` | `8QD2QMLiwao6xRwgAo2DrMdFhRxENGzJ15p7inK17QKU` | 103699028 | `DVGrECNZgUJoeByis3jPR7ta2iHuRD8WnWa2Bmco7C9c` | 152872 | `9714b6649021e888ecf4f1632c82f349f6e31bc4f6b30b2a3c0a66f6e8c03cb0` | `src/biguint/division.rs`<br>`src/biguint/shift.rs`<br>`src/pubkey.rs`<br>`src/biguint/addition.rs` | `None` | `None` |
| `9QUEKQy6LKCUSqmkiiwSkxKALDfhAX5JYx3Uvh7jztJe` | `src/extension/mod.rs` | `HsVq7GMPgMHQ6HkpuJngVd52PXUVbyLVnTSUnkAvP2ma` | 15204985 | `BssAxGv8zAoYkTb459m9fUitH1cHZdZXtPCsLdE71R1r` | 299872 | `8c3283b5cf5e25191f8145626b01c19f31b50ca9883b4f3bebf6b1b5e8c17cbe` | `src/extension/mod.rs`<br>`src/de/mod.rs`<br>`src/slice/sort/stable/quicksort.rs/Users/runner/work/platform-tools/platform-tools/out/rust/library/alloc/src/slice.rs/Users/runner/work/platform-tools/platform-tools/out/rust/library/alloc/src/raw_vec.rs`<br>`src/pubkey.rs` | `None` | `vote: 1` |
| `CFDH8vii4NSDFPX7cRGp1urkjZM4yqUxHYY29wZkvxzU` | `src/pubkey.rs` | `BJgMaqksJNi5W9uVVrJ6u77gz4rrFoyZgjix94m9NLZe` | 14070279 | `6DeGq3woXEK2tj9L8Zxc8vYP9ZvKgkuMkmqdZu35yJRF` | 117768 | `58597ba3125ae88be1bbb5d6601553a4123eb003fdfa25797991585d40887a89` | `src/pubkey.rs`<br>`src/mint.rs`<br>`src/state/account/mint_checks.rs`<br>`src/state.rs` | `None` | `None` |
| `DDXSif7Ya4FC4f4cFYpdGW3UGpghpbbSdrXJJ3ZzhotQ` | `jtx` | `8DTiBJzTWABGGv9BodEsQD23aHBkuRapN3XXrLQ3FMvr` | 86554369 | `GK77eaTmYeEkFvqVXYYybmfDhzXSK1i7tnxtKF8btQPc` | 572752 | `02f61ae76ea2a04a487f5f3df9043f5548563013359afafd92c770e43cde6405` | `src/logger.rssrc/de/mod.rs`<br>`programs/jtx/src/state/oracle.rs`<br>`programs/jtx/src/state/market.rs`<br>`src/string.rs` | `None` | `None` |
| `E6Eh5HML9pA6ACKaRf2cn9NbgRcJniAJbipjJiJPPHqf` | `src/pubkey.rs` | `i3LVfrrRVCLn7uprXMnAyAfeAmfeXmBR1Mzpk93bDqc` | 6231863 | `6DeGq3woXEK2tj9L8Zxc8vYP9ZvKgkuMkmqdZu35yJRF` | 111848 | `61026c56bcd9d7d2f7a687ba3d2ffb16134b7228061a855c4145fda755a81135` | `src/pubkey.rs`<br>`src/mint.rs`<br>`src/state/account/mint_checks.rs`<br>`src/state.rs` | `None` | `None` |
| `E9M2DUEDdzvUQyxYDbZL9pijdXSavWYYPam4vvXchBR7` | `src/raw_vec.rs` | `4EbiMXj6yGtzH2a3BKnBqTT6i1tdBa5tooENDZX8bAbd` | 5913312 | `7P2Jw9iN2iqE2QXxdSnaGoh7Qj7ib5gLRGkaWwgaVbuf` | 72520 | `d74df72c2db1ed859c54011bdad1ea2ab1350a87281dc59b7890aeb223469aa4` | `src/raw_vec.rs`<br>`src/fmt.rs` | `None` | `None` |
| `GUMebNDCYyF81xjyqaHagbgMQVUTb8fBC9YRh25xSH64` | `gum-omnichain` | `Gi8HgbHnykRiHboqG2VHysti773o8bNSjuFJWpyf4Q89` | 106613674 | `7RrBcJS6vbyMdLoYxQUqiUxD3CYVD55FvsGS5L5rfx2x` | 1140464 | `136c7c999694e1e4999f2c71779564c1b001c2d60bc27bd10e692f4bb66f4734` | `src/lib.rs`<br>`src/div/divide_conquer.rs`<br>`src/reduced.rs`<br>`src/mul/karatsuba.rs` | `None` | `jup: 1`<br>`sol_verify_bls_merkle_key: 1` |
| `GZFttP3CHkK3ujbA1edDhB7wP4Nm9jQMyiJiynhoYqKF` | `` | `J7pApEuvze2YGYU1KmFFqQt8heyNati5H3ikykq5KC68` | None | `None` | 0 | `None` | `None` | `None` | `None` |

## Verifier Syscall Candidates

| Program | Label | Evidence |
|---|---|---|
| `brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1` | `gum-omnichain` | `sol_verify_bls_merkle_key`<br>`sol_verify_bls_merkle_key`<br>`sol_verify_bls_merkle_key`<br>`sol_verify_bls_merkle_key` |
| `GUMebNDCYyF81xjyqaHagbgMQVUTb8fBC9YRh25xSH64` | `gum-omnichain` | `sol_verify_bls_merkle_key`<br>`sol_verify_bls_merkle_key`<br>`sol_verify_bls_merkle_key` |

## High-Value Term Examples

### `PoKERjpvXZBFhLF1zQUNxCFUszYBNHAvBCXX6UKXpT6` `poker-staking`

- `stake`: `Uhindex out of bounds: the len is Instruction: StakerClaimWinnings`<br>`UInstruction: ClaimAllFundsraiseInstruction: ClaimPlatformFeesInstruction: CreatePlatformFeeAccountInstruction: ExtendRaiseInstruction: InitializeNoDepositRaiseInstruction: InitializePokerRaiseInstruction: PlayerClaimPre`

### `Tokenis9xgQh7yMRbNBnV6uFq7LANbuZJwebxWBWixf` `src/sysvar/mod.rs`

- `jup`: `PermissionDeniedno storage spaceAddrNotAvailable right` failed: 0123456789abcdefError: IncorrectAuthorityError: ConfidentialTransfersDisabledError: Lamport balance below rent-exempt thresholdError: insufficient fundsErro`<br>`Instruction: InitializeMintInstruction: InitializeAccountInstruction: InitializeMultisigInstruction: TransferInstruction: ApproveInstruction: RevokeInstruction: SetAuthorityInstruction: MintToInstruction: BurnInstruction`<br>`jupiter-program-library/libraries/type-length-value/src/state.rsjupiter-program-library/libraries/pod/src/slice.rsextra-account-metassrc/de/mod.rsfailed to write whole bufferfailed to fill whole buffera Display implement`

### `brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1` `gum-omnichain`

- `jup`: ` (bytes withdrewDeadlockdeadlockamount: operator__inbox_event_authgum-omnichain/src/instructions/complete_claim.rsinbox_hash INBOUNDproof_hash target_token_address: swap_data.chain_id: jupnet_target_token_mint: complete_`<br>`123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyzgum-omnichain/src/instructions/complete_withdrawal.rsSignature validation successfulAccountBurnedAmountAccountBurnedAmount doneChecking dataChecking chain id gum-`<br>`_ZN20jupnet_alt_bn128_bls8g2_point7G2Point16verify_signature17he7f0aeba795deafbE`
- `sol_verify_bls_merkle_key`: `sol_verify_bls_merkle_key`<br>`sol_verify_bls_merkle_key`

### `9QUEKQy6LKCUSqmkiiwSkxKALDfhAX5JYx3Uvh7jztJe` `src/extension/mod.rs`

- `vote`: `Error: Rent reclamation disabledError: Already approvedError: Already rejectedError: Already cancelledError: Invalid number of accountsError: Invalid accountError: No members with Vote permissionError: No members with In`

### `GUMebNDCYyF81xjyqaHagbgMQVUTb8fBC9YRh25xSH64` `gum-omnichain`

- `jup`: `failed to write whole bufferfailed to fill whole buffera Display implementation returned an error unexpectedlyUnexpected length of inputErrorcalled `Result::unwrap()` on an `Err` valuejupderived_object__inbox_event_authU`
- `sol_verify_bls_merkle_key`: `sol_verify_bls_merkle_key`

## Assessment

- The census indexes all upgradeable JupNet executables visible in the saved loader scan.
- `sol_verify_bls_merkle_key` appears in Gum omnichain executables, matching the outbox verifier payload analysis.
- No executable in the census exposed canonical JUP, current validator, vote or stake key material.
- Source-path/string evidence still supports application-level Gum/outbox verification, but did not reveal a public Dove registry, JUP stake-weight table, slashing or reward implementation.
