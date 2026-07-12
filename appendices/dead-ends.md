# Dead Ends and Corrections

## Mistaking empty decoded vote instructions for absence

Initial vote tooling requested raw JSON but looked for direct `programId` fields. Raw instructions use `programIdIndex`. The decoder was corrected.

Lesson: preserve raw transactions and resolve indices against static and loaded account keys.

## Treating native stake as JUP stake

Native stake accounts resembled Solana stake accounts and were denominated in native lamports.

Lesson: JUP is an SPL mint. Native stake cannot be called JUP stake without token-account or explicit mapping evidence.

## OpenID as possible Dove registry

Registry metadata was inspected for validator, BLS and stake information. It appeared identity-focused.

Lesson: program names and account sizes are clues, not proof.

## Random executable searches

Executable enumeration was useful, but no clearly labelled Dove consensus program appeared.

Lesson: absence of strings in stripped binaries is not proof of absence; however, repeated random scans have diminishing value.

## Local Cargo cache

The local machine had no Rust/Cargo toolchain and no Cargo Git checkout cache.

Lesson: do not install tooling merely to search for source that was never fetched.

## Mistaking every burn for utility

A Burn instruction in an omnichain flow may be paired with a mint.

Lesson: classify the protocol mechanism, not isolated instruction names. A trade, bridge burn or mint is noise unless it proves JUP staking, fees, signer weights, access control, governance, rewards, slashing or a permanent protocol sink.

## Treating Omnipair AMM source as Gum validator-security source

The public `jup-ag/omnipair-amm-sdk` repository is real and relevant to Jupiter AMM integration, but inspected source exposes AMM pair state, quote math, swap account metas, rate-model logic and a futarchy-authority configuration. It does not expose Gum validator/Dove software or a JUP-denominated security mechanism.

Lesson: public Jupiter AMM integration code can explain routing and asset support without explaining Gum/JupNet utility. Keep it as a lead, but do not treat it as evidence of JUP utility unless it connects to stake, weights, quorum, fees, governance, access control, slashing, rewards or a permanent sink.
