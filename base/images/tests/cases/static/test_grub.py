# SPDX-License-Identifier: MIT
"""Validate ownership and permissions of GRUB configuration files."""

from __future__ import annotations

import stat
from typing import TYPE_CHECKING

import pytest
from utils.extract import resolve_path_confined

if TYPE_CHECKING:
    import os
    from pathlib import Path

pytestmark = pytest.mark.require_capability("machine-bootable")

REQUIRED_GRUB_FILES = {"grub.cfg", "grubenv"}
FORBIDDEN_MODE_MASK = 0o7177


def test_grub_configuration_files_are_root_only(
    rootfs: Path,
    capabilities: set[str],
) -> None:
    """GRUB configuration files must be owned by root and accessible only by root."""
    if "cvm" in capabilities:
        pytest.skip("CVM images use systemd-boot instead of GRUB")

    grub_dir = resolve_path_confined(rootfs, "boot/grub2")
    assert grub_dir.is_dir(), "/boot/grub2 is missing"

    grub_files: dict[str, os.stat_result] = {}
    for entry in sorted(grub_dir.iterdir()):
        resolved = resolve_path_confined(rootfs, f"boot/grub2/{entry.name}")
        file_stat = resolved.stat()
        if stat.S_ISREG(file_stat.st_mode):
            grub_files[entry.name] = file_stat

    missing = REQUIRED_GRUB_FILES - grub_files.keys()
    assert not missing, f"Required GRUB configuration files are missing: {sorted(missing)}"

    insecure = []
    for name, file_stat in grub_files.items():
        mode = stat.S_IMODE(file_stat.st_mode)
        if file_stat.st_uid != 0 or file_stat.st_gid != 0 or mode & FORBIDDEN_MODE_MASK:
            insecure.append(
                f"/boot/grub2/{name}: uid={file_stat.st_uid}, "
                f"gid={file_stat.st_gid}, mode={mode:04o}"
            )

    assert not insecure, (
        "GRUB configuration files must be root:root with mode 0600 or more restrictive; "
        f"found: {insecure}"
    )
