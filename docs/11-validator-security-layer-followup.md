# Validator Security Layer Follow-Up

## Snapshot

This follow-up tested whether public JupNet state exposes evidence that JUP is used directly in the validator or Dove security layer. It also treats JUP trading/asset metadata as non-decisive unless linked to utility.

The live snapshot was collected on:

```text
2026-07-12T09:55:32Z
```

The bounded RPC evidence is stored under:

```text
evidence/2026-07-12-live-rpc/
```

The generated analyzer output is:

```text
evidence/2026-07-12-live-rpc/analysis.md
evidence/2026-07-12-live-rpc/deep-dive.md
evidence/2026-07-12-live-rpc/authorization.md
```

## Methods Added

Three reproducibility scripts were added:

- `scripts/collect_validator_security_snapshot.py`
- `scripts/analyze_validator_security_snapshot.py`
- `scripts/deep_dive_validator_security_snapshot.py`

The collector captures:

- slot, epoch and RPC identity;
- cluster nodes;
- vote accounts;
- stake-program accounts;
- OpenID Registry accounts;
- Gum-owned accounts;
- NativeLoader-owned accounts;
- the canonical Solana JUP mint account on JupNet;
- SPL token accounts whose mint is canonical JUP;
- recent Gum signatures and a bounded set of parsed Gum transactions.

The analyzer scans saved account data for:

- canonical JUP raw pubkey bytes;
- canonical JUP base58 text;
- `JUP` symbol text;
- current validator identity keys;
- current vote account keys;
- current stake account keys.

The deep-dive analyzer additionally groups Gum JUP-hit accounts by data length, first eight bytes and text offset, then maps Gum program loader metadata and sampled Gum transaction signers.

The Gum authorization analyzer classifies sampled Gum transaction signers, writable accounts, invoked programs, token mints, instruction data lengths, instruction-data prefixes and full Gum instruction account metas.

This scan is intentionally limited to public account data. It cannot detect private validator configuration, off-chain committee state, or encrypted/hashed mappings unless the scanned bytes are directly present.

## Findings

### Native Validator Surface

The snapshot returned:

- 14 cluster nodes;
- 7 current vote accounts;
- 0 delinquent vote accounts;
- 7 stake-program accounts.

Each current vote account had:

```text
999999997717120 activated native stake
```

Each stake account delegated the same native stake amount to one vote account. The stake-account staker and withdrawer were the corresponding validator identity keys.

This is consistent with an equal native-stake validator set for the current public SVM consensus surface. It does not show JUP-denominated validator weight.

### JUP Surface

The canonical Solana JUP mint:

```text
JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN
```

was tested directly on JupNet.

Results:

- `getAccountInfo` for the canonical JUP mint returned `null`.
- The SPL Token Program memcmp query for token accounts with that mint returned zero accounts.
- 0 Gum-owned accounts contained the canonical JUP mint as raw 32-byte pubkey bytes.
- 127 Gum-owned accounts contained the canonical JUP mint as base58 text.
- OpenID Registry accounts contained zero canonical JUP mint hits.
- NativeLoader accounts contained zero canonical JUP mint hits.

Interpretation:

Gum state publicly references canonical JUP as an external or configured asset string. This is asset support, not utility by itself. In this snapshot, the canonical Solana JUP mint does not appear to exist as a native JupNet SPL mint account, no JupNet SPL token accounts were found for that mint, and the scanned Gum layouts did not contain the canonical mint as raw pubkey bytes.

This supports the existing conclusion that JUP is visible in Gum asset configuration/flows, but it does not support the stronger claim that JUP has protocol utility such as staking, signer weight, fee flow, access control, governance, slashing, rewards or validator security.

### Validator-to-JUP Correlation

The analyzer scanned Gum and OpenID account data for:

- current validator identity pubkeys;
- current vote account pubkeys;
- current stake account pubkeys.

Results:

- Gum accounts containing current validator/vote/stake keys: 0.
- OpenID accounts containing current validator/vote/stake keys: 0.

Interpretation:

No public Gum or OpenID account scanned in this snapshot exposed a direct mapping from current validators, vote accounts or stake accounts to JUP configuration.

This does not disprove a private/off-chain Dove mapping, but it narrows the public evidence boundary.

### Gum Activity

The latest 20 signatures returned for the Gum program were from:

```text
2026-05-06T12:01:52Z to 2026-05-06T12:59:33Z
```

The sampled parsed transactions showed Gum message/proof log terms such as:

```text
RequestClaimAccounts verified and loaded
request_claim swap msg_hash
outbox msg_hash
inbox_hash
proof_hash
Verifying input_unified_mint_map PDA
```

The sampled logs did not expose validator stake weights, Dove membership, JUP stake, quorum weight calculation or validator/vote account references.

### Gum Program Control Surface

The Gum program is upgradeable:

```text
Program: brhPfKExpnYDHroomHrk7PNJ4UXJx9SYohCCtd6r8N1
ProgramData: BW7ncAFAX1jjhZU6X5AS8JrkAqr8njfUNQxkuPtUQXjv
Deployment slot: 8167938
Upgrade authority: E9fAVytyjE1EzXfaoCE1it9ZDBKRMTyVndGn1mB1Nvn9
```

The upgrade authority account was system-owned, non-executable and had zero account data space in this snapshot. All eight sampled Gum transactions included the Gum upgrade authority as a signer. None of those sampled transactions included current validator identity keys, vote account keys or stake account keys in their transaction account lists.

Interpretation:

The sampled Gum activity appears operationally controlled by the Gum upgrade-authority key rather than by the public native validator set. This does not rule out private/off-chain Dove signing, but it gives no public evidence that current native validators, their native stake accounts or JUP utility mechanisms are participating directly in sampled Gum message flow.

### Gum Authorization Surface

The Solana-style transaction/account-meta analysis covered eight parsed Gum transactions.

Summary:

- unique signers: 2;
- unique writable accounts: 15;
- unique transaction accounts: 21;
- validator/vote/stake account hits across transactions: 0;
- the Gum upgrade authority signed all eight sampled transactions;
- one sampled transfer-style transaction also included signer `94oZZEp1p1Vwuvc7axgeaRSU4Mk9diugqzjxpz1dnSZv`;
- one parsed token mint was touched: `A5ER4hbDN82jEnf986kZzuJzMzsyw1DRqodnone5yJWo`;
- invoked programs were limited to ComputeBudget, Gum, JPL Token, System and Associated Token.

Five sampled Gum instructions used two-byte data with prefix:

```text
1202
```

The larger sampled instructions had data lengths of 187 and 244 bytes. Those are plausible message/proof/action payloads, but their public account metas still did not include native validator, vote or stake accounts.

Interpretation:

From a Solana program-operator perspective, the sampled public authorization path is dominated by transaction signers, writable Gum/config-like accounts and token-program CPIs. It does not expose a public validator-set, vote-account, stake-account, signer-weight or JUP-weighted quorum dependency.

## Current Assessment

The follow-up strengthens three conclusions:

1. The public native validator layer currently visible through RPC is native-stake based, not visibly JUP-stake based.
2. Gum publicly references canonical JUP as text metadata/configuration, but this is non-decisive asset evidence and not a utility mechanism.
3. No public Gum/OpenID account data in this snapshot maps current validator identities, vote accounts or stake accounts to JUP.
4. The sampled Gum transactions were signed by the Gum upgrade authority and did not expose current validator/vote/stake account participation.
5. The sampled Gum transaction account metas and CPIs show operator/config/token-program authorization surfaces, not a visible native-validator or JUP-weighted Dove surface.

The decisive unresolved boundary remains private or off-chain state:

- validator runtime configuration;
- Dove signer registry;
- BLS signer weights;
- JUP lock/delegation, fee, governance, access-control, reward, slashing or burn/sink records;
- quorum-enforcement code.

## Next Proof Targets

The next highest-value work is:

1. Decode the 127 Gum accounts that contain the canonical JUP mint and classify whether they are only asset metadata or part of a utility mechanism.
2. Identify Gum verifier/config accounts and determine whether any contain signer sets or weight fields.
3. Track Gum program upgrades by ProgramData hash and diff account layouts across snapshots.
4. Search for public validator/Dove source, deployment configs, Docker images or lockfiles that reference JUP-denominated weights.
5. Monitor whether new Gum signatures appear after 2026-05-06 and whether new transactions expose signer or quorum metadata.
