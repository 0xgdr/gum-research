# Bank Account Graph and Payload Analysis

## Scope

- Sampled Bank instructions: `8`
- Distinct account keys passed to Bank instructions: `36`
- Bank instructions with canonical Solana JUP mint account: `0`

## Global Account Frequency

| Account | Count | Role hints |
|---|---:|---|
| `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ` | 17 | Gum Bank Program executable |
| `JUPW3tHBxmNRzVnLmTyYUsUDB6izZSEtupY6znBC5mo` | 10 | signer |
| `HVKuqyK6wjexdVJAUARiGdQTdGBBWhdYyhCZGFXh9d4s` | 8 |  |
| `TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA` | 8 | SPL Token program |
| `2x4wPZePCbq2W9tFfP2bagXjXnysdqNWQWMtwGMoyPFv` | 8 |  |
| `11111111111111111111111111111111` | 7 | system program |
| `2sbhRE62pbi3sLo9CtjM7nYzUynEV4oBAPrGmQPrhnfF` | 6 |  |
| `C8VeT16ySsyMW9xijjmYgvw83FfvEZVJawn5jgpzcf1X` | 6 |  |
| `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` | 6 | USDC mint |
| `ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL` | 5 |  |
| `EG9fKpmLgkzCYZdj8uNDhHu5xmeXCZakccV6QmUavbzt` | 5 |  |
| `9DvDdsw38EB3RPChPqHkgBmntFbM5v79QxMyMSbfXWuy` | 5 |  |
| `JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw` | 5 |  |
| `Sysvar1nstructions1111111111111111111111111` | 4 | instructions sysvar |
| `rfQMFpNueeNufBW4byyEAhvL4To4tCsVBVagcEWG8ea` | 3 | signer |
| `5x38Kp4hvdomTCnCrAny4UtMUt5rQBdB6px2K1Ui45Wq` | 3 |  |
| `7SnRzKKo8QonsMUb1wYCQoqCsLq2njp41yS33gJsVfp8` | 2 |  |
| `7jqXWdiyYkY9XUStYhbGzSgn1VCr9tMF4LNCK52oG76U` | 2 |  |
| `5RD1PyMjzgo3gMCToQTnqk44L99kQZ3MnGnRzxMwRwLj` | 2 |  |
| `Cei4rumgr8ePPdNCMim7yo4C6idaMNv3N8P3qqQbbjyf` | 2 |  |
| `H5Y5aLdTQXRWJ6kitWeUkHyAEVLPPfChgSxhUBVxZ3D2` | 2 |  |
| `4s3gnkf1R2UzAWbfvVowfaW7VdLDNSQhmwjYcSnMYwmT` | 2 |  |
| `GqpFMhoHzfhUnM65kvCRkzozm4c72A9TpNZzt9D69z88` | 2 |  |
| `So11111111111111111111111111111111111111112` | 2 | wrapped SOL mint |
| `5DtSBy1imR7W2Zbdt9Z1gfRPVmVZyTVorvi562SZ7bvd` | 2 |  |
| `3C1LxtpR3Mh5RQjydfeQdvRaAzpStWM7gBi1XzP9oyGt` | 2 |  |
| `jnoUtncGR9ZCCMixtys6Gzy5coTo6mnmUZuEHRQFTFV` | 2 |  |
| `8NiTpug6V5SeWN42wwTGqUcKM3y6dCnRR6ouV7sf4Kak` | 1 |  |
| `ESLg5R1Ry4LXSfxh67BUPusKHeHGpaJWHGjTGeg6oYGE` | 1 |  |
| `gum1UnP99NnohRt3YcdkA4PGubCYvtWiH8mgjT2KhXH` | 1 |  |

## Strong Co-Occurrence Edges

| Account A | Account B | Shared instructions |
|---|---|---:|
| `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ` | `HVKuqyK6wjexdVJAUARiGdQTdGBBWhdYyhCZGFXh9d4s` | 8 |
| `2x4wPZePCbq2W9tFfP2bagXjXnysdqNWQWMtwGMoyPFv` | `HVKuqyK6wjexdVJAUARiGdQTdGBBWhdYyhCZGFXh9d4s` | 8 |
| `2x4wPZePCbq2W9tFfP2bagXjXnysdqNWQWMtwGMoyPFv` | `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ` | 8 |
| `11111111111111111111111111111111` | `HVKuqyK6wjexdVJAUARiGdQTdGBBWhdYyhCZGFXh9d4s` | 7 |
| `11111111111111111111111111111111` | `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ` | 7 |
| `11111111111111111111111111111111` | `2x4wPZePCbq2W9tFfP2bagXjXnysdqNWQWMtwGMoyPFv` | 7 |
| `HVKuqyK6wjexdVJAUARiGdQTdGBBWhdYyhCZGFXh9d4s` | `JUPW3tHBxmNRzVnLmTyYUsUDB6izZSEtupY6znBC5mo` | 6 |
| `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ` | `JUPW3tHBxmNRzVnLmTyYUsUDB6izZSEtupY6znBC5mo` | 6 |
| `11111111111111111111111111111111` | `JUPW3tHBxmNRzVnLmTyYUsUDB6izZSEtupY6znBC5mo` | 6 |
| `2x4wPZePCbq2W9tFfP2bagXjXnysdqNWQWMtwGMoyPFv` | `JUPW3tHBxmNRzVnLmTyYUsUDB6izZSEtupY6znBC5mo` | 6 |
| `2sbhRE62pbi3sLo9CtjM7nYzUynEV4oBAPrGmQPrhnfF` | `HVKuqyK6wjexdVJAUARiGdQTdGBBWhdYyhCZGFXh9d4s` | 6 |
| `C8VeT16ySsyMW9xijjmYgvw83FfvEZVJawn5jgpzcf1X` | `HVKuqyK6wjexdVJAUARiGdQTdGBBWhdYyhCZGFXh9d4s` | 6 |
| `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` | `HVKuqyK6wjexdVJAUARiGdQTdGBBWhdYyhCZGFXh9d4s` | 6 |
| `HVKuqyK6wjexdVJAUARiGdQTdGBBWhdYyhCZGFXh9d4s` | `TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA` | 6 |
| `2sbhRE62pbi3sLo9CtjM7nYzUynEV4oBAPrGmQPrhnfF` | `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ` | 6 |
| `2sbhRE62pbi3sLo9CtjM7nYzUynEV4oBAPrGmQPrhnfF` | `C8VeT16ySsyMW9xijjmYgvw83FfvEZVJawn5jgpzcf1X` | 6 |
| `2sbhRE62pbi3sLo9CtjM7nYzUynEV4oBAPrGmQPrhnfF` | `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` | 6 |
| `2sbhRE62pbi3sLo9CtjM7nYzUynEV4oBAPrGmQPrhnfF` | `TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA` | 6 |
| `2sbhRE62pbi3sLo9CtjM7nYzUynEV4oBAPrGmQPrhnfF` | `2x4wPZePCbq2W9tFfP2bagXjXnysdqNWQWMtwGMoyPFv` | 6 |
| `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ` | `C8VeT16ySsyMW9xijjmYgvw83FfvEZVJawn5jgpzcf1X` | 6 |
| `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ` | `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` | 6 |
| `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ` | `TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA` | 6 |
| `C8VeT16ySsyMW9xijjmYgvw83FfvEZVJawn5jgpzcf1X` | `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` | 6 |
| `C8VeT16ySsyMW9xijjmYgvw83FfvEZVJawn5jgpzcf1X` | `TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA` | 6 |
| `2x4wPZePCbq2W9tFfP2bagXjXnysdqNWQWMtwGMoyPFv` | `C8VeT16ySsyMW9xijjmYgvw83FfvEZVJawn5jgpzcf1X` | 6 |

## Positional Account Layouts

### `sweep` `2817eaaf0e3d9ab1` raw length `52`

- Samples: `2`
- Signers: `JUPW3tHBxmNRzVnLmTyYUsUDB6izZSEtupY6znBC5mo` 4

| Position | Most common account(s) | Label hints |
|---:|---|---|
| 0 | `JUPW3tHBxmNRzVnLmTyYUsUDB6izZSEtupY6znBC5mo` 2 |  |
| 1 | `gum1UnP99NnohRt3YcdkA4PGubCYvtWiH8mgjT2KhXH` 1<br>`4rAgpDkj9iB2cN6BXdQu8Q26RKQaPuZSsDGcQHjCaqz7` 1 |  |
| 2 | `ECho1E2CXg3smpWVqjwpLpgv2A2KzKUeqXuTg9XyBr8R` 1<br>`63S6bZgc9Gky6uFv5g2FyNhwgqKZFKTr22gyT8nowz9b` 1 |  |
| 3 | `HPRQqnbrjnP8m5yu1ZG3sN4c16n7ne17iXuuCE2ACgU5` 1<br>`FZNvPAp875kXHS6Vpu2zJkLfZxp4QCEquTjdfYgXAeGB` 1 | `token account mint=EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v owner=ECho1E2CXg3smpWVqjwpLpgv2A2KzKUeqXuTg9XyBr8R` 1<br>`token account mint=EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v owner=63S6bZgc9Gky6uFv5g2FyNhwgqKZFKTr22gyT8nowz9b` 1 |
| 4 | `HVKuqyK6wjexdVJAUARiGdQTdGBBWhdYyhCZGFXh9d4s` 2 |  |
| 5 | `2sbhRE62pbi3sLo9CtjM7nYzUynEV4oBAPrGmQPrhnfF` 2 |  |
| 6 | `C8VeT16ySsyMW9xijjmYgvw83FfvEZVJawn5jgpzcf1X` 2 | `token account mint=EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v owner=2sbhRE62pbi3sLo9CtjM7nYzUynEV4oBAPrGmQPrhnfF` 2 |
| 7 | `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` 2 | `USDC mint` 2 |
| 8 | `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ` 2 | `Gum Bank Program executable` 2 |
| 9 | `5x38Kp4hvdomTCnCrAny4UtMUt5rQBdB6px2K1Ui45Wq` 2 |  |
| 10 | `JUPW3tHBxmNRzVnLmTyYUsUDB6izZSEtupY6znBC5mo` 2 |  |
| 11 | `TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA` 2 | `SPL Token program` 2 |
| 12 | `ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL` 2 |  |
| 13 | `11111111111111111111111111111111` 2 | `system program` 2 |
| 14 | `Sysvar1nstructions1111111111111111111111111` 2 | `instructions sysvar` 2 |
| 15 | `EG9fKpmLgkzCYZdj8uNDhHu5xmeXCZakccV6QmUavbzt` 2 |  |
| 16 | `9DvDdsw38EB3RPChPqHkgBmntFbM5v79QxMyMSbfXWuy` 2 |  |
| 17 | `JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw` 2 |  |
| 18 | `2x4wPZePCbq2W9tFfP2bagXjXnysdqNWQWMtwGMoyPFv` 2 |  |
| 19 | `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ` 2 | `Gum Bank Program executable` 2 |

### `verify_request` `891f2fe4cdea81ed` raw length `463`

- Samples: `2`
- Signers: `JUPW3tHBxmNRzVnLmTyYUsUDB6izZSEtupY6znBC5mo` 2

| Position | Most common account(s) | Label hints |
|---:|---|---|
| 0 | `JUPW3tHBxmNRzVnLmTyYUsUDB6izZSEtupY6znBC5mo` 2 |  |
| 1 | `7SnRzKKo8QonsMUb1wYCQoqCsLq2njp41yS33gJsVfp8` 1<br>`Cei4rumgr8ePPdNCMim7yo4C6idaMNv3N8P3qqQbbjyf` 1 |  |
| 2 | `HVKuqyK6wjexdVJAUARiGdQTdGBBWhdYyhCZGFXh9d4s` 2 |  |
| 3 | `3C1LxtpR3Mh5RQjydfeQdvRaAzpStWM7gBi1XzP9oyGt` 2 |  |
| 4 | `jnoUtncGR9ZCCMixtys6Gzy5coTo6mnmUZuEHRQFTFV` 2 |  |
| 5 | `11111111111111111111111111111111` 2 | `system program` 2 |
| 6 | `Sysvar1nstructions1111111111111111111111111` 2 | `instructions sysvar` 2 |
| 7 | `2x4wPZePCbq2W9tFfP2bagXjXnysdqNWQWMtwGMoyPFv` 2 |  |
| 8 | `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ` 2 | `Gum Bank Program executable` 2 |

### `withdraw` `b712469c946da122` raw length `8`

- Samples: `2`
- Signers: `JUPW3tHBxmNRzVnLmTyYUsUDB6izZSEtupY6znBC5mo` 4

| Position | Most common account(s) | Label hints |
|---:|---|---|
| 0 | `JUPW3tHBxmNRzVnLmTyYUsUDB6izZSEtupY6znBC5mo` 2 |  |
| 1 | `7SnRzKKo8QonsMUb1wYCQoqCsLq2njp41yS33gJsVfp8` 1<br>`Cei4rumgr8ePPdNCMim7yo4C6idaMNv3N8P3qqQbbjyf` 1 |  |
| 2 | `8NiTpug6V5SeWN42wwTGqUcKM3y6dCnRR6ouV7sf4Kak` 1<br>`ESLg5R1Ry4LXSfxh67BUPusKHeHGpaJWHGjTGeg6oYGE` 1 |  |
| 3 | `HVKuqyK6wjexdVJAUARiGdQTdGBBWhdYyhCZGFXh9d4s` 2 |  |
| 4 | `2sbhRE62pbi3sLo9CtjM7nYzUynEV4oBAPrGmQPrhnfF` 2 |  |
| 5 | `7jqXWdiyYkY9XUStYhbGzSgn1VCr9tMF4LNCK52oG76U` 2 |  |
| 6 | `5RD1PyMjzgo3gMCToQTnqk44L99kQZ3MnGnRzxMwRwLj` 2 | `token account mint=EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v owner=7jqXWdiyYkY9XUStYhbGzSgn1VCr9tMF4LNCK52oG76U` 2 |
| 7 | `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ` 2 | `Gum Bank Program executable` 2 |
| 8 | `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ` 2 | `Gum Bank Program executable` 2 |
| 9 | `C8VeT16ySsyMW9xijjmYgvw83FfvEZVJawn5jgpzcf1X` 2 | `token account mint=EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v owner=2sbhRE62pbi3sLo9CtjM7nYzUynEV4oBAPrGmQPrhnfF` 2 |
| 10 | `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` 2 | `USDC mint` 2 |
| 11 | `TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA` 2 | `SPL Token program` 2 |
| 12 | `ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL` 2 |  |
| 13 | `11111111111111111111111111111111` 2 | `system program` 2 |
| 14 | `EG9fKpmLgkzCYZdj8uNDhHu5xmeXCZakccV6QmUavbzt` 2 |  |
| 15 | `9DvDdsw38EB3RPChPqHkgBmntFbM5v79QxMyMSbfXWuy` 2 |  |
| 16 | `JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw` 2 |  |
| 17 | `JUPW3tHBxmNRzVnLmTyYUsUDB6izZSEtupY6znBC5mo` 2 |  |
| 18 | `2x4wPZePCbq2W9tFfP2bagXjXnysdqNWQWMtwGMoyPFv` 2 |  |
| 19 | `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ` 2 | `Gum Bank Program executable` 2 |

### `rfq_sell_resolve` `14a2fae36fc17bec` raw length `17`

- Samples: `1`
- Signers: `rfQMFpNueeNufBW4byyEAhvL4To4tCsVBVagcEWG8ea` 2

| Position | Most common account(s) | Label hints |
|---:|---|---|
| 0 | `rfQMFpNueeNufBW4byyEAhvL4To4tCsVBVagcEWG8ea` 1 |  |
| 1 | `H5Y5aLdTQXRWJ6kitWeUkHyAEVLPPfChgSxhUBVxZ3D2` 1 |  |
| 2 | `rfQMFpNueeNufBW4byyEAhvL4To4tCsVBVagcEWG8ea` 1 |  |
| 3 | `4s3gnkf1R2UzAWbfvVowfaW7VdLDNSQhmwjYcSnMYwmT` 1 |  |
| 4 | `HVKuqyK6wjexdVJAUARiGdQTdGBBWhdYyhCZGFXh9d4s` 1 |  |
| 5 | `2sbhRE62pbi3sLo9CtjM7nYzUynEV4oBAPrGmQPrhnfF` 1 |  |
| 6 | `GqpFMhoHzfhUnM65kvCRkzozm4c72A9TpNZzt9D69z88` 1 | `token account mint=So11111111111111111111111111111111111111112 owner=2sbhRE62pbi3sLo9CtjM7nYzUynEV4oBAPrGmQPrhnfF` 1 |
| 7 | `So11111111111111111111111111111111111111112` 1 | `wrapped SOL mint` 1 |
| 8 | `TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA` 1 | `SPL Token program` 1 |
| 9 | `C8VeT16ySsyMW9xijjmYgvw83FfvEZVJawn5jgpzcf1X` 1 | `token account mint=EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v owner=2sbhRE62pbi3sLo9CtjM7nYzUynEV4oBAPrGmQPrhnfF` 1 |
| 10 | `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` 1 | `USDC mint` 1 |
| 11 | `TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA` 1 | `SPL Token program` 1 |
| 12 | `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ` 1 | `Gum Bank Program executable` 1 |
| 13 | `5DtSBy1imR7W2Zbdt9Z1gfRPVmVZyTVorvi562SZ7bvd` 1 | `token account mint=EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v owner=rfQMFpNueeNufBW4byyEAhvL4To4tCsVBVagcEWG8ea` 1 |
| 14 | `5x38Kp4hvdomTCnCrAny4UtMUt5rQBdB6px2K1Ui45Wq` 1 |  |
| 15 | `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ` 1 | `Gum Bank Program executable` 1 |
| 16 | `EG9fKpmLgkzCYZdj8uNDhHu5xmeXCZakccV6QmUavbzt` 1 |  |
| 17 | `9DvDdsw38EB3RPChPqHkgBmntFbM5v79QxMyMSbfXWuy` 1 |  |
| 18 | `JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw` 1 |  |
| 19 | `2x4wPZePCbq2W9tFfP2bagXjXnysdqNWQWMtwGMoyPFv` 1 |  |
| 20 | `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ` 1 | `Gum Bank Program executable` 1 |

### `rfq_sell_commit` `9ce6d1a96eebde14` raw length `8`

- Samples: `1`
- Signers: `rfQMFpNueeNufBW4byyEAhvL4To4tCsVBVagcEWG8ea` 1

| Position | Most common account(s) | Label hints |
|---:|---|---|
| 0 | `rfQMFpNueeNufBW4byyEAhvL4To4tCsVBVagcEWG8ea` 1 |  |
| 1 | `H5Y5aLdTQXRWJ6kitWeUkHyAEVLPPfChgSxhUBVxZ3D2` 1 |  |
| 2 | `4s3gnkf1R2UzAWbfvVowfaW7VdLDNSQhmwjYcSnMYwmT` 1 |  |
| 3 | `HVKuqyK6wjexdVJAUARiGdQTdGBBWhdYyhCZGFXh9d4s` 1 |  |
| 4 | `2sbhRE62pbi3sLo9CtjM7nYzUynEV4oBAPrGmQPrhnfF` 1 |  |
| 5 | `GqpFMhoHzfhUnM65kvCRkzozm4c72A9TpNZzt9D69z88` 1 | `token account mint=So11111111111111111111111111111111111111112 owner=2sbhRE62pbi3sLo9CtjM7nYzUynEV4oBAPrGmQPrhnfF` 1 |
| 6 | `So11111111111111111111111111111111111111112` 1 | `wrapped SOL mint` 1 |
| 7 | `TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA` 1 | `SPL Token program` 1 |
| 8 | `C8VeT16ySsyMW9xijjmYgvw83FfvEZVJawn5jgpzcf1X` 1 | `token account mint=EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v owner=2sbhRE62pbi3sLo9CtjM7nYzUynEV4oBAPrGmQPrhnfF` 1 |
| 9 | `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` 1 | `USDC mint` 1 |
| 10 | `TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA` 1 | `SPL Token program` 1 |
| 11 | `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ` 1 | `Gum Bank Program executable` 1 |
| 12 | `ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL` 1 |  |
| 13 | `11111111111111111111111111111111` 1 | `system program` 1 |
| 14 | `DnM9teVNbi4Cebkqtar3sVJs9LcZWSrV8DhwQzPpSeqM` 1 | `token account mint=So11111111111111111111111111111111111111112 owner=rfQMFpNueeNufBW4byyEAhvL4To4tCsVBVagcEWG8ea` 1 |
| 15 | `5DtSBy1imR7W2Zbdt9Z1gfRPVmVZyTVorvi562SZ7bvd` 1 | `token account mint=EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v owner=rfQMFpNueeNufBW4byyEAhvL4To4tCsVBVagcEWG8ea` 1 |
| 16 | `2x4wPZePCbq2W9tFfP2bagXjXnysdqNWQWMtwGMoyPFv` 1 |  |
| 17 | `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ` 1 | `Gum Bank Program executable` 1 |

## Payload Shape Hints

### `sweep` `2817eaaf0e3d9ab1` raw length `52`

- Samples: `2`
- Printable payload strings: offset `28` text `USD Coin` count `2`<br>offset `40` text `USDC` count `2`
- Stable aligned u32 candidates: offset `24` value `8`<br>offset `28` value `541348693`<br>offset `36` value `4`
- Stable aligned u64 candidates: offset `8` value `1000000000`<br>offset `16` value `1000000000`<br>offset `32` value `19032272707`
- Embedded known pubkey candidates: `None`

### `verify_request` `891f2fe4cdea81ed` raw length `463`

- Samples: `2`
- Printable payload strings: offset `34` text `2#:\` count `2`<br>offset `115` text `E/]a` count `2`<br>offset `200` text `K@_N0` count `2`<br>offset `320` text `Tzxg` count `2`<br>offset `331` text `R,}R` count `2`<br>offset `338` text `"~>6` count `2`<br>offset `362` text `BEB:` count `2`<br>offset `252` text `,@%(M` count `1`
- Stable aligned u32 candidates: offset `0` value `179`<br>offset `4` value `1`<br>offset `8` value `50331648`<br>offset `20` value `543805506`<br>offset `32` value `590521643`<br>offset `116` value `6380847`<br>offset `156` value `710710176`<br>offset `172` value `389446767`<br>offset `180` value `233671998`<br>offset `184` value `1`<br>offset `196` value `251080961`<br>offset `204` value `574540336`
- Stable aligned u64 candidates: offset `0` value `4294967475`
- Embedded known pubkey candidates: offset `13` `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ`<br>offset `87` `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v`

### `withdraw` `b712469c946da122` raw length `8`

- Samples: `2`
- Printable payload strings: `None`
- Stable aligned u32 candidates: `None`
- Stable aligned u64 candidates: `None`
- Embedded known pubkey candidates: `None`

### `rfq_sell_resolve` `14a2fae36fc17bec` raw length `17`

- Samples: `1`
- Printable payload strings: `None`
- Stable aligned u32 candidates: offset `0` value `29767681`
- Stable aligned u64 candidates: offset `0` value `29767681`
- Embedded known pubkey candidates: `None`

### `rfq_sell_commit` `9ce6d1a96eebde14` raw length `8`

- Samples: `1`
- Printable payload strings: `None`
- Stable aligned u32 candidates: `None`
- Stable aligned u64 candidates: `None`
- Embedded known pubkey candidates: `None`

## PDA Seed Hunt

| Program | Seeds | Derived observed account |
|---|---|---|
| `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ` | `__inbox_event_auth` | `EG9fKpmLgkzCYZdj8uNDhHu5xmeXCZakccV6QmUavbzt` |

## Assessment

- The account graph shows stable protocol plumbing accounts across variants, especially the repeated Bank Program executable, inbox/outbox-adjacent accounts, SPL Token, system program and instructions sysvar.
- `sweep` carries asset metadata strings in its payload; in the sampled data those strings identify USDC, not JUP.
- `verify_request` has a large mostly binary payload consistent with proof/message verification data, but this report does not decode it into a trusted ABI.
- The bounded PDA search did not expose a canonical JUP-derived PDA or a simple `JUPNET_INBOX`/Merkle seed account in the observed account set.
- This adds negative evidence against visible JUP-denominated security in the sampled Bank path, while strengthening the cross-chain request/proof interpretation.
