# SPDX-License-Identifier: MIT
"""Validate Microsoft build of Go telemetry policy in first-party VM images."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pathlib import Path


def test_golang_telemetry_policy_installed(
    installed_packages: set[str],
    rootfs: Path,
) -> None:
    """First-party images carry the policy without requiring Go itself."""
    assert "golang-msft-telemetry-policy" in installed_packages
    helper = rootfs / "usr/libexec/set-msft-go-telemetry"
    assert helper.is_file(), "Microsoft build of Go telemetry policy helper is missing"
    assert helper.stat().st_mode & 0o111, "Telemetry policy helper is not executable"


def test_golang_telemetry_default(
    installed_packages: set[str],
    rootfs: Path,
) -> None:
    """An installed Microsoft build of Go has telemetry enabled by default."""
    go_env = rootfs / "usr/lib/golang/go.env"
    if "golang-bin" not in installed_packages:
        pytest.skip("Go is not preinstalled; the policy applies when Go is installed")
    assert go_env.is_file(), "The installed Go toolchain is missing go.env"
    settings = [
        line
        for line in go_env.read_text().splitlines()
        if line.startswith("MS_GOTOOLCHAIN_TELEMETRY_ENABLED=")
    ]
    assert settings == ["MS_GOTOOLCHAIN_TELEMETRY_ENABLED=1"], (
        f"Microsoft build of Go telemetry must default to enabled, found {settings}"
    )
