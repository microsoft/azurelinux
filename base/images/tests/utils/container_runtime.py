# SPDX-License-Identifier: MIT
"""Container runtime orchestration for dynamic testing.

Provides fixtures and utilities for creating running containers with exec access
for dynamic integration testing.
"""

from __future__ import annotations

import logging
import subprocess
import time
from pathlib import Path
from typing import NamedTuple

from .tools import NativeTool

logger = logging.getLogger(__name__)

# Container runtime tools
PODMAN = NativeTool(
    name="podman",
    package_hint="podman",
    reason="create and manage test containers",
    when="container",
)

class ContainerExecInstance(NamedTuple):
    """Running container instance with podman exec access."""
    container_id: str
    container_name: str
    image_ref: str


class ContainerRuntimeError(Exception):
    """Container runtime operation failed."""
    pass


def _run_container_cmd(cmd: list[str], timeout: int = 300, **kwargs: object) -> subprocess.CompletedProcess[str]:
    """Run container command with proper error handling.

    Args:
        cmd: Command and arguments to run.
        timeout: Maximum seconds to wait (default 300). Prevents operations
            like ``podman load`` or ``podman run`` from hanging indefinitely
            in CI when storage or network layers stall.
    """
    logger.info("Container runtime: %s", " ".join(cmd))
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, **kwargs)
    if result.returncode != 0:
        logger.error(
            "Container command failed (rc=%d): %s\nstdout: %s\nstderr: %s",
            result.returncode,
            " ".join(cmd), 
            result.stdout,
            result.stderr,
        )
        raise ContainerRuntimeError(
            f"Container command failed: {' '.join(cmd)}\n"
            f"Error: {result.stderr}"
        )
    return result


def _parse_loaded_images(load_stdout: str) -> list[str]:
    """Extract image references from ``podman load`` stdout.

    podman/docker print one or more lines of the form::

        Loaded image: localhost/foo:bar
        Loaded image(s): localhost/foo:bar,localhost/baz:qux

    We accept both forms, split comma-separated lists, and return the
    references in the order they were reported. This is race-free —
    unlike scanning ``podman images --sort created``, it cannot be
    perturbed by other processes loading or pulling images concurrently.
    """
    refs: list[str] = []
    for line in load_stdout.splitlines():
        line = line.strip()
        # Match "Loaded image:" and "Loaded image(s):" (case-insensitive).
        lowered = line.lower()
        for prefix in ("loaded image(s):", "loaded image:"):
            if lowered.startswith(prefix):
                payload = line[len(prefix):].strip()
                # Some versions emit comma-separated lists on one line.
                for ref in payload.split(","):
                    ref = ref.strip()
                    if ref:
                        refs.append(ref)
                break
    return refs


def resolve_image_reference(image_path: Path) -> str:
    """Return a podman-usable image reference for *image_path*.

    If *image_path* looks like an already-resolved image reference (contains
    ``:``) the value is returned as-is.  Otherwise the file is loaded via
    ``podman load`` and the reference reported by podman is returned.
    """
    image_str = str(image_path)

    # If it's already a container reference (contains :), use directly
    if ":" in image_str and not image_str.startswith("/"):
        return image_str

    # If it's an OCI archive file, load it first
    if image_path.exists() and image_path.suffix in (".tar", ".gz", ".xz"):
        logger.info("Loading image archive: %s", image_path)
        load_cmd = [PODMAN.name, "load", "-i", str(image_path)]
        load_result = _run_container_cmd(load_cmd)

        # Parse the actual reference(s) reported by `podman load` rather
        # than picking "the most recently created image", which is racy
        # under parallel test runs or a busy dev machine where another
        # process may have just pulled/loaded an image.
        loaded_images = _parse_loaded_images(load_result.stdout)
        if not loaded_images:
            # Some podman versions write the "Loaded image:" line to
            # stderr; fall back to that before giving up.
            loaded_images = _parse_loaded_images(load_result.stderr)
        if not loaded_images:
            raise ContainerRuntimeError(
                f"Could not determine image reference from `podman load` output "
                f"for {image_path}.\nstdout: {load_result.stdout!r}\n"
                f"stderr: {load_result.stderr!r}"
            )
        if len(loaded_images) > 1:
            logger.info(
                "Archive %s contained %d images; using the first: %s (others: %s)",
                image_path, len(loaded_images), loaded_images[0], loaded_images[1:],
            )
        return loaded_images[0]

    # Assume it's a direct image reference
    return image_str


def create_container_with_exec(
    image_path: Path,
    container_name: str | None = None,
    image_name: str | None = None,
    image_ref: str | None = None,
) -> ContainerExecInstance:
    """Create a running container with podman exec access.

    Args:
        image_path: Path to image file or image reference. Ignored when
            *image_ref* is provided.
        container_name: Container name (auto-generated if ``None``).
        image_name: Human-readable image name used in log messages.
        image_ref: Pre-resolved image reference (skips ``podman load``).
            When provided, ``image_path`` is not touched. Use this to
            amortize the ~10s tarball load across many container creates.
    """

    # Generate container name if not provided
    if container_name is None:
        timestamp = int(time.time())
        import random
        random_suffix = random.randint(1000, 9999)
        container_name = f"azl-test-{timestamp}-{random_suffix}"

    # Get image reference (load if needed) — but skip if caller already
    # resolved one for us (e.g. session-scoped fixture).
    if image_ref is None:
        image_ref = resolve_image_reference(image_path)
    logger.info(
        "Creating exec container %s from image %s%s",
        container_name, image_ref,
        f" ({image_name})" if image_name else "",
    )
    
    # Create and start container
    run_cmd = [
        PODMAN.name, "run", "-d",
        "--name", container_name,
        "--replace",  # Replace existing container with same name
        "--tmpfs", "/run",
        "--tmpfs", "/tmp", 
        image_ref,
        "sleep", "infinity"  # Keep container running indefinitely
    ]
    
    result = _run_container_cmd(run_cmd)
    container_id = result.stdout.strip()

    # Wait briefly for container to start, then verify exec access.
    # If anything goes wrong from here on we MUST tear the container
    # down — otherwise a flaky readiness probe leaks containers in CI
    # and on dev machines, and subsequent runs fail with name conflicts
    # or resource exhaustion.
    try:
        logger.info("Waiting for exec container %s to start...", container_name)
        time.sleep(2)

        test_result = exec_container_command_raw(
            container_name, ["echo", "container-ready"]
        )
        if test_result.returncode != 0 or "container-ready" not in test_result.stdout:
            raise ContainerRuntimeError(
                f"Container exec test failed for {container_name} "
                f"(rc={test_result.returncode}, stdout={test_result.stdout!r}, "
                f"stderr={test_result.stderr!r})"
            )
    except BaseException:
        # Best-effort cleanup; never let cleanup errors mask the original.
        # BaseException covers KeyboardInterrupt / SystemExit too — we
        # still want the container removed when the user Ctrl-C's mid-probe.
        logger.warning(
            "Readiness probe failed for %s; removing leaked container",
            container_name,
        )
        try:
            subprocess.run(
                [PODMAN.name, "rm", "-f", container_name],
                capture_output=True, text=True, timeout=30,
            )
        except Exception as cleanup_exc:  # pragma: no cover
            logger.warning(
                "Failed to remove leaked container %s: %s",
                container_name, cleanup_exc,
            )
        raise

    logger.info(
        "Exec container ready: %s (ID: %s)",
        container_name, container_id[:12]
    )

    return ContainerExecInstance(
        container_id=container_id,
        container_name=container_name,
        image_ref=image_ref,
    )


def exec_container_command_raw(
    container_name: str, 
    command: list[str],
    timeout: int = 60,
    **kwargs: object
) -> subprocess.CompletedProcess[str]:
    """Execute command in container via podman exec (raw version)."""
    exec_cmd = [PODMAN.name, "exec", container_name] + command
    
    logger.debug("Container exec: %s", " ".join(command))
    return subprocess.run(
        exec_cmd,
        capture_output=True,
        text=True,
        timeout=timeout,
        **kwargs
    )


def exec_container_command(
    container: ContainerExecInstance, 
    command: str,
    timeout: int = 60,
    check: bool = True
) -> subprocess.CompletedProcess[str]:
    """Execute command in container via podman exec.
    
    Args:
        container: Container instance
        command: Shell command to execute
        timeout: Command timeout in seconds
        check: Raise exception on non-zero exit code
        
    Returns:
        Completed process with stdout/stderr
    """
    result = exec_container_command_raw(
        container.container_name, 
        ["bash", "-c", command],
        timeout=timeout
    )
    
    if check and result.returncode != 0:
        logger.error(
            "Container exec failed (rc=%d): %s\nstdout: %s\nstderr: %s",
            result.returncode, command, result.stdout, result.stderr
        )
        raise ContainerRuntimeError(
            f"Container exec failed: {command}\n"
            f"Exit code: {result.returncode}\n"
            f"Error: {result.stderr}"
        )
    
    return result


def destroy_exec_container(container: ContainerExecInstance) -> None:
    """Stop and remove exec container."""
    logger.info("Destroying exec container %s", container.container_name)

    # Stop container
    try:
        _run_container_cmd([
            PODMAN.name, "stop", "-t", "10", container.container_name
        ])
    except ContainerRuntimeError:
        logger.warning("Failed to stop container gracefully")
    
    # Remove container
    try:
        _run_container_cmd([
            PODMAN.name, "rm", "-f", container.container_name  
        ])
    except ContainerRuntimeError:
        logger.warning("Failed to remove container")

