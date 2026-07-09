# SPDX-License-Identifier: MIT
"""Validate the Python runtime works on the container-base image.

Uses ``@pytest.mark.dockerfile()`` to build a custom image with the
Python interpreter installed on top of the image-under-test, then runs
a stdlib ``http.server`` app and checks its response.
"""

from __future__ import annotations

from pathlib import Path

import pytest

EXPECTED_RESPONSE = (Path(__file__).with_name("response.txt")).read_text().strip()


@pytest.mark.dockerfile()
def test_python_version(container_exec_shell) -> None:
    """Python interpreter must be present and report version 3."""
    result = container_exec_shell("python3 --version")
    assert result.exit_code == 0, f"python3 --version failed: {result.output}"
    assert "Python 3" in result.output


@pytest.mark.dockerfile()
def test_python_http_server(assert_http_server) -> None:
    """A stdlib http.server app must serve the expected response."""
    assert_http_server(
        "nohup python3 /app/app.py > /tmp/server.log 2>&1 &",
        "http://localhost:8080/",
        EXPECTED_RESPONSE,
    )
