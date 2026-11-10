# SPDX-License-Identifier: MIT
"""Validate installed and excluded packages.

These tests query the RPM database via ``rpm --root``, so they only
make sense on images that ship one. The ``runtime-package-management``
capability marker gates them — distroless container variants without
an rpmdb are automatically skipped.
"""

from __future__ import annotations

import sqlite3
from contextlib import closing
from fnmatch import fnmatchcase
from typing import TYPE_CHECKING

import pytest
from utils.extract import resolve_path_confined

if TYPE_CHECKING:
    from pathlib import Path

# Packages that must be present in every image with an rpmdb.
REQUIRED_PACKAGES = {
    "azurelinux-release-common",
}


@pytest.mark.require_capability("runtime-package-management")
def test_required_packages_installed(installed_packages: set[str]) -> None:
    """Verify every required package is installed."""
    missing = REQUIRED_PACKAGES - installed_packages
    assert not missing, f"Required packages missing: {sorted(missing)}"


@pytest.mark.require_capability("container")
@pytest.mark.require_capability("runtime-package-management")
def test_container_rpm_database_compacted(rootfs: Path) -> None:
    """Container RPM databases must not retain reusable SQLite pages."""
    database = resolve_path_confined(rootfs, "usr/lib/sysimage/rpm/rpmdb.sqlite")
    assert database.is_file(), f"Missing RPM database: {database}"
    wal = resolve_path_confined(rootfs, "usr/lib/sysimage/rpm/rpmdb.sqlite-wal")
    assert not wal.exists() or wal.stat().st_size == 0, f"RPM database has an uncheckpointed WAL: {wal}"
    with closing(sqlite3.connect(f"{database.as_uri()}?mode=ro&immutable=1", uri=True)) as connection:
        free_pages = connection.execute("PRAGMA freelist_count").fetchone()[0]
    assert free_pages == 0, f"RPM database retains {free_pages} unused pages"


@pytest.mark.require_capability("runtime-package-management")
@pytest.mark.parametrize("blocked_package", [
    "fedora-logos",
    "fedora-release",
    "redhat-rpm-config",
    pytest.param("gnutls", marks=pytest.mark.image("container-base")),
    pytest.param("gnutls-*", marks=pytest.mark.image("container-base")),
])
def test_blocklisted_package_absent(blocked_package: str, installed_packages: set[str]) -> None:
    """Verify blocked package-name globs match no installed packages."""
    unexpected = sorted(name for name in installed_packages if fnmatchcase(name, blocked_package))
    assert not unexpected, f"Blocked packages installed: {unexpected}"
