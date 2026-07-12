# JupNet Helper Program Accounts

## Scope

- Inbox helper program: `JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw`
- Outbox helper program: `jnoUtncGR9ZCCMixtys6Gzy5coTo6mnmUZuEHRQFTFV`
- Inbox-owned accounts fetched: `1`
- Outbox-owned accounts fetched: `1`
- Inbox program signature-window count: `20`
- Outbox program signature-window count: `20`
- Accounts with canonical JUP hits: `0`
- Accounts with current JupNet validator/vote/stake key hits: `0`

## Layout Groups

| Program | Space | Discriminator | Count |
|---|---:|---|---:|
| `JupNetInboxProgram` | 64 | `dae4000000000000` | 1 |
| `JupNetOutboxProgram` | 320 | `0f01000000000000` | 1 |

## Account Rows

| Program | Account | Space | Discriminator | SHA256 | Key hits | Term hits | Likely pubkey chunks | Small numbers |
|---|---|---:|---|---|---|---|---|---|
| `JupNetInboxProgram` | `9DvDdsw38EB3RPChPqHkgBmntFbM5v79QxMyMSbfXWuy` | 64 | `dae4000000000000` | `c465bb9d8dfc1d2b6cc1ff9e07a705b8999c1cfa10c18ca8e3e6eb8473bb863c` | `None` | `None` | `None` | `None` |
| `JupNetOutboxProgram` | `3C1LxtpR3Mh5RQjydfeQdvRaAzpStWM7gBi1XzP9oyGt` | 320 | `0f01000000000000` | `bd064d929ac0f29ac717e449f3e967eace574480879607e104d7f083b2e97cbd` | `None` | `None` | `8:85VhemNvPD41eb23MFcFkZ9qc8i53vnmb2dQQeNTfQJL`<br>`40:wfbM5CcTHRpXidqGNP2MmmWH9L1o31j3XtFNZyAaz5s`<br>`72:7PWJ92fedBPxAdX2QrTdEmm6g4TRvXjPdBbSvgysXvyq`<br>`104:DK89qBQFThRxuy4i66qp1ecy2jMkEXJmK35uGTjYgjX5` | `40:270`<br>`80:269` |

## Decoded State Hints

- `9DvDdsw38EB3RPChPqHkgBmntFbM5v79QxMyMSbfXWuy` inbox counter/value candidate: `58586`
- `3C1LxtpR3Mh5RQjydfeQdvRaAzpStWM7gBi1XzP9oyGt` outbox Merkle root entries:
  - `offset 0: epoch 271, root 6928957b2ea436bcc9c44970a0f85364b6f0c8e5e4e886565eea061c9bd8d999`
  - `offset 40: epoch 270, root 6928957b2ea436bcc9c44970a0f85364b6f0c8e5e4e886565eea061c9bd8d999`
  - `offset 80: epoch 269, root 6928957b2ea436bcc9c44970a0f85364b6f0c8e5e4e886565eea061c9bd8d999`

## Assessment

- Helper-program-owned accounts did not expose canonical Solana JUP key material in this snapshot.
- Helper-program-owned accounts did not expose current JupNet validator, vote or stake account keys in this snapshot.
- The outbox-owned account decodes as Merkle root history, not an obvious signer-set, quorum or stake-weight registry.
- If signer-set or quorum state is public, it is not obvious from direct key hits or helper-program-owned account layouts in this snapshot.
