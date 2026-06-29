# SPDX-License-Identifier: MIT
"""Verify the container's python3 computes Pi correctly (Dockerfile adds python3)."""

from __future__ import annotations

import pytest

_PI = "/opt/azl-tests/pi.py"


@pytest.mark.dockerfile()
def test_pi_1000_places(container_exec_shell) -> None:
    """Pi computed to 1000 places must match the known value."""
    result = container_exec_shell(f"python3 {_PI} 1000")
    assert result.exit_code == 0, f"Pi(1000) verification failed: {result.output}"


@pytest.mark.dockerfile()
def test_pi_n_times_1000_places(container_exec_shell) -> None:
    """Sustained Pi compute (10 x 1000 places) must stay correct and fast."""
    result = container_exec_shell(f"python3 {_PI} n1000")
    assert result.exit_code == 0, f"Pi series verification failed: {result.output}"
