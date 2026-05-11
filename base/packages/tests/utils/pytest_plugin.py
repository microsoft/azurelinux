# SPDX-License-Identifier: MIT
"""Pytest plugin for Azure Linux RPM repo validation.

Registered via ``[project.entry-points."pytest11"]`` so that custom CLI
options are known to pytest *before* rootdir determination. This is
important here because ``--workdir`` takes a path-like value and
``--repo`` values can be long opaque strings that would otherwise risk
being interpreted as positional test-path arguments.

Responsibilities:

* Register all CLI options.
* Register the ``repo_kind`` / ``repo_name`` markers.
* Implement ``pytest_generate_tests`` to fan a test out across all
  matching ``(repo, arch)`` pairs at parametrize time, with a no-match
  guard so a typo'd marker can't silently zero out a test.

Higher-level fixtures (``repo_packages``, ``cross_repo_file_index``,
``repoclosure``, ...) live in ``conftest.py`` so tests get the
familiar pytest fixture-discovery experience.

No-``--repo`` policy
--------------------

Because this plugin is registered as a ``pytest11`` entry point, it is
loaded for **every** ``pytest`` invocation in any environment that has
``azl-repo-tests`` installed (including ``pytest --collect-only`` and
unrelated test suites that share the venv). It therefore must not fail
configuration when no ``--repo`` is provided — instead, repo-dependent
tests skip cleanly via ``pytest_generate_tests`` and the
``require_named_repos`` fixture.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

import pytest

from .repos import Repo, RepoSpecError, collect_repos

SUMMARY_JSON_SCHEMA_VERSION = 1

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# CLI options
# ---------------------------------------------------------------------------


def pytest_addoption(parser: pytest.Parser) -> None:
    """Register all CLI options for the repo-validation suite."""

    group = parser.getgroup("azl-repo", "Azure Linux RPM repo validation")
    group.addoption(
        "--repo",
        action="append",
        default=[],
        dest="azl_repos",
        metavar="name=...,kind=...,url=...",
        help=(
            "Add a repository under test (inline form). Required keys: "
            "name, kind (binary|srpm|debuginfo), url. The URL is passed "
            "through librepo, including any $basearch/$releasever "
            "placeholders. Values cannot contain commas (the spec is "
            "split on commas with no quoting); URL-encode commas if "
            "needed, or use --repos-file. May be repeated. Combine "
            "with --repos-file and --repo-prefix as needed; at least "
            "one of --repo / --repos-file / --repo-prefix is required "
            "for any test that touches a repo."
        ),
    )
    group.addoption(
        "--repos-file",
        action="append",
        default=[],
        dest="azl_repos_files",
        metavar="PATH",
        help=(
            "Load repositories from a yum/dnf-style .repo ini file. Each "
            "section becomes one repo; the section name is the repo "
            "name, ``baseurl=`` is the URL, and a custom ``kind=`` key "
            "(binary|srpm|debuginfo) is required. May be repeated."
        ),
    )
    group.addoption(
        "--repo-prefix",
        action="append",
        default=[],
        dest="azl_repo_prefixes",
        metavar="URL",
        help=(
            "Convenience shorthand: assume URL hosts the Standard Azure "
            "Linux Repo Layout (the same layout produced by "
            "scripts/synthesize-repodata.py) and expand it into the six "
            "conventional sub-repos: base, base-debuginfo, base-srpms, "
            "sdk, sdk-debuginfo, sdk-srpms. Each is probed for "
            "repodata/repomd.xml; sub-repos that 404 are silently "
            "skipped (so a partial mirror works fine). Other HTTP/network "
            "errors are fatal. Binary/debuginfo URLs are probed using "
            "the first --arch as a sentinel and registered with a "
            "$basearch placeholder, so they still fan out across all "
            "--arch values at fetch time. Repeatable; combine with "
            "--repo / --repos-file as needed (explicit definitions "
            "override prefix-derived ones with the same name)."
        ),
    )
    group.addoption(
        "--arch",
        action="append",
        default=[],
        dest="azl_arches",
        metavar="ARCH",
        help=(
            "Architecture to test against (substituted for $basearch by "
            "librepo). May be repeated; defaults to x86_64 if not provided."
        ),
    )
    group.addoption(
        "--releasever",
        default=None,
        dest="azl_releasever",
        metavar="RELEASEVER",
        help=(
            "Release version to substitute for $releasever in URLs. "
            "Required only when at least one repo URL contains $releasever. "
            "We never inherit this from the host or from the container image."
        ),
    )
    group.addoption(
        "--workdir",
        default=None,
        dest="azl_workdir",
        metavar="DIR",
        help=(
            "Working directory for repo metadata caches. If set, it is "
            "reused as-is and never cleaned (post-mortem friendly). "
            "Otherwise a fresh temp directory is created and cleaned up "
            "at session end."
        ),
    )
    group.addoption(
        "--expected-vendor",
        default="Microsoft Corporation",
        dest="azl_expected_vendor",
        metavar="VENDOR",
        help=(
            "Expected RPM Vendor: tag for every binary package "
            "(checked by test_vendor_tag). Default: Microsoft Corporation."
        ),
    )
    group.addoption(
        "--release-suffix",
        default=r"\.azl4(?:\.\d+|~.*)?$",
        dest="azl_release_suffix",
        metavar="REGEX",
        help=(
            "Regex that every binary package's Release tag must match "
            "(checked by test_release_suffix). Default: "
            "'\\.azl4(?:\\.\\d+|~.*)?$' for AZL4 — accepts the bare "
            "'.azl4' suffix, a '~prerelease' qualifier ('.azl4~rc1'), "
            "or a numeric '.<N>' rebuild bump ('.azl4.4'). Override "
            "for nightly verification of older distros (e.g. AZL3) "
            "without forking the test."
        ),
    )
    group.addoption(
        "--known-violations-dir",
        default=None,
        dest="azl_known_violations_dir",
        metavar="DIR",
        help=(
            "Directory containing per-test known-violations TOML files "
            "(one file per test, named ``<test-stem>.toml``). When "
            "unset, each test loads its file from "
            "``<test-file-dir>/known-violations/<test-stem>.toml``. "
            "Use this to point a CI run at an alternative allowlist "
            "tree without editing the in-repo defaults."
        ),
    )
    group.addoption(
        "--summary-json",
        default=None,
        dest="azl_summary_json",
        metavar="PATH",
        help=(
            "If set, write a JSON summary of known-violation classifications "
            "to PATH at session end. One record per "
            "(test_nodeid, arch, source_label) describes the bucketed "
            "verdicts (real_fails, known_violations, stale) so CI can "
            "gate on real failures while surfacing stale-allowlist "
            "drift without re-parsing pytest output. Pair with stock "
            "``--junitxml`` for per-subtest pass/fail/xfail records. "
            "Not supported under pytest-xdist (``-n``): per-worker "
            "aggregation is not implemented yet, so the combination is "
            "rejected at startup rather than producing a silently-empty "
            "summary file."
        ),
    )


# ---------------------------------------------------------------------------
# Configuration validation
# ---------------------------------------------------------------------------


def pytest_configure(config: pytest.Config) -> None:
    """Validate global CLI args early and record session-wide derived state.

    We do parsing/validation here (rather than in fixtures) so a
    misconfiguration is reported once with a clean message, before any
    test collection or fixture setup.

    No-``--repo`` policy: this hook runs for **every** pytest
    invocation in the active environment (we're loaded as a
    ``pytest11`` entry point). We therefore must not raise
    :class:`pytest.UsageError` when the user provides no
    ``--repo`` — that would break ``pytest --collect-only``, IDE test
    introspection, and unrelated test suites that share the venv.
    Repo-dependent tests skip cleanly via
    :func:`pytest_generate_tests` and the ``require_named_repos``
    fixture instead.
    """
    inline = list(config.getoption("azl_repos"))
    files = list(config.getoption("azl_repos_files"))
    prefixes = list(config.getoption("azl_repo_prefixes"))

    arches: list[str] = list(config.getoption("azl_arches")) or ["x86_64"]
    seen: set[str] = set()
    deduped_arches: list[str] = []
    for a in arches:
        if a in seen:
            continue
        seen.add(a)
        deduped_arches.append(a)

    # The probing arch for --repo-prefix is the first --arch (after
    # dedup) so the user can steer the probe (e.g., --arch aarch64) when
    # x86_64 isn't published. Picking deterministically — rather than
    # probing every arch — keeps the model "one Repo per (channel, kind)
    # with $basearch placeholder" intact; asymmetric layouts should use
    # explicit --repo.
    probe_arch = deduped_arches[0]

    repos: list[Repo] = []
    if inline or files or prefixes:
        try:
            repos = collect_repos(
                inline=inline,
                file_paths=files,
                prefixes=prefixes,
                probe_arch=probe_arch,
            )
        except RepoSpecError as exc:
            raise pytest.UsageError(str(exc)) from exc

    releasever: str | None = config.getoption("azl_releasever")
    needs_releasever = any("$releasever" in r.url for r in repos)
    if needs_releasever and not releasever:
        urls_using_it = ", ".join(r.name for r in repos if "$releasever" in r.url)
        raise pytest.UsageError(
            f"--releasever is required because the URL(s) for: {urls_using_it} "
            "contain $releasever. We never inherit this from the host."
        )

    config._azl_repos = repos  # type: ignore[attr-defined]
    config._azl_arches = deduped_arches  # type: ignore[attr-defined]
    config._azl_releasever = releasever  # type: ignore[attr-defined]
    config._azl_expected_vendor = config.getoption(  # type: ignore[attr-defined]
        "azl_expected_vendor"
    )
    config._azl_release_suffix = config.getoption(  # type: ignore[attr-defined]
        "azl_release_suffix"
    )
    config._azl_known_violations_dir = config.getoption(  # type: ignore[attr-defined]
        "azl_known_violations_dir"
    )

    # JSON-summary accumulator. Always-on so the ``summary_recorder``
    # fixture is a no-op-but-callable when ``--summary-json`` is unset
    # (tests don't have to branch). The hook below decides whether
    # to actually write the file.
    summary_path = config.getoption("azl_summary_json")
    if summary_path:
        # Hard-fail if the user is also running under xdist: each
        # worker process keeps its own ``_azl_summary_records`` list,
        # they all race to write the same path in their own
        # ``pytest_sessionfinish``, and the controller's run finishes
        # last with an empty list -- so the on-disk file ends up
        # empty and the actually-collected records are silently
        # discarded. Per-worker aggregation is the proper fix and is
        # tracked separately; for now reject the combination outright
        # so a CI run can't go green-but-empty without anyone noticing.
        try:
            numprocesses = config.getoption("numprocesses", default=None)
        except ValueError:
            # ``--numprocesses`` is registered by pytest-xdist; if the
            # plugin isn't installed in this venv the option does not
            # exist and getoption raises ValueError. That's fine -- no
            # xdist means no race.
            numprocesses = None
        # ``numprocesses`` may be None (no -n), 0 (-n 0 -> sequential),
        # a positive int, "auto", or "logical". Anything truthy other
        # than 0 means xdist will spawn workers.
        if numprocesses not in (None, 0, "0"):
            raise pytest.UsageError(
                "--summary-json is not supported under pytest-xdist "
                f"(got --numprocesses={numprocesses!r}); each worker "
                "would race to overwrite the summary file with its own "
                "partial record set, and the controller's empty-record "
                "write would land last. Run without -n, or omit "
                "--summary-json."
            )
    config._azl_summary_json_path = (  # type: ignore[attr-defined]
        Path(summary_path) if summary_path else None
    )
    config._azl_summary_records = []  # type: ignore[attr-defined]


# ---------------------------------------------------------------------------
# JSON-summary writer
# ---------------------------------------------------------------------------


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    """Write the accumulated known-violations summary to ``--summary-json``.

    Records are appended by tests via the ``summary_recorder`` fixture
    (see ``conftest.py``). One record per (test_nodeid, arch,
    source_label) tuple, dumped as a JSON object with ``schema_version``,
    ``exit_status`` (the pytest exit code: 0 = all passed, 1 = test
    failures, 2 = interrupted, 3 = internal error, 4 = usage error,
    5 = no tests collected), and ``records`` keys. Written even when
    no records were produced (so CI gets a well-formed empty file
    rather than a missing file).
    """
    config = session.config
    path: Path | None = getattr(config, "_azl_summary_json_path", None)
    if path is None:
        return

    records: list[dict] = getattr(config, "_azl_summary_records", [])
    payload = {
        "schema_version": SUMMARY_JSON_SCHEMA_VERSION,
        "exit_status": int(exitstatus),
        "records": records,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".partial")
    tmp.write_text(json.dumps(payload, indent=2, sort_keys=True))
    tmp.replace(path)


# ---------------------------------------------------------------------------
# Marker-driven parametrization
# ---------------------------------------------------------------------------


def _get_marker_values(metafunc: pytest.Metafunc, name: str) -> list[str]:
    """Collect arg values from all markers of the given name on a test."""
    values: list[str] = []
    for marker in metafunc.definition.iter_markers(name):
        if not marker.args:
            raise pytest.UsageError(
                f"@pytest.mark.{name}(...) requires an argument on "
                f"{metafunc.definition.nodeid}"
            )
        values.extend(str(a) for a in marker.args)
    return values


def _filter_repos_by_markers(
    metafunc: pytest.Metafunc, repos: list[Repo]
) -> list[Repo]:
    """Apply ``repo_kind`` / ``repo_name`` markers to narrow the repo set."""
    kinds = _get_marker_values(metafunc, "repo_kind")
    names = _get_marker_values(metafunc, "repo_name")

    filtered = repos
    if kinds:
        kinds_set = set(kinds)
        filtered = [r for r in filtered if r.kind in kinds_set]
    if names:
        names_set = set(names)
        filtered = [r for r in filtered if r.name in names_set]
    return filtered


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    """Fan tests out over the matching ``(repo, arch)`` pairs."""
    config = metafunc.config
    repos: list[Repo] = getattr(config, "_azl_repos", [])
    arches: list[str] = getattr(config, "_azl_arches", [])

    needs_repo = "repo" in metafunc.fixturenames
    needs_arch = "arch" in metafunc.fixturenames

    if needs_repo:
        candidates = _filter_repos_by_markers(metafunc, repos)
        if not candidates:
            kinds = _get_marker_values(metafunc, "repo_kind")
            names = _get_marker_values(metafunc, "repo_name")
            reason = (
                f"no --repo matched markers (kinds={kinds or '<any>'}, "
                f"names={names or '<any>'}); "
                f"provided: {[(r.name, r.kind) for r in repos]}"
            )
            metafunc.parametrize(
                "repo",
                [pytest.param(None, marks=pytest.mark.skip(reason=reason))],
                ids=["no-matching-repo"],
            )
            if needs_arch:
                metafunc.parametrize("arch", arches or ["x86_64"])
            return

        if needs_arch:
            params = [(r, a) for r in candidates for a in arches]
            ids = [f"{r.name}-{a}" for r, a in params]
            metafunc.parametrize("repo,arch", params, ids=ids)
        else:
            metafunc.parametrize(
                "repo", candidates, ids=[r.name for r in candidates]
            )
        return

    if needs_arch:
        metafunc.parametrize("arch", arches)
