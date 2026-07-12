# JupNet Helper Program State

## Scope

This pass enumerated accounts owned by the Solana-side JupNet inbox and outbox helper programs.

Generated files:

```text
evidence/2026-07-12-bank-live-rpc/solana-mainnet-getProgramAccounts-JupNetInboxProgram.json
evidence/2026-07-12-bank-live-rpc/solana-mainnet-getProgramAccounts-JupNetOutboxProgram.json
evidence/2026-07-12-bank-live-rpc/jupnet-helper-program-accounts.md
```

Scripts:

```text
scripts/collect_jupnet_helper_program_accounts.py
scripts/analyze_jupnet_helper_program_accounts.py
```

## Result

Only two helper-owned accounts were present in the sampled Solana mainnet state:

| Program | Account | Space | Meaning |
|---|---|---:|---|
| Inbox helper | `9DvDdsw38EB3RPChPqHkgBmntFbM5v79QxMyMSbfXWuy` | 64 | Inbox counter/state candidate |
| Outbox helper | `3C1LxtpR3Mh5RQjydfeQdvRaAzpStWM7gBi1XzP9oyGt` | 320 | Merkle root history |

Negative checks:

| Check | Result |
|---|---:|
| Canonical JUP key hits | 0 accounts |
| Current JupNet validator/vote/stake key hits | 0 accounts |

## Outbox State

The 320-byte outbox account decodes as repeated 40-byte entries:

```text
u64 epoch
[u8; 32] merkle_root
```

Observed non-empty entries:

| Offset | Epoch | Merkle root |
|---:|---:|---|
| 0 | 271 | `6928957b2ea436bcc9c44970a0f85364b6f0c8e5e4e886565eea061c9bd8d999` |
| 40 | 270 | `6928957b2ea436bcc9c44970a0f85364b6f0c8e5e4e886565eea061c9bd8d999` |
| 80 | 269 | `6928957b2ea436bcc9c44970a0f85364b6f0c8e5e4e886565eea061c9bd8d999` |

This matches the outbox binary strings:

- `merkle_root_state`
- `UpdateMerkleRoot invoked`
- `Merkle proof verified`
- `VerifyOutboxMessage invoked`
- `advance_epoch_root: dropped root of epoch`

## Assessment

This is meaningful progress because it identifies what the public outbox state stores: Merkle root history.

It also narrows the unresolved security question. The public helper-owned state does not appear to store:

- JUP stake;
- validator/vote/stake accounts;
- signer-set membership;
- signer weights;
- quorum thresholds;
- slashing, reward or fee state.

The BLS signer set or quorum source is therefore likely one of:

- supplied inside instruction payloads;
- verified against a hardcoded or private runtime/operator configuration;
- stored in another account not owned by these helper programs;
- controlled by off-chain Dove/operator infrastructure;
- present in private `jupnet-svm` code rather than public Solana state.

The next decisive technical target is `verify_request` payload reconstruction, because the public outbox account gives Merkle roots but not the signer set.
