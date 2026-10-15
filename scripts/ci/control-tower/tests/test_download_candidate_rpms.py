"""Tests for Control Tower and Koji candidate RPM acquisition."""

from __future__ import annotations

import argparse
import hashlib
import json
import xmlrpc.client
from typing import TYPE_CHECKING
from unittest.mock import Mock

import download_candidate_rpms as acquisition
import koji
import pytest
import requests
from requests.adapters import HTTPAdapter

TEST_TASK_ID = 12345
TEST_REPORT_SCHEMA_VERSION = 3

if TYPE_CHECKING:
    from collections.abc import Iterator
    from pathlib import Path


def _candidate(
    path: Path, component: str, architecture: str = "x86_64",
) -> acquisition.DownloadedRpm:
    return {
        "architecture": architecture,
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


def _response(body: bytes, headers: dict[str, str] | None = None) -> Mock:
    response = Mock()
    response.__enter__ = Mock(return_value=response)
    response.__exit__ = Mock(return_value=False)
    response.headers = headers or {}
    response.iter_content.return_value = [body]
    return response


@pytest.mark.parametrize("insecure", [False, True])
def test_official_client_sends_metadata_with_tls_policy(
    monkeypatch: pytest.MonkeyPatch, *, insecure: bool,
) -> None:
    """Exercise the upstream client's serialization and TLS request options."""
    body = xmlrpc.client.dumps(({"state": 2},), methodresponse=True).encode()
    post = Mock(return_value=_response(body))
    monkeypatch.setattr(requests.Session, "post", post)
    hub = acquisition.make_koji_client("https://koji.example/kojihub", insecure=insecure)

    assert isinstance(hub, koji.ClientSession)
    assert hub.getTaskInfo(TEST_TASK_ID, request=True, strict=True) == {"state": 2}
    params, method = xmlrpc.client.loads(post.call_args.kwargs["data"])
    assert method == "getTaskInfo"
    assert params[0] == TEST_TASK_ID
    assert params[-1] == {"__starstar": True, "request": True, "strict": True}
    assert post.call_args.args == ("https://koji.example/kojihub",)
    assert post.call_args.kwargs.get("verify", True) is not insecure
    assert post.call_args.kwargs["timeout"] == acquisition.REQUEST_TIMEOUT_SECONDS
    assert hub.opts["anon_retry"]
    assert hub.opts["max_retries"] == acquisition.MAX_REQUEST_RETRIES
    assert not hub.opts["offline_retry"]


def test_official_client_surfaces_hub_fault(monkeypatch: pytest.MonkeyPatch) -> None:
    """A Koji fault remains a failure, not an empty task inventory."""
    fault = xmlrpc.client.Fault(koji.GenericError.faultCode, "missing task")
    post = Mock(return_value=_response(xmlrpc.client.dumps(fault).encode()))
    monkeypatch.setattr(requests.Session, "post", post)
    hub = acquisition.make_koji_client("https://koji.example/kojihub", insecure=False)

    with pytest.raises(koji.GenericError, match="missing task"):
        hub.getTaskInfo(20)
    post.assert_called_once()


@pytest.mark.parametrize("insecure", [False, True])
def test_download_session_reuses_koji_retries_with_tls_policy(*, insecure: bool) -> None:
    """Configure artifact requests independently of the hub's TLS option."""
    with acquisition.make_download_session(insecure=insecure) as session:
        assert session.verify is not insecure
        assert session.headers["Accept-Encoding"] == "identity"
        adapter = session.get_adapter("https://koji.example")
        assert isinstance(adapter, HTTPAdapter)
        retry = adapter.max_retries
        assert retry.total == acquisition.MAX_REQUEST_RETRIES
        assert retry.backoff_factor == acquisition.RETRY_INTERVAL_SECONDS
        assert set(retry.status_forcelist) == set(acquisition.RETRYABLE_HTTP_STATUSES)


def test_download_rpm_streams_and_hashes_valid_rpm(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path,
) -> None:
    """Hash complete RPM bytes and retain the upstream-derived output URL."""
    body = acquisition.RPM_MAGIC + b"candidate rpm"
    response = _response(body, {"Content-Length": str(len(body))})
    response.iter_content.return_value = [body[:2], b"", body[2:]]
    get = Mock(return_value=response)
    with acquisition.make_download_session(insecure=True) as session:
        monkeypatch.setattr(session, "get", get)
        result = acquisition.download_rpm(
            destination=tmp_path,
            filename="jq-1-1.x86_64.rpm",
            koji_files_url="https://koji.example/kojifiles",
            session=session,
            source_component="jq",
            task_id=TEST_TASK_ID,
        )
    assert (tmp_path / result["filename"]).read_bytes() == body
    assert result["sha256"] == hashlib.sha256(body).hexdigest()
    assert result["size"] == len(body)
    assert result["architecture"] == "x86_64"
    get.assert_called_once_with(
        result["url"], stream=True, timeout=acquisition.REQUEST_TIMEOUT_SECONDS,
    )
    response.__exit__.assert_called_once()


@pytest.mark.parametrize(("body", "length", "message"), [
    (b"<html>not an rpm</html>", None, "not an RPM"),
    (b"", None, "not an RPM"),
    (acquisition.RPM_MAGIC, "20", "Content-Length"),
    (acquisition.RPM_MAGIC, "invalid", "invalid literal"),
])
def test_download_rpm_removes_invalid_output(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path,
    body: bytes, length: str | None, message: str,
) -> None:
    """Failed validation must not leave a success-shaped candidate file."""
    headers = {"Content-Length": length} if length is not None else {}
    response = _response(body, headers)
    with acquisition.make_download_session(insecure=False) as session:
        monkeypatch.setattr(session, "get", Mock(return_value=response))
        with pytest.raises((RuntimeError, ValueError), match=message):
            acquisition.download_rpm(
                destination=tmp_path,
                filename="jq-1-1.x86_64.rpm",
                koji_files_url="https://koji.example/kojifiles",
                session=session,
                source_component="jq",
                task_id=TEST_TASK_ID,
            )
    assert not (tmp_path / "jq-1-1.x86_64.rpm").exists()


@pytest.mark.parametrize("error", [
    requests.HTTPError("403 Forbidden"),
    requests.exceptions.SSLError("untrusted certificate"),
    requests.exceptions.ChunkedEncodingError("incomplete body"),
])
def test_download_rpm_surfaces_errors_and_cleans_partial_files(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, error: requests.RequestException,
) -> None:
    """Surface status, TLS, and interrupted-body errors with download context."""
    response = _response(b"")
    if isinstance(error, requests.HTTPError):
        response.raise_for_status.side_effect = error
    else:

        def chunks(*, chunk_size: int) -> Iterator[bytes]:
            del chunk_size
            yield acquisition.RPM_MAGIC
            raise error
        response.iter_content.side_effect = chunks
    with acquisition.make_download_session(insecure=False) as session:
        monkeypatch.setattr(session, "get", Mock(return_value=response))
        with pytest.raises(RuntimeError, match=r"Failed to download https://koji\.example"):
            acquisition.download_rpm(
                destination=tmp_path,
                filename="jq-1-1.x86_64.rpm",
                koji_files_url="https://koji.example/kojifiles",
                session=session,
                source_component="jq",
                task_id=TEST_TASK_ID,
            )
    assert not (tmp_path / "jq-1-1.x86_64.rpm").exists()
    response.__exit__.assert_called_once()


def _arch_task(task_id: int, architecture: str, state: int = 2) -> dict[str, object]:
    return {
        "arch": architecture,
        "id": task_id,
        "method": "buildArch",
        "parent": 10,
        "request": ["tasks/11/11/jq.src.rpm", 13, architecture, True, {"repo_id": 99}],
        "state": state,
    }


def _task_hub(children: object, state: int = 2) -> Mock:
    hub = Mock()
    hub.getTaskInfo.return_value = {
        "id": 10, "method": "build", "state": state,
        "request": ["source", 13, {"scratch": True}],
    }
    hub.getTaskChildren.return_value = children
    return hub


def test_discover_arch_tasks_uses_requested_architecture_and_noarch() -> None:
    """Ignore source tasks and other architectures without interpreting labels."""
    noarch = _arch_task(35, "noarch")
    noarch["arch"] = "x86_64"
    hub = _task_hub([
        {"id": 11, "parent": 10, "method": "buildSRPMFromSCM"},
        _arch_task(20, "x86_64"),
        _arch_task(30, "aarch64"),
        noarch,
    ])

    assert acquisition.discover_arch_tasks(hub, 10, "x86_64") == [
        {"architecture": "noarch", "taskId": 35},
        {"architecture": "x86_64", "taskId": 20},
    ]
    hub.getTaskInfo.assert_called_once_with(10, request=True, strict=True)
    hub.getTaskChildren.assert_called_once_with(10, request=True, strict=True)


@pytest.mark.parametrize("architecture", ["x86_64", "aarch64"])
def test_discover_arch_tasks_accepts_noarch_only_build(architecture: str) -> None:
    """A pure-noarch source must work in either repository view."""
    assert acquisition.discover_arch_tasks(
        _task_hub([_arch_task(20, "noarch")]), 10, architecture,
    ) == [{"architecture": "noarch", "taskId": 20}]


@pytest.mark.parametrize("state", [0, 1, 3, 4, 5, True])
def test_discover_arch_tasks_rejects_nonclosed_root(state: int) -> None:
    """Do not trust a Control Tower Completed label over actual hub state."""
    with pytest.raises(RuntimeError, match="root task 10 is not a closed build"):
        acquisition.discover_arch_tasks(_task_hub([], state), 10, "x86_64")


@pytest.mark.parametrize("state", [0, 1, 3, 4, 5, True])
def test_discover_arch_tasks_rejects_nonclosed_child(state: int) -> None:
    """Reject failed, canceled, and unfinished architecture builds."""
    with pytest.raises(RuntimeError, match=r"buildArch task 20.*not closed"):
        acquisition.discover_arch_tasks(
            _task_hub([_arch_task(20, "x86_64", state)]), 10, "x86_64",
        )


def test_discover_arch_tasks_rejects_retry_ambiguity() -> None:
    """Never pick the newest successful child or merge retry outputs."""
    with pytest.raises(RuntimeError, match=r"ambiguous buildArch retries.*20, 21"):
        acquisition.discover_arch_tasks(
            _task_hub([_arch_task(20, "x86_64"), _arch_task(21, "x86_64")]),
            10, "x86_64",
        )


@pytest.mark.parametrize("children", [
    None, {}, [None],
    [{"id": True, "parent": 10, "method": "buildArch"}],
    [{"id": 20, "parent": 99, "method": "buildArch"}],
    [{"id": 20, "parent": 10, "method": ""}],
    [{"id": 20, "parent": 10, "method": "buildArch", "request": []}],
    [_arch_task(20, "")],
    [_arch_task(20, "x86_64"), _arch_task(20, "x86_64")],
])
def test_discover_arch_tasks_rejects_malformed_children(children: object) -> None:
    """Fail instead of silently ignoring malformed or duplicated task records."""
    with pytest.raises((RuntimeError, TypeError), match=r"malformed|duplicate"):
        acquisition.discover_arch_tasks(_task_hub(children), 10, "x86_64")


def test_discover_arch_tasks_inspects_other_architecture_for_noarch_outputs() -> None:
    """A closed architecture-restricted build can still publish shared RPMs."""
    assert acquisition.discover_arch_tasks(
        _task_hub([_arch_task(30, "aarch64")]), 10, "x86_64",
    ) == [{"architecture": "aarch64", "taskId": 30}]


def test_discover_arch_tasks_requires_a_completed_architecture_build() -> None:
    """An empty root must not masquerade as an architecture restriction."""
    with pytest.raises(RuntimeError, match="no buildArch tasks"):
        acquisition.discover_arch_tasks(_task_hub([]), 10, "x86_64")


@pytest.mark.parametrize("root_request", [
    None, [], ["source"], ["source", 13, {}, "unexpected"],
    ["source", 13, "invalid"], ["source", 13, {"arch_override": ["x86_64"]}],
])
def test_discover_arch_tasks_rejects_malformed_root_request(root_request: object) -> None:
    """Prove the root's build scope before treating absent architectures as valid."""
    hub = Mock()
    hub.getTaskInfo.return_value = {"id": 10, "method": "build", "state": 2, "request": root_request}
    with pytest.raises(RuntimeError, match="malformed"):
        acquisition.discover_arch_tasks(hub, 10, "aarch64")


@pytest.mark.parametrize(("architecture", "override"), [
    ("aarch64", "x86_64"), ("x86_64", "aarch64"),
])
def test_discover_arch_tasks_rejects_override_excluding_repository_architecture(
    architecture: str, override: str,
) -> None:
    """A deliberately narrowed scratch build does not prove native coverage."""
    hub = Mock()
    hub.getTaskInfo.return_value = {
        "id": 10, "method": "build", "state": 2,
        "request": ["source", 13, {"scratch": True, "arch_override": override}],
    }
    with pytest.raises(RuntimeError, match=f"architecture override excluding {architecture}"):
        acquisition.discover_arch_tasks(hub, 10, architecture)


@pytest.mark.parametrize("options", [None, {}, {"arch_override": "x86_64 aarch64"}])
def test_discover_arch_tasks_accepts_complete_root_architecture_scope(
    options: object,
) -> None:
    """Default and full-architecture requests retain normal task selection."""
    hub = _task_hub([_arch_task(20, "x86_64"), _arch_task(30, "aarch64")])
    hub.getTaskInfo.return_value["request"] = ["source", 13, options]
    assert acquisition.discover_arch_tasks(hub, 10, "aarch64") == [
        {"architecture": "aarch64", "taskId": 30},
    ]


def _output_hub(rpms: list[str] | None = None, outputs: object = None) -> Mock:
    filenames = rpms if rpms is not None else [
        "jq-1-1.x86_64.rpm",
        "jq-devel-1-1.x86_64.rpm",
        "jq-doc-1-1.noarch.rpm",
        "jq-debuginfo-1-1.x86_64.rpm",
        "jq-debugsource-1-1.x86_64.rpm",
    ]
    inventory = outputs if outputs is not None else {
        **{filename: ["DEFAULT"] for filename in filenames},
        "jq-1-1.src.rpm": ["DEFAULT"],
        "build.log": ["DEFAULT"],
    }
    hub = Mock()
    hub.getTaskResult.return_value = {"rpms": [f"tasks/20/20/{filename}" for filename in filenames]}
    hub.listTaskOutput.return_value = inventory
    return hub


def test_discover_rpm_outputs_keeps_complete_publishable_binary_set() -> None:
    """Verify debug outputs too, then exclude source/debug RPMs and logs."""
    hub = _output_hub()

    assert acquisition.discover_rpm_outputs(hub, 20, "x86_64") == [
        "jq-1-1.x86_64.rpm",
        "jq-devel-1-1.x86_64.rpm",
        "jq-doc-1-1.noarch.rpm",
    ]
    hub.getTaskResult.assert_called_once_with(20)
    hub.listTaskOutput.assert_called_once_with(20, all_volumes=True, strict=True)


@pytest.mark.parametrize("architecture", ["x86_64", "aarch64", "noarch"])
def test_discover_rpm_outputs_accepts_noarch_only(architecture: str) -> None:
    """Noarch RPMs are valid in both architecture views and pure-noarch tasks."""
    assert acquisition.discover_rpm_outputs(
        _output_hub(["jq-doc-1-1.noarch.rpm"]), 20, architecture,
    ) == ["jq-doc-1-1.noarch.rpm"]


@pytest.mark.parametrize("rpms", [
    [], ["../secret.x86_64.rpm"], ["dir/jq-1-1.x86_64.rpm"],
    ["jq-1-1.aarch64.rpm"], ["jq-1-1.src.rpm"],
    ["jq-1-1.x86_64.rpm", "jq-1-1.x86_64.rpm"],
    ["jq\\bad-1-1.x86_64.rpm"], ["jq\nbad-1-1.x86_64.rpm"],
])
def test_discover_rpm_outputs_rejects_invalid_manifests(rpms: list[str]) -> None:
    """Reject empty, unsafe, duplicate, source, or wrong-architecture results."""
    with pytest.raises((RuntimeError, ValueError), match=r"RPM result|Unsafe"):
        acquisition.discover_rpm_outputs(_output_hub(rpms), 20, "x86_64")


def test_discover_rpm_outputs_rejects_another_tasks_result_paths() -> None:
    """Never reconstruct a filename in this task from another task's output."""
    hub = _output_hub()
    hub.getTaskResult.return_value = {"rpms": ["tasks/21/21/jq-1-1.x86_64.rpm"]}
    with pytest.raises(RuntimeError, match=r"invalid.*RPM result path"):
        acquisition.discover_rpm_outputs(hub, 20, "x86_64")


@pytest.mark.parametrize("result", [None, [], {}, {"rpms": "not-an-array"}, {"rpms": [None]}])
def test_discover_rpm_outputs_rejects_malformed_result(result: object) -> None:
    """Malformed metadata is an error rather than a successful empty candidate."""
    hub = _output_hub()
    hub.getTaskResult.return_value = result
    with pytest.raises((RuntimeError, TypeError), match=r"RPM result|RPM result manifest"):
        acquisition.discover_rpm_outputs(hub, 20, "x86_64")


@pytest.mark.parametrize(("outputs", "message"), [
    ({}, "missing="),
    ({"jq-1-1.x86_64.rpm": ["DEFAULT"], "extra-1-1.x86_64.rpm": ["DEFAULT"]}, "unexpected="),
    ({"jq-1-1.x86_64.rpm": ["ARCHIVE"]}, "unsupported or ambiguous volumes"),
    ({"jq-1-1.x86_64.rpm": ["DEFAULT", "ARCHIVE"]}, "unsupported or ambiguous volumes"),
    ({"jq-1-1.x86_64.rpm": []}, "unsupported or ambiguous volumes"),
    ({"jq-1-1.x86_64.rpm": "DEFAULT"}, "unsupported or ambiguous volumes"),
    ([], "malformed output inventory"),
    ({20: ["DEFAULT"]}, "malformed output inventory"),
])
def test_discover_rpm_outputs_rejects_incomplete_or_unsupported_inventory(
    outputs: object, message: str,
) -> None:
    """Do not treat a partial/default-volume-only listing as complete output."""
    with pytest.raises(RuntimeError, match=message):
        acquisition.discover_rpm_outputs(
            _output_hub(["jq-1-1.x86_64.rpm"], outputs), 20, "x86_64",
        )


def test_discover_rpm_outputs_checks_debug_output_completeness() -> None:
    """Filtering debug RPMs must not hide incomplete task metadata."""
    hub = _output_hub(
        ["jq-1-1.x86_64.rpm", "jq-debuginfo-1-1.x86_64.rpm"],
        {"jq-1-1.x86_64.rpm": ["DEFAULT"]},
    )
    with pytest.raises(RuntimeError, match=r"missing=.*jq-debuginfo"):
        acquisition.discover_rpm_outputs(hub, 20, "x86_64")


def test_discover_rpm_outputs_requires_publishable_binary() -> None:
    """One empty selected task cannot be hidden by another task's outputs."""
    with pytest.raises(RuntimeError, match="no publishable binary RPMs"):
        acquisition.discover_rpm_outputs(
            _output_hub(["jq-debuginfo-1-1.x86_64.rpm"]), 20, "x86_64",
        )


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

    assert acquisition.select_completed_component_tasks(results, {"jq", "oniguruma"}) == [
        {"component": "jq", "rootTaskId": 20},
        {"component": "oniguruma", "rootTaskId": 30},
    ]


def test_select_completed_component_tasks_rejects_missing_expected_component() -> None:
    """Do not check closure against only the successful subset of a build."""
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

    with pytest.raises(RuntimeError, match=r"oniguruma \(failed\)"):
        acquisition.select_completed_component_tasks(results, {"jq", "oniguruma"})


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
[default-component-config.publish]
rpm-channel = "rpm-sdk"

[component-groups.base-packages]
default-component-config.publish.rpm-channel = "rpm-base"
components = ["jq"]

[package-groups.exceptions-packages]
default-package-config.publish.rpm-channel = "rpm-sdk"
packages = [
    "jq-doc", # srpm: jq
]
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


@pytest.mark.parametrize(
    ("overall", "koji"),
    [("Completed", "Failed"), ("Completed", "Canceled"), ("Failed", "Closed")],
)
def test_select_completed_component_tasks_rejects_disagreeing_statuses(
    overall: str, koji: str,
) -> None:
    """An overall Completed label cannot disguise a failed Koji build."""
    results = {"buildTasks": [{
        "taskStatus": overall,
        "kojiInfo": {
            "componentName": "jq", "kojiTaskNumber": 20, "kojiTaskStatus": koji,
        },
    }]}
    with pytest.raises(RuntimeError, match="no completed"):
        acquisition.select_completed_component_tasks(results, {"jq"})


def test_select_completed_component_tasks_rejects_ambiguous_successful_retries() -> None:
    """Report the component and task IDs before downloading duplicate outputs."""
    results = {"buildTasks": [
        {
            "taskStatus": "Completed",
            "kojiInfo": {
                "componentName": "jq", "kojiTaskNumber": task_id,
                "kojiTaskStatus": "Closed",
            },
        }
        for task_id in [20, 30]
    ]}
    with pytest.raises(RuntimeError, match=r"component jq.*\[20, 30\]"):
        acquisition.select_completed_component_tasks(results, {"jq"})


@pytest.fixture
def acquisition_args(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path,
) -> argparse.Namespace:
    """Prepare one complete Control Tower component transaction without network I/O."""
    job_id_file = tmp_path / "job-id.txt"
    job_id_file.write_text("test-job\n", encoding="utf-8")
    expected_file = tmp_path / "components.json"
    expected_file.write_text(json.dumps(["jq"]), encoding="utf-8")
    replaced_file = tmp_path / "replaced.json"
    replaced_file.write_text(json.dumps(["deleted-component"]), encoding="utf-8")
    args = argparse.Namespace(
        api_audience="api://control-tower",
        api_base_url="https://ct.example",
        architecture="x86_64",
        candidate_base_dir=tmp_path / "base",
        candidate_sdk_dir=tmp_path / "sdk",
        download_directory=tmp_path / "downloads",
        expected_components_file=expected_file,
        insecure_koji_tls=False,
        job_id_file=job_id_file,
        koji_files_url="https://koji.example/kojifiles",
        koji_hub_url="https://koji.example/kojihub",
        publish_policy=tmp_path / "publish.toml",
        report=tmp_path / "report.json",
        replaced_components_file=replaced_file,
    )
    args.publish_policy.write_text(
        """
default-component-config.publish.rpm-channel = "rpm-sdk"
[component-groups.base-packages]
components = []
default-component-config.publish.rpm-channel = "rpm-base"
[package-groups.exceptions-packages]
packages = []
default-package-config.publish.rpm-channel = "rpm-sdk"
""",
        encoding="utf-8",
    )
    monkeypatch.setattr(acquisition.ct, "make_credential", Mock())
    monkeypatch.setattr(acquisition.ct, "get_token", Mock(return_value="test-token"))
    monkeypatch.setattr(acquisition.ct, "get_koji_package_results", Mock(return_value={
        "buildTasks": [{
            "taskStatus": "Completed",
            "kojiInfo": {
                "componentName": "jq", "kojiTaskNumber": 10, "kojiTaskStatus": "Closed",
            },
        }],
    }))
    return args


@pytest.mark.parametrize("architecture", ["x86_64", "aarch64"])
@pytest.mark.parametrize("missing_output", [False, True])
@pytest.mark.parametrize("insecure", [False, True])
def test_run_acquisition_uses_structured_discovery_before_downloading(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, acquisition_args: argparse.Namespace,
    architecture: str, *, missing_output: bool, insecure: bool,
) -> None:
    """Check each architecture and noarch outputs without mixing native RPMs."""
    args = acquisition_args
    args.architecture = architecture
    args.insecure_koji_tls = insecure
    rpm_path = tmp_path / f"jq-1-1.{architecture}.rpm"
    rpm_path.write_bytes(acquisition.RPM_MAGIC)
    noarch_path = tmp_path / "jq-doc-1-1.noarch.rpm"
    noarch_path.write_bytes(acquisition.RPM_MAGIC)
    task_id = 20 if architecture == "x86_64" else 30
    hub = _task_hub([_arch_task(20, "x86_64"), _arch_task(30, "aarch64")])
    hub.getTaskResult.return_value = {"rpms": [
        f"tasks/{task_id}/{task_id}/{rpm_path.name}",
        f"tasks/{task_id}/{task_id}/{noarch_path.name}",
    ]}
    hub.listTaskOutput.return_value = {} if missing_output else {
        rpm_path.name: ["DEFAULT"], noarch_path.name: ["DEFAULT"],
    }
    make_client = Mock(return_value=hub)
    monkeypatch.setattr(acquisition, "make_koji_client", make_client)
    first_candidate = _candidate(rpm_path, "jq", architecture)
    download = Mock(side_effect=[first_candidate, _candidate(noarch_path, "jq", "noarch")])
    monkeypatch.setattr(acquisition, "download_rpm", download)
    route = Mock()
    monkeypatch.setattr(acquisition, "route_candidates", route)

    if missing_output:
        with pytest.raises(RuntimeError, match="inventory disagrees"):
            acquisition.run_acquisition(args)
        download.assert_not_called()
        route.assert_not_called()
        return

    report = acquisition.run_acquisition(args)

    assert report["result"] == "passed"
    assert report["architecture"] == architecture
    assert report["acquisition"]["kojiHubUrl"] == args.koji_hub_url
    assert report["acquisition"]["kojiDiscovery"] == "xmlrpc-result-manifest-and-output-inventory"
    assert report["schemaVersion"] == TEST_REPORT_SCHEMA_VERSION
    assert report["acquisition"]["kojiClientVersion"] == koji.__version__
    assert report["acquisition"]["kojiTlsCertificateVerification"] is not insecure
    assert report["acquisition"]["retryPolicy"] == {
        "maximumRetries": acquisition.MAX_REQUEST_RETRIES,
        "requestTimeoutSeconds": acquisition.REQUEST_TIMEOUT_SECONDS,
        "type": "koji-client-and-http-adapter",
    }
    assert report["acquisition"]["kojiPackageTasks"] == [{
        "architectureTaskIds": [task_id],
        "architectureTasks": [{"architecture": architecture, "taskId": task_id}],
        "component": "jq",
        "hasMatchingArchitectureTask": True,
        "rootTaskId": 10,
    }]
    assert json.loads(args.replaced_components_file.read_text(encoding="utf-8")) == [
        "deleted-component", "jq",
    ]
    assert download.call_count == len(report["candidates"])
    assert download.call_args.kwargs["session"].verify is not insecure
    make_client.assert_called_once_with(args.koji_hub_url, insecure=insecure)
    assert download.call_args.kwargs["task_id"] == task_id
    assert download.call_args_list[0].kwargs["filename"] == rpm_path.name
    assert download.call_args.kwargs["koji_files_url"] == args.koji_files_url
    route.assert_called_once()


@pytest.mark.parametrize("architecture", ["x86_64", "aarch64"])
@pytest.mark.parametrize("include_noarch", [False, True])
@pytest.mark.parametrize("missing_output", [False, True])
def test_run_acquisition_handles_architecture_restricted_components(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, acquisition_args: argparse.Namespace,
    capsys: pytest.CaptureFixture[str], architecture: str, *, include_noarch: bool, missing_output: bool,
) -> None:
    """Keep shared outputs and removals without accepting incomplete other-arch data."""
    args = acquisition_args
    args.architecture = architecture
    other_architecture = "aarch64" if architecture == "x86_64" else "x86_64"
    filenames = [f"jq-1-1.{other_architecture}.rpm"]
    if include_noarch:
        filenames.append("jq-doc-1-1.noarch.rpm")
    hub = _task_hub([_arch_task(20, other_architecture)])
    hub.getTaskResult.return_value = {"rpms": [f"tasks/20/20/{filename}" for filename in filenames]}
    hub.listTaskOutput.return_value = {} if missing_output else {
        filename: ["DEFAULT"] for filename in filenames
    }
    monkeypatch.setattr(acquisition, "make_koji_client", Mock(return_value=hub))
    noarch_path = tmp_path / "jq-doc-1-1.noarch.rpm"
    noarch_path.write_bytes(acquisition.RPM_MAGIC)
    download = Mock(return_value=_candidate(noarch_path, "jq", "noarch"))
    monkeypatch.setattr(acquisition, "download_rpm", download)
    monkeypatch.setattr(acquisition, "query_package_name", Mock(return_value="jq-doc"))

    if missing_output:
        with pytest.raises(RuntimeError, match="inventory disagrees"):
            acquisition.run_acquisition(args)
        download.assert_not_called()
        return

    report = acquisition.run_acquisition(args)

    assert report["result"] == "passed"
    assert report["architecture"] == architecture
    assert report["acquisition"]["kojiPackageTasks"] == [{
        "architectureTaskIds": [20],
        "architectureTasks": [{"architecture": other_architecture, "taskId": 20}],
        "component": "jq",
        "hasMatchingArchitectureTask": False,
        "rootTaskId": 10,
    }]
    assert json.loads(args.replaced_components_file.read_text(encoding="utf-8")) == [
        "deleted-component", "jq",
    ]
    assert list(args.candidate_base_dir.iterdir()) == []
    assert [path.name for path in args.candidate_sdk_dir.iterdir()] == (
        ["jq-doc-1-1.noarch.rpm"] if include_noarch else []
    )
    assert len(report["candidates"]) == int(include_noarch)
    if include_noarch:
        download.assert_called_once()
        assert download.call_args.kwargs["filename"] == noarch_path.name
    else:
        download.assert_not_called()
    assert f"has no {architecture} buildArch task" in capsys.readouterr().err


@pytest.mark.parametrize("architecture", ["x86_64", "aarch64"])
def test_run_acquisition_accepts_noarch_only_component(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, acquisition_args: argparse.Namespace,
    architecture: str,
) -> None:
    """A logical noarch task supplies the same package to either repository view."""
    args = acquisition_args
    args.architecture = architecture
    noarch_path = tmp_path / "jq-doc-1-1.noarch.rpm"
    noarch_path.write_bytes(acquisition.RPM_MAGIC)
    hub = _task_hub([_arch_task(20, "noarch")])
    hub.getTaskResult.return_value = {"rpms": [f"tasks/20/20/{noarch_path.name}"]}
    hub.listTaskOutput.return_value = {noarch_path.name: ["DEFAULT"]}
    monkeypatch.setattr(acquisition, "make_koji_client", Mock(return_value=hub))
    download = Mock(return_value=_candidate(noarch_path, "jq", "noarch"))
    monkeypatch.setattr(acquisition, "download_rpm", download)
    monkeypatch.setattr(acquisition, "query_package_name", Mock(return_value="jq-doc"))

    report = acquisition.run_acquisition(args)

    assert report["result"] == "passed"
    assert report["acquisition"]["kojiPackageTasks"][0]["hasMatchingArchitectureTask"]
    assert report["candidates"][0]["architecture"] == "noarch"
    assert (args.candidate_sdk_dir / noarch_path.name).is_file()
    download.assert_called_once()


def test_run_acquisition_deduplicates_shared_noarch_within_closed_root(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, acquisition_args: argparse.Namespace,
) -> None:
    """Duplicate noarch outputs from one finalized build are one candidate RPM."""
    args = acquisition_args
    noarch_path = tmp_path / "jq-doc-1-1.noarch.rpm"
    noarch_path.write_bytes(acquisition.RPM_MAGIC)
    native_path = tmp_path / "jq-1-1.x86_64.rpm"
    native_path.write_bytes(acquisition.RPM_MAGIC)
    hub = _task_hub([_arch_task(20, "x86_64"), _arch_task(35, "noarch")])
    hub.getTaskResult.side_effect = [
        {"rpms": [f"tasks/35/35/{noarch_path.name}"]},
        {"rpms": [f"tasks/20/20/{filename}" for filename in [native_path.name, noarch_path.name]]},
    ]
    hub.listTaskOutput.side_effect = [
        {noarch_path.name: ["DEFAULT"]},
        {native_path.name: ["DEFAULT"], noarch_path.name: ["DEFAULT"]},
    ]
    monkeypatch.setattr(acquisition, "make_koji_client", Mock(return_value=hub))
    download = Mock(side_effect=[
        _candidate(native_path, "jq"), _candidate(noarch_path, "jq", "noarch"),
    ])
    monkeypatch.setattr(acquisition, "download_rpm", download)
    monkeypatch.setattr(acquisition, "query_package_name", lambda path: (
        "jq-doc" if path.name == noarch_path.name else "jq"
    ))

    report = acquisition.run_acquisition(args)

    assert report["result"] == "passed"
    assert {candidate["filename"] for candidate in report["candidates"]} == {
        native_path.name, noarch_path.name,
    }
    assert download.call_count == len(report["candidates"])


@pytest.mark.parametrize("error", [
    koji.GenericError("Koji task failed"),
    requests.Timeout("Koji hub timed out"),
    acquisition.ExpatError("malformed XML"),
    xmlrpc.client.Fault(123, "unknown hub fault"),
])
def test_main_reports_official_client_errors(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, error: Exception,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Preserve failure reports and pipeline errors for upstream exceptions."""
    report_path = tmp_path / "acquisition.json"
    monkeypatch.setattr(acquisition, "_parse_args", Mock(return_value=argparse.Namespace(
        report=report_path, insecure_koji_tls=False,
    )))
    monkeypatch.setattr(acquisition, "run_acquisition", Mock(side_effect=error))

    assert acquisition.main() == 1
    assert json.loads(report_path.read_text(encoding="utf-8")) == {
        "error": str(error), "result": "failed", "schemaVersion": 3,
    }
    assert "##vso[task.logissue type=error]" in capsys.readouterr().err
