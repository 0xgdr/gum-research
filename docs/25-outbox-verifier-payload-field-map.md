# Outbox Verifier Payload Field Map

## Purpose

The public JupNet article says outbox verification receives:

```text
message hash
JupNet sender program id
epoch
aggregated BLS public key
aggregated BLS signature
Merkle proof
```

Earlier reports proved the root-update path. This pass maps ordinary Bank/outbox verification payloads to that argument shape.

Report:

```text
evidence/2026-07-12-bank-live-rpc/outbox-verifier-payload-field-map.md
```

Script:

```text
scripts/map_outbox_verifier_payloads.py
```

## Result

The sampled inner outbox verifier payload decodes as:

| Offset | Length | Field |
|---:|---:|---|
| `0` | 1 | tag, observed `0` |
| `1` | 32 | message hash |
| `33` | 32 | sender/program id candidate |
| `65` | 8 | epoch, little-endian u64 |
| `73` | 64 | aggregate-key material |
| `137` | 32 | compact signature/verifier field |
| `169` | 4 | Merkle path bitmap |
| `173` | 4 | Merkle proof count |
| `177` | 160 | five 32-byte proof nodes |

Parsed rows:

| Metric | Value |
|---|---:|
| Verifier payloads parsed | `21` |
| Bank wrapper payloads | `10` |
| Inner outbox payloads | `11` |
| Payloads that recompute to stored root | `21` |
| Payloads with canonical JUP key hit | `0` |
| Payloads with current validator/vote/stake key hit | `0` |

## Sender Program Lead

The sender/program candidate in every parsed inner outbox verifier payload is:

```text
GUMebNDCYyF81xjyqaHagbgMQVUTb8fBC9YRh25xSH64
```

That account exists on JupNet as an upgradeable executable. It became the next investigation target in:

```text
docs/26-gum-omnichain-sender-program.md
```

## What This Adds

This is a direct field-level match to the article's outbox interface, not just a high-level architectural match.

```text
message hash
  -> sender/program id
  -> epoch
  -> aggregate key
  -> compact signature/verifier field
  -> Merkle proof
  -> stored outbox root
```

Every parsed payload recomputes to the stored root for its epoch using the same `0x00` leaf and `0x01` parent hash formulas.

## Utility Boundary

This still does not prove JUP secures the verifier.

The payloads prove that Gum/outbox messages are certified by an aggregate-key Merkle proof. They do not expose:

- individual Dove identities;
- individual BLS public keys;
- JUP balances;
- stake weights;
- slashing/reward state;
- the rule that produced the aggregate key.
