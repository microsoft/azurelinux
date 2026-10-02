# SPDX-License-Identifier: MIT
"""Validate kernel FIPS boot configuration."""

from __future__ import annotations

from pathlib import Path

import pytest


@pytest.mark.require_capability("machine-bootable")
def test_kernel_fips_matches_image_variant(
    boot_entry_kernel_options: dict[Path, list[str]],
    image_name: str | None,
) -> None:
    assert image_name is not None, "Image name is required to identify FIPS variants"
    expected_fips_options = ["fips=1"] if image_name.endswith("-fips") else []

    for entry, options in boot_entry_kernel_options.items():
        fips_options = [
            option for option in options if option.partition("=")[0] == "fips"
        ]
        assert fips_options == expected_fips_options, (
            f"Kernel FIPS options do not match image variant {image_name!r} "
            f"in {entry}"
        )
