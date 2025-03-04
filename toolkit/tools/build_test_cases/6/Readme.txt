Test dynamic build dependencies.

Pre-test state:
- A explicitly -> B
- A uses the "macro_from_B" macro in its "%generate_buildrequires" section.
- B provides the "macro_from_B" macro.
- The "macro_from_B" macro echoes "C".

Test case I:
- Upstream A older than the local one.
- Upstream B current with the local one.
- Upstream C current with the local one.

Expectation:
- A is analyzed with B installed from the upstream cache.
- A builds with B and C installed from the upstream cache.


Test case II:
- Upstream A older than the local one.
- Upstream B older than the local one.
- Upstream C current with the local one.

Expectation:
- B builds.
- A is analyzed with B installed from the local cache.
- A builds with B from the local cache and C from the upstream cache.


Test case III:
- Upstream A older than the local one.
- Upstream B current with the local one.
- Upstream C older than the local one.

Expectation:
- A is analyzed with B installed from the local cache.
- C builds.
- A builds with B from the upstream cache and C from the local cache.


Test case IV:
- Upstream A older than the local one.
- Upstream B current with the local one.
- C doesn't exist.

Expectation:
- A is analyzed with B installed from the local cache.
- Build fails due to missing C.
