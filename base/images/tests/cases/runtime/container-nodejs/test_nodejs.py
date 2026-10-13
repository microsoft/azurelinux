# SPDX-License-Identifier: MIT
"""Validate the container-nodejs workload image.

The image's default command is a bare `node` REPL, which expects an
interactive stdin the shared exec-based test harness cannot feed in
(exec_in_container has no stdin support). These tests instead validate
the interpreter via `node -e`, which is a documented scope limitation
rather than an oversight.
"""

from __future__ import annotations

import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from python_on_whales import DockerClient
    from utils.container_runtime import ExecShell, WriteFile

HTTP_RESPONSE = "Hello from container-nodejs"
HTTP_SERVER = f"""\
const http = require('http');
http.createServer((request, response) => {{
    response.writeHead(200, {{ 'Content-Type': 'text/plain' }});
    response.end('{HTTP_RESPONSE}');
}}).listen(8080, '127.0.0.1');
"""


def test_node_image_config_cmd(podman_client: DockerClient, container_image_ref: str) -> None:
    """The image must start the Node.js interpreter by default."""
    cmd = podman_client.image.inspect(container_image_ref).config.cmd
    assert cmd == ["/usr/bin/node"], f"unexpected Config.Cmd: {cmd!r}"


def test_node_version(container_exec_shell: ExecShell) -> None:
    """Node must report a version."""
    result = container_exec_shell("node --version")
    assert result.exit_code == 0, f"node --version failed: {result.output}"
    assert result.stdout.strip().startswith("v"), f"unexpected node --version output: {result.output}"


def test_node_executes_code(container_exec_shell: ExecShell) -> None:
    """Node -e must execute code and print the expected result."""
    result = container_exec_shell("node -e 'console.log(1 + 1)'")
    assert result.exit_code == 0, f"node -e failed: {result.output}"
    assert result.stdout.strip() == "2", f"expected '2', got {result.stdout!r}: {result.output}"


def test_node_http_server(container_exec_shell: ExecShell, write_file_in_container: WriteFile) -> None:
    """Node's standard library must serve and receive an HTTP response."""
    write = write_file_in_container(
        "/tmp/server.js",  # noqa: S108 - inside a fresh test container
        HTTP_SERVER,
    )
    assert write.exit_code == 0, f"failed to write HTTP server: {write.output}"

    start = container_exec_shell("nohup node /tmp/server.js > /tmp/server.log 2>&1 &")
    assert start.exit_code == 0, f"failed to start HTTP server: {start.output}"

    probe_command = (
        "node -e \"require('http').get('http://127.0.0.1:8080/', response => { "
        "let body = ''; response.on('data', chunk => body += chunk); "
        "response.on('end', () => { console.log(response.statusCode); console.log(body); }); "
        "}).on('error', error => { console.error(error.message); process.exit(1); })\""
    )
    result = None
    for _ in range(5):
        result = container_exec_shell(probe_command)
        if result.exit_code == 0:
            break
        time.sleep(1)

    assert result is not None
    assert result.exit_code == 0, f"HTTP probe failed: {result.output}"
    assert result.stdout.splitlines() == ["200", HTTP_RESPONSE], f"unexpected HTTP response: {result.output}"
