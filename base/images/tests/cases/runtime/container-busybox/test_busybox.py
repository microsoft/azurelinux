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

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable

    from python_on_whales import DockerClient
    from utils.container_runtime import ContainerExecResult


def test_busybox_image_config_cmd(podman_client: DockerClient, container_image_ref: str) -> None:
    """The image must start the BusyBox shell by default."""
    cmd = podman_client.image.inspect(container_image_ref).config.cmd
    assert cmd == ["/usr/sbin/busybox", "sh"], f"unexpected Config.Cmd: {cmd!r}"


def test_busybox_applet_runs(container_exec: Callable[[list[str]], ContainerExecResult]) -> None:
    """The busybox multi-call binary must execute an applet successfully."""
    result = container_exec(["busybox", "echo", "hello-from-busybox"])
    assert result.exit_code == 0, f"busybox echo failed: {result.output}"
    assert "hello-from-busybox" in result.output, f"unexpected busybox echo output: {result.output}"


def test_busybox_default_command_shell_works(container_exec: Callable[[list[str]], ContainerExecResult]) -> None:
    """The image's default command (``/bin/busybox sh``) must be usable directly."""
    result = container_exec(["/bin/busybox", "sh", "-c", "echo via-busybox-sh"])
    assert result.exit_code == 0, f"/bin/busybox sh failed: {result.output}"
    assert "via-busybox-sh" in result.output, f"unexpected /bin/busybox sh output: {result.output}"
