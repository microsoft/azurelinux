# Copyright (c) 2026 Microsoft Corporation.
# SPDX-License-Identifier: MIT
# ruff: noqa: INP001 - Image-family directories are discovered by pytest, not imported as packages.
"""Check the WSL defaults in the assembled image, not just RPM presets."""

from __future__ import annotations

import configparser
import fnmatch
from pathlib import Path

import pytest
from utils.extract import read_text_confined

_SYSTEM_UNIT_DIRS = ("etc/systemd/system", "run/systemd/system", "usr/lib/systemd/system")
_MASKED_UNITS = (
    "console-getty.service",
    "systemd-vconsole-setup.service",
    "tmp.mount",
    "systemd-tmpfiles-setup-dev.service",
    "systemd-tmpfiles-setup-dev-early.service",
)
_DISABLED_UNITS = (
    "console-getty.service",
    "getty@*.service",
    "systemd-networkd.service",
    "systemd-networkd.socket",
    "systemd-networkd-varlink.socket",
    "systemd-networkd-wait-online.service",
    "systemd-resolved.service",
    "systemd-resolved-monitor.socket",
    "systemd-resolved-varlink.socket",
)


def test_wsl_release_packages(installed_packages: set[str]) -> None:
    """Install the WSL identity without pulling in another release variant."""
    required = {"azurelinux-release-wsl", "azurelinux-release-identity-wsl", "wsl-setup"}
    missing = required - installed_packages
    if missing:
        pytest.fail(f"Missing WSL packages: {sorted(missing)}")
    other_variants = {
        "azurelinux-release-cloud",
        "azurelinux-release-container",
        "azurelinux-release-identity-basic",
        "azurelinux-release-identity-cloud",
        "azurelinux-release-identity-container",
    }
    unexpected = installed_packages & other_variants
    if unexpected:
        pytest.fail(f"Non-WSL release packages installed: {sorted(unexpected)}")


def test_wsl_registration(rootfs: Path) -> None:
    """Use a stable registration name and a real Azure Linux icon."""
    config = configparser.ConfigParser(interpolation=None)
    config.read_string(read_text_confined(rootfs, "etc/wsl-distribution.conf"))
    if config["oobe"]["defaultName"] != "AzureLinux-4.0":
        pytest.fail("WSL must register as AzureLinux-4.0, without a prerelease suffix")
    if config["shortcut"]["icon"] != "/usr/share/pixmaps/azurelinux-logo.ico":
        pytest.fail("WSL must reference the Azure Linux icon")
    icon = rootfs / "usr/share/pixmaps/azurelinux-logo.ico"
    if icon.is_symlink() or not icon.is_file():
        pytest.fail("The Azure Linux icon must be shipped as a real file")
    icon_header = b"\x00\x00\x01\x00"
    with icon.open("rb") as stream:
        if stream.read(len(icon_header)) != icon_header:
            pytest.fail("The WSL icon is not a Windows ICO file")


@pytest.mark.parametrize("unit", _MASKED_UNITS)
def test_wsl_unit_mask(rootfs: Path, unit: str) -> None:
    """Block static and generator-activated units even without preset support."""
    mask = rootfs / "etc/systemd/system" / unit
    if not mask.is_symlink() or mask.readlink() != Path("/dev/null"):
        pytest.fail(f"{unit} must be masked in the WSL image")


@pytest.mark.parametrize("pattern", _DISABLED_UNITS)
def test_wsl_units_not_enabled(rootfs: Path, pattern: str) -> None:
    """Check actual dependency links left by the image's RPM transactions."""
    enabled = [
        str(link.relative_to(rootfs))
        for directory in _SYSTEM_UNIT_DIRS
        for suffix in ("wants", "requires")
        for link in (rootfs / directory).glob(f"*.{suffix}/*")
        if fnmatch.fnmatchcase(link.name, pattern)
    ]
    if enabled:
        pytest.fail(f"WSL-discouraged units are enabled: {sorted(enabled)}")


@pytest.mark.parametrize(
    "unit",
    [
        "systemd-tmpfiles-setup.service",
        "systemd-tmpfiles-clean.service",
        "systemd-tmpfiles-clean.timer",
    ],
)
def test_wsl_tmpfiles_available(rootfs: Path, unit: str) -> None:
    """Keep WSLg link creation and periodic temporary-file cleanup available."""
    for directory in _SYSTEM_UNIT_DIRS:
        candidate = rootfs / directory / unit
        if candidate.is_symlink() or candidate.exists():
            contents = read_text_confined(rootfs, f"{directory}/{unit}")
            if "[Unit]" not in contents:
                pytest.fail(f"{unit} is masked or empty")
            return
    pytest.fail(f"{unit} is missing from the WSL image")


@pytest.mark.parametrize(
    "dependency",
    [
        "sysinit.target.wants/systemd-tmpfiles-setup.service",
        "timers.target.wants/systemd-tmpfiles-clean.timer",
    ],
)
def test_wsl_tmpfiles_scheduled(rootfs: Path, dependency: str) -> None:
    """Preserve boot-time setup and the cleanup timer's dependency links."""
    for directory in _SYSTEM_UNIT_DIRS:
        link = rootfs / directory / dependency
        if link.is_symlink():
            if link.readlink() == Path("/dev/null"):
                pytest.fail(f"Masked tmpfiles dependency: {dependency}")
            if "[Unit]" not in read_text_confined(rootfs, f"{directory}/{dependency}"):
                pytest.fail(f"Invalid tmpfiles dependency: {dependency}")
            return
    pytest.fail(f"Missing tmpfiles dependency: {dependency}")


def test_wslg_x11_tmpfiles_entry(rootfs: Path) -> None:
    """Give the X11 socket link its own entry so parent-directory cleanup skips it."""
    entries = [
        line.split()
        for line in read_text_confined(rootfs, "usr/lib/tmpfiles.d/wsl-setup.conf").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    expected = [
        "L+",
        "/tmp/.X11-unix",  # noqa: S108 - Match image configuration; do not create a host temporary path.
        "-",
        "-",
        "-",
        "-",
        "/mnt/wslg/.X11-unix",
    ]
    if expected not in entries:
        pytest.fail("Missing the WSLg X11 symlink's dedicated tmpfiles entry")
