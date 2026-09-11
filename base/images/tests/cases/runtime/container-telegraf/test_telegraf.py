# SPDX-License-Identifier: MIT
"""Validate the container-telegraf workload image.

telegraf is already installed with its packaged default config
(/etc/telegraf/telegraf.conf). That config has no output plugin
enabled (standard upstream telegraf packaging), so the image's default
command intentionally exits non-zero -- this is documented in
containers-workloads.xml and asserted explicitly below, rather than
being an untracked regression.
"""

from __future__ import annotations

from utils.container_runtime import ExecShell

TELEGRAF_CONFIG = "/etc/telegraf/telegraf.conf"


def test_telegraf_version(container_exec_shell: ExecShell) -> None:
    """telegraf binary must report its version."""
    result = container_exec_shell("telegraf --version")
    assert result.exit_code == 0, f"telegraf --version failed: {result.output}"
    assert "Telegraf" in result.output, f"unexpected telegraf --version output: {result.output}"


def test_telegraf_test_mode_emits_mem_metrics(container_exec_shell: ExecShell) -> None:
    """telegraf --test (which bypasses outputs) must gather real input metrics."""
    result = container_exec_shell(f"telegraf --config {TELEGRAF_CONFIG} --test")
    assert result.exit_code == 0, f"telegraf --test failed: {result.output}"
    assert "mem,host" in result.output, f"expected mem metrics in telegraf --test output: {result.output}"


def test_telegraf_default_command_exits_no_outputs_configured(container_exec_shell: ExecShell) -> None:
    """The default command must fail with the documented 'no outputs found' error.

    This pins the known scope limitation: the packaged default config
    ships inputs but no outputs, so running the bare `telegraf` command
    (this image's default OCI Cmd) is expected to exit non-zero rather
    than silently do nothing.
    """
    result = container_exec_shell(f"telegraf --config {TELEGRAF_CONFIG}")
    assert result.exit_code != 0, f"expected telegraf to exit non-zero: {result.output}"
    assert "no outputs found" in result.output, f"expected 'no outputs found' in telegraf output: {result.output}"
