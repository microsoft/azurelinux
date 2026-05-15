# SPDX-License-Identifier: MIT
"""Combined runtime + buildtime closure of ``base + sdk + base-srpms + sdk-srpms``.

Why one walk, two assertion passes
----------------------------------

A single ``check_kind="buildtime"`` walk of the union universe visits every
package on the test arch (binaries from ``base + sdk``) plus every ``noarch``
and every ``src`` / ``nosrc`` package (SRPMs from ``base-srpms + sdk-srpms``):
see ``utils.repoclosure.Repoclosure.run`` for why ``buildtime`` does not filter
``to_check_query`` to ``target_repos``. Each unresolved finding is then
partitioned by consumer arch:

* ``arch in {"src", "nosrc"}``  → buildtime gap (unresolved BuildRequires)
* otherwise                     → runtime gap (unresolved Requires)

Each partition is asserted against its own section of the known-violations
TOML (``[runtime-missing]`` / ``[buildtime-missing]``).

This collapses two previously separate tests
(``test_repoclosure_base_plus_sdk`` and ``test_repoclosure_srpms_buildtime``)
that were checking the same universe twice with overlapping allowlists. The
binary universe is identical and the buildtime walk is a strict superset, so
collapsing halves the work and removes the cross-list drift footgun.

Hard-coded for ``base``, ``sdk``, ``base-srpms``, ``sdk-srpms``. If any of
those ``--repo`` flags are missing, the test fails (see
:func:`require_named_repos` -- silently skipping a release-gating closure
check is worse than failing loudly). Use ``pytest -k`` / ``--ignore`` to
deselect intentionally.

Known violations
----------------

The list of known-but-tolerated unresolved deps lives in
``cases/known-violations/test_repoclosure_base_plus_sdk_full.toml`` with
``[runtime-missing]`` and ``[buildtime-missing]`` sections (and parallel
``-arch-gated.<consumer>`` tables for arch-restricted entries). Schema, the
four-way classification (real failure, known violation/XFAIL, stale-consumer,
stale-dep), and the ``--known-violations-dir`` CLI override are documented in
``cases/known-violations.schema.json`` and in
``utils/known_violations.py`` / ``utils/repoclosure.py``.
"""

from __future__ import annotations

from utils.repoclosure import assert_known_violations
from utils.types import RepoclosureResult


_RUNTIME_SECTION = "runtime-missing"
_BUILDTIME_SECTION = "buildtime-missing"
_BUILDTIME_ARCHES = frozenset({"src", "nosrc"})


def _split_by_kind(
    result: RepoclosureResult,
    *,
    runtime_target_repo_names: tuple[str, ...],
    buildtime_target_repo_names: tuple[str, ...],
) -> tuple[RepoclosureResult, RepoclosureResult]:
    """Partition unresolved findings by consumer-arch into runtime vs buildtime.

    The original ``result`` is a single SRPM-target run with the binary
    repos in the universe; partitioning by consumer arch separates
    runtime (binary-arch consumers) from buildtime (``src``/``nosrc``
    consumers). Each half carries its own ``target_repo_names`` label
    reflecting where the consumers conceptually live, so any future log
    rendering of the partitioned ``RepoclosureResult.__str__`` doesn't
    misrepresent the runtime half as a srpm-target run.
    """
    runtime_unresolved: dict = {}
    buildtime_unresolved: dict = {}
    runtime_repos: dict = {}
    buildtime_repos: dict = {}

    for nevra, deps in result.unresolved.items():
        repo = result.repos_by_nevra.get(nevra, "")
        if nevra.arch in _BUILDTIME_ARCHES:
            buildtime_unresolved[nevra] = deps
            buildtime_repos[nevra] = repo
        else:
            runtime_unresolved[nevra] = deps
            runtime_repos[nevra] = repo

    runtime = RepoclosureResult(
        target_repo_names=runtime_target_repo_names,
        arch=result.arch,
        unresolved=runtime_unresolved,
        repos_by_nevra=runtime_repos,
    )
    buildtime = RepoclosureResult(
        target_repo_names=buildtime_target_repo_names,
        arch=result.arch,
        unresolved=buildtime_unresolved,
        repos_by_nevra=buildtime_repos,
    )
    return runtime, buildtime


def test_repoclosure_base_plus_sdk_full(
    arch: str,
    require_named_repos,
    repoclosure,
    subtests,
    known_violations,
    summary_recorder,
) -> None:
    binaries = require_named_repos(["base", "sdk"], kind="binary")
    srpms = require_named_repos(["base-srpms", "sdk-srpms"], kind="srpm")

    result = repoclosure(
        target_repos=srpms,
        arch=arch,
        universe_repos=srpms + binaries,
        check_kind="buildtime",
    )

    runtime, buildtime = _split_by_kind(
        result,
        runtime_target_repo_names=tuple(r.name for r in binaries),
        buildtime_target_repo_names=tuple(r.name for r in srpms),
    )

    assert_known_violations(
        runtime,
        arch,
        known_violations.section(_RUNTIME_SECTION),
        subtests=subtests,
        dep_kind="runtime dep",
        source_label=f"{known_violations.path.name} [{_RUNTIME_SECTION}]",
        recorder=summary_recorder,
    )
    assert_known_violations(
        buildtime,
        arch,
        known_violations.section(_BUILDTIME_SECTION),
        subtests=subtests,
        dep_kind="dep",
        source_label=f"{known_violations.path.name} [{_BUILDTIME_SECTION}]",
        recorder=summary_recorder,
    )
