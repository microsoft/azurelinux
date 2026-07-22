# SPDX-License-Identifier: MIT
"""Validate the Valkey server on the container-base image."""

from __future__ import annotations

import pytest
from utils.container_runtime import wait_until_service_ready

EXPECTED_LEN = "4"


def _start_valkey(container_exec_shell) -> None:
    """Start valkey-server daemonized and wait until it answers PING."""
    start = container_exec_shell("valkey-server --protected-mode no --save 60 1 --daemonize yes")
    assert start.exit_code == 0, f"valkey-server failed to start: {start.output}"

    wait_until_service_ready(container_exec_shell, "valkey-cli ping", contains="PONG")


@pytest.mark.dockerfile()
def test_valkey_version(container_exec_shell) -> None:
    """The Valkey server reports its version."""
    _start_valkey(container_exec_shell)
    result = container_exec_shell("valkey-cli INFO server")
    assert result.exit_code == 0, f"INFO server failed: {result.output}"
    assert "valkey_version:" in result.output


@pytest.mark.dockerfile()
def test_valkey_cross_container(client_server_exec_shell) -> None:
    """A client container reaches the server container's Valkey over the network and runs LPUSH."""
    server_exec, client_exec, server_host = client_server_exec_shell

    _start_valkey(server_exec)

    cli = f"valkey-cli -h {server_host}"

    push = client_exec(f"{cli} LPUSH mylist a b c d")
    assert push.exit_code == 0, f"remote LPUSH failed: {push.output}"
    assert push.output.strip() == EXPECTED_LEN, f"expected list length {EXPECTED_LEN}: {push.output}"
