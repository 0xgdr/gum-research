# RPC Catalogue

## Basic health

```bash
curl https://mainnet-beta-rpc.jup.net/ \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"getSlot"}'
```

## Chain identity

```bash
curl https://mainnet-beta-rpc.jup.net/ \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"getIdentity"}'
```

## Validator nodes

```bash
curl https://mainnet-beta-rpc.jup.net/ \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"getClusterNodes"}'
```

## Stake accounts

```bash
curl https://mainnet-beta-rpc.jup.net/ \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc":"2.0",
    "id":1,
    "method":"getProgramAccounts",
    "params":[
      "Stake11111111111111111111111111111111111111",
      {"encoding":"jsonParsed"}
    ]
  }'
```

## Program accounts

```bash
curl https://mainnet-beta-rpc.jup.net/ \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc":"2.0",
    "id":1,
    "method":"getProgramAccounts",
    "params":["<PROGRAM_ID>",{"encoding":"base64"}]
  }'
```

## Transaction history

Use:

```text
getSignaturesForAddress
getTransaction
```

with `maxSupportedTransactionVersion` set appropriately.
