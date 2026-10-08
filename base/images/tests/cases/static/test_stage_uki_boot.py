"""Isolated fixtures for the shared UKI boot staging hook.

Fixture version strings are deliberately synthetic. They exercise discovery,
version ordering, and symlink handling without tracking package releases.
"""

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
EXPECTED_FILE_MODE = 0o644
OLDER_KERNEL_VERSION = "6.9"
NEWER_KERNEL_VERSION = "6.10"
SHIM_VERSION = "16.1"


def put(root: Path, path: str, data: bytes) -> Path:
    """Write fixture data below the synthetic image root."""
    destination = root / path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(data)
    return destination


@pytest.fixture
def root() -> Iterator[Path]:
    """Create a minimal image root containing UKI boot inputs."""
    WORK.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=WORK) as sandbox:
        root = Path(sandbox)
        put(root, "etc/kernel/entry-token", b"azurelinux\n")
        put(root, f"usr/share/shim/{SHIM_VERSION}/x64/shimx64.efi", b"unsigned shim")
        put(root, "usr/lib/systemd/boot/efi/systemd-bootx64.efi", b"unsigned boot")
        put(root, f"lib/modules/{OLDER_KERNEL_VERSION}/vmlinuz-virt.efi", b"older UKI")
        put(root, f"lib/modules/{NEWER_KERNEL_VERSION}/vmlinuz-virt.efi", b"newest UKI")
        yield root


def run_hook(root: Path, *, success: bool = True) -> None:
    """Run the UKI staging hook and verify its expected outcome."""
    result = subprocess.run(
        ["bash", str(IMAGES / "UkiBootCore/image/stage-uki-boot.sh")],
        env={**os.environ, "UKI_ROOT": str(root)},
        capture_output=True,
        text=True,
        check=False,
    )
    if success:
        assert result.returncode == 0, result.stderr
    else:
        assert result.returncode != 0, f"hook unexpectedly succeeded: {result}"
        assert "ERROR:" in result.stderr, f"unexpected hook error: {result}"
        assert not (root / "boot/efi/EFI/BOOT/BOOTX64.EFI").exists(), (
            "hook staged boot files after invalid inputs"
        )


def test_stages_shim_boot_and_newest_uki(root: Path) -> None:
    """Stage shim, systemd-boot, and the newest UKI."""
    run_hook(root)
    esp = root / "boot/efi"
    expected = {
        "EFI/BOOT/BOOTX64.EFI": b"unsigned shim",
        "EFI/BOOT/grubx64.efi": b"unsigned boot",
        f"EFI/Linux/azurelinux-{NEWER_KERNEL_VERSION}.efi": b"newest UKI",
        "loader/loader.conf": b"default azurelinux-*\ntimeout 1\n",
    }
    for name, content in expected.items():
        path = esp / name
        assert path.read_bytes() == content, f"unexpected contents for {name}"
        assert stat.S_IMODE(path.stat().st_mode) == EXPECTED_FILE_MODE, (
            f"unexpected mode for {name}"
        )
    assert not (esp / f"EFI/Linux/azurelinux-{OLDER_KERNEL_VERSION}.efi").exists(), "older UKI was staged"


@pytest.mark.parametrize("content", [b"azurelinux", b"azurelinux\x00", b"azurelinux\n\n", b"other\n"])
def test_rejects_invalid_token(root: Path, content: bytes) -> None:
    """Reject malformed or unexpected kernel entry tokens."""
    (root / "etc/kernel/entry-token").write_bytes(content)
    run_hook(root, success=False)


def test_rejects_missing_token(root: Path) -> None:
    """Reject an image root without a kernel entry token."""
    (root / "etc/kernel/entry-token").unlink()
    run_hook(root, success=False)


def test_rejects_missing_multiple_or_unsupported_boot_payloads(root: Path) -> None:
    """Reject missing, multiple, or unsupported systemd-boot payloads."""
    boot = root / "usr/lib/systemd/boot/efi/systemd-bootx64.efi"
    boot.unlink()
    run_hook(root, success=False)
    put(root, "usr/lib/systemd/boot/efi/systemd-bootaa64.efi", b"other arch")
    run_hook(root, success=False)
    put(root, "usr/lib/systemd/boot/efi/systemd-bootx64.efi", b"unsigned boot")
    run_hook(root, success=False)


def test_accepts_symlinked_shim_version_directory(root: Path) -> None:
    """Accept package-version aliases that resolve to one shim payload."""
    (root / f"usr/share/shim/{SHIM_VERSION}").rename(root / "usr/share/shim/15.8-4.azl4")
    (root / "usr/share/shim/15.8-2").symlink_to("15.8-4.azl4", target_is_directory=True)
    run_hook(root)
    assert (root / "boot/efi/EFI/BOOT/BOOTX64.EFI").read_bytes() == b"unsigned shim", (
        "hook did not stage the shim payload"
    )


def test_rejects_missing_shim(root: Path) -> None:
    """Reject an image root without the required shim payload."""
    shim = root / f"usr/share/shim/{SHIM_VERSION}/x64/shimx64.efi"
    shim.unlink()
    run_hook(root, success=False)


def test_rejects_distinct_shim_payloads(root: Path) -> None:
    """Reject multiple distinct shim payloads."""
    (root / "usr/share/shim/16.0").symlink_to(SHIM_VERSION, target_is_directory=True)
    put(root, "usr/share/shim/16.2/x64/shimx64.efi", b"other shim")
    run_hook(root, success=False)


def test_rejects_missing_uki(root: Path) -> None:
    """Reject an image root without a packaged virt UKI."""
    for uki in (root / "lib/modules").glob("*/vmlinuz-virt.efi"):
        uki.unlink()
    run_hook(root, success=False)
