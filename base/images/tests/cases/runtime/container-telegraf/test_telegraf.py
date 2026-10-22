# SPDX-License-Identifier: MIT
"""Validate the container-telegraf workload image."""

from __future__ import annotations

import time
from typing import TYPE_CHECKING

from utils.container_runtime import (
    ExecShell,
    create_container,
    destroy_container,
)

if TYPE_CHECKING:
    from pathlib import Path

    from python_on_whales import DockerClient
    from utils.container_runtime import WriteFile

TELEGRAF_CONFIG = "/etc/telegraf/telegraf.conf"
TELEGRAF_TEST_CONFIG = """\
[agent]
  interval = "1s"
  flush_interval = "1s"

[[inputs.mem]]

[[outputs.file]]
  files = ["stdout"]
  data_format = "influx"
"""


def test_telegraf_version(container_exec_shell: ExecShell) -> None:
    """Telegraf binary must report its version."""
    result = container_exec_shell("telegraf --version")
    assert result.exit_code == 0, f"telegraf --version failed: {result.output}"
    assert "Telegraf" in result.output, f"unexpected telegraf --version output: {result.output}"


def test_telegraf_test_mode_emits_mem_metrics(container_exec_shell: ExecShell) -> None:
    """Telegraf --test (which bypasses outputs) must gather real input metrics."""
    result = container_exec_shell(f"telegraf --config {TELEGRAF_CONFIG} --test")
    assert result.exit_code == 0, f"telegraf --test failed: {result.output}"
    assert "mem,host" in result.output, f"expected mem metrics in telegraf --test output: {result.output}"


def test_telegraf_cpu_plugin_usage(container_exec_shell: ExecShell) -> None:
    """The CPU input plugin must expose its usage information."""
    result = container_exec_shell("telegraf --usage cpu")
    assert result.exit_code == 0, f"CPU plugin usage failed: {result.output}"
    assert "cpu" in result.output.lower(), f"expected CPU plugin usage: {result.output}"


def test_telegraf_file_output_plugin_writes_metrics(
    container_exec_shell: ExecShell,
    write_file_in_container: WriteFile,
) -> None:
    """A one-shot collection must flush memory metrics to a real file."""
    config = TELEGRAF_TEST_CONFIG.replace('["stdout"]', '["/tmp/telegraf-metrics.out"]')
    write = write_file_in_container(
        "/tmp/telegraf-file-output.conf",  # noqa: S108 - inside a fresh test container
        config,
    )
    assert write.exit_code == 0, f"failed writing file-output config: {write.output}"

    result = container_exec_shell("telegraf --config /tmp/telegraf-file-output.conf --once")
    assert result.exit_code == 0, f"telegraf file output run failed: {result.output}"

    result = container_exec_shell(
        'test -s /tmp/telegraf-metrics.out && grep -q "mem,host" /tmp/telegraf-metrics.out',
    )
    assert result.exit_code == 0, f"telegraf file output validation failed: {result.output}"


def test_telegraf_default_command_uses_mounted_config(
    podman_client: DockerClient,
    container_image_ref: str,
    workdir: Path,
) -> None:
    """The default command must run with a caller-supplied configuration."""
    config_path = workdir / "telegraf-workload.conf"
    config_path.write_text(TELEGRAF_TEST_CONFIG, encoding="utf-8")

    instance = create_container(
        podman_client,
        container_image_ref,
        command=None,
        volumes=[(str(config_path), TELEGRAF_CONFIG, "ro,Z")],
    )
    try:
        logs = ""
        for _ in range(5):
            current_logs = podman_client.container.logs(instance.container_name)
            assert isinstance(current_logs, str), "expected non-streaming container logs"
            logs = current_logs
            if "mem," in logs:
                break
            time.sleep(1)

        assert "mem," in logs, f"expected Telegraf memory metrics in container logs: {logs}"
    finally:
        destroy_container(podman_client, instance.container_name)
