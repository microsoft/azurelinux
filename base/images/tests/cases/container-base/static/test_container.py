# SPDX-License-Identifier: MIT

from __future__ import annotations

import os
import re
import pytest
from pathlib import Path

# Default upper-bound for the unpacked container rootfs (MiB).
# Ported from the legacy "Memory Usage Check" / "Container Size Max Check"
# in the CBL-Mariner ContainerBase BVT. Override via env var
# AZL_CONTAINER_MAX_SIZE_MB to adjust the gate per build flavor.
_DEFAULT_MAX_ROOTFS_MB = 250



def test_no_kernel_modules(rootfs: Path) -> None:
    """Container images must not ship kernel modules."""
    for modules_dir in (
        rootfs / "lib" / "modules",
        rootfs / "usr" / "lib" / "modules",
    ):
        if modules_dir.exists():
            versions = list(modules_dir.iterdir())
            assert not versions, (
                f"Container image has kernel modules under {modules_dir}: "
                f"{[v.name for v in versions]}"
            )

def test_file_exists_root(rootfs: Path) -> None:
    """Root directory must exist."""
    assert rootfs.exists(), "Root directory does not exist"


def test_file_exists_bin_date(rootfs: Path) -> None:
    """Date binary must exist and be executable by owner."""
    path = rootfs / "bin" / "date"
    assert path.exists(), f"File {path} does not exist"
    # Check executable by owner (user x bit)
    mode = path.stat().st_mode
    assert mode & 0o100, f"File {path} is not executable by owner"


def test_file_exists_bin_bash(rootfs: Path) -> None:
    """Bash must exist."""
    path = rootfs / "bin" / "bash"
    assert path.exists(), f"File {path} does not exist"


def test_file_exists_etc_dnf_dnf_conf(rootfs: Path) -> None:
    """DNF config must exist."""
    path = rootfs / "etc" / "dnf" / "dnf.conf"
    assert path.exists(), f"File {path} does not exist"


def test_file_not_exists_etc_dummy(rootfs: Path) -> None:
    """Dummy file should not exist (negative test)."""
    path = rootfs / "etc" / "dummy"
    assert not path.exists(), f"File {path} should not exist"


def test_os_release(rootfs: Path, os_release: dict[str, str]) -> None:
    """os-release must exist and identify the container variant.

    ID and VERSION_ID are validated globally in cases/test_os_release.py;
    here we only assert the container-specific VARIANT_ID.
    """
    path = rootfs / "etc" / "os-release"
    assert path.exists(), f"File {path} does not exist"
    assert os_release.get("VARIANT_ID") == "container", \
        f"Expected VARIANT_ID=container, got {os_release.get('VARIANT_ID')}"


def test_passwd(rootfs: Path) -> None:
    """passwd must exist and contain a valid root entry."""
    path = rootfs / "etc" / "passwd"
    assert path.exists(), f"File {path} does not exist"
    content = path.read_text()
    # Pattern: root:x:0:0:Super User:/root:/bin/bash or similar
    pattern = r"^root:x:0:0:.*:/root:/bin/bash"
    assert re.search(pattern, content, re.MULTILINE), \
        f"Root entry not found in passwd file matching pattern {pattern}"


def test_license_bash_exists(rootfs: Path) -> None:
    """Bash license file must exist."""
    path = rootfs / "usr" / "share" / "licenses" / "bash" / "COPYING"
    assert path.exists(), f"License file {path} does not exist"


def test_license_coreutils_single_exists(rootfs: Path) -> None:
    """coreutils-single license file must exist."""
    path = rootfs / "usr" / "share" / "licenses" / "coreutils-single" / "COPYING"
    assert path.exists(), f"License file {path} does not exist"


def test_root_home_dir_exists(rootfs: Path) -> None:
    """Root user home directory must exist."""
    root_home = rootfs / "root"
    assert root_home.exists(), "root home directory does not exist"


def test_container_rootfs_size(rootfs: Path) -> None:
    """Container rootfs footprint must stay within the configured max.

    Ports the legacy ContainerBase BVT "Memory Usage Check" /
    "Container Size Max Check": walks the extracted rootfs and asserts
    the total on-disk size is under AZL_CONTAINER_MAX_SIZE_MB (MiB).
    """
    max_mb = int(os.environ.get("AZL_CONTAINER_MAX_SIZE_MB", _DEFAULT_MAX_ROOTFS_MB))

    total_bytes = 0
    for dirpath, _dirnames, filenames in os.walk(rootfs, followlinks=False):
        for name in filenames:
            fp = Path(dirpath) / name
            try:
                # lstat: don't follow symlinks, don't double-count targets
                total_bytes += fp.lstat().st_size
            except (FileNotFoundError, PermissionError):
                continue

    total_mb = total_bytes / (1024 * 1024)
    print(f"Container rootfs size: {total_mb:.1f} MiB (limit {max_mb} MiB)")
    assert total_mb <= max_mb, (
        f"Container rootfs is {total_mb:.1f} MiB, exceeds limit of {max_mb} MiB"
    )
