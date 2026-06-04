# SPDX-License-Identifier: MIT
"""Kernel-related checks for VM images."""

from __future__ import annotations

from pathlib import Path

import pytest


def test_kernel_modules_present(rootfs: Path) -> None:
    """A bootable VM image must ship at least one kernel's modules."""
    modules_dir = rootfs / "usr" / "lib" / "modules"
    if not modules_dir.exists():
        modules_dir = rootfs / "lib" / "modules"
    assert modules_dir.exists(), "No kernel modules directory found"
    versions = [d.name for d in modules_dir.iterdir() if d.is_dir()]
    assert versions, "No kernel version subdirectories under modules dir"


def _parse_config_lsm(rootfs: Path) -> str | None:
    """Extract the CONFIG_LSM value from the installed kernel config."""
    modules_dir = rootfs / "usr" / "lib" / "modules"
    if not modules_dir.exists():
        modules_dir = rootfs / "lib" / "modules"
    assert modules_dir.exists(), "No kernel modules directory found"
    versions = sorted(d.name for d in modules_dir.iterdir() if d.is_dir())
    assert versions, "No kernel version subdirectories under modules dir"
    config_path = modules_dir / versions[-1] / "config"
    assert config_path.exists(), f"Kernel config not found at {config_path}"
    for line in config_path.read_text().splitlines():
        if line.startswith("CONFIG_LSM="):
            return line.split("=", 1)[1].strip('"')
    pytest.fail(f"CONFIG_LSM not found in {config_path}")


def test_config_lsm_matches_upstream(rootfs: Path) -> None:
    """CONFIG_LSM must match the Fedora 43 upstream value exactly.

    Upstream reference:
    https://src.fedoraproject.org/rpms/kernel/blob/f43/f/kernel-x86_64-fedora.config#_3941
    """
    expected = "lockdown,yama,integrity,selinux,bpf,landlock,ipe"
    actual = _parse_config_lsm(rootfs)
    assert actual == expected, f"CONFIG_LSM does not match upstream.\n  Expected: {expected}\n  Actual:   {actual}"
