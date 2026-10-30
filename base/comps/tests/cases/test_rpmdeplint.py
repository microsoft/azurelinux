# SPDX-License-Identifier: MIT
"""Dependency-graph checks for built RPM artifacts, performed by rpmdeplint."""

from __future__ import annotations

import subprocess
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pathlib import Path


def run_rpmdeplint(
    subcommand: str, rpm_paths: list[Path], repositories: list[str]
) -> subprocess.CompletedProcess[str]:
    """Run an rpmdeplint subcommand against the candidate RPMs and given repos."""
    command = ["rpmdeplint", subcommand]
    for repository in repositories:
        command.extend(("--repo", repository))
    command.extend(str(rpm_path) for rpm_path in rpm_paths)
    return subprocess.run(command, check=False, capture_output=True, text=True)


@pytest.mark.requires_tool("rpmdeplint")
@pytest.mark.rpmdeplint
def test_rpmdeplint_dependencies_are_satisfiable(
    rpm_paths: list[Path], rpmdeplint_repositories: list[str]
) -> None:
    """Every dependency the candidate RPMs declare must resolve against the given repos."""
    result = run_rpmdeplint("check-sat", rpm_paths, rpmdeplint_repositories)
    assert result.returncode == 0, (
        "rpmdeplint found unsatisfiable dependencies "
        f"(rc={result.returncode})\n{result.stdout}{result.stderr}"
    )


@pytest.mark.requires_tool("rpmdeplint")
@pytest.mark.rpmdeplint
def test_rpmdeplint_has_no_undeclared_file_conflicts(
    rpm_paths: list[Path], rpmdeplint_repositories: list[str]
) -> None:
    """Candidate RPMs must not install a file already owned by another package.

    Unless a Conflicts: relationship is declared between the two packages.
    """
    result = run_rpmdeplint("check-conflicts", rpm_paths, rpmdeplint_repositories)
    assert result.returncode == 0, (
        "rpmdeplint found undeclared file conflicts "
        f"(rc={result.returncode})\n{result.stdout}{result.stderr}"
    )


@pytest.mark.requires_tool("rpmdeplint")
@pytest.mark.rpmdeplint
def test_rpmdeplint_is_not_a_downgrade(
    rpm_paths: list[Path], rpmdeplint_repositories: list[str]
) -> None:
    """Candidate RPMs must not be older than any existing package of the same name.

    Compares against whatever package of the same name is already present in
    the given repos.
    """
    result = run_rpmdeplint("check-upgrade", rpm_paths, rpmdeplint_repositories)
    assert result.returncode == 0, (
        "rpmdeplint found a candidate that is not an upgrade over an existing package "
        f"(rc={result.returncode})\n{result.stdout}{result.stderr}"
    )
