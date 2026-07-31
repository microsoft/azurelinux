# SPDX-License-Identifier: MIT
"""Validate the Memcached server on the container-base image."""

from __future__ import annotations

import pytest
from utils.container_runtime import ExecShell, wait_until_service_ready

PORT = 11211


def _start_memcached(container_exec_shell: ExecShell) -> None:
    """Start memcached daemonized and wait until it accepts connections."""
    # Run as the memcached user, since the server cannot run as root.
    start = container_exec_shell(f"memcached -u memcached -d -p {PORT}")
    assert start.exit_code == 0, f"memcached failed to start: {start.output}"

    wait_until_service_ready(
        container_exec_shell,
        f"printf 'version\\r\\nquit\\r\\n' | nc localhost {PORT}",
        contains="VERSION",
    )


@pytest.mark.dockerfile()
def test_memcached_version(container_exec_shell: ExecShell) -> None:
    """The Memcached server binary reports a version."""
    result = container_exec_shell("memcached --version")
    assert result.exit_code == 0, f"memcached --version failed: {result.output}"
    assert "memcached" in result.output


@pytest.mark.dockerfile()
def test_memcached_set_get(container_exec_shell: ExecShell) -> None:
    """Store a value with memcached and read it back."""
    _start_memcached(container_exec_shell)
    # Text protocol: "set <key> <flags> <exptime> <bytes>" + the value, then get it back.
    result = container_exec_shell(
        f"printf 'set TestValue 0 100 4\\r\\nTest\\r\\nget TestValue\\r\\nquit\\r\\n' | nc localhost {PORT}",
    )
    assert result.exit_code == 0, f"nc failed: {result.output}"
    assert "STORED" in result.output, f"set not acknowledged: {result.output}"
    body = result.output.replace("\r\n", "\n")
    assert "VALUE TestValue 0 4\nTest\nEND" in body, f"unexpected get response: {result.output}"
