# SPDX-License-Identifier: MIT
"""Disk-footprint checks shared across images.

Sum the installed on-disk size from the RPM ``%{SIZE}`` headers and guard
against gross size regressions using per-family installed-size caps.
Tarball sizes must fall within the exact image and architecture's KiB bounds.

The installed-size tests need an rpmdb, so they gate on the
``runtime-package-management`` capability. The tarball-size test applies
only to families whose artifact is a compressed rootfs tarball (container,
wsl); it skips for VM images, which ship a provisioned raw disk.
"""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from collections.abc import Iterable

logger = logging.getLogger(__name__)

_BYTES_PER_KIB = 1024
_BYTES_PER_MB = 1024 * 1024

# Max total installed size (MB) per family; unlisted families fall back to
# the default. Caps catch gross regressions, not normal growth.
_INSTALLED_CAP_MB: dict[str, int] = {
    "container-base": 400,
    "1p-vm-base-gen2": 2048,
    "wsl": 800,
}
_INSTALLED_CAP_DEFAULT_MB = 2048

_TARBALL_IMAGE_TYPES = frozenset({"container", "wsl"})
_ARCHITECTURES = frozenset({"x86_64", "aarch64"})

_LARGEST_PACKAGES_TO_LOG = 15


def _family_of(image_name: str, known: Iterable[str]) -> str | None:
    """Map an ``--image-name`` to its family, including optional suffixed variants."""
    for family in known:
        if image_name == family or image_name.startswith(family + "-"):
            return family
    return None


def _installed_cap_bytes(image_name: str) -> int:
    family = _family_of(image_name, _INSTALLED_CAP_MB)
    cap_mb = _INSTALLED_CAP_MB.get(family, _INSTALLED_CAP_DEFAULT_MB) if family else _INSTALLED_CAP_DEFAULT_MB
    return cap_mb * _BYTES_PER_MB


def _parse_artifact_range(entry: object, context: str) -> tuple[int, int]:
    """Validate KiB bounds and convert them to bytes for artifact comparisons."""
    required = {"min_kib", "max_kib"}
    if not isinstance(entry, dict) or entry.keys() != required:
        raise ValueError(f"{context}: specify min_kib and max_kib only")
    minimum, maximum = entry["min_kib"], entry["max_kib"]
    if type(minimum) is not int or type(maximum) is not int:
        raise ValueError(f"{context}: limits must be integer KiB counts")
    if minimum < 0 or maximum <= 0 or minimum > maximum:
        raise ValueError(f"{context}: requires 0 <= min_kib <= max_kib and max_kib > 0")
    return minimum * _BYTES_PER_KIB, maximum * _BYTES_PER_KIB


def validate_artifact_limits(config: object) -> dict[str, dict[str, tuple[int, int]]]:
    """Validate per-image, per-architecture KiB bounds and return byte ranges."""
    if not isinstance(config, dict):
        raise TypeError("expected an image bounds dictionary")

    limits: dict[str, dict[str, tuple[int, int]]] = {}
    for name, architectures in config.items():
        if not isinstance(name, str):
            raise TypeError("image names must be strings")
        if not isinstance(architectures, dict):
            raise TypeError(f"image '{name}' must contain architecture mappings")
        limits[name] = {}
        for arch, entry in architectures.items():
            context = f"image '{name}' architecture '{arch}'"
            if arch not in _ARCHITECTURES:
                raise ValueError(f"{context}: unsupported architecture")
            limits[name][arch] = _parse_artifact_range(entry, context)
    return limits


def artifact_architecture(image_path: Path, configured: str | None) -> str:
    """Resolve the target architecture from an explicit option or artifact filename."""
    detected = set(re.split(r"[.-]", image_path.name.lower())) & _ARCHITECTURES
    if len(detected) > 1:
        pytest.fail(f"Conflicting architectures in artifact filename: {image_path.name}")
    if configured is not None:
        if configured not in _ARCHITECTURES:
            pytest.fail(f"Unsupported --image-arch: {configured}")
        if detected and configured not in detected:
            pytest.fail(f"--image-arch '{configured}' disagrees with artifact filename: {image_path.name}")
        return configured
    if detected:
        return detected.pop()
    pytest.fail(f"Cannot determine target architecture from '{image_path.name}'; pass --image-arch")


def _tarball_artifact(image_path: Path | None, image_type: str) -> Path:
    if image_type not in _TARBALL_IMAGE_TYPES:
        pytest.skip("tarball size cap only applies to rootfs-tarball images (container, wsl)")
    if image_path is None:
        pytest.skip("tarball size check requires --image-path (not --image-ref)")
    return image_path


@pytest.fixture(scope="session")
def artifact_size_limits(
    image_path: Path | None,
    image_type: str,
) -> dict[str, dict[str, tuple[int, int]]]:
    """Load the checked-in JSON file once, only for applicable tarball checks."""
    _tarball_artifact(image_path, image_type)
    path = Path(__file__).resolve().parents[2] / "image-size-bounds.json"
    try:
        with path.open(encoding="utf-8") as stream:
            return validate_artifact_limits(json.load(stream))
    except (OSError, ValueError, TypeError) as exc:
        pytest.fail(f"Cannot load tarball footprint limits: {exc}")


@pytest.fixture(scope="session")
def image_arch(request: pytest.FixtureRequest) -> str | None:
    """Optional target architecture override, never inferred from the test host."""
    return request.config.getoption("--image-arch")


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


def test_image_tarball_within_limits(
    image_path: Path | None,
    image_type: str,
    image_name: str | None,
    artifact_size_limits: dict[str, dict[str, tuple[int, int]]],
    image_arch: str | None,
) -> None:
    """The shipped rootfs artifact must fall within its exact image's range.

    Applies only to images whose artifact is a compressed rootfs tarball
    (container, wsl); skips for VM images and for ``--image-ref`` sessions.

    This test surfaces image composition and package content churn. Policy based
    size limit, typically an upper bound, is not the target.
    """
    image_path = _tarball_artifact(image_path, image_type)
    assert image_name is not None, "--image-name is required to resolve the artifact size limits"
    if image_name not in artifact_size_limits:
        pytest.skip(f"No tarball footprint limits configured for image '{image_name}' (exact name required)")
    arch = artifact_architecture(image_path, image_arch)
    if arch not in artifact_size_limits[image_name]:
        pytest.skip(f"No tarball footprint limits configured for image '{image_name}' architecture '{arch}'")
    minimum, maximum = artifact_size_limits[image_name][arch]

    size_bytes = image_path.stat().st_size
    logger.info(
        "Image artifact %s (%s): %d bytes (%.1f MiB)",
        image_path.name,
        arch,
        size_bytes,
        size_bytes / _BYTES_PER_MB,
    )
    assert size_bytes > 0, f"image artifact is empty: {image_path}"
    assert minimum <= size_bytes <= maximum, (
        f"image artifact {size_bytes} bytes ({size_bytes / _BYTES_PER_MB:.1f} MiB) is outside the "
        f"configured range [{minimum}, {maximum}] bytes for image '{image_name}' architecture '{arch}'"
    )
