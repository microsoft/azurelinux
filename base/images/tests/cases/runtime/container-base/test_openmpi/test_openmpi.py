# SPDX-License-Identifier: MIT
"""Validate OpenMPI runtime behavior on container-base images.

Uses ``@pytest.mark.dockerfile()`` to build a custom image with
OpenMPI installed on top of the image-under-test.
"""

from __future__ import annotations

import pytest
from utils.container_runtime import ExecShell

MPI_RUN = "/usr/lib64/openmpi/bin/mpirun"
PRTE_RUN = "/usr/lib64/openmpi/bin/prterun"
MPI_CC = "/usr/lib64/openmpi/bin/mpicc"
MPI_TIMEOUT_SECS = 30


@pytest.mark.dockerfile()
def test_openmpi_mpirun_version(container_exec_shell: ExecShell) -> None:
    """mpirun binary must exist and report version."""
    result = container_exec_shell(f"OMPI_PRTERUN={PRTE_RUN} {MPI_RUN} --version")
    assert result.exit_code == 0, f"mpirun --version failed: {result.output}"
    assert "Open MPI" in result.output


@pytest.mark.dockerfile()
def test_openmpi_runs_multiple_ranks(container_exec_shell: ExecShell) -> None:
    """mpirun should launch two ranks in a single container."""
    result = container_exec_shell(
        f"OMPI_PRTERUN={PRTE_RUN} "
        "OMPI_ALLOW_RUN_AS_ROOT=1 OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1 "
        f"{MPI_RUN} --timeout {MPI_TIMEOUT_SECS} --oversubscribe -np 2 "
        "/bin/sh -c 'echo rank=$OMPI_COMM_WORLD_RANK'"
    )
    assert result.exit_code == 0, f"mpirun rank launch failed: {result.output}"
    ranks = sorted(
        line.strip()
        for line in result.output.splitlines()
        if line.startswith("rank=")
    )
    assert ranks == ["rank=0", "rank=1"], f"unexpected rank output: {result.output}"


@pytest.mark.dockerfile()
def test_openmpi_send_receive_between_two_ranks(container_exec_shell: ExecShell) -> None:
    """Two MPI ranks should exchange tagged messages successfully."""
    compile_and_run = (
        f"{MPI_CC} -O2 -o /tmp/send_receive "
        "/opt/mpi-tests/send_receive.c && "
        f"OMPI_PRTERUN={PRTE_RUN} "
        "OMPI_ALLOW_RUN_AS_ROOT=1 "
        "OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1 "
        f"{MPI_RUN} --timeout {MPI_TIMEOUT_SECS} --oversubscribe -np 2 /tmp/send_receive"
    )
    result = container_exec_shell(compile_and_run)
    assert result.exit_code == 0, f"send/receive MPI test failed: {result.output}"
    assert "rank0 sent messages" in result.output
    assert "tag2:Using Tag2" in result.output
    assert "tag2:Again Using Tag2" in result.output
    assert "tag1:Using Tag1" in result.output
    assert "tag1:Again Using Tag1" in result.output