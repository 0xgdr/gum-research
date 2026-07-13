# Security Boundary Corpus

## Purpose

This pass tests the public boundary where hidden JupNet/Dove security material would have to meet Solana-visible Gum verification.

It combines:

- helper-program-owned inbox/outbox account layouts;
- every locally saved Solana Bank/outbox/history transaction body;
- decoded verifier payload roots, aggregate keys, senders, proof layouts and key-hit checks.

## Helper-Owned Account Layouts

- Helper accounts decoded: `2`
- Helper accounts with canonical JUP / validator / vote / stake hits: `0`

| Program | Space | Discriminator | Count |
|---|---:|---|---:|
| `JupNetInboxProgram` | 64 | `dae4000000000000` | 1 |
| `JupNetOutboxProgram` | 320 | `0f01000000000000` | 1 |

| Program | Account | Space | SHA256 | Root-like entries | U64 candidates | Aligned 32-byte chunks |
|---|---|---:|---|---|---|---|
| `JupNetInboxProgram` | `9DvDdsw38EB3RPChPqHkgBmntFbM5v79QxMyMSbfXWuy` | 64 | `c465bb9d8dfc1d2b6cc1ff9e07a705b8999c1cfa10c18ca8e3e6eb8473bb863c` | `None` | `0:58586` | `0:FjTXJajSNwauBJbvHeuS1yWBP5xXrhmzr4pe1YZ8ki2T` |
| `JupNetOutboxProgram` | `3C1LxtpR3Mh5RQjydfeQdvRaAzpStWM7gBi1XzP9oyGt` | 320 | `bd064d929ac0f29ac717e449f3e967eace574480879607e104d7f083b2e97cbd` | `offset 0: epoch 271, root 6928957b2ea436bcc9c44970a0f85364b6f0c8e5e4e886565eea061c9bd8d999`<br>`offset 40: epoch 270, root 6928957b2ea436bcc9c44970a0f85364b6f0c8e5e4e886565eea061c9bd8d999`<br>`offset 80: epoch 269, root 6928957b2ea436bcc9c44970a0f85364b6f0c8e5e4e886565eea061c9bd8d999` | `0:271`<br>`40:270`<br>`80:269` | `0:21ZzzZvhM7vXwQkomseUFhWjY9tnVz7ddQC8smHAJnkD`<br>`32:7PWJ92fedBPxFvCDYAsoUUHeGJXHdqhgsX2joj1PiiFm`<br>`64:DK89qBQFThRxuy4i66qp1eeaAZsbbs8s3RRuwkyMcBbh`<br>`96:EacYaDceiDK3zeJo3kaA2yLtNwW6ZTNPPa7EF4EhCNTH` |

### Helper Layout Assessment

- No helper-owned account exposed canonical JUP, current validator, vote or stake account bytes/text.
- The public outbox helper account still presents as epoch/root storage rather than a signer-set, quorum or stake-weight registry.
- No helper-owned account in this snapshot had an obvious sequence of current validator/vote/stake keys paired with small integer weights.

## Verifier Payload Corpus

- Transaction files available: `128`
- Transaction files with decoded verifier payloads: `21`
- Decoded verifier payloads: `42`
- Time range: `2026-07-12T18:00:48+00:00` -> `2026-07-13T05:32:18+00:00`
- Slot range: `432481451` -> `432582489`
- Root mismatches against stored outbox roots: `0`
- Payloads with canonical JUP / validator / vote / stake hits: `0`

| Group | Values |
|---|---|
| Payload kinds | `bank-verify-wrapper: 21`<br>`inner-outbox: 21` |
| Epochs | `270: 38`<br>`269: 4` |
| Sender/program ids | `None: 21`<br>`GUMebNDCYyF81xjyqaHagbgMQVUTb8fBC9YRh25xSH64: 21` |
| Aggregate keys | `87e930814a0131f70e4b405f4e30ca3e...: 38`<br>`257ff69e3a7757268a94f2908f6462f4...: 2`<br>`05eebac3af7909fd6e3349703ebbe4c0...: 2` |
| Recomputed roots | `6928957b2ea436bcc9c44970a0f85364b6f0c8e5e4e886565eea061c9bd8d999: 42` |
| Compact signature/verifier fields | `9e7d4e0079fa4c05a493c4733893b9a0...: 2`<br>`284da295e350bc7b882c3398ec4342dc...: 2`<br>`8bd60de45a6294291cc64f84188542eb...: 2`<br>`282052314e4ad9b7a235d18dba848953...: 2`<br>`0a5a0d038887e45dbbc77102819ca981...: 2`<br>`9397f2faf599dec3cbb186941e925de6...: 2`<br>`85f2d7754dfbf4ccd68640eae635ec05...: 2`<br>`3009cc42f3962bfe2c4c51dafbb7723a...: 2`<br>`9835012a5a752b2efde4f7fbf3fa312e...: 2`<br>`972c3f8e240add68359efd1a9fb66618...: 2`<br>`168f8408225dcf42a1e0019e06cb31a5...: 2`<br>`a9a1259e3a7da931a9d48917942578bf...: 2` |
| Proof layouts | `inner-outbox len=337 aggregate=73 bitmap=18 proof=5: 19`<br>`bank-verify-wrapper len=463 aggregate=199 bitmap=18 proof=5: 11`<br>`bank-verify-wrapper len=496 aggregate=232 bitmap=18 proof=5: 8`<br>`bank-verify-wrapper len=463 aggregate=199 bitmap=11 proof=5: 1`<br>`inner-outbox len=337 aggregate=73 bitmap=11 proof=5: 1`<br>`bank-verify-wrapper len=496 aggregate=232 bitmap=5 proof=5: 1`<br>`inner-outbox len=337 aggregate=73 bitmap=5 proof=5: 1` |

### Verifier Boundary Transitions

- `2026-07-12T18:00:48+00:00 slot 432481451 epoch 269 sender None aggregate 87e930814a0131f70e4b405f4e30ca3e... root 6928957b2ea436bcc9c44970a0f85364... bitmap 18 proof 5`
- `2026-07-12T18:00:48+00:00 slot 432481451 epoch 269 sender GUMebNDCYyF81xjyqaHagbgMQVUTb8fBC9YRh25xSH64 aggregate 87e930814a0131f70e4b405f4e30ca3e... root 6928957b2ea436bcc9c44970a0f85364... bitmap 18 proof 5`
- `2026-07-12T18:04:26+00:00 slot 432481982 epoch 269 sender None aggregate 87e930814a0131f70e4b405f4e30ca3e... root 6928957b2ea436bcc9c44970a0f85364... bitmap 18 proof 5`
- `2026-07-12T18:04:26+00:00 slot 432481982 epoch 269 sender GUMebNDCYyF81xjyqaHagbgMQVUTb8fBC9YRh25xSH64 aggregate 87e930814a0131f70e4b405f4e30ca3e... root 6928957b2ea436bcc9c44970a0f85364... bitmap 18 proof 5`
- `2026-07-12T21:10:51+00:00 slot 432509203 epoch 270 sender None aggregate 87e930814a0131f70e4b405f4e30ca3e... root 6928957b2ea436bcc9c44970a0f85364... bitmap 18 proof 5`
- `2026-07-12T21:10:51+00:00 slot 432509203 epoch 270 sender GUMebNDCYyF81xjyqaHagbgMQVUTb8fBC9YRh25xSH64 aggregate 87e930814a0131f70e4b405f4e30ca3e... root 6928957b2ea436bcc9c44970a0f85364... bitmap 18 proof 5`
- `2026-07-12T21:13:40+00:00 slot 432509620 epoch 270 sender None aggregate 87e930814a0131f70e4b405f4e30ca3e... root 6928957b2ea436bcc9c44970a0f85364... bitmap 18 proof 5`
- `2026-07-12T21:13:40+00:00 slot 432509620 epoch 270 sender GUMebNDCYyF81xjyqaHagbgMQVUTb8fBC9YRh25xSH64 aggregate 87e930814a0131f70e4b405f4e30ca3e... root 6928957b2ea436bcc9c44970a0f85364... bitmap 18 proof 5`
- `2026-07-12T21:15:21+00:00 slot 432509862 epoch 270 sender None aggregate 87e930814a0131f70e4b405f4e30ca3e... root 6928957b2ea436bcc9c44970a0f85364... bitmap 18 proof 5`
- `2026-07-12T21:15:21+00:00 slot 432509862 epoch 270 sender GUMebNDCYyF81xjyqaHagbgMQVUTb8fBC9YRh25xSH64 aggregate 87e930814a0131f70e4b405f4e30ca3e... root 6928957b2ea436bcc9c44970a0f85364... bitmap 18 proof 5`
- `2026-07-12T21:15:33+00:00 slot 432509888 epoch 270 sender None aggregate 87e930814a0131f70e4b405f4e30ca3e... root 6928957b2ea436bcc9c44970a0f85364... bitmap 18 proof 5`
- `2026-07-12T21:15:33+00:00 slot 432509888 epoch 270 sender GUMebNDCYyF81xjyqaHagbgMQVUTb8fBC9YRh25xSH64 aggregate 87e930814a0131f70e4b405f4e30ca3e... root 6928957b2ea436bcc9c44970a0f85364... bitmap 18 proof 5`
- `2026-07-12T21:15:49+00:00 slot 432509927 epoch 270 sender None aggregate 87e930814a0131f70e4b405f4e30ca3e... root 6928957b2ea436bcc9c44970a0f85364... bitmap 18 proof 5`
- `2026-07-12T21:15:49+00:00 slot 432509927 epoch 270 sender GUMebNDCYyF81xjyqaHagbgMQVUTb8fBC9YRh25xSH64 aggregate 87e930814a0131f70e4b405f4e30ca3e... root 6928957b2ea436bcc9c44970a0f85364... bitmap 18 proof 5`
- `2026-07-12T21:30:24+00:00 slot 432512054 epoch 270 sender None aggregate 87e930814a0131f70e4b405f4e30ca3e... root 6928957b2ea436bcc9c44970a0f85364... bitmap 18 proof 5`
- `2026-07-12T21:30:24+00:00 slot 432512054 epoch 270 sender GUMebNDCYyF81xjyqaHagbgMQVUTb8fBC9YRh25xSH64 aggregate 87e930814a0131f70e4b405f4e30ca3e... root 6928957b2ea436bcc9c44970a0f85364... bitmap 18 proof 5`
- `2026-07-12T21:30:32+00:00 slot 432512072 epoch 270 sender None aggregate 87e930814a0131f70e4b405f4e30ca3e... root 6928957b2ea436bcc9c44970a0f85364... bitmap 18 proof 5`
- `2026-07-12T21:30:32+00:00 slot 432512072 epoch 270 sender GUMebNDCYyF81xjyqaHagbgMQVUTb8fBC9YRh25xSH64 aggregate 87e930814a0131f70e4b405f4e30ca3e... root 6928957b2ea436bcc9c44970a0f85364... bitmap 18 proof 5`
- `2026-07-12T21:30:36+00:00 slot 432512081 epoch 270 sender None aggregate 05eebac3af7909fd6e3349703ebbe4c0... root 6928957b2ea436bcc9c44970a0f85364... bitmap 5 proof 5`
- `2026-07-12T21:30:36+00:00 slot 432512081 epoch 270 sender GUMebNDCYyF81xjyqaHagbgMQVUTb8fBC9YRh25xSH64 aggregate 05eebac3af7909fd6e3349703ebbe4c0... root 6928957b2ea436bcc9c44970a0f85364... bitmap 5 proof 5`
- `2026-07-12T21:30:51+00:00 slot 432512119 epoch 270 sender None aggregate 87e930814a0131f70e4b405f4e30ca3e... root 6928957b2ea436bcc9c44970a0f85364... bitmap 18 proof 5`
- `2026-07-12T21:30:51+00:00 slot 432512119 epoch 270 sender GUMebNDCYyF81xjyqaHagbgMQVUTb8fBC9YRh25xSH64 aggregate 87e930814a0131f70e4b405f4e30ca3e... root 6928957b2ea436bcc9c44970a0f85364... bitmap 18 proof 5`
- `2026-07-13T05:04:24+00:00 slot 432578402 epoch 270 sender None aggregate 87e930814a0131f70e4b405f4e30ca3e... root 6928957b2ea436bcc9c44970a0f85364... bitmap 18 proof 5`
- `2026-07-13T05:04:24+00:00 slot 432578402 epoch 270 sender GUMebNDCYyF81xjyqaHagbgMQVUTb8fBC9YRh25xSH64 aggregate 87e930814a0131f70e4b405f4e30ca3e... root 6928957b2ea436bcc9c44970a0f85364... bitmap 18 proof 5`
- `2026-07-13T05:15:23+00:00 slot 432580024 epoch 270 sender None aggregate 87e930814a0131f70e4b405f4e30ca3e... root 6928957b2ea436bcc9c44970a0f85364... bitmap 18 proof 5`
- `2026-07-13T05:15:23+00:00 slot 432580024 epoch 270 sender GUMebNDCYyF81xjyqaHagbgMQVUTb8fBC9YRh25xSH64 aggregate 87e930814a0131f70e4b405f4e30ca3e... root 6928957b2ea436bcc9c44970a0f85364... bitmap 18 proof 5`
- `2026-07-13T05:15:40+00:00 slot 432580064 epoch 270 sender None aggregate 87e930814a0131f70e4b405f4e30ca3e... root 6928957b2ea436bcc9c44970a0f85364... bitmap 18 proof 5`
- `2026-07-13T05:15:40+00:00 slot 432580064 epoch 270 sender GUMebNDCYyF81xjyqaHagbgMQVUTb8fBC9YRh25xSH64 aggregate 87e930814a0131f70e4b405f4e30ca3e... root 6928957b2ea436bcc9c44970a0f85364... bitmap 18 proof 5`
- `2026-07-13T05:15:51+00:00 slot 432580091 epoch 270 sender None aggregate 87e930814a0131f70e4b405f4e30ca3e... root 6928957b2ea436bcc9c44970a0f85364... bitmap 18 proof 5`
- `2026-07-13T05:15:51+00:00 slot 432580091 epoch 270 sender GUMebNDCYyF81xjyqaHagbgMQVUTb8fBC9YRh25xSH64 aggregate 87e930814a0131f70e4b405f4e30ca3e... root 6928957b2ea436bcc9c44970a0f85364... bitmap 18 proof 5`
- Additional transitions omitted: `12`

### Corpus Assessment

- No decoded verifier payload or account list exposed canonical JUP, current validator, vote or stake account material.
- The larger local corpus still exposes aggregate-key/proof verification state, not the producer-side Dove/JUP/stake source used to build that aggregate-key set.
- The most useful future signal is a transition where aggregate keys or roots change near a validator/stake snapshot change.

## Bottom Line

- Public helper accounts and verifier payloads still support the BLS/Merkle verifier model.
- They do not currently expose a JUP-denominated stake table, Dove signer registry, validator-key registry, quorum threshold or weight mapping.
- This narrows the likely hiding place to private runtime/source, private off-chain epoch construction, or a public account layout not yet reachable from the sampled helper/Bank/outbox surface.
