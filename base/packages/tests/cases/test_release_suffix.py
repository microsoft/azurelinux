# SPDX-License-Identifier: MIT
"""Every binary package's Release tag must match the configured suffix.

The required suffix is configurable via ``--release-suffix`` (a regex
that ``re.search`` must match) so the same suite can validate AZL4
(default: ``\\.azl4(?:\\.\\d+|~.*)?$``) as well as nightly verification of
older distros (e.g. AZL3, ``\\.azl3(?:\\.\\d+|~.*)?$``) without a fork.

The default AZL4 pattern accepts three shapes:

* ``.azl4`` — the standard suffix.
* ``.azl4~prerelease`` — a tilde-qualified pre-release tag (RPM treats
  ``~`` as "less than", e.g. ``1.azl4~rc1`` < ``1.azl4``).
* ``.azl4.<N>`` — a numeric rebuild bump appended after the dist tag,
  used by some packages to track Azure-Linux-side rebuilds without
  touching the upstream release. Only a positive integer is accepted;
  combining it with ``~prerelease`` is intentionally not supported.
"""

from __future__ import annotations

import re

import pytest

from utils.repos import Repo


@pytest.mark.repo_kind("binary")
def test_release_suffix(
    repo: Repo, arch: str, repo_packages, release_suffix_pattern: str
) -> None:
    """Aggregate: every non-source package's Release tag must match the suffix regex."""
    pattern = re.compile(release_suffix_pattern)
    packages = repo_packages(repo, arch)
    offenders = [
        p for p in packages
        if not p.is_source and not pattern.search(p.nevra.release)
    ]
    if offenders:
        listing = "\n".join(
            f"  - {p.nevra}: release={p.nevra.release!r}" for p in offenders
        )
        pytest.fail(
            f"binary repo {repo.name!r} (arch {arch}) has "
            f"{len(offenders)} package(s) with unexpected Release suffix "
            f"(expected match: {pattern.pattern!r}):\n{listing}"
        )
