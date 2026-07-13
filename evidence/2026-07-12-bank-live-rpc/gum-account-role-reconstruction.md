# Gum Account Role Reconstruction

## Scope

- Direct JupNet Gum `brhPf...` instructions decoded: `8`
- Direct Solana Bank instructions decoded: `17`
- Direct sampled top-level `GUMeb...` instructions: `0`
- Inner verifier payload sender/program ids: `GUMebNDCYyF81xjyqaHagbgMQVUTb8fBC9YRh25xSH64: 11`
- Account-meta canonical JUP hits: `0`
- Account-meta current validator/vote/stake hits: `0`

## High-Confidence Account Roles

| Account / role | Observations |
|---|---:|
| `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ => Solana Gum Bank Program executable` | 26 |
| `11111111111111111111111111111111 => system program` | 23 |
| `brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1 => JupNet Gum omnichain executable brhPf` | 16 |
| `HVKuqyK6wjexdVJAUARiGdQTdGBBWhdYyhCZGFXh9d4s => Bank state/config candidate` | 16 |
| `JUPW3tHBxmNRzVnLmTyYUsUDB6izZSEtupY6znBC5mo => payer/signer` | 15 |
| `2x4wPZePCbq2W9tFfP2bagXjXnysdqNWQWMtwGMoyPFv => request/account state candidate` | 15 |
| `Sysvar1nstructions1111111111111111111111111 => instructions sysvar` | 13 |
| `3C1LxtpR3Mh5RQjydfeQdvRaAzpStWM7gBi1XzP9oyGt => outbox Merkle root-history account` | 11 |
| `jnoUtncGR9ZCCMixtys6Gzy5coTo6mnmUZuEHRQFTFV => JupNet outbox helper program` | 11 |
| `GUMebNDCYyF81xjyqaHagbgMQVUTb8fBC9YRh25xSH64 => verifier payload sender/program id` | 11 |
| `E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9 => Gum upgrade/admin authority` | 9 |
| `TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA => SPL Token program` | 8 |
| `Hso4y8rKEXUUvMbxnyDmjCxA7yk1wbVsZNHSGXcDEUyU => JupNet Gum-owned account` | 7 |
| `ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL => Associated Token program` | 6 |
| `C8VeT16ySsyMW9xijjmYgvw83FfvEZVJawn5jgpzcf1X => token account mint=EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v owner=2sbhRE62pbi3sLo9CtjM7nYzUynEV4oBAPrGmQPrhnfF` | 6 |
| `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v => USDC mint` | 6 |
| `ESUtymMEp6NULmLBcREaumM87TRpgt5R4eNYVrKjCKQq => candidate created/managed account` | 5 |
| `76WKTLzujFUnj7TyB7CqLywPE3YZQf4Fmxj9SwcFAJrY => JupNet Gum-owned account` | 5 |
| `EG9fKpmLgkzCYZdj8uNDhHu5xmeXCZakccV6QmUavbzt => Bank __inbox_event_auth PDA` | 5 |
| `9DvDdsw38EB3RPChPqHkgBmntFbM5v79QxMyMSbfXWuy => inbox helper state/counter account` | 5 |
| `JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw => JupNet inbox helper program` | 5 |
| `Fh54LKACZCzo3GzDcxoPQomTZamBsFy6XLbj15zJP1WH => JupNet Gum-owned account` | 3 |
| `GZF3sfYF27BU83fd5BPgB419SZiLLZPty3qL6465JTp6 => JupNet Gum-owned account` | 2 |
| `FCNefQTEYCsPyQA64hdCpekucCDJFPHm2qfwg8F61jgc => token account mint=A5ER4hbDN82jEnf986kZzuJzMzsyw1DRqodnone5yJWo owner=Fh54LKACZCzo3GzDcxoPQomTZamBsFy6XLbj15zJP1WH` | 2 |
| `Tokenis9xgQh7yMRbNBnV6uFq7LANbuZJwebxWBWixf => token program` | 2 |
| `2sbhRE62pbi3sLo9CtjM7nYzUynEV4oBAPrGmQPrhnfF => recipient/authority candidate` | 2 |
| `5RD1PyMjzgo3gMCToQTnqk44L99kQZ3MnGnRzxMwRwLj => token account mint=EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v owner=7jqXWdiyYkY9XUStYhbGzSgn1VCr9tMF4LNCK52oG76U` | 2 |
| `rfQMFpNueeNufBW4byyEAhvL4To4tCsVBVagcEWG8ea => payer/signer` | 2 |
| `GqpFMhoHzfhUnM65kvCRkzozm4c72A9TpNZzt9D69z88 => token account mint=So11111111111111111111111111111111111111112 owner=2sbhRE62pbi3sLo9CtjM7nYzUynEV4oBAPrGmQPrhnfF` | 2 |
| `So11111111111111111111111111111111111111112 => wrapped SOL mint` | 2 |
| `5DtSBy1imR7W2Zbdt9Z1gfRPVmVZyTVorvi562SZ7bvd => token account mint=EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v owner=rfQMFpNueeNufBW4byyEAhvL4To4tCsVBVagcEWG8ea` | 2 |
| `2VL6frjfzZN8qSqMVjQosJP213uetibbzxtMsGgBZvkv => token account mint=A5ER4hbDN82jEnf986kZzuJzMzsyw1DRqodnone5yJWo owner=feesWdbbRKoP8s1vTpEL1Pw5RNNFHAaK7rntKrifJN4` | 1 |
| `94oZZEp1p1Vwuvc7axgeaRSU4Mk9diugqzjxpz1dnSZv => secondary signer/payer` | 1 |
| `3TsVLe3ZxEU9vhini76zkNZpRmd1xxygVQxH8obAhsmz => token account mint=A5ER4hbDN82jEnf986kZzuJzMzsyw1DRqodnone5yJWo owner=94oZZEp1p1Vwuvc7axgeaRSU4Mk9diugqzjxpz1dnSZv` | 1 |
| `4s3gnkf1R2UzAWbfvVowfaW7VdLDNSQhmwjYcSnMYwmT => Bank-owned compact state candidate` | 1 |
| `HPRQqnbrjnP8m5yu1ZG3sN4c16n7ne17iXuuCE2ACgU5 => token account mint=EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v owner=ECho1E2CXg3smpWVqjwpLpgv2A2KzKUeqXuTg9XyBr8R` | 1 |
| `FZNvPAp875kXHS6Vpu2zJkLfZxp4QCEquTjdfYgXAeGB => token account mint=EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v owner=63S6bZgc9Gky6uFv5g2FyNhwgqKZFKTr22gyT8nowz9b` | 1 |
| `HVKuqyK6wjexdVJAUARiGdQTdGBBWhdYyhCZGFXh9d4s => Bank-owned compact state candidate` | 1 |
| `2sbhRE62pbi3sLo9CtjM7nYzUynEV4oBAPrGmQPrhnfF => Bank state/config candidate` | 1 |
| `DnM9teVNbi4Cebkqtar3sVJs9LcZWSrV8DhwQzPpSeqM => token account mint=So11111111111111111111111111111111111111112 owner=rfQMFpNueeNufBW4byyEAhvL4To4tCsVBVagcEWG8ea` | 1 |

## Direct JupNet Gum Account Positions

| Variant | Raw len | Samples |
|---|---:|---:|
| `1202` | 2 | 5 |
| `0184030000781177` | 244 | 1 |
| `0020000000633166` | 187 | 1 |
| `0a` | 1 | 1 |

### `1202` raw len `2`

| Pos | Signer | Writable | Common accounts | Role labels | Inferred role |
|---:|---:|---:|---|---|---|
| 0 | 0 | 5 | `ESUtymMEp6NULmLBcREaumM87TRpgt5R4eNYVrKjCKQq: 5` | `None` | `candidate created/managed account: 5` |
| 1 | 5 | 5 | `E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9: 5` | `Gum upgrade/admin authority: 5` | `admin/upgrade authority signer: 5` |
| 2 | 0 | 5 | `76WKTLzujFUnj7TyB7CqLywPE3YZQf4Fmxj9SwcFAJrY: 5` | `JupNet Gum-owned account: 5` | `Gum-owned config/state account: 5` |
| 3 | 0 | 0 | `brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1: 5` | `JupNet Gum omnichain executable brhPf: 5` | `None` |
| 4 | 0 | 0 | `11111111111111111111111111111111: 5` | `system program: 5` | `system program: 5` |
| 5 | 0 | 0 | `brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1: 5` | `JupNet Gum omnichain executable brhPf: 5` | `None` |
| 6 | 0 | 0 | `Hso4y8rKEXUUvMbxnyDmjCxA7yk1wbVsZNHSGXcDEUyU: 5` | `JupNet Gum-owned account: 5` | `candidate chain_config or readonly Gum config: 5` |
| 7 | 0 | 0 | `brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1: 5` | `JupNet Gum omnichain executable brhPf: 5` | `None` |

### `0184030000781177` raw len `244`

| Pos | Signer | Writable | Common accounts | Role labels | Inferred role |
|---:|---:|---:|---|---|---|
| 0 | 1 | 1 | `E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9: 1` | `Gum upgrade/admin authority: 1` | `admin/upgrade authority signer: 1` |
| 1 | 1 | 1 | `E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9: 1` | `Gum upgrade/admin authority: 1` | `admin/upgrade authority signer: 1` |
| 2 | 0 | 1 | `Fh54LKACZCzo3GzDcxoPQomTZamBsFy6XLbj15zJP1WH: 1` | `JupNet Gum-owned account: 1` | `Gum-owned mint/config state: 1` |
| 3 | 0 | 0 | `94oZZEp1p1Vwuvc7axgeaRSU4Mk9diugqzjxpz1dnSZv: 1` | `None` | `None` |
| 4 | 0 | 1 | `9tQb7MwoU2BubmX24nzDtdVBn2dQGSuSDUGAPuv6sabb: 1` | `None` | `None` |
| 5 | 0 | 1 | `CFwUkiwnHWsiqJCaVoX9SH3yAGfrbHWJygAxRVECejH3: 1` | `None` | `None` |
| 6 | 0 | 1 | `J7CzJ45sTMD5Bwc9Xo9cRVbtuR7fng6GBppqfbqitjxm: 1` | `None` | `None` |
| 7 | 0 | 1 | `GZF3sfYF27BU83fd5BPgB419SZiLLZPty3qL6465JTp6: 1` | `JupNet Gum-owned account: 1` | `None` |
| 8 | 0 | 1 | `5nPsQ5HnUuykL1VjR5AhzE847Ch61zY2U12F6Ft9oKML: 1` | `None` | `None` |
| 9 | 0 | 1 | `3rsSjn9vH779W23fofF4jxJcpsDCTdN5Hm9MPqKwMMUW: 1` | `None` | `None` |
| 10 | 0 | 1 | `A5ER4hbDN82jEnf986kZzuJzMzsyw1DRqodnone5yJWo: 1` | `None` | `None` |
| 11 | 0 | 1 | `FCNefQTEYCsPyQA64hdCpekucCDJFPHm2qfwg8F61jgc: 1` | `token account mint=A5ER4hbDN82jEnf986kZzuJzMzsyw1DRqodnone5yJWo owner=Fh54LKACZCzo3GzDcxoPQomTZamBsFy6XLbj15zJP1WH: 1` | `None` |
| 12 | 0 | 1 | `2VL6frjfzZN8qSqMVjQosJP213uetibbzxtMsGgBZvkv: 1` | `token account mint=A5ER4hbDN82jEnf986kZzuJzMzsyw1DRqodnone5yJWo owner=feesWdbbRKoP8s1vTpEL1Pw5RNNFHAaK7rntKrifJN4: 1` | `None` |
| 13 | 0 | 0 | `Hso4y8rKEXUUvMbxnyDmjCxA7yk1wbVsZNHSGXcDEUyU: 1` | `JupNet Gum-owned account: 1` | `candidate chain_config or readonly Gum config: 1` |
| 14 | 0 | 0 | `Tokenis9xgQh7yMRbNBnV6uFq7LANbuZJwebxWBWixf: 1` | `None` | `token program: 1` |
| 15 | 0 | 0 | `11111111111111111111111111111111: 1` | `system program: 1` | `system program: 1` |
| 16 | 0 | 0 | `ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL: 1` | `Associated Token program: 1` | `associated token program: 1` |

### `0020000000633166` raw len `187`

| Pos | Signer | Writable | Common accounts | Role labels | Inferred role |
|---:|---:|---:|---|---|---|
| 0 | 1 | 1 | `E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9: 1` | `Gum upgrade/admin authority: 1` | `admin/upgrade authority signer: 1` |
| 1 | 1 | 1 | `94oZZEp1p1Vwuvc7axgeaRSU4Mk9diugqzjxpz1dnSZv: 1` | `None` | `secondary signer/payer: 1` |
| 2 | 0 | 1 | `Fh54LKACZCzo3GzDcxoPQomTZamBsFy6XLbj15zJP1WH: 1` | `JupNet Gum-owned account: 1` | `Gum-owned mint/config state: 1` |
| 3 | 0 | 0 | `GZF3sfYF27BU83fd5BPgB419SZiLLZPty3qL6465JTp6: 1` | `JupNet Gum-owned account: 1` | `Gum-owned state: 1` |
| 4 | 0 | 1 | `A5ER4hbDN82jEnf986kZzuJzMzsyw1DRqodnone5yJWo: 1` | `None` | `None` |
| 5 | 0 | 1 | `3TsVLe3ZxEU9vhini76zkNZpRmd1xxygVQxH8obAhsmz: 1` | `token account mint=A5ER4hbDN82jEnf986kZzuJzMzsyw1DRqodnone5yJWo owner=94oZZEp1p1Vwuvc7axgeaRSU4Mk9diugqzjxpz1dnSZv: 1` | `None` |
| 6 | 0 | 1 | `FCNefQTEYCsPyQA64hdCpekucCDJFPHm2qfwg8F61jgc: 1` | `token account mint=A5ER4hbDN82jEnf986kZzuJzMzsyw1DRqodnone5yJWo owner=Fh54LKACZCzo3GzDcxoPQomTZamBsFy6XLbj15zJP1WH: 1` | `None` |
| 7 | 0 | 0 | `Hso4y8rKEXUUvMbxnyDmjCxA7yk1wbVsZNHSGXcDEUyU: 1` | `JupNet Gum-owned account: 1` | `candidate chain_config or readonly Gum config: 1` |
| 8 | 0 | 0 | `Tokenis9xgQh7yMRbNBnV6uFq7LANbuZJwebxWBWixf: 1` | `None` | `token program: 1` |
| 9 | 0 | 0 | `11111111111111111111111111111111: 1` | `system program: 1` | `system program: 1` |

### `0a` raw len `1`

| Pos | Signer | Writable | Common accounts | Role labels | Inferred role |
|---:|---:|---:|---|---|---|
| 0 | 1 | 1 | `E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9: 1` | `Gum upgrade/admin authority: 1` | `admin/upgrade authority signer: 1` |
| 1 | 0 | 0 | `Fh54LKACZCzo3GzDcxoPQomTZamBsFy6XLbj15zJP1WH: 1` | `JupNet Gum-owned account: 1` | `Gum-owned config/state account: 1` |
| 2 | 0 | 0 | `brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1: 1` | `JupNet Gum omnichain executable brhPf: 1` | `program id self-reference: 1` |

## Solana Bank Account Positions

| Variant | Raw len | Samples |
|---|---:|---:|
| `verify_request` | 463 | 6 |
| `verify_request` | 496 | 5 |
| `withdraw` | 8 | 2 |
| `sweep` | 52 | 2 |
| `rfq_sell_resolve` | 17 | 1 |
| `rfq_sell_commit` | 8 | 1 |

### `verify_request` raw len `463`

| Pos | Signer | Writable | Common accounts | Role labels | Inferred role |
|---:|---:|---:|---|---|---|
| 0 | 6 | 6 | `JUPW3tHBxmNRzVnLmTyYUsUDB6izZSEtupY6znBC5mo: 6` | `None` | `payer/signer: 6` |
| 1 | 0 | 6 | `7SnRzKKo8QonsMUb1wYCQoqCsLq2njp41yS33gJsVfp8: 1`<br>`Cei4rumgr8ePPdNCMim7yo4C6idaMNv3N8P3qqQbbjyf: 1`<br>`JAx8oX7aqF5arRsLMgYJuHXziEZP8HkhbUuNvMLtnJC7: 1`<br>`3MDjM5pU8mULSUyDdJrokc13zWDJCWGRUPWjDXNKLNQe: 1` | `None` | `None` |
| 2 | 0 | 0 | `HVKuqyK6wjexdVJAUARiGdQTdGBBWhdYyhCZGFXh9d4s: 6` | `None` | `Bank state/config candidate: 6` |
| 3 | 0 | 0 | `3C1LxtpR3Mh5RQjydfeQdvRaAzpStWM7gBi1XzP9oyGt: 6` | `outbox Merkle root-history account: 6` | `outbox Merkle root-history account: 6` |
| 4 | 0 | 0 | `jnoUtncGR9ZCCMixtys6Gzy5coTo6mnmUZuEHRQFTFV: 6` | `JupNet outbox helper program: 6` | `outbox helper program: 6` |
| 5 | 0 | 0 | `11111111111111111111111111111111: 6` | `system program: 6` | `system program: 6` |
| 6 | 0 | 0 | `Sysvar1nstructions1111111111111111111111111: 6` | `instructions sysvar: 6` | `instructions sysvar: 6` |
| 7 | 0 | 0 | `2x4wPZePCbq2W9tFfP2bagXjXnysdqNWQWMtwGMoyPFv: 6` | `None` | `request/account state candidate: 6` |
| 8 | 0 | 0 | `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ: 6` | `Solana Gum Bank Program executable: 6` | `Bank Program executable: 6` |

### `verify_request` raw len `496`

| Pos | Signer | Writable | Common accounts | Role labels | Inferred role |
|---:|---:|---:|---|---|---|
| 0 | 5 | 5 | `JUPW3tHBxmNRzVnLmTyYUsUDB6izZSEtupY6znBC5mo: 5` | `None` | `payer/signer: 5` |
| 1 | 0 | 5 | `C7MGCL4pxxYP7egxQ8EWKvUDTpAtbmrSRhGgedMWd1yd: 1`<br>`GYiaXrqtQackSySRWcgbef1PT4sJizrvmJeXJKkmZAFr: 1`<br>`4qUazTEKmYiDzWt425cpqiuzjjRfz7quPtNVEX2LPtUy: 1`<br>`E9SzMKyfH6d7WmHBA3FS5dKuHQfcW1nTAEVLRnJgWvXM: 1` | `None` | `None` |
| 2 | 0 | 0 | `HVKuqyK6wjexdVJAUARiGdQTdGBBWhdYyhCZGFXh9d4s: 5` | `None` | `Bank state/config candidate: 5` |
| 3 | 0 | 0 | `3C1LxtpR3Mh5RQjydfeQdvRaAzpStWM7gBi1XzP9oyGt: 5` | `outbox Merkle root-history account: 5` | `outbox Merkle root-history account: 5` |
| 4 | 0 | 0 | `jnoUtncGR9ZCCMixtys6Gzy5coTo6mnmUZuEHRQFTFV: 5` | `JupNet outbox helper program: 5` | `outbox helper program: 5` |
| 5 | 0 | 0 | `11111111111111111111111111111111: 5` | `system program: 5` | `system program: 5` |
| 6 | 0 | 0 | `Sysvar1nstructions1111111111111111111111111: 5` | `instructions sysvar: 5` | `instructions sysvar: 5` |
| 7 | 0 | 0 | `2x4wPZePCbq2W9tFfP2bagXjXnysdqNWQWMtwGMoyPFv: 5` | `None` | `request/account state candidate: 5` |
| 8 | 0 | 0 | `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ: 5` | `Solana Gum Bank Program executable: 5` | `Bank Program executable: 5` |

### `withdraw` raw len `8`

| Pos | Signer | Writable | Common accounts | Role labels | Inferred role |
|---:|---:|---:|---|---|---|
| 0 | 2 | 2 | `JUPW3tHBxmNRzVnLmTyYUsUDB6izZSEtupY6znBC5mo: 2` | `None` | `payer/signer: 2` |
| 1 | 0 | 2 | `7SnRzKKo8QonsMUb1wYCQoqCsLq2njp41yS33gJsVfp8: 1`<br>`Cei4rumgr8ePPdNCMim7yo4C6idaMNv3N8P3qqQbbjyf: 1` | `None` | `None` |
| 2 | 0 | 2 | `8NiTpug6V5SeWN42wwTGqUcKM3y6dCnRR6ouV7sf4Kak: 1`<br>`ESLg5R1Ry4LXSfxh67BUPusKHeHGpaJWHGjTGeg6oYGE: 1` | `None` | `None` |
| 3 | 0 | 0 | `HVKuqyK6wjexdVJAUARiGdQTdGBBWhdYyhCZGFXh9d4s: 2` | `None` | `Bank state/config candidate: 2` |
| 4 | 0 | 0 | `2sbhRE62pbi3sLo9CtjM7nYzUynEV4oBAPrGmQPrhnfF: 2` | `None` | `recipient/authority candidate: 2` |
| 5 | 0 | 2 | `7jqXWdiyYkY9XUStYhbGzSgn1VCr9tMF4LNCK52oG76U: 2` | `None` | `None` |
| 6 | 0 | 2 | `5RD1PyMjzgo3gMCToQTnqk44L99kQZ3MnGnRzxMwRwLj: 2` | `token account mint=EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v owner=7jqXWdiyYkY9XUStYhbGzSgn1VCr9tMF4LNCK52oG76U: 2` | `destination token account: 2` |
| 7 | 0 | 0 | `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ: 2` | `Solana Gum Bank Program executable: 2` | `None` |
| 8 | 0 | 0 | `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ: 2` | `Solana Gum Bank Program executable: 2` | `None` |
| 9 | 0 | 2 | `C8VeT16ySsyMW9xijjmYgvw83FfvEZVJawn5jgpzcf1X: 2` | `token account mint=EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v owner=2sbhRE62pbi3sLo9CtjM7nYzUynEV4oBAPrGmQPrhnfF: 2` | `source token account: 2` |
| 10 | 0 | 0 | `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v: 2` | `USDC mint: 2` | `token mint: 2` |
| 11 | 0 | 0 | `TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA: 2` | `SPL Token program: 2` | `token program: 2` |
| 12 | 0 | 0 | `ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL: 2` | `Associated Token program: 2` | `None` |
| 13 | 0 | 0 | `11111111111111111111111111111111: 2` | `system program: 2` | `None` |
| 14 | 0 | 0 | `EG9fKpmLgkzCYZdj8uNDhHu5xmeXCZakccV6QmUavbzt: 2` | `Bank __inbox_event_auth PDA: 2` | `Bank inbox event authority PDA: 2` |
| 15 | 0 | 2 | `9DvDdsw38EB3RPChPqHkgBmntFbM5v79QxMyMSbfXWuy: 2` | `inbox helper state/counter account: 2` | `inbox state/counter account: 2` |
| 16 | 0 | 0 | `JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw: 2` | `JupNet inbox helper program: 2` | `inbox helper program: 2` |
| 17 | 2 | 2 | `JUPW3tHBxmNRzVnLmTyYUsUDB6izZSEtupY6znBC5mo: 2` | `None` | `None` |
| 18 | 0 | 0 | `2x4wPZePCbq2W9tFfP2bagXjXnysdqNWQWMtwGMoyPFv: 2` | `None` | `request/account state candidate: 2` |
| 19 | 0 | 0 | `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ: 2` | `Solana Gum Bank Program executable: 2` | `None` |

### `sweep` raw len `52`

| Pos | Signer | Writable | Common accounts | Role labels | Inferred role |
|---:|---:|---:|---|---|---|
| 0 | 2 | 2 | `JUPW3tHBxmNRzVnLmTyYUsUDB6izZSEtupY6znBC5mo: 2` | `None` | `payer/signer: 2` |
| 1 | 0 | 0 | `gum1UnP99NnohRt3YcdkA4PGubCYvtWiH8mgjT2KhXH: 1`<br>`4rAgpDkj9iB2cN6BXdQu8Q26RKQaPuZSsDGcQHjCaqz7: 1` | `None` | `None` |
| 2 | 0 | 2 | `ECho1E2CXg3smpWVqjwpLpgv2A2KzKUeqXuTg9XyBr8R: 1`<br>`63S6bZgc9Gky6uFv5g2FyNhwgqKZFKTr22gyT8nowz9b: 1` | `None` | `None` |
| 3 | 0 | 2 | `HPRQqnbrjnP8m5yu1ZG3sN4c16n7ne17iXuuCE2ACgU5: 1`<br>`FZNvPAp875kXHS6Vpu2zJkLfZxp4QCEquTjdfYgXAeGB: 1` | `token account mint=EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v owner=ECho1E2CXg3smpWVqjwpLpgv2A2KzKUeqXuTg9XyBr8R: 1`<br>`token account mint=EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v owner=63S6bZgc9Gky6uFv5g2FyNhwgqKZFKTr22gyT8nowz9b: 1` | `None` |
| 4 | 0 | 0 | `HVKuqyK6wjexdVJAUARiGdQTdGBBWhdYyhCZGFXh9d4s: 2` | `None` | `Bank state/config candidate: 2` |
| 5 | 0 | 0 | `2sbhRE62pbi3sLo9CtjM7nYzUynEV4oBAPrGmQPrhnfF: 2` | `None` | `None` |
| 6 | 0 | 2 | `C8VeT16ySsyMW9xijjmYgvw83FfvEZVJawn5jgpzcf1X: 2` | `token account mint=EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v owner=2sbhRE62pbi3sLo9CtjM7nYzUynEV4oBAPrGmQPrhnfF: 2` | `destination token account: 2` |
| 7 | 0 | 0 | `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v: 2` | `USDC mint: 2` | `token mint: 2` |
| 8 | 0 | 0 | `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ: 2` | `Solana Gum Bank Program executable: 2` | `Bank Program executable: 2` |
| 9 | 0 | 0 | `5x38Kp4hvdomTCnCrAny4UtMUt5rQBdB6px2K1Ui45Wq: 2` | `None` | `None` |
| 10 | 2 | 2 | `JUPW3tHBxmNRzVnLmTyYUsUDB6izZSEtupY6znBC5mo: 2` | `None` | `None` |
| 11 | 0 | 0 | `TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA: 2` | `SPL Token program: 2` | `token program: 2` |
| 12 | 0 | 0 | `ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL: 2` | `Associated Token program: 2` | `None` |
| 13 | 0 | 0 | `11111111111111111111111111111111: 2` | `system program: 2` | `None` |
| 14 | 0 | 0 | `Sysvar1nstructions1111111111111111111111111: 2` | `instructions sysvar: 2` | `instructions sysvar: 2` |
| 15 | 0 | 0 | `EG9fKpmLgkzCYZdj8uNDhHu5xmeXCZakccV6QmUavbzt: 2` | `Bank __inbox_event_auth PDA: 2` | `Bank inbox event authority PDA: 2` |
| 16 | 0 | 2 | `9DvDdsw38EB3RPChPqHkgBmntFbM5v79QxMyMSbfXWuy: 2` | `inbox helper state/counter account: 2` | `inbox state/counter account: 2` |
| 17 | 0 | 0 | `JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw: 2` | `JupNet inbox helper program: 2` | `inbox helper program: 2` |
| 18 | 0 | 0 | `2x4wPZePCbq2W9tFfP2bagXjXnysdqNWQWMtwGMoyPFv: 2` | `None` | `request/account state candidate: 2` |
| 19 | 0 | 0 | `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ: 2` | `Solana Gum Bank Program executable: 2` | `None` |

### `rfq_sell_resolve` raw len `17`

| Pos | Signer | Writable | Common accounts | Role labels | Inferred role |
|---:|---:|---:|---|---|---|
| 0 | 1 | 1 | `rfQMFpNueeNufBW4byyEAhvL4To4tCsVBVagcEWG8ea: 1` | `None` | `payer/signer: 1` |
| 1 | 0 | 1 | `H5Y5aLdTQXRWJ6kitWeUkHyAEVLPPfChgSxhUBVxZ3D2: 1` | `None` | `None` |
| 2 | 1 | 1 | `rfQMFpNueeNufBW4byyEAhvL4To4tCsVBVagcEWG8ea: 1` | `None` | `None` |
| 3 | 0 | 1 | `4s3gnkf1R2UzAWbfvVowfaW7VdLDNSQhmwjYcSnMYwmT: 1` | `None` | `Bank-owned compact state candidate: 1` |
| 4 | 0 | 0 | `HVKuqyK6wjexdVJAUARiGdQTdGBBWhdYyhCZGFXh9d4s: 1` | `None` | `Bank state/config candidate: 1` |
| 5 | 0 | 0 | `2sbhRE62pbi3sLo9CtjM7nYzUynEV4oBAPrGmQPrhnfF: 1` | `None` | `None` |
| 6 | 0 | 1 | `GqpFMhoHzfhUnM65kvCRkzozm4c72A9TpNZzt9D69z88: 1` | `token account mint=So11111111111111111111111111111111111111112 owner=2sbhRE62pbi3sLo9CtjM7nYzUynEV4oBAPrGmQPrhnfF: 1` | `None` |
| 7 | 0 | 0 | `So11111111111111111111111111111111111111112: 1` | `wrapped SOL mint: 1` | `token mint: 1` |
| 8 | 0 | 0 | `TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA: 1` | `SPL Token program: 1` | `None` |
| 9 | 0 | 1 | `C8VeT16ySsyMW9xijjmYgvw83FfvEZVJawn5jgpzcf1X: 1` | `token account mint=EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v owner=2sbhRE62pbi3sLo9CtjM7nYzUynEV4oBAPrGmQPrhnfF: 1` | `None` |
| 10 | 0 | 0 | `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v: 1` | `USDC mint: 1` | `destination/source token account: 1` |
| 11 | 0 | 0 | `TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA: 1` | `SPL Token program: 1` | `None` |
| 12 | 0 | 0 | `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ: 1` | `Solana Gum Bank Program executable: 1` | `None` |
| 13 | 0 | 1 | `5DtSBy1imR7W2Zbdt9Z1gfRPVmVZyTVorvi562SZ7bvd: 1` | `token account mint=EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v owner=rfQMFpNueeNufBW4byyEAhvL4To4tCsVBVagcEWG8ea: 1` | `token program: 1` |
| 14 | 0 | 0 | `5x38Kp4hvdomTCnCrAny4UtMUt5rQBdB6px2K1Ui45Wq: 1` | `None` | `None` |
| 15 | 0 | 0 | `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ: 1` | `Solana Gum Bank Program executable: 1` | `None` |
| 16 | 0 | 0 | `EG9fKpmLgkzCYZdj8uNDhHu5xmeXCZakccV6QmUavbzt: 1` | `Bank __inbox_event_auth PDA: 1` | `None` |
| 17 | 0 | 1 | `9DvDdsw38EB3RPChPqHkgBmntFbM5v79QxMyMSbfXWuy: 1` | `inbox helper state/counter account: 1` | `None` |
| 18 | 0 | 0 | `JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw: 1` | `JupNet inbox helper program: 1` | `None` |
| 19 | 0 | 0 | `2x4wPZePCbq2W9tFfP2bagXjXnysdqNWQWMtwGMoyPFv: 1` | `None` | `None` |
| 20 | 0 | 0 | `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ: 1` | `Solana Gum Bank Program executable: 1` | `None` |

### `rfq_sell_commit` raw len `8`

| Pos | Signer | Writable | Common accounts | Role labels | Inferred role |
|---:|---:|---:|---|---|---|
| 0 | 1 | 1 | `rfQMFpNueeNufBW4byyEAhvL4To4tCsVBVagcEWG8ea: 1` | `None` | `payer/signer: 1` |
| 1 | 0 | 0 | `H5Y5aLdTQXRWJ6kitWeUkHyAEVLPPfChgSxhUBVxZ3D2: 1` | `None` | `None` |
| 2 | 0 | 1 | `4s3gnkf1R2UzAWbfvVowfaW7VdLDNSQhmwjYcSnMYwmT: 1` | `None` | `None` |
| 3 | 0 | 0 | `HVKuqyK6wjexdVJAUARiGdQTdGBBWhdYyhCZGFXh9d4s: 1` | `None` | `Bank-owned compact state candidate: 1` |
| 4 | 0 | 0 | `2sbhRE62pbi3sLo9CtjM7nYzUynEV4oBAPrGmQPrhnfF: 1` | `None` | `Bank state/config candidate: 1` |
| 5 | 0 | 1 | `GqpFMhoHzfhUnM65kvCRkzozm4c72A9TpNZzt9D69z88: 1` | `token account mint=So11111111111111111111111111111111111111112 owner=2sbhRE62pbi3sLo9CtjM7nYzUynEV4oBAPrGmQPrhnfF: 1` | `None` |
| 6 | 0 | 0 | `So11111111111111111111111111111111111111112: 1` | `wrapped SOL mint: 1` | `None` |
| 7 | 0 | 0 | `TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA: 1` | `SPL Token program: 1` | `token mint: 1` |
| 8 | 0 | 1 | `C8VeT16ySsyMW9xijjmYgvw83FfvEZVJawn5jgpzcf1X: 1` | `token account mint=EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v owner=2sbhRE62pbi3sLo9CtjM7nYzUynEV4oBAPrGmQPrhnfF: 1` | `None` |
| 9 | 0 | 0 | `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v: 1` | `USDC mint: 1` | `None` |
| 10 | 0 | 0 | `TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA: 1` | `SPL Token program: 1` | `destination/source token account: 1` |
| 11 | 0 | 0 | `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ: 1` | `Solana Gum Bank Program executable: 1` | `None` |
| 12 | 0 | 0 | `ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL: 1` | `Associated Token program: 1` | `None` |
| 13 | 0 | 0 | `11111111111111111111111111111111: 1` | `system program: 1` | `token program: 1` |
| 14 | 0 | 1 | `DnM9teVNbi4Cebkqtar3sVJs9LcZWSrV8DhwQzPpSeqM: 1` | `token account mint=So11111111111111111111111111111111111111112 owner=rfQMFpNueeNufBW4byyEAhvL4To4tCsVBVagcEWG8ea: 1` | `None` |
| 15 | 0 | 1 | `5DtSBy1imR7W2Zbdt9Z1gfRPVmVZyTVorvi562SZ7bvd: 1` | `token account mint=EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v owner=rfQMFpNueeNufBW4byyEAhvL4To4tCsVBVagcEWG8ea: 1` | `None` |
| 16 | 0 | 0 | `2x4wPZePCbq2W9tFfP2bagXjXnysdqNWQWMtwGMoyPFv: 1` | `None` | `None` |
| 17 | 0 | 0 | `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ: 1` | `Solana Gum Bank Program executable: 1` | `None` |

## Interpretation

- `GUMeb...` is not directly invoked in the saved transaction bodies; its role comes from decoded inner outbox verifier payloads, where it is the stable sender/program id.
- Direct `brhPf...` Gum samples are admin/authority-heavy and mostly touch Gum-owned config/state, Token-2022, system and associated-token surfaces.
- Direct Solana Bank samples split into asset movement (`withdraw`, `sweep`, RFQ variants) and proof verification (`verify_request`).
- Bank `verify_request` consistently uses the outbox root-history account and outbox helper program, matching the proof-chain model.
- The visible account-role surface still does not expose JUP staking, Dove signer weights, validator mappings, quorum state, slashing or rewards.
