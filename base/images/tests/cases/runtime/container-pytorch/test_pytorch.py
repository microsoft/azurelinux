# SPDX-License-Identifier: MIT
"""Validate the container-pytorch workload image.

The image's default command is a bare `python3` REPL, which expects an
interactive stdin the shared exec-based test harness cannot feed in
(exec_in_container has no stdin support). These tests instead validate
torch via `python3 -c`, which is a documented scope limitation rather
than an oversight.
"""

from __future__ import annotations

from utils.container_runtime import ExecShell


def test_torch_importable(container_exec_shell: ExecShell) -> None:
    """torch must import and report a version."""
    result = container_exec_shell("python3 -c 'import torch; print(torch.__version__)'")
    assert result.exit_code == 0, f"importing torch failed: {result.output}"
    assert result.stdout.strip(), f"expected a torch version string, got: {result.output}"


def test_torch_tensor_math(container_exec_shell: ExecShell) -> None:
    """torch must perform basic tensor arithmetic."""
    result = container_exec_shell(
        "python3 -c 'import torch; print((torch.tensor([1, 2]) + torch.tensor([3, 4])).tolist())'"
    )
    assert result.exit_code == 0, f"torch tensor math failed: {result.output}"
    assert result.stdout.strip() == "[4, 6]", f"expected '[4, 6]', got {result.stdout!r}: {result.output}"
