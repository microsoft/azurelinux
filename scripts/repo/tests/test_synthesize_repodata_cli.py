# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
"""CLI orchestration tests for repository synthesis."""

from __future__ import annotations

import importlib.util
import json
import sys
import urllib.error
from collections import Counter
from email.message import Message
from pathlib import Path
from types import ModuleType, SimpleNamespace
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from collections.abc import Callable

_SCRIPT_PATH = Path(__file__).resolve().parents[1] / "synthesize-repodata.py"
_CREATEREPO_CLASSES = (
    "PrimaryXmlFile",
    "PrimarySqlite",
    "FilelistsXmlFile",
    "FilelistsSqlite",
    "OtherXmlFile",
    "OtherSqlite",
)
_WRITER_EVENTS: list[tuple[object, ...]] = []


class _FakeXml:
    def __init__(self, path: str) -> None:
        self.path = path
        _WRITER_EVENTS.append(("xml-open", path))

    def set_num_of_pkgs(self, count: int) -> None:
        _WRITER_EVENTS.append(("xml-count", count))

    def add_pkg(self, package: object) -> None:
        _WRITER_EVENTS.append(("xml-add", package))

    def close(self) -> None:
        _WRITER_EVENTS.append(("xml-close", self.path))


class _FakeDatabase:
    def __init__(self, path: str) -> None:
        self.path = path
        _WRITER_EVENTS.append(("db-open", path))

    def add_pkg(self, package: object) -> None:
        _WRITER_EVENTS.append(("db-add", package))

    def dbinfo_update(self, checksum: str) -> None:
        _WRITER_EVENTS.append(("dbinfo", checksum))

    def close(self) -> None:
        _WRITER_EVENTS.append(("db-close", self.path))


class _FakeRecord:
    def __init__(self, record_type: str, path: str) -> None:
        self.record_type = record_type
        self.path = path
        self.checksum = f"{record_type}-checksum"

    def fill(self, checksum_type: int) -> None:
        _WRITER_EVENTS.append(("fill", self.record_type, checksum_type))


class _FakeRepomd:
    def __init__(self) -> None:
        self.records: list[_FakeRecord] = []

    def set_record(self, record: _FakeRecord) -> None:
        self.records.append(record)

    def xml_dump(self) -> str:
        return ",".join(record.record_type for record in self.records)


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


def test_main_preserves_explicit_repo_validation_error(
    synth_module: ModuleType,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Report malformed explicit repository arguments without a traceback."""
    result = synth_module.main(
        [
            "--output-dir",
            str(tmp_path / "output"),
            "--repo",
            "bogus",
        ]
    )

    assert result == 1
    assert capsys.readouterr().err.endswith(
        "ERROR: --repo 'bogus': expected TYPE:URL where TYPE in "
        "{main, debuginfo, srpms}\n"
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


def test_build_package_universe_collects_source_map(
    synth_module: ModuleType,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Build distinct universe entries and deduplicate package-source pairs."""
    repo = synth_module.InputRepo(
        "main",
        "x86_64",
        "https://example.test/base/x86_64",
        "explicit",
    )
    packages = [
        SimpleNamespace(
            name="example",
            epoch=None,
            version="1.0",
            release="1.azl4",
            arch="x86_64",
            rpm_sourcerpm="example-1.0-1.azl4.src.rpm",
        ),
        SimpleNamespace(
            name="example",
            epoch=None,
            version="2.0",
            release="1.azl4",
            arch="x86_64",
            rpm_sourcerpm="example-1.0-1.azl4.src.rpm",
        ),
    ]

    monkeypatch.setattr(
        synth_module,
        "_find_metadata_path",
        lambda _repo_dir, _kind: "primary.xml",
    )

    def parse_primary(
        _path: str,
        *,
        pkgcb: Callable[[object], None],
        do_files: bool,
        warningcb: Callable[..., bool],
    ) -> None:
        assert not do_files
        assert warningcb("ignored")
        for package in packages:
            pkgcb(package)

    monkeypatch.setattr(
        synth_module.cr,
        "xml_parse_primary",
        parse_primary,
        raising=False,
    )

    universe, source_map = synth_module.build_package_universe({repo: tmp_path})

    expected_versions = {"1.0", "2.0"}
    assert len(universe) == len(expected_versions)
    assert {key[4] for key in universe} == expected_versions
    assert source_map == [
        {
            "packageName": "example",
            "sourcePackageName": "example",
        }
    ]


def test_query_azldev_normalizes_routing_rows(
    synth_module: ModuleType,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Normalize azldev output and exclude rows for foreign components."""
    rows = [
        {
            "packageName": "example",
            "type": "rpm",
            "component": "example",
            "publishChannel": "rpm-base",
            "group": "core",
        },
        {
            "packageName": "example-devel",
            "type": "rpm",
            "component": "example",
            "publishChannel": "",
        },
        {
            "packageName": "foreign",
            "type": "rpm",
            "component": "not-an-azl-component",
            "publishChannel": "rpm-base",
        },
    ]
    completed = SimpleNamespace(
        returncode=0,
        stdout=json.dumps(rows),
        stderr="",
    )
    monkeypatch.setattr(synth_module.subprocess, "run", lambda *_args, **_kwargs: completed)
    source_map = [
        {
            "packageName": "example",
            "sourcePackageName": "example",
        }
    ]

    routing = synth_module.query_azldev(
        tmp_path,
        source_map,
        tmp_path,
        {"example"},
    )

    assert json.loads((tmp_path / "rpm_source_map.json").read_text()) == source_map
    assert routing.rpm["example"] == {
        "component": "example",
        "channel": "base",
        "raw_channel": "rpm-base",
        "group": "core",
    }
    assert routing.rpm["example-devel"]["channel"] == ""
    assert routing.component_channels == {"example": Counter({"base": 1})}
    assert routing.foreign_names == {"foreign"}


def test_collect_emission_plan_builds_typed_reports(
    synth_module: ModuleType,
) -> None:
    """Count destinations and build unpublished and fallback report rows."""
    repo = synth_module.InputRepo(
        "main",
        "x86_64",
        "https://example.test/base/x86_64",
        "explicit",
    )
    published_key = ("main", "x86_64", "published", "0", "1", "1", "x86_64")
    unpublished_key = ("main", "x86_64", "missing", "0", "1", "1", "x86_64")
    universe = {
        published_key: synth_module.UniverseEntry(repo, "published-source"),
        unpublished_key: synth_module.UniverseEntry(repo, "missing-source"),
    }
    decisions = {
        published_key: synth_module.RoutingDecision(
            "base",
            "inherited from siblings",
            inherited=True,
            tie_break_used=True,
        ),
        unpublished_key: synth_module.RoutingDecision(
            None,
            "no azldev entry for package",
        ),
    }

    counts, unpublished, fallbacks = synth_module._collect_emission_plan(  # noqa: SLF001
        universe,
        decisions,
    )

    destination = synth_module.Destination("base", "main", "x86_64")
    assert counts == Counter({destination: 1})
    assert unpublished == [
        {
            "name": "missing",
            "kind": "main",
            "arch": "x86_64",
            "source_repo": repo.url,
            "source_package": "missing-source",
            "reason": "no azldev entry for package",
        }
    ]
    assert fallbacks == [
        {
            "name": "published",
            "kind": "main",
            "arch": "x86_64",
            "source_repo": repo.url,
            "source_package": "published-source",
            "dest_channel": "base",
            "reason": "inherited from siblings",
            "tie_break_used": True,
        }
    ]


def test_write_routing_reports(
    synth_module: ModuleType,
    tmp_path: Path,
) -> None:
    """Serialize routing reports and retain fallback tie-break markers."""
    unpublished = [
        {
            "name": "missing",
            "kind": "main",
            "arch": "x86_64",
            "source_repo": "https://example.test/base/x86_64",
            "source_package": "missing-source",
            "reason": "no route",
        }
    ]
    fallbacks = [
        {
            "name": "published",
            "kind": "main",
            "arch": "x86_64",
            "source_repo": "https://example.test/base/x86_64",
            "source_package": "published-source",
            "dest_channel": "base",
            "reason": "inherited",
            "tie_break_used": True,
        }
    ]

    unpublished_json, unpublished_text = synth_module.write_unpublished_report(
        unpublished,
        tmp_path,
    )
    fallback_json, fallback_text = synth_module.write_fallback_report(
        fallbacks,
        tmp_path,
    )

    assert json.loads(unpublished_json.read_text()) == unpublished
    assert "main      x86_64  missing" in unpublished_text.read_text()
    assert json.loads(fallback_json.read_text()) == fallbacks
    assert "published  -> base [tie-break]" in fallback_text.read_text()


def test_repo_writer_uses_createrepo_stream_contract(
    synth_module: ModuleType,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Drive the native writer API through the locally modeled contract."""
    _WRITER_EVENTS.clear()

    monkeypatch.setattr(
        synth_module._RepoWriter,  # noqa: SLF001
        "_STREAMS",
        (("primary", "primary_db", _FakeXml, _FakeDatabase),),
    )
    monkeypatch.setattr(synth_module.cr, "Repomd", _FakeRepomd, raising=False)
    monkeypatch.setattr(synth_module.cr, "RepomdRecord", _FakeRecord, raising=False)
    monkeypatch.setattr(synth_module.cr, "SHA256", 42, raising=False)

    destination = synth_module.Destination("base", "main", "x86_64")
    writer = synth_module._RepoWriter(destination, tmp_path, 1)  # noqa: SLF001
    package = object()

    writer.add_pkg(package)
    writer.finish()

    assert writer.added == 1
    assert ("xml-count", 1) in _WRITER_EVENTS
    assert ("xml-add", package) in _WRITER_EVENTS
    assert ("db-add", package) in _WRITER_EVENTS
    assert ("dbinfo", "primary-checksum") in _WRITER_EVENTS
    assert (tmp_path / "base/x86_64/repodata/repomd.xml").read_text() == (
        "primary,primary_db"
    )
