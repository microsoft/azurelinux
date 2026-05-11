# SPDX-License-Identifier: MIT
"""Service layer that turns raw repodata into typed package + file
records for tests.

This is what conftest.py fixtures call into. Tests do not import this
directly.

Responsibilities:

* Memoize package lists per ``(repo.fingerprint, arch)``. The
  ``releasever`` is captured at construction time so the cache key
  doesn't need to repeat it.
* Build the cross-repo file index used by the file-conflicts test.
* Map :class:`~utils.repodata.RepodataError` raised below into
  ``pytest.fail`` calls so test output stays focused on the failing
  test rather than tracebacks from the loader.
"""

from __future__ import annotations

import logging
import os
from collections import defaultdict
from pathlib import Path

import pytest

from .repodata import (
    RepoLayout,
    RepodataError,
    RpmDownloadError,
    download_rpm,
    fetch_repo,
    iter_filelist_entries,
    iter_packages,
    read_rpm_file_metadata,
)
from .repos import Repo
from .types import FileMeta, FileOwner, Package

logger = logging.getLogger(__name__)


class MetadataService:
    """Caching loader for package metadata across repos.

    A single instance is created at session scope by the
    ``metadata_service`` fixture.
    """

    def __init__(self, *, workdir: Path, releasever: str | None) -> None:
        self._workdir = workdir
        self._releasever = releasever
        self._packages_cache: dict[tuple[str, str], list[Package]] = {}
        self._file_index_cache: dict[
            tuple[tuple[str, ...], str], dict[str, list[FileOwner]]
        ] = {}
        self._layout_cache: dict[tuple[str, str], RepoLayout] = {}
        # Per-NEVRA cache of {path -> FileMeta} for packages that have
        # had their RPM downloaded for ``rpmfilesCompare``-style
        # comparison (used by the cross-repo file-conflicts test).
        # Keyed on NEVRA alone (epoch / version / release / arch fully
        # determine the RPM contents, regardless of the repo it was
        # served from).
        self._package_files_cache: dict[
            tuple[str, int, str, str, str], dict[str, FileMeta]
        ] = {}

    # ------------------------------------------------------------------
    # Caching helpers
    # ------------------------------------------------------------------

    def cache_dir_for(self, repo: Repo, arch: str) -> Path:
        """Stable per-repo, per-arch cache dir.

        Scoped by xdist worker so concurrent workers never share a
        librepo destdir (librepo writes the same filenames each run,
        so two workers fetching the same repo would race on
        ``repomd.xml`` writes). Also exposed publicly so the
        repoclosure module can reuse the same on-disk metadata.
        """
        rv = self._releasever or "none"
        worker = os.environ.get("PYTEST_XDIST_WORKER", "main")
        return (
            self._workdir
            / "repodata"
            / f"rv-{rv}"
            / worker
            / arch
            / f"{repo.name}-{repo.fingerprint}"
        )

    def fetch(self, repo: Repo, arch: str) -> RepoLayout:
        """Fetch (or reuse a cached) metadata layout for ``(repo, arch)``."""
        key = (repo.fingerprint, arch)
        if key in self._layout_cache:
            return self._layout_cache[key]
        try:
            layout = fetch_repo(
                base_url=repo.url,
                cache_dir=self.cache_dir_for(repo, arch),
                arch=arch,
                releasever=self._releasever,
            )
        except RepodataError as exc:
            pytest.fail(
                f"failed to fetch metadata for repo {repo.name!r} "
                f"at arch {arch}: {exc}"
            )
        self._layout_cache[key] = layout
        return layout

    # ------------------------------------------------------------------
    # Public surface
    # ------------------------------------------------------------------

    def list_packages(self, repo: Repo, arch: str) -> list[Package]:
        """Return every package in *repo* at *arch*. Memoized per call."""
        key = (repo.fingerprint, arch)
        if key in self._packages_cache:
            return self._packages_cache[key]
        layout = self.fetch(repo, arch)
        try:
            packages = list(iter_packages(layout.primary))
        except RepodataError as exc:
            pytest.fail(
                f"failed to parse primary metadata for repo {repo.name!r} "
                f"at arch {arch}: {exc}"
            )
        self._packages_cache[key] = packages
        logger.debug(
            "Loaded %d package(s) from repo %s for arch %s",
            len(packages), repo.name, arch,
        )
        return packages

    def build_file_index(
        self, repos: list[Repo], arch: str
    ) -> dict[str, list[FileOwner]]:
        """Return ``path -> [FileOwner, ...]`` for every *real* file across *repos*.

        This is the *first-pass* index used by the cross-repo
        file-conflicts test. Filtering applied here is intentionally
        cheap and metadata-only:

        * Directory entries (``type="dir"``) — RPM permits shared
          directory ownership when modes/owner/group match; the
          ``rpmfilesCompare``-equivalent comparison in the test
          itself re-validates that, but for path-overlap discovery
          we drop dirs because RPM's vast majority of legitimate
          shared ownerships are dirs and including them would force
          a per-package RPM download for nearly every repo file.
        * Ghost entries (``type="ghost"``) — these mean "I claim this
          path but don't install it". Multiple packages can ghost the
          same path; that is the canonical mechanism for non-conflicting
          shared file ownership in RPM, and ``rpmfilesCompare`` short-
          circuits any pair where either side is ghost.

        Identical NEVRAs that appear in multiple repos contribute a
        single :class:`FileOwner` (the first repo encountered wins for
        the ``repo_name`` attribution).

        The returned overlaps are *candidates*: the test layer uses
        :meth:`fetch_package_files` to download the involved RPMs and
        compare per-file metadata via the same rules
        ``rpmfilesCompare`` itself applies.
        """
        key = (tuple(sorted(r.fingerprint for r in repos)), arch)
        if key in self._file_index_cache:
            return self._file_index_cache[key]

        # path -> { NEVRA -> FileOwner }, so we can dedupe by NEVRA.
        path_to_owners: dict[str, dict[object, FileOwner]] = defaultdict(dict)

        for repo in repos:
            layout = self.fetch(repo, arch)
            try:
                for entry in iter_filelist_entries(layout.filelists):
                    if entry.is_directory or entry.is_ghost:
                        continue
                    owner = FileOwner(
                        nevra=entry.nevra,
                        repo_name=repo.name,
                        is_directory=False,
                        is_ghost=False,
                    )
                    bucket = path_to_owners[entry.path]
                    bucket.setdefault(entry.nevra, owner)
            except RepodataError as exc:
                pytest.fail(
                    f"failed to load filelists for repo {repo.name!r} "
                    f"at arch {arch}: {exc}"
                )

        result: dict[str, list[FileOwner]] = {
            path: list(owners.values())
            for path, owners in path_to_owners.items()
        }
        self._file_index_cache[key] = result
        logger.debug(
            "Built cross-repo file index for arch %s: %d distinct path(s) "
            "(after filtering directories and ghost entries)",
            arch, len(result),
        )
        return result

    # ------------------------------------------------------------------
    # Per-package file-metadata fetcher (downloads RPMs on demand)
    # ------------------------------------------------------------------

    def _package_cache_dir(self, repo: Repo, arch: str) -> Path:
        """Per-repo, per-arch cache dir for downloaded RPMs.

        Same xdist-worker scoping as :meth:`cache_dir_for` so parallel
        workers never race on the same destination filename. A reused
        ``--workdir`` keeps RPMs warm across runs.
        """
        rv = self._releasever or "none"
        worker = os.environ.get("PYTEST_XDIST_WORKER", "main")
        return (
            self._workdir
            / "rpms"
            / f"rv-{rv}"
            / worker
            / arch
            / f"{repo.name}-{repo.fingerprint}"
        )

    def fetch_package_files(
        self, repo: Repo, package: Package, arch: str
    ) -> dict[str, FileMeta]:
        """Return ``path -> FileMeta`` for *package*, downloading the RPM if needed.

        Memoized per NEVRA: a package that appears in two different
        repos (identical NEVRA) is only fetched once. The downloaded
        RPM is also cached on disk in :meth:`_package_cache_dir` so
        a rerun against the same ``--workdir`` doesn't re-download.

        Raises :class:`utils.repodata.RepodataError` (typically
        :class:`utils.repodata.RpmDownloadError`) if the RPM cannot
        be fetched or read.
        """
        nevra = package.nevra
        key = (nevra.name, nevra.epoch, nevra.version, nevra.release, nevra.arch)
        cached = self._package_files_cache.get(key)
        if cached is not None:
            return cached

        if not package.location_href:
            raise RepodataError(
                f"package {nevra} from repo {repo.name!r} has no "
                f"location_href in primary metadata; cannot fetch the "
                f"RPM to read per-file metadata"
            )

        rpm_path = download_rpm(
            repo_url=repo.url,
            location_href=package.location_href,
            location_base=package.location_base,
            arch=arch,
            releasever=self._releasever,
            dest_dir=self._package_cache_dir(repo, arch),
        )
        meta = read_rpm_file_metadata(rpm_path)
        self._package_files_cache[key] = meta
        logger.debug(
            "Fetched + parsed RPM for %s (%d file entries) from %s",
            nevra, len(meta), repo.name,
        )
        return meta
