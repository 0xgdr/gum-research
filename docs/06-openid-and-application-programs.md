# OpenID and Application Programs

## OpenID Registry

Registry-owned accounts split into fixed-size binary records and larger metadata records.

Readable provider metadata included references such as:

- Apple
- Twitter/X
- application/issuer-style identifiers

## Conclusion

The OpenID Registry appears to bind users and external identity providers to JupNet identities.

No clear evidence was found for:

- validator committee membership;
- BLS public keys;
- JUP stake weights;
- Dove registration.

## Executable program scan

Twenty-nine executable programs were enumerated in the captured snapshot.

String analysis identified application-layer components including:

- Gum-related deposit forwarders;
- JTX oracle components;
- verifier programs;
- user/account programs;
- token and identity infrastructure.

A verifier executable included configuration and signer-related concepts such as:

```text
Fault tolerance
Too many signers provided
Insufficient number of signers provided
Non-unique signatures provided
Mismatched signatures
DonConfig
```

The surrounding paths and terminology suggested an oracle/external-proof verifier rather than native validator consensus.

## Evidence boundary

No deployed executable clearly identified itself as:

- Dove consensus;
- validator committee;
- JUP staking;
- quorum certificate coordinator.
