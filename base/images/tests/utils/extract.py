# SPDX-License-Identifier: MIT
"""Image mounting/unmounting orchestration.

Uses CLI tools (guestmount, skopeo, umoci) via subprocess to avoid
system site-packages dependencies.
"""

from __future__ import annotations

import logging
import os
import subprocess
from pathlib import Path

from .tools import NativeTool

logger = logging.getLogger(__name__)

# Native tool dependencies. Declared at module level so they're registered
# (and used at the call sites below) where they're needed.
GUESTMOUNT = NativeTool(
    name="guestmount",
    package_hint="libguestfs / libguestfs-tools",
    reason="FUSE-mount VM images read-only",
    when="vm",
)
GUESTUNMOUNT = NativeTool(
    name="guestunmount",
    package_hint="libguestfs / libguestfs-tools",
    reason="unmount guestmount FUSE mounts",
    when="vm",
)
SKOPEO = NativeTool(
    name="skopeo",
    package_hint="skopeo",
    reason="convert OCI archives to OCI layouts",
    when="container",
)
UMOCI = NativeTool(
    name="umoci",
    package_hint="umoci",
    reason="rootless OCI image unpacking",
    when="container",
)
BUILDAH = NativeTool(
    name="buildah",
    package_hint="buildah",
    reason="cleanup rootless umoci extracts (buildah unshare)",
    when="container",
)


def _run(cmd: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
    """Run a command, logging it and raising with stderr on failure."""
    logger.info("Running: %s", " ".join(cmd))
    result = subprocess.run(cmd, capture_output=True, text=True, **kwargs)
    if result.returncode != 0:
        logger.error(
            "Command failed (rc=%d): %s\nstdout: %s\nstderr: %s",
            result.returncode,
            " ".join(cmd),
            result.stdout,
            result.stderr,
        )
        raise subprocess.CalledProcessError(
            result.returncode,
            cmd,
            output=result.stdout,
            stderr=result.stderr,
        )
    return result


# -- VM image mounting (libguestfs FUSE) ------------------------------------

def _guestfs_env() -> dict[str, str]:
    """Build environment with direct libguestfs backend."""
    return {**os.environ, "LIBGUESTFS_BACKEND": "direct"}


def mount_vm_image(image_path: Path, mountpoint: Path) -> Path:
    """Mount a VM image read-only via ``guestmount``.

    Enables aggressive FUSE kernel caching since the mount is read-only
    and the image never changes during the test session.

    Returns the *mountpoint* path on success.
    """
    mountpoint.mkdir(parents=True, exist_ok=True)
    cmd = [
        GUESTMOUNT.name,
        "--ro",
        "-a", str(image_path),
        "-i", str(mountpoint),
        # Aggressive caching — safe because the mount is read-only.
        "-o", "kernel_cache",
        "-o", "entry_timeout=3600",
        "-o", "attr_timeout=3600",
        "-o", "negative_timeout=3600",
        "-o", "noforget",
        "--dir-cache-timeout", "3600",
    ]
    _run(cmd, env=_guestfs_env())
    return mountpoint


def unmount_vm_image(mountpoint: Path) -> None:
    """Unmount a guestmount FUSE mount.

    Logs a warning on failure rather than raising — leaving teardown
    to fail the whole pytest session would obscure the real test
    result, and a stale FUSE mount is recoverable manually with
    ``fusermount -u``.
    """
    logger.info("Unmounting VM image at %s", mountpoint)
    result = subprocess.run(
        [GUESTUNMOUNT.name, str(mountpoint)],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        logger.warning(
            "guestunmount failed for %s (rc=%d): %s",
            mountpoint, result.returncode, result.stderr.strip(),
        )


# -- Container image extraction (skopeo + umoci) ---------------------------


def mount_container_image(image_path: Path, extract_dir: Path) -> Path:
    """Extract a container image rootfs using ``skopeo`` + ``umoci``.

    Converts the OCI archive to an OCI layout via ``skopeo copy``, then
    unpacks it with ``umoci unpack --rootless``. Returns the rootfs path.
    """
    image_path = image_path.resolve()
    extract_dir = extract_dir.resolve()
    oci_layout = extract_dir / "oci-layout"
    bundle = extract_dir / "bundle"
    extract_dir.mkdir(parents=True, exist_ok=True)

    # Convert OCI archive → OCI layout
    logger.info("Converting OCI archive to layout: %s", image_path)
    _run([
        SKOPEO.name, "copy",
        f"oci-archive:{image_path}",
        f"oci:{oci_layout}:latest",
    ])

    # Unpack into an OCI runtime bundle (rootless, no user-ns required)
    logger.info("Unpacking OCI layout to bundle: %s", bundle)
    _run([
        UMOCI.name, "unpack", "--rootless",
        "--image", f"{oci_layout}:latest",
        str(bundle),
    ])

    rootfs = bundle / "rootfs"
    logger.info("Container rootfs at %s", rootfs)
    return rootfs


def unmount_container_image(extract_dir: Path) -> None:
    """Clean up the extracted container filesystem.

    Uses ``buildah unshare`` so that read-only directories (preserved by
    rootless ``umoci unpack``) can be removed without permission errors.
    Failures are logged rather than raised; see :func:`unmount_vm_image`.
    """
    logger.info("Removing container extract dir %s", extract_dir)
    result = subprocess.run(
        [BUILDAH.name, "unshare", "rm", "-rf", str(extract_dir)],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        logger.warning(
            "buildah unshare rm failed for %s (rc=%d): %s",
            extract_dir, result.returncode, result.stderr.strip(),
        )
