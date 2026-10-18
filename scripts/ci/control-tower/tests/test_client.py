# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
"""Tests for Control Tower credential selection."""

from __future__ import annotations

from http import HTTPStatus
from unittest.mock import Mock

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
