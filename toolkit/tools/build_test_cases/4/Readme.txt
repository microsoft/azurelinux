Dependency on a dynamically-generated provides. Similar to tests suite 2.
Uses the "bogus-generators" package.

Pre-test state:
- A -> DynDep(B).
- DynDep(B) provides in B derived by the generator.


Test case I:
- B current in the upstream cache.

Expectation:
- A builds with B from the upstream cache.


Test case II:
- Upstream A older than the local one.
- Upstream B older than the local one.

Expectation:
- Version 1:
    - Tooling realizes the local B has a chance to provide DynDep(B), since older upstream B provides it.
    - B builds.
    - A builds with the local B.
- Version 2:
    - A and B build in parallel. A builds with upstream B.
    - A rebuilds with the local B, since its DynDep(B) dependency is available from a newer B.


Test case III:
- B absent locally and upstream.

Expectation:
- A fails to build due to missing dependency.
