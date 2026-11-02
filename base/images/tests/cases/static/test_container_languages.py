# SPDX-License-Identifier: MIT
"""Validate the lifecycle of the bootstrap-only container language policy."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pathlib import Path

pytestmark = pytest.mark.require_capability("container")


def test_bootstrap_language_macro_absent(rootfs: Path) -> None:
    """Do not ship the build-time RPM language override."""
    assert not (rootfs / "etc/rpm/macros.container-languages").exists()


@pytest.mark.require_capability("runtime-package-management")
def test_bootstrap_language_package_absent(installed_packages: set[str]) -> None:
    """Remove the policy RPM rather than only deleting its macro."""
    assert "azurelinux-release-locale-minimal" not in installed_packages


def test_only_english_message_catalogs(rootfs: Path, image_name: str | None) -> None:
    """Keep only C, POSIX, and English catalogs in the filtered images."""
    if image_name not in {"container-base", "container-distroless-minimal"}:
        pytest.skip("Bootstrap language filtering is enabled only for base and distroless-minimal")

    unexpected = [
        catalog.relative_to(rootfs).as_posix()
        for catalog in (rootfs / "usr/share/locale").glob("*/LC_MESSAGES/*")
        if catalog.is_file()
        and catalog.parent.parent.name.split("_", 1)[0].split("@", 1)[0].split(".", 1)[0] not in {"C", "POSIX", "en"}
    ]
    assert not unexpected, f"Unexpected non-English message catalogs: {unexpected}"
