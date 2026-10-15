# SPDX-License-Identifier: MIT
"""Check the WSL defaults in the assembled image."""

from __future__ import annotations

import configparser
from pathlib import Path

import pytest
from utils.extract import read_text_confined

_SYSTEM_UNIT_DIRS = ("etc/systemd/system", "run/systemd/system", "usr/lib/systemd/system")
_CONDITIONAL_UNITS = (
    "console-getty.service",
    "getty@.service",
    "systemd-vconsole-setup.service",
    "tmp.mount",
    "systemd-tmpfiles-setup-dev.service",
    "systemd-tmpfiles-setup-dev-early.service",
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
    assert not missing, f"Missing WSL packages: {sorted(missing)}"

    other_variants = {
        "azurelinux-release-cloud",
        "azurelinux-release-container",
        "azurelinux-release-identity-basic",
        "azurelinux-release-identity-cloud",
        "azurelinux-release-identity-container",
    }
    unexpected = installed_packages & other_variants
    assert not unexpected, f"Non-WSL release packages installed: {sorted(unexpected)}"


def test_wsl_registration(rootfs: Path) -> None:
    """Use a stable registration name and a real Azure Linux icon."""
    config = configparser.ConfigParser(interpolation=None)
    config.read_string(read_text_confined(rootfs, "etc/wsl-distribution.conf"))
    assert config["oobe"]["defaultName"] == "AzureLinux-4", (
        "WSL must register as AzureLinux-4, the name used by WSL's DistributionInfo.json entry"
    )
    assert config["shortcut"]["icon"] == "/usr/share/pixmaps/azurelinux-logo.ico", (
        "WSL must reference the Azure Linux icon"
    )

    icon = rootfs / "usr/share/pixmaps/azurelinux-logo.ico"
    assert not icon.is_symlink(), "The Azure Linux icon must not be a symlink"
    assert icon.is_file(), "The Azure Linux icon must be shipped as a real file"

    icon_header = b"\x00\x00\x01\x00"
    with icon.open("rb") as stream:
        assert stream.read(len(icon_header)) == icon_header, "The WSL icon is not a Windows ICO file"


@pytest.mark.parametrize("unit", _CONDITIONAL_UNITS)
def test_wsl_unit_condition(rootfs: Path, unit: str) -> None:
    """Skip WSL-conflicting units with a vendor drop-in, not a mask."""
    relative = f"usr/lib/systemd/system/{unit}.d/wsl-disable.conf"
    drop_in = rootfs / relative
    assert drop_in.is_file(), f"{unit} is missing its WSL drop-in at /{relative}"

    config = configparser.ConfigParser(interpolation=None)
    config.read_string(read_text_confined(rootfs, relative))
    assert config["Unit"].get("ConditionVirtualization") == "!wsl", (
        f"{unit} drop-in must set ConditionVirtualization=!wsl"
    )


def test_wsl_units_are_not_masked(rootfs: Path) -> None:
    """Leave /etc/systemd/system to the administrator; packages must not mask there."""
    etc_units = rootfs / "etc/systemd/system"
    masked = sorted(
        str(entry.relative_to(rootfs))
        for entry in etc_units.rglob("*")
        if entry.is_symlink() and entry.readlink() == Path("/dev/null")
    )
    assert not masked, f"Units masked under /etc/systemd/system: {masked}"


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
            assert "[Unit]" in contents, f"{unit} is masked or empty"
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
            assert link.readlink() != Path("/dev/null"), f"Masked tmpfiles dependency: {dependency}"
            assert "[Unit]" in read_text_confined(rootfs, f"{directory}/{dependency}"), (
                f"Invalid tmpfiles dependency: {dependency}"
            )
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
    assert expected in entries, "Missing the WSLg X11 symlink's dedicated tmpfiles entry"
