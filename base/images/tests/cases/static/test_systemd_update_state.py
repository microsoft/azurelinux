# SPDX-License-Identifier: MIT
"""Validate that cloud VM images ship with finalized systemd update state."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pathlib import Path

pytestmark = pytest.mark.require_capability("machine-bootable")
GENERATED_STATE_PATHS = (
    "etc/ld.so.cache",
    "etc/udev/hwdb.bin",
    "var/lib/systemd/catalog/database",
)


def test_systemd_update_state_is_finalized(rootfs: Path, image_name: str | None) -> None:
    """Prevent first boot from rebuilding state already generated in the image."""
    if image_name != "marketplace-gen2":
        pytest.skip("systemd update state is finalized only for marketplace-gen2")

    usr_mtime_ns = (rootfs / "usr").stat().st_mtime_ns
    for relative_path in ("etc/.updated", "var/.updated"):
        marker = rootfs / relative_path
        assert marker.is_file(), f"Missing systemd update marker: /{relative_path}"
        marker_stat = marker.stat()
        assert marker_stat.st_size > 0, f"Empty systemd update marker: /{relative_path}"
        assert marker_stat.st_mtime_ns == usr_mtime_ns, (
            f"/{relative_path} does not match /usr and will trigger first-boot updates"
        )

    for relative_path in GENERATED_STATE_PATHS:
        generated_state = rootfs / relative_path
        assert generated_state.is_file(), f"Missing generated state: /{relative_path}"
        generated_state_stat = generated_state.stat()
        assert generated_state_stat.st_size > 0, f"Empty generated state: /{relative_path}"
        assert generated_state_stat.st_mtime_ns >= usr_mtime_ns, (
            f"/{relative_path} predates the finalized /usr tree"
        )
