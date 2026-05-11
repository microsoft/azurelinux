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


def _parse_config_lsm(rootfs: Path) -> set[str]:
    """Extract the CONFIG_LSM value from the installed kernel config."""
    boot = rootfs / "boot"
    configs = sorted(boot.glob("config-*"))
    assert configs, f"No kernel config found under {boot}"
    config_path = configs[-1]
    for line in config_path.read_text().splitlines():
        if line.startswith("CONFIG_LSM="):
            value = line.split("=", 1)[1].strip('"')
            return set(value.split(","))
    pytest.fail(f"CONFIG_LSM not found in {config_path}")


def test_required_lsms_in_config(rootfs: Path) -> None:
    """CONFIG_LSM must list bpf and ipe so they are active at boot.

    At runtime these appear in /sys/kernel/security/lsm. This static
    check verifies the kernel config will produce that result without
    needing to boot the image.
    """
    required = {"bpf", "ipe"}
    active = _parse_config_lsm(rootfs)
    missing = required - active
    assert not missing, (
        f"CONFIG_LSM is missing required LSMs: {', '.join(sorted(missing))}. "
        f"Current value: {', '.join(sorted(active))}"
    )
