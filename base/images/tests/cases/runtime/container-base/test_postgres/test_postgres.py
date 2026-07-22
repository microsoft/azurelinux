# SPDX-License-Identifier: MIT
"""Validate the PostgreSQL server on the container-base image."""

from __future__ import annotations

import contextlib

import pytest
from utils.container_runtime import wait_until_service_ready

DB_PORT = 5432
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "secret"  # noqa: S105 - throwaway password for the test container
EXPECTED_ROWS = 2

PG_DIR = "/var/lib/pgsql"
PG_DATADIR = f"{PG_DIR}/data"
PG_LOGFILE = f"{PG_DIR}/logfile"
PG_RUNDIR = "/run/postgresql"


@contextlib.contextmanager
def _postgres_password_file(container_exec_shell, password: str):
    """Yield a postgres-owned temp password file; remove it on exit."""
    mk = container_exec_shell("mktemp")
    assert mk.exit_code == 0, f"mktemp failed: {mk.output}"
    filepath = mk.stdout.strip()
    try:
        setup = container_exec_shell(f"printf %s {password} > {filepath} && chown postgres {filepath}")
        assert setup.exit_code == 0, f"password file setup failed: {setup.output}"
        yield filepath
    finally:
        container_exec_shell(f"runuser -u postgres rm -f {filepath}")


def _start_postgresql(container_exec_shell, *, listen_all: bool = False) -> None:
    """Init the cluster and start the server; listen_all also opens it to remote hosts."""
    socket = container_exec_shell(
        f"mkdir -p {PG_RUNDIR} && chown postgres:postgres {PG_RUNDIR}",
    )
    assert socket.exit_code == 0, f"socket dir setup failed: {socket.output}"

    # initdb and the server cannot run as root.
    with _postgres_password_file(container_exec_shell, DB_PASSWORD) as pwfile_path:
        initdb = container_exec_shell(
            "runuser -l postgres -c '"
            "initdb --locale=C --encoding=UTF8 --auth-local=peer "
            f"--auth-host=scram-sha-256 --pwfile={pwfile_path} -D {PG_DATADIR}'",
        )
        assert initdb.exit_code == 0, f"initdb failed: {initdb.output}"

    if listen_all:
        # Open the server to remote TCP; it listens on localhost only by default.
        config = container_exec_shell(
            f"echo \"listen_addresses = '*'\" >> {PG_DATADIR}/postgresql.conf && "
            f"echo 'host all all 0.0.0.0/0 scram-sha-256' >> {PG_DATADIR}/pg_hba.conf",
        )
        assert config.exit_code == 0, f"network config setup failed: {config.output}"

    start = container_exec_shell(
        f"runuser -l postgres -c 'pg_ctl -D {PG_DATADIR} -l {PG_LOGFILE} -w start'",
    )
    assert start.exit_code == 0, f"pg_ctl start failed: {start.output}"

    wait_until_service_ready(container_exec_shell, f"pg_isready -h localhost -p {DB_PORT}")


def _run_crud_workflow(exec_shell, host: str) -> None:
    """Create a table, insert two rows, and read them back against the DB at ``host``."""
    psql = f"PGPASSWORD={DB_PASSWORD} psql -h {host} -p {DB_PORT} -U {DB_USER} -d {DB_NAME}"

    create = exec_shell(f'{psql} -c "CREATE TABLE cities (name varchar(80), location point);"')
    assert create.exit_code == 0, f"create failed: {create.output}"
    assert "CREATE TABLE" in create.output

    insert_sql = (
        "INSERT INTO cities VALUES ('San Francisco', '(-194.0, 53.0)'); "
        "INSERT INTO cities VALUES ('Seattle', '(-150.0, 86.0)');"
    )
    insert = exec_shell(f'{psql} -c "{insert_sql}"')
    assert insert.exit_code == 0, f"insert failed: {insert.output}"
    assert insert.output.count("INSERT 0 1") == EXPECTED_ROWS, f"expected two inserts: {insert.output}"

    select = exec_shell(f'{psql} -c "SELECT * FROM cities;"')
    assert select.exit_code == 0, f"select failed: {select.output}"
    assert f"{EXPECTED_ROWS} rows" in select.output, f"expected {EXPECTED_ROWS} rows: {select.output}"


def _assert_bad_auth_rejected(exec_shell, host: str) -> None:
    """A wrong password must be rejected, proving the scram rule is enforced (not trust)."""
    bad_auth = exec_shell(
        f"PGPASSWORD=wrong psql -h {host} -p {DB_PORT} -U {DB_USER} -d {DB_NAME} -c 'SELECT 1;'",
    )
    assert bad_auth.exit_code != 0, f"wrong password was accepted: {bad_auth.output}"
    assert "authentication failed" in bad_auth.output, f"unexpected auth error: {bad_auth.output}"


@pytest.mark.dockerfile()
def test_postgresql_version(container_exec_shell) -> None:
    """The PostgreSQL server binary reports a version."""
    result = container_exec_shell("postgres --version")
    assert result.exit_code == 0, f"postgres --version failed: {result.output}"
    assert "postgres (PostgreSQL)" in result.output


@pytest.mark.dockerfile()
def test_postgresql_database_server(container_exec_shell) -> None:
    """Server accepts TCP connections and handles create/insert/select."""
    _start_postgresql(container_exec_shell)
    _assert_bad_auth_rejected(container_exec_shell, "localhost")
    _run_crud_workflow(container_exec_shell, "localhost")


@pytest.mark.dockerfile()
def test_postgresql_cross_container(client_server_exec_shell) -> None:
    """A client container reaches a server container's database over the network."""
    server_exec, client_exec, server_host = client_server_exec_shell

    _start_postgresql(server_exec, listen_all=True)
    _assert_bad_auth_rejected(client_exec, server_host)
    _run_crud_workflow(client_exec, server_host)
