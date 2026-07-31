# SPDX-License-Identifier: MIT
"""Basic runtime tests for container-base images.

Validate fundamental container behavior by exec-ing commands into a
running container. Each test gets a fresh container instance via the
``container_exec_shell`` fixture (see conftest.py).
"""

from __future__ import annotations

from utils.container_runtime import ExecShell


def test_shell_accessible(container_exec_shell: ExecShell) -> None:
    """Container shell must be functional via exec."""
    result = container_exec_shell("echo hello-from-container")
    assert result.exit_code == 0, (
        f"Shell exec failed (exit_code={result.exit_code}): {result.output}"
    )
    assert "hello-from-container" in result.output


def test_dns_resolution(container_exec_shell: ExecShell) -> None:
    """Container must be able to resolve localhost via DNS."""
    result = container_exec_shell("getent hosts localhost")
    assert result.exit_code == 0, (
        f"DNS resolution failed (exit_code={result.exit_code}): {result.output}"
    )
    assert "localhost" in result.output
