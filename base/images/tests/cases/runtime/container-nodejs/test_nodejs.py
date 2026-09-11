# SPDX-License-Identifier: MIT
"""Validate the container-nodejs workload image.

The image's default command is a bare `node` REPL, which expects an
interactive stdin the shared exec-based test harness cannot feed in
(exec_in_container has no stdin support). These tests instead validate
the interpreter via `node -e`, which is a documented scope limitation
rather than an oversight.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from python_on_whales import DockerClient
    from utils.container_runtime import ExecShell


def test_node_image_config_cmd(podman_client: DockerClient, container_image_ref: str) -> None:
    """The image must start the Node.js interpreter by default."""
    cmd = podman_client.image.inspect(container_image_ref).config.cmd
    assert cmd == ["/usr/bin/node"], f"unexpected Config.Cmd: {cmd!r}"


def test_node_version(container_exec_shell: ExecShell) -> None:
    """Node must report a version."""
    result = container_exec_shell("node --version")
    assert result.exit_code == 0, f"node --version failed: {result.output}"
    assert result.stdout.strip().startswith("v"), f"unexpected node --version output: {result.output}"


def test_node_executes_code(container_exec_shell: ExecShell) -> None:
    """Node -e must execute code and print the expected result."""
    result = container_exec_shell("node -e 'console.log(1 + 1)'")
    assert result.exit_code == 0, f"node -e failed: {result.output}"
    assert result.stdout.strip() == "2", f"expected '2', got {result.stdout!r}: {result.output}"
