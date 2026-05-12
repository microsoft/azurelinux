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
    when="dynamic-container-tests",
)

class ContainerExecInstance(NamedTuple):
    """Running container instance with podman exec access."""
    container_id: str
    container_name: str
    image_ref: str


class ContainerRuntimeError(Exception):
    """Container runtime operation failed."""
    pass


def _run_container_cmd(cmd: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
    """Run container command with proper error handling."""
    logger.info("Container runtime: %s", " ".join(cmd))
    result = subprocess.run(cmd, capture_output=True, text=True, **kwargs)
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


def _get_image_reference(image_path: Path) -> str:
    """Get container image reference from path or direct reference."""
    image_str = str(image_path)
    
    # If it's already a container reference (contains :), use directly
    if ":" in image_str and not image_str.startswith("/"):
        return image_str
    
    # If it's an OCI archive file, load it first
    if image_path.exists() and image_path.suffix in (".tar", ".gz", ".xz"):
        logger.info("Loading image archive: %s", image_path)
        load_cmd = [PODMAN.name, "load", "-i", str(image_path)]
        load_result = _run_container_cmd(load_cmd)
        
        # Get all images sorted by creation date (most recent first)
        images_result = _run_container_cmd([
            PODMAN.name, "images", "--format", "{{.Repository}}:{{.Tag}}", 
            "--sort", "created"
        ])
        loaded_images = [line.strip() for line in images_result.stdout.strip().split('\n') if line.strip()]
        if loaded_images:
            return loaded_images[0]  # Use the most recently created image
        else:
            raise ContainerRuntimeError(f"No image loaded from {image_path}")
    
    # Assume it's a direct image reference
    return image_str


def create_container_with_exec(
    image_path: Path,
    workdir: Path,
    container_name: str | None = None,
    image_name: str | None = None,
    image_ref: str | None = None,
) -> ContainerExecInstance:
    """Create a running container with podman exec access.

    Args:
        image_path: Path to image file or image reference
        workdir: Working directory (unused but kept for compatibility)
        container_name: Container name (auto-generated if None)
        image_name: Image name for logging (derived if None)
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
        image_ref = _get_image_reference(image_path)
    logger.info("Creating exec container %s from image %s", container_name, image_ref)
    
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
    
    # Wait briefly for container to start
    logger.info("Waiting for exec container %s to start...", container_name)
    time.sleep(2)
    
    # Test basic exec access
    test_result = exec_container_command_raw(container_name, ["echo", "container-ready"])
    if test_result.returncode != 0 or "container-ready" not in test_result.stdout:
        raise ContainerRuntimeError(f"Container exec test failed for {container_name}")

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

