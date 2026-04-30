# SPDX-License-Identifier: MIT
"""Root conftest — fixtures for image validation.

CLI options (``--image-path``, ``--image-name``, ``--image-type``,
``--capabilities``, ``--workdir``) are registered in
:mod:`utils.pytest_plugin` (loaded early via entry point).
"""

from __future__ import annotations

import logging
import shutil
import subprocess
import tempfile
from pathlib import Path

import pytest

from utils.disk import inspect_disk
from utils.extract import (
    mount_container_image,
    mount_vm_image,
    unmount_container_image,
    unmount_vm_image,
)
from utils.parsers import parse_os_release, query_rpm_packages
from utils.pytest_plugin import (
    derive_image_type_from_capabilities,
    detect_image_type,
    parse_capabilities,
)
from utils.types import DiskInfo, PartitionInfo

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Core fixtures (session-scoped)
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def image_name(request: pytest.FixtureRequest) -> str | None:
    """Image name from ``--image-name`` (or ``None`` if not provided)."""
    name = request.config.getoption("--image-name")
    if name:
        logger.info("Image name: %s", name)
    return name


@pytest.fixture(scope="session")
def capabilities(request: pytest.FixtureRequest) -> set[str]:
    """Image capabilities from ``--capabilities``."""
    caps = parse_capabilities(request.config.getoption("--capabilities"))
    logger.info("Capabilities: %s", sorted(caps) if caps else "(none)")
    return caps


@pytest.fixture(scope="session")
def image_path(request: pytest.FixtureRequest) -> Path:
    p = Path(request.config.getoption("--image-path")).resolve()
    logger.info("Image path: %s", p)
    if not p.exists():
        pytest.fail(f"Image file does not exist: {p}")
    logger.debug("Image file size: %d bytes", p.stat().st_size)
    return p


@pytest.fixture(scope="session")
def image_type(
    request: pytest.FixtureRequest, capabilities: set[str], image_path: Path,
) -> str:
    """``'vm'`` or ``'container'`` — from ``--image-type``, capabilities, or file extension."""
    explicit = request.config.getoption("--image-type")
    if explicit:
        logger.info("Image type (explicit): %s", explicit)
        return explicit

    from_caps = derive_image_type_from_capabilities(capabilities)
    if from_caps:
        logger.info("Image type (from capabilities): %s", from_caps)
        return from_caps

    detected = detect_image_type(str(image_path))
    if detected is None:
        pytest.fail(
            f"Cannot detect image type from extension of {image_path.name}. "
            "Pass --image-type or --capabilities explicitly."
        )
    logger.info("Image type (auto-detected from extension): %s", detected)
    return detected


@pytest.fixture(scope="session")
def workdir(request: pytest.FixtureRequest) -> Path:
    """Working directory for mounts and extractions.

    If ``--workdir`` is set, the directory is reused as-is and never
    removed (useful for post-mortem debugging). Otherwise a fresh
    temp directory is created and cleaned up at session teardown.
    """
    explicit = request.config.getoption("--workdir")
    if explicit:
        p = Path(explicit).resolve()
        p.mkdir(parents=True, exist_ok=True)
        logger.debug("Work dir (explicit, will not be removed): %s", p)
        yield p
        return

    p = Path(tempfile.mkdtemp(prefix="azl-image-tests-"))
    logger.debug("Work dir (temp, will be removed at session end): %s", p)
    try:
        yield p
    finally:
        # Use buildah unshare for cleanup so any read-only dirs left
        # behind by rootless umoci unpack are removable.
        logger.debug("Removing temp work dir %s", p)
        rc = subprocess.run(
            ["buildah", "unshare", "rm", "-rf", str(p)],
            check=False,
            capture_output=True,
            text=True,
        )
        if rc.returncode != 0:
            # Fall back to plain rm; if that also fails, log and move on
            # rather than failing the test session at teardown.
            try:
                shutil.rmtree(p, ignore_errors=True)
            except Exception as exc:  # pragma: no cover
                logger.warning("Failed to remove work dir %s: %s", p, exc)


@pytest.fixture(scope="session")
def rootfs(image_path: Path, image_type: str, workdir: Path) -> Path:
    """Mounted rootfs — session yield-fixture with cleanup."""
    if image_type == "vm":
        mountpoint = workdir / "vm-rootfs"
        mountpoint.mkdir(parents=True, exist_ok=True)
        logger.info("Mounting VM image at %s", mountpoint)
        mount_vm_image(image_path, mountpoint)
        yield mountpoint
        logger.info("Unmounting VM image at %s", mountpoint)
        unmount_vm_image(mountpoint)
    else:
        container_dir = workdir / "container"
        logger.info("Extracting container image to %s", container_dir)
        rootfs_path = mount_container_image(image_path, container_dir)
        logger.info("Container rootfs ready at %s", rootfs_path)
        yield rootfs_path
        logger.info("Cleaning up container extract at %s", container_dir)
        unmount_container_image(container_dir)


@pytest.fixture(scope="session")
def disk_info(image_path: Path, image_type: str) -> DiskInfo | None:
    """Partition/filesystem info — ``None`` for container images."""
    if image_type != "vm":
        logger.debug("Skipping disk inspection (not a VM image)")
        return None
    logger.info("Inspecting disk: %s", image_path)
    return inspect_disk(image_path)


# ---------------------------------------------------------------------------
# Rich parsed fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def os_release(rootfs: Path) -> dict[str, str]:
    """Parsed ``/etc/os-release``."""
    os_release_path = rootfs / "etc" / "os-release"
    logger.debug("Looking for os-release at %s", os_release_path)
    if not os_release_path.exists():
        pytest.fail("/etc/os-release not found in image")
    result = parse_os_release(os_release_path.read_text())
    logger.info("os-release: ID=%s VERSION_ID=%s", result.get("ID"), result.get("VERSION_ID"))
    logger.debug("os-release full: %s", result)
    return result


@pytest.fixture(scope="session")
def installed_packages(rootfs: Path) -> set[str]:
    """Set of installed RPM package names."""
    logger.info("Querying installed RPM packages via rpm --root")
    pkgs = query_rpm_packages(rootfs)
    logger.info("Found %d installed packages", len(pkgs))
    logger.debug("Packages: %s", sorted(pkgs))
    return pkgs


@pytest.fixture(scope="session")
def partition_table(
    disk_info: DiskInfo | None, image_type: str
) -> list[PartitionInfo]:
    """Partition metadata — auto-skips for container images."""
    if image_type != "vm":
        pytest.skip("partition_table not applicable to container images")
    assert disk_info is not None
    logger.info("Partition table: %d partitions", len(disk_info.partitions))
    for p in disk_info.partitions:
        logger.debug("  %s: type=%s mount=%s size=%d", p.device, p.type, p.mountpoint, p.size_bytes)
    return disk_info.partitions
