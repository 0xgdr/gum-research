# Scripts Index

Scripts developed or discussed during the investigation included:

- validator/native-program inspection;
- stake account enumeration;
- vote transaction capture;
- corrected raw vote decoding;
- OpenID Registry decoding;
- executable program dumping;
- binary string extraction;
- JUP-in-Gum tracing;
- public dependency/lockfile analysis.

## Reproducibility note

The original scripts were developed iteratively. Before publishing them as production tooling:

1. consolidate duplicated RPC helpers;
2. add rate limiting and retries;
3. persist raw responses;
4. record generated timestamps and RPC versions;
5. hash every downloaded binary;
6. distinguish parsed-instruction and compiled-instruction formats;
7. add tests for base58 and account-index decoding.
