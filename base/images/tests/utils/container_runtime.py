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
    """Running container instance with exec access (faster alternative to SSH)."""
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
) -> ContainerExecInstance:
    """Create running container with exec access (fast alternative to SSH).
    
    This is much faster than SSH-based containers as it:
    - Skips SSH key generation
    - Skips openssh-server installation
    - Skips SSH daemon setup and connectivity testing
    - Uses direct podman exec for command execution
    
    Args:
        image_path: Path to image file or image reference
        workdir: Working directory (unused but kept for compatibility)
        container_name: Container name (auto-generated if None)
        image_name: Image name for logging (derived if None)
    """
    
    # Generate container name if not provided
    if container_name is None:
        timestamp = int(time.time())
        import random
        random_suffix = random.randint(1000, 9999)
        container_name = f"azl-test-{timestamp}-{random_suffix}"

    # Container names can be reused across test suites; clear any stale
    # package-install cache from prior container instances with same name.
    _installed_packages_cache.pop(container_name, None)
    
    # Get image reference (load if needed)
    image_ref = _get_image_reference(image_path)
    logger.info("Creating exec container %s from image %s", container_name, image_ref)
    
    # Create and start container - much simpler than SSH version
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
    time.sleep(2)  # Much shorter wait than SSH setup
    
    # Test basic exec access
    test_result = exec_container_command_raw(container_name, ["echo", "container-ready"])
    if test_result.returncode != 0 or "container-ready" not in test_result.stdout:
        raise ContainerRuntimeError(f"Container exec test failed for {container_name}")
    
    # Pre-warm the dnf metadata cache so subsequent installs are fast.
    # This is non-fatal: if it times out the installs will just be slow.
    try:
        logger.info("Pre-warming dnf metadata cache")
        exec_container_command_raw(container_name, ["dnf", "makecache"], timeout=300)
        logger.info("dnf metadata cache warmed")
    except subprocess.TimeoutExpired:
        logger.warning("dnf makecache timed out — installs may be slow")

    # Pre-install essential packages only if any are actually missing.
    # Checking binaries first avoids a dnf metadata refresh when the
    # image already ships these packages.
    essential = {
        "procps-ng":   "free",
        "util-linux":  "logger",
        "gawk":        "awk",
        "which":       "which",
        "hostname":    "hostname",
        "python3":     "python3",
    }
    missing = [
        pkg for pkg, cmd in essential.items()
        if exec_container_command_raw(container_name, ["which", cmd], timeout=5).returncode != 0
    ]
    if missing:
        logger.info("Installing missing essential packages: %s", missing)
        try:
            install_result = exec_container_command_raw(
                container_name,
                ["dnf", "install", "-y"] + missing,
                timeout=300,
            )
            if install_result.returncode == 0:
                logger.info("Essential packages installed successfully")
            else:
                logger.warning("Some essential packages may not have installed: %s", install_result.stderr)
        except subprocess.TimeoutExpired:
            logger.warning(
                "Preinstall timed out after 300s — packages will be installed on-demand per test"
            )
    else:
        logger.info("All essential packages already present — skipping dnf install")
    
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


# Global cache to track installed packages per container
_installed_packages_cache: dict[str, set[str]] = {}

def ensure_packages_in_container(container_name: str, packages: list[str]) -> bool:
    """Ensure packages are installed in the container. Install if missing."""
    if not packages:
        return True
        
    # Initialize cache for this container
    if container_name not in _installed_packages_cache:
        _installed_packages_cache[container_name] = set()
    
    # Filter out packages we've already tried installing
    packages_to_install = [
        pkg for pkg in packages 
        if pkg not in _installed_packages_cache[container_name]
    ]
    
    if not packages_to_install:
        return True  # All packages already processed
    
    # Test commands for each package to see if they're available
    package_commands = {
        "procps-ng": "free",
        "gawk": "awk", 
        "util-linux": "logger",
        "bc": "bc",
        "bind-utils": "nslookup",
        "iproute": "ip",
        "iproute2": "ip",
        "iputils": "ping",
        "shadow-utils": "useradd",
        "python3": "python3",
        "which": "which",
        "hostname": "hostname",
        "systemd": "systemctl",
    }
    
    missing_packages = []
    for package in packages_to_install:
        command = package_commands.get(package, package)
        test_result = exec_container_command_raw(
            container_name, ["which", command], timeout=3
        )
        
        if test_result.returncode != 0:
            missing_packages.append(package)
    
    # Install all missing packages in a single command with shorter timeout and retry
    if missing_packages:
        logger.info("Installing packages %s in container %s", missing_packages, container_name)
        
        # First attempt with shorter timeout
        install_result = exec_container_command_raw(
            container_name, 
            ["dnf", "install", "-y"] + missing_packages, 
            timeout=90
        )
        
        # If first attempt failed due to timeout, try individual packages
        if install_result.returncode != 0:
            logger.warning("Bulk install failed, trying individual packages")
            success_count = 0
            for package in missing_packages:
                individual_result = exec_container_command_raw(
                    container_name, 
                    ["dnf", "install", "-y", package], 
                    timeout=60
                )
                if individual_result.returncode == 0:
                    success_count += 1
            
            # Consider it successful if most packages installed
            install_success = success_count >= len(missing_packages) * 0.7
        else:
            install_success = True
        
        # Mark all packages as processed (even if installation failed)
        _installed_packages_cache[container_name].update(packages_to_install)
        
        return install_success
    else:
        # Mark as processed since all were available
        _installed_packages_cache[container_name].update(packages_to_install)
        return True


def ensure_package_in_container(container_name: str, package: str) -> bool:
    """Ensure a package is installed in the container. Install if missing."""
    return ensure_packages_in_container(container_name, [package])


def detect_required_packages(command: str) -> list[str]:
    """Detect what packages might be needed for a command."""
    command_to_package = {
        "free": "procps-ng",
        "ps": "procps-ng", 
        "awk": "gawk",
        "logger": "util-linux",
        "bc": "bc",
        "nslookup": "bind-utils",
        "ip": "iproute",
        "ping": "iputils", 
        "useradd": "shadow-utils",
        "systemctl": "systemd",
        "python3": "python3",
        "python": "python3",
        "which": "which",
        "hostname": "hostname",
        "whereis": "which",
        "uptime": "procps-ng",
        "top": "procps-ng",
    }
    
    packages = []
    for cmd, pkg in command_to_package.items():
        if cmd in command:
            packages.append(pkg)
    
    return packages


def exec_container_command_with_fallback(
    container: ContainerExecInstance, 
    command: str,
    required_packages: list[str] | None = None,
    timeout: int = 60,
    check: bool = True
) -> subprocess.CompletedProcess[str]:
    """Execute command in container, installing packages if needed."""
    
    # First try the command as-is
    result = exec_container_command_raw(
        container.container_name, 
        ["bash", "-c", command],
        timeout=timeout
    )
    
    # If command failed due to missing binary or missing target binary for
    # `which <tool>`, install required packages and retry once.
    should_install = (
        required_packages
        and (
            (result.returncode == 127 and "command not found" in result.stderr)
            or (
                result.returncode == 1
                and command.strip().startswith("which ")
                and "no " in result.stderr
            )
        )
    )

    if should_install:
        
        logger.info("Command failed, installing required packages: %s", required_packages)
        
        # Install all required packages in one operation
        ensure_packages_in_container(container.container_name, required_packages)
        
        # Retry the command
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

    # Clear package cache for this container name to avoid stale state when
    # a new container reuses the same name in a later suite.
    _installed_packages_cache.pop(container.container_name, None)
    
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

