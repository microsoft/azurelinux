# SPDX-License-Identifier: MIT
"""Validate the container-postgres workload image.

postgresql-server is already installed, and dnf5 pulls in the postgresql
client package transitively (psql, initdb, pg_ctl all present). This
image intentionally ships no entrypoint/initdb wrapper (see
containers-workloads.xml), so tests perform the same manual
initdb/start sequence a user of this image would need to run.
"""

from __future__ import annotations

from utils.container_runtime import ExecShell

PG_DATADIR = "/tmp/pgdata"
PG_RUNDIR = "/run/postgresql"


def test_postgres_default_command_reports_version(container_exec_shell: ExecShell) -> None:
    """The image's default command (``postgres --version``) must succeed.

    This is intentionally a version smoke check, not a running server --
    see the scope note in containers-workloads.xml.
    """
    result = container_exec_shell("postgres --version")
    assert result.exit_code == 0, f"postgres --version failed: {result.output}"
    assert "postgres (PostgreSQL)" in result.output, f"unexpected postgres --version output: {result.output}"


def test_postgres_server_starts_and_accepts_queries(container_exec_shell: ExecShell) -> None:
    """A manually initialized PostgreSQL server must start and answer queries.

    The image does not pre-create /run/postgresql, so the socket
    directory is created here first, mirroring what a real deployment's
    entrypoint would need to do.
    """
    rundir = container_exec_shell(f"mkdir -p {PG_RUNDIR} && chown postgres:postgres {PG_RUNDIR}")
    assert rundir.exit_code == 0, f"failed to create {PG_RUNDIR}: {rundir.output}"

    initdb = container_exec_shell(
        f"runuser -u postgres -- initdb --locale=C --encoding=UTF8 --auth-local=trust --auth-host=trust -D {PG_DATADIR}"
    )
    assert initdb.exit_code == 0, f"initdb failed: {initdb.output}"

    start = container_exec_shell(f"runuser -u postgres -- pg_ctl -D {PG_DATADIR} -l /tmp/pg.log -w start")
    assert start.exit_code == 0, f"pg_ctl start failed: {start.output}"

    query = container_exec_shell("runuser -u postgres -- psql -h localhost -U postgres -c 'SELECT 1;'")
    assert query.exit_code == 0, f"psql query failed: {query.output}"
    assert "1 row" in query.output, f"unexpected psql output: {query.output}"
