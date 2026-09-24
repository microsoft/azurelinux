# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
"""Repository URL scheme policy tests."""

from __future__ import annotations

import importlib.machinery
import importlib.util
import urllib.request
from pathlib import Path
from typing import TYPE_CHECKING, Protocol, cast

import pytest
from _repo_layout import UnsupportedRepoSchemeError, validate_repo_url

if TYPE_CHECKING:
    from collections.abc import Callable


class _DnfModule(Protocol):
    def probe_repo(self, probe_url: str, *, timeout: float = 30.0) -> tuple[str, str | None]:
        """Describe the dnf wrapper's repository probe."""


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
