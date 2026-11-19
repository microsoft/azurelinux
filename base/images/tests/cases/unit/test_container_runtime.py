# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
"""Regression tests for credential-safe container diagnostics."""

from __future__ import annotations

import logging
from unittest.mock import Mock, call

import pytest
from python_on_whales import DockerClient
from utils import container_runtime
from utils.container_runtime import ContainerExecResult, exec_in_container, wait_until_service_ready


@pytest.mark.parametrize(
    ("text", "values", "expected"),
    [
        ("PGPASSWORD=value psql", ("value",), "PGPASSWORD=<redacted> psql"),
        (
            "printf %s longer-value value longer-value",
            ("value", "longer-value", "value"),
            "printf %s <redacted> <redacted> <redacted>",
        ),
        ("printf %s pa'ss\\word\n[value].*", ("pa'ss\\word\n[value].*",), "printf %s <redacted>"),
        ("echo ready", (), "echo ready"),
    ],
)
def test_exec_masks_diagnostics_without_changing_execution(
    text: str,
    values: tuple[str, ...],
    expected: str,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Mask literals before argv formatting, preserving raw execution/results."""
    client = Mock(spec=DockerClient())
    client.container.execute.return_value = iter([("stdout", text.encode()), ("stderr", b"diagnostic")])
    command = ["bash", "-c", text]

    with caplog.at_level(logging.DEBUG, logger=container_runtime.__name__):
        result = exec_in_container(client, "test-container", command, sensitive_values=values)

    client.container.execute.assert_called_once_with("test-container", ["bash", "-c", text], stream=True)
    assert command == ["bash", "-c", text], "Masking must not mutate the caller's command"
    assert result == ContainerExecResult(0, text, "diagnostic", text + "diagnostic")
    assert caplog.messages == [f"Container exec [test-container]: {['bash', '-c', expected]}"]


def test_exec_omits_command_by_default(caplog: pytest.LogCaptureFixture) -> None:
    """Callers without credential metadata must not expose command arguments."""
    client = Mock(spec=DockerClient())
    client.container.execute.return_value = iter([])
    command = ["bash", "-c", "PGPASSWORD=unregistered-value psql"]

    with caplog.at_level(logging.DEBUG, logger=container_runtime.__name__):
        exec_in_container(client, "test-container", command)

    client.container.execute.assert_called_once_with("test-container", command, stream=True)
    assert caplog.messages == ["Container exec [test-container]: <omitted>"]


@pytest.mark.parametrize(
    ("values", "expected_command", "expected_output"),
    [
        (
            ("longer-value", "value"),
            "PGPASSWORD=<redacted> psql",
            "psql: <redacted> denied; <redacted> echoed",
        ),
        (
            (),
            "PGPASSWORD=longer-value psql",
            "psql: longer-value denied; value echoed",
        ),
    ],
)
def test_readiness_timeout_masks_command_and_output(
    values: tuple[str, ...],
    expected_command: str,
    expected_output: str,
) -> None:
    """Keep useful timeout context while masking both command and probe output."""
    command = "PGPASSWORD=longer-value psql"
    output = "psql: longer-value denied; value echoed"
    execute = Mock(return_value=ContainerExecResult(2, "", output, output))
    attempts = 2

    with pytest.raises(AssertionError) as exc_info:
        wait_until_service_ready(execute, command, attempts=attempts, delay=0, sensitive_values=values)

    assert str(exc_info.value) == (
        f"Service never became ready (attempts={attempts}, last_exit_code=2): "
        f"command={expected_command!r}, output={expected_output!r}"
    )
    assert execute.call_args_list == [call(command)] * attempts


@pytest.mark.parametrize("attempts", [0, 2])
def test_readiness_timeout_omits_text_by_default(attempts: int) -> None:
    """Unregistered command/output values stay out of readiness errors."""
    command = "PGPASSWORD=unregistered-value psql"
    execute = Mock(return_value=ContainerExecResult(1, "", "unregistered-output", "unregistered-output"))

    with pytest.raises(AssertionError) as exc_info:
        wait_until_service_ready(execute, command, attempts=attempts, delay=0)

    message = str(exc_info.value)
    assert "unregistered-value" not in message
    assert "unregistered-output" not in message
    assert "command='<omitted>', output='<omitted>'" in message
    assert execute.call_count == attempts


def test_readiness_preserves_retries_and_returned_results(monkeypatch: pytest.MonkeyPatch) -> None:
    """Redaction must not alter readiness checks, delays, or successful output."""
    command = "PGPASSWORD=value psql"
    success = ContainerExecResult(0, "ready value", "", "ready value")
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
        execute, command, contains="ready", attempts=attempts, delay=delay, sensitive_values=("value",),
    )

    assert result is success, "Successful results must be returned without masking"
    assert execute.call_args_list == [call(command)] * attempts
    assert sleep.call_args_list == [call(delay)] * (attempts - 1)


def test_empty_sensitive_values_are_rejected_before_execution() -> None:
    """An empty literal is invalid and must not trigger command execution."""
    client = Mock(spec=DockerClient())
    execute = Mock()

    with pytest.raises(ValueError, match="Sensitive values must not be empty"):
        exec_in_container(client, "test-container", ["echo", "ready"], sensitive_values=("",))
    with pytest.raises(ValueError, match="Sensitive values must not be empty"):
        wait_until_service_ready(execute, "echo ready", sensitive_values=("",))

    client.container.execute.assert_not_called()
    execute.assert_not_called()
