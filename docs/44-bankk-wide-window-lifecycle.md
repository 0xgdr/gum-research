# BankK Wide-Window Lifecycle

## Purpose

The earlier `BankK...` local-id lifecycle analysis used current 41-byte state accounts plus the sampled transaction corpus. This follow-up widened the `BankK...` transaction window to 200 Solana mainnet transactions and tested whether the same Bank-local ids cross into outbox roots, verifier/root fields, JUP, validators, vote accounts or stake accounts.

The goal was to reduce the small-sample objection. If `BankK...` local ids are part of the public validator-security path, a wider contiguous window should have a better chance of exposing them in `jnoUtn...` outbox payloads, root-update slots, verifier fields or security-key material.

## Evidence

- Report: `evidence/2026-07-12-bank-live-rpc/bankk-wide-window-lifecycle.md`
- Signatures: `evidence/2026-07-12-bank-live-rpc/solana-mainnet-bank-program-wide-window-signatures.json`
- Manifest: `evidence/2026-07-12-bank-live-rpc/solana-mainnet-bank-program-wide-window-manifest.json`
- Created-account state fetch: `evidence/2026-07-12-bank-live-rpc/solana-mainnet-getMultipleAccounts-BankKWideWindowCreatedAccounts.json`

## Scripts

- `scripts/collect_bank_withdrawal_cohort.py`
- `scripts/collect_bankk_window_created_accounts.py`
- `scripts/analyze_bankk_wide_window_lifecycle.py`

Example manual workflow:

```bash
python3 scripts/collect_bank_withdrawal_cohort.py \
  evidence/YYYY-MM-DD-live-rpc \
  --address BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ \
  --output-prefix bank-program-wide-window \
  --signature-limit 200 \
  --transaction-limit 200

python3 scripts/collect_bankk_window_created_accounts.py \
  evidence/YYYY-MM-DD-live-rpc \
  --input-prefix bank-program-wide-window

python3 scripts/analyze_bankk_wide_window_lifecycle.py \
  evidence/YYYY-MM-DD-live-rpc \
  > evidence/YYYY-MM-DD-live-rpc/bankk-wide-window-lifecycle.md
```

This is intentionally a manual workflow for now because it fetches a much larger Solana mainnet transaction window than the default monitor.

## Findings

The 200-transaction window covered slots `432700510` to `432724705`, a span of `24195` slots.

The run fetched current state for 155 accounts created in the wide `BankK...` window. All 155 were closed by the time current account state was fetched, so no durable current-state bytes remained for those accounts. The analyzer therefore recovered additional Bank-local id candidates from transaction payload offsets:

- operation payload offset `16`;
- `VerifyRequest` payload offset `54`.

This produced:

- `194` local ids analyzed;
- `175` payload-derived local ids;
- `175` local ids seen in `BankK...` raw payloads;
- `69` local ids seen in `JNiN...` inbox raw payloads;
- `138` local ids seen in `VerifyRequest` rows;
- `69` local ids with operation plus verify lifecycle evidence;
- `52` local ids with same-slot operation plus verify evidence.

The same wider sample still produced:

- `0` local ids seen in `jnoUtn...` outbox raw payloads;
- `0` local ids matching decoded request fields;
- `0` local ids matching verifier/root fields;
- `0` local ids matching canonical JUP, current validators, vote accounts or stake accounts;
- `0` local ids sharing a slot with root updates.

## Interpretation

This is meaningful progress, but it is not proof of JUP utility.

The stronger positive result is that `BankK...` local ids are not random one-off state artifacts. Across a contiguous 200-transaction window, they repeatedly bridge Bank operation payloads, inbox helper payloads and `VerifyRequest` payloads. That makes them a real Bank-layer lifecycle handle.

The stronger negative result is that the handle still does not cross the public security boundary. In this wider window, it does not appear in outbox payloads, verifier/root fields, root-update slots, decoded `bk1PDA...` request fields, canonical JUP or current validator/vote/stake material.

The current evidence therefore supports this model:

- `BankK...` exposes a public Bank-local message/request lifecycle;
- `JNiN...` participates in the inbox side of that lifecycle;
- `VerifyRequest` ties Bank-local activity to the public proof-checking path;
- the root-builder, Dove/JUP weight source and aggregate-key producer side remain outside the public data recovered so far.

This reduces the likelihood that the missing JUP/Dove/security evidence is merely hidden in a small unrepresentative `BankK...` sample. It does not disprove a private or off-chain JUP-weighted security system.
