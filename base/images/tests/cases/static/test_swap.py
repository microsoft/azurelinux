# SPDX-License-Identifier: MIT
"""Validate that bootable images do not configure a swap device.

Azure Linux images are meant to ship with swap disabled by default; any
image that needs swap is expected to enable it via later customization
rather than by default in the base profile.
"""

from __future__ import annotations

import configparser
import re
from typing import TYPE_CHECKING

import pytest
from utils.extract import read_text_confined

if TYPE_CHECKING:
    from pathlib import Path

    from utils.types import PartitionInfo

# fstab fields are: device, mountpoint, filesystem, options, dump, pass.
FSTAB_FSTYPE_FIELD = 2

# zram-generator reads its main config file from each of these
# directories, plus any drop-in fragments under a same-named
# "zram-generator.conf.d/*.conf" subdirectory (systemd drop-in
# convention); any section found in any of them can configure a
# device, so all must be checked.
ZRAM_GENERATOR_CONFIG_DIRS = (
    "usr/lib/systemd",
    "usr/local/lib/systemd",
    "etc/systemd",
)

# zram-generator permits global "set!variable=value" directives before the
# first "[section]" header (used to define arithmetic variables reusable in
# zram-size= etc). configparser has no concept of pre-section content, so
# such lines must be dropped before handing the text to it.
ZRAM_GLOBAL_DIRECTIVE_RE = re.compile(r"^\s*set!\S+\s*=.*$")

# BLS boot entries and the grub2 config both embed the effective kernel
# command line; zram-generator enables a default zram0 swap device when
# "systemd.zram" is present with no value, or any value other than "0"/
# "false" (see zram-generator.conf(5)).
KERNEL_CMDLINE_GLOB_PATHS = (
    "boot/loader/entries/*.conf",
    "boot/efi/loader/entries/*.conf",
    "boot/grub2/grub.cfg",
)
SYSTEMD_ZRAM_OPTION_RE = re.compile(r"\bsystemd\.zram(?:=(\S+))?\b")
SYSTEMD_ZRAM_DISABLED_VALUES = {"0", "false", "no", "off"}


@pytest.mark.require_capability("machine-bootable")
def test_no_swap_partition(partition_table: list[PartitionInfo]) -> None:
    """Bootable images must not include a swap partition."""
    swap_parts = [p for p in partition_table if p.type == "swap"]
    assert not swap_parts, f"Expected no swap partitions, found: {swap_parts}"


@pytest.mark.require_capability("machine-bootable")
def test_no_swap_fstab_entry(rootfs: Path) -> None:
    """Bootable images must not mount a swap device via fstab."""
    fstab_path = rootfs / "etc" / "fstab"
    if not fstab_path.exists():
        pytest.skip("No fstab present in image")

    fstab_text = read_text_confined(rootfs, "etc/fstab")
    swap_entries = [
        line
        for line in fstab_text.splitlines()
        if (fields := line.split())
        and not fields[0].startswith("#")
        and len(fields) > FSTAB_FSTYPE_FIELD
        and fields[FSTAB_FSTYPE_FIELD] == "swap"
    ]
    assert not swap_entries, f"Expected no swap entries in fstab, found: {swap_entries}"


@pytest.mark.require_capability("machine-bootable")
def test_no_zram_swap_device(rootfs: Path) -> None:
    """Bootable images must not configure a zram swap device.

    zram devices (e.g. ``/dev/zram0``) are created at boot by
    zram-generator from ``zram-generator.conf`` (and any
    ``zram-generator.conf.d/*.conf`` drop-in fragment); they never
    appear in ``fstab`` or a persistent partition table, yet still
    provide a swap device unless the section sets ``mount-point``
    (which repurposes the device as a regular filesystem instead of
    swap).

    Real zram-generator precedence lets a later drop-in add
    ``mount-point`` to a section the main file defined without it.
    This check deliberately does not replicate that merge logic: it
    flags *any* file that defines a ``[zramN]`` section without
    ``mount-point``, even if another file would override it. This
    trades a possible false failure (a legitimately overridden
    section) for never missing a real swap device — acceptable for a
    hard "no swap" policy.
    """
    swap_sections: list[str] = []
    for conf_dir in ZRAM_GENERATOR_CONFIG_DIRS:
        candidates = [f"{conf_dir}/zram-generator.conf"]
        dropin_dir = rootfs / conf_dir / "zram-generator.conf.d"
        if dropin_dir.is_dir():
            candidates.extend(
                f"{conf_dir}/zram-generator.conf.d/{p.name}"
                for p in sorted(dropin_dir.iterdir())
                if p.suffix == ".conf"
            )

        for rel_path in candidates:
            if not (rootfs / rel_path).exists():
                continue
            conf_text = read_text_confined(rootfs, rel_path)
            # Strip global "set!var=value" directives that may precede the
            # first "[section]" header — valid zram-generator syntax that
            # configparser cannot parse (it raises MissingSectionHeaderError
            # on any pre-section content).
            conf_text = "\n".join(
                line for line in conf_text.splitlines() if not ZRAM_GLOBAL_DIRECTIVE_RE.match(line)
            )
            # Disable configparser's own "[DEFAULT]" section, which would
            # otherwise make has_option() report a false "mount-point is
            # set" for any [zramN] section merely because an unrelated
            # [DEFAULT] section set it — zram-generator itself has no
            # such fallback, so that would let a real swap section slip
            # through undetected.
            parser = configparser.ConfigParser(default_section="")
            parser.read_string(conf_text)
            for section in parser.sections():
                if not parser.has_option(section, "mount-point"):
                    swap_sections.append(f"{rel_path}:[{section}]")

    assert not swap_sections, f"Expected no zram swap devices configured, found: {swap_sections}"


@pytest.mark.require_capability("machine-bootable")
def test_no_zram_swap_kernel_cmdline(rootfs: Path) -> None:
    """Bootable images must not enable zram swap via the kernel command line.

    zram-generator activates a default ``zram0`` swap device when the
    kernel command line carries ``systemd.zram`` with no value, or any
    value other than ``0``/``false``/``no``/``off`` — independent of any
    on-disk ``zram-generator.conf``.
    """
    enabling_entries: list[str] = []
    for glob_pattern in KERNEL_CMDLINE_GLOB_PATHS:
        for conf_path in sorted(rootfs.glob(glob_pattern)):
            rel_path = str(conf_path.relative_to(rootfs))
            cmdline_text = read_text_confined(rootfs, rel_path)
            for match in SYSTEMD_ZRAM_OPTION_RE.finditer(cmdline_text):
                value = match.group(1)
                if value is None or value.lower() not in SYSTEMD_ZRAM_DISABLED_VALUES:
                    enabling_entries.append(f"{rel_path}: {match.group(0)!r}")

    assert not enabling_entries, (
        f"Expected no 'systemd.zram' kernel cmdline option enabling swap, found: {enabling_entries}"
    )
