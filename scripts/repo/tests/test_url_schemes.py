# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
"""Repository URL scheme policy tests."""

from __future__ import annotations

import importlib.machinery
import importlib.util
import urllib.error
import urllib.request
from email.message import Message
from http import HTTPStatus
from pathlib import Path
from typing import TYPE_CHECKING, Protocol, cast

import pytest
from _repo_layout import UnsupportedRepoSchemeError, validate_repo_url

if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import Self


class _DnfModule(Protocol):
    def probe_repo(self, probe_url: str, *, timeout: float = 30.0) -> tuple[str, str | None]:
        """Describe the dnf wrapper's repository probe."""
        ...


@pytest.fixture
def dnf_module() -> _DnfModule:
    """Load the extensionless dnf wrapper as a module."""
    script_path = Path(__file__).resolve().parents[1] / "dnf-with-azl-repos"
    loader = importlib.machinery.SourceFileLoader("_test_dnf_with_azl_repos", str(script_path))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    if spec is None:
        pytest.fail(f"Unable to load module spec for {script_path}")

    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return cast("_DnfModule", module)


@pytest.mark.parametrize("scheme", ["file", "http", "https"])
def test_supported_repository_schemes_are_accepted(scheme: str) -> None:
    validate_repo_url(f"{scheme}://example.test/repo")


@pytest.mark.parametrize("url", ["ftp://example.test/repo", "custom://example.test/repo", "relative/repo"])
def test_unsupported_repository_schemes_are_rejected(url: str) -> None:
    with pytest.raises(UnsupportedRepoSchemeError, match="unsupported repository URL scheme"):
        validate_repo_url(url)


def test_probe_rejects_unsupported_scheme_before_urlopen(
    dnf_module: _DnfModule,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def unexpected_urlopen(*_args: object, **_kwargs: object) -> None:
        pytest.fail("urlopen was called for an unsupported scheme")

    urlopen: Callable[..., object] = unexpected_urlopen
    monkeypatch.setattr(urllib.request, "urlopen", urlopen)

    status, error = dnf_module.probe_repo("ftp://example.test/repo")

    assert status == "fail"
    assert error is not None
    assert "'ftp'" in error


def test_probe_supports_file_repositories(dnf_module: _DnfModule, tmp_path: Path) -> None:
    repodata_dir = tmp_path / "repo" / "repodata"
    repodata_dir.mkdir(parents=True)
    (repodata_dir / "repomd.xml").write_text("<repomd/>")

    status, error = dnf_module.probe_repo((tmp_path / "repo").as_uri())

    assert status == "ok"
    assert error is None


class _Response:
    """Minimal context-managed URL response for probe tests."""

    def __init__(self, status: int) -> None:
        self.status = status

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *_args: object) -> None:
        return None


def test_probe_reports_non_success_status(
    dnf_module: _DnfModule,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Treat non-2xx responses that do not raise as failures."""
    monkeypatch.setattr(
        urllib.request,
        "urlopen",
        lambda *_args, **_kwargs: _Response(HTTPStatus.INTERNAL_SERVER_ERROR),
    )

    status, error = dnf_module.probe_repo("https://example.test/repo")

    assert status == "fail"
    assert error == "HTTP 500"


@pytest.mark.parametrize(
    ("exception", "expected"),
    [
        (
            urllib.error.HTTPError(
                "https://example.test/repo",
                HTTPStatus.NOT_FOUND,
                "Not Found",
                Message(),
                None,
            ),
            ("missing", None),
        ),
        (
            urllib.error.HTTPError(
                "https://example.test/repo",
                HTTPStatus.FORBIDDEN,
                "Forbidden",
                Message(),
                None,
            ),
            ("fail", "HTTP 403"),
        ),
        (
            urllib.error.URLError(FileNotFoundError()),
            ("missing", None),
        ),
        (
            urllib.error.URLError("connection refused"),
            ("fail", "URL error: connection refused"),
        ),
        (
            TimeoutError(),
            ("fail", "timed out after 7s"),
        ),
        (
            OSError("network down"),
            ("fail", "OS error: network down"),
        ),
    ],
)
def test_probe_translates_transport_errors(
    dnf_module: _DnfModule,
    monkeypatch: pytest.MonkeyPatch,
    exception: BaseException,
    expected: tuple[str, str | None],
) -> None:
    """Preserve the probe outcome assigned to each transport failure."""
    def fail(*_args: object, **_kwargs: object) -> None:
        raise exception

    monkeypatch.setattr(urllib.request, "urlopen", fail)

    assert dnf_module.probe_repo("https://example.test/repo", timeout=7) == expected
