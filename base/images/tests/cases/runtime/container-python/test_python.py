# SPDX-License-Identifier: MIT
"""Validate the container-python workload image.

The image's default command is a bare `python3` REPL, which expects an
interactive stdin the shared exec-based test harness cannot feed in
(exec_in_container has no stdin support). These tests instead validate
the interpreter via explicit commands, which is a documented scope
limitation rather than an oversight.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from utils.container_runtime import wait_until_service_ready

if TYPE_CHECKING:
    from python_on_whales import DockerClient
    from utils.container_runtime import ExecShell, WriteFile

HTTP_RESPONSE = "Hello from container-python"
HTTP_SERVER = """\
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

RESPONSE = Path(__file__).with_name("python-response.txt").read_bytes()

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(RESPONSE)

HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
"""


def test_python_image_config_cmd(podman_client: DockerClient, container_image_ref: str) -> None:
    """The image must start the Python interpreter by default."""
    cmd = podman_client.image.inspect(container_image_ref).config.cmd
    assert cmd == ["/usr/bin/python3"], f"unexpected Config.Cmd: {cmd!r}"


def test_python_version(container_exec_shell: ExecShell) -> None:
    """python3 must report a version."""
    result = container_exec_shell("python3 --version")
    assert result.exit_code == 0, f"python3 --version failed: {result.output}"
    assert result.stdout.strip().startswith("Python 3"), f"unexpected python3 --version output: {result.output}"


def test_python_executes_code(container_exec_shell: ExecShell) -> None:
    """python3 -c must execute code and print the expected result."""
    result = container_exec_shell("python3 -c 'print(1 + 1)'")
    assert result.exit_code == 0, f"python3 -c failed: {result.output}"
    assert result.stdout.strip() == "2", f"expected '2', got {result.stdout!r}: {result.output}"


def test_python_http_server(container_exec_shell: ExecShell, write_file_in_container: WriteFile) -> None:
    """A script must read a file and serve its contents over HTTP."""
    for path, content in (
        ("/tmp/python-server.py", HTTP_SERVER),  # noqa: S108 - inside a fresh test container
        ("/tmp/python-response.txt", HTTP_RESPONSE),  # noqa: S108 - inside a fresh test container
    ):
        write = write_file_in_container(path, content)
        assert write.exit_code == 0, f"failed to write {path}: {write.output}"

    start = container_exec_shell("nohup python3 /tmp/python-server.py > /tmp/python-server.log 2>&1 &")
    assert start.exit_code == 0, f"failed to start HTTP server: {start.output}"

    result = wait_until_service_ready(
        container_exec_shell,
        "python3 -c 'from urllib.request import urlopen; "
        'response = urlopen("http://127.0.0.1:8080/", timeout=2); '
        'print(response.status); print(response.read().decode(), end="")\'',
        contains=HTTP_RESPONSE,
        attempts=5,
    )
    assert result.stdout.splitlines() == ["200", HTTP_RESPONSE], f"unexpected HTTP response: {result.output}"
