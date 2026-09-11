# SPDX-License-Identifier: MIT
"""Validate the container-python workload image.

The image's default command is a bare `python3` REPL, which expects an
interactive stdin the shared exec-based test harness cannot feed in
(exec_in_container has no stdin support). These tests instead validate
the interpreter via `python3 -c`, which is a documented scope
limitation rather than an oversight.
"""

from __future__ import annotations

from utils.container_runtime import ExecShell


def test_python_version(container_exec_shell: ExecShell) -> None:
    """python3 must report a version."""
    result = container_exec_shell("python3 --version")
    assert result.exit_code == 0, f"python3 --version failed: {result.output}"
    assert result.stdout.strip().startswith("Python 3"), f"unexpected python3 --version output: {result.output}"


def test_python_executes_code(container_exec_shell: ExecShell) -> None:
    """python3 -c must execute code and print the expected result."""
    result = container_exec_shell("python3 -c 'print(1 + 1)'")
    assert result.exit_code == 0, f"python3 -c failed: {result.output}"
    assert result.stdout.strip() == "2", f"expected '2', got {result.stdout!r}: {result.output}"
