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
