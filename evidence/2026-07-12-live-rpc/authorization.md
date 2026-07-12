# Gum Authorization Analysis

## Summary

- Gum upgrade authority: `E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9`
- Parsed Gum transaction files analyzed: `8`
- Unique signers: `2`
- Unique writable accounts: `15`
- Unique transaction accounts: `21`
- Validator/vote/stake account hits across transactions: `0`

## Signers

| Signer | Count | Role |
|---|---:|---|
| `E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9` | 8 | `gum_upgrade_authority` |
| `94oZZEp1p1Vwuvc7axgeaRSU4Mk9diugqzjxpz1dnSZv` | 1 | `` |

## Gum Instruction Data

| First 8 bytes | Count |
|---|---:|
| `1202` | 5 |
| `0184030000781177` | 1 |
| `0020000000633166` | 1 |
| `0a` | 1 |

| Data length | Count |
|---:|---:|
| 2 | 5 |
| 244 | 1 |
| 187 | 1 |
| 1 | 1 |

## Invoked Programs

| Program | Count |
|---|---:|
| `ComputeBudget111111111111111111111111111111` | 10 |
| `brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1` | 8 |
| `Tokenis9xgQh7yMRbNBnV6uFq7LANbuZJwebxWBWixf` | 4 |
| `11111111111111111111111111111111` | 2 |
| `ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL` | 1 |

## Token Mints Touched

| Mint | Count |
|---|---:|
| `A5ER4hbDN82jEnf986kZzuJzMzsyw1DRqodnone5yJWo` | 4 |

## Repeated Writable Accounts

| Account | Writable tx count | Role |
|---|---:|---|
| `E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9` | 8 | `gum_upgrade_authority` |
| `76WKTLzujFUnj7TyB7CqLywPE3YZQf4Fmxj9SwcFAJrY` | 5 | `gum_owned_account` |
| `ESUtymMEp6NULmLBcREaumM87TRpgt5R4eNYVrKjCKQq` | 5 | `` |
| `A5ER4hbDN82jEnf986kZzuJzMzsyw1DRqodnone5yJWo` | 2 | `` |
| `FCNefQTEYCsPyQA64hdCpekucCDJFPHm2qfwg8F61jgc` | 2 | `` |
| `Fh54LKACZCzo3GzDcxoPQomTZamBsFy6XLbj15zJP1WH` | 2 | `gum_owned_account` |
| `2VL6frjfzZN8qSqMVjQosJP213uetibbzxtMsGgBZvkv` | 1 | `` |
| `3rsSjn9vH779W23fofF4jxJcpsDCTdN5Hm9MPqKwMMUW` | 1 | `` |
| `5nPsQ5HnUuykL1VjR5AhzE847Ch61zY2U12F6Ft9oKML` | 1 | `` |
| `9tQb7MwoU2BubmX24nzDtdVBn2dQGSuSDUGAPuv6sabb` | 1 | `` |
| `CFwUkiwnHWsiqJCaVoX9SH3yAGfrbHWJygAxRVECejH3` | 1 | `` |
| `GZF3sfYF27BU83fd5BPgB419SZiLLZPty3qL6465JTp6` | 1 | `gum_owned_account` |
| `J7CzJ45sTMD5Bwc9Xo9cRVbtuR7fng6GBppqfbqitjxm` | 1 | `` |
| `94oZZEp1p1Vwuvc7axgeaRSU4Mk9diugqzjxpz1dnSZv` | 1 | `` |
| `3TsVLe3ZxEU9vhini76zkNZpRmd1xxygVQxH8obAhsmz` | 1 | `` |

## Per-Transaction Authorization Surface

| File | Slot | Signers | Writable accounts | Top-level programs | Inner programs | Validator/vote/stake hits |
|---|---:|---|---:|---|---|---|
| `tx-2944E3ze.json` | 43481695 | `E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9` | 11 | `ComputeBudget111111111111111111111111111111, brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1` | `` | `` |
| `tx-2vXVfZ5i.json` | 43481480 | `E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9, 94oZZEp1p1Vwuvc7axgeaRSU4Mk9diugqzjxpz1dnSZv` | 6 | `ComputeBudget111111111111111111111111111111, ComputeBudget111111111111111111111111111111, ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL, brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1` | `Tokenis9xgQh7yMRbNBnV6uFq7LANbuZJwebxWBWixf, 11111111111111111111111111111111, Tokenis9xgQh7yMRbNBnV6uFq7LANbuZJwebxWBWixf, Tokenis9xgQh7yMRbNBnV6uFq7LANbuZJwebxWBWixf, 11111111111111111111111111111111, Tokenis9xgQh7yMRbNBnV6uFq7LANbuZJwebxWBWixf` | `` |
| `tx-4Tmru364.json` | 43512860 | `E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9` | 1 | `ComputeBudget111111111111111111111111111111, ComputeBudget111111111111111111111111111111, brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1` | `` | `` |
| `tx-4rx2suR2.json` | 43479949 | `E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9` | 3 | `ComputeBudget111111111111111111111111111111, brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1` | `` | `` |
| `tx-5Z24iZ7L.json` | 43508011 | `E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9` | 3 | `ComputeBudget111111111111111111111111111111, brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1` | `` | `` |
| `tx-5qJXJSqe.json` | 43482205 | `E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9` | 3 | `ComputeBudget111111111111111111111111111111, brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1` | `` | `` |
| `tx-61k6WhYH.json` | 43512259 | `E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9` | 3 | `ComputeBudget111111111111111111111111111111, brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1` | `` | `` |
| `tx-qZnYsiDe.json` | 43479376 | `E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9` | 3 | `ComputeBudget111111111111111111111111111111, brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1` | `` | `` |

## Gum Instruction Accounts

### `tx-2944E3ze.json`

- Instruction index: `1`
- Data length: `244`
- First 8 bytes: `0184030000781177`

| Position | Account | Signer | Writable | Role |
|---:|---|---|---|---|
| 0 | `E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9` | `True` | `True` | `gum_upgrade_authority` |
| 1 | `E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9` | `True` | `True` | `gum_upgrade_authority` |
| 2 | `Fh54LKACZCzo3GzDcxoPQomTZamBsFy6XLbj15zJP1WH` | `False` | `True` | `gum_owned_account` |
| 3 | `94oZZEp1p1Vwuvc7axgeaRSU4Mk9diugqzjxpz1dnSZv` | `False` | `False` | `` |
| 4 | `9tQb7MwoU2BubmX24nzDtdVBn2dQGSuSDUGAPuv6sabb` | `False` | `True` | `` |
| 5 | `CFwUkiwnHWsiqJCaVoX9SH3yAGfrbHWJygAxRVECejH3` | `False` | `True` | `` |
| 6 | `J7CzJ45sTMD5Bwc9Xo9cRVbtuR7fng6GBppqfbqitjxm` | `False` | `True` | `` |
| 7 | `GZF3sfYF27BU83fd5BPgB419SZiLLZPty3qL6465JTp6` | `False` | `True` | `gum_owned_account` |
| 8 | `5nPsQ5HnUuykL1VjR5AhzE847Ch61zY2U12F6Ft9oKML` | `False` | `True` | `` |
| 9 | `3rsSjn9vH779W23fofF4jxJcpsDCTdN5Hm9MPqKwMMUW` | `False` | `True` | `` |
| 10 | `A5ER4hbDN82jEnf986kZzuJzMzsyw1DRqodnone5yJWo` | `False` | `True` | `` |
| 11 | `FCNefQTEYCsPyQA64hdCpekucCDJFPHm2qfwg8F61jgc` | `False` | `True` | `` |
| 12 | `2VL6frjfzZN8qSqMVjQosJP213uetibbzxtMsGgBZvkv` | `False` | `True` | `` |
| 13 | `Hso4y8rKEXUUvMbxnyDmjCxA7yk1wbVsZNHSGXcDEUyU` | `False` | `False` | `gum_owned_account` |
| 14 | `Tokenis9xgQh7yMRbNBnV6uFq7LANbuZJwebxWBWixf` | `False` | `False` | `` |
| 15 | `11111111111111111111111111111111` | `False` | `False` | `system_program` |
| 16 | `ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL` | `False` | `False` | `associated_token_program` |

### `tx-2vXVfZ5i.json`

- Instruction index: `3`
- Data length: `187`
- First 8 bytes: `0020000000633166`

| Position | Account | Signer | Writable | Role |
|---:|---|---|---|---|
| 0 | `E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9` | `True` | `True` | `gum_upgrade_authority` |
| 1 | `94oZZEp1p1Vwuvc7axgeaRSU4Mk9diugqzjxpz1dnSZv` | `True` | `True` | `` |
| 2 | `Fh54LKACZCzo3GzDcxoPQomTZamBsFy6XLbj15zJP1WH` | `False` | `True` | `gum_owned_account` |
| 3 | `GZF3sfYF27BU83fd5BPgB419SZiLLZPty3qL6465JTp6` | `False` | `False` | `gum_owned_account` |
| 4 | `A5ER4hbDN82jEnf986kZzuJzMzsyw1DRqodnone5yJWo` | `False` | `True` | `` |
| 5 | `3TsVLe3ZxEU9vhini76zkNZpRmd1xxygVQxH8obAhsmz` | `False` | `True` | `` |
| 6 | `FCNefQTEYCsPyQA64hdCpekucCDJFPHm2qfwg8F61jgc` | `False` | `True` | `` |
| 7 | `Hso4y8rKEXUUvMbxnyDmjCxA7yk1wbVsZNHSGXcDEUyU` | `False` | `False` | `gum_owned_account` |
| 8 | `Tokenis9xgQh7yMRbNBnV6uFq7LANbuZJwebxWBWixf` | `False` | `False` | `` |
| 9 | `11111111111111111111111111111111` | `False` | `False` | `system_program` |

### `tx-4Tmru364.json`

- Instruction index: `2`
- Data length: `1`
- First 8 bytes: `0a`

| Position | Account | Signer | Writable | Role |
|---:|---|---|---|---|
| 0 | `E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9` | `True` | `True` | `gum_upgrade_authority` |
| 1 | `Fh54LKACZCzo3GzDcxoPQomTZamBsFy6XLbj15zJP1WH` | `False` | `False` | `gum_owned_account` |
| 2 | `brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1` | `False` | `False` | `gum_program` |

### `tx-4rx2suR2.json`

- Instruction index: `1`
- Data length: `2`
- First 8 bytes: `1202`

| Position | Account | Signer | Writable | Role |
|---:|---|---|---|---|
| 0 | `ESUtymMEp6NULmLBcREaumM87TRpgt5R4eNYVrKjCKQq` | `False` | `True` | `` |
| 1 | `E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9` | `True` | `True` | `gum_upgrade_authority` |
| 2 | `76WKTLzujFUnj7TyB7CqLywPE3YZQf4Fmxj9SwcFAJrY` | `False` | `True` | `gum_owned_account` |
| 3 | `brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1` | `False` | `False` | `gum_program` |
| 4 | `11111111111111111111111111111111` | `False` | `False` | `system_program` |
| 5 | `brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1` | `False` | `False` | `gum_program` |
| 6 | `Hso4y8rKEXUUvMbxnyDmjCxA7yk1wbVsZNHSGXcDEUyU` | `False` | `False` | `gum_owned_account` |
| 7 | `brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1` | `False` | `False` | `gum_program` |

### `tx-5Z24iZ7L.json`

- Instruction index: `1`
- Data length: `2`
- First 8 bytes: `1202`

| Position | Account | Signer | Writable | Role |
|---:|---|---|---|---|
| 0 | `ESUtymMEp6NULmLBcREaumM87TRpgt5R4eNYVrKjCKQq` | `False` | `True` | `` |
| 1 | `E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9` | `True` | `True` | `gum_upgrade_authority` |
| 2 | `76WKTLzujFUnj7TyB7CqLywPE3YZQf4Fmxj9SwcFAJrY` | `False` | `True` | `gum_owned_account` |
| 3 | `brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1` | `False` | `False` | `gum_program` |
| 4 | `11111111111111111111111111111111` | `False` | `False` | `system_program` |
| 5 | `brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1` | `False` | `False` | `gum_program` |
| 6 | `Hso4y8rKEXUUvMbxnyDmjCxA7yk1wbVsZNHSGXcDEUyU` | `False` | `False` | `gum_owned_account` |
| 7 | `brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1` | `False` | `False` | `gum_program` |

### `tx-5qJXJSqe.json`

- Instruction index: `1`
- Data length: `2`
- First 8 bytes: `1202`

| Position | Account | Signer | Writable | Role |
|---:|---|---|---|---|
| 0 | `ESUtymMEp6NULmLBcREaumM87TRpgt5R4eNYVrKjCKQq` | `False` | `True` | `` |
| 1 | `E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9` | `True` | `True` | `gum_upgrade_authority` |
| 2 | `76WKTLzujFUnj7TyB7CqLywPE3YZQf4Fmxj9SwcFAJrY` | `False` | `True` | `gum_owned_account` |
| 3 | `brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1` | `False` | `False` | `gum_program` |
| 4 | `11111111111111111111111111111111` | `False` | `False` | `system_program` |
| 5 | `brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1` | `False` | `False` | `gum_program` |
| 6 | `Hso4y8rKEXUUvMbxnyDmjCxA7yk1wbVsZNHSGXcDEUyU` | `False` | `False` | `gum_owned_account` |
| 7 | `brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1` | `False` | `False` | `gum_program` |

### `tx-61k6WhYH.json`

- Instruction index: `1`
- Data length: `2`
- First 8 bytes: `1202`

| Position | Account | Signer | Writable | Role |
|---:|---|---|---|---|
| 0 | `ESUtymMEp6NULmLBcREaumM87TRpgt5R4eNYVrKjCKQq` | `False` | `True` | `` |
| 1 | `E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9` | `True` | `True` | `gum_upgrade_authority` |
| 2 | `76WKTLzujFUnj7TyB7CqLywPE3YZQf4Fmxj9SwcFAJrY` | `False` | `True` | `gum_owned_account` |
| 3 | `brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1` | `False` | `False` | `gum_program` |
| 4 | `11111111111111111111111111111111` | `False` | `False` | `system_program` |
| 5 | `brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1` | `False` | `False` | `gum_program` |
| 6 | `Hso4y8rKEXUUvMbxnyDmjCxA7yk1wbVsZNHSGXcDEUyU` | `False` | `False` | `gum_owned_account` |
| 7 | `brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1` | `False` | `False` | `gum_program` |

### `tx-qZnYsiDe.json`

- Instruction index: `1`
- Data length: `2`
- First 8 bytes: `1202`

| Position | Account | Signer | Writable | Role |
|---:|---|---|---|---|
| 0 | `ESUtymMEp6NULmLBcREaumM87TRpgt5R4eNYVrKjCKQq` | `False` | `True` | `` |
| 1 | `E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9` | `True` | `True` | `gum_upgrade_authority` |
| 2 | `76WKTLzujFUnj7TyB7CqLywPE3YZQf4Fmxj9SwcFAJrY` | `False` | `True` | `gum_owned_account` |
| 3 | `brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1` | `False` | `False` | `gum_program` |
| 4 | `11111111111111111111111111111111` | `False` | `False` | `system_program` |
| 5 | `brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1` | `False` | `False` | `gum_program` |
| 6 | `Hso4y8rKEXUUvMbxnyDmjCxA7yk1wbVsZNHSGXcDEUyU` | `False` | `False` | `gum_owned_account` |
| 7 | `brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1` | `False` | `False` | `gum_program` |

## Interpretation

- The sampled Gum transactions are enough to identify the public authorization surface for those flows, but not enough to prove every Gum instruction variant.
- If validator or Dove security is enforced privately or through hashed/encrypted state, this transaction-level scan will not expose it directly.
- Public evidence for validator/Dove participation would become stronger if validator, vote, stake, signer-set, quorum, or weight accounts appeared in these account lists or verifier/config account layouts.
