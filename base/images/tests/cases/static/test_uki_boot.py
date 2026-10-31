# SPDX-License-Identifier: MIT
"""Validate the CVM boot chain and its package-owned ESP.

On first boot, when no Boot#### entry exists yet, firmware starts shim via
the removable-media path EFI/BOOT/BOOTX64.EFI. When started from that path
and EFI/BOOT/fbx64.efi exists, shim runs that fallback loader. It reads
EFI/azurelinux/BOOTX64.CSV, creates a Boot#### entry for
EFI/azurelinux/shimx64.efi, and resets if a TPM is present. Later boots use
the registered entry directly. Shim then loads EFI/azurelinux/grubx64.efi
(systemd-boot), which uses loader/loader.conf to boot
EFI/Linux/azurelinux-<version>.efi (the UKI).

The shim-x64 RPM payload owns EFI/BOOT/{BOOTX64.EFI,fbx64.efi} and
EFI/azurelinux/{shimx64.efi,mmx64.efi,shim.efi,BOOTX64.CSV}. The
azurelinux-uki-boot RPM payload owns loader/loader.conf; its file trigger
copies systemd-boot to EFI/azurelinux/grubx64.efi (%ghost-owned).
Kernel-install (run by kernel-uki-virt's scriptlet) creates the versioned UKI.

RPM-owned ESP files can be updated or removed by dnf. Cvmutils predicts PCR
4/7 by discovering this chain from BOOTX64.CSV, grubx64.efi, and
EFI/Linux/*.efi, including any addons; stray paths or extra boot entries
would change the predicted chain.
"""

from __future__ import annotations

import csv
import hashlib
import io
import stat
import subprocess
from typing import TYPE_CHECKING

import pytest
from utils.extract import read_bytes_confined, read_text_confined, resolve_path_confined
from utils.parsers import RPM

if TYPE_CHECKING:
    from pathlib import Path

pytestmark = pytest.mark.require_capability("cvm")

CSV_MIN_FIELDS = 3


def _entry_token(rootfs: Path) -> str:
    token = read_text_confined(rootfs, "etc/kernel/entry-token").strip()
    assert token, "Kernel entry token must not be empty"
    assert "/" not in token, f"Invalid kernel entry token: {token!r}"
    return token


def _uki_files(rootfs: Path) -> list[Path]:
    uki_dir = resolve_path_confined(rootfs, "boot/efi/EFI/Linux")
    assert uki_dir.is_dir(), "Missing Type #2 UKI directory /boot/efi/EFI/Linux"
    # lstat avoids following a symlink masquerading as a regular UKI.
    return sorted(path for path in uki_dir.iterdir() if stat.S_ISREG(path.lstat().st_mode) and path.suffix == ".efi")


def test_esp_regular_files_are_rpm_owned_except_kernel_install_uki(rootfs: Path) -> None:
    """Require RPM ownership of every ESP file except the versioned UKI.

    Unowned files cannot be updated or removed by dnf; kernel-install's UKI
    is the only expected unowned artifact.
    """
    esp = resolve_path_confined(rootfs, "boot/efi")
    assert esp.is_dir(), "Missing ESP at /boot/efi"
    token = _entry_token(rootfs)
    versions = {
        path.name
        for path in resolve_path_confined(rootfs, "usr/lib/modules").iterdir()
        if stat.S_ISDIR(path.lstat().st_mode)
    }
    # kernel-install names one unowned UKI per installed kernel version.
    managed = {f"boot/efi/EFI/Linux/{token}-{version}.efi" for version in versions}
    unowned: list[str] = []
    for path in sorted(esp.rglob("*")):
        # Inspect the directory entry, not a symlink target outside the ESP.
        if not stat.S_ISREG(path.lstat().st_mode):
            continue
        relative = path.relative_to(rootfs).as_posix()
        resolved = resolve_path_confined(rootfs, relative)
        # Reject paths whose symlinks resolve somewhere other than the file we checked.
        assert resolved == path, f"Unexpected ESP path resolution for {relative}: {resolved}"
        result = subprocess.run(
            [RPM.name, "--root", str(rootfs), "-qf", f"/{relative}"],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0 and relative not in managed:
            unowned.append(f"/{relative}: {result.stderr.strip() or result.stdout.strip()}")
    assert not unowned, f"ESP has unexpected files without RPM ownership: {unowned}"


def test_shim_second_stage_is_systemd_boot(rootfs: Path) -> None:
    """Require shim's own-directory grubx64.efi to equal systemd-boot.

    A stale second-stage copy could boot an old or unsigned loader after an
    update; EFI/BOOT/grubx64.efi is unused by this fallback chain and would
    become another stale copy.
    """
    second_stage = "boot/efi/EFI/azurelinux/grubx64.efi"
    installed_boot = "usr/lib/systemd/boot/efi/systemd-bootx64.efi"
    assert resolve_path_confined(rootfs, second_stage).is_file(), f"Missing shim second stage /{second_stage}"
    assert (
        hashlib.sha256(read_bytes_confined(rootfs, second_stage)).digest()
        == hashlib.sha256(read_bytes_confined(rootfs, installed_boot)).digest()
    ), f"/{second_stage} differs from /{installed_boot}"
    assert not resolve_path_confined(rootfs, "boot/efi/EFI/BOOT/grubx64.efi").exists(), (
        "Unexpected fallback /boot/efi/EFI/BOOT/grubx64.efi"
    )


def test_shim_fallback_csv_has_no_uki_override(rootfs: Path) -> None:
    """Require the fallback CSV to register shim with no load options.

    With no load options, the registered shim entry chain-loads grubx64.efi
    (systemd-boot) rather than a UKI directly; cvmutils parses this field to
    predict the chain.
    """
    csv_path = "boot/efi/EFI/azurelinux/BOOTX64.CSV"
    # Shim fallback CSV is UTF-16LE and may begin with a BOM.
    content = read_bytes_confined(rootfs, csv_path).decode("utf-16-le").lstrip("\ufeff")
    entries = list(csv.reader(io.StringIO(content)))
    assert entries, f"/{csv_path} has no fallback entries"
    for entry in entries:
        assert len(entry) >= CSV_MIN_FIELDS, f"/{csv_path} has incomplete fallback entry: {entry!r}"
        assert entry[0].lower() == "shimx64.efi", f"/{csv_path} must register shimx64.efi: {entry!r}"
        assert entry[2] == "", f"/{csv_path} must not override shim load options: {entry!r}"


def test_single_uki_matches_installed_kernel_without_addons(rootfs: Path) -> None:
    """Require exactly one installed-kernel UKI and no addons.

    Every EFI/Linux/*.efi is a boot entry and a separate PCR-predicted
    chain; addons also change PCR 4 and the kernel command line.
    """
    ukis = _uki_files(rootfs)
    assert len(ukis) == 1, f"Expected exactly one Type #2 UKI, found: {[path.name for path in ukis]}"
    modules = resolve_path_confined(rootfs, "usr/lib/modules")
    versions = sorted(
        path.name
        for path in modules.iterdir()
        if stat.S_ISDIR(path.lstat().st_mode)
        and resolve_path_confined(rootfs, f"usr/lib/modules/{path.name}/vmlinuz-virt.efi").is_file()
    )
    assert len(versions) == 1, f"Expected exactly one installed virt UKI version, found: {versions}"
    expected_name = f"{_entry_token(rootfs)}-{versions[0]}.efi"
    uki = ukis[0]
    assert uki.name == expected_name, f"Type #2 UKI must be {expected_name}, found {uki.name}"
    assert read_bytes_confined(rootfs, uki.relative_to(rootfs).as_posix()) == read_bytes_confined(
        rootfs, f"usr/lib/modules/{versions[0]}/vmlinuz-virt.efi"
    ), f"/{uki.relative_to(rootfs)} differs from installed vmlinuz-virt.efi"
    assert not resolve_path_confined(rootfs, "boot/efi/loader/addons").exists(), "Global UKI addons must not exist"
    assert not resolve_path_confined(rootfs, f"boot/efi/EFI/Linux/{uki.name}.extra.d").exists(), (
        f"Per-UKI addons must not exist for {uki.name}"
    )


def test_loader_default_matches_entry_token(rootfs: Path) -> None:
    """Match the loader default to kernel-install's ``<token>-*`` UKI name.

    A mismatched default could select the wrong entry or none at all.
    """
    lines = read_text_confined(rootfs, "boot/efi/loader/loader.conf").splitlines()
    defaults = [
        fields[1] for line in lines if (fields := line.split(maxsplit=1)) and fields[0] == "default" and len(fields) > 1
    ]
    expected = f"{_entry_token(rootfs)}-*"
    assert defaults == [expected], f"Loader default must be {expected!r}, found {defaults}"


def test_no_kernel_install_output_outside_esp(rootfs: Path) -> None:
    """Reject kernel-install output under /boot/EFI outside the ESP.

    Such a stray UKI means the BOOT_ROOT drop-in was missing or ignored;
    it would remain in the root filesystem without being cleaned up.
    """
    assert not resolve_path_confined(rootfs, "boot/EFI").exists(), "Stray kernel-install output at /boot/EFI"


def test_no_conventional_boot_packages(installed_packages: set[str]) -> None:
    """Exclude packages that conflict with or bypass the UKI boot chain.

    grub2-efi-x64 owns the same grubx64.efi path; uki-direct adds firmware
    entries that bypass systemd-boot; a conventional kernel adds non-UKI
    boot entries.
    """
    forbidden = sorted(
        pkg for pkg in installed_packages if pkg.startswith("grub2") or pkg in {"uki-direct", "kernel", "kernel-core"}
    )
    assert not forbidden, f"Conventional boot packages installed in CVM image: {forbidden}"
