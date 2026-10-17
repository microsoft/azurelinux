# SPDX-License-Identifier: MIT
"""Validate container package inventories independently of runtime package management."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pathlib import Path

pytestmark = pytest.mark.require_capability("container")

_RPM_MIN_FIELDS = 5
_MAIN_PACKAGES = {
    "container-busybox": "busybox",
    "container-nginx": "nginx",
    "container-postgres": "postgresql-server",
    "container-telegraf": "telegraf",
    "container-python": "python3",
    "container-nodejs": "nodejs",
    "container-pytorch": "python3-torch",
}


def test_container_package_inventory(image_path: Path | None, image_name: str | None) -> None:
    """Built containers must have a nonempty inventory with the main package's version."""
    if image_path is None:
        pytest.skip("package inventories require a local image artifact")

    stem = image_path.name.removesuffix(".xz").removesuffix(".tar").removesuffix(".oci")
    inventory = image_path.with_name(f"{stem}.packages")
    assert inventory.is_file(), f"Missing package inventory: {inventory}"

    versions: dict[str, str] = {}
    for line in inventory.read_text().splitlines():
        if not line.strip():
            continue
        fields = line.split("|")
        assert len(fields) >= _RPM_MIN_FIELDS, f"Invalid package inventory entry: {line!r}"
        name, _, version, release, arch = fields[:_RPM_MIN_FIELDS]
        assert all((name, version, release, arch)), f"Incomplete package inventory entry: {line!r}"
        versions[name] = f"{version}-{release}"

    assert versions, f"Package inventory is empty: {inventory}"
    main_package = _MAIN_PACKAGES.get(image_name or "")
    if main_package is not None:
        assert main_package in versions, f"Package inventory is missing {main_package}: {inventory}"


def test_container_package_database_retained(installed_packages: set[str]) -> None:
    """Containers retain queryable package records without requiring RPM/DNF executables."""
    assert installed_packages, "Container RPM database has no installed-package records"
