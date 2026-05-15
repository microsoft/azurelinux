# SPDX-License-Identifier: MIT
"""The ``base`` repo must be closed over runtime dependencies on its own.

This test is hard-coded for the ``base`` repo (per design — see
``docs/architecture.md``). It runs once per architecture.

Behavior:

* If ``--repo name=base,...`` was provided, run repoclosure with
  ``[base]`` as the universe.
* Otherwise, skip with a clear message.
"""

from __future__ import annotations


def test_repoclosure_base(arch: str, require_named_repos, repoclosure, subtests) -> None:
    repos = require_named_repos(["base"], kind="binary")
    result = repoclosure(repos, arch)
    if result.success:
        return
    for nevra, missing in sorted(result.unresolved.items(), key=lambda kv: str(kv[0])):
        repo = result.repos_by_nevra.get(nevra)
        suffix = f" (from {repo!r})" if repo else ""
        with subtests.test(package=str(nevra), arch=arch):
            import pytest
            pytest.fail(
                f"{nevra}{suffix} has unresolved runtime dep(s):\n"
                + "\n".join(f"  - {d}" for d in missing)
            )
