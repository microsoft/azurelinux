# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
"""Behavioral tests for MCP request-pipeline helpers."""

from __future__ import annotations

import http.client
import importlib.util
import ssl
import subprocess
import urllib.error
import urllib.request
from email.message import Message
from pathlib import Path
from typing import TYPE_CHECKING

import _mcp_utils
import pytest

if TYPE_CHECKING:
    from types import ModuleType
    from typing import Self

_MCP_DIR = Path(__file__).resolve().parents[1]


def _load_module(monkeypatch: pytest.MonkeyPatch, filename: str) -> ModuleType:
    """Load a hyphenated MCP entrypoint without starting stdio."""
    monkeypatch.setattr(_mcp_utils, "load_env", lambda: None)
    script_path = _MCP_DIR / filename
    module_name = f"_test_{filename.removesuffix('.py').replace('-', '_')}"
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    if spec is None or spec.loader is None:
        pytest.fail(f"Unable to load module spec for {script_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_distgit_clone_timeout_preserves_error(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Translate clone timeouts and remove the partial repository."""
    distgit = _load_module(monkeypatch, "fedora-distgit-mcp.py")
    repo_dir = tmp_path / "repos" / "example"

    def timeout(*_args: object, **_kwargs: object) -> None:
        raise subprocess.TimeoutExpired(["git", "clone"], 120)

    monkeypatch.setattr(distgit.subprocess, "run", timeout)

    path, error = distgit._clone_repo(  # noqa: SLF001 - exercising extracted boundary
        repo_dir,
        "https://example.test/rpms/example.git",
    )

    assert path == ""
    assert error == "Clone of https://example.test/rpms/example.git timed out after 120s."
    assert not repo_dir.exists()


def test_distgit_fetch_preserves_http_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """Return the existing HTTP failure message and status fields."""
    distgit = _load_module(monkeypatch, "fedora-distgit-mcp.py")

    def fail_request(*_args: object, **_kwargs: object) -> None:
        raise urllib.error.HTTPError(
            "https://example.test/missing",
            404,
            "Not Found",
            Message(),
            None,
        )

    monkeypatch.setattr(distgit.urllib.request, "urlopen", fail_request)

    result = distgit.distgit_fetch("/missing", "https://example.test")

    assert result["error"] == "HTTP 404 fetching https://example.test/missing: Not Found"
    assert result["default_base_url"] == "https://src.fedoraproject.org"


def test_distgit_fetch_preserves_incomplete_response(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Translate incomplete HTTP responses through the public MCP result."""
    distgit = _load_module(monkeypatch, "fedora-distgit-mcp.py")

    class IncompleteResponse:
        def __enter__(self) -> Self:
            return self

        def __exit__(self, *_args: object) -> None:
            return None

        def read(self) -> bytes:
            raise http.client.IncompleteRead(b"partial", 10)

    monkeypatch.setattr(
        distgit.urllib.request,
        "urlopen",
        lambda *_args, **_kwargs: IncompleteResponse(),
    )

    result = distgit.distgit_fetch("/partial", "https://example.test")

    assert result["error"].startswith(
        "can't fetch https://example.test/partial: IncompleteRead"
    )


def test_distgit_fetch_preserves_non_ascii_url_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Translate urllib encoding failures through the public MCP result."""
    distgit = _load_module(monkeypatch, "fedora-distgit-mcp.py")

    def fail_request(request: urllib.request.Request, **_kwargs: object) -> None:
        assert "pürge" in request.full_url
        raise UnicodeEncodeError("ascii", "pürge", 1, 2, "ordinal not in range")

    monkeypatch.setattr(distgit.urllib.request, "urlopen", fail_request)

    result = distgit.distgit_fetch("/pürge.log", "https://example.test")

    assert result["error"].startswith(
        "can't fetch https://example.test/pürge.log: "
    )


def test_distgit_search_preserves_invalid_command_input(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Translate invalid subprocess arguments through the search result."""
    distgit = _load_module(monkeypatch, "fedora-distgit-mcp.py")

    def fail_command(*_args: object, **_kwargs: object) -> None:
        raise ValueError("embedded null byte")

    monkeypatch.setattr(distgit.subprocess, "run", fail_command)

    output, error = distgit._run_search_command(  # noqa: SLF001
        ["git", "grep", "bad\0query"],
        "grep",
        "bad\0query",
        "example",
        "rawhide",
    )

    assert output == ""
    assert error is not None
    assert error["error"] == "running git: embedded null byte"


def test_distgit_git_commands_preserve_decode_errors(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Translate invalid Git output encoding through both command helpers."""
    distgit = _load_module(monkeypatch, "fedora-distgit-mcp.py")
    decode_error = UnicodeDecodeError("utf-8", b"\xff", 0, 1, "invalid start byte")

    def fail_command(*_args: object, **_kwargs: object) -> None:
        raise decode_error

    monkeypatch.setattr(distgit.subprocess, "run", fail_command)

    search_output, search_error = distgit._run_search_command(  # noqa: SLF001
        ["git", "log"],
        "log-grep",
        "example",
        "example",
        "rawhide",
    )
    show_output, show_error = distgit._run_git_show(".git", "abcd")  # noqa: SLF001

    assert search_output == ""
    assert search_error is not None
    assert search_error["error"].startswith("running git: 'utf-8' codec")
    assert show_output == ""
    assert show_error is not None
    assert show_error.startswith("running git: 'utf-8' codec")


def test_distgit_show_preserves_git_failure(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Return git-show failures through the public MCP response."""
    distgit = _load_module(monkeypatch, "fedora-distgit-mcp.py")
    monkeypatch.setattr(
        distgit,
        "_ensure_repo",
        lambda *_args, **_kwargs: (str(tmp_path / "example"), None),
    )
    monkeypatch.setattr(
        distgit,
        "_run_git_show",
        lambda *_args: ("", "git show failed (exit 128): bad object"),
    )

    result = distgit.distgit_show("example", "abcd")

    assert result["error"] == "git show failed (exit 128): bad object"


@pytest.mark.parametrize(
    ("path", "base_url", "expected_error"),
    [
        (
            "/taskinfo",
            None,
            "No Koji URL available. Pass override_base_url or call set_koji_url first.",
        ),
        ("taskinfo", "https://koji.example.test", "path must start with '/'"),
    ],
)
def test_koji_fetch_preserves_request_validation(
    monkeypatch: pytest.MonkeyPatch,
    path: str,
    base_url: str | None,
    expected_error: str,
) -> None:
    """Reject missing endpoints and malformed paths before network access."""
    koji = _load_module(monkeypatch, "koji-mcp.py")

    result = koji.koji_fetch(path, base_url)

    assert result["error"] == expected_error


def test_koji_fetch_preserves_connectivity_guidance(monkeypatch: pytest.MonkeyPatch) -> None:
    """Keep the network-access guidance attached to ordinary URL failures."""
    koji = _load_module(monkeypatch, "koji-mcp.py")

    def fail_request(*_args: object, **_kwargs: object) -> None:
        raise urllib.error.URLError("connection refused")

    monkeypatch.setattr(koji.urllib.request, "urlopen", fail_request)

    result = koji.koji_fetch("/taskinfo", "https://koji.example.test")

    assert result["error"].startswith(
        "can't fetch https://koji.example.test/taskinfo: <urlopen error connection refused>."
    )
    assert "verify that you are connected to the appropriate network" in result["error"]


def test_koji_fetch_preserves_incomplete_response(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Translate incomplete HTTP responses through the public MCP result."""
    koji = _load_module(monkeypatch, "koji-mcp.py")

    class IncompleteResponse:
        def __enter__(self) -> Self:
            return self

        def __exit__(self, *_args: object) -> None:
            return None

        def read(self) -> bytes:
            raise http.client.IncompleteRead(b"partial", 10)

    monkeypatch.setattr(
        koji.urllib.request,
        "urlopen",
        lambda *_args, **_kwargs: IncompleteResponse(),
    )

    result = koji.koji_fetch("/partial", "https://koji.example.test")

    assert result["error"].startswith(
        "can't fetch https://koji.example.test/partial: IncompleteRead"
    )
    assert "verify that you are connected to the appropriate network" in result["error"]


def test_koji_fetch_preserves_non_ascii_url_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Translate urllib encoding failures through the public MCP result."""
    koji = _load_module(monkeypatch, "koji-mcp.py")

    def fail_request(request: urllib.request.Request, **_kwargs: object) -> None:
        assert "pürge" in request.full_url
        raise UnicodeEncodeError("ascii", "pürge", 1, 2, "ordinal not in range")

    monkeypatch.setattr(koji.urllib.request, "urlopen", fail_request)

    result = koji.koji_fetch("/pürge.log", "https://koji.example.test")

    assert result["error"].startswith(
        "can't fetch https://koji.example.test/pürge.log: "
    )
    assert "verify that you are connected to the appropriate network" in result["error"]


def test_koji_fetch_records_ssl_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """Record certificate failures so insecure mode can require prior evidence."""
    koji = _load_module(monkeypatch, "koji-mcp.py")

    def fail_request(*_args: object, **_kwargs: object) -> None:
        raise urllib.error.URLError(ssl.SSLCertVerificationError("self signed"))

    monkeypatch.setattr(koji.urllib.request, "urlopen", fail_request)

    result = koji.koji_fetch("/taskinfo", "https://koji.example.test")

    assert result["error"].startswith(
        "SSL certificate verification failed for https://koji.example.test/taskinfo:"
    )
    allowed = koji.koji_allow_insecure("https://koji.example.test")
    assert allowed["allowed_url"] == "https://koji.example.test"
