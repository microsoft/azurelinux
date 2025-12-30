Validate test-only dependencies.

Pre-test state:
- A(T) -> B.
- B -R> A.

Where:
- "A(T) ->" is a test-only build dependency of A.
- "B -R>" is a runtime dependency of B.
- A and B have a "%check" section.

Test case I:
- Upstream A older than the local one.
- Upstream B current with the local one.

Expectation:
- A builds and runs its tests.
- B only runs its tests against the locally-built A.


Test case II:
- Upstream A current than the local one.
- Upstream B older with the local one.

Expectation:
- B builds.
- A only runs its tests against the locally-built B.
