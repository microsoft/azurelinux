# SPDX-License-Identifier: MIT
"""Validate VM partition layout."""

from __future__ import annotations

import pytest

from utils.types import PartitionInfo


def test_has_root_partition(partition_table: list[PartitionInfo]) -> None:
    """Image must define exactly one root ('/') filesystem."""
    root_parts = [p for p in partition_table if p.mountpoint == "/"]
    assert len(root_parts) == 1, (
        f"Expected exactly one root partition, found {len(root_parts)}: "
        f"{root_parts}"
    )


def test_has_efi_partition(partition_table: list[PartitionInfo]) -> None:
    """UEFI VM images must have a vfat EFI system partition."""
    efi_mountpoints = {"/boot/efi", "/efi"}
    efi_parts = [
        p
        for p in partition_table
        if p.mountpoint in efi_mountpoints and p.type == "vfat"
    ]
    if not efi_parts:
        pytest.fail(
            "No vfat EFI partition found "
            f"(expected mountpoint in {sorted(efi_mountpoints)})"
        )
