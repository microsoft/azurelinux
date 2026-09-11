# SPDX-License-Identifier: MIT
"""Validate the busybox applet on the container-busybox workload image.

This image is genuinely minimal: config.sh routes busybox-workload to
config-container-base.sh in strip mode, which force-removes bash/dnf5/rpm
and autoremoves everything not on the profile's keep list. No real shell
binary ships in the final image -- only the busybox multi-call binary,
with `sh`/`sleep`/`echo` applet symlinks installed by that same script so
the shared runtime test harness (which needs a `sh` on PATH to exec into
the container, and `sleep infinity` to keep it alive) can still drive it.
"""

from __future__ import annotations

import pytest
from utils.container_runtime import ExecShell


def test_busybox_applet_runs(container_exec_shell: ExecShell) -> None:
    """The busybox multi-call binary must execute an applet successfully."""
    result = container_exec_shell("busybox echo hello-from-busybox", shell="sh")
    if result.exit_code != 0:
        pytest.fail(f"busybox echo failed: {result.output}")
    if "hello-from-busybox" not in result.output:
        pytest.fail(f"unexpected busybox echo output: {result.output}")


def test_busybox_default_command_shell_works(container_exec_shell: ExecShell) -> None:
    """The image's default command (``/bin/busybox sh``) must be usable directly."""
    result = container_exec_shell("/bin/busybox sh -c 'echo via-busybox-sh'", shell="sh")
    if result.exit_code != 0:
        pytest.fail(f"/bin/busybox sh failed: {result.output}")
    if "via-busybox-sh" not in result.output:
        pytest.fail(f"unexpected /bin/busybox sh output: {result.output}")
