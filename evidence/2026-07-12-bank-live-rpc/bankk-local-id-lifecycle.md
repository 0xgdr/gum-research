# BankK Local ID Lifecycle

## Scope

- 41-byte local ids analyzed: `19`
- Local ids with sampled lifecycle events: `18`
- Local ids seen in `BankK...` raw payloads: `18`
- Local ids seen in `JNiN...` inbox raw payloads: `18`
- Local ids seen in `jnoUtn...` outbox raw payloads: `0`
- Local ids seen in `VerifyRequest` rows: `18`
- Local ids with operation + verify lifecycle evidence: `18`
- Local ids with same-slot operation + verify evidence: `12`
- Local ids matching decoded `bk1PDA...` request fields: `0`
- Local ids matching verifier/root fields: `0`
- Local ids matching canonical JUP / validator / vote / stake keys: `0`
- Local ids sharing a slot with root updates: `0`

## Lifecycle Rows

| State account | Local id | Phases | Payload programs | Same-slot operation/verify | Closest root-update slot delta | Decoded request hits | Verifier/root hits | Security hits | Events |
|---|---|---|---|---|---:|---|---|---|---|
| `28PLtC5DUpvECjnS1HkauSBQE2cme9UDGvzvNZdHMCQL` | `5MQgFr8SVQvrVg8AUKDqKhTwAQ8FvRLJMAz7GSmo2AcJ` | `verify-request: 1`<br>`withdraw/inbox: 1` | `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ: 2`<br>`JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw: 1`<br>`unknown: 1` | `432636751` | 125364 | `None` | `None` | `None` | `432636751 verify-request VerifyRequest BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ 2kKgHStS locations=1`<br>`432636751 withdraw/inbox Withdraw BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ,JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw,unknown 5dgeXhBd locations=4` |
| `2dMnSaFa8T4jqdHAH92T3QiFN9M4pW2LURH1YYYDiNya` | `gXgmsVn7aak8tLEpmnT4GqQS9bsuiH4q2Jnju5vmpyu` | `verify-request: 1`<br>`withdraw/inbox: 1` | `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ: 2`<br>`JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw: 1`<br>`unknown: 1` | `432632792` | 121405 | `None` | `None` | `None` | `432632792 verify-request VerifyRequest BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ 2WR6T5RJ locations=1`<br>`432632792 withdraw/inbox Withdraw BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ,JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw,unknown K1iki3ds locations=4` |
| `4s3gnkf1R2UzAWbfvVowfaW7VdLDNSQhmwjYcSnMYwmT` | `5Tv692BDJinbjR6Beb2K9bGmxnbQeFaGb1rJqCs2y3Q6` | `None` | `None` | `None` | None | `None` | `None` | `None` | `None` |
| `9365dmaj6LvfB9CKeZx4WSQhAvRHFy4J5nLbzd82vmDR` | `99wB6iLbm1xFjyU3ybEoAKY8nkxU4RLMQ5F1oqPzByCW` | `verify-request: 1`<br>`withdraw/inbox: 1` | `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ: 2`<br>`JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw: 1`<br>`unknown: 1` | `432636479` | 125092 | `None` | `None` | `None` | `432636479 verify-request VerifyRequest BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ 25cPmCsi locations=1`<br>`432636479 withdraw/inbox Withdraw BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ,JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw,unknown GpwYZRvq locations=4` |
| `9LdadjLYo2R2P4SvHPe1TFY3xo74mgTzScrx53TEEi8a` | `4KQMggJ5x9L9rq65tPQaHRynVLQfm3RNSxNZ1JVNW9Kz` | `rfq/inbox: 2`<br>`verify-request: 1` | `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ: 3`<br>`JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw: 1`<br>`unknown: 1` | `None` | 125755 | `None` | `None` | `None` | `432637142 verify-request VerifyRequest BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ 3Y96QXBt locations=1`<br>`432637146 rfq/inbox RfqSellCommit BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ 3hByVRoy locations=1`<br>`432637152 rfq/inbox RfqSellResolve BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ,JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw,unknown 5A2j3aow locations=4` |
| `9SiKWpVwtyehB91q7A2CFkLz9nqLvvygK34v9GMepPPi` | `GstTi6nfFmwcLTBN4PLP8zVVjWodNUz6Ho6vtjH3w3zB` | `verify-request: 1`<br>`swap/inbox: 1`<br>`metadata: 1` | `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ: 2`<br>`JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw: 1`<br>`unknown: 1` | `432632730` | 121343 | `None` | `None` | `None` | `432632730 verify-request VerifyRequest BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ 2MxbNZJC locations=1`<br>`432632730 swap/inbox Swap,RouteV2 BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ,JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw,unknown 4UGAHXBi locations=4`<br>`432632730 metadata CacheTokenMetadata none 58UnA73X locations=0` |
| `Amq8xxEYMt35Q1ghom7psKxkXkGTLvsKXEXFeRmR6PcY` | `7h3xELrPgxSFjA8T2WCm5Uham61VThkySaHvrq1jTEYu` | `rfq/inbox: 2`<br>`verify-request: 1` | `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ: 3`<br>`JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw: 1`<br>`unknown: 1` | `None` | 119160 | `None` | `None` | `None` | `432630547 verify-request VerifyRequest BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ 5nQE7nvi locations=1`<br>`432630550 rfq/inbox RfqSellCommit BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ 3u7aZGQJ locations=1`<br>`432630558 rfq/inbox RfqSellResolve BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ,JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw,unknown 4huB1ax2 locations=4` |
| `AxdbJwLRX8y5Up4vQSPvDASg1vSxjsfSDB69vFQkAVnp` | `5Y5RSMeCNYCZqxCw27h1cG13yNQeZZn1tWFRVaSxN88C` | `verify-request: 1`<br>`withdraw/inbox: 1` | `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ: 2`<br>`JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw: 1`<br>`unknown: 1` | `432634980` | 123593 | `None` | `None` | `None` | `432634980 verify-request VerifyRequest BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ 3UF6RqL8 locations=1`<br>`432634980 withdraw/inbox Withdraw BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ,JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw,unknown 3ZyYaWyc locations=4` |
| `Bc1BzVrVzGpzLYzuanCGa2BCVnvrGKR91rBH5aLjBDBv` | `5twYrZDqeLpXnegGhPSLRKAcmhmeTBVzjGxz1FNbmZE7` | `verify-request: 1`<br>`withdraw/inbox: 1` | `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ: 2`<br>`JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw: 1`<br>`unknown: 1` | `432636238` | 124851 | `None` | `None` | `None` | `432636238 verify-request VerifyRequest BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ 1jLUs6zr locations=1`<br>`432636238 withdraw/inbox Withdraw BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ,JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw,unknown 5rwgP1PX locations=4` |
| `Bj1jaRaBkpGEceFY5qXauaUiQTk2twqRBd126Vxo6yQ4` | `29eoLuBwTD7u1RAEugWnjJ2956yS1UVHg55FkMc9WAdx` | `rfq/inbox: 2`<br>`verify-request: 1` | `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ: 3`<br>`JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw: 1`<br>`unknown: 1` | `None` | 123557 | `None` | `None` | `None` | `432634944 verify-request VerifyRequest BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ 4ed7TYej locations=1`<br>`432634947 rfq/inbox RfqSellCommit BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ 5BTrhKTk locations=1`<br>`432634954 rfq/inbox RfqSellResolve BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ,JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw,unknown 2DwLMRUm locations=4` |
| `Bod11EbXJtLhuVkSmtBC2mgbPMruUqZiTr3UvVq3xyVv` | `6rKVUjumEUZqgQPzr2Zqdy3AYudAFv3vCGZPc1JKuf8t` | `verify-request: 1`<br>`withdraw/inbox: 1` | `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ: 2`<br>`JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw: 1`<br>`unknown: 1` | `432636201` | 124814 | `None` | `None` | `None` | `432636201 verify-request VerifyRequest BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ 268T61ak locations=1`<br>`432636201 withdraw/inbox Withdraw BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ,JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw,unknown 3SSU22k4 locations=4` |
| `C2s6EVawFZBCHdWF6LxCeCJtdtDGwp6NefEZvGMZwmqt` | `BHAkv4LygwQ6L3r9F91asxxvvuXnfbfh4fcnaX6SPgUM` | `rfq/inbox: 2`<br>`verify-request: 1` | `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ: 3`<br>`JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw: 1`<br>`unknown: 1` | `None` | 121367 | `None` | `None` | `None` | `432632754 verify-request VerifyRequest BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ 5BkMUKiS locations=1`<br>`432632757 rfq/inbox RfqSellCommit BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ 7ZrmnZ5W locations=1`<br>`432632765 rfq/inbox RfqSellResolve BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ,JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw,unknown 2bPapHKs locations=4` |
| `CaQ5ZAFVTWzQcWfTLjHUTQXrAr5XLGPpr3GbgBQREXfu` | `AH6RegHZjxewftm9cHNjUCT8L1cfJyUmgkRsNvRyyBTH` | `withdraw/inbox: 1`<br>`verify-request: 1` | `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ: 2`<br>`JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw: 1`<br>`unknown: 1` | `432633576` | 122189 | `None` | `None` | `None` | `432633576 withdraw/inbox Withdraw BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ,JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw,unknown 62mdypRz locations=4`<br>`432633576 verify-request VerifyRequest BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ EEmbDuBZ locations=1` |
| `Eoii26BVRLbGHYQESCqWQ8AB2Cu5MBPFPSmn6HvRGjzG` | `3AxoHN6NTFFVuqSTUByd5j8FEYP3WNGnekhSquoqGxdr` | `withdraw/inbox: 1`<br>`verify-request: 1` | `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ: 2`<br>`JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw: 1`<br>`unknown: 1` | `432638501` | 127114 | `None` | `None` | `None` | `432638501 withdraw/inbox Withdraw BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ,JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw,unknown 3Q6vTA5N locations=4`<br>`432638501 verify-request VerifyRequest BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ 4Bi9e8Hz locations=1` |
| `GNL9D5sLSs21MMBpWN4kkDzhokC4ZTuVV89tPE6KXgE1` | `Ck8c61tBP3BxnupK5ADjxRe5rD1RC1bemdykyprxeQoQ` | `verify-request: 1`<br>`withdraw/inbox: 1` | `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ: 2`<br>`JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw: 1`<br>`unknown: 1` | `432636176` | 124789 | `None` | `None` | `None` | `432636176 verify-request VerifyRequest BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ 5213DmWq locations=1`<br>`432636176 withdraw/inbox Withdraw,TransferChecked BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ,JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw,unknown 5ytkX2WP locations=4` |
| `GyMHaC8RzvMDMuALGQFYh7RUsqokUFe43DxuanaF9Bdz` | `2nek4emrB7cYTVq176i8Y4uWDXY8SB4FfuB4y13dgFjq` | `verify-request: 1`<br>`rfq/inbox: 1` | `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ: 2`<br>`JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw: 1`<br>`unknown: 1` | `None` | 125725 | `None` | `None` | `None` | `432637112 verify-request VerifyRequest BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ 3V2ikMDe locations=1`<br>`432637120 rfq/inbox RfqSwap BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ,JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw,unknown 2Z3xZGaF locations=4` |
| `HYizrG8XrkdQE55cDfx51PUiN8GTMWfj5PMJJcCaDjPK` | `FvtwBdJ3evQ4ovt5Qa2vkLUkdzsVdo5NMrxV7GFqfcow` | `verify-request: 1`<br>`rfq/inbox: 1` | `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ: 2`<br>`JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw: 1`<br>`unknown: 1` | `None` | 123526 | `None` | `None` | `None` | `432634913 verify-request VerifyRequest BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ 3NnbL2rP locations=1`<br>`432634921 rfq/inbox RfqSwap BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ,JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw,unknown EnJ5zkfm locations=4` |
| `J6m19Tciv3FpaB1C2THW4AdoYtnVLknQ27Em3NEH1HfG` | `BxePu1KUBTrb4AqkPpHPQeHXGuuc8jwYDFKn71oJtXQ1` | `withdraw/inbox: 1`<br>`verify-request: 1` | `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ: 2`<br>`JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw: 1`<br>`unknown: 1` | `432637177` | 125790 | `None` | `None` | `None` | `432637177 withdraw/inbox Withdraw BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ,JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw,unknown 2FUZdA1b locations=4`<br>`432637177 verify-request VerifyRequest BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ 5KqrmktC locations=1` |
| `JDatg1ZvHcN4mMkC2vff4wzfKSpUt4wLhk1krwamjbtr` | `CQ3gXwrKhF1NMRPBwBez3JzqzTp2JLhUKSraLmwA2xVM` | `withdraw/inbox: 1`<br>`verify-request: 1` | `BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ: 2`<br>`JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw: 1`<br>`unknown: 1` | `432630586` | 119199 | `None` | `None` | `None` | `432630586 withdraw/inbox Withdraw BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ,JNiN12VC7ApitDkW7roQ1FmeyKSN1MnmZyCVyLiqAQw,unknown 2zAjJY3F locations=4`<br>`432630586 verify-request VerifyRequest BankK1Y7HK6ZYmPorzAuUNk1TbJixDFQnqfWnP7HNmFZ 447EAoNK locations=1` |

## Same-Slot Operation And Verify

| Local id | Slots |
|---|---|
| `5MQgFr8SVQvrVg8AUKDqKhTwAQ8FvRLJMAz7GSmo2AcJ` | `432636751` |
| `gXgmsVn7aak8tLEpmnT4GqQS9bsuiH4q2Jnju5vmpyu` | `432632792` |
| `99wB6iLbm1xFjyU3ybEoAKY8nkxU4RLMQ5F1oqPzByCW` | `432636479` |
| `GstTi6nfFmwcLTBN4PLP8zVVjWodNUz6Ho6vtjH3w3zB` | `432632730` |
| `5Y5RSMeCNYCZqxCw27h1cG13yNQeZZn1tWFRVaSxN88C` | `432634980` |
| `5twYrZDqeLpXnegGhPSLRKAcmhmeTBVzjGxz1FNbmZE7` | `432636238` |
| `6rKVUjumEUZqgQPzr2Zqdy3AYudAFv3vCGZPc1JKuf8t` | `432636201` |
| `AH6RegHZjxewftm9cHNjUCT8L1cfJyUmgkRsNvRyyBTH` | `432633576` |
| `3AxoHN6NTFFVuqSTUByd5j8FEYP3WNGnekhSquoqGxdr` | `432638501` |
| `Ck8c61tBP3BxnupK5ADjxRe5rD1RC1bemdykyprxeQoQ` | `432636176` |
| `BxePu1KUBTrb4AqkPpHPQeHXGuuc8jwYDFKn71oJtXQ1` | `432637177` |
| `CQ3gXwrKhF1NMRPBwBez3JzqzTp2JLhUKSraLmwA2xVM` | `432630586` |

## Root Update Context

| Time | Slot | File | Epoch | Signers |
|---|---:|---|---:|---|
| `2026-07-12T21:25:50+00:00` | 432511387 | `solana-mainnet-outbox-tx-3Zjq8FZd.json` | 271 | `6f5muRjigWVnoQHfXWLeXFfafUqMVJfzoBBJL8Gwquji` |

## Assessment

- Most sampled local ids bridge Bank operation payloads and `VerifyRequest` payloads, so the 32-byte value is a useful Bank-local lifecycle handle.
- Some local ids have same-slot operation and verification evidence, which is the strongest public timing link in this pass.
- No local id crossed into decoded `bk1PDA...` request fields, verifier/root fields, canonical JUP or current validator/vote/stake keys.
- The public lifecycle currently stops at a Bank-local operation/verify handle; it does not expose the Dove/JUP/stake producer side.
