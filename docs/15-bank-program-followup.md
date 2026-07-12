# Bank Program Follow-up

## Why This Matters

The public `jup-ag/platform-list` crawl exposed a GUM registry entry with a `Global Deposit` service and two Solana-labelled addresses:

```text
Bank:
bk1PDAkbHEBGtVRiM94Lzets8gVFP7FgySyfkAc8MPN

Bank Program:
BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ
```

This is the best public-code clue found so far because it names GUM/JupNet and points to live infrastructure.

## JupNet RPC Result

The 2026-07-12 Bank-enabled JupNet snapshot found:

- Bank account on JupNet RPC: not present.
- Bank Program on JupNet RPC: not present.
- Bank signatures on JupNet RPC: 0.
- Bank Program signatures on JupNet RPC: 0.
- Gum/Bank signature overlap on JupNet RPC: 0.
- Gum/Bank Program signature overlap on JupNet RPC: 0.

Interpretation: the `platform-list` Bank addresses are not JupNet-side accounts on the configured JupNet RPC endpoint.

## Solana Mainnet Result

The same addresses are live executable accounts on Solana mainnet.

| Account | ProgramData | Deployment slot | Upgrade authority |
|---|---|---:|---|
| `bk1PDAkbHEBGtVRiM94Lzets8gVFP7FgySyfkAc8MPN` | `5ERop4TJtnRXpyUdRYuTfwWaxRTRTcb97An1jRAqa15L` | `425956918` | `F5p1mBd6C3v6NB2oLGM9bLKmtHQ53RMsYKeGPPg4s113` |
| `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ` | `4KsDDc7zoiShDXepLMu246anaW9uGxYPdgsgG2BX9L36` | `432453318` | `GRr146QcbpANhTZPCo9QBJa1tP5Fr9B6vfua4zRC5cc3` |

The latest sampled Bank Program signature was observed at Solana slot `432481982`, with block time `2026-07-12T18:04:26+00:00`.

## Sampled Transaction Evidence

Eight recent Solana mainnet Bank Program transactions were sampled.

Observed signers:

- `JUPW3tHBxmNRzVnLmTyYUsUDB6izZSEtupY6znBC5mo`: 6 sampled transactions.
- `rfQMFpNueeNufBW4byyEAhvL4To4tCsVBVagcEWG8ea`: 2 sampled transactions.

Observed utility-relevant logs:

```text
Program log: SubmitInboxMessageWithFinality invoked
Program log: VerifyOutboxMessage invoked
Program log: Outbox verification passed
```

Observed parsed token mints:

- USDC: `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v`
- Wrapped SOL: `So11111111111111111111111111111111111111112`

Canonical Solana JUP mint account-key hits in the sampled Bank Program transactions:

```text
0
```

## Assessment

This is a strong cross-chain message-passing lead. The Bank Program appears to operate Solana-side inbox/outbox verification for GUM/JupNet deposit or message flow.

It still does not prove JUP-denominated utility:

- no canonical JUP account key was present in the sampled Bank Program transactions;
- sampled parsed token mints were USDC and wrapped SOL;
- no validator, Dove, stake-weight, quorum, slashing, reward, governance or JUP fee/sink mechanism was observed in the sampled Bank surface.

The next useful evidence would be:

- a decoded Bank Program IDL or source leak;
- transactions where Bank Program handles canonical JUP;
- Bank account state that maps messages to validators, Doves, signers or quorum proofs;
- a link between the Solana-side Bank Program and the private `jupnet-svm` vote/BLS crates.
