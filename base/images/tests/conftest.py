# SPDX-License-Identifier: MIT
"""Root conftest — fixtures for image validation.

CLI options (``--image-path``, ``--image-ref``, ``--image-name``,
``--image-type``, ``--capabilities``, ``--workdir``) are registered
in :mod:`utils.pytest_plugin` (loaded early via entry point).
"""

from __future__ import annotations

import logging
import shlex
import shutil
import subprocess
import tempfile
import time
import uuid
from collections.abc import Iterator
from pathlib import Path

import pytest
from python_on_whales import DockerClient
from utils.container_runtime import (
    AssertHttpServer,
    ContainerExecResult,
    ContainerInstance,
    ExecShell,
    WaitForHttp,
    WriteFile,
    build_image,
    cleanup_test_images,
    create_container,
    destroy_container,
    exec_in_container,
    get_podman_client,
    resolve_image_reference,
)
from utils.disk import inspect_disk
from utils.extract import (
    inspect_oci_config,
    mount_container_image,
    mount_vm_image,
    mount_wsl_image,
    read_text_confined,
    unmount_container_image,
    unmount_vm_image,
    unmount_wsl_image,
)
from utils.parsers import parse_os_release, query_rpm_package_sizes
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
def image_path(request: pytest.FixtureRequest) -> Path | None:
    """Path to image artifact from ``--image-path``, or None if ``--image-ref`` is used."""
    raw = request.config.getoption("--image-path")
    if not raw:
        return None
    p = Path(raw).resolve()
    logger.info("Image path: %s", p)
    if not p.exists():
        pytest.fail(f"Image file does not exist: {p}")
    logger.debug("Image file size: %d bytes", p.stat().st_size)
    return p


@pytest.fixture(scope="session")
def image_ref(request: pytest.FixtureRequest) -> str | None:
    """Image reference from ``--image-ref``, or None if ``--image-path`` is used."""
    ref = request.config.getoption("--image-ref")
    if ref:
        logger.info("Image ref: %s", ref)
    return ref


@pytest.fixture(scope="session")
def image_type(
    request: pytest.FixtureRequest,
    capabilities: set[str],
    image_path: Path | None, image_ref: str | None,
) -> str:
    """``'vm'``, ``'container'``, or ``'wsl'`` — from ``--image-type``, capabilities, or file extension."""
    explicit = request.config.getoption("--image-type")
    if explicit:
        logger.info("Image type (explicit): %s", explicit)
        return explicit

    from_caps = derive_image_type_from_capabilities(capabilities)
    if from_caps:
        logger.info("Image type (from capabilities): %s", from_caps)
        return from_caps

    # --image-ref implies container.
    if image_ref:
        logger.info("Image type (from --image-ref): container")
        return "container"

    if image_path:
        detected = detect_image_type(str(image_path))
        if detected is not None:
            logger.info("Image type (auto-detected from extension): %s", detected)
            return detected

    pytest.fail(
        "Cannot detect image type. "
        "Pass --image-type or --capabilities explicitly."
    )


@pytest.fixture(scope="session")
def workdir(request: pytest.FixtureRequest) -> Iterator[Path]:
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
def rootfs(image_path: Path | None, image_type: str, workdir: Path) -> Iterator[Path]:
    """Mounted rootfs — session yield-fixture with cleanup.

    Requires ``--image-path`` (not ``--image-ref``); skips otherwise.
    """
    if image_path is None:
        pytest.skip("rootfs requires --image-path (not available with --image-ref)")

    if image_type == "vm":
        mountpoint = workdir / "vm-rootfs"
        mountpoint.mkdir(parents=True, exist_ok=True)
        logger.info("Mounting VM image at %s", mountpoint)
        mount_vm_image(image_path, mountpoint)
        yield mountpoint
        logger.info("Unmounting VM image at %s", mountpoint)
        unmount_vm_image(mountpoint)
    elif image_type == "wsl":
        wsl_dir = workdir / "wsl"
        logger.info("Extracting WSL image to %s", wsl_dir)
        rootfs_path = mount_wsl_image(image_path, wsl_dir)
        logger.info("WSL rootfs ready at %s", rootfs_path)
        yield rootfs_path
        logger.info("Cleaning up WSL extract at %s", wsl_dir)
        unmount_wsl_image(wsl_dir)
    else:
        container_dir = workdir / "container"
        logger.info("Extracting container image to %s", container_dir)
        rootfs_path = mount_container_image(image_path, container_dir)
        logger.info("Container rootfs ready at %s", rootfs_path)
        yield rootfs_path
        logger.info("Cleaning up container extract at %s", container_dir)
        unmount_container_image(container_dir)


@pytest.fixture(scope="session")
def oci_image_config(image_path: Path | None) -> dict[str, object]:
    """Return the parsed OCI image config.

    Only meaningful for container images; tests using this fixture gate on
    the ``container`` capability via
    ``@pytest.mark.require_capability("container")``.
    """
    if image_path is None:
        pytest.skip("oci_image_config requires --image-path")
    config = inspect_oci_config(image_path)
    logger.info("OCI image config.config keys: %s", sorted(config.get("config", {})))
    return config


@pytest.fixture(scope="session")
def disk_info(image_path: Path | None, image_type: str) -> DiskInfo | None:
    """Partition/filesystem info — ``None`` for container images."""
    if image_type != "vm":
        logger.debug("Skipping disk inspection (not a VM image)")
        return None
    if image_path is None:
        pytest.skip("disk_info requires --image-path")
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
    # Read via a chroot-confined resolver: /etc/os-release is commonly a
    # symlink, and the extracted tree is inspected through host paths, so a
    # crafted absolute link must not let this read escape the rootfs.
    result = parse_os_release(read_text_confined(rootfs, "etc/os-release"))
    logger.info("os-release: ID=%s VERSION_ID=%s", result.get("ID"), result.get("VERSION_ID"))
    logger.debug("os-release full: %s", result)
    return result


@pytest.fixture(scope="session")
def installed_package_sizes(rootfs: Path) -> dict[str, int]:
    """Mapping of installed RPM package name to on-disk size in bytes.

    Single source of truth for installed-package data; the
    :func:`installed_packages` fixture derives its name set from this.
    """
    logger.info("Querying installed RPM package sizes via rpm --root")
    sizes = query_rpm_package_sizes(rootfs)
    logger.info("Found size info for %d packages", len(sizes))
    logger.debug("Packages: %s", sorted(sizes))
    return sizes


@pytest.fixture(scope="session")
def installed_packages(installed_package_sizes: dict[str, int]) -> set[str]:
    """Set of installed RPM package names (derived from package sizes)."""
    return set(installed_package_sizes)


@pytest.fixture(scope="session")
def partition_table(disk_info: DiskInfo | None, image_type: str) -> list[PartitionInfo]:
    """Partition metadata — auto-skips for container images."""
    if image_type != "vm":
        pytest.skip("partition_table not applicable to container images")
    assert disk_info is not None
    logger.info("Partition table: %d partitions", len(disk_info.partitions))
    for p in disk_info.partitions:
        logger.debug(
            "  %s: type=%s mount=%s size=%d",
            p.device,
            p.type,
            p.mountpoint,
            p.size_bytes,
        )
    return disk_info.partitions


# ---------------------------------------------------------------------------
# Container runtime fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def podman_client(image_type: str):
    """Session-scoped python-on-whales Podman client; skips for non-container images."""
    if image_type != "container":
        yield None
        return

    client = get_podman_client()
    try:
        yield client
    finally:
        cleanup_test_images(client)


@pytest.fixture(scope="session")
def container_image_ref(
    podman_client: DockerClient, image_path: Path | None, image_ref: str | None,
    image_type: str,
) -> str | None:
    """Resolve the container image once per session and cache the reference.

    - If ``--image-ref`` was given, returns it directly.
    - If ``--image-path`` was given, loads the archive via ``podman load``
      and returns the resulting image ID.
    - Returns ``None`` for non-container sessions.
    """
    if image_type != "container":
        return None

    return resolve_image_reference(podman_client, image_path=image_path, image_ref=image_ref)


def _effective_image(podman_client: DockerClient, container_image_ref: str, request: pytest.FixtureRequest) -> str:
    """Build the per-test image from ``@pytest.mark.dockerfile()`` if present, else use the base image."""
    marker = request.node.get_closest_marker("dockerfile")
    if marker is None:
        return container_image_ref
    test_dir = request.path.parent
    dockerfile_path = (test_dir / (marker.args[0] if marker.args else "Dockerfile")).resolve()
    if not dockerfile_path.exists():
        pytest.fail(
            f"Dockerfile not found: {dockerfile_path} "
            f"(from @pytest.mark.dockerfile on {request.node.name})"
        )
    return build_image(podman_client, dockerfile_path, container_image_ref)


@pytest.fixture
def running_container(
    podman_client: DockerClient, image_type: str,
    container_image_ref: str | None, request: pytest.FixtureRequest,
):
    """Fresh container per test with guaranteed teardown.

    If marked with ``@pytest.mark.dockerfile()``, builds a custom
    image from the specified Dockerfile first. Skips for non-container
    images.
    """
    if image_type != "container":
        pytest.skip("running_container only applicable to container images")
    if container_image_ref is None:
        pytest.fail("container_image_ref was not resolved for a container image")

    effective_image = _effective_image(podman_client, container_image_ref, request)

    logger.info("Creating container for test %s", request.node.name)
    instance = create_container(podman_client, effective_image)

    try:
        yield instance
    finally:
        logger.info("Destroying container for test %s", request.node.name)
        destroy_container(podman_client, instance.container_name)


@pytest.fixture
def container_exec(podman_client: DockerClient, running_container: ContainerInstance):
    """Callable to execute commands in the running test container.

    Usage::

        def test_example(container_exec):
            result = container_exec(["echo", "hello"])
            assert result.exit_code == 0
            assert "hello" in result.output
    """
    def _exec(command: list[str]):
        return exec_in_container(
            podman_client,
            running_container.container_name,
            command,
        )
    return _exec


@pytest.fixture
def container_exec_shell(podman_client: DockerClient, running_container: ContainerInstance) -> ExecShell:
    """Callable to execute shell commands in the running test container.

    Usage::

        def test_example(container_exec_shell):
            result = container_exec_shell("echo hello")
            assert result.exit_code == 0
            assert "hello" in result.output
    """
    def _exec_shell(command: str, *, shell: str = "bash"):
        return exec_in_container(
            podman_client,
            running_container.container_name,
            [shell, "-c", command],
        )
    return _exec_shell


@pytest.fixture
def write_file_in_container(container_exec_shell: ExecShell) -> WriteFile:
    """Callable to write file content into the running test container.

    Preserves leading whitespace and content exactly as provided, while
    normalizing trailing newlines so the written file ends with exactly
    one trailing newline.

    Usage::

        def test_example(write_file_in_container):
            result = write_file_in_container("/tmp/example.conf", "key=value")
            assert result.exit_code == 0
    """

    def _write(path: str, content: str):
        normalized_content = content.rstrip("\n") + "\n"
        write_cmd = (
            f"printf %s {shlex.quote(normalized_content)} > "
            f"{shlex.quote(path)}"
        )
        return container_exec_shell(write_cmd)

    return _write


@pytest.fixture
def client_server_exec_shell(
    podman_client: DockerClient, image_type: str,
    container_image_ref: str | None, request: pytest.FixtureRequest,
) -> Iterator[tuple[ExecShell, ExecShell, str]]:
    """Two networked containers, each with a callable to execute shell commands.

    Usage::

        def test_example(client_server_exec_shell):
            server_exec, client_exec, server_host = client_server_exec_shell
            server_exec("some-daemon &")
            result = client_exec(f"curl http://{server_host}:8080")
            assert result.exit_code == 0
    """
    if image_type != "container":
        pytest.skip("client_server_exec_shell only applicable to container images")
    if container_image_ref is None:
        pytest.fail("container_image_ref was not resolved for a container image")

    effective_image = _effective_image(podman_client, container_image_ref, request)

    network_name = f"azl-test-net-{uuid.uuid4().hex[:12]}"
    podman_client.network.create(network_name)

    def _exec_shell_for(container: ContainerInstance) -> ExecShell:
        def _exec_shell(command: str, *, shell: str = "bash") -> ContainerExecResult:
            return exec_in_container(podman_client, container.container_name, [shell, "-c", command])
        return _exec_shell

    suffix = uuid.uuid4().hex[:12]
    logger.info("Creating server and client containers for test %s", request.node.name)
    server = client = None
    try:
        server = create_container(
            podman_client, effective_image, f"azl-test-server-{suffix}", networks=[network_name],
        )
        client = create_container(
            podman_client, effective_image, f"azl-test-client-{suffix}", networks=[network_name],
        )
        yield _exec_shell_for(server), _exec_shell_for(client), server.container_name
    finally:
        try:
            for container in (server, client):
                if container is not None:
                    destroy_container(podman_client, container.container_name)
        finally:
            podman_client.network.remove(network_name)


@pytest.fixture
def wait_for_http(container_exec_shell: ExecShell) -> WaitForHttp:
    """Callable that polls an in-container HTTP endpoint until it responds.

    Runs ``curl -sSf <url>`` inside the running test container, retrying
    until the request succeeds. Bounded connect/read timeouts keep a
    hung server from stalling the suite, and the call fails explicitly
    (raising ``AssertionError``) once the retries are exhausted rather
    than returning a failed result a caller might forget to check.

    Usage::

        def test_example(container_exec_shell, wait_for_http):
            container_exec_shell("nginx")
            result = wait_for_http("http://localhost:80/health")
            assert "healthy" in result.output
    """
    def _wait(
        url: str,
        *,
        retries: int = 5,
        delay: float = 1.0,
        connect_timeout: float = 2.0,
        max_time: float = 5.0,
    ):
        result = None
        for _ in range(retries):
            result = container_exec_shell(
                f"curl -sSf --connect-timeout {connect_timeout} "
                f"--max-time {max_time} {shlex.quote(url)}"
            )
            if result.exit_code == 0:
                return result
            time.sleep(delay)

        output = result.output if result is not None else "<no attempts>"
        raise AssertionError(
            f"HTTP endpoint {url} did not respond after {retries} attempt(s): "
            f"{output}"
        )
    return _wait


@pytest.fixture
def assert_http_server(container_exec_shell: ExecShell, wait_for_http: WaitForHttp) -> AssertHttpServer:
    """Start an HTTP server in the container and assert its response.

    Runs ``start_command`` inside the running test container, waits for
    ``url`` to respond, and asserts ``expected`` appears in the response
    body. Returns the successful result for further assertions.

    Usage::

        def test_example(assert_http_server):
            assert_http_server(
                "nohup python3 /app/app.py > /tmp/server.log 2>&1 &",
                "http://localhost:8080/",
                "Hello from the server",
            )
    """
    def _assert(
        start_command: str,
        url: str,
        expected: str,
        *,
        retries: int = 5,
        delay: float = 1.0,
    ):
        start = container_exec_shell(start_command)
        assert start.exit_code == 0, f"failed to start server: {start.output}"

        result = wait_for_http(url, retries=retries, delay=delay)
        assert expected in result.output, (
            f"unexpected response body: {result.output!r}"
        )
        return result
    return _assert
