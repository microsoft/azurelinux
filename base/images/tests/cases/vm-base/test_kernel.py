# SPDX-License-Identifier: MIT
"""Kernel-related checks for VM images."""

from __future__ import annotations

from pathlib import Path


def test_kernel_modules_present(rootfs: Path) -> None:
    """A bootable VM image must ship at least one kernel's modules."""
    modules_dir = rootfs / "usr" / "lib" / "modules"
    if not modules_dir.exists():
        modules_dir = rootfs / "lib" / "modules"
    assert modules_dir.exists(), "No kernel modules directory found"
    versions = [d.name for d in modules_dir.iterdir() if d.is_dir()]
    assert versions, "No kernel version subdirectories under modules dir"
