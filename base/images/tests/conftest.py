# SPDX-License-Identifier: MIT
"""Root conftest — fixtures for image validation.

CLI options (``--image-path``, ``--image-name``, ``--image-type``,
``--capabilities``, ``--workdir``) are registered in
:mod:`utils.pytest_plugin` (loaded early via entry point).
"""

from __future__ import annotations

import logging
import os
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
from utils.container_runtime import (
    ContainerExecInstance, 
    create_container_with_exec,
    destroy_exec_container,
)
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
        # behind by rootless umoci unpack are removable. buildah is
        # only preflight-validated for container sessions, so on a
        # VM-only host without buildah we must avoid an unhandled
        # FileNotFoundError during teardown (subprocess.run raises it
        # regardless of check=False) and fall through to shutil.rmtree.
        logger.debug("Removing temp work dir %s", p)
        cleanup_failed = True
        if shutil.which("buildah") is not None:
            rc = subprocess.run(
                ["buildah", "unshare", "rm", "-rf", str(p)],
                check=False,
                capture_output=True,
                text=True,
            )
            cleanup_failed = rc.returncode != 0
        if cleanup_failed:
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


# ---------------------------------------------------------------------------
# Dynamic Container Testing Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def running_container(
    image_path: Path, image_type: str, image_name: str | None, workdir: Path, request: pytest.FixtureRequest
) -> ContainerExecInstance | None:
    """Fresh container per test, with exec access and guaranteed teardown.

    A new container is started for every runtime test and destroyed on
    teardown so tests cannot leak state to one another (installed
    packages, created users, processes, files). The container name is
    auto-generated to avoid collisions when tests run in parallel.
    """
    if image_type != "container":
        pytest.skip("running_container only applicable to container images")

    # Only spin up a container for tests that actually need one.
    if not request.node.get_closest_marker("runtime_container_tests"):
        pytest.skip("running_container only for runtime container tests")

    logger.info("Creating fresh container for test %s", request.node.name)
    container = create_container_with_exec(
        image_path,
        workdir,
        container_name=None,  # auto-generate a unique name per test
        image_name=image_name,
    )

    try:
        yield container
    finally:
        logger.info("Destroying container for test %s", request.node.name)
        destroy_exec_container(container)


@pytest.fixture
def container_exec(running_container: ContainerExecInstance):
    """Execute a shell command in the running container via ``podman exec``.

    Returns a callable ``(command: str, timeout: int = 60) ->
    subprocess.CompletedProcess[str]``. The framework does **not** install
    packages or mutate the container in any way — tests see the image as
    shipped. If a test needs a binary that the image does not ship, it
    must declare the dependency itself (and either skip or fail loudly).
    """
    from utils.container_runtime import exec_container_command_raw

    def _exec(command: str, timeout: int = 60) -> subprocess.CompletedProcess[str]:
        return exec_container_command_raw(
            running_container.container_name,
            ["bash", "-c", command],
            timeout=timeout,
        )
    return _exec


@pytest.fixture(autouse=True)
def _apply_requires_pkg(request: pytest.FixtureRequest) -> None:
    """Honor ``@pytest.mark.requires_pkg(...)`` on runtime tests.

    Collects all packages declared by ``requires_pkg`` markers on the
    test (multiple markers stack), installs them once via ``dnf`` in
    the live container, and skips the test on installation failure.

    No-op for tests that don't carry the marker or don't request
    ``container_exec`` (e.g. static rootfs tests).
    """
    markers = list(request.node.iter_markers("requires_pkg"))
    if not markers:
        return
    if "container_exec" not in request.fixturenames:
        pytest.skip("requires_pkg marker is only valid for runtime container tests")

    pkgs: list[str] = []
    for m in markers:
        pkgs.extend(m.args)
    if not pkgs:
        return

    container_exec = request.getfixturevalue("container_exec")
    cmd = "dnf install -y " + " ".join(pkgs)
    logger.info("requires_pkg: installing %s", pkgs)
    result = container_exec(cmd, timeout=300)
    if result.returncode != 0:
        pytest.skip(
            f"requires_pkg: failed to install {pkgs} (rc={result.returncode}): "
            f"{result.stderr.strip()[:200]}"
        )


@pytest.fixture
def container_info(running_container: ContainerExecInstance) -> dict[str, str]:
    """Container runtime metadata (id, name, image, IP)."""
    try:
        from utils.container_runtime import exec_container_command_raw
        ip_result = exec_container_command_raw(
            running_container.container_name,
            ["hostname", "-i"],
            timeout=5
        )
        container_ip = ip_result.stdout.strip() if ip_result.returncode == 0 else "127.0.0.1"
    except Exception:
        container_ip = "127.0.0.1"

    return {
        "container_id": running_container.container_id,
        "container_name": running_container.container_name,
        "image_ref": running_container.image_ref,
        "ip_address": container_ip,
    }


