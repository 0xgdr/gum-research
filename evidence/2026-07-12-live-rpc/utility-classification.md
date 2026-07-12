# Gum Utility Surface Classifier

## Scope

This report classifies JUP-related Gum data as utility evidence or non-decisive asset evidence.
Trading, route and token-transfer evidence is treated as noise unless it connects to stake, signer weight, quorum, fees, governance, access control, rewards, slashing or permanent protocol sinks.

## JUP Metadata Account Classification

- Gum accounts scanned: `2902`
- Gum accounts with canonical JUP base58 text: `127`
- Gum accounts with canonical JUP raw pubkey bytes: `0`
- Gum JUP accounts with utility-keyword strings: `0`

| Count | Data length | Prefix | JUP text offset | Classification |
|---:|---:|---|---:|---|
| 68 | 592 | `01ff010000000000` | 416 | `asset_metadata_or_route_config` |
| 30 | 592 | `01fe010000000000` | 416 | `asset_metadata_or_route_config` |
| 19 | 592 | `01fd010000000000` | 416 | `asset_metadata_or_route_config` |
| 4 | 592 | `01fb010000000000` | 416 | `asset_metadata_or_route_config` |
| 3 | 592 | `01fc010000000000` | 416 | `asset_metadata_or_route_config` |
| 1 | 592 | `01fa010000000000` | 416 | `asset_metadata_or_route_config` |
| 1 | 672 | `02fe010000000000` | 320 | `asset_metadata_or_route_config` |
| 1 | 672 | `02ff010000000000` | 320 | `asset_metadata_or_route_config` |

- No JUP metadata accounts contained utility keywords in printable strings.

Interpretation: the 127 JUP accounts look like asset metadata or route/config records. This is non-decisive asset evidence unless a future decoder ties these layouts to fees, staking, signer weights, access control or other utility.

## Repeated Gum Path Accounts

| Account | Owner | Executable | Space | Lamports | Utility string hits | Classification | Note |
|---|---|---|---:|---:|---|---|---|
| `ESUtymMEp6NULmLBcREaumM87TRpgt5R4eNYVrKjCKQq` | `missing` | `` |  |  | `` | `missing` | `transient writable account in repeated 1202 variant; missing by snapshot account fetch` |
| `76WKTLzujFUnj7TyB7CqLywPE3YZQf4Fmxj9SwcFAJrY` | `brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1` | `False` | 136 | 1837440 | `` | `gum_owned_config_or_state` | `gum-owned 136-byte repeated state/config account in 1202 variant` |
| `Hso4y8rKEXUUvMbxnyDmjCxA7yk1wbVsZNHSGXcDEUyU` | `brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1` | `False` | 200 | 2282880 | `` | `gum_owned_config_or_state` | `gum-owned 200-byte readonly account; candidate chain_config based on swap logs` |
| `GZF3sfYF27BU83fd5BPgB419SZiLLZPty3qL6465JTp6` | `brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1` | `False` | 336 | 3229440 | `` | `gum_owned_config_or_state` | `gum-owned 336-byte readonly account; candidate input_unified_mint_map based on swap logs` |
| `Fh54LKACZCzo3GzDcxoPQomTZamBsFy6XLbj15zJP1WH` | `brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1` | `False` | 592 | 5011200 | `` | `gum_owned_config_or_state` | `gum-owned 592-byte account created in swap flow; candidate swap_request/request state` |
| `A5ER4hbDN82jEnf986kZzuJzMzsyw1DRqodnone5yJWo` | `Tokenis9xgQh7yMRbNBnV6uFq7LANbuZJwebxWBWixf` | `False` | 631 | 5282640 | `` | `token_mint_or_account` | `JPL token mint touched in sampled token CPI; not canonical Solana JUP` |
| `94oZZEp1p1Vwuvc7axgeaRSU4Mk9diugqzjxpz1dnSZv` | `missing` | `` |  |  | `` | `missing` | `token transfer authority/user signer in sampled swap flow; missing by snapshot account fetch` |
| `FCNefQTEYCsPyQA64hdCpekucCDJFPHm2qfwg8F61jgc` | `Tokenis9xgQh7yMRbNBnV6uFq7LANbuZJwebxWBWixf` | `False` | 218 | 2408160 | `` | `token_mint_or_account` | `JPL token account created in sampled swap flow` |

## Gum Instruction Variant Classification

| First bytes | Data length | Count | Utility relevance |
|---|---:|---:|---|
| `1202` | 2 | 5 | `small_admin_or_state_transition; no embedded utility payload visible` |
| `0184030000781177` | 244 | 1 | `message_or_proof_payload; inspect accounts/logs for utility` |
| `0020000000633166` | 187 | 1 | `message_or_proof_payload; inspect accounts/logs for utility` |
| `0a` | 1 | 1 | `small_admin_or_state_transition; no embedded utility payload visible` |

| File | Slot | Variant | Data length | Accounts | Signer accounts | Writable accounts | Validator/vote/stake hits |
|---|---:|---|---:|---:|---|---|---|
| `tx-2944E3ze.json` | 43481695 | `0184030000781177` | 244 | 17 | `E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9, E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9` | `E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9, E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9, Fh54LKACZCzo3GzDcxoPQomTZamBsFy6XLbj15zJP1WH, 9tQb7MwoU2BubmX24nzDtdVBn2dQGSuSDUGAPuv6sabb, CFwUkiwnHWsiqJCaVoX9SH3yAGfrbHWJygAxRVECejH3, J7CzJ45sTMD5Bwc9Xo9cRVbtuR7fng6GBppqfbqitjxm, GZF3sfYF27BU83fd5BPgB419SZiLLZPty3qL6465JTp6, 5nPsQ5HnUuykL1VjR5AhzE847Ch61zY2U12F6Ft9oKML, 3rsSjn9vH779W23fofF4jxJcpsDCTdN5Hm9MPqKwMMUW, A5ER4hbDN82jEnf986kZzuJzMzsyw1DRqodnone5yJWo, FCNefQTEYCsPyQA64hdCpekucCDJFPHm2qfwg8F61jgc, 2VL6frjfzZN8qSqMVjQosJP213uetibbzxtMsGgBZvkv` | `` |
| `tx-2vXVfZ5i.json` | 43481480 | `0020000000633166` | 187 | 10 | `E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9, 94oZZEp1p1Vwuvc7axgeaRSU4Mk9diugqzjxpz1dnSZv` | `E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9, 94oZZEp1p1Vwuvc7axgeaRSU4Mk9diugqzjxpz1dnSZv, Fh54LKACZCzo3GzDcxoPQomTZamBsFy6XLbj15zJP1WH, A5ER4hbDN82jEnf986kZzuJzMzsyw1DRqodnone5yJWo, 3TsVLe3ZxEU9vhini76zkNZpRmd1xxygVQxH8obAhsmz, FCNefQTEYCsPyQA64hdCpekucCDJFPHm2qfwg8F61jgc` | `` |
| `tx-4Tmru364.json` | 43512860 | `0a` | 1 | 3 | `E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9` | `E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9` | `` |
| `tx-4rx2suR2.json` | 43479949 | `1202` | 2 | 8 | `E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9` | `ESUtymMEp6NULmLBcREaumM87TRpgt5R4eNYVrKjCKQq, E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9, 76WKTLzujFUnj7TyB7CqLywPE3YZQf4Fmxj9SwcFAJrY` | `` |
| `tx-5Z24iZ7L.json` | 43508011 | `1202` | 2 | 8 | `E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9` | `ESUtymMEp6NULmLBcREaumM87TRpgt5R4eNYVrKjCKQq, E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9, 76WKTLzujFUnj7TyB7CqLywPE3YZQf4Fmxj9SwcFAJrY` | `` |
| `tx-5qJXJSqe.json` | 43482205 | `1202` | 2 | 8 | `E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9` | `ESUtymMEp6NULmLBcREaumM87TRpgt5R4eNYVrKjCKQq, E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9, 76WKTLzujFUnj7TyB7CqLywPE3YZQf4Fmxj9SwcFAJrY` | `` |
| `tx-61k6WhYH.json` | 43512259 | `1202` | 2 | 8 | `E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9` | `ESUtymMEp6NULmLBcREaumM87TRpgt5R4eNYVrKjCKQq, E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9, 76WKTLzujFUnj7TyB7CqLywPE3YZQf4Fmxj9SwcFAJrY` | `` |
| `tx-qZnYsiDe.json` | 43479376 | `1202` | 2 | 8 | `E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9` | `ESUtymMEp6NULmLBcREaumM87TRpgt5R4eNYVrKjCKQq, E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9, 76WKTLzujFUnj7TyB7CqLywPE3YZQf4Fmxj9SwcFAJrY` | `` |

## Token Mint Noise Check

| Parsed token mint | Count | Utility classification |
|---|---:|---|
| `A5ER4hbDN82jEnf986kZzuJzMzsyw1DRqodnone5yJWo` | 3 | `non_jup_token_path` |

## Utility Finding

- No JUP staking, signer-weight, quorum, fee, governance, access-control, reward, slashing or permanent sink mechanism was identified in this pass.
- The 127 JUP hits remain classified as non-decisive asset metadata/config evidence.
- The repeated transaction-path accounts are worth decoding further, but current owner/role classification does not expose JUP utility.
