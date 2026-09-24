# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# SPDX-License-Identifier: MIT
"""Container-specific validation tests."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


def test_no_kernel_modules(rootfs: Path) -> None:
    """Container images must not ship kernel modules."""
    for modules_dir in (
        rootfs / "lib" / "modules",
        rootfs / "usr" / "lib" / "modules",
    ):
        if modules_dir.exists():
            versions = list(modules_dir.iterdir())
            assert not versions, f"Container image has kernel modules under {modules_dir}: {[v.name for v in versions]}"
