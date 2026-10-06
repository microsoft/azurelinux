# SPDX-License-Identifier: MIT
"""Validate kernel FIPS boot configuration."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from utils.parsers import parse_boot_entry_kernel_options

if TYPE_CHECKING:
    from pathlib import Path


@pytest.mark.require_capability("machine-bootable")
def test_kernel_fips_matches_image_variant(
    boot_entry_option_lines: dict[Path, list[str]],
    capabilities: set[str],
) -> None:
    expected_fips_options = ["fips=1"] if "fips-enabled" in capabilities else []
    options_by_entry = parse_boot_entry_kernel_options(boot_entry_option_lines)

    for entry, options in options_by_entry.items():
        fips_options = [
            option for option in options if option.partition("=")[0] == "fips"
        ]
        assert fips_options == expected_fips_options, (
            "Kernel FIPS options do not match the image's capabilities "
            f"in {entry}"
        )
