# Evidence Matrix

| Claim | Assessment | Evidence |
|---|---|---|
| JupNet is an independent chain | Confirmed | Independent RPC identity, slot and validator set |
| JupNet uses a customised SVM | Confirmed | JupNet-specific loaders, versions and dependencies |
| Native validators exist | Confirmed | `getClusterNodes` |
| Native vote accounts exist | Confirmed | Vote/stake account inspection |
| Native stake exists | Confirmed | Standard stake-program delegated accounts |
| Native stake is JUP | Rejected | Accounts are native stake, not SPL JUP token accounts |
| BLS components exist | Strong evidence | Public JupNet dependency metadata |
| BN254/Merkle components exist | Strong evidence | Public dependency metadata |
| BLS is embedded in normal vote txs | Not observed | Decoded vote payloads |
| Gum supports JUP | Confirmed | Canonical mint found in Gum state |
| Gum burns JUP in observed flows | Confirmed | Parsed Burn instruction |
| Observed burn is permanently deflationary | Unverified | A mint also appeared in the flow |
| OpenID stores validator stake | Not observed | Registry decoding |
| Public Dove registry exists | Not observed | Program/account searches |
| JUP currently weights Dove security | Unverified | No public stake-weight mapping found |
| Two-thirds of staked JUP is enforced live | Unverified | Validator source/private configuration unavailable |
| Canonical Solana JUP mint exists as a JupNet account in the 2026-07-12 snapshot | Not observed | `getAccountInfo` returned `null` |
| JupNet SPL token accounts hold the canonical JUP mint in the 2026-07-12 snapshot | Not observed | Token-program memcmp query returned zero accounts |
| Gum state references canonical JUP mint as base58 text in the 2026-07-12 snapshot | Confirmed | 127 Gum-owned accounts contained the canonical JUP mint string |
| Gum state references canonical JUP mint as raw pubkey bytes in the 2026-07-12 snapshot | Not observed | Deep scan found zero raw 32-byte canonical JUP pubkey hits in Gum account data |
| Gum/OpenID state maps current validator/vote/stake keys to JUP in the 2026-07-12 snapshot | Not observed | Byte/text scan found zero current validator/vote/stake key hits in Gum and OpenID account data |
| Native validator consensus stake is equal-weight in the 2026-07-12 snapshot | Confirmed | Seven current vote accounts and seven stake accounts each reported `999999997717120` delegated native stake |
| Sampled Gum transactions are signed by current validator/vote/stake keys | Not observed | Eight sampled Gum transactions contained zero current validator/vote/stake account-key hits |
| Sampled Gum transactions are signed by the Gum upgrade authority | Confirmed | Eight sampled Gum transactions included `E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9` as a signer |
