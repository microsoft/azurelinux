# SPDX-License-Identifier: MIT
"""Validate /etc/os-release fields. Runs against every image."""

from __future__ import annotations


def test_os_release_has_required_keys(os_release: dict[str, str]) -> None:
    """os-release must contain the distro-identifying keys."""
    for key in ("NAME", "ID", "VERSION_ID"):
        assert key in os_release, f"Missing required key: {key}"


def test_os_release_id(os_release: dict[str, str]) -> None:
    """Verify os-release identifies Azure Linux."""
    assert os_release.get("ID") == "azurelinux"


def test_os_release_version(os_release: dict[str, str]) -> None:
    """Verify os-release identifies Azure Linux 4.0."""
    assert os_release.get("VERSION_ID") == "4.0"


def test_os_release_is_stable(os_release: dict[str, str]) -> None:
    """All image variants must identify the stable release without beta branding."""
    assert os_release.get("RELEASE_TYPE") == "stable"
    for key in ("VERSION", "PRETTY_NAME"):
        value = os_release[key].lower()
        assert "beta" not in value, f"{key} still contains beta branding"
        assert "prerelease" not in value, f"{key} still identifies a prerelease"
