# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
"""Tests for Control Tower authentication and job monitoring."""

from __future__ import annotations

from http import HTTPStatus
from unittest.mock import Mock, call

import client
import pytest

_PIPELINE_ENV = {
    "AZURESUBSCRIPTION_CLIENT_ID": "client-id",
    "AZURESUBSCRIPTION_SERVICE_CONNECTION_ID": "service-connection-id",
    "AZURESUBSCRIPTION_TENANT_ID": "tenant-id",
    "SYSTEM_ACCESSTOKEN": "system-access-token",
}
_EXPECTED_REFRESH_REQUESTS = 2
_INITIAL_AUTH_VALUE = "initial-value"
_REFRESHED_AUTH_VALUE = "refreshed-value"


def test_make_credential_uses_renewable_pipeline_identity(monkeypatch: pytest.MonkeyPatch) -> None:
    """Use AzurePipelinesCredential when AzureCLI@2 provides pipeline context."""
    for name, value in _PIPELINE_ENV.items():
        monkeypatch.setenv(name, value)

    pipeline_credential = Mock(return_value=object())
    cli_credential = Mock(side_effect=AssertionError("AzureCliCredential must not be used"))
    monkeypatch.setattr(client, "AzurePipelinesCredential", pipeline_credential, raising=False)
    monkeypatch.setattr(client, "AzureCliCredential", cli_credential, raising=False)

    client.make_credential()

    pipeline_credential.assert_called_once_with(
        tenant_id="tenant-id",
        client_id="client-id",
        service_connection_id="service-connection-id",
        system_access_token=_PIPELINE_ENV["SYSTEM_ACCESSTOKEN"],
    )
    cli_credential.assert_not_called()


def test_make_credential_uses_azure_cli_outside_pipeline(monkeypatch: pytest.MonkeyPatch) -> None:
    """Keep local execution available through the developer's Azure CLI session."""
    for name in _PIPELINE_ENV:
        monkeypatch.delenv(name, raising=False)

    cli_credential = Mock(return_value=object())
    monkeypatch.setattr(client, "AzureCliCredential", cli_credential, raising=False)

    client.make_credential()

    cli_credential.assert_called_once_with()


def test_make_credential_rejects_partial_pipeline_context(monkeypatch: pytest.MonkeyPatch) -> None:
    """Fail clearly instead of silently selecting a nonrenewable pipeline identity."""
    for name in _PIPELINE_ENV:
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("AZURESUBSCRIPTION_CLIENT_ID", "client-id")

    with pytest.raises(RuntimeError, match="Missing Azure Pipelines credential variables"):
        client.make_credential()


def test_make_request_context_collects_shared_request_state(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Create one context containing transport and renewable-token state."""
    credential = Mock()
    session = Mock()
    events: list[str] = []
    token_calls: list[tuple[object, str]] = []

    def make_credential() -> Mock:
        events.append("credential")
        return credential

    def get_token(received_credential: object, received_audience: str) -> str:
        events.append("token")
        token_calls.append((received_credential, received_audience))
        return _INITIAL_AUTH_VALUE

    def make_session() -> Mock:
        events.append("session")
        return session

    monkeypatch.setattr(client, "make_credential", make_credential)
    monkeypatch.setattr(client, "make_session", make_session)
    monkeypatch.setattr(client, "get_token", get_token)

    request_context = client.make_request_context(
        "https://control-tower.example",
        "api://control-tower",
    )

    assert request_context == client.RequestContext(
        session=session,
        base_url="https://control-tower.example",
        credential=credential,
        audience="api://control-tower",
        token_holder=client.TokenHolder(token=_INITIAL_AUTH_VALUE),
    )
    assert events == ["credential", "token", "session"]
    assert token_calls == [(credential, "api://control-tower")]


def test_request_context_refreshes_rejected_token_once(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Refresh the context's shared token after one unauthorized response."""
    rejected = Mock(status_code=HTTPStatus.UNAUTHORIZED)
    accepted = Mock(status_code=HTTPStatus.OK)
    session = Mock()
    session.request.side_effect = [rejected, accepted]
    credential = Mock()
    request_context = client.RequestContext(
        session=session,
        base_url="https://control-tower.example",
        credential=credential,
        audience="api://control-tower",
        token_holder=client.TokenHolder(token=_INITIAL_AUTH_VALUE),
    )
    get_token = Mock(return_value=_REFRESHED_AUTH_VALUE)
    monkeypatch.setattr(client, "get_token", get_token)

    response = client._request_with_refresh(  # noqa: SLF001 - verify token refresh state
        request_context,
        "POST",
        "https://control-tower.example/api/Scenario/test",
        json_payload={"value": "test"},
    )

    assert response is accepted
    assert request_context.token_holder.token == _REFRESHED_AUTH_VALUE
    get_token.assert_called_once_with(credential, "api://control-tower")
    assert session.request.call_count == _EXPECTED_REFRESH_REQUESTS
    for request_call in session.request.call_args_list:
        assert request_call.args == (
            "POST",
            "https://control-tower.example/api/Scenario/test",
        )
        assert request_call.kwargs["json"] == {"value": "test"}
        assert request_call.kwargs["timeout"] == (10, 60)
    assert session.request.call_args_list[0].kwargs["headers"]["Authorization"] == f"Bearer {_INITIAL_AUTH_VALUE}"
    assert session.request.call_args_list[1].kwargs["headers"]["Authorization"] == f"Bearer {_REFRESHED_AUTH_VALUE}"


def test_request_context_retries_unauthorized_response_only_once(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Return the second rejection without entering an unbounded refresh loop."""
    session = Mock()
    session.request.side_effect = [
        Mock(status_code=HTTPStatus.UNAUTHORIZED),
        Mock(status_code=HTTPStatus.UNAUTHORIZED),
    ]
    request_context = client.RequestContext(
        session=session,
        base_url="https://control-tower.example",
        credential=Mock(),
        audience="api://control-tower",
        token_holder=client.TokenHolder(token=_INITIAL_AUTH_VALUE),
    )
    get_token = Mock(return_value=_REFRESHED_AUTH_VALUE)
    monkeypatch.setattr(client, "get_token", get_token)

    response = client._request_with_refresh(  # noqa: SLF001 - verify bounded token refresh
        request_context,
        "GET",
        "https://control-tower.example/api/Workflow/jobs/status/job-id",
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert session.request.call_count == _EXPECTED_REFRESH_REQUESTS
    get_token.assert_called_once_with(
        request_context.credential,
        request_context.audience,
    )


def test_refreshed_token_is_shared_by_submission_and_polling(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Use a token refreshed during submission for later status polling."""
    rejected = Mock(status_code=HTTPStatus.UNAUTHORIZED)
    submitted = Mock(status_code=HTTPStatus.OK, ok=True)
    submitted.json.return_value = {"jobId": "job-id"}
    polled = Mock(status_code=HTTPStatus.OK, ok=True)
    polled.json.return_value = {"status": "Completed"}
    session = Mock()
    session.request.side_effect = [rejected, submitted, polled]
    request_context = client.RequestContext(
        session=session,
        base_url="https://control-tower.example",
        credential=Mock(),
        audience="api://control-tower",
        token_holder=client.TokenHolder(token=_INITIAL_AUTH_VALUE),
    )
    monkeypatch.setattr(
        client,
        "get_token",
        Mock(return_value=_REFRESHED_AUTH_VALUE),
    )

    submission = client.post_scenario(
        request_context,
        "/api/Scenario/test",
        {"value": "test"},
        context="test",
    )
    status = client.get_job_status(request_context, "job-id")

    assert submission == {"jobId": "job-id"}
    assert status == {"status": "Completed"}
    assert session.request.call_args_list[2].kwargs["headers"]["Authorization"] == (
        f"Bearer {_REFRESHED_AUTH_VALUE}"
    )


@pytest.mark.parametrize(
    ("results", "expected"),
    [
        ({}, (set(), False)),
        ({"buildTasks": []}, (set(), False)),
        ({"buildTasks": [{"kojiInfo": None}]}, (set(), False)),
        ({"buildTasks": [{"kojiInfo": {"kojiTaskNumber": 0}}]}, (set(), False)),
        ({"buildTasks": [{"kojiInfo": {"kojiTaskNumber": True}}]}, (set(), False)),
        ({"buildTasks": [{"kojiInfo": {"kojiTaskNumber": "12345"}}]}, (set(), False)),
        ({"buildTasks": [{"kojiInfo": {"kojiTaskNumber": 12345}}]}, ({12345}, True)),
        (
            {"buildTasks": [
                {"kojiInfo": {"kojiTaskNumber": 12345}},
                {"kojiInfo": {"kojiTaskNumber": 67890}},
            ]},
            ({12345, 67890}, True),
        ),
        (
            {"buildTasks": [
                {"kojiInfo": {"kojiTaskNumber": 12345}},
                {"kojiInfo": {"kojiTaskNumber": 12345}},
            ]},
            ({12345}, True),
        ),
        (
            {"buildTasks": [
                {"kojiInfo": {"kojiTaskNumber": 12345}},
                {"kojiInfo": None},
            ]},
            ({12345}, False),
        ),
        (
            {"buildTasks": [
                {"kojiInfo": None},
                {"kojiInfo": {"kojiTaskNumber": 12345}},
            ]},
            ({12345}, False),
        ),
        (
            {"buildTasks": [
                {"kojiInfo": {"kojiTaskNumber": 12345}},
                None,
            ]},
            ({12345}, False),
        ),
    ],
)
def test_get_koji_task_numbers(
    results: client.JsonObject,
    expected: tuple[set[int], bool],
) -> None:
    """Deduplicate available task numbers without losing pending tasks."""
    response = Mock(ok=True, status_code=HTTPStatus.OK)
    response.json.return_value = results
    request_context = client.RequestContext(
        session=Mock(),
        base_url="https://control-tower.example",
        credential=Mock(),
        audience="api://control-tower",
        token_holder=client.TokenHolder(token=_INITIAL_AUTH_VALUE),
    )
    request_context.session.request = Mock(return_value=response)

    assert client.get_koji_task_numbers(request_context, "job-id") == expected
    assert request_context.session.request.call_args.args == (
        "GET",
        "https://control-tower.example/api/Results/jobs/job-id/koji",
    )


@pytest.mark.parametrize("failure", ["http", "invalid-json", "non-object"])
def test_get_koji_task_numbers_reports_response_errors(
    monkeypatch: pytest.MonkeyPatch,
    failure: str,
) -> None:
    """Surface endpoint failures instead of treating them as pending task IDs."""
    response = Mock(ok=True, status_code=HTTPStatus.OK)
    if failure == "http":
        response.ok = False
        monkeypatch.setattr(client, "format_error", Mock(return_value="request failed"))
        message = "Control Tower Koji results request failed"
    elif failure == "invalid-json":
        response.json.side_effect = ValueError("invalid JSON")
        message = "body was not valid JSON"
    else:
        response.json.return_value = []
        message = "non-object JSON body"
    monkeypatch.setattr(client, "_request_with_refresh", Mock(return_value=response))

    with pytest.raises(RuntimeError, match=message):
        client.get_koji_task_numbers(Mock(), "job-id")


@pytest.mark.parametrize("status", ["Completed", "Failed", "Running"])
def test_poll_logs_koji_task_once_when_available(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    status: str,
) -> None:
    """Log a delayed task assignment before terminal or timeout handling."""
    get_job_status = Mock(
        side_effect=[{"status": "Running"}, {"status": "Running"}, {"status": status}],
    )
    get_koji_task_numbers = Mock(side_effect=[(set(), False), ({12345, 67890}, True)])
    monkeypatch.setattr(client, "get_job_status", get_job_status)
    monkeypatch.setattr(client, "get_koji_task_numbers", get_koji_task_numbers)
    monkeypatch.setattr(client.time, "sleep", Mock())
    monkeypatch.setattr(client.time, "monotonic", Mock(side_effect=[0, 0, 0, 1, 1, 2, 10, 10]))
    request_context = Mock()

    final, timed_out = client.poll_until_terminal(request_context, "job-id", 10)

    assert final == {"status": status}
    assert timed_out is (status == "Running")
    output = capsys.readouterr().out
    assert output.count("Job job-id Koji task IDs:") == 1
    assert "12345" in output
    assert "67890" in output
    assert get_koji_task_numbers.call_args_list == [
        call(request_context, "job-id"),
        call(request_context, "job-id"),
    ]


def test_poll_logs_koji_tasks_incrementally_until_all_assigned(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Log partial assignments once and stop lookups only after completion."""
    monkeypatch.setattr(
        client,
        "get_job_status",
        Mock(side_effect=[{"status": "Running"}] * 4 + [{"status": "Completed"}]),
    )
    get_koji_task_numbers = Mock(side_effect=[
        (set(), False),
        ({12345}, False),
        ({12345}, False),
        ({67890, 12345}, True),
    ])
    monkeypatch.setattr(client, "get_koji_task_numbers", get_koji_task_numbers)
    monkeypatch.setattr(client.time, "sleep", Mock())
    request_context = Mock()

    final, timed_out = client.poll_until_terminal(request_context, "job-id", 10)

    assert final == {"status": "Completed"}
    assert not timed_out
    task_lines = [
        line for line in capsys.readouterr().out.splitlines() if "Koji task IDs:" in line
    ]
    assert task_lines == [
        "Job job-id Koji task IDs: {12345}",
        "Job job-id Koji task IDs: {67890}",
    ]
    assert get_koji_task_numbers.call_args_list == [call(request_context, "job-id")] * 4


@pytest.mark.parametrize("result", [(set(), False), ({12345}, False), ({12345, 67890}, True)])
def test_poll_checks_koji_on_first_terminal_status(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    result: tuple[set[int], bool],
) -> None:
    """Handle jobs that finish before the initial status observation."""
    monkeypatch.setattr(client, "get_job_status", Mock(return_value={"status": "Completed"}))
    get_koji_task_numbers = Mock(return_value=result)
    monkeypatch.setattr(client, "get_koji_task_numbers", get_koji_task_numbers)
    request_context = Mock()

    final, timed_out = client.poll_until_terminal(request_context, "job-id", 10)

    assert final == {"status": "Completed"}
    assert not timed_out
    assert ("Koji task IDs:" in capsys.readouterr().out) is bool(result[0])
    get_koji_task_numbers.assert_called_once_with(request_context, "job-id")


@pytest.mark.parametrize(
    "error",
    [
        RuntimeError("Koji results request failed"),
        client.requests.ConnectionError("connection failed"),
        client.requests.Timeout("request timed out"),
        client.AzureError("token refresh failed"),
    ],
)
@pytest.mark.parametrize("partial_assignment", [False, True])
def test_poll_logs_koji_lookup_errors_without_retrying(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    error: Exception,
    *,
    partial_assignment: bool,
) -> None:
    """Keep monitoring the build but stop task lookups after an operational error."""
    monkeypatch.setattr(
        client,
        "get_job_status",
        Mock(side_effect=[{"status": "Running"}] * 2 + [{"status": "Completed"}]),
    )
    lookup_results = [({12345}, False), error] if partial_assignment else [error]
    get_koji_task_numbers = Mock(side_effect=lookup_results)
    monkeypatch.setattr(client, "get_koji_task_numbers", get_koji_task_numbers)
    monkeypatch.setattr(client.time, "sleep", Mock())

    request_context = Mock()

    final, timed_out = client.poll_until_terminal(request_context, "job-id", 10)

    assert final == {"status": "Completed"}
    assert not timed_out
    output = capsys.readouterr().out
    assert f"##[error]Failed to get Koji task ID for job job-id: {error}" in output
    assert ("Job job-id Koji task IDs: {12345}" in output) is partial_assignment
    assert "Job job-id Koji task IDs: set()" not in output
    expected_calls = 2 if partial_assignment else 1
    assert get_koji_task_numbers.call_args_list == [call(request_context, "job-id")] * expected_calls
