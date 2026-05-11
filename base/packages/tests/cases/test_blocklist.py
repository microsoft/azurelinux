# SPDX-License-Identifier: MIT
"""Names that must not appear (as N of NEVR) in *any* provided repo.

This is the global blocklist — entries here are forbidden across every
repo kind (binary, srpm, debuginfo). Typical entries:

* upstream Fedora/RHEL packages that AZL replaces with its own (e.g.
  ``fedora-release``, ``fedora-repos``, ``redhat-rpm-config``);

The test fans out over every provided ``--repo`` × every entry in
``GLOBAL_BLOCKLIST``: each pair becomes its own pytest case (data
parametrization), so a regression on any single name is easy to
spot in the report.

If you ever need a *per-repo* blocklist (i.e., something allowed in
``sdk`` but not in ``base``), add a separate test alongside this
one — don't try to cram both shapes into a single function.
"""

from __future__ import annotations

import pytest

from utils.repos import Repo


# rules-as-code: edit me to adjust the global blocklist. Names here
# must not appear in any --repo at any arch.
GLOBAL_BLOCKLIST: tuple[str, ...] = (
    "fedora-logos",
    "fedora-release",
    "fedora-repos",
    "ffmpeg",
    "redhat-rpm-config",
)


# Sentinel used so the test still collects (and fails loudly) when
# the blocklist is empty. Without this, pytest.parametrize with an
# empty list collects zero items and the test silently disappears,
# which would let an accidentally-cleared GLOBAL_BLOCKLIST sail
# through CI as a green run.
_EMPTY_SENTINEL = "__EMPTY_GLOBAL_BLOCKLIST__"


@pytest.mark.parametrize("blocked_name", GLOBAL_BLOCKLIST or [_EMPTY_SENTINEL])
def test_no_globally_blocklisted_name(
    repo: Repo, arch: str, blocked_name: str, repo_packages
) -> None:
    """Per-(repo, blocked_name): each blocklisted name must not appear."""
    if blocked_name == _EMPTY_SENTINEL:
        pytest.fail(
            "GLOBAL_BLOCKLIST is empty — this is almost certainly a "
            "misconfiguration. Restore the blocklist (see "
            "GLOBAL_BLOCKLIST at the top of this file) or, if the rule "
            "no longer applies, delete this test rather than leaving an "
            "empty list that would silently no-op forever."
        )
    packages = repo_packages(repo, arch)
    hits = [p for p in packages if p.name == blocked_name]
    if hits:
        listing = "\n".join(f"  - {p.nevra}" for p in hits)
        pytest.fail(
            f"repo {repo.name!r} (kind={repo.kind!r}, arch={arch}) "
            f"contains globally-blocklisted name {blocked_name!r}:\n{listing}"
        )
