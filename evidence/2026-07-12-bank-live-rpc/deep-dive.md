# Validator Security Deep Dive

## Gum JUP Account Structure

- Gum accounts scanned: `2902`
- Gum accounts with canonical JUP raw pubkey bytes: `0`
- Gum accounts with canonical JUP base58 text: `127`
- Gum accounts with `JUP` symbol text: `127`

| Count | Data length | First 8 bytes | Text offset(s) | Example account |
|---:|---:|---|---|---|
| 68 | 592 | `01ff010000000000` | `[416]` | `TaB617AuCmKGyNSfpzcXCNXRQjmVAXEVcSjwEuVt4pz` |
| 30 | 592 | `01fe010000000000` | `[416]` | `CUaR9p81LZir33hx1b6DvxuFGpUW7BuoyubaagpbEgF` |
| 19 | 592 | `01fd010000000000` | `[416]` | `14QWpYiPkC5S6LW67YfmqYYXW8NZVGmbbVz76cWb9AY5` |
| 4 | 592 | `01fb010000000000` | `[416]` | `2qwRen9xwkjkmVSxg8kUaP3UrXPPzL4QpRDDc7XDbb3p` |
| 3 | 592 | `01fc010000000000` | `[416]` | `77F2qQbjwfDm7MUjTF273sd6MCpupK5CWgxLpemDyhKE` |
| 1 | 592 | `01fa010000000000` | `[416]` | `52ui8Xxjb2NBvMGFT6EuTqv4xaDJteorxwZNaqxdSBFG` |
| 1 | 672 | `02fe010000000000` | `[320]` | `9Vz7e1MCNZEceDnKHZ8TvSSVym6DqEPo67RV6zWVnuKS` |
| 1 | 672 | `02ff010000000000` | `[320]` | `HpD5ms9NWpdgBZL2ikXp7dEiMAZUQz22QFqjRswFCe5h` |

Interpretation: the JUP references in Gum account data are textual asset identifiers, not raw 32-byte mint pubkey fields in the scanned account layouts.

## Program Loader Surface

- Gum program: `brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1`
- Gum program owner: `BPFLoaderUpgradeab1e11111111111111111111111`
- Gum ProgramData account: `BW7ncAFAX1jjhZU6X5AS8JrkAqr8njfUNQxkuPtUQXjv`
- Gum ProgramData owner: `BPFLoaderUpgradeab1e11111111111111111111111`
- Gum ProgramData deployment slot: `8167938`
- Gum ProgramData upgrade authority: `E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9`
- Upgrade authority account owner: `11111111111111111111111111111111`
- Upgrade authority lamports: `309295808040`
- Upgrade authority executable: `False`
- Upgrade authority data space: `0`
- Upgradeable loader account tags: `{2: 23, 3: 22, 1: 20}`
- Gum program maps to ProgramData in loader scan: `BW7ncAFAX1jjhZU6X5AS8JrkAqr8njfUNQxkuPtUQXjv`

## Public Registry Bank Surface

- Registry Bank account: `bk1PDAkbHEBGtVRiM94Lzets8gVFP7FgySyfkAc8MPN`
- Registry Bank Program: `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ`
- Bank account on configured RPC: `not present`
- Bank Program on configured RPC: `not present`
- Bank ProgramData account: `None`
- Bank ProgramData owner: `None`
- Bank ProgramData deployment slot: `None`
- Bank ProgramData upgrade authority: `None`
- Bank Program maps to ProgramData in loader scan: `None`

## Sample Gum Transaction Signers

| Transaction file | Slot | Signers | Upgrade authority signed | Validator/vote/stake account hits |
|---|---:|---|---|---|
| `tx-2944E3ze.json` | 43481695 | `E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9` | `True` | `` |
| `tx-2vXVfZ5i.json` | 43481480 | `E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9, 94oZZEp1p1Vwuvc7axgeaRSU4Mk9diugqzjxpz1dnSZv` | `True` | `` |
| `tx-4Tmru364.json` | 43512860 | `E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9` | `True` | `` |
| `tx-4rx2suR2.json` | 43479949 | `E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9` | `True` | `` |
| `tx-5Z24iZ7L.json` | 43508011 | `E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9` | `True` | `` |
| `tx-5qJXJSqe.json` | 43482205 | `E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9` | `True` | `` |
| `tx-61k6WhYH.json` | 43512259 | `E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9` | `True` | `` |
| `tx-qZnYsiDe.json` | 43479376 | `E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9` | `True` | `` |

## Sample Bank Program Transaction Signers

| Transaction file | Slot | Signers | Bank upgrade authority signed | Validator/vote/stake account hits | Watched Gum/Bank/JUP account hits |
|---|---:|---|---|---|---|
| `none` |  |  |  |  |  |

Interpretation: in the sampled Gum transactions, the Gum upgrade authority appears as a signer and no current validator, vote-account or stake-account keys appear in the transaction account lists.
