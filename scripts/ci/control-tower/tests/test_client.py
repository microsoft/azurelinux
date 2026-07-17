"""Tests for Control Tower HTTP and authentication diagnostics."""

from __future__ import annotations

import base64
import json
from unittest.mock import Mock

import client
import pytest
import requests


def _jwt(claims: dict[str, object]) -> str:
    """Build a signature-free JWT-shaped value for diagnostic tests."""

    def encode(value: dict[str, object]) -> str:
        raw = json.dumps(value).encode()
        return base64.urlsafe_b64encode(raw).decode().rstrip("=")

    return f"{encode({'alg': 'none'})}.{encode(claims)}.signature"


def test_get_token_prints_safe_claims_without_raw_token(capsys: pytest.CaptureFixture[str]) -> None:
    """Log identity claims while keeping the bearer token secret."""
    token = _jwt(
        {
            "aud": "api://control-tower",
            "appid": "client-id",
            "roles": ["ControlTower.Invoke"],
            "tid": "tenant-id",
        }
    )
    credential = Mock()
    credential.get_token.return_value = Mock(token=token)

    assert client.get_token(credential, "api://control-tower") == token

    output = capsys.readouterr().out
    assert token not in output
    assert "Mock token claims" in output
    assert '"aud": "api://control-tower"' in output
    assert '"appid": "client-id"' in output
    assert '"roles": [' in output
    assert '"tid": "tenant-id"' in output


def test_format_error_includes_safe_gateway_headers() -> None:
    """Surface request correlation and authentication challenge headers."""
    response = requests.Response()
    response.status_code = 401
    response.reason = "Unauthorized"
    response.url = "https://control-tower.example/api/Scenario/prcheck"
    response.request = requests.Request("POST", response.url).prepare()
    response.headers.update(
        {
            "apim-request-id": "apim-correlation",
            "WWW-Authenticate": 'Bearer error="invalid_token"',
            "x-azure-ref": "front-door-correlation",
        }
    )
    response._content = b""

    diagnostic = client.format_error(response)

    assert "apim-request-id: apim-correlation" in diagnostic
    assert 'WWW-Authenticate: Bearer error="invalid_token"' in diagnostic
    assert "x-azure-ref: front-door-correlation" in diagnostic
