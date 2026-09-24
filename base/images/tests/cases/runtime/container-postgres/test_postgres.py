# SPDX-License-Identifier: MIT
"""Validate the container-postgres workload image."""

from __future__ import annotations

import logging
import sys
import uuid
from typing import TYPE_CHECKING

from python_on_whales.exceptions import DockerException
from utils.container_runtime import (
    create_container,
    destroy_container,
    exec_in_container,
    wait_until_service_ready,
)

if TYPE_CHECKING:
    from pathlib import Path

    from python_on_whales import DockerClient
    from utils.container_runtime import ContainerExecResult, ExecShell

PGDATA = "/var/lib/pgsql/data"
POSTGRES_DB = "workload_test"
POSTGRES_PASSWORD = "workload-test-password"  # noqa: S105 - isolated test credential

logger = logging.getLogger(__name__)


def test_postgres_binary_reports_version(container_exec_shell: ExecShell) -> None:
    """The PostgreSQL server binary must report a version."""
    result = container_exec_shell("postgres --version")
    assert result.exit_code == 0, f"postgres --version failed: {result.output}"
    assert "postgres (PostgreSQL)" in result.output, f"unexpected postgres --version output: {result.output}"


def test_postgres_rejects_unsafe_pgdata(container_exec_shell: ExecShell) -> None:
    """The entrypoint must reject paths that could corrupt the container."""
    result = container_exec_shell(
        "PGDATA=/ POSTGRES_PASSWORD=test /usr/local/bin/postgres-entrypoint.sh",
    )
    assert result.exit_code != 0, "entrypoint accepted PGDATA=/"
    assert "refusing unsafe PGDATA path: /" in result.output, f"unexpected error: {result.output}"


def test_postgres_default_command_initializes_and_serves(
    podman_client: DockerClient,
    container_image_ref: str,
    workdir: Path,
) -> None:
    """The default command must initialize an empty data volume and serve queries."""
    data_dir = workdir / "postgres-data"
    data_dir.mkdir()

    suffix = uuid.uuid4().hex[:12]
    network_name = f"azl-test-net-{suffix}"
    server_name = f"azl-test-server-{suffix}"
    client_name = f"azl-test-client-{suffix}"
    podman_client.network.create(network_name)
    try:
        create_container(
            podman_client,
            container_image_ref,
            server_name,
            command=None,
            envs={
                "POSTGRES_DB": POSTGRES_DB,
                "POSTGRES_PASSWORD": POSTGRES_PASSWORD,
            },
            networks=[network_name],
            volumes=[(str(data_dir), PGDATA, "Z,U")],
        )
        create_container(
            podman_client,
            container_image_ref,
            client_name,
            networks=[network_name],
        )

        def server_exec_shell(command: str, *, shell: str = "bash") -> ContainerExecResult:
            return exec_in_container(podman_client, server_name, [shell, "-c", command])

        def client_exec_shell(command: str, *, shell: str = "bash") -> ContainerExecResult:
            return exec_in_container(podman_client, client_name, [shell, "-c", command])

        query = wait_until_service_ready(
            client_exec_shell,
            (
                f"PGPASSWORD={POSTGRES_PASSWORD} psql "
                f"--host={server_name} --username=postgres --dbname={POSTGRES_DB} "
                "--tuples-only --no-align --command='SELECT 1;'"
            ),
            contains="1",
            attempts=30,
        )
        assert query.stdout.strip() == "1", f"unexpected psql output: {query.output}"

        bad_auth = client_exec_shell(
            f"PGPASSWORD=wrong psql "
            f"--host={server_name} --username=postgres --dbname={POSTGRES_DB} "
            "--command='SELECT 1;'",
        )
        assert bad_auth.exit_code != 0, f"wrong password was accepted: {bad_auth.output}"
        assert "authentication failed" in bad_auth.output, f"unexpected authentication error: {bad_auth.output}"

        pid_one = server_exec_shell("cat /proc/1/comm")
        assert pid_one.exit_code == 0, f"failed to inspect PID 1: {pid_one.output}"
        assert pid_one.stdout.strip() == "postgres", f"expected postgres as PID 1: {pid_one.output}"
    finally:
        preserve_primary_failure = sys.exc_info()[0] is not None
        try:
            for container_name in (client_name, server_name):
                destroy_container(podman_client, container_name)
        finally:
            try:
                podman_client.network.remove(network_name)
            except DockerException as exc:
                if not preserve_primary_failure:
                    raise
                logger.warning("Failed to remove test network %s: %s", network_name, exc)
