# SPDX-License-Identifier: MIT
"""Validate the Ruby runtime works on the container-base image.

Uses ``@pytest.mark.dockerfile()`` to build a custom image with Ruby
installed on top of the image-under-test, then runs a stdlib socket
HTTP server and checks its response.
"""

from __future__ import annotations

from pathlib import Path

import pytest

EXPECTED_RESPONSE = (Path(__file__).with_name("response.txt")).read_text().strip()


@pytest.mark.dockerfile()
def test_ruby_version(container_exec_shell) -> None:
    """Ruby interpreter must be present and report a version."""
    result = container_exec_shell("ruby --version")
    assert result.exit_code == 0, f"ruby --version failed: {result.output}"
    assert "ruby" in result.output


@pytest.mark.dockerfile()
def test_ruby_http_server(assert_http_server) -> None:
    """A stdlib socket HTTP server must serve the expected response."""
    assert_http_server(
        "nohup ruby /app/app.rb > /tmp/server.log 2>&1 &",
        "http://localhost:8080/",
        EXPECTED_RESPONSE,
    )
