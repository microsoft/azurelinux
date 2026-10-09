# SPDX-License-Identifier: MIT
"""File content parsers for image validation."""

from __future__ import annotations

import logging
import shlex
import subprocess
from typing import TYPE_CHECKING

from .tools import NativeTool

if TYPE_CHECKING:
    from pathlib import Path

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
    for raw_line in content.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip()
        # Strip matching quotes
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):  # noqa: PLR2004 - matching quotes require two characters
            value = value[1:-1]
        result[key] = value
    logger.debug("Parsed os-release: %d keys", len(result))
    return result


def parse_boot_entry_kernel_options(
    option_lines_by_entry: dict[Path, list[str]],
) -> dict[Path, list[str]]:
    """Parse one literal kernel option line from each BLS boot entry."""
    if not option_lines_by_entry:
        raise ValueError("no BLS boot loader entries found")

    options_by_entry: dict[Path, list[str]] = {}
    for entry, option_lines in option_lines_by_entry.items():
        if len(option_lines) != 1:
            raise ValueError(
                f"expected exactly one options line in {entry}, "
                f"found {len(option_lines)}"
            )
        try:
            options = shlex.split(option_lines[0])
        except ValueError as exc:
            raise ValueError(
                f"failed to parse boot loader options in {entry}: {exc}"
            ) from exc
        if not options:
            raise ValueError(f"boot loader options are empty in {entry}")
        indirections = [option for option in options if option.startswith("$")]
        if indirections:
            raise ValueError(
                f"boot loader option indirection is not supported in {entry}: "
                f"{indirections}. This is likely a test issue."
            )
        options_by_entry[entry] = options
    return options_by_entry


def query_rpm_package_sizes(rootfs: Path) -> dict[str, int]:
    """Query installed RPM package on-disk sizes via ``rpm --root``.

    Returns a mapping of package name to total installed size in bytes (the
    RPM ``%{SIZE}`` header). ``%{NAME}`` is not unique — install-only
    packages (e.g. the kernel) can be present at multiple versions — so
    sizes for repeated names are summed rather than overwritten.

    Raises:
        RuntimeError: If the ``rpm`` query fails (e.g. missing rpmdb) or
            returns a non-integer ``%{SIZE}`` (incomplete data would
            silently undercount the footprint).
    """
    cmd = [RPM.name, "--root", str(rootfs), "-qa", "--qf", "%{NAME} %{SIZE}\n"]
    logger.debug("Running: %s", " ".join(cmd))
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"rpm size query failed (rc={result.returncode}): {result.stderr.strip()}")
    sizes: dict[str, int] = {}
    for raw_line in result.stdout.splitlines():
        entry = raw_line.strip()
        if not entry:
            continue
        name, separator, size_str = entry.rpartition(" ")
        if not separator or not name or not size_str:
            raise RuntimeError(f"unexpected rpm size entry: {entry!r}")
        try:
            size = int(size_str)
        except ValueError as exc:
            raise RuntimeError(f"unexpected rpm size for {name}: {size_str!r}") from exc
        sizes[name] = sizes.get(name, 0) + size
    logger.debug("rpm size query returned %d package names", len(sizes))
    return sizes
