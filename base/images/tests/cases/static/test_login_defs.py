# SPDX-License-Identifier: MIT
"""Validate account defaults configured in /etc/login.defs."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

import pytest
from utils.extract import read_text_confined

if TYPE_CHECKING:
    from pathlib import Path

pytestmark = pytest.mark.require_capability("runtime-package-management")

ACTIVE_UMASK_RE = re.compile(r"^[ \t]*UMASK[ \t]+(\S+)", re.MULTILINE)
RESTRICTIVE_UMASK_RE = re.compile(r"0[0-7]?[2367]7")


def test_login_defs_has_restrictive_default_umask(
    rootfs: Path,
    installed_packages: set[str],
) -> None:
    """The login.defs UMASK must be 027 or more restrictive."""
    if "shadow-utils" not in installed_packages:
        pytest.skip("Image does not ship shadow-utils")

    login_defs_path = rootfs / "etc" / "login.defs"
    assert login_defs_path.is_file(), "shadow-utils is installed but /etc/login.defs is missing"

    login_defs = read_text_confined(rootfs, "etc/login.defs")
    umasks = ACTIVE_UMASK_RE.findall(login_defs)

    assert len(umasks) == 1, (
        "Expected exactly one active UMASK setting in /etc/login.defs; "
        f"found {len(umasks)}: {umasks}"
    )

    umask = umasks[0]
    assert RESTRICTIVE_UMASK_RE.fullmatch(umask), (
        "The active UMASK in /etc/login.defs must be 027 or more restrictive; "
        f"found: {umask!r}"
    )
