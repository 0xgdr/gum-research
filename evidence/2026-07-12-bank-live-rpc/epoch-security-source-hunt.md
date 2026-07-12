# Epoch Security Source Hunt

## Scope

- Snapshot: `evidence/2026-07-12-bank-live-rpc`
- Binary records scanned: `3153`
- Outbox update payloads decoded: `1`
- Watched validator/vote/stake keys: `21`

## Root Under Test

- Source transaction file: `solana-mainnet-outbox-tx-3Zjq8FZd.json`
- Signature: `3Zjq8FZdd9srj5UbC9FrRrstNB8eSXreTCWTKG7b4ozsZLVHjXoPkcQKK72gTuzLZcLFsV2MebiaMDiCiVKLS4pQ`
- Slot: `432511387`
- Time: `2026-07-12T21:25:50+00:00`
- Epoch/root slot: `271`
- Root: `6928957b2ea436bcc9c44970a0f85364b6f0c8e5e4e886565eea061c9bd8d999`
- Candidate aggregate-key material: `87e930814a0131f70e4b405f4e30ca3e226ad5bee2e5e40d584947d48c4bcceb15f96af18671975c31abc6d2c3ea8230ee775da12cd69b5331e35865ad2c4025`
- Candidate leaf hash: `549627c9007f9bde82667fab9390ede2ff81307d18b4b391beda278f8bb48e44`
- Merkle match: `True`

## Target Byte Hits

| Target | Hits | Hit classes | First hit locations |
|---|---:|---|---|
| `epoch root` | 6 | `other saved artifact: 2`<br>`outbox-owned account state: 1`<br>`outbox transaction: 2`<br>`outbox instruction: 1` | `solana-mainnet-getMultipleAccounts-BankOwnerContext.json $.response.result.value[2].data (account-base64, 320 bytes)`<br>`solana-mainnet-getMultipleAccounts-BankRecurringAccounts.json $.response.result.value[18].data (account-base64, 320 bytes)`<br>`solana-mainnet-getProgramAccounts-JupNetOutboxProgram.json $.result[0].account.data (account-base64, 320 bytes)`<br>`solana-mainnet-outbox-tx-3Zjq8FZd.json $.result.meta.logMessages[6] (program-data-log, 32 bytes)`<br>`solana-mainnet-outbox-tx-3Zjq8FZd.json $.result.meta.logMessages[7] (program-data-log, 40 bytes)`<br>`solana-mainnet-outbox-tx-3Zjq8FZd.json $.result.transaction.message.instructions[0].data (instruction-base58, 305 bytes)` |
| `candidate aggregate key material` | 21 | `outbox instruction: 11`<br>`other saved artifact: 2`<br>`outbox transaction: 8` | `solana-mainnet-bank-tx-5EivNpnD.json $.result.meta.innerInstructions[0].instructions[0].data (instruction-base58, 337 bytes)`<br>`solana-mainnet-bank-tx-5EivNpnD.json $.result.transaction.message.instructions[2].data (instruction-base58, 463 bytes)`<br>`solana-mainnet-bank-tx-5JQFCWSE.json $.result.meta.innerInstructions[0].instructions[0].data (instruction-base58, 337 bytes)`<br>`solana-mainnet-bank-tx-5JQFCWSE.json $.result.transaction.message.instructions[2].data (instruction-base58, 463 bytes)`<br>`solana-mainnet-outbox-tx-2CzThmfQ.json $.result.meta.innerInstructions[0].instructions[0].data (instruction-base58, 337 bytes)`<br>`solana-mainnet-outbox-tx-2CzThmfQ.json $.result.transaction.message.instructions[2].data (instruction-base58, 463 bytes)` |
| `candidate aggregate-key leaf hash` | 0 | `None` | `None` |
| `untyped 32-byte verifier field` | 1 | `outbox instruction: 1` | `solana-mainnet-outbox-tx-3Zjq8FZd.json $.result.transaction.message.instructions[0].data (instruction-base58, 305 bytes)` |
| `full 305-byte update payload` | 1 | `outbox instruction: 1` | `solana-mainnet-outbox-tx-3Zjq8FZd.json $.result.transaction.message.instructions[0].data (instruction-base58, 305 bytes)` |

## Watched Security Text Hits

| Watched value | Files containing text |
|---|---:|
| `canonical JUP mint` | 0 |
| `validator node idtxyt9e3XHKu9yEHdaTYdYmZSbeeramkseguZ94yf4` | 3 |
| `vote account votbYAneU8HVs8HvNCToMMxEsMfTsmzSharYFy94dcb` | 2 |
| `validator node idt4cGQcDaGmZGv19coMivuLgJUsKbiWrxu1hse6xXA` | 3 |
| `vote account votmS9U1br5cmR19X57V5Nc7WU8JtQNwRkxxFMhUkit` | 2 |
| `validator node idtjSRacRANaBzv1HsJeQQco4Ydomqm6Popiu9rYnpS` | 3 |
| `vote account votxjy8SwJvdbR3K9wur4RzViUTDVt5DYFwv91QqFUr` | 2 |
| `validator node idtwvwFjrD1revnK7R3usirxke5NUW2ra6L15zFAgR8` | 3 |
| `vote account votneC7rvDKitBgNid5ZkirjmV15rnNCc5TTfBihqtc` | 2 |
| `validator node idttUP3C6BQseTUzSaHVUcgtFdWDr7uyvVwDf1onwnH` | 3 |
| `vote account votEYiWe4mxxVKhyuK74WERFcT9usAKL62vgAo8EXaq` | 2 |
| `validator node idt57UCtb44m66agbVUfQKtAwQhj3oj8CP49kixWTUj` | 3 |
| `vote account votU897ZBdxsPfJjvJzgSp2Dba9D8xnnyevLXmvRSJp` | 2 |
| `validator node idtcqyhGdL3f32N1wKCKhkR2ehdpxrap1cbyQQQUVFH` | 3 |
| `vote account votibKxNCsASJ1yQes2VQn7jrhbBLWGDwShMUP1KhdH` | 2 |
| `stake account stk23puGctEYcSvPb3DzTqJoujUWpyywFq316wSRqAF` | 1 |
| `stake account stk9TpCLWABpcpVMyrjYr78PCHLv5truqoEDxLuviNZ` | 1 |
| `stake account stkUMGCfQkcGzWfLAe613452NeZAwLacNKvg1PiGeck` | 1 |
| `stake account stkeSVxj9zHmL4Mi4R4oi1Ry99nrUr4gXq9sPGbQPMD` | 1 |
| `stake account stkozfFfy6194UZgY8M5CevPQZQX12qt6NFp8cemb2t` | 1 |
| `stake account stkxTGGZMvpDANsvPLgLfd63eJk8hFdJM76VZ7xMKv6` | 1 |
| `stake account stkyWcr6Vvr1KNztLHYdy1kcjde1zyD5z1ZSL87doMu` | 1 |

## Co-Location Checks

| Check | Matching records |
|---|---:|
| Candidate aggregate key in same binary record as canonical JUP/validator/vote/stake key | 0 |
| Epoch root in same binary record as canonical JUP/validator/vote/stake key | 0 |

## Candidate Registry Records

| File | JSON path | Kind | Size | Signals | Security hits | SHA256 |
|---|---|---|---:|---|---|---|
| `solana-mainnet-bank-tx-5EivNpnD.json` | `$.result.meta.innerInstructions[0].instructions[0].data` | `instruction-base58` | 337 | `candidate aggregate key` | `None` | `3f95cf465620117b8c395667ce58e856c686fe83343abf8d17dfdebeef60c130` |
| `solana-mainnet-bank-tx-5EivNpnD.json` | `$.result.transaction.message.instructions[2].data` | `instruction-base58` | 463 | `candidate aggregate key` | `None` | `ca9dd49edb149ba051be5b0a9c0a9d1c529c8b6a7461a7a4b478d450d78b0463` |
| `solana-mainnet-bank-tx-5JQFCWSE.json` | `$.result.meta.innerInstructions[0].instructions[0].data` | `instruction-base58` | 337 | `candidate aggregate key` | `None` | `d9080bbd192d4bcb3a838bc48bb1b5a32e6acd8675e34c08ce9ded3941c6084f` |
| `solana-mainnet-bank-tx-5JQFCWSE.json` | `$.result.transaction.message.instructions[2].data` | `instruction-base58` | 463 | `candidate aggregate key` | `None` | `65769c2631c2570d4247f24f30b4c6d9ca6d2b7a92ae2d111e943674f6f0d5b8` |
| `solana-mainnet-getAccountInfo-GumBankProgramData-full.json` | `$.result.value.data` | `account-base64` | 602517 | `epoch 271 little-endian` | `None` | `0b493204c0e455d60c9b8dde8f9e6b9f0248b4e9dc8dc083522a34357d2b0b65` |
| `solana-mainnet-getAccountInfo-GumBankProgramProgramData-full.json` | `$.result.value.data` | `account-base64` | 795965 | `epoch 271 little-endian` | `None` | `b69ba14a2ed24be64edd6e87d77cbf72ba829153b16e759213152797d83a28b4` |
| `solana-mainnet-getAccountInfo-OwnerProgramData-jnoUtncG.json` | `$.result.value.data` | `account-base64` | 149861 | `epoch 271 little-endian` | `None` | `2a77b556136180e1883ae678dafaf77d6da3315297ecec748412cde39aa06bc8` |
| `solana-mainnet-getMultipleAccounts-BankOwnerContext.json` | `$.response.result.value[2].data` | `account-base64` | 320 | `root` | `None` | `5fd9c0b75277dfd2e1a1dd5e04dd3f75f09d7052e3893bab0d6b8c142b98146c` |
| `solana-mainnet-getMultipleAccounts-BankRecurringAccounts.json` | `$.response.result.value[18].data` | `account-base64` | 320 | `root` | `None` | `5fd9c0b75277dfd2e1a1dd5e04dd3f75f09d7052e3893bab0d6b8c142b98146c` |
| `solana-mainnet-getProgramAccounts-JupNetOutboxProgram.json` | `$.result[0].account.data` | `account-base64` | 320 | `root`<br>`epoch 271 little-endian` | `None` | `bd064d929ac0f29ac717e449f3e967eace574480879607e104d7f083b2e97cbd` |
| `solana-mainnet-outbox-tx-2CzThmfQ.json` | `$.result.meta.innerInstructions[0].instructions[0].data` | `instruction-base58` | 337 | `candidate aggregate key` | `None` | `42b7297e43d80687d883ddeea3ed1e1f11452806bbeb8829053bb9014974806f` |
| `solana-mainnet-outbox-tx-2CzThmfQ.json` | `$.result.transaction.message.instructions[2].data` | `instruction-base58` | 463 | `candidate aggregate key` | `None` | `4a4a84e1da9e5ec92985c7242c123bb65ee0e07c85294c5b9c4c336466428f6b` |
| `solana-mainnet-outbox-tx-2FzPsrQ1.json` | `$.result.meta.innerInstructions[0].instructions[0].data` | `instruction-base58` | 337 | `candidate aggregate key` | `None` | `2fd56f03a7c76a1094f9adb1ce5c11d2841cbf6b6f96f7781a2bb7de451b3578` |
| `solana-mainnet-outbox-tx-2FzPsrQ1.json` | `$.result.transaction.message.instructions[2].data` | `instruction-base58` | 496 | `candidate aggregate key` | `None` | `f1953473b84e2765f0fb5ac00a4f622a1a1e329d7a7ff2d50262a5247861f626` |
| `solana-mainnet-outbox-tx-2NbTujvU.json` | `$.result.meta.innerInstructions[0].instructions[0].data` | `instruction-base58` | 337 | `candidate aggregate key` | `None` | `5782dfd77ee849bdb8b77d80217ac2c5bbae64e881fcf3640438089fdf557df9` |
| `solana-mainnet-outbox-tx-2NbTujvU.json` | `$.result.transaction.message.instructions[2].data` | `instruction-base58` | 496 | `candidate aggregate key` | `None` | `b7ecba03169fd0714513db71a0b4945f94c187c338bdd5d862a2a2286c91b31f` |
| `solana-mainnet-outbox-tx-2cMxqNYU.json` | `$.result.meta.innerInstructions[0].instructions[0].data` | `instruction-base58` | 337 | `candidate aggregate key` | `None` | `b503114b0b057e337131ad192a2ad822a91820c25e671d279613e24c94b4feab` |
| `solana-mainnet-outbox-tx-2cMxqNYU.json` | `$.result.transaction.message.instructions[2].data` | `instruction-base58` | 463 | `candidate aggregate key` | `None` | `068281ab33bfb8b704ea481e0e81932189f6d5515103fcfd42f7be965f83407b` |
| `solana-mainnet-outbox-tx-34DtKNBj.json` | `$.result.meta.innerInstructions[0].instructions[0].data` | `instruction-base58` | 337 | `candidate aggregate key` | `None` | `0caaf35d563fe6db66c4cc91c29403ca1d6550457ca90ba6c1a90268bad49d68` |
| `solana-mainnet-outbox-tx-34DtKNBj.json` | `$.result.transaction.message.instructions[2].data` | `instruction-base58` | 463 | `candidate aggregate key` | `None` | `dc41fefe69b5c83b5d2351a4c32b6a6e7468ddf00d96bf7ebf698c82a21ed85f` |
| `solana-mainnet-outbox-tx-3Zjq8FZd.json` | `$.result.meta.logMessages[6]` | `program-data-log` | 32 | `root` | `None` | `bd914d055147fa98c499d5e423d2d436a7f8d1a23f5a734882b042716140c82c` |
| `solana-mainnet-outbox-tx-3Zjq8FZd.json` | `$.result.meta.logMessages[7]` | `program-data-log` | 40 | `root`<br>`epoch 271 little-endian` | `None` | `13e0a1b863f7ad1e0f82470a805f4e3bab6f7e665e2044b8d089fd237f8be61d` |
| `solana-mainnet-outbox-tx-3Zjq8FZd.json` | `$.result.transaction.message.instructions[0].data` | `instruction-base58` | 305 | `root`<br>`candidate aggregate key`<br>`untyped verifier field`<br>`epoch 271 little-endian` | `None` | `b335265c6e8e17244e0b74b803ad834f93fa4cafa1e82b3e2950622e1f789485` |
| `solana-mainnet-outbox-tx-4ivz1c34.json` | `$.result.meta.innerInstructions[0].instructions[0].data` | `instruction-base58` | 337 | `candidate aggregate key` | `None` | `f1fee661b9beef824efec4e8e184a98a61db6e18ed6a4ad46127f05a23954307` |
| `solana-mainnet-outbox-tx-4ivz1c34.json` | `$.result.transaction.message.instructions[2].data` | `instruction-base58` | 496 | `candidate aggregate key` | `None` | `070f4e78e7bac0e340a48c6c49765ef92259cc90a5b661ec6596a473cc3b650e` |
| `solana-mainnet-outbox-tx-4u2aHaAt.json` | `$.result.meta.innerInstructions[0].instructions[0].data` | `instruction-base58` | 337 | `candidate aggregate key` | `None` | `a1587321e0eacd76e3424d9f55a7e1b81e483db02764f6998befd9ce06dd21cf` |
| `solana-mainnet-outbox-tx-4u2aHaAt.json` | `$.result.transaction.message.instructions[2].data` | `instruction-base58` | 463 | `candidate aggregate key` | `None` | `6d3205f22c7572d8993143c87bd4643026629bcf8262a381087ef6ee0cf71f35` |
| `solana-mainnet-outbox-tx-Xdk7KN25.json` | `$.result.meta.innerInstructions[0].instructions[0].data` | `instruction-base58` | 337 | `candidate aggregate key` | `None` | `7f3b4fe9438e6bcb2dc52965467c8323cc2ab1e6bae7a98d3e5c7a6cfec69775` |
| `solana-mainnet-outbox-tx-Xdk7KN25.json` | `$.result.transaction.message.instructions[2].data` | `instruction-base58` | 496 | `candidate aggregate key` | `None` | `f2cd92e7275cd9fd2e3d341008263144b6c8d3a5969601c18d81f5153fcfd309` |

## Assessment

- The candidate aggregate-key material appears in saved public artifacts.
- No saved binary record co-located the epoch root or candidate aggregate key with canonical JUP, current validator, vote or stake keys.
- This hunt did not find a public top-half source that maps Dove identities, stake weights or JUP balances into the aggregate-key Merkle tree.
- The current public evidence still stops at the compact verification boundary: aggregate-key material, Merkle proof, epoch root and BLS verification logs.
