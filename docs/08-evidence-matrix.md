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
