# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
"""Tests for MCP fetch exception boundaries."""

from __future__ import annotations

import importlib.util
import ssl
import subprocess
import urllib.error
import urllib.request
from pathlib import Path
from typing import TYPE_CHECKING, Self

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


def test_koji_fetch_records_ssl_verification_failures(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Record the affected Koji URL before offering insecure access."""
    module = _load_mcp_module(monkeypatch, "koji-mcp.py")
    ssl_error = ssl.SSLError("certificate rejected")

    def raise_ssl_error(*_args: object, **_kwargs: object) -> None:
        raise urllib.error.URLError(ssl_error)

    monkeypatch.setattr(module.urllib.request, "urlopen", raise_ssl_error)
    result = module.koji_fetch("/path", override_base_url="https://example.test")

    assert "SSL certificate verification failed" in result["error"]
    assert module._ssl_errors_seen == {"https://example.test"}  # noqa: SLF001 - verify internal approval gate state


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


@pytest.mark.parametrize(
    ("tool_name", "arguments"),
    [
        (
            "distgit_fetch",
            {
                "path": "relative/path",
            },
        ),
        (
            "distgit_search",
            {
                "package": "example",
                "query": "needle\0suffix",
            },
        ),
        (
            "distgit_show",
            {
                "package": "example",
                "commit": "not-a-sha",
            },
        ),
    ],
)
def test_distgit_validates_base_url_before_tool_arguments(
    monkeypatch: pytest.MonkeyPatch,
    tool_name: str,
    arguments: dict[str, str],
) -> None:
    """Preserve base URL validation precedence over tool-specific checks."""
    module = _load_mcp_module(monkeypatch, "fedora-distgit-mcp.py")

    def fail_if_called(*_args: object, **_kwargs: object) -> None:
        pytest.fail("repository setup must not run for invalid input")

    monkeypatch.setattr(module, "_ensure_repo", fail_if_called)
    result = getattr(module, tool_name)(
        **arguments,
        override_base_url="ftp://example.test",
    )

    assert result["error"] == "Only http/https URLs are supported (got 'ftp')"


def test_distgit_fetch_uses_default_for_empty_override(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Treat an empty override as absent and fetch from the configured base."""
    module = _load_mcp_module(monkeypatch, "fedora-distgit-mcp.py")
    monkeypatch.setattr(module, "_base_url", "https://default.example.test")
    requested_urls: list[str] = []

    class Response:
        def __enter__(self) -> Self:
            return self

        def __exit__(self, *_args: object) -> None:
            return None

        @staticmethod
        def read() -> bytes:
            return b"content"

    def urlopen(request: urllib.request.Request, **_kwargs: object) -> Response:
        requested_urls.append(request.full_url)
        return Response()

    monkeypatch.setattr(module.urllib.request, "urlopen", urlopen)
    monkeypatch.setattr(module, "write_output", lambda *_args, **_kwargs: "written-output")

    result = module.distgit_fetch("/path", override_base_url="")

    assert requested_urls == ["https://default.example.test/path"]
    assert result["output"] == "written-output"


def test_distgit_fetch_rejects_authority_injection(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Reject a path that supplies an authority absent from the base URL."""
    module = _load_mcp_module(monkeypatch, "fedora-distgit-mcp.py")

    def fail_if_called(*_args: object, **_kwargs: object) -> None:
        pytest.fail("blocked URL must not be requested")

    monkeypatch.setattr(module.urllib.request, "urlopen", fail_if_called)

    result = module.distgit_fetch(
        "//169.254.169.254/latest/meta-data",
        override_base_url="http://",
    )

    assert "Constructed URL does not match the configured endpoint" in result["error"]


def test_distgit_show_rejects_git_option_as_commit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Reject a Git option where a hexadecimal commit is required."""
    module = _load_mcp_module(monkeypatch, "fedora-distgit-mcp.py")

    def fail_if_called(*_args: object, **_kwargs: object) -> None:
        pytest.fail("repository setup must not run for an invalid commit")

    monkeypatch.setattr(module, "_ensure_repo", fail_if_called)

    result = module.distgit_show(
        package="example",
        commit="--output=/tmp/distgit-show",
        override_base_url="https://example.test",
    )

    assert result["error"] == "commit must be a hex SHA hash (4-40 chars)."


@pytest.mark.parametrize(
    ("exception", "expected_error"),
    [
        (
            subprocess.TimeoutExpired(["git", "clone"], 120),
            "Clone of https://example.test/rpms/example.git timed out after 120s.",
        ),
        (FileNotFoundError(), "git is not installed or not in PATH."),
    ],
)
def test_distgit_clone_reports_expected_launch_failures(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    exception: Exception,
    expected_error: str,
) -> None:
    """Preserve clone failure translation after extracting clone handling."""
    module = _load_mcp_module(monkeypatch, "fedora-distgit-mcp.py")
    repo_path = tmp_path / "example"

    def raise_exception(*_args: object, **_kwargs: object) -> None:
        if isinstance(exception, subprocess.TimeoutExpired):
            (repo_path / ".git").mkdir(parents=True)
        raise exception

    monkeypatch.setattr(module.subprocess, "run", raise_exception)
    clone_url = "https://example.test/rpms/example.git"

    repo_dir, error = module._clone_repo(  # noqa: SLF001 - verify clone failure cleanup
        str(repo_path),
        clone_url,
    )

    assert repo_dir == ""
    assert error == expected_error
    if isinstance(exception, subprocess.TimeoutExpired):
        assert not repo_path.exists()


def test_distgit_clone_preserves_process_failure_details(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Return git's exit status and diagnostic when cloning fails."""
    module = _load_mcp_module(monkeypatch, "fedora-distgit-mcp.py")
    command = ["git", "clone"]
    repo_path = tmp_path / "example"

    def run(*_args: object, **_kwargs: object) -> subprocess.CompletedProcess[str]:
        (repo_path / ".git").mkdir(parents=True)
        return subprocess.CompletedProcess(
            command,
            23,
            stdout="",
            stderr="repository unavailable\n",
        )

    monkeypatch.setattr(module.subprocess, "run", run)

    repo_dir, error = module._clone_repo(  # noqa: SLF001 - verify process failure cleanup
        str(repo_path),
        "https://example.test/rpms/example.git",
    )

    assert repo_dir == ""
    assert error == "git clone failed (exit 23): repository unavailable"
    assert not repo_path.exists()


def test_distgit_ensure_repo_preserves_clone_command_and_touch(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Clone the expected URL and touch the completed cache entry."""
    module = _load_mcp_module(monkeypatch, "fedora-distgit-mcp.py")
    monkeypatch.setattr(module, "_repos_dir", str(tmp_path / "repos"))
    commands: list[list[str]] = []
    touched: list[str] = []

    def run(command: list[str], **_kwargs: object) -> subprocess.CompletedProcess[str]:
        commands.append(command)
        Path(command[-1]).mkdir()
        return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

    monkeypatch.setattr(module.subprocess, "run", run)
    monkeypatch.setattr(module, "_touch_repo", touched.append)

    repo_dir, error = module._ensure_repo(  # noqa: SLF001 - verify clone setup and cache touching
        "example",
        "https://example.test",
        auto_clean=False,
    )

    assert commands == [
        [
            "git",
            "clone",
            "--quiet",
            "https://example.test/rpms/example.git",
            repo_dir,
        ]
    ]
    assert error is None
    assert touched == [repo_dir]


@pytest.mark.parametrize(
    ("mode", "ref", "expected_tail"),
    [
        ("pickaxe", "rawhide", ["log", "--oneline", "-20", "-Sneedle", "rawhide", "--"]),
        ("pickaxe", "--all", ["log", "--oneline", "-20", "-Sneedle", "--all", "--"]),
        ("grep", "rawhide", ["grep", "-n", "-i", "-e", "needle", "rawhide", "--"]),
        ("log-grep", "rawhide", ["log", "--oneline", "-20", "--grep=needle", "rawhide"]),
        ("log-grep", "--all", ["log", "--oneline", "-20", "--grep=needle", "--all"]),
    ],
)
def test_distgit_search_preserves_git_commands(
    monkeypatch: pytest.MonkeyPatch,
    mode: str,
    ref: str,
    expected_tail: list[str],
) -> None:
    """Build the same git command for every supported search mode."""
    module = _load_mcp_module(monkeypatch, "fedora-distgit-mcp.py")
    monkeypatch.setattr(module, "_ensure_repo", lambda *_args, **_kwargs: ("repo/example", None))
    monkeypatch.setattr(module, "_git_dir", lambda *_args: "repo/example/.git")
    monkeypatch.setattr(module, "write_output", lambda *_args, **_kwargs: "written-output")
    commands: list[list[str]] = []

    def run(command: list[str], **_kwargs: object) -> subprocess.CompletedProcess[str]:
        commands.append(command)
        return subprocess.CompletedProcess(command, 0, stdout="one match\n", stderr="")

    monkeypatch.setattr(module.subprocess, "run", run)

    result = module.distgit_search(
        package="example",
        query="needle",
        ref=ref,
        mode=mode,
        override_base_url="https://example.test",
    )

    assert commands == [["git", "--git-dir", "repo/example/.git", *expected_tail]]
    assert result["output"] == "written-output"
    assert result["repo_dir"] == "repo/example"
