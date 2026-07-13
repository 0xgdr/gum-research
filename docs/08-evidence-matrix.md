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
| Gum supports JUP as a tradable/configured asset | Confirmed, non-decisive | Canonical mint found in Gum state; asset support is not utility by itself |
| Gum burns JUP in observed flows | Confirmed, non-decisive | Parsed Burn instruction; utility requires a permanent protocol sink or fee mechanism |
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
| Sampled Gum transaction account metas expose validator/vote/stake accounts | Not observed | Gum authorization analyzer found zero validator/vote/stake hits across eight parsed Gum transactions |
| Sampled Gum transactions expose JUP-weighted quorum accounts | Not observed | Account-meta and CPI analysis found operator/config/token-program surfaces, but no signer-weight/quorum/JUP-stake accounts |
| Gum JUP metadata accounts expose utility strings | Not observed | Utility classifier found zero utility-keyword strings after filtering hash-like false positives |
| Gum JUP metadata accounts look like asset metadata or route config | Strong evidence, non-decisive | 127 JUP text hits grouped into 592-byte or 672-byte layouts with no raw JUP pubkey bytes |
| Sampled Gum token CPI touches canonical Solana JUP | Not observed | Parsed token mint was `A5ER4hbDN82jEnf986kZzuJzMzsyw1DRqodnone5yJWo`, not canonical JUP |
| Public literal Gum repository exists under `jup-ag` | Not observed | GitHub API checks for `jup-ag/gum`, `jup-ag/GUM`, `jup-ag/gum-sdk` and `jup-ag/jupnet` returned `404` on 2026-07-12 |
| Public `jupnet/jupnet-svm` source is inspectable | Not observed | GitHub API check returned `404` on 2026-07-12 despite dependency metadata referencing the repo URL |
| Public `jup-ag/omnipair-amm-sdk` explains Gum/JUP validator utility | Not observed | Source shows Omnipair AMM integration, quote math, swap metas, rate model and futarchy-authority config, but no JUP stake/weight/quorum/security mechanism |
| Public Jupiter registry names GUM/JupNet | Confirmed, non-decisive | `jup-ag/platform-list` contains the only exact public-org `gum`/`jupnet` crawl hits and registers GUM as a Jupiter-parented DEX with bank-related Solana addresses |
| Public `jup-ag` crawl exposes Gum source or JUP security utility | Not observed | Boundary-matched crawl scanned 186 public repositories; no `proof_hash`/`outbox` hits and no public JUP stake/weight/quorum/validator-security mechanism found |
| Public registry Bank addresses exist on JupNet RPC | Not observed | 2026-07-12 Bank snapshot returned `null` account info and zero signature-window hits for both registry Bank addresses on JupNet RPC |
| Public registry Bank addresses exist on Solana mainnet | Confirmed | Both `bk1PDA...` and `BankK1...` are executable upgradeable-loader accounts on Solana mainnet |
| Solana Bank Program exposes inbox/outbox message flow | Confirmed | Sampled Bank Program transactions logged `SubmitInboxMessageWithFinality`, `VerifyOutboxMessage` and `Outbox verification passed` |
| Sampled Solana Bank Program transactions use canonical JUP | Not observed | Eight sampled Bank Program transactions had zero canonical JUP account-key hits; parsed token mints were USDC and wrapped SOL |
| Solana Bank Program proves JUP validator/Dove utility | Not observed | Bank evidence supports cross-chain message/deposit plumbing, but no JUP stake/weight/quorum/security/fee mechanism was observed |
| Solana Bank instruction variants are recoverable from sampled txs | Confirmed | Five Anchor-style variants identified: `withdraw`, `sweep`, `verify_request`, `rfq_sell_resolve`, `rfq_sell_commit` |
| Solana Bank binaries expose request/inbox/outbox/Merkle strings | Confirmed | Full ProgramData string scan found request, inbox, outbox, `JUPNET_INBOX`, `merkle_root_state`, `message_hash`, `InvalidMerkleProof` and related source paths |
| Solana Bank binary strings prove JUP token utility | Not observed | `jup`/`jupnet` strings establish JupNet context, but no JUP-denominated staking, weights, fees, rewards, slashing or governance mechanism was recovered |
| Solana Bank account graph exposes inbox PDA plumbing | Confirmed | Bounded PDA hunt matched `__inbox_event_auth` under the Bank Program to observed account `EG9fKpmLgkzCYZdj8uNDhHu5xmeXCZakccV6QmUavbzt` |
| Solana Bank account graph exposes canonical JUP-derived security state | Not observed | Sampled Bank instructions had zero canonical JUP mint account hits and no bounded JUP-derived PDA match |
| Recurring Solana Bank accounts hide canonical JUP state | Not observed | Full account fetch for 20 recurring Bank instruction accounts found zero canonical JUP raw pubkey/text hits |
| Recurring Solana Bank accounts expose validator/vote/stake mappings | Not observed | The same 20-account fetch found zero current JupNet validator/vote/stake key hits |
| Recurring Solana Bank accounts include compact Bank-owned state | Confirmed | Two recurring accounts were Bank Program-owned: 9-byte state `HVKuqy...` and 41-byte state `4s3g...` with no JUP/security key hits |
| Solana Bank owner context exposes JupNet inbox helper program | Confirmed | Program `JNiN12...` ProgramData strings include `programs/jupnet-inbox-program`, `SubmitInboxMessage`, `SubmitInboxMessageWithFinality` and `JUPNET_INBOX` |
| Solana Bank owner context exposes JupNet outbox helper program | Confirmed | Program `jnoUtn...` ProgramData strings include `programs/jupnet-outbox-program`, `VerifyOutboxMessage`, `Verifying BLS signature`, `Merkle proof verified` and `merkle_root_state` |
| Solana Bank owner context exposes JUP validator-security state | Not observed | Owner-context accounts and helper ProgramData did not expose canonical JUP key material or current JupNet validator/vote/stake key mappings |
| JupNet helper-owned accounts expose Merkle root history | Confirmed | Outbox helper program owns one 320-byte account decoding as epoch/root entries for epochs 271, 270 and 269 |
| JupNet helper-owned accounts expose signer-set or quorum state | Not observed | Inbox/outbox helper programs each own one public account; neither contains canonical JUP, current validator/vote/stake keys, signer-set labels, quorum thresholds or obvious weight state |
| `verify_request` payloads expose Merkle proof data | Confirmed | Two sampled 455-byte payloads include a five-node 32-byte proof tail and reference the outbox root state through account metas |
| `verify_request` payloads expose JUP security utility | Not observed | Payload scans found USDC and Bank Program pubkeys but zero canonical JUP, current validator/vote/stake keys, signer-set or quorum fields |
| Outbox root updates verify BLS signatures publicly | Confirmed | One recent outbox transaction logged `UpdateMerkleRoot invoked`, `Merkle proof verified`, `Verifying BLS signature` and `Signature verified` |
| Outbox root update payload exposes JUP signer/quorum source | Not observed | The sampled 305-byte update payload and account keys exposed the outbox root account and Merkle data, but zero canonical JUP or current validator/vote/stake key hits |
| Outbox root update payload matches the published JupNet Merkle formula | Confirmed | Recomputed `SHA256(0x00 || candidate_64_bytes)` leaf and `SHA256(0x01 || left || right)` parents reproduce the stored epoch `271` root |
| Outbox root update payload exposes the aggregate-key inclusion boundary | Strong evidence | The final 64-byte field hashes into the Merkle leaf; the following proof path and bitmap reconstruct the emitted root exactly |
| Outbox root update payload exposes underlying Dove members or JUP weights | Not observed | The compact proof verifies aggregate-key inclusion but does not list Dove identities, individual BLS keys, stake balances, JUP denomination or threshold calculation |
| Candidate aggregate-key material is reused across verification payloads | Confirmed | Epoch source hunt found the same 64-byte candidate aggregate key in 21 saved binary records, including repeated outbox/Bank verification payloads |
| Candidate aggregate-key material co-locates with JUP or validator stake keys | Not observed | Epoch source hunt found zero binary records containing the candidate aggregate key or epoch root together with canonical JUP, current validator, vote or stake keys |
| Public artifacts expose the top-half root source | Not observed | Scanning 3153 saved binary records did not find a Dove/JUP/stake-weight source for the aggregate-key Merkle tree |
| Outbox verifier payloads match the published argument shape | Confirmed | 21 parsed Bank/outbox verifier payloads expose message hash, sender/program id or wrapper context, epoch, aggregate-key material, compact signature/verifier field and Merkle proof |
| Parsed verifier payloads recompute to the stored epoch root | Confirmed | All 21 parsed verifier payloads recompute to `6928957b...9bd8d999` using the `0x00` leaf and `0x01` parent hash formula |
| Outbox verifier sender resolves to Gum omnichain | Confirmed | Stable sender/program candidate `GUMebNDC...` is an executable upgradeable JupNet program whose ProgramData strings identify `programs/gum-omnichain` |
| Gum omnichain executable exposes BLS/Merkle verification | Confirmed | ProgramData strings include `programs/gum-omnichain/src/utils/verification.rs` and `sol_verify_bls_merkle_key` |
| Gum omnichain executable exposes JUP security source | Not observed | ProgramData string/key scan found zero canonical JUP, current validator, vote or stake key hits and no Dove/JUP stake-weight registry strings |
| JupNet executable census covers visible upgradeable programs | Confirmed | Full ProgramData was fetched and analyzed for 23 upgradeable JupNet executables visible in the loader scan |
| JupNet executable census exposes verifier syscall consumers | Confirmed | `sol_verify_bls_merkle_key` appeared in two Gum omnichain executables: `brhPf...` and `GUMeb...` |
| JupNet executable census exposes root-builder or Dove/JUP producer | Not observed | Census found zero canonical JUP/current validator/vote/stake key hits and no public Dove registry, JUP stake-weight table, slashing/reward or root-builder implementation |
