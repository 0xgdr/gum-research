# Outbox Root History Analysis

## Scope

- Snapshot: `evidence/2026-07-12-bank-live-rpc`
- Transaction files scanned: `120`
- Root-update payloads decoded: `1`
- Inner verifier payloads decoded: `19`
- Current vote accounts in snapshot: `7`
- Current stake accounts in snapshot: `7`
- Current unique delegated native stake values: `[999999997717120]`
- Root/update or verifier rows with canonical JUP / validator / vote / stake key hits: `0`

## Root Update Timeline

| Time | Slot | Epoch | Root | Aggregate key | Compact verifier field | Bitmap | Proof nodes | Root match | Key hits |
|---|---:|---:|---|---|---|---:|---:|---|---|
| `2026-07-12T21:25:50+00:00` | 432511387 | 271 | `6928957b2ea436bc...` | `87e930814a0131f7...` | `1936cf6325733174...` | 18 | 5 | `True` | `None` |

## Root Update Groups

| Group | Unique count | Values |
|---|---:|---|
| Roots | 1 | `6928957b2ea436bcc9c44970a0f85364b6f0c8e5e4e886565eea061c9bd8d999: 1` |
| Aggregate keys | 1 | `87e930814a0131f70e4b405f4e30ca3e...: 1` |
| Compact verifier fields | 1 | `1936cf6325733174d35ff22f86bebabd...: 1` |

## Verifier Context Groups

| Group | Unique count | Values |
|---|---:|---|
| Verifier recomputed roots | 1 | `6928957b2ea436bcc9c44970a0f85364b6f0c8e5e4e886565eea061c9bd8d999: 19` |
| Verifier aggregate keys | 3 | `257ff69e3a7757268a94f2908f6462f4...: 1`<br>`87e930814a0131f70e4b405f4e30ca3e...: 17`<br>`05eebac3af7909fd6e3349703ebbe4c0...: 1` |

## Change Signals

- Root-update material was stable within the fetched history window.
- Verifier aggregate-key material changed within ordinary verification payloads.
- No decoded root-update or verifier row exposed canonical JUP, current validator, vote or stake keys.

## Assessment

- This history pass compares public root/update proof material over a wider outbox transaction window.
- It can identify changes in epoch root, aggregate key, compact verifier field and proof path, but it only correlates against the current validator/stake snapshot unless older validator snapshots are supplied separately.
- A stable root/aggregate-key history does not disprove JUP utility, but it gives no public evidence of live stake-weight churn.
- A future change that introduces JUP/validator/stake key material or root/key changes around validator/stake changes would be a high-value signal.
