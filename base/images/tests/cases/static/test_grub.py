# SPDX-License-Identifier: MIT
"""Validate GRUB configuration permissions and Minimal OS console settings."""

from __future__ import annotations

import shlex
import stat
from typing import TYPE_CHECKING

import pytest
from utils.extract import read_text_confined, resolve_path_confined
from utils.parsers import parse_boot_entry_kernel_options

if TYPE_CHECKING:
    import os
    from pathlib import Path

pytestmark = pytest.mark.require_capability("machine-bootable")

REQUIRED_GRUB_FILES = {"grub.cfg", "grubenv"}
FORBIDDEN_MODE_MASK = 0o7177


def test_grub_configuration_files_are_root_only(rootfs: Path) -> None:
    """GRUB configuration files must be owned by root and accessible only by root."""
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


@pytest.mark.image("minimal-os")
def test_minimal_os_grub_supports_console_and_serial(rootfs: Path) -> None:
    """Both GRUB terminals must remain available, including after regeneration."""
    defaults = read_text_confined(rootfs, "etc/default/grub")
    assert 'GRUB_TERMINAL="console serial"' in defaults.splitlines()

    config = read_text_confined(rootfs, "boot/grub2/grub.cfg")
    for command, expected in {
        "terminal_input": {"console", "serial"},
        "terminal_output": {"console", "serial"},
    }.items():
        settings = [
            shlex.split(line)
            for line in config.splitlines()
            if line.strip().startswith(f"{command} ")
        ]
        assert settings, f"GRUB configuration has no {command}"
        assert set(settings[-1][1:]) == expected, (
            f"GRUB {command} has incorrect terminals: {settings[-1]}"
        )


@pytest.mark.image("minimal-os")
def test_minimal_os_kernel_supports_console_and_serial(
    boot_entry_option_lines: dict[Path, list[str]],
) -> None:
    """Every kernel must log to the display and the architecture's serial port."""
    serial_by_arch = {
        "x86_64": "console=ttyS0,115200n8",
        "aarch64": "console=ttyAMA0,115200n8",
    }
    for entry, options in parse_boot_entry_kernel_options(boot_entry_option_lines).items():
        arch = entry.name.rsplit(".", 2)[-2]
        assert arch in serial_by_arch, f"Unrecognized kernel architecture in {entry}"
        consoles = [option for option in options if option.startswith("console=")]
        assert consoles == ["console=tty0", serial_by_arch[arch]], (
            f"Kernel consoles are incorrect in {entry}: {consoles}"
        )
