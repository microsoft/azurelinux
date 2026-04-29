# SPDX-License-Identifier: MIT
"""VM disk inspection via libguestfs CLI tools."""

from __future__ import annotations

import logging
import xml.etree.ElementTree as ET
from pathlib import Path

from .extract import _guestfs_env, _run
from .tools import NativeTool
from .types import DiskInfo, PartitionInfo

logger = logging.getLogger(__name__)

VIRT_INSPECTOR = NativeTool(
    name="virt-inspector",
    package_hint="guestfs-tools",
    reason="inspect VM disk partitions and filesystems",
    when="vm",
)


def inspect_disk(image_path: Path) -> DiskInfo:
    """Run ``virt-inspector`` on a VM image and return structured disk info."""
    result = _run(
        [VIRT_INSPECTOR.name, "-a", str(image_path)],
        env=_guestfs_env(),
    )
    return _parse_virt_inspector(result.stdout)


def _parse_virt_inspector(xml_output: str) -> DiskInfo:
    """Parse ``virt-inspector`` XML output into :class:`DiskInfo`.

    Expected structure::

        <operatingsystems>
          <operatingsystem>
            <mountpoints>
              <mountpoint dev="/dev/sda2">/</mountpoint>
            </mountpoints>
            <filesystems>
              <filesystem dev="/dev/sda1">
                <type>vfat</type>
                <label>EFI</label>
                <uuid>...</uuid>
              </filesystem>
            </filesystems>
          </operatingsystem>
        </operatingsystems>
    """
    root = ET.fromstring(xml_output)  # noqa: S314 — trusted tool output

    # Build a device → mountpoint map from <mountpoints>
    dev_to_mount: dict[str, str] = {}
    for mp in root.iter("mountpoint"):
        dev = mp.get("dev")
        if dev and mp.text:
            dev_to_mount[dev] = mp.text
    logger.debug("Mountpoint map: %s", dev_to_mount)

    partitions: list[PartitionInfo] = []
    total_size = 0

    for fs_elem in root.iter("filesystem"):
        device = fs_elem.get("dev", "")
        fs_type = fs_elem.findtext("type", "unknown")
        uuid = fs_elem.findtext("uuid")
        label = fs_elem.findtext("label")
        size = int(fs_elem.findtext("size", "0"))

        mountpoint = dev_to_mount.get(device)

        logger.debug(
            "Partition: dev=%s type=%s label=%s mount=%s size=%d",
            device, fs_type, label, mountpoint, size,
        )

        partitions.append(
            PartitionInfo(
                device=device,
                type=fs_type,
                size_bytes=size,
                label=label or None,
                mountpoint=mountpoint,
                uuid=uuid or None,
            )
        )
        total_size += size

    return DiskInfo(partitions=partitions, total_size_bytes=total_size)
