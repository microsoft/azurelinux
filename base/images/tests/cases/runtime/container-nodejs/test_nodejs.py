# SPDX-License-Identifier: MIT
"""Validate the container-nodejs workload image.

The image's default command is a bare `node` REPL, which expects an
interactive stdin the shared exec-based test harness cannot feed in
(exec_in_container has no stdin support). These tests instead validate
the interpreter via `node -e`, which is a documented scope limitation
rather than an oversight.
"""

from __future__ import annotations

import pytest
from utils.container_runtime import ExecShell


def test_node_version(container_exec_shell: ExecShell) -> None:
    """node must report a version."""
    result = container_exec_shell("node --version")
    if result.exit_code != 0:
        pytest.fail(f"node --version failed: {result.output}")
    if not result.stdout.strip().startswith("v"):
        pytest.fail(f"unexpected node --version output: {result.output}")


def test_node_executes_code(container_exec_shell: ExecShell) -> None:
    """node -e must execute code and print the expected result."""
    result = container_exec_shell("node -e 'console.log(1 + 1)'")
    if result.exit_code != 0:
        pytest.fail(f"node -e failed: {result.output}")
    if result.stdout.strip() != "2":
        pytest.fail(f"expected '2', got {result.stdout!r}: {result.output}")
