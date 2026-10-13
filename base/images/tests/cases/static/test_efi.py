# SPDX-License-Identifier: MIT
"""Validate EFI system partition configuration."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pathlib import Path

    from utils.types import PartitionInfo

MIN_FSTAB_FIELDS = 4


@pytest.mark.require_capability("machine-bootable")
def test_efi_partition_has_restrictive_mount_options(
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
        if (
            fields
            and not fields[0].startswith("#")
            and len(fields) >= MIN_FSTAB_FIELDS
            and fields[1] in efi_mountpoints
        ):
            efi_entries.append(fields)

    assert len(efi_entries) == 1, (
        f"Expected exactly one EFI fstab entry, found {len(efi_entries)}: "
        f"{efi_entries}"
    )

    efi_entry = efi_entries[0]
    assert re.fullmatch(r"UUID=[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}", efi_entry[0]), (
        f"EFI system partition must use a filesystem UUID; found: {efi_entry[0]}"
    )
    assert efi_entry[1:] == [
        "/boot/efi",
        "vfat",
        "defaults,umask=0077,noexec,nodev,nosuid,nosymfollow",
        "0",
        "0",
    ], (
        "EFI system partition must use the canonical restrictive fstab fields; "
        f"found: {' '.join(efi_entry)}"
    )
