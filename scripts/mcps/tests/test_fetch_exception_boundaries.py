# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
"""Tests for MCP fetch exception boundaries."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import TYPE_CHECKING

import _mcp_utils
import pytest

if TYPE_CHECKING:
    from types import ModuleType

_MCP_DIR = Path(__file__).resolve().parents[1]


def _load_mcp_module(monkeypatch: pytest.MonkeyPatch, filename: str) -> ModuleType:
    """Load a hyphenated MCP entrypoint without reading environment files."""
    monkeypatch.setattr(_mcp_utils, "load_env", lambda: None)
    script_path = _MCP_DIR / filename
    spec = importlib.util.spec_from_file_location(f"_test_{script_path.stem}", script_path)
    if spec is None or spec.loader is None:
        pytest.fail(f"Unable to load module spec for {script_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize(
    ("filename", "fetch_name"),
    [
        ("fedora-distgit-mcp.py", "distgit_fetch"),
        ("koji-mcp.py", "koji_fetch"),
    ],
)
def test_fetch_reports_expected_transport_errors(
    monkeypatch: pytest.MonkeyPatch,
    filename: str,
    fetch_name: str,
) -> None:
    """Return structured errors for expected URL transport failures."""
    module = _load_mcp_module(monkeypatch, filename)

    def raise_os_error(*_args: object, **_kwargs: object) -> None:
        raise OSError

    monkeypatch.setattr(module.urllib.request, "urlopen", raise_os_error)
    result = getattr(module, fetch_name)("/path", override_base_url="https://example.test")

    assert "can't fetch" in result["error"]


@pytest.mark.parametrize(
    ("filename", "fetch_name"),
    [
        ("fedora-distgit-mcp.py", "distgit_fetch"),
        ("koji-mcp.py", "koji_fetch"),
    ],
)
def test_fetch_does_not_hide_unexpected_errors(
    monkeypatch: pytest.MonkeyPatch,
    filename: str,
    fetch_name: str,
) -> None:
    """Allow unexpected programming errors to propagate to the MCP runtime."""
    module = _load_mcp_module(monkeypatch, filename)

    def raise_runtime_error(*_args: object, **_kwargs: object) -> None:
        raise RuntimeError

    monkeypatch.setattr(module.urllib.request, "urlopen", raise_runtime_error)

    with pytest.raises(RuntimeError):
        getattr(module, fetch_name)("/path", override_base_url="https://example.test")


@pytest.mark.parametrize(
    ("tool_name", "arguments"),
    [
        (
            "distgit_search",
            {
                "package": "example",
                "query": "needle",
                "mode": "grep",
                "override_base_url": "https://example.test",
            },
        ),
        (
            "distgit_show",
            {
                "package": "example",
                "commit": "deadbeef",
                "override_base_url": "https://example.test",
            },
        ),
    ],
)
def test_distgit_reports_git_output_decode_errors(
    monkeypatch: pytest.MonkeyPatch,
    tool_name: str,
    arguments: dict[str, str],
) -> None:
    """Return structured errors when git emits non-UTF-8 output."""
    module = _load_mcp_module(monkeypatch, "fedora-distgit-mcp.py")
    monkeypatch.setattr(module, "_ensure_repo", lambda *_args, **_kwargs: ("repo/example", None))
    decode_error = UnicodeDecodeError("utf-8", b"\xff", 0, 1, "invalid start byte")

    def raise_decode_error(*_args: object, **_kwargs: object) -> None:
        raise decode_error

    monkeypatch.setattr(module.subprocess, "run", raise_decode_error)
    result = getattr(module, tool_name)(**arguments)

    assert "running git:" in result["error"]


@pytest.mark.parametrize(
    ("query", "ref", "field"),
    [
        ("needle\0suffix", "rawhide", "query"),
        ("needle", "rawhide\0suffix", "ref"),
    ],
)
def test_distgit_search_rejects_nul_arguments(
    monkeypatch: pytest.MonkeyPatch,
    query: str,
    ref: str,
    field: str,
) -> None:
    """Reject NUL-containing Git arguments before launching a subprocess."""
    module = _load_mcp_module(monkeypatch, "fedora-distgit-mcp.py")

    def fail_if_called(*_args: object, **_kwargs: object) -> None:
        pytest.fail("repository setup must not run for invalid input")

    monkeypatch.setattr(module, "_ensure_repo", fail_if_called)
    result = module.distgit_search(
        package="example",
        query=query,
        ref=ref,
        mode="grep",
        override_base_url="https://example.test",
    )

    assert result["error"] == f"{field} must not contain NUL characters."
