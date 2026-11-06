# SPDX-License-Identifier: MIT
"""Validate container RPM payload filtering and build-time policy cleanup."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pathlib import Path

pytestmark = pytest.mark.require_capability("container")


def test_bootstrap_language_macro_absent(rootfs: Path) -> None:
    """Do not ship the build-time RPM language override."""
    assert not (rootfs / "etc/rpm/macros.kiwi-image-config").exists()
    assert not (rootfs / "etc/rpm/macros.container-languages").exists()


@pytest.mark.require_capability("runtime-package-management")
def test_bootstrap_language_package_absent(installed_packages: set[str]) -> None:
    """Do not ship the retired custom language-policy RPM."""
    assert "azurelinux-release-locale-minimal" not in installed_packages


@pytest.mark.image("container-base")
def test_rpm_excludedocs(rootfs: Path) -> None:
    """Exclude RPM documentation without removing licenses."""
    assert not (rootfs / "usr/share/doc/bash/README").exists(), "Bash documentation was not excluded"
    assert (rootfs / "usr/share/licenses/bash/COPYING").is_file(), "Bash license must be retained"


def test_only_english_message_catalogs(rootfs: Path, image_name: str | None) -> None:
    """Keep only C, POSIX, and English catalogs in the filtered base image."""
    if image_name != "container-base":
        pytest.skip("Bootstrap language filtering is enabled only for container-base")

    unexpected = [
        catalog.relative_to(rootfs).as_posix()
        for catalog in (rootfs / "usr/share/locale").glob("*/LC_MESSAGES/*")
        if catalog.is_file()
        and catalog.parent.parent.name.split("_", 1)[0].split("@", 1)[0].split(".", 1)[0] not in {"C", "POSIX", "en"}
    ]
    assert not unexpected, f"Unexpected non-English message catalogs: {unexpected}"
