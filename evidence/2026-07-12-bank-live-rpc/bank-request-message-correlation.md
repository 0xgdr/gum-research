# Bank Request / Message Correlation

## Scope

- Snapshot: `evidence/2026-07-12-bank-live-rpc`
- `bk1PDA...` rows loaded: `50`
- root-submitter setup rows loaded: `1`
- `BankK...` rows loaded: `50`
- decoded `bk1PDA...` / setup request rows: `19`
- `BankK...` Withdraw rows: `11`
- `BankK...` VerifyRequest rows: `18`
- canonical JUP / current validator / vote / stake intersections: `0`

## Surface Decodability

| Surface | Txs | Decoded message hashes | Decoded request pubkeys | SubmitInbox | VerifyOutbox | Signature verified | Created account spaces | Fee payers | Signers |
|---|---:|---:|---:|---:|---:|---:|---|---|---|
| `bk1PDA` | 50 | 18 | 18 | 0 | 0 | 24 | `bk1PDAkbHEBGtVRiM94Lzets8gVFP7FgySyfkAc8MPN space=72: 18`<br>`bk1PDAkbHEBGtVRiM94Lzets8gVFP7FgySyfkAc8MPN space=448: 17`<br>`bk1PDAkbHEBGtVRiM94Lzets8gVFP7FgySyfkAc8MPN space=300: 6`<br>`TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA space=165: 2` | `JUPW3tHBxmNRzVnLmTyYUsUDB6izZSEtupY6znBC5mo: 49`<br>`F5p1mBd6C3v6NB2oLGM9bLKmtHQ53RMsYKeGPPg4s113: 1` | `JUPW3tHBxmNRzVnLmTyYUsUDB6izZSEtupY6znBC5mo: 49`<br>`F5p1mBd6C3v6NB2oLGM9bLKmtHQ53RMsYKeGPPg4s113: 1` |
| `root_submitter_setup` | 1 | 1 | 1 | 0 | 0 | 1 | `TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA space=165: 2`<br>`bk1PDAkbHEBGtVRiM94Lzets8gVFP7FgySyfkAc8MPN space=72: 1` | `JUPW3tHBxmNRzVnLmTyYUsUDB6izZSEtupY6znBC5mo: 1` | `JUPW3tHBxmNRzVnLmTyYUsUDB6izZSEtupY6znBC5mo: 1` |
| `BankK` | 50 | 0 | 0 | 27 | 18 | 0 | `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ space=41: 14`<br>`BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ space=223: 11`<br>`BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ space=256: 7`<br>`TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA space=165: 5`<br>`BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ space=73: 4`<br>`BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ space=64: 1` | `JUPW3tHBxmNRzVnLmTyYUsUDB6izZSEtupY6znBC5mo: 40`<br>`rfQMFpNueeNufBW4byyEAhvL4To4tCsVBVagcEWG8ea: 10` | `JUPW3tHBxmNRzVnLmTyYUsUDB6izZSEtupY6znBC5mo: 40`<br>`rfQMFpNueeNufBW4byyEAhvL4To4tCsVBVagcEWG8ea: 10` |

## Correlation Summary

- Exact high-value request/message/recipient hits from `bk1PDA...`/setup into `BankK...`: `0`
- Exact `message_hash` hits inside `BankK...` account keys or raw payload blobs: `0`
- Exact withdrawal-request / `jupnet` pubkey hits inside `BankK...`: `0`
- Exact recipient pubkey hits inside `BankK...`: `0`
- Exact common mint/implementation context hits inside `BankK...`: `864`
- Token near-matches between decoded `bk1PDA...` withdrawals and `BankK...` Withdraw transfers: `0`

## Exact Message Hash Matches

- None

## Exact Request / JupNet Pubkey Matches

- None

## Token Near-Matches

- None

## BankK Role Map

| Instruction | Count | SubmitInbox | VerifyOutbox | Programs | Created account spaces | Token authorities |
|---|---:|---:|---:|---|---|---|
| `CacheTokenMetadata` | 1 | 0 | 0 | `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ: 1`<br>`ComputeBudget111111111111111111111111111111: 1`<br>`11111111111111111111111111111111: 1` | `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ space=64: 1` | `None` |
| `RfqSellCommit` | 4 | 0 | 0 | `TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA: 4`<br>`BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ: 4`<br>`ComputeBudget111111111111111111111111111111: 4`<br>`11111111111111111111111111111111: 4`<br>`ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL: 4` | `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ space=73: 4`<br>`TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA space=165: 2` | `2sbhRE62pbi3sLo9CtjM7nYzUynEV4oBAPrGmQPrhnfF: 4`<br>`rfQMFpNueeNufBW4byyEAhvL4To4tCsVBVagcEWG8ea: 4` |
| `RfqSellResolve` | 4 | 4 | 0 | `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ: 4`<br>`JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw: 4`<br>`TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA: 4`<br>`ComputeBudget111111111111111111111111111111: 4` | `None` | `rfQMFpNueeNufBW4byyEAhvL4To4tCsVBVagcEWG8ea: 4` |
| `RfqSwap` | 2 | 2 | 0 | `TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA: 2`<br>`JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw: 2`<br>`BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ: 2`<br>`ComputeBudget111111111111111111111111111111: 2`<br>`11111111111111111111111111111111: 2`<br>`ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL: 2` | `TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA space=165: 2`<br>`BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ space=41: 2` | `rfQMFpNueeNufBW4byyEAhvL4To4tCsVBVagcEWG8ea: 2`<br>`2sbhRE62pbi3sLo9CtjM7nYzUynEV4oBAPrGmQPrhnfF: 2` |
| `RouteV2` | 1 | 1 | 0 | `DRVSpZ2YUYYKgZP8XtLhAGtT1zYSCKzeHfb4DgRnrgqD: 1`<br>`TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA: 1`<br>`JUP6LkbZbjS1jKKwapdHNy74zcZ3tLUZoi5QNyVTaV4: 1`<br>`JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw: 1`<br>`BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ: 1`<br>`ComputeBudget111111111111111111111111111111: 1` | `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ space=41: 1`<br>`TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA space=165: 1` | `2sbhRE62pbi3sLo9CtjM7nYzUynEV4oBAPrGmQPrhnfF: 1` |
| `Swap` | 1 | 1 | 0 | `DRVSpZ2YUYYKgZP8XtLhAGtT1zYSCKzeHfb4DgRnrgqD: 1`<br>`TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA: 1`<br>`JUP6LkbZbjS1jKKwapdHNy74zcZ3tLUZoi5QNyVTaV4: 1`<br>`JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw: 1`<br>`BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ: 1`<br>`ComputeBudget111111111111111111111111111111: 1` | `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ space=41: 1`<br>`TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA space=165: 1` | `2sbhRE62pbi3sLo9CtjM7nYzUynEV4oBAPrGmQPrhnfF: 1` |
| `Sweep` | 9 | 9 | 0 | `TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA: 9`<br>`JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw: 9`<br>`BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ: 9`<br>`ComputeBudget111111111111111111111111111111: 9`<br>`11111111111111111111111111111111: 9`<br>`ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL: 9` | `None` | `FaYMb5VeMUDRTFSjbjpz2Xo4N61qpvEVNvDKA2NELtZt: 2`<br>`CcyZXf2cZeCdL5aQGEtNiAJLrxXaPC8Gi6KAmJns4XLL: 1`<br>`4Xg5h2wuU5DihS2TcfswDrwmtWAXfQXMqsdQtDBr3Cng: 1`<br>`GjbTAUTZmWKK53bdBfvxqNaYYjHidkBg45QPGAH6FSaB: 1`<br>`BeGkobidighjgfRxHR66Mwy5wDBwNFYwtKmitMK1TRzK: 1`<br>`FsGPbH6Y7f8zMphzxfgECh5Q5RkFTugUuT4jbdRqLznh: 1` |
| `TransferChecked` | 1 | 1 | 0 | `JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw: 1`<br>`BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ: 1`<br>`TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb: 1`<br>`ComputeBudget111111111111111111111111111111: 1`<br>`11111111111111111111111111111111: 1`<br>`ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL: 1` | `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ space=41: 1` | `2sbhRE62pbi3sLo9CtjM7nYzUynEV4oBAPrGmQPrhnfF: 1` |
| `VerifyRequest` | 18 | 0 | 18 | `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ: 18`<br>`11111111111111111111111111111111: 18`<br>`ComputeBudget111111111111111111111111111111: 18`<br>`jnoUtncGR9ZCCMixtys6Gzy5coTo6mnmUZuEHRQFTFV: 18` | `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ space=223: 11`<br>`BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ space=256: 7` | `None` |
| `Withdraw` | 11 | 11 | 0 | `JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw: 11`<br>`BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ: 11`<br>`ComputeBudget111111111111111111111111111111: 11`<br>`11111111111111111111111111111111: 11`<br>`ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL: 11`<br>`TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA: 10` | `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ space=41: 11` | `2sbhRE62pbi3sLo9CtjM7nYzUynEV4oBAPrGmQPrhnfF: 11` |

## Assessment

- No decoded `bk1PDA...` message hash, withdrawal-request pubkey or `jupnet` pubkey appeared directly in sampled `BankK...` account keys or raw payload blobs.
- No amount+recipient or amount+mint token near-match was found between decoded `bk1PDA...` withdrawals and sampled `BankK...` Withdraw transfers.
- The strongest connection remains structural: shared operational signer behavior, shared Bank/Gum domain, and adjacent inbox/outbox helper behavior, not a per-message proof across the two sampled windows.
- The `BankK...` rows create Bank-owned request/state accounts with 41-byte and 223-byte layouts, while decoded `bk1PDA...` request rows create 72-byte request accounts; this supports separate public state layouts for the two surfaces.
- No canonical JUP/current validator/vote/stake key intersections appeared in the correlation corpus.
