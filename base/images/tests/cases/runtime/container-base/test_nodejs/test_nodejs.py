# SPDX-License-Identifier: MIT
"""Validate the Node.js runtime works on the container-base image.

Uses ``@pytest.mark.dockerfile()`` to build a custom image with Node.js
installed on top of the image-under-test, then runs a stdlib ``http``
server and checks its response.
"""

from __future__ import annotations

from pathlib import Path

import pytest

EXPECTED_RESPONSE = (Path(__file__).with_name("response.txt")).read_text().strip()


@pytest.mark.dockerfile()
def test_nodejs_version(container_exec_shell) -> None:
    """Node.js interpreter must be present and report a version."""
    result = container_exec_shell("node --version")
    assert result.exit_code == 0, f"node --version failed: {result.output}"
    assert result.output.strip().startswith("v")


@pytest.mark.dockerfile()
def test_nodejs_http_server(assert_http_server) -> None:
    """A stdlib http server must serve the expected response."""
    assert_http_server(
        "nohup node /app/server.js > /tmp/server.log 2>&1 &",
        "http://localhost:8080/",
        EXPECTED_RESPONSE,
    )
