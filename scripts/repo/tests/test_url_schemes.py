# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
"""Tests for repository URL scheme validation."""

from __future__ import annotations

import importlib.machinery
import importlib.util
import sys
import types
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from typing import TYPE_CHECKING
from unittest.mock import patch

import pytest
from _url_utils import validate_repository_url

if TYPE_CHECKING:
    from collections.abc import Iterator


def _load_module(
    path: Path,
    name: str,
    *,
    dependencies: dict[str, types.ModuleType] | None = None,
) -> types.ModuleType:
    """Load a repository tool with optional native dependency stubs."""
    loader = importlib.machinery.SourceFileLoader(name, str(path))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    if spec is None:
        pytest.fail(f"Unable to load module spec for {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    with patch.dict(sys.modules, dependencies or {}):
        loader.exec_module(module)
    return module


def _load_dnf_wrapper() -> types.ModuleType:
    """Load the extensionless dnf wrapper as a Python module."""
    path = Path(__file__).resolve().parents[1] / "dnf-with-azl-repos"
    return _load_module(path, "_test_dnf_with_azl_repos")


def _load_repodata_synthesizer() -> types.ModuleType:
    """Load the synthesizer with its unavailable native module stubbed."""
    path = Path(__file__).resolve().parents[1] / "synthesize-repodata.py"
    createrepo = types.ModuleType("createrepo_c")
    for name in (
        "FilelistsSqlite",
        "FilelistsXmlFile",
        "OtherSqlite",
        "OtherXmlFile",
        "PrimarySqlite",
        "PrimaryXmlFile",
    ):
        setattr(createrepo, name, type(name, (), {}))
    return _load_module(
        path,
        "_test_synthesize_repodata",
        dependencies={"createrepo_c": createrepo},
    )


def test_synthesizer_rejects_missing_repositories_before_output_setup(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Reject missing inputs without touching the requested output path."""
    module = _load_repodata_synthesizer()
    output_path = tmp_path / "existing-output"
    original_content = "leave this file untouched"
    output_path.write_text(original_content, encoding="utf-8")
    args = types.SimpleNamespace(
        arch=[],
        ca_bundle=None,
        insecure=False,
        repo_sources=[],
        output_dir=output_path,
        repo_root=tmp_path,
        keep_cache=False,
    )
    monkeypatch.setattr(module, "parse_args", lambda _argv: args)

    assert module.main([]) == 1
    assert capsys.readouterr().err == "ERROR: at least one --repo-prefix or --repo must be provided\n"
    assert output_path.read_text(encoding="utf-8") == original_content


class _FtpRedirectHandler(BaseHTTPRequestHandler):
    """Redirect every request to a disallowed FTP target."""

    def _redirect(self) -> None:
        self.send_response(302)
        self.send_header("Location", "ftp://packages.example.test/repo")
        self.end_headers()

    def do_GET(self) -> None:
        """Redirect GET requests."""
        self._redirect()

    def do_HEAD(self) -> None:
        """Redirect HEAD requests."""
        self._redirect()

    def log_message(self, format: str, *args: object) -> None:  # noqa: A002 - BaseHTTPRequestHandler API
        """Suppress test-server request logs."""


@contextmanager
def _ftp_redirect_server() -> Iterator[str]:
    """Run a local server that redirects requests to FTP."""
    server = ThreadingHTTPServer(("127.0.0.1", 0), _FtpRedirectHandler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://{server.server_name}:{server.server_port}"
    finally:
        server.shutdown()
        thread.join()
        server.server_close()


@pytest.mark.parametrize(
    "url",
    [
        "file:///tmp/repo",
        "http://packages.example.test/repo",
        "https://packages.example.test/repo",
    ],
)
def test_validate_repository_url_accepts_supported_schemes(url: str) -> None:
    """Accept the repository transports supported by the tools."""
    validate_repository_url(url)


@pytest.mark.parametrize(
    "url",
    [
        "repo/path",
        "data:text/plain,repo",
        "ftp://packages.example.test/repo",
    ],
)
def test_validate_repository_url_rejects_unexpected_schemes(url: str) -> None:
    """Reject repository transports outside the audited policy."""
    with pytest.raises(ValueError, match="unsupported scheme"):
        validate_repository_url(url)


def test_probe_repo_accepts_file_repository(tmp_path: Path) -> None:
    """Probe a local file repository through the audited URL-open path."""
    repodata = tmp_path / "repodata"
    repodata.mkdir()
    (repodata / "repomd.xml").write_text("<repomd/>")

    wrapper = _load_dnf_wrapper()
    status, error = wrapper.probe_repo(tmp_path.as_uri())

    assert status == "ok"
    assert error is None


def test_probe_repo_rejects_redirect_to_ftp() -> None:
    """Reject a repository probe redirected to a disallowed transport."""
    wrapper = _load_dnf_wrapper()

    with _ftp_redirect_server() as url:
        status, error = wrapper.probe_repo(url)

    assert status == "fail"
    assert error is not None
    assert "unsupported scheme 'ftp'" in error


def test_http_get_rejects_redirect_to_ftp(tmp_path: Path) -> None:
    """Reject a metadata download redirected to a disallowed transport."""
    synthesizer = _load_repodata_synthesizer()

    with _ftp_redirect_server() as url, pytest.raises(ValueError, match="unsupported scheme 'ftp'"):
        synthesizer._http_get(  # noqa: SLF001 - direct regression coverage for the download boundary
            url,
            tmp_path / "download",
            None,
            retries=1,
        )


def test_synthesizer_reports_redirect_to_ftp(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """Report a blocked redirect through the synthesizer's fatal-error path."""
    synthesizer = _load_repodata_synthesizer()

    with _ftp_redirect_server() as url:
        status = synthesizer.main(
            [
                "--repo",
                f"main:{url}/x86_64",
                "--output-dir",
                str(tmp_path / "output"),
            ]
        )

    assert status == 1
    assert "ERROR: repository redirect URL has unsupported scheme 'ftp'" in capsys.readouterr().err
