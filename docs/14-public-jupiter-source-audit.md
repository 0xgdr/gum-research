# Public Jupiter Source Audit

## Purpose

This note records the public GitHub source check prompted by the question:

```text
Is there a public Jupiter Gum repository that explains JUP utility or validator security?
```

The audit is intentionally narrow. It looks for source code that connects JUP to Gum/JupNet utility, especially validator/Dove security, signer weights, quorum, fees, governance, access control, slashing, rewards or a permanent JUP sink.

## Repositories Checked

### `jup-ag/gum`, `jup-ag/GUM`, `jup-ag/gum-sdk`, `jup-ag/jupnet`

GitHub API checks for these literal repositories returned `404` on 2026-07-12.

Assessment: no public literal Gum repository was visible under the `jup-ag` GitHub org from these paths at the time of this audit.

### `jupnet/jupnet-svm`

The dependency metadata referenced:

```text
https://github.com/jupnet/jupnet-svm.git
```

The GitHub API also returned `404` for `jupnet/jupnet-svm` on 2026-07-12.

Assessment: this remains a source boundary. The reference is useful because it identifies a JupNet SVM dependency name, but the repository was not publicly inspectable during this audit.

### `jup-ag/omnipair-amm-sdk`

This repository is public and relevant to Jupiter routing, but the inspected code identifies an Omnipair AMM integration, not Gum validator or Dove security source.

Observed source facts:

- `README.md` describes a Rust SDK for integrating Omnipair with the Jupiter AMM interface.
- `Cargo.toml` describes the package as an SDK for interacting with Omnipair AMM, built for Jupiter.
- `src/lib.rs` defines `OMNIPAIR_PROGRAM_ID` as `omnixgS8fnqHfCcTGKWj6JtKjzpJZ1Y5y9pyFkQDkYE`.
- `src/lib.rs` implements pair state, quote math, reserve mints, update accounts and swap account metas through the Jupiter AMM interface.
- `src/omnipair_amm_client.rs` derives reserve vaults, a `futarchy_authority` PDA and event authority for Omnipair swaps.
- `src/interest.rs` models rate calculation, interest accrual and a futarchy-authority revenue configuration.

Utility assessment:

- This is useful AMM/routing evidence.
- It does not expose Gum validator/Dove software.
- It does not show JUP-denominated validator stake, signer weights, quorum, fees, slashing, rewards, governance or access control.
- The `futarchy_authority` naming is worth monitoring because it is governance/economics-adjacent, but the public SDK itself does not tie that authority to JUP utility.

### `jup-ag/chainkit`

This repository is public and describes a cross-platform blockchain utility library with Rust core plus Swift/Kotlin bindings.

Assessment: it is crypto/blockchain tooling, but no Gum/JupNet validator-security or JUP utility mechanism was identified from the README-level inspection.

## Current Conclusion

The public Jupiter source found in this pass does not change the repo's main conclusion:

```text
JUP is visible as a Gum asset/configuration surface, but public evidence still does not show JUP being used for Gum/JupNet protocol utility or validator security.
```

The strongest new lead is `jup-ag/omnipair-amm-sdk`, but it currently looks like an AMM integration source, not the missing Gum/Dove validator-security layer.

## Follow-up Checks

When re-running this audit, check:

- whether `jup-ag/gum`, `jup-ag/gum-sdk`, `jup-ag/jupnet` or `jupnet/jupnet-svm` becomes publicly accessible;
- whether `jup-ag/omnipair-amm-sdk` adds account types involving JUP stake, governance or fee sinks;
- whether Omnipair program accounts overlap with Gum repeated accounts from the live JupNet snapshot;
- whether any Jupiter source exposes a Dove, validator, signer, quorum, BLS or JUP-weight registry.
