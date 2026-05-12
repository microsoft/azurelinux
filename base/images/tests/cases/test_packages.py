# SPDX-License-Identifier: MIT
"""Validate installed and excluded packages.

These tests query the RPM database via ``rpm --root``, so they only
make sense on images that ship one. The ``runtime-package-management``
capability marker gates them — distroless container variants without
an rpmdb are automatically skipped.
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
    missing = REQUIRED_PACKAGES - installed_packages
    assert not missing, f"Required packages missing: {sorted(missing)}"


@pytest.mark.require_capability("runtime-package-management")
@pytest.mark.parametrize("pkg", sorted(BLOCKLISTED_PACKAGES))
def test_blocklisted_package_absent(
    pkg: str, installed_packages: set[str]
) -> None:
    assert pkg not in installed_packages, f"Blocklisted package installed: {pkg}"
