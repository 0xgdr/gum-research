# Repository Catalogue

This catalogue tracks public and private source leads investigated for Gum/JupNet utility. It is focused on whether JUP is used for protocol utility: validator/Dove security, signer weights, quorum, fees, governance, access control, slashing, rewards or a permanent sink.

| Repository or source | Status | Notes |
|---|---:|---|
| `jupnet/jupnet-svm` | Private / 404 | Referenced by public dependency metadata. Strongest source lead for JupNet validator/runtime implementation, but not publicly inspectable during the investigation. |
| `jupnet-vote` | Private dependency reference | JupNet-specific vote crate named in dependency metadata. Indicates custom vote/runtime surface, but source was not directly inspectable. |
| `jupnet-vote-program` | Private dependency reference | JupNet-specific vote-program crate named in dependency metadata. High-value lead for validator security mechanics if source becomes accessible. |
| `jupnet-bls-sdk` | Private dependency reference | BLS-related JupNet crate named in dependency metadata. Supports the hypothesis that BLS/aggregate-signature components exist in the private runtime stack. |
| `jupnet-bn254` | Private dependency reference | BN254-related JupNet crate named in dependency metadata. Useful cryptographic lead, not JUP utility evidence by itself. |
| `jupnet-merkle-tree` | Private dependency reference | Merkle-related JupNet crate named in dependency metadata. Useful proof/commitment lead, not JUP utility evidence by itself. |
| `jupnet-crosschain-hash` | Private dependency reference | Cross-chain hashing crate named in dependency metadata. Relevant to message/proof plumbing, not decisive for JUP utility. |
| `jupnet-define-syscall` | Private dependency reference | Runtime/syscall-related crate named in dependency metadata. High-value runtime lead if source becomes public. |
| Gum source repository | Not found publicly | On-chain Gum programs, program IDs, transaction flows and Gum-related binary behavior were observed through RPC, but no public Gum source repository owned by Jupiter was located. |
| `jup-ag/docs` | Public | Jupiter developer documentation. Useful ecosystem source, but not observed to expose Gum validator/Dove security source in this investigation. |
| `jup-ag/cli` | Public | Jupiter CLI tooling. Useful for ecosystem investigation and future operational checks. |
| `jup-ag/omnipair-amm-sdk` | Public | Public AMM integration source. It exposes Omnipair pair state, quote math, swap metas, rate model and `futarchy_authority` configuration, but no JUP-denominated validator security mechanism was observed. |
| `jup-ag/platform-list` | Public | Public platform registry. It contains a `gum` platform entry, JupNet social links and a Solana `Bank` / `Bank Program` service, but not Gum implementation source. |
| `jup-ag/chainkit` | Public | Cross-platform crypto/blockchain utility library. README-level inspection did not expose Gum/JupNet validator security or JUP utility. |
| LiteSVM/JupNet dependency metadata | Public metadata, private target | Public dependency metadata referenced `https://github.com/jupnet/jupnet-svm.git` and JupNet-specific crates. This is source-location evidence, not direct source access. |

## Public Crawl

Use the repository crawler to scan public Jupiter repositories for source clues:

```bash
python3 scripts/crawl_jup_ag_public_repos.py
```

Default search terms:

- `gum`
- `dove`
- `jupnet`
- `bls`
- `bn254`
- `merkle`
- `crosschain`
- `proof_hash`
- `inbox`
- `outbox`

Hits from this crawl are clue leads only. They become utility evidence only if they connect JUP to validator/Dove security, signer weights, quorum, fees, governance, access control, slashing, rewards or a permanent protocol sink.

## 2026-07-12 Crawl Findings

The public `jup-ag` crawl scanned 186 public repositories and completed without clone failures. Results were written to:

- [`research/jup-ag-public-repo-crawl-2026-07-12.md`](jup-ag-public-repo-crawl-2026-07-12.md)
- [`research/jup-ag-public-repo-crawl-2026-07-12.json`](jup-ag-public-repo-crawl-2026-07-12.json)

After tightening the crawler to avoid substring false positives:

- `gum` appeared as an exact term in only one repository: `jup-ag/platform-list`.
- `jupnet` appeared as an exact term in only one repository: `jup-ag/platform-list`.
- `proof_hash` was not found.
- `outbox` was not found.
- `inbox` hits were unrelated Arbitrum/Reown UI references.
- `dove` hits were unrelated Dove Swap/BIP39 references.
- `bls`, `bn254`, `merkle` and `crosschain` appeared mostly in generic Solana, Pyth, lockfile or Merkle-distribution contexts.

The `jup-ag/platform-list` hit is useful because it publicly registers:

```text
id: "gum"
name: "GUM"
website: "https://x.com/Jupnet"
twitter: "https://x.com/Jupnet"
tags: ["dex"]
parentId: Jupiter
service: "Global Deposit"
contract: "Bank" at bk1PDAkbHEBGtVRiM94Lzets8gVFP7FgySyfkAc8MPN
program: "Bank Program" at BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ
```

Assessment: this confirms a public Jupiter-maintained registry entry for GUM/JupNet and exposes bank-related Solana addresses to monitor, but it does not expose Gum source code or prove JUP-denominated utility.

Follow-up Bank monitoring found those addresses absent from JupNet RPC but live on Solana mainnet as executable upgradeable-loader programs. Sampled Bank Program transactions exposed inbox/outbox logs and touched USDC/wrapped SOL, not canonical JUP.
