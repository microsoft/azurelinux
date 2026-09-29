# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""Pytest-backed kernel config validation checks."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from kernel_config_checker.check_config import (
    _collect_configs,
    check_config_across_all,
    check_kernel_config,
    parse_kernel_config,
)

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


def test_collect_configs_resolves_values(
    intentional_schema: IntentionalKernelConfigSchema,
) -> None:
    """Collect architecture-specific expected values with provenance."""
    configs = _collect_configs(
        intentional_schema.default.kernel_configs,
        "x86_64",
        "default",
    )

    first = intentional_schema.default.kernel_configs[0]
    assert configs[first.name]["source"] == "default"
    assert configs[first.name]["justification"] == first.justification


def test_check_config_across_all_reports_missing(
    intentional_schema: IntentionalKernelConfigSchema,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Return false for a config absent from every policy section."""
    assert not check_config_across_all(intentional_schema, "CONFIG_DOES_NOT_EXIST")
    assert capsys.readouterr().out.endswith("❌ Not found\n")
