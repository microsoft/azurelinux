# SPDX-License-Identifier: MIT
"""Test-facing fixture surface for Azure Linux repo validation.

This module is the single place tests touch. They never reach below
into ``utils.metadata``, ``utils.repodata``, or ``utils.repoclosure``
directly — those are implementation. To wire new data into a test,
extend the relevant service and add (or extend) a fixture here.

CLI options, markers, and the parametrize-time fan-out across
``(repo, arch)`` pairs all live in :mod:`utils.pytest_plugin`.
"""

from __future__ import annotations

import logging
import shutil
import tempfile
from pathlib import Path
from typing import Generator

import pytest

from utils.metadata import MetadataService
from utils.known_violations import (
    ClassifiedViolations,
    KnownViolationsFile,
    load_known_violations,
)
from utils.repoclosure import Repoclosure, make_repoclosure
from utils.repos import Repo
from utils.types import FileMeta, FileOwner, NEVRA, Package, RepoclosureResult

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Session-scoped basics
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def workdir(request: pytest.FixtureRequest) -> Generator[Path, None, None]:
    """Working directory for repo metadata caches.

    If ``--workdir`` is set, the directory is reused as-is and never
    removed (post-mortem friendly). Otherwise a fresh temp directory
    is created and cleaned up at session end.
    """
    explicit = request.config.getoption("azl_workdir")
    if explicit:
        p = Path(explicit).resolve()
        p.mkdir(parents=True, exist_ok=True)
        logger.debug("Workdir (explicit, will not be removed): %s", p)
        yield p
        return

    p = Path(tempfile.mkdtemp(prefix="azl-repo-tests-"))
    logger.debug("Workdir (temp, will be removed at session end): %s", p)
    try:
        yield p
    finally:
        shutil.rmtree(p, ignore_errors=True)


@pytest.fixture(scope="session")
def releasever(request: pytest.FixtureRequest) -> str | None:
    """Effective ``$releasever`` for this run, or ``None`` if not set."""
    return getattr(request.config, "_azl_releasever", None)


@pytest.fixture(scope="session")
def expected_vendor(request: pytest.FixtureRequest) -> str:
    """The expected RPM Vendor: tag (driven by ``--expected-vendor``)."""
    return getattr(
        request.config, "_azl_expected_vendor", "Microsoft Corporation"
    )


@pytest.fixture(scope="session")
def release_suffix_pattern(request: pytest.FixtureRequest) -> str:
    """The expected Release-tag regex (driven by ``--release-suffix``)."""
    return getattr(
        request.config, "_azl_release_suffix", r"\.azl4(?:\.\d+|~.*)?$"
    )


@pytest.fixture(scope="session")
def all_repos(request: pytest.FixtureRequest) -> list[Repo]:
    """Every repo passed via ``--repo`` / ``--repos-file`` (in input order)."""
    return list(getattr(request.config, "_azl_repos", []))


@pytest.fixture(scope="session")
def binary_repos(all_repos: list[Repo]) -> list[Repo]:
    """All ``binary`` repos."""
    return [r for r in all_repos if r.kind == "binary"]


@pytest.fixture(scope="session")
def srpm_repos(all_repos: list[Repo]) -> list[Repo]:
    """All ``srpm`` repos."""
    return [r for r in all_repos if r.kind == "srpm"]


@pytest.fixture(scope="session")
def debuginfo_repos(all_repos: list[Repo]) -> list[Repo]:
    """All ``debuginfo`` repos."""
    return [r for r in all_repos if r.kind == "debuginfo"]


# ---------------------------------------------------------------------------
# Service layer fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def metadata_service(workdir: Path, releasever: str | None) -> MetadataService:
    """Service that loads repo packages and file lists from repodata.

    Tests should not call this directly — use the higher-level
    fixtures (``repo_packages``, ``all_binary_packages``,
    ``cross_repo_file_index``) instead.
    """
    return MetadataService(workdir=workdir, releasever=releasever)


@pytest.fixture(scope="session")
def _repoclosure_runner(metadata_service: MetadataService) -> Repoclosure:
    """The libdnf5-backed in-process repoclosure runner.

    Tests should not call this directly — use the ``repoclosure``
    fixture instead. The metadata cache is shared with
    ``metadata_service`` so we never double-fetch.
    """
    return make_repoclosure(metadata_service)


# ---------------------------------------------------------------------------
# High-level test-facing fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def repo_packages(metadata_service: MetadataService):
    """Return a callable ``(repo, arch) -> list[Package]``."""
    def _load(repo: Repo, arch: str) -> list[Package]:
        return metadata_service.list_packages(repo, arch)

    return _load


@pytest.fixture
def all_binary_packages(metadata_service: MetadataService, binary_repos: list[Repo]):
    """Return a callable ``arch -> dict[Repo, list[Package]]``."""
    def _load(arch: str) -> dict[Repo, list[Package]]:
        return {r: metadata_service.list_packages(r, arch) for r in binary_repos}

    return _load


@pytest.fixture
def cross_repo_file_index(
    metadata_service: MetadataService, binary_repos: list[Repo]
):
    """Return a callable ``arch -> dict[path, list[FileOwner]]``."""
    def _load(arch: str) -> dict[str, list[FileOwner]]:
        return metadata_service.build_file_index(binary_repos, arch)

    return _load


@pytest.fixture
def package_file_metadata(
    metadata_service: MetadataService,
    all_binary_packages,
):
    """Return a callable ``(arch, nevra) -> dict[path, FileMeta]``.

    The metadata service downloads the requested RPM on first lookup
    (and caches it on disk under the workdir) and parses per-file
    attributes — ``mode`` / ``user`` / ``group`` / ``size`` /
    ``digest`` / ``linkto`` / ``rdev`` — out of its header. This is
    the data the cross-repo file-conflicts test needs to mirror RPM's
    own ``rpmfilesCompare`` rules; ``filelists.xml`` does not carry
    any of it.

    Lookups are O(1) after the first call per arch — we build the
    NEVRA → (Repo, Package) map once and memoize it.
    """
    cached_index: dict[str, dict[NEVRA, tuple[Repo, Package]]] = {}

    def _build_index(arch: str) -> dict[NEVRA, tuple[Repo, Package]]:
        if arch in cached_index:
            return cached_index[arch]
        idx: dict[NEVRA, tuple[Repo, Package]] = {}
        for repo, packages in all_binary_packages(arch).items():
            for pkg in packages:
                if pkg.is_source:
                    continue
                # Identical NEVRAs in two repos: keep the first
                # encountered, mirroring the dedup behaviour in
                # build_file_index. The RPM bytes are identical, so
                # which repo we fetch from doesn't matter.
                idx.setdefault(pkg.nevra, (repo, pkg))
        cached_index[arch] = idx
        return idx

    def _load(arch: str, nevra: NEVRA) -> dict[str, FileMeta]:
        idx = _build_index(arch)
        try:
            repo, pkg = idx[nevra]
        except KeyError as exc:
            raise KeyError(
                f"NEVRA {nevra} not found in any binary repo at arch "
                f"{arch}; the cross-repo file index referenced a NEVRA "
                f"that doesn't appear in primary metadata"
            ) from exc
        return metadata_service.fetch_package_files(repo, pkg, arch)

    return _load


@pytest.fixture
def repoclosure(_repoclosure_runner: Repoclosure):
    """Return a callable that runs repoclosure.

    Signature::

        repoclosure(
            target_repos,           # repos whose packages we expect to close
            arch,                   # target architecture
            *,
            universe_repos=None,    # wider universe (defaults to target_repos)
            check_kind="binary",    # "binary" | "buildtime" | "all"
        ) -> RepoclosureResult

    See :class:`utils.repoclosure.Repoclosure` for argument semantics.
    """
    def _run(
        target_repos: list[Repo],
        arch: str,
        *,
        universe_repos: list[Repo] | None = None,
        check_kind: str = "binary",
    ) -> RepoclosureResult:
        return _repoclosure_runner.run(
            target_repos=target_repos,
            arch=arch,
            universe_repos=universe_repos,
            check_kind=check_kind,
        )

    return _run


# ---------------------------------------------------------------------------
# Helper available to tests that have hard-coded repo expectations.
# ---------------------------------------------------------------------------


@pytest.fixture
def require_named_repos(all_repos: list[Repo]):
    """Helper used by hard-coded tests like ``test_repoclosure_base_plus_sdk_full``."""
    by_name = {r.name: r for r in all_repos}

    def _require(expected: list[str], *, kind: str | None = None) -> list[Repo]:
        present = [n for n in expected if n in by_name]
        if len(present) != len(expected):
            missing = sorted(set(expected) - set(present))
            pytest.fail(
                f"misconfigured run: expected --repo for {expected} but "
                f"missing {missing}; this test is hard-coded for those "
                f"named repos and is only meaningful with the full set. "
                f"Pass them via --repo / --repos-file or use pytest -k / "
                f"--ignore to deselect this test if you intentionally want "
                f"to skip it."
            )
        repos = [by_name[n] for n in expected]
        if kind is not None:
            wrong_kind = [r for r in repos if r.kind != kind]
            if wrong_kind:
                pytest.fail(
                    f"expected all of {expected} to have kind={kind!r}, but "
                    f"{[(r.name, r.kind) for r in wrong_kind]} did not"
                )
        return repos

    return _require


# ---------------------------------------------------------------------------
# Known-violations file loader (per-test).
# ---------------------------------------------------------------------------


@pytest.fixture
def known_violations(request: pytest.FixtureRequest) -> KnownViolationsFile:
    """Load the known-violations TOML file for the calling test.

    The file is read from
    ``<test-file-dir>/known-violations/<test-stem>.toml`` by default,
    or from ``<--known-violations-dir>/<test-stem>.toml`` when
    ``--known-violations-dir`` is set on the command line. The file
    is parsed and validated against
    ``cases/known-violations.schema.json`` at load time, so authoring
    mistakes surface here with a clear message rather than as a
    confusing ``KeyError`` deep in the test.

    Tests that don't use an allowlist (e.g. ``test_repoclosure_base``)
    simply don't request this fixture.
    """
    cli_dir = getattr(request.config, "_azl_known_violations_dir", None)
    test_file = Path(request.path)
    stem = test_file.stem
    if cli_dir:
        path = Path(cli_dir) / f"{stem}.toml"
    else:
        path = test_file.parent / "known-violations" / f"{stem}.toml"
    return load_known_violations(path)


# ---------------------------------------------------------------------------
# JSON-summary recorder.
# ---------------------------------------------------------------------------


@pytest.fixture
def summary_recorder(request: pytest.FixtureRequest):
    """Return a callable that appends a known-violations summary record.

    Signature::

        summary_recorder(*, arch, source_label, classified)

    Each call appends one record describing the bucketed verdicts
    (``real_fails``, ``known_violations``, ``stale``) for the
    calling test on the given arch and allowlist source. The records
    are accumulated session-wide and written as JSON at session end
    when ``--summary-json=PATH`` is set (see
    :func:`utils.pytest_plugin.pytest_sessionfinish`).

    The fixture is always callable; if ``--summary-json`` is unset
    the records still accumulate but the writer is a no-op. Tests
    that produce per-arch / per-section classifications can call
    this once per (arch, section) pair without branching.
    """
    nodeid = request.node.nodeid
    records: list[dict] = request.config._azl_summary_records  # type: ignore[attr-defined]

    def _record(
        *,
        arch: str,
        source_label: str,
        classified: ClassifiedViolations,
    ) -> None:
        def _verdict_dict(v) -> dict:
            d = {
                "key": str(v.key),
                "consumer": v.consumer,
                "observed": sorted(v.observed),
                "listed": sorted(v.listed) if v.listed is not None else None,
            }
            # Per-entry metadata (ST2): omit when absent so the JSON
            # stays small for the bare-array short form.
            if v.reason is not None:
                d["reason"] = v.reason
            if v.issue is not None:
                d["issue"] = v.issue
            return d

        records.append(
            {
                "test_nodeid": nodeid,
                "arch": arch,
                "source_label": source_label,
                "real_fails": [_verdict_dict(v) for v in classified.real_fails],
                "known_violations": [
                    _verdict_dict(v) for v in classified.known_violations
                ],
                "stale": [
                    {
                        "consumer": s.consumer,
                        "kind": s.kind,
                        "listed_dep": s.listed_dep,
                    }
                    for s in classified.stale
                ],
            }
        )

    return _record
