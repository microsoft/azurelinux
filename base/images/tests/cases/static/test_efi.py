# SPDX-License-Identifier: MIT
"""Validate EFI system partition configuration."""

from __future__ import annotations

from pathlib import Path

import pytest

from utils.types import PartitionInfo


@pytest.mark.require_capability("machine-bootable")
def test_efi_partition_has_restrictive_umask(
    partition_table: list[PartitionInfo],
    rootfs: Path,
) -> None:
    """UEFI images must restrict access to the EFI system partition."""
    efi_mountpoints = {"/boot/efi", "/efi"}

    # BIOS images share the machine-bootable capability but have no ESP.
    efi_parts = [
        part
        for part in partition_table
        if part.mountpoint in efi_mountpoints and part.type == "vfat"
    ]
    if not efi_parts:
        pytest.skip("Image has no EFI system partition")

    fstab_path = rootfs / "etc" / "fstab"
    assert fstab_path.exists(), f"fstab not found at {fstab_path}"

    # fstab fields are: device, mountpoint, filesystem, options, dump, pass.
    # Parse active rows so fields[1] is the mountpoint and fields[3] the options.
    efi_entries = []
    for line in fstab_path.read_text().splitlines():
        fields = line.split()
        if fields and not fields[0].startswith("#") and len(fields) >= 4:
            if fields[1] in efi_mountpoints:
                efi_entries.append(fields)

    assert len(efi_entries) == 1, (
        f"Expected exactly one EFI fstab entry, found {len(efi_entries)}: "
        f"{efi_entries}"
    )

    # FAT has no Unix mode bits, so its mounted permissions come from these options.
    mount_options = set(efi_entries[0][3].split(","))
    assert "umask=0077" in mount_options, (
        "EFI system partition must be mounted with umask=0077; "
        f"found options: {efi_entries[0][3]}"
    )
