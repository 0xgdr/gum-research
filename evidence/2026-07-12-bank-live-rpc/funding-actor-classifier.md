# Funding Actor Classifier

## Scope

- Snapshot: `evidence/2026-07-12-bank-live-rpc`
- Positive funding/setup events: `1`
- Funding actors collected: `20`
- Evidence seed: root submitter funding-history positive-delta transaction(s)

## Funding Events

| File | Time | Slot | Signature | Submitter delta | Fee payer | Transfer sources | Non-standard programs |
|---|---|---:|---|---:|---|---|---|
| `solana-mainnet-root-submitter-funding-6f5muRji-tx-3tT26UGo.json` | `2026-03-17T13:55:02+00:00` | 407026644 | `3tT26UGoe2Vdeg4drULx3jbwZQe9uzMDW1xwuoB33opzfs9SXdmiWMRcCWXXKsPtwd9v2qCCV63Pt2qWGfh8iBX3` | 2132273211 | `JUPW3tHBxmNRzVnLmTyYUsUDB6izZSEtupY6znBC5mo` | `7r3RH97CtnYvoUTG18pH3y8c47K7XtTVwzuDifgjiTMM` | `bk1PDAkbHEBGtVRiM94Lzets8gVFP7FgySyfkAc8MPN`<br>`op16NNe3ZDePmRze6ySKvZzKgT1D2duqSWg9b1rfCnR` |

## Actor Classification

| Account | Inferred roles | Owner | Executable | Lamports | Space | Local tx files | Local signer files | Local program files | Recent signatures | Latest seen | Security role |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|---|
| `11111111111111111111111111111111` | `funding-tx instruction account`<br>`instruction program`<br>`invoked program` | `NativeLoader1111111111111111111111111111111` | `True` | 1 | 21 | 35 | 0 | 29 | 0 | `unknown` | `None` |
| `5SdaDQZA6fTKmvCps5GjcKqhoompsJ9hPabmAi6A3LCK` | `funding-tx instruction account`<br>`writable funding event account`<br>`writable funding-tx account` | `None` | `None` | None | None | 1 | 0 | 0 | 0 | `unknown` | `None` |
| `6f5muRjigWVnoQHfXWLeXFfafUqMVJfzoBBJL8Gwquji` | `funding-tx instruction account`<br>`root submitter`<br>`root submitter funded in positive event`<br>`writable funding event account`<br>`writable funding-tx account` | `11111111111111111111111111111111` | `False` | 2127865131 | 0 | 260 | 259 | 0 | 20 | `2026-07-13T07:47:25+00:00` | `None` |
| `7ioMTUh2oA2FGBpkwZPRRe8MsS6Po2nJfnoUengnKU7G` | `funding-tx instruction account`<br>`writable funding event account`<br>`writable funding-tx account` | `TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA` | `False` | 2039280 | 165 | 1 | 0 | 0 | 0 | `unknown` | `None` |
| `7r3RH97CtnYvoUTG18pH3y8c47K7XtTVwzuDifgjiTMM` | `funding-tx instruction account`<br>`parsed transfer source into root submitter`<br>`writable funding event account`<br>`writable funding-tx account` | `None` | `None` | None | None | 1 | 0 | 0 | 20 | `2026-03-27T16:24:54+00:00` | `None` |
| `ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL` | `funding-tx instruction account`<br>`instruction program`<br>`invoked program` | `BPFLoader2111111111111111111111111111111111` | `True` | 3388605256 | 105032 | 8 | 0 | 7 | 0 | `unknown` | `None` |
| `ComputeBudget111111111111111111111111111111` | `instruction program`<br>`invoked program` | `NativeLoader1111111111111111111111111111111` | `True` | 1 | 22 | 36 | 0 | 36 | 0 | `unknown` | `None` |
| `Dimb7bb1c3x4RAQAhHiP6w3pox6UFfp1eGqN5Ym7P99s` | `funding-tx instruction account`<br>`writable funding event account`<br>`writable funding-tx account` | `None` | `None` | None | None | 1 | 0 | 0 | 0 | `unknown` | `None` |
| `DyEnjnLsr56cwJ4FK38xKw3YyjQ5BgHTq1dgwYMjRCxQ` | `funding-tx instruction account`<br>`writable funding event account`<br>`writable funding-tx account` | `bk1PDAkbHEBGtVRiM94Lzets8gVFP7FgySyfkAc8MPN` | `False` | 1392000 | 72 | 1 | 0 | 0 | 0 | `unknown` | `None` |
| `FyKUkJTtx6WdUdxkqNkKGq5ZhJNJVAa2jUrtXAZoxXfK` | `funding-tx instruction account`<br>`writable funding event account`<br>`writable funding-tx account` | `TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA` | `False` | 10420273016 | 165 | 1 | 0 | 0 | 0 | `unknown` | `None` |
| `HuKNTnyZ1fD4yXwXrTLyNSEkmXqERH6nbxazyDzFVuhU` | `funding-tx instruction account`<br>`writable funding event account`<br>`writable funding-tx account` | `None` | `None` | None | None | 1 | 0 | 0 | 0 | `unknown` | `None` |
| `JUPW3tHBxmNRzVnLmTyYUsUDB6izZSEtupY6znBC5mo` | `fee payer`<br>`funding-tx instruction account`<br>`transaction signer`<br>`writable funding event account`<br>`writable funding-tx account` | `11111111111111111111111111111111` | `False` | 4053384455 | 0 | 26 | 26 | 0 | 20 | `2026-07-13T11:00:47+00:00` | `None` |
| `NSwJLtxb6S62dEJPygFBREmJKyvTEQ5e9Nsmrn4pKJn` | `funding-tx instruction account` | `None` | `None` | None | None | 1 | 0 | 0 | 0 | `unknown` | `None` |
| `So11111111111111111111111111111111111111112` | `funding-tx instruction account` | `TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA` | `False` | 1588190431867 | 82 | 3 | 0 | 0 | 0 | `unknown` | `None` |
| `Sysvar1nstructions1111111111111111111111111` | `funding-tx instruction account` | `None` | `None` | None | None | 24 | 0 | 0 | 0 | `unknown` | `None` |
| `TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA` | `funding-tx instruction account`<br>`instruction program`<br>`invoked program` | `BPFLoaderUpgradeab1e11111111111111111111111` | `True` | 58238313 | 36 | 7 | 0 | 7 | 0 | `unknown` | `None` |
| `VUMS4yy6oKWw4zqHHn9o9moDbaPuRmB7a6fGB7sNVXT` | `funding-tx instruction account` | `bk1PDAkbHEBGtVRiM94Lzets8gVFP7FgySyfkAc8MPN` | `False` | 953520 | 9 | 1 | 0 | 0 | 0 | `unknown` | `None` |
| `bk1PDAkbHEBGtVRiM94Lzets8gVFP7FgySyfkAc8MPN` | `Gum Bank request path`<br>`instruction program`<br>`invoked program`<br>`non-standard funding event program` | `BPFLoaderUpgradeab1e11111111111111111111111` | `True` | 1141440 | 36 | 1 | 0 | 1 | 0 | `unknown` | `None` |
| `op16NNe3ZDePmRze6ySKvZzKgT1D2duqSWg9b1rfCnR` | `funding-tx instruction account`<br>`instruction program`<br>`invoked program`<br>`non-standard funding event program` | `BPFLoaderUpgradeab1e11111111111111111111111` | `True` | 1141440 | 36 | 1 | 0 | 1 | 0 | `unknown` | `None` |
| `zVFYUJR5N4jnbxcSQFznjD5hjEmVbjSb9aiVLS4zQHh` | `funding-tx instruction account` | `bk1PDAkbHEBGtVRiM94Lzets8gVFP7FgySyfkAc8MPN` | `False` | 3173760 | 328 | 1 | 0 | 0 | 0 | `unknown` | `None` |

## Decoded Funding Logs

### `solana-mainnet-root-submitter-funding-6f5muRji-tx-3tT26UGo.json`

| Label | Bytes | Base58 | Known account match | Hex | Integer interpretation |
|---|---:|---|---|---|---|
| `withdrawal_request_pubkey` | 32 | `Eveu6MH3DxUaH5ZTHBU8BdxjiBcmKJ91wVi6tqjvWBY8` | `None` | `cee690825ee771b7092f089b4fd876ef5cb79327c11d05a96292cc8e3905f40d` | `n/a` |
| `mint` | 32 | `So11111111111111111111111111111111111111112` | `So11111111111111111111111111111111111111112` | `069b8857feab8184fb687f634618c035dac439dc1aeb3b5598a0f00000000001` | `n/a` |
| `amount 1` | 16 | `1111111111111111` | `None` | `00000000000000000000000000000000` | `u128_be=0` |
| `amount 0` | 16 | `1111111111114FRTYE` | `None` | `0000000000000000000000007f17e83b` | `u128_be=2132273211` |
| `recipient` | 32 | `6f5muRjigWVnoQHfXWLeXFfafUqMVJfzoBBJL8Gwquji` | `6f5muRjigWVnoQHfXWLeXFfafUqMVJfzoBBJL8Gwquji` | `540be751862e820b3965a1960f980e4e66d860448aac1d47f529e2ecd4cd927d` | `n/a` |
| `jupnet` | 32 | `Eveu6MH3DxUaH5ZTHBU8BdxjiBcmKJ91wVi6tqjvWBY8` | `None` | `cee690825ee771b7092f089b4fd876ef5cb79327c11d05a96292cc8e3905f40d` | `n/a` |
| `valid_till` | 8 | `11113hjxnu` | `None` | `0000000069b95d72` | `u64_be=1773755762, u64_le=8240946753780580352` |
| `impl program key` | 32 | `op16NNe3ZDePmRze6ySKvZzKgT1D2duqSWg9b1rfCnR` | `op16NNe3ZDePmRze6ySKvZzKgT1D2duqSWg9b1rfCnR` | `0bfddcb2046ffea10c2a38ee50143aff4db314121af2ee0e5e885f557dd62256` | `n/a` |
| `message_hash` | 32 | `82hXVPWyuFKqApkC89jnstv4Z9yrpwg1GFNERswp71wk` | `None` | `6871363a3e8eb06c79f2c8b1072b2db4a25ed236fc7fa0f3754921a091085287` | `n/a` |

Program data payloads:

| Bytes | Base64 | Hex prefix |
|---:|---|---|
| 80 | `D335QYJWFKbO5pCCXudxtwkvCJtP2HbvXLeTJ8EdBaliksyOOQX0DQabiFf+q4GE+2h/Y0YYwDXaxDncGus7VZig8AAAAAABO+gXfwAAAAA=` | `0f7df941825614a6cee690825ee771b7092f089b4fd876ef5cb79327c11d05a96292cc8e3905f40d069b8857feab8184fb687f634618c035dac439dc1aeb3b5598a0f000000000013be8177f00000000` |
| 112 | `Wr/fNZOIBGQL/dyyBG/+oQwqOO5QFDr/TbMUEhry7g5eiF9VfdYiVs7mkIJe53G3CS8Im0/Ydu9ct5MnwR0FqWKSzI45BfQNwLRb9enHFyeSm9tCoJudRsatAy+siHXb9L6QOFI2zblyXblpAAAAAA==` | `5abfdf35938804640bfddcb2046ffea10c2a38ee50143aff4db314121af2ee0e5e885f557dd62256cee690825ee771b7092f089b4fd876ef5cb79327c11d05a96292cc8e3905f40dc0b45bf5e9c71727929bdb42a09b9d46c6ad032fac8875db` |

## Assessment

- The funding/setup event is tied to the Gum Bank request path rather than a plain wallet-to-wallet top-up.
- The root submitter received SOL through a parsed transfer during a transaction that also invoked non-standard Gum/JupNet programs.
- The collector/analyzer found no canonical JUP, current validator, vote or stake key classification among the funding actors.
- The most useful next comparison is a cohort of other `bk1PDA...` request/withdrawal transactions to determine whether funding infrastructure accounts through this path is exceptional or routine.
