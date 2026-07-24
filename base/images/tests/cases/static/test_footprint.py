# SPDX-License-Identifier: MIT
"""Disk-footprint checks shared across image families.

Sum the installed on-disk size from the RPM ``%{SIZE}`` headers and guard
against gross size regressions. Size caps are looked up per family, since
families (container-base, vm-base, wsl, ...) differ widely in size.

The installed-size tests need an rpmdb, so they gate on the
``runtime-package-management`` capability. The tarball-size test applies
only to families whose artifact is a compressed rootfs tarball (container,
wsl); it skips for VM images, which ship a provisioned raw disk.
"""

from __future__ import annotations

import logging
from collections.abc import Iterable
from pathlib import Path

import pytest

logger = logging.getLogger(__name__)

_BYTES_PER_MB = 1024 * 1024

# Max total installed size (MB) per family; unlisted families fall back to
# the default. Caps catch gross regressions, not normal growth.
_INSTALLED_CAP_MB: dict[str, int] = {
    "container-base": 400,
    "vm-base": 2048,
    "wsl": 800,
}
_INSTALLED_CAP_DEFAULT_MB = 2048

# Max size (MB) of the shipped rootfs tarball per family; smaller than the
# installed-size cap since the artifact is compressed.
_ARTIFACT_CAP_MB: dict[str, int] = {
    "container-base": 200,
    "wsl": 300,
}
_ARTIFACT_CAP_DEFAULT_MB = 300

_TARBALL_IMAGE_TYPES = frozenset({"container", "wsl"})

_LARGEST_PACKAGES_TO_LOG = 15


def _family_of(image_name: str, known: Iterable[str]) -> str | None:
    """Map an ``--image-name`` to its family (e.g. ``container-base-dev`` → ``container-base``)."""
    for family in known:
        if image_name == family or image_name.startswith(family + "-"):
            return family
    return None


def _installed_cap_bytes(image_name: str) -> int:
    family = _family_of(image_name, _INSTALLED_CAP_MB)
    cap_mb = _INSTALLED_CAP_MB.get(family, _INSTALLED_CAP_DEFAULT_MB) if family else _INSTALLED_CAP_DEFAULT_MB
    return cap_mb * _BYTES_PER_MB


def _artifact_cap_bytes(image_name: str) -> int:
    family = _family_of(image_name, _ARTIFACT_CAP_MB)
    cap_mb = _ARTIFACT_CAP_MB.get(family, _ARTIFACT_CAP_DEFAULT_MB) if family else _ARTIFACT_CAP_DEFAULT_MB
    return cap_mb * _BYTES_PER_MB


def _log_footprint(package_sizes: dict[str, int]) -> int:
    """Log the total footprint and the largest packages; return total bytes."""
    total = sum(package_sizes.values())
    top = sorted(package_sizes.items(), key=lambda kv: kv[1], reverse=True)[:_LARGEST_PACKAGES_TO_LOG]
    logger.info(
        "Installed footprint: %d package names, %d bytes (%.1f MB)",
        len(package_sizes),
        total,
        total / _BYTES_PER_MB,
    )
    for name, size in top:
        logger.info("  %-40s %10d bytes (%.1f MB)", name, size, size / _BYTES_PER_MB)
    return total


@pytest.mark.require_capability("runtime-package-management")
def test_installed_footprint_reported(installed_package_sizes: dict[str, int]) -> None:
    """Every installed package reports a non-negative size and the total is positive."""
    assert installed_package_sizes, "rpm returned no package size information"

    negative = {name: size for name, size in installed_package_sizes.items() if size < 0}
    assert not negative, f"packages with negative reported size: {sorted(negative)}"

    # Individual packages may legitimately report 0 (metapackages / no files,
    # e.g. azurelinux-release-wsl, glibc-minimal-langpack, dbus), so only
    # negatives are rejected above. The grand total, however, must be strictly
    # positive: a zero total means rpm returned no usable size data at all.
    total = _log_footprint(installed_package_sizes)
    assert total > 0, "total installed footprint is not positive (no rpm size data)"


@pytest.mark.require_capability("runtime-package-management")
def test_installed_footprint_under_threshold(
    installed_package_sizes: dict[str, int],
    image_name: str | None,
) -> None:
    """Total installed on-disk size must stay under the per-family cap."""
    assert image_name is not None, "--image-name is required to resolve the per-family footprint cap"
    total = _log_footprint(installed_package_sizes)
    cap = _installed_cap_bytes(image_name)
    assert total <= cap, (
        f"installed footprint {total / _BYTES_PER_MB:.1f} MB exceeds the "
        f"{cap / _BYTES_PER_MB:.0f} MB cap for image '{image_name}'"
    )


def test_image_tarball_under_threshold(
    image_path: Path | None,
    image_type: str,
    image_name: str | None,
) -> None:
    """The shipped rootfs artifact (tarball) must stay under the per-family cap.

    Applies only to families whose artifact is a compressed rootfs tarball
    (container, wsl); skips for VM images and for ``--image-ref`` sessions.
    """
    if image_type not in _TARBALL_IMAGE_TYPES:
        pytest.skip("tarball size cap only applies to rootfs-tarball images (container, wsl)")
    if image_path is None:
        pytest.skip("tarball size check requires --image-path (not --image-ref)")
    assert image_name is not None, "--image-name is required to resolve the per-family artifact cap"

    size_bytes = image_path.stat().st_size
    cap = _artifact_cap_bytes(image_name)
    logger.info(
        "Image artifact %s: %d bytes (%.1f MB)",
        image_path.name,
        size_bytes,
        size_bytes / _BYTES_PER_MB,
    )
    assert size_bytes > 0, f"image artifact is empty: {image_path}"
    assert size_bytes <= cap, (
        f"image artifact {size_bytes / _BYTES_PER_MB:.1f} MB exceeds the "
        f"{cap / _BYTES_PER_MB:.0f} MB cap for image '{image_name}'"
    )
