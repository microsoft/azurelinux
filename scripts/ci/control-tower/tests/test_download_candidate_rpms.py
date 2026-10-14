"""Tests for Control Tower and Koji candidate RPM acquisition."""

from __future__ import annotations

import argparse
import errno
import hashlib
import http.client
import json
import socket
import ssl
import urllib.error
import urllib.request
import xmlrpc.client
from email.message import Message
from email.utils import formatdate
from typing import TYPE_CHECKING
from unittest.mock import Mock

import download_candidate_rpms as acquisition
import pytest

TEST_TASK_ID = 12345
TEST_WALL_TIME = 1_700_000_000
RETRIED_ATTEMPTS = 2

if TYPE_CHECKING:
    from pathlib import Path


@pytest.fixture(autouse=True)
def retry_clock(monkeypatch: pytest.MonkeyPatch) -> Mock:
    """Make retry timing deterministic without sleeping in unit tests."""
    clock = Mock()
    clock.monotonic.return_value = 0.0
    clock.time.return_value = TEST_WALL_TIME

    def advance(seconds: float) -> None:
        clock.monotonic.return_value += seconds

    clock.sleep.side_effect = advance
    monkeypatch.setattr(acquisition, "time", clock)
    monkeypatch.setattr(acquisition.RETRY_RANDOM, "uniform", Mock(return_value=0.0))
    return clock


def _candidate(
    path: Path, component: str, architecture: str = "x86_64",
) -> acquisition.DownloadedRpm:
    return {
        "architecture": architecture,
        "component": component,
        "downloadAttempts": 1,
        "filename": path.name,
        "name": "",
        "path": str(path),
        "repository": "",
        "sha256": "abc",
        "size": path.stat().st_size,
        "taskId": TEST_TASK_ID,
        "transferredBytes": path.stat().st_size,
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


def _rpc_response(body: bytes, headers: dict[str, str] | None = None) -> Mock:
    response = Mock()
    response.__enter__ = Mock(return_value=response)
    response.__exit__ = Mock(return_value=False)
    response.headers = headers or {}
    response.read1.side_effect = [body, b""]
    return response


def _http_error(status: int, retry_after: str | None = None) -> urllib.error.HTTPError:
    headers = Message()
    if retry_after is not None:
        headers["Retry-After"] = retry_after
    return urllib.error.HTTPError("https://koji.example/kojihub", status, "test error", headers, None)


def test_koji_client_posts_xmlrpc_with_tls_context_and_timeout(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Use Koji's positional API arguments without an unbounded transport."""
    body = xmlrpc.client.dumps(({"state": 2},), methodresponse=True).encode()
    urlopen = Mock(return_value=_rpc_response(body))
    monkeypatch.setattr(urllib.request, "urlopen", urlopen)
    context = ssl.create_default_context()
    hub = acquisition.KojiClient("https://koji.example/kojihub", context)

    assert hub.call("getTaskInfo", (20, False, True)) == {"state": 2}

    request = urlopen.call_args.args[0]
    assert request.full_url == hub.url
    assert request.get_method() == "POST"
    assert xmlrpc.client.loads(request.data) == ((20, False, True), "getTaskInfo")
    assert urlopen.call_args.kwargs == {
        "context": context, "timeout": acquisition.REQUEST_TIMEOUT_SECONDS,
    }


@pytest.mark.parametrize("advertised_length", [False, True])
def test_koji_client_bounds_response_size(
    monkeypatch: pytest.MonkeyPatch, advertised_length: bool, retry_clock: Mock,
) -> None:
    """Reject oversized metadata both with and without Content-Length."""
    monkeypatch.setattr(acquisition, "MAX_KOJI_RESPONSE_SIZE", 64)
    headers = {"Content-Length": "65"} if advertised_length else {}
    response = _rpc_response(b"x" * 65, headers)
    urlopen = Mock(return_value=response)
    monkeypatch.setattr(urllib.request, "urlopen", urlopen)
    hub = acquisition.KojiClient("https://koji.example/kojihub", ssl.create_default_context())

    with pytest.raises(RuntimeError, match=r"getTaskInfo.*exceeds the size limit"):
        hub.call("getTaskInfo", (20,))

    if advertised_length:
        response.read1.assert_not_called()
    urlopen.assert_called_once()
    retry_clock.sleep.assert_not_called()


@pytest.mark.parametrize("body", [
    b"<broken",
    xmlrpc.client.dumps(xmlrpc.client.Fault(1, "missing task")).encode(),
    b"<methodResponse><params/></methodResponse>",
])
def test_koji_client_surfaces_protocol_errors(
    monkeypatch: pytest.MonkeyPatch, body: bytes, retry_clock: Mock,
) -> None:
    """No malformed response or XML-RPC fault may become empty output."""
    urlopen = Mock(return_value=_rpc_response(body))
    monkeypatch.setattr(urllib.request, "urlopen", urlopen)
    hub = acquisition.KojiClient("https://koji.example/kojihub", ssl.create_default_context())

    with pytest.raises(RuntimeError, match=r"getTaskInfo.*koji.example"):
        hub.call("getTaskInfo", (20,))
    urlopen.assert_called_once()
    retry_clock.sleep.assert_not_called()


def test_koji_client_restarts_interrupted_response(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Do not combine partial XML from one attempt with a complete fresh reply."""
    body = xmlrpc.client.dumps(({"state": 2},), methodresponse=True).encode()
    failed = _rpc_response(b"")
    failed.read1.side_effect = [body[:10], TimeoutError("timed out")]
    urlopen = Mock(side_effect=[failed, _rpc_response(body, {"Content-Length": str(len(body))})])
    monkeypatch.setattr(urllib.request, "urlopen", urlopen)
    hub = acquisition.KojiClient("https://koji.example/kojihub", ssl.create_default_context())

    assert hub.call("getTaskInfo", (20,)) == {"state": 2}
    assert urlopen.call_count == RETRIED_ATTEMPTS
    failed.__exit__.assert_called_once()


@pytest.mark.parametrize("length", ["-1", "invalid", "1"])
def test_koji_client_does_not_retry_invalid_content_length(
    monkeypatch: pytest.MonkeyPatch, retry_clock: Mock, length: str,
) -> None:
    """Malformed or inconsistent metadata length is not a transient failure."""
    body = xmlrpc.client.dumps(([],), methodresponse=True).encode()
    urlopen = Mock(return_value=_rpc_response(body, {"Content-Length": length}))
    monkeypatch.setattr(urllib.request, "urlopen", urlopen)
    hub = acquisition.KojiClient("https://koji.example/kojihub", ssl.create_default_context())

    with pytest.raises(RuntimeError, match=r"getTaskInfo.*koji.example"):
        hub.call("getTaskInfo", (20,))
    urlopen.assert_called_once()
    retry_clock.sleep.assert_not_called()


@pytest.mark.parametrize(("error", "attempts"), [
    (urllib.error.URLError("connection reset"), 1),
    (TimeoutError("timed out"), acquisition.MAX_REQUEST_ATTEMPTS),
    (ssl.SSLCertVerificationError("untrusted certificate"), 1),
    (http.client.IncompleteRead(b"partial"), acquisition.MAX_REQUEST_ATTEMPTS),
])
def test_koji_client_surfaces_transport_errors_without_fallback(
    monkeypatch: pytest.MonkeyPatch, error: OSError | http.client.HTTPException, attempts: int,
) -> None:
    """Keep network and certificate failures loud and preserve request context."""
    urlopen = Mock(side_effect=error)
    monkeypatch.setattr(urllib.request, "urlopen", urlopen)
    hub = acquisition.KojiClient("https://koji.example/kojihub", ssl.create_default_context())

    with pytest.raises(RuntimeError, match=r"getTaskChildren.*koji.example"):
        hub.call("getTaskChildren", (10, True, True))

    assert urlopen.call_count == attempts


@pytest.mark.parametrize("method", sorted(acquisition.READ_ONLY_KOJI_METHODS))
def test_koji_client_retries_only_allowlisted_metadata_methods(
    monkeypatch: pytest.MonkeyPatch, method: str,
) -> None:
    """A transient failure may replay any of the four explicitly read-only RPCs."""
    body = xmlrpc.client.dumps(({"ok": True},), methodresponse=True).encode()
    urlopen = Mock(side_effect=[
        urllib.error.URLError(ConnectionResetError("reset")),
        _rpc_response(body),
    ])
    monkeypatch.setattr(urllib.request, "urlopen", urlopen)
    hub = acquisition.KojiClient("https://koji.example/kojihub", ssl.create_default_context())

    assert hub.call(method, (20,)) == {"ok": True}
    assert urlopen.call_count == RETRIED_ATTEMPTS
    assert urlopen.call_args_list[0].args[0].data == urlopen.call_args_list[1].args[0].data


@pytest.mark.parametrize("method", ["build", "resubmitTask", "getAPIVersion"])
def test_koji_client_rejects_other_methods_before_sending(
    monkeypatch: pytest.MonkeyPatch, method: str,
) -> None:
    """Never grow metadata retries into arbitrary replayable Koji POSTs."""
    urlopen = Mock()
    monkeypatch.setattr(urllib.request, "urlopen", urlopen)
    hub = acquisition.KojiClient("https://koji.example/kojihub", ssl.create_default_context())

    with pytest.raises(ValueError, match="Unsupported Koji metadata method"):
        hub.call(method, (20,))
    urlopen.assert_not_called()


@pytest.mark.parametrize("status", [408, 429, 500, 502, 503, 504])
def test_koji_client_retries_selected_http_errors(
    monkeypatch: pytest.MonkeyPatch, status: int, retry_clock: Mock,
) -> None:
    """Close error responses before a bounded retry of transient HTTP failures."""
    body = xmlrpc.client.dumps(([],), methodresponse=True).encode()
    error = _http_error(status)
    close = Mock()
    monkeypatch.setattr(error, "close", close)
    urlopen = Mock(side_effect=[error, _rpc_response(body)])
    monkeypatch.setattr(urllib.request, "urlopen", urlopen)
    hub = acquisition.KojiClient("https://koji.example/kojihub", ssl.create_default_context())

    assert hub.call("getTaskChildren", (20,)) == []
    assert urlopen.call_count == RETRIED_ATTEMPTS
    close.assert_called_once()
    retry_clock.sleep.assert_called_once_with(acquisition.RETRY_BACKOFF_SECONDS)


@pytest.mark.parametrize("error", [
    _http_error(status)
    for status in (400, 401, 403, 404, 409, 501)
] + [
    urllib.error.URLError(ssl.SSLCertVerificationError("untrusted certificate")),
    urllib.error.URLError(ssl.SSLError("TLS failure")),
    urllib.error.URLError(socket.gaierror(socket.EAI_NONAME, "unknown host")),
    PermissionError(errno.EACCES, "permission denied"),
    OSError(errno.ENOSPC, "disk full"),
    http.client.BadStatusLine("invalid status"),
])
def test_koji_client_does_not_retry_permanent_errors(
    monkeypatch: pytest.MonkeyPatch, error: OSError | http.client.HTTPException, retry_clock: Mock,
) -> None:
    """Configuration, certificate, authorization, and local failures are terminal."""
    urlopen = Mock(side_effect=error)
    monkeypatch.setattr(urllib.request, "urlopen", urlopen)
    hub = acquisition.KojiClient("https://koji.example/kojihub", ssl.create_default_context())

    with pytest.raises(RuntimeError, match=r"attempt 1/4"):
        hub.call("getTaskInfo", (20,))
    urlopen.assert_called_once()
    retry_clock.sleep.assert_not_called()


@pytest.mark.parametrize("error", [
    urllib.error.URLError(socket.gaierror(socket.EAI_AGAIN, "temporary DNS failure")),
    OSError(errno.ECONNRESET, "reset"),
    ConnectionAbortedError("aborted"),
    http.client.RemoteDisconnected("disconnected"),
])
def test_koji_client_retries_typed_transient_errors(
    monkeypatch: pytest.MonkeyPatch, error: OSError | http.client.HTTPException,
) -> None:
    """Use error types/codes, not exception-message substring guesses."""
    body = xmlrpc.client.dumps(([],), methodresponse=True).encode()
    urlopen = Mock(side_effect=[error, _rpc_response(body)])
    monkeypatch.setattr(urllib.request, "urlopen", urlopen)
    hub = acquisition.KojiClient("https://koji.example/kojihub", ssl.create_default_context())

    assert hub.call("getTaskChildren", (20,)) == []
    assert urlopen.call_count == RETRIED_ATTEMPTS


def test_koji_client_exhausts_bounded_attempts_with_backoff_and_jitter(
    monkeypatch: pytest.MonkeyPatch, retry_clock: Mock,
) -> None:
    """Persistent transport failures terminate with attempt and URL evidence."""
    monkeypatch.setattr(acquisition.RETRY_RANDOM, "uniform", Mock(return_value=0.5))
    urlopen = Mock(side_effect=TimeoutError("timeout"))
    monkeypatch.setattr(urllib.request, "urlopen", urlopen)
    hub = acquisition.KojiClient("https://koji.example/kojihub", ssl.create_default_context())

    with pytest.raises(RuntimeError, match=r"koji.example.*attempt 4/4"):
        hub.call("getTaskInfo", (20,))

    assert urlopen.call_count == acquisition.MAX_REQUEST_ATTEMPTS
    assert [call.args[0] for call in retry_clock.sleep.call_args_list] == [2.5, 4.5, 8.5]


@pytest.mark.parametrize(("header", "delay"), [
    ("5", 5.0),
    (formatdate(TEST_WALL_TIME + 10, usegmt=True), 10.0),
    (formatdate(TEST_WALL_TIME - 10, usegmt=True), float(acquisition.RETRY_BACKOFF_SECONDS)),
    ("invalid", float(acquisition.RETRY_BACKOFF_SECONDS)),
])
def test_koji_client_handles_bounded_retry_after(
    monkeypatch: pytest.MonkeyPatch, retry_clock: Mock, header: str, delay: float,
) -> None:
    """Honor valid bounded delta/date delays; malformed headers use logged backoff."""
    body = xmlrpc.client.dumps(([],), methodresponse=True).encode()
    error = _http_error(429, header)
    monkeypatch.setattr(urllib.request, "urlopen", Mock(side_effect=[error, _rpc_response(body)]))
    hub = acquisition.KojiClient("https://koji.example/kojihub", ssl.create_default_context())

    assert hub.call("getTaskChildren", (20,)) == []
    retry_clock.sleep.assert_called_once_with(delay)


@pytest.mark.parametrize("header", [
    str(acquisition.MAX_RETRY_DELAY_SECONDS + 1),
    formatdate(TEST_WALL_TIME + 3600, usegmt=True),
    "9" * 1000,
])
def test_koji_client_rejects_excessive_retry_after(
    monkeypatch: pytest.MonkeyPatch, retry_clock: Mock, header: str,
) -> None:
    """Do not sleep unboundedly or retry sooner than a server's long minimum."""
    error = _http_error(429, header)
    urlopen = Mock(side_effect=error)
    monkeypatch.setattr(urllib.request, "urlopen", urlopen)
    hub = acquisition.KojiClient("https://koji.example/kojihub", ssl.create_default_context())

    with pytest.raises(RuntimeError, match="Retry-After exceeds"):
        hub.call("getTaskChildren", (20,))
    urlopen.assert_called_once()
    retry_clock.sleep.assert_not_called()


def test_koji_client_stops_after_elapsed_deadline(
    monkeypatch: pytest.MonkeyPatch, retry_clock: Mock,
) -> None:
    """The attempt limit must not restart an expired overall operation window."""
    def expire(*_args: object, **_kwargs: object) -> None:
        retry_clock.monotonic.return_value = acquisition.MAX_OPERATION_SECONDS
        raise TimeoutError("timed out")

    urlopen = Mock(side_effect=expire)
    monkeypatch.setattr(urllib.request, "urlopen", urlopen)
    hub = acquisition.KojiClient("https://koji.example/kojihub", ssl.create_default_context())

    with pytest.raises(RuntimeError, match=r"remaining retry window: 0.0s"):
        hub.call("getTaskInfo", (20,))
    urlopen.assert_called_once()
    retry_clock.sleep.assert_not_called()


def test_koji_client_clamps_timeout_to_remaining_window(
    monkeypatch: pytest.MonkeyPatch, retry_clock: Mock,
) -> None:
    """A final attempt cannot receive a fresh full socket timeout."""
    remaining = 10
    body = xmlrpc.client.dumps(([],), methodresponse=True).encode()
    calls = 0

    def respond(*_args: object, **_kwargs: object) -> Mock:
        nonlocal calls
        calls += 1
        if calls == 1:
            retry_clock.monotonic.return_value = acquisition.MAX_OPERATION_SECONDS - remaining
            raise TimeoutError("timed out")
        return _rpc_response(body)

    urlopen = Mock(side_effect=respond)
    monkeypatch.setattr(urllib.request, "urlopen", urlopen)
    hub = acquisition.KojiClient("https://koji.example/kojihub", ssl.create_default_context())

    assert hub.call("getTaskChildren", (20,)) == []
    assert urlopen.call_args.kwargs["timeout"] == remaining - acquisition.RETRY_BACKOFF_SECONDS


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
    hub = Mock(spec=acquisition.KojiClient)
    hub.call.side_effect = [
        {
            "id": 10, "method": "build", "state": state,
            "request": ["source", 13, {"scratch": True}],
        },
        children,
    ]
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
    assert hub.call.call_args_list[0].args == ("getTaskInfo", (10, True, True))
    assert hub.call.call_args_list[1].args == ("getTaskChildren", (10, True, True))


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
    hub = Mock(spec=acquisition.KojiClient)
    hub.call.return_value = {"id": 10, "method": "build", "state": 2, "request": root_request}
    with pytest.raises(RuntimeError, match="malformed"):
        acquisition.discover_arch_tasks(hub, 10, "aarch64")


@pytest.mark.parametrize(("architecture", "override"), [
    ("aarch64", "x86_64"), ("x86_64", "aarch64"),
])
def test_discover_arch_tasks_rejects_override_excluding_repository_architecture(
    architecture: str, override: str,
) -> None:
    """A deliberately narrowed scratch build does not prove native coverage."""
    hub = Mock(spec=acquisition.KojiClient)
    hub.call.return_value = {
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
    hub = _task_hub([])
    hub.call.side_effect = [
        {"id": 10, "method": "build", "state": 2, "request": ["source", 13, options]},
        [_arch_task(20, "x86_64"), _arch_task(30, "aarch64")],
    ]
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
    hub = Mock(spec=acquisition.KojiClient, url="https://koji.example/kojihub")
    hub.call.side_effect = [
        {"rpms": [f"tasks/20/20/{filename}" for filename in filenames]},
        inventory,
    ]
    return hub


def test_discover_rpm_outputs_keeps_complete_publishable_binary_set() -> None:
    """Verify debug outputs too, then exclude source/debug RPMs and logs."""
    hub = _output_hub()

    assert acquisition.discover_rpm_outputs(hub, 20, "x86_64") == [
        "jq-1-1.x86_64.rpm",
        "jq-devel-1-1.x86_64.rpm",
        "jq-doc-1-1.noarch.rpm",
    ]
    assert hub.call.call_args_list[0].args == ("getTaskResult", (20,))
    assert hub.call.call_args_list[1].args == ("listTaskOutput", (20, False, True, True))


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
    hub.call.side_effect = [
        {"rpms": ["tasks/21/21/jq-1-1.x86_64.rpm"]},
    ]
    with pytest.raises(RuntimeError, match=r"invalid.*RPM result path"):
        acquisition.discover_rpm_outputs(hub, 20, "x86_64")


@pytest.mark.parametrize("result", [None, [], {}, {"rpms": "not-an-array"}, {"rpms": [None]}])
def test_discover_rpm_outputs_rejects_malformed_result(result: object) -> None:
    """Malformed metadata is an error rather than a successful empty candidate."""
    hub = _output_hub()
    hub.call.side_effect = [result]
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
    response.read1.side_effect = [body[:2], body[2:], b""]
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
    assert result["sha256"] == hashlib.sha256(body).hexdigest()
    assert result["downloadAttempts"] == 1
    assert result["transferredBytes"] == len(body)


def test_download_rpm_removes_invalid_output(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Do not leave HTML error bodies masquerading as candidate RPMs."""
    response = Mock()
    response.__enter__ = Mock(return_value=response)
    response.__exit__ = Mock(return_value=False)
    response.headers = {}
    response.read1.side_effect = [b"<html>not an rpm</html>", b""]
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


def test_download_rpm_rejects_truncated_content_length(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Require the response body to match its advertised complete size."""
    body = acquisition.RPM_MAGIC + b"short"
    response = Mock()
    response.__enter__ = Mock(return_value=response)
    response.__exit__ = Mock(return_value=False)
    response.headers = {"Content-Length": str(len(body) + 10)}
    response.read1.side_effect = [body, b""]
    monkeypatch.setattr(urllib.request, "urlopen", Mock(return_value=response))

    with pytest.raises(RuntimeError, match="does not match Content-Length"):
        acquisition.download_rpm(
            destination=tmp_path,
            filename="jq-1.8.1-8.azl4.x86_64.rpm",
            koji_files_url="https://koji.example/kojifiles",
            ssl_context=ssl.create_default_context(),
            source_component="jq",
            task_id=TEST_TASK_ID,
        )

    assert not (tmp_path / "jq-1.8.1-8.azl4.x86_64.rpm").exists()


def _download(tmp_path: Path, maximum_size: int = acquisition.MAX_RPM_SIZE) -> acquisition.DownloadedRpm:
    return acquisition.download_rpm(
        destination=tmp_path,
        filename="jq-1-1.x86_64.rpm",
        koji_files_url="https://koji.example/kojifiles",
        ssl_context=ssl.create_default_context(),
        source_component="jq",
        task_id=TEST_TASK_ID,
        maximum_size=maximum_size,
    )


@pytest.mark.parametrize("incomplete_read", [False, True])
def test_download_rpm_restarts_partial_transfer_cleanly(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, incomplete_read: bool,
) -> None:
    """Reset the file, hash, and response length, but retain all received bytes."""
    partial = acquisition.RPM_MAGIC + b"discarded prefix"
    body = acquisition.RPM_MAGIC + b"complete"
    failed = _rpc_response(b"", {"Content-Length": str(len(partial) + 10)})
    failed.read1.side_effect = (
        [http.client.IncompleteRead(partial)]
        if incomplete_read else [partial, ConnectionResetError("reset")]
    )
    successful = _rpc_response(body, {"Content-Length": str(len(body))})
    output_path = tmp_path / "jq-1-1.x86_64.rpm"
    calls = 0

    def respond(request: urllib.request.Request, **_kwargs: object) -> Mock:
        nonlocal calls
        calls += 1
        assert request.get_method() == "GET"
        assert not output_path.exists()
        return failed if calls == 1 else successful

    urlopen = Mock(side_effect=respond)
    monkeypatch.setattr(urllib.request, "urlopen", urlopen)

    result = _download(tmp_path)

    assert output_path.read_bytes() == body
    assert result["size"] == len(body)
    assert result["sha256"] == hashlib.sha256(body).hexdigest()
    assert result["downloadAttempts"] == RETRIED_ATTEMPTS
    assert result["transferredBytes"] == len(partial) + len(body)
    failed.__exit__.assert_called_once()
    successful.__exit__.assert_called_once()


@pytest.mark.parametrize("advertised_length", [False, True])
def test_download_rpm_retry_cannot_reset_transfer_budget(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, advertised_length: bool,
) -> None:
    """A failed prefix still consumes the same aggregate acquisition budget."""
    body = acquisition.RPM_MAGIC + b"candidate"
    failed = _rpc_response(b"")
    failed.read1.side_effect = [http.client.IncompleteRead(body)]
    successful = _rpc_response(
        body, {"Content-Length": str(len(body))} if advertised_length else {},
    )
    urlopen = Mock(side_effect=[failed, successful])
    monkeypatch.setattr(urllib.request, "urlopen", urlopen)

    with pytest.raises(RuntimeError, match="aggregate download budget"):
        _download(tmp_path, maximum_size=len(body))

    assert urlopen.call_count == RETRIED_ATTEMPTS
    if advertised_length:
        successful.read1.assert_not_called()
    assert not (tmp_path / "jq-1-1.x86_64.rpm").exists()


@pytest.mark.parametrize(("body", "headers", "message"), [
    (b"bad magic", {}, "not an RPM"),
    (b"sh", {}, "too short"),
    (acquisition.RPM_MAGIC, {"Content-Length": "5"}, "does not match Content-Length"),
    (acquisition.RPM_MAGIC, {"Content-Length": "-1"}, "negative Content-Length"),
    (acquisition.RPM_MAGIC, {"Content-Length": "invalid"}, "invalid literal"),
])
def test_download_rpm_does_not_retry_invalid_content(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, retry_clock: Mock,
    body: bytes, headers: dict[str, str], message: str,
) -> None:
    """Metadata/content validation failures must not trigger fresh downloads."""
    urlopen = Mock(return_value=_rpc_response(body, headers))
    monkeypatch.setattr(urllib.request, "urlopen", urlopen)

    with pytest.raises(RuntimeError, match=message):
        _download(tmp_path)

    urlopen.assert_called_once()
    retry_clock.sleep.assert_not_called()
    assert not (tmp_path / "jq-1-1.x86_64.rpm").exists()


@pytest.mark.parametrize(("rpm_limit", "advertised_length"), [
    (True, False), (True, True), (False, False), (False, True),
])
def test_download_rpm_does_not_retry_safety_limits(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, retry_clock: Mock,
    rpm_limit: bool, advertised_length: bool,
) -> None:
    """Both per-file and aggregate limits are terminal with or without headers."""
    body = acquisition.RPM_MAGIC + b"oversized"
    limit = len(body) - 1
    if rpm_limit:
        monkeypatch.setattr(acquisition, "MAX_RPM_SIZE", limit)
    response = _rpc_response(
        body, {"Content-Length": str(len(body))} if advertised_length else {},
    )
    urlopen = Mock(return_value=response)
    monkeypatch.setattr(urllib.request, "urlopen", urlopen)

    with pytest.raises(RuntimeError, match=r"limit|budget"):
        _download(tmp_path, maximum_size=acquisition.MAX_TOTAL_RPM_SIZE if rpm_limit else limit)

    urlopen.assert_called_once()
    retry_clock.sleep.assert_not_called()
    if advertised_length:
        response.read1.assert_not_called()
    assert not (tmp_path / "jq-1-1.x86_64.rpm").exists()


@pytest.mark.parametrize("error", [
    urllib.error.URLError(ssl.SSLCertVerificationError("untrusted certificate")),
    _http_error(403),
    OSError(errno.ENOSPC, "disk full"),
])
def test_download_rpm_does_not_retry_permanent_failures(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, retry_clock: Mock, error: OSError,
) -> None:
    """Permanent transport/local errors leave no file and never sleep."""
    response = _rpc_response(b"")
    response.read1.side_effect = error
    urlopen = Mock(return_value=response)
    monkeypatch.setattr(urllib.request, "urlopen", urlopen)

    with pytest.raises(RuntimeError, match=r"attempt 1/4"):
        _download(tmp_path)

    urlopen.assert_called_once()
    retry_clock.sleep.assert_not_called()
    assert not (tmp_path / "jq-1-1.x86_64.rpm").exists()


def test_download_rpm_exhausted_retries_remove_partial_output(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path,
) -> None:
    """No truncated last attempt may remain after the retry limit."""
    responses = [_rpc_response(b"") for _ in range(acquisition.MAX_REQUEST_ATTEMPTS)]
    for response in responses:
        response.read1.side_effect = [acquisition.RPM_MAGIC, TimeoutError("timed out")]
    urlopen = Mock(side_effect=responses)
    monkeypatch.setattr(urllib.request, "urlopen", urlopen)

    with pytest.raises(RuntimeError, match=r"after 4 attempt.*attempt 4/4"):
        _download(tmp_path)

    assert urlopen.call_count == acquisition.MAX_REQUEST_ATTEMPTS
    assert not (tmp_path / "jq-1-1.x86_64.rpm").exists()


def test_download_rpm_deadline_stops_stream_without_retry(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, retry_clock: Mock,
) -> None:
    """A progressing response does not grant an unbounded operation window."""
    def expire(_size: int) -> bytes:
        retry_clock.monotonic.return_value = acquisition.MAX_OPERATION_SECONDS
        return acquisition.RPM_MAGIC

    response = _rpc_response(b"")
    response.read1.side_effect = expire
    urlopen = Mock(return_value=response)
    monkeypatch.setattr(urllib.request, "urlopen", urlopen)

    with pytest.raises(RuntimeError, match="deadline exceeded"):
        _download(tmp_path)

    urlopen.assert_called_once()
    retry_clock.sleep.assert_not_called()
    assert not (tmp_path / "jq-1-1.x86_64.rpm").exists()


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
def test_run_acquisition_uses_structured_discovery_before_downloading(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, acquisition_args: argparse.Namespace,
    architecture: str, missing_output: bool,
) -> None:
    """Check each architecture and noarch outputs without mixing native RPMs."""
    args = acquisition_args
    args.architecture = architecture
    rpm_path = tmp_path / f"jq-1-1.{architecture}.rpm"
    rpm_path.write_bytes(acquisition.RPM_MAGIC)
    noarch_path = tmp_path / "jq-doc-1-1.noarch.rpm"
    noarch_path.write_bytes(acquisition.RPM_MAGIC)
    task_id = 20 if architecture == "x86_64" else 30
    hub = Mock(spec=acquisition.KojiClient, url=args.koji_hub_url)
    hub.call.side_effect = [
        {
            "id": 10, "method": "build", "state": 2,
            "request": ["source", 13, {"scratch": True}],
        },
        [_arch_task(20, "x86_64"), _arch_task(30, "aarch64")],
        {"rpms": [
            f"tasks/{task_id}/{task_id}/{rpm_path.name}",
            f"tasks/{task_id}/{task_id}/{noarch_path.name}",
        ]},
        {} if missing_output else {
            rpm_path.name: ["DEFAULT"], noarch_path.name: ["DEFAULT"],
        },
    ]
    monkeypatch.setattr(acquisition, "KojiClient", Mock(return_value=hub))
    first_candidate = _candidate(rpm_path, "jq", architecture)
    first_candidate["transferredBytes"] = 10
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
    assert report["acquisition"]["retryPolicy"] == {
        "maximumAttempts": acquisition.MAX_REQUEST_ATTEMPTS,
        "maximumDelaySeconds": acquisition.MAX_RETRY_DELAY_SECONDS,
        "operationDeadlineSeconds": acquisition.MAX_OPERATION_SECONDS,
        "requestTimeoutSeconds": acquisition.REQUEST_TIMEOUT_SECONDS,
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
    assert download.call_args_list[0].kwargs["maximum_size"] == acquisition.MAX_TOTAL_RPM_SIZE
    assert download.call_args.kwargs["maximum_size"] == acquisition.MAX_TOTAL_RPM_SIZE - 10
    assert download.call_args.kwargs["task_id"] == task_id
    assert download.call_args_list[0].kwargs["filename"] == rpm_path.name
    assert download.call_args.kwargs["koji_files_url"] == args.koji_files_url
    route.assert_called_once()


@pytest.mark.parametrize("architecture", ["x86_64", "aarch64"])
@pytest.mark.parametrize("include_noarch", [False, True])
@pytest.mark.parametrize("missing_output", [False, True])
def test_run_acquisition_handles_architecture_restricted_components(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, acquisition_args: argparse.Namespace,
    capsys: pytest.CaptureFixture[str], architecture: str, include_noarch: bool, missing_output: bool,
) -> None:
    """Keep shared outputs and removals without accepting incomplete other-arch data."""
    args = acquisition_args
    args.architecture = architecture
    other_architecture = "aarch64" if architecture == "x86_64" else "x86_64"
    filenames = [f"jq-1-1.{other_architecture}.rpm"]
    if include_noarch:
        filenames.append("jq-doc-1-1.noarch.rpm")
    hub = Mock(spec=acquisition.KojiClient, url=args.koji_hub_url)
    hub.call.side_effect = [
        {
            "id": 10, "method": "build", "state": 2,
            "request": ["source", 13, {"scratch": True}],
        },
        [_arch_task(20, other_architecture)],
        {"rpms": [f"tasks/20/20/{filename}" for filename in filenames]},
        {} if missing_output else {filename: ["DEFAULT"] for filename in filenames},
    ]
    monkeypatch.setattr(acquisition, "KojiClient", Mock(return_value=hub))
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
    hub = Mock(spec=acquisition.KojiClient, url=args.koji_hub_url)
    hub.call.side_effect = [
        {
            "id": 10, "method": "build", "state": 2,
            "request": ["source", 13, {"scratch": True}],
        },
        [_arch_task(20, "noarch")],
        {"rpms": [f"tasks/20/20/{noarch_path.name}"]},
        {noarch_path.name: ["DEFAULT"]},
    ]
    monkeypatch.setattr(acquisition, "KojiClient", Mock(return_value=hub))
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
    hub = Mock(spec=acquisition.KojiClient, url=args.koji_hub_url)
    hub.call.side_effect = [
        {
            "id": 10, "method": "build", "state": 2,
            "request": ["source", 13, {"scratch": True}],
        },
        [_arch_task(20, "x86_64"), _arch_task(35, "noarch")],
        {"rpms": [f"tasks/35/35/{noarch_path.name}"]},
        {noarch_path.name: ["DEFAULT"]},
        {"rpms": [f"tasks/20/20/{filename}" for filename in [native_path.name, noarch_path.name]]},
        {native_path.name: ["DEFAULT"], noarch_path.name: ["DEFAULT"]},
    ]
    monkeypatch.setattr(acquisition, "KojiClient", Mock(return_value=hub))
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
