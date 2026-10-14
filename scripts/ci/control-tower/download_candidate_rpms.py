#!/usr/bin/env python3
"""Download candidate RPMs from a completed Control Tower scratch build."""

from __future__ import annotations

import argparse
import errno
import hashlib
import http.client
import json
import shutil
import socket
import ssl
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xmlrpc.client
from email.utils import parsedate_to_datetime
from pathlib import Path, PurePosixPath
from random import SystemRandom
from typing import TYPE_CHECKING, Any, TypedDict
from xml.parsers.expat import ExpatError

import client as ct
import package_build
from publication_policy import load_publication_policy

if TYPE_CHECKING:
    from collections.abc import Callable, Iterator

DOWNLOAD_CHUNK_SIZE = 1024 * 1024
REQUEST_TIMEOUT_SECONDS = 60
MAX_OPERATION_SECONDS = 600
MAX_REQUEST_ATTEMPTS = 4
RETRY_BACKOFF_SECONDS = 2
MAX_RETRY_DELAY_SECONDS = 30
RETRY_RANDOM = SystemRandom()
MAX_RPM_COUNT = 10_000
MAX_KOJI_RESPONSE_SIZE = 16 * 1024 * 1024
MAX_RPM_SIZE = 1024 * 1024 * 1024
MAX_TOTAL_RPM_SIZE = 50 * 1024 * 1024 * 1024
RPM_MAGIC = b"\xed\xab\xee\xdb"
KOJI_TASK_CLOSED = 2
BUILD_ARCH_REQUEST_ARCH_INDEX = 2
BUILD_REQUEST_OPTIONS_INDEX = 2
READ_ONLY_KOJI_METHODS = frozenset({
    "getTaskChildren", "getTaskInfo", "getTaskResult", "listTaskOutput",
})
RETRYABLE_HTTP_STATUSES = frozenset({408, 429, 500, 502, 503, 504})
RETRYABLE_NETWORK_ERRNOS = frozenset({
    errno.ECONNABORTED, errno.ECONNREFUSED, errno.ECONNRESET,
    errno.EHOSTUNREACH, errno.ENETUNREACH, errno.EPIPE, errno.ETIMEDOUT,
})


class ArchitectureTask(TypedDict):
    """One completed buildArch task and its requested architecture."""

    architecture: str
    taskId: int


class ComponentTask(TypedDict):
    """One completed component build from the Control Tower job."""

    component: str
    rootTaskId: int


class DownloadedRpm(TypedDict):
    """One downloaded candidate RPM and its acquisition provenance."""

    architecture: str
    component: str
    downloadAttempts: int
    filename: str
    name: str
    path: str
    repository: str
    sha256: str
    size: int
    taskId: int
    transferredBytes: int
    url: str


def _remaining_request_timeout(deadline: float) -> float:
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise TimeoutError("Koji operation deadline exceeded")
    return min(REQUEST_TIMEOUT_SECONDS, remaining)


def _response_chunks(
    response: http.client.HTTPResponse, deadline: float,
) -> Iterator[bytes]:
    while True:
        _remaining_request_timeout(deadline)
        try:
            chunk = response.read1(DOWNLOAD_CHUNK_SIZE)
        except http.client.IncompleteRead as exc:
            if exc.partial:
                yield exc.partial
            raise
        _remaining_request_timeout(deadline)
        if not chunk:
            return
        yield chunk


def _is_retryable_transport_error(error: OSError | http.client.HTTPException) -> bool:
    if isinstance(error, urllib.error.HTTPError):
        return error.code in RETRYABLE_HTTP_STATUSES
    if isinstance(error, urllib.error.URLError):
        reason = error.reason
        return (
            isinstance(reason, (OSError, http.client.HTTPException))
            and _is_retryable_transport_error(reason)
        )
    if isinstance(error, ssl.SSLError):
        return False
    if isinstance(error, socket.gaierror):
        return error.errno == socket.EAI_AGAIN
    if isinstance(error, (TimeoutError, ConnectionError, http.client.IncompleteRead)):
        return True
    return isinstance(error, OSError) and error.errno in RETRYABLE_NETWORK_ERRNOS


def _retry_after_seconds(value: str | None) -> float | None:
    if value is None:
        return None
    value = value.strip()
    if value.isascii() and value.isdigit():
        return float(value)
    try:
        when = parsedate_to_datetime(value)
        if when.tzinfo is not None:
            return max(0.0, when.timestamp() - time.time())
    except (OverflowError, TypeError, ValueError):
        pass
    print("Ignoring malformed Koji Retry-After header; using bounded backoff.", file=sys.stderr)
    return None


def _retry_koji_read[T](operation: Callable[[float], T], *, label: str) -> T:
    deadline = time.monotonic() + MAX_OPERATION_SECONDS
    for attempt in range(1, MAX_REQUEST_ATTEMPTS + 1):
        try:
            _remaining_request_timeout(deadline)
            return operation(deadline)
        except (OSError, http.client.HTTPException) as exc:
            retry_after = None
            if isinstance(exc, urllib.error.HTTPError):
                if exc.headers is not None:
                    retry_after = exc.headers.get("Retry-After")
                exc.close()
            remaining = deadline - time.monotonic()
            if (
                not _is_retryable_transport_error(exc)
                or attempt == MAX_REQUEST_ATTEMPTS
                or remaining <= 0
            ):
                raise RuntimeError(
                    f"{label} failed on attempt {attempt}/{MAX_REQUEST_ATTEMPTS} "
                    f"(remaining retry window: {max(0.0, remaining):.1f}s): {exc}"
                ) from exc
            delay = min(
                MAX_RETRY_DELAY_SECONDS,
                RETRY_BACKOFF_SECONDS * 2 ** (attempt - 1) + RETRY_RANDOM.uniform(0.0, 1.0),
            )
            requested_delay = _retry_after_seconds(retry_after)
            if requested_delay is not None:
                if requested_delay > MAX_RETRY_DELAY_SECONDS:
                    raise RuntimeError(
                        f"{label} failed on attempt {attempt}/{MAX_REQUEST_ATTEMPTS}: "
                        f"Retry-After exceeds the {MAX_RETRY_DELAY_SECONDS}s retry-delay limit; {exc}"
                    ) from exc
                delay = max(delay, requested_delay)
            if delay >= remaining:
                raise RuntimeError(
                    f"{label} exhausted its retry window after attempt "
                    f"{attempt}/{MAX_REQUEST_ATTEMPTS}: {exc}"
                ) from exc
            print(
                f"{label}: attempt {attempt}/{MAX_REQUEST_ATTEMPTS} failed: {exc}; "
                f"retrying in {delay:.1f}s.",
                file=sys.stderr,
            )
            time.sleep(delay)
        except (RuntimeError, ValueError) as exc:
            raise RuntimeError(
                f"{label} failed on attempt {attempt}/{MAX_REQUEST_ATTEMPTS}: {exc}"
            ) from exc
    raise AssertionError("Unreachable Koji retry state")


class KojiClient:
    """Read bounded XML-RPC metadata without a separate Koji dependency."""

    def __init__(self, url: str, ssl_context: ssl.SSLContext) -> None:
        """Use an explicitly configured HTTPS hub and TLS policy."""
        self.url = validate_https_url("koji-hub-url", url)
        self.ssl_context = ssl_context

    def call(self, method: str, args: tuple[int | bool, ...]) -> object:
        """Read one response, surfacing transport, protocol, and hub faults."""
        if method not in READ_ONLY_KOJI_METHODS:
            raise ValueError(f"Unsupported Koji metadata method: {method}")
        request = urllib.request.Request(
            self.url,
            data=xmlrpc.client.dumps(args, methodname=method).encode("utf-8"),
            headers={
                "Content-Type": "text/xml",
                "User-Agent": "azurelinux-candidate-rpm-acquisition/1",
            },
        )
        label = f"Koji {method}{args!r} at {self.url}"
        try:
            document = _retry_koji_read(
                lambda deadline: self._read_response(request, deadline),
                label=label,
            )
            values, _ = xmlrpc.client.loads(document)
            if len(values) != 1:
                raise RuntimeError(
                    f"Koji {method}{args!r} response must contain exactly one value at {self.url}"
                )
        except (OSError, ValueError, http.client.HTTPException, xmlrpc.client.Error, ExpatError) as exc:
            raise RuntimeError(
                f"Koji {method}{args!r} failed at {self.url}: {exc}"
            ) from exc
        return values[0]

    def _read_response(self, request: urllib.request.Request, deadline: float) -> bytes:
        with urllib.request.urlopen(
            request,
            context=self.ssl_context,
            timeout=_remaining_request_timeout(deadline),
        ) as response:
            content_length = response.headers.get("Content-Length")
            expected_size = int(content_length) if content_length is not None else None
            if expected_size is not None and expected_size < 0:
                raise ValueError("Koji XML-RPC response has negative Content-Length")
            if expected_size is not None and expected_size > MAX_KOJI_RESPONSE_SIZE:
                raise RuntimeError(f"Koji {request.full_url} response exceeds the size limit")
            document = bytearray()
            for chunk in _response_chunks(response, deadline):
                if len(document) + len(chunk) > MAX_KOJI_RESPONSE_SIZE:
                    raise RuntimeError(f"Koji {request.full_url} response exceeds the size limit")
                document.extend(chunk)
            if expected_size is not None and len(document) != expected_size:
                raise RuntimeError("Koji XML-RPC response does not match Content-Length")
        return bytes(document)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--api-audience", required=True)
    parser.add_argument("--api-base-url", required=True)
    parser.add_argument("--architecture", default="x86_64")
    parser.add_argument("--candidate-base-dir", required=True, type=Path)
    parser.add_argument("--candidate-sdk-dir", required=True, type=Path)
    parser.add_argument("--download-directory", required=True, type=Path)
    parser.add_argument("--expected-components-file", required=True, type=Path)
    parser.add_argument(
        "--insecure-koji-tls",
        action="store_true",
        help="Disable Koji TLS certificate and hostname verification.",
    )
    parser.add_argument("--job-id-file", required=True, type=Path)
    parser.add_argument("--koji-files-url", required=True)
    parser.add_argument("--koji-hub-url", required=True)
    parser.add_argument("--publish-policy", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument("--replaced-components-file", type=Path)
    return parser.parse_args()


def validate_https_url(name: str, value: str) -> str:
    """Validate a credential-free HTTPS endpoint URL."""
    parsed = urllib.parse.urlsplit(value)
    if (
        parsed.scheme != "https"
        or not parsed.netloc
        or parsed.username is not None
        or parsed.password is not None
        or parsed.query
        or parsed.fragment
    ):
        raise ValueError(f"{name} must be an HTTPS URL without credentials, query, or fragment")
    return value.rstrip("/")


def make_koji_ssl_context(insecure: bool) -> ssl.SSLContext:
    """Create the SSL context used for Koji hub and file requests."""
    context = ssl.create_default_context()
    if insecure:
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
    return context


def read_job_id(path: Path) -> str:
    """Read a nonempty Control Tower job ID."""
    job_id = path.read_text(encoding="utf-8").strip()
    if not job_id:
        raise RuntimeError("Control Tower job ID is empty")
    return job_id


def _validate_task_output_filename(filename: str) -> None:
    path = PurePosixPath(filename)
    if (
        path.name != filename
        or filename in {".", ".."}
        or "\\" in filename
        or not filename.isprintable()
    ):
        raise ValueError(f"Unsafe Koji task output filename: {filename!r}")


def make_task_output_url(koji_files_url: str, task_id: int, filename: str) -> str:
    """Construct a Koji work/tasks URL without permitting path traversal."""
    _validate_task_output_filename(filename)
    quoted_filename = urllib.parse.quote(filename, safe="")
    return f"{koji_files_url}/work/tasks/{task_id % 10000}/{task_id}/{quoted_filename}"


def _validate_rpm_size(size: int, filename: str) -> None:
    if size > MAX_RPM_SIZE:
        raise RuntimeError(f"Koji RPM exceeds the {MAX_RPM_SIZE}-byte safety limit: {filename}")


def _validate_rpm_magic(chunk: bytes, filename: str) -> None:
    if not chunk.startswith(RPM_MAGIC):
        raise RuntimeError(f"Koji output is not an RPM: {filename}")


def _validate_download_budget(size: int, maximum_size: int, filename: str) -> None:
    if size > maximum_size:
        raise RuntimeError(
            f"Koji RPM exceeds the remaining aggregate download budget: {filename}"
        )


def discover_arch_tasks(
    hub: KojiClient, root_task_id: int, architecture: str,
) -> list[ArchitectureTask]:
    """Prefer matching tasks, inspecting other arches for shared noarch outputs."""
    root = hub.call("getTaskInfo", (root_task_id, True, True))
    if (
        not isinstance(root, dict)
        or type(root.get("id")) is not int
        or root["id"] != root_task_id
        or root.get("method") != "build"
        or type(root.get("state")) is not int
        or root["state"] != KOJI_TASK_CLOSED
    ):
        raise RuntimeError(f"Koji root task {root_task_id} is not a closed build")
    request = root.get("request")
    if (
        not isinstance(request, list)
        or len(request) not in {BUILD_REQUEST_OPTIONS_INDEX, BUILD_REQUEST_OPTIONS_INDEX + 1}
    ):
        raise RuntimeError(f"Koji root task {root_task_id} has a malformed build request")
    options = request[BUILD_REQUEST_OPTIONS_INDEX] if len(request) > BUILD_REQUEST_OPTIONS_INDEX else None
    if options is not None and not isinstance(options, dict):
        raise RuntimeError(f"Koji root task {root_task_id} has malformed build options")
    override = options.get("arch_override") if options is not None else None
    if override is not None and not isinstance(override, str):
        raise RuntimeError(f"Koji root task {root_task_id} has a malformed architecture override")
    if override and architecture not in override.split() and set(override.split()) != {"noarch"}:
        raise RuntimeError(
            f"Koji root task {root_task_id} has an architecture override excluding {architecture}"
        )
    children = hub.call("getTaskChildren", (root_task_id, True, True))
    if not isinstance(children, list):
        raise TypeError(f"Koji task {root_task_id} has malformed child metadata")
    selected: dict[str, int] = {}
    seen: set[int] = set()
    for child in children:
        if (
            not isinstance(child, dict)
            or type(child.get("id")) is not int
            or child["id"] <= 0
            or child["id"] in seen
            or type(child.get("parent")) is not int
            or child["parent"] != root_task_id
            or not isinstance(child.get("method"), str)
            or not child["method"]
        ):
            raise RuntimeError(f"Koji task {root_task_id} has malformed or duplicate child metadata")
        task_id = child["id"]
        seen.add(task_id)
        if child["method"] != "buildArch":
            continue
        request = child.get("request")
        if (
            not isinstance(request, list)
            or len(request) <= BUILD_ARCH_REQUEST_ARCH_INDEX
            or not isinstance(request[BUILD_ARCH_REQUEST_ARCH_INDEX], str)
            or not request[BUILD_ARCH_REQUEST_ARCH_INDEX]
        ):
            raise RuntimeError(f"Koji buildArch task {task_id} has a malformed request")
        requested_arch = request[BUILD_ARCH_REQUEST_ARCH_INDEX]
        if type(child.get("state")) is not int or child["state"] != KOJI_TASK_CLOSED:
            raise RuntimeError(f"Koji buildArch task {task_id} for {requested_arch} is not closed")
        if requested_arch in selected:
            raise RuntimeError(
                f"Koji task {root_task_id} has ambiguous buildArch retries for "
                f"{requested_arch}: {selected[requested_arch]}, {task_id}"
            )
        selected[requested_arch] = task_id
    if not selected:
        raise RuntimeError(f"Koji task {root_task_id} exposes no buildArch tasks")
    compatible = {arch: task_id for arch, task_id in selected.items() if arch in {architecture, "noarch"}}
    return [
        {"architecture": arch, "taskId": task_id}
        for arch, task_id in sorted((compatible or selected).items())
    ]


def discover_rpm_outputs(hub: KojiClient, task_id: int, architecture: str) -> list[str]:
    """Cross-check the build result against the complete task output inventory."""
    result = hub.call("getTaskResult", (task_id,))
    if not isinstance(result, dict) or not isinstance(result.get("rpms"), list) or not result["rpms"]:
        raise RuntimeError(f"Koji buildArch task {task_id} has no RPM result manifest")
    expected: set[str] = set()
    for path in result["rpms"]:
        if not isinstance(path, str):
            raise TypeError(f"Koji task {task_id} has a malformed RPM result path")
        filename = PurePosixPath(path).name
        _validate_task_output_filename(filename)
        if (
            path != f"tasks/{task_id % 10000}/{task_id}/{filename}"
            or not filename.endswith((f".{architecture}.rpm", ".noarch.rpm"))
            or filename in expected
        ):
            raise RuntimeError(f"Koji task {task_id} has an invalid or duplicate RPM result path: {path!r}")
        expected.add(filename)
    outputs = hub.call("listTaskOutput", (task_id, False, True, True))
    if not isinstance(outputs, dict) or any(not isinstance(name, str) for name in outputs):
        raise RuntimeError(f"Koji task {task_id} has a malformed output inventory")
    listed: set[str] = set()
    for filename, volumes in outputs.items():
        if not filename.endswith(".rpm") or filename.endswith((".src.rpm", ".nosrc.rpm")):
            continue
        _validate_task_output_filename(filename)
        if volumes != ["DEFAULT"]:
            raise RuntimeError(
                f"Koji task {task_id} output {filename!r} has unsupported or ambiguous volumes: {volumes!r}"
            )
        listed.add(filename)
    if expected != listed:
        raise RuntimeError(
            f"Koji task {task_id} RPM output inventory disagrees with its result manifest: "
            f"missing={sorted(expected - listed)}, unexpected={sorted(listed - expected)}"
        )
    filenames = sorted(
        filename for filename in expected
        if "-debuginfo-" not in filename and "-debugsource-" not in filename
    )
    if not filenames:
        raise RuntimeError(f"Koji task {task_id} exposes no publishable binary RPMs")
    return filenames


def select_completed_component_tasks(
    results: dict[str, Any],
    expected_components: set[str],
) -> list[ComponentTask]:
    """Return completed tasks and require every requested component."""
    build_tasks = results.get("buildTasks")
    if not isinstance(build_tasks, list):
        raise RuntimeError(  # noqa: TRY004 - malformed remote data is operational
            "Control Tower Koji package results do not contain a buildTasks array"
        )

    completed: set[tuple[str, int]] = set()
    statuses: dict[str, set[str]] = {}
    for build_task in build_tasks:
        if not isinstance(build_task, dict):
            continue
        koji_info = build_task.get("kojiInfo")
        if not isinstance(koji_info, dict):
            continue
        component = koji_info.get("componentName")
        task_id = koji_info.get("kojiTaskNumber")
        if not isinstance(component, str) or not component or not isinstance(task_id, int):
            raise RuntimeError("Control Tower build task contains malformed Koji component information")
        status = str(build_task.get("taskStatus", "")).lower()
        koji_status = str(koji_info.get("kojiTaskStatus", "")).lower()
        statuses.setdefault(component, set()).add(status or "missing")
        if koji_status and koji_status not in {"completed", "succeeded", "closed"}:
            statuses[component].add(f"koji:{koji_status}")
            continue
        if status not in {"completed", "succeeded"}:
            continue
        completed.add((component, task_id))

    if not completed:
        raise RuntimeError("Control Tower job contains no completed Koji package tasks")
    completed_components = {component for component, _ in completed}
    missing = expected_components - completed_components
    if missing:
        details = ", ".join(
            f"{component} ({'/'.join(sorted(statuses.get(component, {'absent'})))})"
            for component in sorted(missing)
        )
        raise RuntimeError(
            f"Control Tower job produced no completed Koji task for: {details}"
        )
    for component in sorted(completed_components):
        task_ids = sorted(task_id for name, task_id in completed if name == component)
        if len(task_ids) > 1:
            raise RuntimeError(
                f"Control Tower component {component} has multiple successful Koji tasks: {task_ids}"
            )
    return [
        {"component": component, "rootTaskId": task_id}
        for component, task_id in sorted(completed)
    ]


def download_rpm(
    *,
    destination: Path,
    filename: str,
    koji_files_url: str,
    ssl_context: ssl.SSLContext,
    source_component: str,
    task_id: int,
    maximum_size: int = MAX_RPM_SIZE,
) -> DownloadedRpm:
    """Download one bounded Koji RPM and return its manifest entry."""
    destination.mkdir(parents=True, exist_ok=True)
    output_path = destination / filename
    url = make_task_output_url(koji_files_url, task_id, filename)
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "azurelinux-candidate-rpm-acquisition/1"},
    )
    transferred_bytes = 0
    attempts = 0

    def attempt_download(deadline: float) -> tuple[int, str]:
        nonlocal transferred_bytes, attempts
        attempts += 1
        digest = hashlib.sha256()
        size = 0
        prefix = bytearray()
        complete = False
        try:
            with (
                urllib.request.urlopen(
                    request,
                    context=ssl_context,
                    timeout=_remaining_request_timeout(deadline),
                ) as response,
                output_path.open("wb") as output,
            ):
                content_length = response.headers.get("Content-Length")
                expected_size: int | None = None
                if content_length is not None:
                    expected_size = int(content_length)
                    if expected_size < 0:
                        raise ValueError(f"Koji output has negative Content-Length: {filename}")
                    _validate_rpm_size(expected_size, filename)
                    _validate_download_budget(expected_size, maximum_size - transferred_bytes, filename)
                for chunk in _response_chunks(response, deadline):
                    transferred_bytes += len(chunk)
                    size += len(chunk)
                    _validate_rpm_size(size, filename)
                    _validate_download_budget(transferred_bytes, maximum_size, filename)
                    if len(prefix) < len(RPM_MAGIC):
                        prefix.extend(chunk[:len(RPM_MAGIC) - len(prefix)])
                        if len(prefix) == len(RPM_MAGIC):
                            _validate_rpm_magic(bytes(prefix), filename)
                    digest.update(chunk)
                    output.write(chunk)
            if size < len(RPM_MAGIC):
                raise RuntimeError(f"Koji output is too short to be an RPM: {filename}")
            if expected_size is not None and size != expected_size:
                raise RuntimeError(
                    f"Koji output size does not match Content-Length for {filename}: "
                    f"expected {expected_size}, received {size}"
                )
            complete = True
        finally:
            if not complete:
                output_path.unlink(missing_ok=True)
        return size, digest.hexdigest()

    try:
        size, sha256 = _retry_koji_read(attempt_download, label=f"Download {url}")
    except (RuntimeError, ValueError) as exc:
        raise RuntimeError(f"Failed to download {url} after {attempts} attempt(s): {exc}") from exc
    architecture = filename.removesuffix(".rpm").rsplit(".", maxsplit=1)[-1]
    return {
        "architecture": architecture,
        "component": source_component,
        "downloadAttempts": attempts,
        "filename": filename,
        "name": "",
        "path": str(output_path),
        "repository": "",
        "sha256": sha256,
        "size": size,
        "taskId": task_id,
        "transferredBytes": transferred_bytes,
        "url": url,
    }


def query_package_name(rpm_path: Path) -> str:
    """Read one binary package name from an RPM header."""
    result = subprocess.run(
        ["rpm", "-qp", "--qf", "%{NAME}\\n", str(rpm_path)],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Failed to query RPM header for {rpm_path}: {result.stdout.strip()}")
    names = {line.strip() for line in result.stdout.splitlines() if line.strip()}
    if len(names) != 1:
        raise RuntimeError(f"Candidate RPM header must expose exactly one package name: {rpm_path}")
    return names.pop()


def candidate_repository(
    component: str,
    package_name: str,
    base_components: set[str],
    sdk_exceptions: set[str],
) -> str:
    """Return the candidate repository implied by publication policy."""
    if component in base_components and package_name not in sdk_exceptions:
        return "candidate-base"
    return "candidate-sdk"


def require_empty_directory(path: Path) -> None:
    """Create a candidate directory or require it to be empty."""
    path.mkdir(parents=True, exist_ok=True)
    if any(path.iterdir()):
        raise RuntimeError(f"Candidate RPM directory must be empty: {path}")


def route_candidates(
    *,
    base_directory: Path,
    candidates: list[DownloadedRpm],
    publish_policy: Path,
    report_path: Path,
    sdk_directory: Path,
) -> None:
    """Apply publication policy and move downloaded RPMs into channel directories."""
    if base_directory.resolve() == sdk_directory.resolve():
        raise RuntimeError("Candidate base and SDK directories must be different")
    policy = load_publication_policy(publish_policy)
    require_empty_directory(base_directory)
    require_empty_directory(sdk_directory)
    package_names: set[str] = set()
    for candidate in candidates:
        source_path = Path(candidate["path"])
        package_name = query_package_name(source_path)
        if package_name in package_names:
            raise RuntimeError(f"Completed Koji tasks produced duplicate package name: {package_name}")
        package_names.add(package_name)
        repository = candidate_repository(
            candidate["component"],
            package_name,
            set(policy.base_components),
            set(policy.sdk_exceptions),
        )
        destination_directory = (
            base_directory if repository == "candidate-base" else sdk_directory
        )
        destination_path = destination_directory / candidate["filename"]
        shutil.move(source_path, destination_path)
        candidate["name"] = package_name
        candidate["repository"] = repository
        try:
            candidate["path"] = str(destination_path.relative_to(report_path.parent))
        except ValueError:
            candidate["path"] = str(destination_path.resolve())


def run_acquisition(args: argparse.Namespace) -> dict[str, Any]:
    """Discover, download, and route every binary RPM from the completed build."""
    api_base_url = validate_https_url("api-base-url", args.api_base_url)
    koji_files_url = validate_https_url("koji-files-url", args.koji_files_url)
    koji_hub_url = validate_https_url("koji-hub-url", args.koji_hub_url)
    job_id = read_job_id(args.job_id_file)
    expected_components = set(package_build.load_component_names(args.expected_components_file))

    credential = ct.make_credential()
    token_holder = ct.TokenHolder(token=ct.get_token(credential, args.api_audience))
    with ct.make_session() as session:
        results = ct.get_koji_package_results(
            session,
            api_base_url,
            credential,
            args.api_audience,
            token_holder,
            job_id,
        )
    component_tasks = select_completed_component_tasks(results, expected_components)
    if args.replaced_components_file is not None:
        replaced_components = set(
            package_build.load_component_names(args.replaced_components_file)
        )
        replaced_components.update(task["component"] for task in component_tasks)
        args.replaced_components_file.write_text(
            json.dumps(sorted(replaced_components), indent=2) + "\n", encoding="utf-8"
        )

    koji_context = make_koji_ssl_context(args.insecure_koji_tls)
    hub = KojiClient(koji_hub_url, koji_context)
    discovered: list[tuple[str, int, str]] = []
    package_tasks: list[dict[str, Any]] = []
    for component_task in component_tasks:
        component = component_task["component"]
        root_task_id = component_task["rootTaskId"]
        arch_tasks = discover_arch_tasks(hub, root_task_id, args.architecture)
        component_outputs: dict[str, int] = {}
        for arch_task in arch_tasks:
            task_id = arch_task["taskId"]
            filenames = discover_rpm_outputs(hub, task_id, arch_task["architecture"])
            for filename in filenames:
                if not filename.endswith((f".{args.architecture}.rpm", ".noarch.rpm")):
                    continue
                if filename in component_outputs:
                    if not filename.endswith(".noarch.rpm"):
                        raise RuntimeError(f"Koji task {root_task_id} has duplicate RPM output: {filename}")
                    # A closed Koji build has already compared duplicate noarch outputs.
                    continue
                component_outputs[filename] = task_id
        has_matching_task = any(
            task["architecture"] in {args.architecture, "noarch"} for task in arch_tasks
        )
        if not has_matching_task:
            print(
                f"Koji component {component} root task {root_task_id} has no {args.architecture} "
                f"buildArch task; selecting only its {len(component_outputs)} noarch output(s). "
                "Former outputs remain excluded from this architecture's baseline.",
                file=sys.stderr,
            )
        discovered.extend(
            (component, task_id, filename) for filename, task_id in sorted(component_outputs.items())
        )
        package_tasks.append(
            {
                "architectureTaskIds": sorted(task["taskId"] for task in arch_tasks),
                "architectureTasks": arch_tasks,
                "component": component,
                "hasMatchingArchitectureTask": has_matching_task,
                "rootTaskId": root_task_id,
            }
        )

    filenames = [filename for _, _, filename in discovered]
    if len(filenames) != len(set(filenames)):
        raise RuntimeError("Completed Koji package tasks expose duplicate RPM filenames")
    if len(filenames) > MAX_RPM_COUNT:
        raise RuntimeError(
            f"Completed Koji tasks expose {len(filenames)} RPMs, exceeding the "
            f"{MAX_RPM_COUNT}-file safety limit"
        )

    candidates: list[DownloadedRpm] = []
    remaining_bytes = MAX_TOTAL_RPM_SIZE
    for component, task_id, filename in discovered:
        candidate = download_rpm(
            destination=args.download_directory,
            filename=filename,
            koji_files_url=koji_files_url,
            maximum_size=remaining_bytes,
            source_component=component,
            ssl_context=koji_context,
            task_id=task_id,
        )
        candidates.append(candidate)
        remaining_bytes -= candidate["transferredBytes"]
    route_candidates(
        base_directory=args.candidate_base_dir,
        candidates=candidates,
        publish_policy=args.publish_policy,
        report_path=args.report,
        sdk_directory=args.candidate_sdk_dir,
    )

    return {
        "acquisition": {
            "controlTowerJobId": job_id,
            "expectedComponents": sorted(expected_components),
            "kojiDiscovery": "xmlrpc-result-manifest-and-output-inventory",
            "kojiHubUrl": koji_hub_url,
            "kojiPackageTasks": package_tasks,
            "kojiTlsCertificateVerification": not args.insecure_koji_tls,
            "retryPolicy": {
                "maximumAttempts": MAX_REQUEST_ATTEMPTS,
                "maximumDelaySeconds": MAX_RETRY_DELAY_SECONDS,
                "operationDeadlineSeconds": MAX_OPERATION_SECONDS,
                "requestTimeoutSeconds": REQUEST_TIMEOUT_SECONDS,
            },
            "safetyLimits": {
                "maximumRpmBytes": MAX_RPM_SIZE,
                "maximumRpmCount": MAX_RPM_COUNT,
                "maximumTotalRpmBytes": MAX_TOTAL_RPM_SIZE,
            },
            "type": "control-tower-koji",
        },
        "architecture": args.architecture,
        "candidates": candidates,
        "result": "passed",
        "schemaVersion": 2,
    }


def write_report(path: Path, report: dict[str, Any]) -> None:
    """Write a stable candidate acquisition report."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    """Download and route candidates, preserving acquisition provenance."""
    args = _parse_args()
    if args.insecure_koji_tls:
        print(
            "##vso[task.logissue type=warning]"
            "Koji TLS certificate and hostname verification are disabled; "
            "Koji connections are not authenticated.",
            file=sys.stderr,
        )
    try:
        report = run_acquisition(args)
    except (OSError, RuntimeError, TypeError, ValueError) as exc:
        write_report(
            args.report,
            {
                "error": str(exc),
                "result": "failed",
                "schemaVersion": 2,
            },
        )
        print(f"##vso[task.logissue type=error]{exc}", file=sys.stderr)
        return 1

    write_report(args.report, report)
    print(f"Downloaded and routed {len(report['candidates'])} candidate RPMs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
