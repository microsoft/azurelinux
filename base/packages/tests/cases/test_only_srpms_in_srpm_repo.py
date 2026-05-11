# SPDX-License-Identifier: MIT
"""SRPM repos must contain only source RPMs (``src`` or ``nosrc``)."""

from __future__ import annotations

import pytest

from utils.repos import Repo
from utils.types import Package


_SRPM_ARCHES = frozenset({"src", "nosrc"})


@pytest.mark.repo_kind("srpm")
def test_srpm_repo_only_has_source_rpms(
    repo: Repo, arch: str, repo_packages
) -> None:
    """Every package in an SRPM repo must have arch ``src`` or ``nosrc``."""
    packages: list[Package] = repo_packages(repo, arch)
    offenders = [p for p in packages if p.arch not in _SRPM_ARCHES]
    if offenders:
        listing = "\n".join(f"  - {p.nevra}" for p in offenders)
        pytest.fail(
            f"srpm repo {repo.name!r} (arch {arch}) contains "
            f"{len(offenders)} non-source package(s):\n{listing}"
        )
