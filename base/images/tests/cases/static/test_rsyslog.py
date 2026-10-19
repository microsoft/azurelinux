# SPDX-License-Identifier: MIT
"""Validate ownership and permissions of rsyslog configuration files."""

from __future__ import annotations

import stat
from typing import TYPE_CHECKING

import pytest
from utils.extract import resolve_path_confined

if TYPE_CHECKING:
    import os
    from pathlib import Path

FORBIDDEN_MODE_MASK = 0o7137
RSYSLOG_CONFIG_PATH = "etc/rsyslog.conf"
RSYSLOG_DROPIN_DIR = "etc/rsyslog.d"
RSYSLOG_PACKAGE = "rsyslog"
CLOUD_INIT_PACKAGE = "cloud-init"
AZURELINUX_RELEASE_CLOUD_PACKAGE = "azurelinux-release-cloud"


def _assert_regular_file_not_symlink(rootfs: Path, relative_path: str) -> os.stat_result:
    path = rootfs / relative_path
    assert path.exists() or path.is_symlink(), f"Required path is missing: /{relative_path}"
    assert not path.is_symlink(), f"Required path is a symlink: /{relative_path}"

    confined = resolve_path_confined(rootfs, relative_path)
    file_stat = confined.stat()
    assert stat.S_ISREG(file_stat.st_mode), f"Required path is not a regular file: /{relative_path}"
    return file_stat


def _collect_dropin_regular_files(rootfs: Path) -> tuple[dict[str, os.stat_result], list[str]]:
    dropin_dir = rootfs / RSYSLOG_DROPIN_DIR
    assert dropin_dir.exists() or dropin_dir.is_symlink(), "Missing required path: /etc/rsyslog.d"
    assert not dropin_dir.is_symlink(), "/etc/rsyslog.d must not be a symlink"

    confined_dropin_dir = resolve_path_confined(rootfs, RSYSLOG_DROPIN_DIR)
    assert confined_dropin_dir.is_dir(), "/etc/rsyslog.d is not a directory"

    files: dict[str, os.stat_result] = {}
    symlinks: list[str] = []
    pending = ["etc/rsyslog.d"]

    while pending:
        current_rel = pending.pop()
        current_dir = resolve_path_confined(rootfs, current_rel)
        for entry in sorted(current_dir.iterdir(), key=lambda candidate: candidate.name):
            entry_rel = f"{current_rel}/{entry.name}"
            entry_path = f"/{entry_rel}"
            if entry.is_symlink():
                symlinks.append(entry_path)
                continue

            confined_entry = resolve_path_confined(rootfs, entry_rel)
            entry_stat = confined_entry.stat()
            if stat.S_ISDIR(entry_stat.st_mode):
                pending.append(entry_rel)
            elif stat.S_ISREG(entry_stat.st_mode):
                files[entry_path] = entry_stat

    return files, sorted(symlinks)


def _validate_rsyslog_config_files(rootfs: Path, installed_packages: set[str]) -> None:
    if RSYSLOG_PACKAGE not in installed_packages:
        pytest.skip("rsyslog package not installed")

    file_stats: dict[str, os.stat_result] = {
        "/etc/rsyslog.conf": _assert_regular_file_not_symlink(rootfs, RSYSLOG_CONFIG_PATH),
    }

    dropin_files, symlink_entries = _collect_dropin_regular_files(rootfs)
    assert not symlink_entries, (
        "Rsyslog drop-in tree contains symlink entries (refusing traversal): "
        f"{symlink_entries}"
    )
    file_stats.update(dropin_files)

    if CLOUD_INIT_PACKAGE in installed_packages:
        file_stats["/etc/rsyslog.d/21-cloudinit.conf"] = _assert_regular_file_not_symlink(
            rootfs, "etc/rsyslog.d/21-cloudinit.conf"
        )

    if AZURELINUX_RELEASE_CLOUD_PACKAGE in installed_packages:
        file_stats["/etc/rsyslog.d/00-rsyslog_filecreatemode.conf"] = (
            _assert_regular_file_not_symlink(
                rootfs, "etc/rsyslog.d/00-rsyslog_filecreatemode.conf"
            )
        )

    violations = []
    for path, file_stat in sorted(file_stats.items()):
        mode = stat.S_IMODE(file_stat.st_mode)
        if file_stat.st_uid != 0 or file_stat.st_gid != 0 or mode & FORBIDDEN_MODE_MASK:
            violations.append(
                f"{path}: uid={file_stat.st_uid}, gid={file_stat.st_gid}, mode={mode:04o}"
            )

    assert not violations, (
        "Rsyslog configuration files must be root:root with mode 0640 or more restrictive "
        f"(mask {FORBIDDEN_MODE_MASK:04o}); found: {violations}"
    )


@pytest.mark.require_capability("runtime-package-management")
def test_rsyslog_configuration_files_are_root_only(
    rootfs: Path, installed_packages: set[str]
) -> None:
    """Rsyslog configuration files must be root-owned and restrictive."""
    _validate_rsyslog_config_files(rootfs, installed_packages)
