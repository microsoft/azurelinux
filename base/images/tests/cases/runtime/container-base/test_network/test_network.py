# SPDX-License-Identifier: MIT
"""Verify outbound networking from the container (Dockerfile adds python3)."""

from __future__ import annotations

import pytest

_NET = "/opt/azl-tests/netcheck.py"


@pytest.mark.dockerfile()
def test_online_service_weather(container_exec_shell) -> None:
    """Test Online Services: A single outbound HTTPS fetch must return a non-empty page."""
    result = container_exec_shell(f"python3 {_NET} weather")
    assert result.exit_code == 0, f"Outbound HTTP fetch failed: {result.output}"


@pytest.mark.dockerfile()
def test_sustained_http_fetch(container_exec_shell) -> None:
    """Test Core Networking: 50 sequential outbound fetches must all return valid repo config."""
    result = container_exec_shell(f"python3 {_NET} sustained --strict")
    assert result.exit_code == 0, f"Sustained HTTP fetch failed: {result.output}"
