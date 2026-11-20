# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
"""Regression tests for separate execution and diagnostic commands."""

from __future__ import annotations

import logging
from functools import partial
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from unittest.mock import Mock, call

import pytest
from python_on_whales import DockerClient
from utils import container_runtime
from utils.container_runtime import ContainerExecResult, exec_in_container, wait_until_service_ready


@pytest.mark.parametrize("display", [None, [], ["bash", "-c", "PGPASSWORD=<redacted> psql"]])
def test_exec_logs_only_display_command(
    display: list[str] | None, caplog: pytest.LogCaptureFixture,
) -> None:
    """Execute real arguments and return raw output, but log only display arguments."""
    client = Mock(spec=DockerClient())
    text = "PGPASSWORD=test-credential psql"
    client.container.execute.return_value = iter([("stdout", text.encode()), ("stderr", b"diagnostic")])
    command = ["bash", "-c", text]

    with caplog.at_level(logging.DEBUG, logger=container_runtime.__name__):
        result = exec_in_container(client, "test-container", command, command_for_log=display)

    client.container.execute.assert_called_once_with("test-container", ["bash", "-c", text], stream=True)
    assert command == ["bash", "-c", text], "Diagnostics must not mutate the real command"
    assert result == ContainerExecResult(0, text, "diagnostic", text + "diagnostic")
    expected_display = "<command omitted>" if display is None else display
    assert caplog.messages == [f"Container exec [test-container]: {expected_display}"]
    assert "test-credential" not in caplog.text


@pytest.mark.parametrize("display", [None, "", "PGPASSWORD=<redacted> psql --command='SELECT 1;'"])
@pytest.mark.parametrize("attempts", [0, 2])
def test_readiness_uses_display_without_exposing_command_or_output(display: str | None, attempts: int) -> None:
    """Forward display metadata and include only it and numeric context in errors."""
    command = "PGPASSWORD=test-credential psql"
    output = "probe-output-with-credentials"
    execute = Mock(return_value=ContainerExecResult(2, "", output, output))
    wait = partial(wait_until_service_ready, command_for_log=display)

    with pytest.raises(AssertionError) as exc_info:
        wait(execute, command, attempts=attempts, delay=0)

    expected_display = "<command omitted>" if display is None else display
    expected_exit_code = None if attempts == 0 else 2
    message = str(exc_info.value)
    assert message == (
        f"Service never became ready (attempts={attempts}, last_exit_code={expected_exit_code}): "
        f"{expected_display}"
    )
    expected_call = call(command) if display is None else call(command, command_for_log=display)
    assert execute.call_args_list == [expected_call] * attempts
    assert "test-credential" not in message
    assert output not in message


@pytest.mark.parametrize("display", [None, "PGPASSWORD=<redacted> psql"])
def test_readiness_preserves_retries_and_returned_results(
    display: str | None, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Diagnostics must not alter readiness checks, delays, or successful output."""
    command = "PGPASSWORD=test-credential psql"
    success = ContainerExecResult(0, "ready test-credential", "", "ready test-credential")
    execute = Mock(side_effect=[
        ContainerExecResult(1, "", "not yet", "not yet"),
        ContainerExecResult(0, "starting", "", "starting"),
        success,
    ])
    sleep = Mock()
    monkeypatch.setattr(container_runtime.time, "sleep", sleep)
    attempts = 3
    delay = 0.25

    result = wait_until_service_ready(
        execute, command, contains="ready", attempts=attempts, delay=delay, command_for_log=display,
    )

    assert result is success, "Successful results must be returned unchanged"
    expected_call = call(command) if display is None else call(command, command_for_log=display)
    assert execute.call_args_list == [expected_call] * attempts
    assert sleep.call_args_list == [call(delay)] * (attempts - 1)


def test_postgres_workflow_supplies_redacted_display_commands(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path,
) -> None:
    """Keep SQL details visible while both valid and invalid passwords stay out."""
    path = Path(__file__).resolve().parents[1] / "runtime" / "container-postgres" / "test_postgres.py"
    spec = spec_from_file_location("postgres_workload_tests", path)
    if spec is None or spec.loader is None:
        pytest.fail("Cannot load PostgreSQL workload tests")
    postgres = module_from_spec(spec)
    spec.loader.exec_module(postgres)
    monkeypatch.setattr(postgres, "create_container", Mock())
    monkeypatch.setattr(postgres, "destroy_container", Mock())
    responses = [
        ContainerExecResult(0, "1\n", "", "1\n"),
        ContainerExecResult(1, "", "authentication failed", "authentication failed"),
        ContainerExecResult(0, "CREATE TABLE", "", "CREATE TABLE"),
        ContainerExecResult(0, "INSERT 0 2", "", "INSERT 0 2"),
        ContainerExecResult(0, "San Francisco|(-194,53)\nSeattle|(-150,86)\n", "", ""),
        ContainerExecResult(0, "postgres\n", "", "postgres\n"),
    ]
    execute = Mock(side_effect=responses)
    monkeypatch.setattr(postgres, "exec_in_container", execute)
    client = Mock(spec=DockerClient())

    postgres.test_postgres_default_command_initializes_and_serves(client, "test-image", tmp_path)

    assert execute.call_count == len(responses)
    for invocation in execute.call_args_list[:-1]:
        real = invocation.args[2]
        display = invocation.kwargs["command_for_log"]
        expected = real[2].replace(postgres.POSTGRES_PASSWORD, "<redacted>").replace(
            "PGPASSWORD=wrong", "PGPASSWORD=<redacted>",
        )
        assert display == ["bash", "-c", expected]
        assert "PGPASSWORD=<redacted>" in display[2]
