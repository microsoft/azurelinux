"""Pytest-backed kernel config validation checks."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from kernel_config_checker.check_config import check_kernel_config, parse_kernel_config

if TYPE_CHECKING:
    from pathlib import Path

    from kernel_config_checker.schema.schema import IntentionalKernelConfigSchema


def test_deleted_kernel_config_files_are_rejected(deleted_kernel_config_files: list[str]) -> None:
    """Fail if any kernel config file was deleted in the diff range."""
    if deleted_kernel_config_files:
        message = "Deletion of tracked kernel config files is not allowed:\n" + "\n".join(deleted_kernel_config_files)
        pytest.fail(message)


def test_changed_kernel_configs_match_policy(
    kernel_config_case: tuple[str, str, str],
    intentional_schema: IntentionalKernelConfigSchema,
    repo_root: Path,
) -> None:
    """Validate each changed tracked kernel config against the intentional policy."""
    config_path, kernel_name, architecture = kernel_config_case
    actual_config = parse_kernel_config(repo_root / config_path)

    if not check_kernel_config(actual_config, intentional_schema, kernel_name, architecture):
        message = f"Kernel config validation failed for {config_path}"
        pytest.fail(message)
