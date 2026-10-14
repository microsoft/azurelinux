#!/usr/bin/env python3
"""Download candidate RPMs from a completed Control Tower scratch build."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import urllib.parse
from pathlib import Path, PurePosixPath
from typing import Any, TypedDict
from xml.parsers.expat import ExpatError
from xmlrpc.client import Error as XmlRpcError

import client as ct
import koji
import package_build
import requests
from publication_policy import load_publication_policy

DOWNLOAD_CHUNK_SIZE = 1024 * 1024
REQUEST_TIMEOUT_SECONDS = 60
MAX_REQUEST_RETRIES = 3
RETRY_INTERVAL_SECONDS = 2
RPM_MAGIC = b"\xed\xab\xee\xdb"
BUILD_ARCH_REQUEST_ARCH_INDEX = 2
BUILD_REQUEST_OPTIONS_INDEX = 2
RETRYABLE_HTTP_STATUSES = (408, 429, 500, 502, 503, 504)


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
    filename: str
    name: str
    path: str
    repository: str
    sha256: str
    size: int
    taskId: int
    url: str


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


def make_koji_client(url: str, *, insecure: bool) -> koji.ClientSession:
    """Configure the official client for anonymous metadata reads."""
    return koji.ClientSession(
        validate_https_url("koji-hub-url", url),
        opts={
            "anon_retry": True,
            "max_retries": MAX_REQUEST_RETRIES,
            "no_ssl_verify": insecure,
            "offline_retry": False,
            "retry_interval": RETRY_INTERVAL_SECONDS,
            "timeout": REQUEST_TIMEOUT_SECONDS,
        },
    )


def make_download_session(*, insecure: bool) -> requests.Session:
    """Reuse Koji's HTTP retries with explicit artifact TLS verification."""
    session = requests.Session()
    session.verify = not insecure
    session.headers["User-Agent"] = "azurelinux-candidate-rpm-acquisition/1"
    session.headers["Accept-Encoding"] = "identity"
    return koji.request_with_retry(
        retries=MAX_REQUEST_RETRIES,
        backoff_factor=RETRY_INTERVAL_SECONDS,
        status_forcelist=RETRYABLE_HTTP_STATUSES,
        session=session,
    )


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
    return f"{koji.PathInfo(topdir=koji_files_url).task(task_id)}/{quoted_filename}"


def discover_arch_tasks(
    hub: koji.ClientSession, root_task_id: int, architecture: str,
) -> list[ArchitectureTask]:
    """Prefer matching tasks, inspecting other arches for shared noarch outputs."""
    root = hub.getTaskInfo(root_task_id, request=True, strict=True)
    if (
        not isinstance(root, dict)
        or type(root.get("id")) is not int
        or root["id"] != root_task_id
        or root.get("method") != "build"
        or type(root.get("state")) is not int
        or root["state"] != koji.TASK_STATES["CLOSED"]
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
    children = hub.getTaskChildren(root_task_id, request=True, strict=True)
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
        if type(child.get("state")) is not int or child["state"] != koji.TASK_STATES["CLOSED"]:
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


def discover_rpm_outputs(hub: koji.ClientSession, task_id: int, architecture: str) -> list[str]:
    """Cross-check the build result against the complete task output inventory."""
    result = hub.getTaskResult(task_id)
    if not isinstance(result, dict) or not isinstance(result.get("rpms"), list) or not result["rpms"]:
        raise RuntimeError(f"Koji buildArch task {task_id} has no RPM result manifest")
    expected: set[str] = set()
    for path in result["rpms"]:
        if not isinstance(path, str):
            raise TypeError(f"Koji task {task_id} has a malformed RPM result path")
        filename = PurePosixPath(path).name
        _validate_task_output_filename(filename)
        if (
            path != f"{koji.PathInfo().taskrelpath(task_id)}/{filename}"
            or not filename.endswith((f".{architecture}.rpm", ".noarch.rpm"))
            or filename in expected
        ):
            raise RuntimeError(f"Koji task {task_id} has an invalid or duplicate RPM result path: {path!r}")
        expected.add(filename)
    outputs = hub.listTaskOutput(task_id, all_volumes=True, strict=True)
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
    session: requests.Session,
    source_component: str,
    task_id: int,
) -> DownloadedRpm:
    """Stream one RPM with explicit TLS policy and record its content hash."""
    destination.mkdir(parents=True, exist_ok=True)
    output_path = destination / filename
    url = make_task_output_url(koji_files_url, task_id, filename)
    digest = hashlib.sha256()
    size = 0
    prefix = bytearray()
    complete = False
    try:
        with session.get(url, stream=True, timeout=REQUEST_TIMEOUT_SECONDS) as response:
            response.raise_for_status()
            with output_path.open("wb") as output:
                for chunk in response.iter_content(chunk_size=DOWNLOAD_CHUNK_SIZE):
                    if len(prefix) < len(RPM_MAGIC):
                        prefix.extend(chunk[:len(RPM_MAGIC) - len(prefix)])
                    size += len(chunk)
                    digest.update(chunk)
                    output.write(chunk)
            if bytes(prefix) != RPM_MAGIC:
                raise RuntimeError(f"Koji output is not an RPM: {filename}")
            content_length = response.headers.get("Content-Length")
            if content_length is not None and size != int(content_length):
                raise RuntimeError(f"Koji output size does not match Content-Length for {filename}")
        complete = True
    except requests.RequestException as exc:
        raise RuntimeError(f"Failed to download {url}: {exc}") from exc
    finally:
        if not complete:
            output_path.unlink(missing_ok=True)
    architecture = filename.removesuffix(".rpm").rsplit(".", maxsplit=1)[-1]
    return {
        "architecture": architecture,
        "component": source_component,
        "filename": filename,
        "name": "",
        "path": str(output_path),
        "repository": "",
        "sha256": digest.hexdigest(),
        "size": size,
        "taskId": task_id,
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

    hub = make_koji_client(koji_hub_url, insecure=args.insecure_koji_tls)
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
    candidates: list[DownloadedRpm] = []
    with make_download_session(insecure=args.insecure_koji_tls) as download_session:
        for component, task_id, filename in discovered:
            candidates.append(download_rpm(
                destination=args.download_directory,
                filename=filename,
                koji_files_url=koji_files_url,
                source_component=component,
                session=download_session,
                task_id=task_id,
            ))
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
            "kojiClientVersion": koji.__version__,
            "kojiPackageTasks": package_tasks,
            "kojiTlsCertificateVerification": not args.insecure_koji_tls,
            "retryPolicy": {
                "maximumRetries": MAX_REQUEST_RETRIES,
                "requestTimeoutSeconds": REQUEST_TIMEOUT_SECONDS,
                "type": "koji-client-and-http-adapter",
            },
            "type": "control-tower-koji",
        },
        "architecture": args.architecture,
        "candidates": candidates,
        "result": "passed",
        "schemaVersion": 3,
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
    except (
        OSError, RuntimeError, TypeError, ValueError,
        koji.GenericError, requests.RequestException, ExpatError, XmlRpcError,
    ) as exc:
        write_report(
            args.report,
            {
                "error": str(exc),
                "result": "failed",
                "schemaVersion": 3,
            },
        )
        print(f"##vso[task.logissue type=error]{exc}", file=sys.stderr)
        return 1

    write_report(args.report, report)
    print(f"Downloaded and routed {len(report['candidates'])} candidate RPMs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
