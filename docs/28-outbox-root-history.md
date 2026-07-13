# Outbox Root History

## Purpose

This pass looks for changes in public outbox root/update material over a wider transaction window.

The target question is whether aggregate-key or root changes reveal anything about the hidden producer side:

```text
Dove/JUP/stake state
  -> aggregate keys
  -> epoch roots
```

Report:

```text
evidence/2026-07-12-bank-live-rpc/outbox-root-history.md
```

Scripts:

```text
scripts/collect_outbox_root_history.py
scripts/analyze_outbox_root_history.py
```

## Scope

| Metric | Value |
|---|---:|
| Outbox transaction files scanned | `120` |
| Root-update payloads decoded | `1` |
| Inner verifier payloads decoded | `19` |
| Current vote accounts in snapshot | `7` |
| Current stake accounts in snapshot | `7` |
| Canonical JUP / validator / vote / stake key hits | `0` |

## Root Update Observed

| Field | Value |
|---|---|
| Time | `2026-07-12T21:25:50Z` |
| Slot | `432511387` |
| Epoch/root slot | `271` |
| Root | `6928957b2ea436bcc9c44970a0f85364b6f0c8e5e4e886565eea061c9bd8d999` |
| Aggregate-key material | `87e930814a0131f70e4b405f4e30ca3e226ad5bee2e5e40d584947d48c4bcceb15f96af18671975c31abc6d2c3ea8230ee775da12cd69b5331e35865ad2c4025` |
| Compact verifier field | `1936cf6325733174d35ff22f86bebabdf33abd441315398d8d4b61313eda628d` |
| Path bitmap | `18` |
| Proof nodes | `5` |
| Recomputed root match | `true` |

## Change Signals

| Signal | Result |
|---|---|
| Root-update roots | `1` unique value |
| Root-update aggregate keys | `1` unique value |
| Root-update compact verifier fields | `1` unique value |
| Verifier recomputed roots | `1` unique value |
| Verifier aggregate keys | `3` unique values |

The ordinary verifier payloads showed three aggregate-key values, but all recomputed to the same stored root.

## Interpretation

The public history window still supports the compact-verifier model:

```text
aggregate-key material
  -> Merkle proof
  -> stored epoch root
```

It does not reveal the producer source:

```text
Dove set + JUP/stake weights
  -> aggregate-key set
```

The useful negative result remains:

```text
0 decoded rows exposed canonical JUP, current validator keys, vote accounts or stake accounts.
```

## Limitation

This pass correlates against the current validator/stake snapshot only. To prove root changes line up with validator or stake changes, we need multiple snapshots captured at different dates, each with:

- current validator/vote/stake state;
- outbox root-history transactions;
- verifier payload field map;
- executable census hashes.
