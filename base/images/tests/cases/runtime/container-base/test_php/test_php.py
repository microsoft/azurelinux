# SPDX-License-Identifier: MIT
"""Validate the PHP runtime works on the container-base image.

Uses ``@pytest.mark.dockerfile()`` to build a custom image with PHP and
the zip extension installed on top of the image-under-test, then runs
the built-in PHP web server and verifies a zip round-trip via router.php.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from utils.container_runtime import AssertHttpServer, ExecShell

EXPECTED_RESPONSE = (Path(__file__).with_name("response.txt")).read_text().strip()


@pytest.mark.dockerfile()
def test_php_version(container_exec_shell: ExecShell) -> None:
    """PHP interpreter must be present and report a version."""
    result = container_exec_shell("php --version")
    assert result.exit_code == 0, f"php --version failed: {result.output}"
    assert "PHP" in result.output


@pytest.mark.dockerfile()
def test_php_zip_extension_loaded(container_exec_shell: ExecShell) -> None:
    """The zip extension must be loaded in the PHP runtime."""
    result = container_exec_shell("php -m")
    assert result.exit_code == 0, f"php -m failed: {result.output}"
    assert "zip" in result.output


@pytest.mark.dockerfile()
def test_php_http_server(assert_http_server: AssertHttpServer) -> None:
    """The built-in PHP server must serve a successful zip round-trip."""
    assert_http_server(
        "nohup php -S 0.0.0.0:8080 /app/router.php > /tmp/server.log 2>&1 &",
        "http://localhost:8080/",
        EXPECTED_RESPONSE,
    )
