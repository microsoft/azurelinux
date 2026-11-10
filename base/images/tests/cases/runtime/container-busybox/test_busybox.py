# SPDX-License-Identifier: MIT
"""Validate BusyBox applets on the container-busybox workload image.

This image is genuinely minimal: config.sh routes busybox-workload to
config-container-base.sh in strip mode, which force-removes bash/dnf5/rpm
and autoremoves everything not on the profile's keep list. No real shell
binary ships in the final image -- only the busybox multi-call binary,
with symlinks for all enabled applets installed in /bin by that same script.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

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


def test_busybox_applet_symlinks(container_exec: Callable[[list[str]], ContainerExecResult]) -> None:
    """Every enabled applet must have a /bin symlink to the shipped BusyBox binary."""
    result = container_exec([
        "/bin/busybox", "sh", "-ec",
        (
            'for applet in $(/bin/busybox --list); do '
            'link="/bin/$applet"; '
            'if ! [ -L "$link" ] || ! [ "$link" -ef /bin/busybox ]; then '
            'echo "Missing or incorrect applet symlink: $link" >&2; exit 1; '
            "fi; done"
        ),
    ])
    assert result.exit_code == 0, f"busybox applet symlinks are incomplete: {result.output}"


@pytest.mark.parametrize(
    ("command", "expected"),
    [
        (["ls", "/"], "usr"),
        (["uname", "-s"], "Linux"),
    ],
)
def test_busybox_applets_on_path(
    container_exec: Callable[[list[str]], ContainerExecResult],
    command: list[str],
    expected: str,
) -> None:
    """Applets beyond the runtime harness's minimum must work without a BusyBox prefix."""
    result = container_exec(command)
    assert result.exit_code == 0, f"{command[0]} failed: {result.output}"
    assert expected in result.output.split(), f"unexpected {command[0]} output: {result.output}"
