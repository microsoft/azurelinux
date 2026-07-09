# SPDX-License-Identifier: MIT
"""Validate nginx works on the container-base image.

Uses ``@pytest.mark.dockerfile()`` to build a custom image with
nginx installed on top of the image-under-test.
"""

from __future__ import annotations

import pytest


@pytest.mark.dockerfile()
def test_nginx_config_valid(container_exec_shell) -> None:
    """nginx configuration must pass validation."""
    result = container_exec_shell("nginx -t")
    assert result.exit_code == 0, f"nginx -t failed: {result.output}"
    assert "syntax is ok" in result.output
    assert "test is successful" in result.output


@pytest.mark.dockerfile()
def test_nginx_health_endpoint(assert_http_server) -> None:
    """nginx /health endpoint must return 200."""
    assert_http_server("nginx", "http://localhost:80/health", "healthy")
