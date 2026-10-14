"""Tests for Control Tower credential selection."""

from __future__ import annotations

from unittest.mock import Mock

import client
import pytest

_PIPELINE_ENV = {
    "AZURESUBSCRIPTION_CLIENT_ID": "client-id",
    "AZURESUBSCRIPTION_SERVICE_CONNECTION_ID": "service-connection-id",
    "AZURESUBSCRIPTION_TENANT_ID": "tenant-id",
    "SYSTEM_ACCESSTOKEN": "system-access-token",
}


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


def test_get_koji_package_results_uses_package_endpoint() -> None:
    """Request the package-specific result shape used by the probe."""
    response = Mock(ok=True, status_code=200)
    response.json.return_value = {"buildTasks": []}
    session = Mock()
    session.request.return_value = response

    result = client.get_koji_package_results(
        session,
        "https://control-tower.example",
        Mock(),
        "api://control-tower",
        client.TokenHolder(token=""),
        "job-id",
    )

    assert result == {"buildTasks": []}
    session.request.assert_called_once()
    request_args, request_kwargs = session.request.call_args
    assert request_args == (
        "GET",
        "https://control-tower.example/api/Results/jobs/job-id/koji/packages",
    )
    assert request_kwargs["timeout"] == (10, 60)
