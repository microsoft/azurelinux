# SPDX-License-Identifier: MIT
"""Binary repos must not contain source RPMs."""

from __future__ import annotations

import pytest

from utils.repos import Repo
from utils.types import Package


@pytest.mark.repo_kind("binary")
def test_binary_repo_has_no_source_rpms(
    repo: Repo, arch: str, repo_packages
) -> None:
    """Aggregate: every package in a binary repo must have a binary arch."""
    packages: list[Package] = repo_packages(repo, arch)
    offenders = [p for p in packages if p.is_source]
    if offenders:
        listing = "\n".join(f"  - {p.nevra}" for p in offenders)
        pytest.fail(
            f"binary repo {repo.name!r} (arch {arch}) contains "
            f"{len(offenders)} source-arch package(s):\n{listing}"
        )
