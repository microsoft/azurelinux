# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
"""Tests for MCP endpoint URL validation."""

from __future__ import annotations

import pytest
from _mcp_utils import validate_base_url


@pytest.mark.parametrize(
    "url",
    [
        "http://example.test",
        "https://example.test/path/",
    ],
)
def test_validate_base_url_accepts_http_endpoints(url: str) -> None:
    """Accept HTTP and HTTPS MCP endpoints."""
    normalized, error = validate_base_url(url)
    assert normalized
    assert error is None


@pytest.mark.parametrize(
    "url",
    [
        "file:///tmp/repo",
        "ftp://example.test",
    ],
)
def test_validate_base_url_rejects_non_http_endpoints(url: str) -> None:
    """Reject endpoint schemes that bypass MCP network policy."""
    normalized, error = validate_base_url(url)
    assert normalized == ""
    assert error is not None
