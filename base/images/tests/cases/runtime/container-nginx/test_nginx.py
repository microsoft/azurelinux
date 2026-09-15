# SPDX-License-Identifier: MIT
"""Validate nginx's default command on the container-nginx workload image.

Unlike the generic container-base nginx test, nginx is already installed
in this image, so no ``@pytest.mark.dockerfile()`` build step is needed.
"""

from __future__ import annotations

import time

import pytest
from python_on_whales import DockerClient
from utils.container_runtime import (
    ContainerExecResult,
    ExecShell,
    create_container,
    destroy_container,
    exec_in_container,
)


def _poll_http_status(exec_shell: ExecShell, retries: int = 5, delay: float = 1.0) -> ContainerExecResult:
    result = None
    for _ in range(retries):
        result = exec_shell(
            'exec 3<>/dev/tcp/localhost/80 && printf "GET / HTTP/1.0\\r\\n\\r\\n" >&3 && head -n1 <&3'
        )
        if result.exit_code == 0 and result.stdout.strip():
            return result
        time.sleep(delay)
    return result if result is not None else pytest.fail("no attempts were made")


def test_nginx_config_valid(container_exec_shell: ExecShell) -> None:
    """The packaged nginx configuration must pass validation."""
    result = container_exec_shell("nginx -t")
    if result.exit_code != 0:
        pytest.fail(f"nginx -t failed: {result.output}")
    if "syntax is ok" not in result.output or "test is successful" not in result.output:
        pytest.fail(f"unexpected nginx -t output: {result.output}")


def test_nginx_default_command_serves_requests(container_exec_shell: ExecShell) -> None:
    """The image's default command (``nginx -g "daemon off;"``) must start and answer HTTP."""
    start = container_exec_shell('nohup nginx -g "daemon off;" > /tmp/nginx.log 2>&1 &')
    if start.exit_code != 0:
        pytest.fail(f"failed to start nginx: {start.output}")

    result = _poll_http_status(container_exec_shell)
    if result.exit_code != 0:
        pytest.fail(f"HTTP probe to nginx failed: {result.output}")
    if "403" not in result.stdout:
        pytest.fail(f"expected nginx's default 403 response, got: {result.stdout!r}")


def test_nginx_image_config_cmd(podman_client: DockerClient, container_image_ref: str) -> None:
    """The image's ``Config.Cmd`` must be the literal argv nginx expects, with no stray quoting."""
    cmd = podman_client.image.inspect(container_image_ref).config.cmd
    if cmd != ["/usr/sbin/nginx", "-g", "daemon off;"]:
        pytest.fail(f"unexpected Config.Cmd: {cmd!r}")


def test_nginx_runs_as_pid1_without_override(podman_client: DockerClient, container_image_ref: str) -> None:
    """Running the image's actual default command (unmodified) must start nginx and serve HTTP."""
    instance = create_container(podman_client, container_image_ref, command=None)
    try:
        def exec_shell(command: str, shell: str = "bash") -> ContainerExecResult:
            return exec_in_container(podman_client, instance.container_name, [shell, "-c", command])

        result = _poll_http_status(exec_shell)
        if result.exit_code != 0:
            pytest.fail(f"HTTP probe to nginx failed: {result.output}")
        if "403" not in result.stdout:
            pytest.fail(f"expected nginx's default 403 response, got: {result.stdout!r}")
    finally:
        destroy_container(podman_client, instance.container_name)
