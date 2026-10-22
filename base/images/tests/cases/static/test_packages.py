# SPDX-License-Identifier: MIT
"""Validate installed and excluded packages.

These policy checks apply to images with runtime package management.
Minimal-container inventories and retained package records are checked
independently in ``test_container_inventory.py``.
"""

from __future__ import annotations

import pytest

# Packages that must be present in every image with an rpmdb.
REQUIRED_PACKAGES = {
    "azurelinux-release-common",
}

# Packages that must NOT be present in any Azure Linux image.
BLOCKLISTED_PACKAGES = {
    "fedora-release",
    "fedora-logos",
    "redhat-rpm-config",
}


@pytest.mark.require_capability("runtime-package-management")
def test_required_packages_installed(installed_packages: set[str]) -> None:
    """Verify every required package is installed."""
    missing = REQUIRED_PACKAGES - installed_packages
    assert not missing, f"Required packages missing: {sorted(missing)}"


@pytest.mark.require_capability("runtime-package-management")
@pytest.mark.parametrize("pkg", sorted(BLOCKLISTED_PACKAGES))
def test_blocklisted_package_absent(pkg: str, installed_packages: set[str]) -> None:
    """Verify blocklisted packages are not installed."""
    assert pkg not in installed_packages, f"Blocklisted package installed: {pkg}"
