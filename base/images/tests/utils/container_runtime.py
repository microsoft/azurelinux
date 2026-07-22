# SPDX-License-Identifier: MIT
"""Container runtime orchestration using python-on-whales.

Provides utilities for creating running containers with exec access
for runtime integration testing. Uses python-on-whales to drive the
Podman CLI directly.
"""

from __future__ import annotations

import logging
import time
import uuid
from collections.abc import Callable
from pathlib import Path
from typing import Iterator, NamedTuple, cast

from python_on_whales import DockerClient
from python_on_whales.exceptions import DockerException, NoSuchContainer, NoSuchImage

from .tools import NativeTool


logger = logging.getLogger(__name__)

# Register podman as a required native tool for container testing.
PODMAN = NativeTool(
    name="podman",
    package_hint="podman",
    reason="container runtime for live container tests",
    when="container",
)

_loaded_image_refs: set[str] = set()
_built_image_cache: dict[tuple[Path, str], str] = {}


class ContainerExecResult(NamedTuple):
    """Result of executing a command inside a container.

    *stdout* and *stderr* hold the per-stream output. *output* is the
    two streams concatenated, kept for convenience.
    """
    exit_code: int
    stdout: str
    stderr: str
    output: str


class ContainerInstance(NamedTuple):
    """A running container managed by the test framework."""
    container_id: str
    container_name: str
    image_ref: str


class ContainerRuntimeError(Exception):
    """Container runtime operation failed."""


def get_podman_client() -> DockerClient:
    """Create a python-on-whales client configured for the Podman CLI."""
    client = DockerClient(client_call=["podman"], client_type="podman")
    try:
        client.version()
    except DockerException as exc:
        raise ContainerRuntimeError(
            f"Cannot run podman through python-on-whales: {exc}"
        ) from exc
    return client


def resolve_image_reference(
    client: DockerClient,
    *,
    image_path: Path | None = None,
    image_ref: str | None = None,
) -> str:
    """Resolve to a Podman-usable image reference.

    Exactly one of *image_path* or *image_ref* must be provided.

    - **image_path**: a local archive file (``.tar``, ``.tar.xz``, etc.)
      is loaded via ``podman load`` and the resulting image ID is returned.
    - **image_ref**: an image reference (e.g. ``mcr.microsoft.com/azurelinux/base/core:4.0``
      or ``localhost/container-base:latest``). Pulled from the registry
      if not already present locally.

    Returns:
        Image ID (for archives) or the image reference string.
    """
    if image_path and image_ref:
        raise ContainerRuntimeError(
            "image_path and image_ref are mutually exclusive"
        )
    if not image_path and not image_ref:
        raise ContainerRuntimeError(
            "Either image_path or image_ref must be provided"
        )

    if image_ref:
        # Ensure the image is available locally; pull if needed.
        if client.image.exists(image_ref):
            logger.info("Image already present locally: %s", image_ref)
        else:
            logger.info("Pulling image: %s", image_ref)
            client.image.pull(image_ref)
        return image_ref

    # Load from archive file.
    assert image_path is not None
    logger.info("Loading image archive: %s", image_path)
    image_refs = client.image.load(image_path)

    if not image_refs:
        raise ContainerRuntimeError(
            f"podman load returned no images for {image_path}"
        )

    image_ref = image_refs[0]
    if image_ref is None:
        raise ContainerRuntimeError(
            f"podman load returned an empty image reference for {image_path}"
        )
    image_ref = str(image_ref)
    logger.info("Loaded image: %s", image_ref)
    _loaded_image_refs.add(image_ref)
    return image_ref


def _build_cache_key(dockerfile_path: Path, base_image_ref: str) -> tuple[Path, str]:
    return (dockerfile_path.resolve(), base_image_ref)


def build_image(
    client: DockerClient,
    dockerfile_path: Path,
    base_image_ref: str,
) -> str:
    """Build a container image from a Dockerfile.

    Injects the image-under-test as the ``BASE_IMAGE`` build arg.
    Results are cached per session by Dockerfile path and base image.
    """
    cache_key = _build_cache_key(dockerfile_path, base_image_ref)
    if cache_key in _built_image_cache:
        cached = _built_image_cache[cache_key]
        logger.info("Using cached build for %s: %s", dockerfile_path.name, cached)
        return cached

    context_dir = dockerfile_path.parent
    image_tag = f"localhost/azl-test-{uuid.uuid4().hex[:12]}:latest"
    logger.info(
        "Building image from %s (base: %s, context: %s)",
        dockerfile_path, base_image_ref, context_dir,
    )

    client.legacy_build(
        context_path=context_dir,
        file=dockerfile_path,
        build_args={"BASE_IMAGE": base_image_ref},
        tags=image_tag,
        quiet=True,
    )

    logger.info("Built image: %s", image_tag)
    _built_image_cache[cache_key] = image_tag
    return image_tag


def cleanup_test_images(client: DockerClient) -> None:
    """Remove test-created images (best-effort, never raises)."""
    image_ref_groups = (
        ("built", sorted(set(_built_image_cache.values()))),
        ("loaded", sorted(_loaded_image_refs)),
    )
    _built_image_cache.clear()
    _loaded_image_refs.clear()

    for image_source, image_refs in image_ref_groups:
        for image_ref in image_refs:
            logger.info("Removing %s test image %s", image_source, image_ref)
            try:
                client.image.remove(image_ref, force=True)
            except (NoSuchImage, DockerException) as exc:
                logger.debug("Image remove skipped (%s): %s", image_ref, exc)


def create_container(
    client: DockerClient,
    image_ref: str,
    container_name: str | None = None,
    *,
    networks: list[str] | None = None,
) -> ContainerInstance:
    """Create and start a container with exec access.

    The container runs ``sleep infinity`` to stay alive for the duration
    of the test, allowing repeated ``exec`` calls.

    Args:
        client: Active python-on-whales Podman client.
        image_ref: Image ID or reference to run.
        container_name: Optional name; auto-generated if None.
        networks: Optional networks to attach the container to.

    Returns:
        A ContainerInstance with the container's ID, name, and image ref.
    """
    if container_name is None:
        container_name = f"azl-test-{uuid.uuid4().hex[:12]}"

    logger.info("Creating container %s from image %s", container_name, image_ref)

    container = client.container.run(
        image_ref,
        command=["sleep", "infinity"],
        name=container_name,
        detach=True,
        networks=networks or [],
    )

    # Verify the container is running and exec works.
    try:
        container.reload()
        if container.state.status != "running":
            raise ContainerRuntimeError(
                f"Container {container_name} is not running "
                f"(status: {container.state.status})"
            )

        result = exec_in_container(client, container_name, ["echo", "ready"])
        if result.exit_code != 0:
            raise ContainerRuntimeError(
                f"Container exec readiness check failed for {container_name} "
                f"(exit_code={result.exit_code}, output={result.output!r})"
            )
    except BaseException:
        # Clean up on any failure (including KeyboardInterrupt).
        logger.warning("Readiness check failed; removing container %s", container_name)
        try:
            container.remove(force=True)
        except Exception as cleanup_exc:
            logger.warning("Failed to clean up container %s: %s", container_name, cleanup_exc)
        raise

    logger.info("Container ready: %s (ID: %s)", container_name, container.id[:12])
    return ContainerInstance(
        container_id=container.id,
        container_name=container_name,
        image_ref=image_ref,
    )


def exec_in_container(
    client: DockerClient,
    container_name: str,
    command: list[str],
) -> ContainerExecResult:
    """Execute a command inside a running container.

    Args:
        client: Active python-on-whales Podman client.
        container_name: Name of the running container.
        command: Command argv to execute.

    Returns:
        ContainerExecResult with exit_code, per-stream stdout/stderr, and a
        combined ``output`` for convenience.
    """
    logger.debug("Container exec [%s]: %s", container_name, command)
    stdout_parts: list[str] = []
    stderr_parts: list[str] = []

    try:
        # stream=True yields (stream_name, chunk) tuples so we can keep
        # stdout and stderr separate; stream=False would merge them.
        output = client.container.execute(
            container_name,
            command,
            stream=True,
        )
        if output is None:
            raise ContainerRuntimeError(
                f"podman exec returned no output stream for {container_name}"
            )

        for stream_name, chunk in cast("Iterator[tuple[str, bytes]]", output):
            parts = stderr_parts if stream_name == "stderr" else stdout_parts
            parts.append(chunk.decode("utf-8", errors="replace"))
        return _make_exec_result(0, stdout_parts, stderr_parts)
    except DockerException as exc:
        # If the exception streamed nothing through, fall back to the
        # output captured on the exception itself.
        if not stdout_parts and exc.stdout:
            stdout_parts.append(exc.stdout)
        if not stderr_parts and exc.stderr:
            stderr_parts.append(exc.stderr)
        return _make_exec_result(exc.return_code, stdout_parts, stderr_parts)


def _make_exec_result(
    exit_code: int,
    stdout_parts: list[str],
    stderr_parts: list[str],
) -> ContainerExecResult:
    stdout = "".join(stdout_parts)
    stderr = "".join(stderr_parts)
    return ContainerExecResult(
        exit_code=exit_code,
        stdout=stdout,
        stderr=stderr,
        output=stdout + stderr,
    )


def wait_until_service_ready(
    exec_shell: Callable[[str], ContainerExecResult],
    command: str,
    *,
    contains: str = "",
    attempts: int = 10,
    delay: float = 1.0,
) -> ContainerExecResult:
    """Poll ``command`` until it exits 0 and its output contains ``contains``."""
    output = ""
    for attempt in range(attempts):
        if attempt:
            time.sleep(delay)
        result = exec_shell(command)
        if result.exit_code == 0 and contains in result.output:
            return result
        output = result.output
    raise AssertionError(f"{command!r} never became ready: {output}")


def destroy_container(client: DockerClient, container_name: str) -> None:
    """Kill and remove a container (best-effort, never raises)."""
    logger.info("Destroying container %s", container_name)
    try:
        client.container.remove(container_name, force=True)
    except (NoSuchContainer, DockerException) as exc:
        logger.debug("Container remove skipped (%s): %s", container_name, exc)
