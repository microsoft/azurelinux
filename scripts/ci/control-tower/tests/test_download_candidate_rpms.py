"""Tests for Control Tower and Koji candidate RPM acquisition."""

from __future__ import annotations

import ssl
import urllib.request
from typing import TYPE_CHECKING
from unittest.mock import Mock

import download_candidate_rpms as acquisition
import pytest

TEST_TASK_ID = 12345

if TYPE_CHECKING:
    from pathlib import Path


def _candidate(path: Path, component: str) -> acquisition.DownloadedRpm:
    return {
        "architecture": "x86_64",
        "component": component,
        "filename": path.name,
        "name": "",
        "path": str(path),
        "repository": "",
        "sha256": "abc",
        "size": path.stat().st_size,
        "taskId": TEST_TASK_ID,
        "url": f"https://koji.example/{path.name}",
    }


def test_validate_https_url_rejects_credentials() -> None:
    """Do not permit secrets in endpoint URLs that may be logged."""
    with pytest.raises(ValueError, match="without credentials"):
        acquisition.validate_https_url(
            "koji-files-url",
            "https://user:password@koji.example/kojifiles",
        )


def test_make_koji_ssl_context_verifies_by_default() -> None:
    """Authenticate Koji endpoints unless the explicit override is used."""
    context = acquisition.make_koji_ssl_context(insecure=False)

    assert context.verify_mode == ssl.CERT_REQUIRED
    assert context.check_hostname


def test_make_koji_ssl_context_supports_explicit_override() -> None:
    """Keep the current self-signed Koji deployment available when requested."""
    context = acquisition.make_koji_ssl_context(insecure=True)

    assert context.verify_mode == ssl.CERT_NONE
    assert not context.check_hostname


def test_read_job_id_requires_nonempty_file(tmp_path: Path) -> None:
    """Reject a missing build identity instead of querying an ambiguous result."""
    job_id_file = tmp_path / "job-id.txt"
    job_id_file.write_text("\n", encoding="utf-8")

    with pytest.raises(RuntimeError, match="job ID is empty"):
        acquisition.read_job_id(job_id_file)


def test_make_task_output_url_uses_koji_task_layout() -> None:
    """Use Koji's task-ID bucket convention for scratch outputs."""
    assert acquisition.make_task_output_url(
        "https://koji.example/kojifiles",
        12345,
        "jq-1.8.1-8.azl4.x86_64.rpm",
    ) == (
        "https://koji.example/kojifiles/work/tasks/2345/12345/"
        "jq-1.8.1-8.azl4.x86_64.rpm"
    )


def test_make_task_output_url_rejects_nested_path() -> None:
    """Prevent remote filenames from escaping the expected task directory."""
    with pytest.raises(ValueError, match="Unsafe"):
        acquisition.make_task_output_url(
            "https://koji.example/kojifiles",
            12345,
            "../secret",
        )


def test_discover_arch_task_ids_selects_requested_build_arch() -> None:
    """Ignore source, tag, and other-architecture descendants."""
    document = b"""
    <a href="taskinfo?taskID=10">buildSRPMFromSCM (repo)</a>
    <a href="taskinfo?taskID=20">buildArch (jq.src.rpm, x86_64)</a>
    <a href="taskinfo?taskID=30">buildArch (jq.src.rpm, aarch64)</a>
    <a href="taskinfo?taskID=40">tagBuild (noarch)</a>
    """

    assert acquisition.discover_arch_task_ids(document, "x86_64") == [20]


def test_fetch_bytes_rejects_oversized_task_page(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Bound untrusted Koji HTML before parsing it in memory."""
    response = Mock()
    response.__enter__ = Mock(return_value=response)
    response.__exit__ = Mock(return_value=False)
    response.headers = {"Content-Length": str(acquisition.MAX_TASK_PAGE_SIZE + 1)}
    monkeypatch.setattr(urllib.request, "urlopen", Mock(return_value=response))

    with pytest.raises(RuntimeError, match="exceeds the size limit"):
        acquisition.fetch_bytes(
            "https://koji.example/taskinfo?taskID=20",
            ssl.create_default_context(),
        )

    response.read.assert_not_called()


def test_discover_arch_task_ids_requires_matching_architecture() -> None:
    """Fail rather than silently checking no candidate artifacts."""
    with pytest.raises(RuntimeError, match="no buildArch task"):
        acquisition.discover_arch_task_ids(
            b'<a href="taskinfo?taskID=30">buildArch (jq.src.rpm, aarch64)</a>',
            "x86_64",
        )


def test_discover_rpm_outputs_keeps_publishable_binary_rpms() -> None:
    """Exclude source, debug, logs, and outputs belonging to another task."""
    document = b"""
    <a href="http://koji-hub/kojifiles/work/tasks/20/20/jq-1-1.x86_64.rpm">jq</a>
    <a href="http://koji-hub/kojifiles/work/tasks/20/20/jq-devel-1-1.x86_64.rpm">devel</a>
    <a href="http://koji-hub/kojifiles/work/tasks/20/20/jq-doc-1-1.noarch.rpm">docs</a>
    <a href="http://koji-hub/kojifiles/work/tasks/20/20/jq-1-1.src.rpm">source</a>
    <a href="http://koji-hub/kojifiles/work/tasks/20/20/jq-debuginfo-1-1.x86_64.rpm">debug</a>
    <a href="http://koji-hub/kojifiles/work/tasks/20/20/jq-1-1.x86_64.rpm.log">log</a>
    <a href="http://koji-hub/kojifiles/work/tasks/21/21/not-jq-1-1.x86_64.rpm">other</a>
    """

    assert acquisition.discover_rpm_outputs(document, 20, "x86_64") == [
        "jq-1-1.x86_64.rpm",
        "jq-devel-1-1.x86_64.rpm",
        "jq-doc-1-1.noarch.rpm",
    ]


def test_select_completed_component_tasks_returns_entire_build_transaction() -> None:
    """Use all successful package tasks rather than a configured component name."""
    results = {
        "buildTasks": [
            {
                "taskStatus": "Completed",
                "kojiInfo": {"componentName": "jq", "kojiTaskNumber": 20},
            },
            {
                "taskStatus": "Succeeded",
                "kojiInfo": {"componentName": "oniguruma", "kojiTaskNumber": 30},
            },
            {"taskStatus": "Completed", "kojiInfo": None},
        ]
    }

    assert acquisition.select_completed_component_tasks(results) == [
        {"component": "jq", "rootTaskId": 20},
        {"component": "oniguruma", "rootTaskId": 30},
    ]


def test_select_completed_component_tasks_ignores_failed_attempts() -> None:
    """Use successful outputs without treating failed attempts as candidates."""
    results = {
        "buildTasks": [
            {
                "taskStatus": "Completed",
                "kojiInfo": {"componentName": "jq", "kojiTaskNumber": 20},
            },
            {
                "taskStatus": "Failed",
                "kojiInfo": {"componentName": "oniguruma", "kojiTaskNumber": 30},
            },
        ]
    }

    assert acquisition.select_completed_component_tasks(results) == [
        {"component": "jq", "rootTaskId": 20}
    ]


def test_download_rpm_streams_and_hashes_valid_rpm(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Persist complete RPM bytes only after validating their lead."""
    body = acquisition.RPM_MAGIC + b"candidate rpm"
    response = Mock()
    response.__enter__ = Mock(return_value=response)
    response.__exit__ = Mock(return_value=False)
    response.headers = {"Content-Length": str(len(body))}
    response.read.side_effect = [body, b""]
    monkeypatch.setattr(urllib.request, "urlopen", Mock(return_value=response))

    result = acquisition.download_rpm(
        destination=tmp_path,
        filename="jq-1.8.1-8.azl4.x86_64.rpm",
        koji_files_url="https://koji.example/kojifiles",
        ssl_context=ssl.create_default_context(),
        source_component="jq",
        task_id=TEST_TASK_ID,
    )

    assert (tmp_path / result["filename"]).read_bytes() == body
    assert result["taskId"] == TEST_TASK_ID
    assert result["component"] == "jq"
    assert result["size"] == len(body)


def test_download_rpm_removes_invalid_output(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Do not leave HTML error bodies masquerading as candidate RPMs."""
    response = Mock()
    response.__enter__ = Mock(return_value=response)
    response.__exit__ = Mock(return_value=False)
    response.headers = {}
    response.read.side_effect = [b"<html>not an rpm</html>", b""]
    monkeypatch.setattr(urllib.request, "urlopen", Mock(return_value=response))

    with pytest.raises(RuntimeError, match="not an RPM"):
        acquisition.download_rpm(
            destination=tmp_path,
            filename="jq-1.8.1-8.azl4.x86_64.rpm",
            koji_files_url="https://koji.example/kojifiles",
            ssl_context=ssl.create_default_context(),
            source_component="jq",
            task_id=TEST_TASK_ID,
        )

    assert not (tmp_path / "jq-1.8.1-8.azl4.x86_64.rpm").exists()


def test_route_candidates_applies_component_and_package_policy(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Route base components, SDK defaults, and binary SDK carve-outs."""
    download_directory = tmp_path / "downloads"
    download_directory.mkdir()
    jq_path = download_directory / "jq.rpm"
    jq_doc_path = download_directory / "jq-doc.rpm"
    jo_path = download_directory / "jo.rpm"
    for path in (jq_path, jq_doc_path, jo_path):
        path.write_bytes(acquisition.RPM_MAGIC)
    policy_path = tmp_path / "publish.toml"
    policy_path.write_text(
        """
[component-groups.base-packages]
components = ["jq"]

[package-groups.exceptions-packages]
packages = ["jq-doc"]
""",
        encoding="utf-8",
    )
    names = {
        jq_path: "jq",
        jq_doc_path: "jq-doc",
        jo_path: "jo",
    }
    monkeypatch.setattr(acquisition, "query_package_name", lambda path: names[path])
    candidates = [
        _candidate(jq_path, "jq"),
        _candidate(jq_doc_path, "jq"),
        _candidate(jo_path, "jo"),
    ]
    base_directory = tmp_path / "candidate-inputs" / "base"
    sdk_directory = tmp_path / "candidate-inputs" / "sdk"

    acquisition.route_candidates(
        base_directory=base_directory,
        candidates=candidates,
        publish_policy=policy_path,
        report_path=tmp_path / "candidate-acquisition.json",
        sdk_directory=sdk_directory,
    )

    assert sorted(path.name for path in base_directory.iterdir()) == ["jq.rpm"]
    assert sorted(path.name for path in sdk_directory.iterdir()) == [
        "jo.rpm",
        "jq-doc.rpm",
    ]
    assert {candidate["name"]: candidate["repository"] for candidate in candidates} == {
        "jo": "candidate-sdk",
        "jq": "candidate-base",
        "jq-doc": "candidate-sdk",
    }
