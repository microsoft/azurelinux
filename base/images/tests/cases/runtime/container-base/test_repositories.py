# SPDX-License-Identifier: MIT
"""Check production package resolution and non-persistent Preview opt-in."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from utils.container_runtime import ExecShell

PRODUCTION_REPOS = {
    "azurelinux-base",
    "azurelinux-cloud-native",
    "azurelinux-microsoft",
}

pytestmark = pytest.mark.require_capability("runtime-package-management")


def test_package_operations_use_production(container_exec_shell: ExecShell) -> None:
    result = container_exec_shell("dnf --refresh makecache")
    assert result.exit_code == 0, f"Default repository refresh failed: {result.output}"

    result = container_exec_shell("dnf repoquery --available --qf '%{repoid}\\n' tree")
    assert result.exit_code == 0, f"Default package query failed: {result.output}"
    repo_ids = set(result.stdout.splitlines())
    assert repo_ids
    assert repo_ids <= PRODUCTION_REPOS, (
        f"Expected tree only from Production repositories, got: {result.output}"
    )

    result = container_exec_shell("dnf -y install tree && tree --version")
    assert result.exit_code == 0, f"Default package transaction failed: {result.output}"


def test_preview_requires_explicit_opt_in(container_exec_shell: ExecShell) -> None:
    result = container_exec_shell(
        "dnf --enable-repo=azurelinux-preview-base repolist --enabled",
    )
    assert result.exit_code == 0, f"Explicit Preview opt-in failed: {result.output}"
    assert "azurelinux-preview-base" in result.output, (
        f"Preview repository not enabled by opt-in: {result.output}"
    )

    result = container_exec_shell("dnf repolist --enabled")
    assert result.exit_code == 0, f"Default repository listing failed: {result.output}"
    assert "azurelinux-preview-" not in result.output, (
        f"Preview opt-in changed persisted defaults: {result.output}"
    )
    for repo_id in PRODUCTION_REPOS:
        assert repo_id in result.output, (
            f"Missing enabled Production repository {repo_id}: {result.output}"
        )
