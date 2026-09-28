# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
"""CLI orchestration tests for repository synthesis."""

from __future__ import annotations

import importlib.util
import sys
import urllib.error
from email.message import Message
from pathlib import Path
from types import ModuleType

import pytest

_SCRIPT_PATH = Path(__file__).resolve().parents[1] / "synthesize-repodata.py"
_CREATEREPO_CLASSES = (
    "PrimaryXmlFile",
    "PrimarySqlite",
    "FilelistsXmlFile",
    "FilelistsSqlite",
    "OtherXmlFile",
    "OtherSqlite",
)


@pytest.fixture
def synth_module(monkeypatch: pytest.MonkeyPatch) -> ModuleType:
    """Load the synthesis script with its native dependency stubbed."""
    createrepo = ModuleType("createrepo_c")
    for name in _CREATEREPO_CLASSES:
        setattr(createrepo, name, object)
    monkeypatch.setitem(sys.modules, "createrepo_c", createrepo)

    spec = importlib.util.spec_from_file_location("_test_synthesize_repodata", _SCRIPT_PATH)
    if spec is None or spec.loader is None:
        pytest.fail(f"Unable to load module spec for {_SCRIPT_PATH}")

    module = importlib.util.module_from_spec(spec)
    monkeypatch.setitem(sys.modules, spec.name, module)
    spec.loader.exec_module(module)
    return module


def _stub_routing_pipeline(
    module: ModuleType,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Replace native metadata processing while retaining CLI orchestration."""
    monkeypatch.setattr(module, "build_package_universe", lambda _repos: ({}, []))
    monkeypatch.setattr(module, "query_known_components", lambda _root: set())
    monkeypatch.setattr(
        module,
        "query_azldev",
        lambda *_args: module.AzldevRouting(),
    )
    monkeypatch.setattr(module, "decide_routing", lambda *_args: {})
    monkeypatch.setattr(module, "emit_repos", lambda *_args: ({}, [], []))
    monkeypatch.setattr(
        module,
        "write_unpublished_report",
        lambda _records, output_dir: (
            output_dir / "unpublished-packages.json",
            output_dir / "unpublished-packages.txt",
        ),
    )
    monkeypatch.setattr(
        module,
        "write_fallback_report",
        lambda _records, output_dir: (
            output_dir / "fallback-channel-packages.json",
            output_dir / "fallback-channel-packages.txt",
        ),
    )


@pytest.mark.parametrize("cache_arg", [None, "--keep-cache"])
def test_main_runs_pipeline_and_honors_cache_option(
    synth_module: ModuleType,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    cache_arg: str | None,
) -> None:
    """Run every orchestration phase and apply the requested cache policy."""
    output_dir = tmp_path / "output"

    def fake_download(repo: object, cache_root: Path, _ssl_context: object) -> Path:
        cache_dir = cache_root / str(hash(repo))
        cache_dir.mkdir()
        return cache_dir

    monkeypatch.setattr(synth_module, "download_repo_metadata", fake_download)
    _stub_routing_pipeline(synth_module, monkeypatch)

    argv = [
        "--output-dir",
        str(output_dir),
        "--repo",
        "main:https://example.test/base/x86_64",
    ]
    if cache_arg is not None:
        argv.append(cache_arg)

    result = synth_module.main(argv)

    assert result == 0
    assert (output_dir / ".cache").exists() is (cache_arg is not None)


def test_main_preserves_download_error(
    synth_module: ModuleType,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Report metadata download failures with repository context."""
    def fail_download(*_args: object) -> None:
        raise urllib.error.HTTPError(
            "https://example.test/base/x86_64/repodata/repomd.xml",
            503,
            "Unavailable",
            Message(),
            None,
        )

    monkeypatch.setattr(synth_module, "download_repo_metadata", fail_download)

    result = synth_module.main(
        [
            "--output-dir",
            str(tmp_path / "output"),
            "--repo",
            "main:https://example.test/base/x86_64",
        ]
    )

    assert result == 1
    assert capsys.readouterr().err.endswith(
        "ERROR: HTTP 503 fetching "
        "https://example.test/base/x86_64/repodata/repomd.xml "
        "(origin=explicit)\n"
    )


def test_main_requires_repository_source(
    synth_module: ModuleType,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Reject an empty repository source list before creating output."""
    output_dir = tmp_path / "output"

    result = synth_module.main(["--output-dir", str(output_dir)])

    assert result == 1
    assert capsys.readouterr().err.endswith(
        "ERROR: at least one --repo-prefix or --repo must be provided\n"
    )
    assert not output_dir.exists()
