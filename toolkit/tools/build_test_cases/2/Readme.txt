Dependency on a file path.

Pre-test state:
- A -> /a/b/c.
- B installs /a/b/c but doesn't explicitly provide it.


Test case I:
- A and B not in the upstream cache.
- B has no dependencies.

Expectation:
- B builds first.
- A unblocked and builds after B.


Test case II:
- B in the upstream cache.
- Local B the same as upstream.

Expectation:
- B doesn't build.
- A uses upstream B to build.


Test case III:
- B absent locally and upstream.

Expectation:
- A fails to build due to missing dependency.
