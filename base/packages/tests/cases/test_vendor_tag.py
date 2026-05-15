# SPDX-License-Identifier: MIT
"""Every binary package must carry the expected Vendor tag.

The expected vendor is configurable via ``--expected-vendor`` so the
same suite can validate both AZL4 (default: ``Microsoft Corporation``)
and any future vendor string without a fork.
"""

from __future__ import annotations

import pytest

from utils.repos import Repo


@pytest.mark.repo_kind("binary")
def test_binary_packages_have_expected_vendor(
    repo: Repo, arch: str, repo_packages, expected_vendor: str
) -> None:
    """Aggregate: every non-source package must have ``Vendor == expected_vendor``."""
    packages = repo_packages(repo, arch)
    offenders = [
        p for p in packages
        if not p.is_source and (p.vendor or "").strip() != expected_vendor
    ]
    if offenders:
        listing = "\n".join(
            f"  - {p.nevra}: vendor={(p.vendor or '<none>')!r}"
            for p in offenders
        )
        pytest.fail(
            f"binary repo {repo.name!r} (arch {arch}) has "
            f"{len(offenders)} package(s) with unexpected Vendor "
            f"(expected {expected_vendor!r}):\n{listing}"
        )
