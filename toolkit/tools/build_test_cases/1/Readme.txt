Circular build dependency test.

Pre-test state:
- A and B not built.


Test case I:
- A and B available in upstream cache.
- Upstream A and B older than the local ones.

Expectation:
- Intermediate A and/or B may be built using the upstream cache.
- Final A and B built using the local output.


Test case II:
- A and B available in upstream cache.
- Upstream A older than the local ones.
- Upstream B same as the local one.

Expectation:
- B not rebuilt.
- A built with upstream B.


Test case III:
- A and B NOT available in upstream cache.

Expectation:
- Toolkit fails with a circular dependency error.
