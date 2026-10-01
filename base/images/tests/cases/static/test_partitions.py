# SPDX-License-Identifier: MIT
"""Validate VM partition layout."""

from __future__ import annotations

import pytest
from utils.types import PartitionInfo

# Only UEFI images should run efi_partition test. Until we have uefi support in
# ImageCapabilities we exclude non-UEFI images with a name match.
_UEFI_IMAGE_FAMILIES = ("1p-vm-base-gen2", "marketplace-gen2", "minimal-os")


def _is_uefi_image(image_name: str | None) -> bool:
    if not image_name:
        return False
    return any(image_name == family or image_name.startswith(f"{family}-") for family in _UEFI_IMAGE_FAMILIES)


@pytest.mark.require_capability("machine-bootable")
def test_has_root_partition(partition_table: list[PartitionInfo]) -> None:
    """Image must define exactly one root ('/') filesystem."""
    root_parts = [p for p in partition_table if p.mountpoint == "/"]
    if len(root_parts) != 1:
        pytest.fail(f"Expected exactly one root partition, found {len(root_parts)}: {root_parts}")


@pytest.mark.require_capability("machine-bootable")
def test_has_efi_partition(partition_table: list[PartitionInfo], image_name: str | None) -> None:
    """UEFI (gen2) VM images must have a vfat EFI system partition."""
    if not _is_uefi_image(image_name):
        pytest.skip(f"EFI partition check only applies to UEFI (gen2) images (running: {image_name!r})")
    efi_mountpoints = {"/boot/efi", "/efi"}
    efi_parts = [p for p in partition_table if p.mountpoint in efi_mountpoints and p.type == "vfat"]
    if not efi_parts:
        pytest.fail(f"No vfat EFI partition found (expected mountpoint in {sorted(efi_mountpoints)})")
