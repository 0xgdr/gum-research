# Runtime and Cryptographic Components

## Native programs

NativeLoader-owned accounts included familiar Solana programs and JupNet-labelled loader strings.

Examples:

```text
jupnet_bpf_loader_program
jupnet_bpf_loader_upgradeable_program
jupnet_bpf_loader_deprecated_program
```

This is direct evidence that JupNet is not simply an untouched Solana node deployment.

## Public dependency metadata

The public LiteSVM-related lockfile referenced a private repository:

```text
https://github.com/jupnet/jupnet-svm.git
```

at commit:

```text
e0f0c00427b3b52e7a744cef7dcff21a7df3e0c4
```

JupNet-specific crates referenced in dependency metadata included:

- `jupnet-bls-sdk`
- `jupnet-alt-bn128-bls`
- `jupnet-bn254`
- `jupnet-merkle-tree`
- `jupnet-define-syscall`
- `jupnet-crosschain-hash`
- `jupnet-vote`
- `jupnet-vote-program`

## Important inference

The runtime and program dependency graph strongly supports BLS/BN254 and Merkle-based verification within JupNet's customised stack.

However, dependency presence does not alone prove:

- which messages are signed;
- who signs;
- how signers are weighted;
- whether weighting comes from JUP;
- whether the functionality is active in the current beta.

## Private source boundary

The referenced `jupnet-svm` repository was not publicly cloneable at the time of investigation. A follow-up GitHub API check for `jupnet/jupnet-svm` returned `404` on 2026-07-12, so this remains a source boundary rather than an inspectable public dependency.

This prevents direct inspection of:

- validator consensus logic;
- committee selection;
- stake-weight calculation;
- BLS aggregation;
- quorum enforcement.
