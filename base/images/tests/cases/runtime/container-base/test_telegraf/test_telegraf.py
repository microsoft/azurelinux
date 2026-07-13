# SPDX-License-Identifier: MIT
"""Validate Telegraf runtime behavior on container-base images.

Use checked-in config, run in test mode, and verify mem metrics output.
"""

from __future__ import annotations

from pathlib import Path

import pytest


TELEGRAF_CONFIG = "/etc/telegraf/telegraf.conf"


@pytest.mark.dockerfile()
def test_telegraf_emits_mem_metrics(container_exec_shell) -> None:
    """telegraf --test must emit mem plugin measurement output."""
    result = container_exec_shell(f"telegraf --config {TELEGRAF_CONFIG} --test")
    assert result.exit_code == 0, f"telegraf --test failed: {result.output}"
    assert "mem,host" in result.output


@pytest.mark.dockerfile()
def test_telegraf_reports_version_and_plugin_usage(container_exec_shell) -> None:
    """telegraf binary should report version and cpu plugin usage details."""
    result = container_exec_shell("telegraf --version && telegraf --usage cpu")
    assert result.exit_code == 0, f"telegraf version/usage check failed: {result.output}"
    assert "Telegraf" in result.output
    assert "cpu" in result.output.lower()


@pytest.mark.dockerfile()
def test_telegraf_file_output_plugin_writes_metrics(
    container_exec_shell, write_file_in_container
) -> None:
    """telegraf should be able to flush metrics to file output."""
    config_body = (
        Path(__file__).parent / "configs" / "file_output.conf"
    ).read_text(encoding="utf-8")
    result = write_file_in_container("/tmp/telegraf-file-output.conf", config_body)
    assert result.exit_code == 0, f"failed writing file-output config: {result.output}"

    result = container_exec_shell(
        "set -o pipefail; telegraf --config /tmp/telegraf-file-output.conf --once 2>&1 | tee /tmp/telegraf-file.log"
    )
    assert result.exit_code == 0, f"telegraf file output run failed: {result.output}"

    result = container_exec_shell(
        'test -s /tmp/telegraf-metrics.out && grep -q "mem,host" /tmp/telegraf-metrics.out'
    )
    assert result.exit_code == 0, f"telegraf file output validation failed: {result.output}"

