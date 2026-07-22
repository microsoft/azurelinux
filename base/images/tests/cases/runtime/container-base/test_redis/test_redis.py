# SPDX-License-Identifier: MIT
"""Validate the Redis server on the container-base image."""

from __future__ import annotations

import pytest
from utils.container_runtime import wait_until_service_ready

EXPECTED_LEN = "4"


def _start_redis(container_exec_shell) -> None:
    """Start redis-server daemonized and wait until it answers PING."""
    start = container_exec_shell("redis-server --protected-mode no --save 60 1 --daemonize yes")
    assert start.exit_code == 0, f"redis-server failed to start: {start.output}"

    wait_until_service_ready(container_exec_shell, "redis-cli ping", contains="PONG")


@pytest.mark.dockerfile()
def test_redis_version(container_exec_shell) -> None:
    """The Redis server reports its version."""
    _start_redis(container_exec_shell)
    result = container_exec_shell("redis-cli INFO server")
    assert result.exit_code == 0, f"INFO server failed: {result.output}"
    assert "redis_version:" in result.output


@pytest.mark.dockerfile()
def test_redis_cross_container(client_server_exec_shell) -> None:
    """A client container reaches the server container's Redis over the network and runs LPUSH."""
    server_exec, client_exec, server_host = client_server_exec_shell

    _start_redis(server_exec)

    cli = f"redis-cli -h {server_host}"

    push = client_exec(f"{cli} LPUSH mylist a b c d")
    assert push.exit_code == 0, f"remote LPUSH failed: {push.output}"
    assert push.output.strip() == EXPECTED_LEN, f"expected list length {EXPECTED_LEN}: {push.output}"
