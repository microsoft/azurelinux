# SPDX-License-Identifier: MIT
"""File content parsers for image validation."""

from __future__ import annotations

import logging
import subprocess
from pathlib import Path

from .tools import NativeTool

logger = logging.getLogger(__name__)

RPM = NativeTool(
    name="rpm",
    package_hint="rpm",
    reason="query installed packages via rpm --root",
    when="always",
)


def parse_os_release(content: str) -> dict[str, str]:
    """Parse ``/etc/os-release`` KEY=VALUE format into a dict.

    Handles quoted and unquoted values per the os-release spec.
    """
    result: dict[str, str] = {}
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip()
        # Strip matching quotes
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
            value = value[1:-1]
        result[key] = value
    logger.debug("Parsed os-release: %d keys", len(result))
    return result


def query_rpm_packages(rootfs: Path) -> set[str]:
    """Query installed RPM packages via ``rpm --root``.

    Raises :class:`RuntimeError` if the query fails (e.g. missing rpmdb).
    """
    cmd = [RPM.name, "--root", str(rootfs), "-qa", "--qf", "%{NAME}\n"]
    logger.debug("Running: %s", " ".join(cmd))
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"rpm query failed (rc={result.returncode}): {result.stderr.strip()}"
        )
    pkgs = {line.strip() for line in result.stdout.splitlines() if line.strip()}
    logger.debug("rpm query returned %d packages", len(pkgs))
    return pkgs
