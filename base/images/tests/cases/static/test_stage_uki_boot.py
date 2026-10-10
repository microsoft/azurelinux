"""Isolated fixtures for the shared UKI boot staging hook."""

from __future__ import annotations

import os
import stat
import subprocess
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from collections.abc import Iterator

IMAGES = Path(__file__).resolve().parents[3]
WORK = IMAGES.parents[1] / "base/build/work"


def put(root: Path, path: str, data: bytes) -> Path:
    destination = root / path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(data)
    return destination


@pytest.fixture
def root() -> Iterator[Path]:
    WORK.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=WORK) as sandbox:
        root = Path(sandbox)
        put(root, "etc/kernel/entry-token", b"azurelinux\n")
        put(root, "usr/share/shim/16.1/x64/shimx64.efi", b"unsigned shim")
        put(root, "usr/lib/systemd/boot/efi/systemd-bootx64.efi", b"unsigned boot")
        put(root, "lib/modules/6.9/vmlinuz-virt.efi", b"older UKI")
        put(root, "lib/modules/6.10/vmlinuz-virt.efi", b"newest UKI")
        yield root


def run_hook(root: Path, *, success: bool = True) -> None:
    result = subprocess.run(
        ["bash", str(IMAGES / "UkiBootCore/image/stage-uki-boot.sh")],
        env={**os.environ, "UKI_ROOT": str(root)},
        capture_output=True,
        text=True,
        check=False,
    )
    if success and result.returncode != 0:
        pytest.fail(result.stderr)
    if not success:
        if result.returncode == 0 or "ERROR:" not in result.stderr:
            pytest.fail(f"unexpected hook result: {result}")
        if (root / "boot/efi/EFI/BOOT/BOOTX64.EFI").exists():
            pytest.fail("hook staged boot files after invalid inputs")


def test_stages_shim_boot_and_newest_uki(root: Path) -> None:
    run_hook(root)
    esp = root / "boot/efi"
    expected = {
        "EFI/BOOT/BOOTX64.EFI": b"unsigned shim",
        "EFI/BOOT/grubx64.efi": b"unsigned boot",
        "EFI/Linux/azurelinux-6.10.efi": b"newest UKI",
        "loader/loader.conf": b"default azurelinux-*\ntimeout 1\n",
    }
    for name, content in expected.items():
        path = esp / name
        if path.read_bytes() != content or stat.S_IMODE(path.stat().st_mode) != 0o644:
            pytest.fail(f"unexpected contents or mode for {name}")
    if (esp / "EFI/Linux/azurelinux-6.9.efi").exists():
        pytest.fail("older UKI was staged")


@pytest.mark.parametrize("content", [b"azurelinux", b"azurelinux\x00", b"azurelinux\n\n", b"other\n"])
def test_rejects_invalid_token(root: Path, content: bytes) -> None:
    (root / "etc/kernel/entry-token").write_bytes(content)
    run_hook(root, success=False)


def test_rejects_missing_token(root: Path) -> None:
    (root / "etc/kernel/entry-token").unlink()
    run_hook(root, success=False)


def test_rejects_missing_multiple_or_unsupported_boot_payloads(root: Path) -> None:
    boot = root / "usr/lib/systemd/boot/efi/systemd-bootx64.efi"
    boot.unlink()
    run_hook(root, success=False)
    put(root, "usr/lib/systemd/boot/efi/systemd-bootaa64.efi", b"other arch")
    run_hook(root, success=False)
    put(root, "usr/lib/systemd/boot/efi/systemd-bootx64.efi", b"unsigned boot")
    run_hook(root, success=False)


def test_accepts_symlinked_shim_version_directory(root: Path) -> None:
    (root / "usr/share/shim/16.1").rename(root / "usr/share/shim/15.8-4.azl4")
    (root / "usr/share/shim/15.8-2").symlink_to("15.8-4.azl4", target_is_directory=True)
    run_hook(root)
    if (root / "boot/efi/EFI/BOOT/BOOTX64.EFI").read_bytes() != b"unsigned shim":
        pytest.fail("hook did not stage the shim payload")


def test_rejects_missing_shim(root: Path) -> None:
    shim = root / "usr/share/shim/16.1/x64/shimx64.efi"
    shim.unlink()
    run_hook(root, success=False)


def test_rejects_distinct_shim_payloads(root: Path) -> None:
    (root / "usr/share/shim/16.0").symlink_to("16.1", target_is_directory=True)
    put(root, "usr/share/shim/16.2/x64/shimx64.efi", b"other shim")
    run_hook(root, success=False)


def test_rejects_missing_uki(root: Path) -> None:
    for uki in (root / "lib/modules").glob("*/vmlinuz-virt.efi"):
        uki.unlink()
    run_hook(root, success=False)
