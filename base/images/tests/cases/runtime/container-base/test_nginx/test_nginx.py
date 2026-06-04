# SPDX-License-Identifier: MIT
"""Validate nginx works on the container-base image.

Uses ``@pytest.mark.dockerfile()`` to build a custom image with
nginx installed on top of the image-under-test.
"""

from __future__ import annotations

import time

import pytest


def wait_for_http(container_exec_shell, url: str):
    """Poll until an HTTP endpoint responds successfully."""
    result = None
    for _ in range(5):
        result = container_exec_shell(f"curl -sf {url}")
        if result.exit_code == 0:
            return result
        time.sleep(1)

    assert result is not None
    return result


@pytest.mark.dockerfile()
def test_nginx_config_valid(container_exec_shell) -> None:
    """nginx configuration must pass validation."""
    result = container_exec_shell("nginx -t")
    assert result.exit_code == 0, f"nginx -t failed: {result.output}"
    assert "syntax is ok" in result.output
    assert "test is successful" in result.output


@pytest.mark.dockerfile()
def test_nginx_health_endpoint(container_exec_shell) -> None:
    """nginx /health endpoint must return 200."""
    start = container_exec_shell("nginx")
    assert start.exit_code == 0, f"nginx failed to start: {start.output}"

    result = wait_for_http(container_exec_shell, "http://localhost:80/health")
    assert result.exit_code == 0, f"health check failed: {result.output}"
    assert "healthy" in result.output
