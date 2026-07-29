# SPDX-License-Identifier: MIT
"""Validate the .NET runtime works on the container-base image.

Uses ``@pytest.mark.dockerfile()`` to build a custom image with the
.NET SDK installed on top of the image-under-test. The Dockerfile
publishes a stdlib ``HttpListener`` web app and a RestSharp client
that communicates with it over localhost.
"""

from __future__ import annotations

import pytest

EXPECTED_RESPONSE = "Hello World!"


@pytest.mark.dockerfile()
def test_dotnet_version(container_exec_shell) -> None:
    """.NET runtime must be present and report a version."""
    result = container_exec_shell("dotnet --version")
    assert result.exit_code == 0, f"dotnet --version failed: {result.output}"


@pytest.mark.dockerfile()
def test_dotnet_web(assert_http_server, container_exec_shell) -> None:
    """A .NET server and RestSharp client must communicate over localhost."""
    assert_http_server(
        "nohup dotnet /app/webapp/app.dll > /tmp/server.log 2>&1 &",
        "http://localhost:8080/",
        EXPECTED_RESPONSE,
    )
    result = container_exec_shell("dotnet /app/restclient/app.dll")
    assert result.exit_code == 0, f"dotnet app failed: {result.output}"
    assert "RestSharp reached the .NET server." in result.output
