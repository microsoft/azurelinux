#!/usr/bin/env python3
"""Download candidate RPMs from a completed Control Tower scratch build."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import ssl
import subprocess
import sys
import tomllib
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from typing import Any, TypedDict

import client as ct

DOWNLOAD_CHUNK_SIZE = 1024 * 1024
DOWNLOAD_TIMEOUT_SECONDS = 300
MAX_TASK_PAGE_SIZE = 16 * 1024 * 1024
MAX_RPM_SIZE = 1024 * 1024 * 1024
RPM_MAGIC = b"\xed\xab\xee\xdb"


class Link(TypedDict):
    """One anchor parsed from a Koji task page."""

    href: str
    text: str


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


class TaskPageParser(HTMLParser):
    """Collect links and their visible text from a Koji task page."""

    def __init__(self) -> None:
        """Initialize link collection state."""
        super().__init__(convert_charrefs=True)
        self.links: list[Link] = []
        self._href: str | None = None
        self._text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        """Start collecting one anchor."""
        if tag != "a" or self._href is not None:
            return
        href = dict(attrs).get("href")
        if href is not None:
            self._href = href
            self._text = []

    def handle_data(self, data: str) -> None:
        """Collect visible text inside an anchor."""
        if self._href is not None:
            self._text.append(data)

    def handle_endtag(self, tag: str) -> None:
        """Finish collecting one anchor."""
        if tag != "a" or self._href is None:
            return
        self.links.append({"href": self._href, "text": "".join(self._text).strip()})
        self._href = None
        self._text = []


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--api-audience", required=True)
    parser.add_argument("--api-base-url", required=True)
    parser.add_argument("--architecture", default="x86_64")
    parser.add_argument("--candidate-base-dir", required=True, type=Path)
    parser.add_argument("--candidate-sdk-dir", required=True, type=Path)
    parser.add_argument("--download-directory", required=True, type=Path)
    parser.add_argument(
        "--insecure-koji-tls",
        action="store_true",
        help="Disable Koji TLS certificate and hostname verification.",
    )
    parser.add_argument("--job-id-file", required=True, type=Path)
    parser.add_argument("--koji-files-url", required=True)
    parser.add_argument("--koji-web-url", required=True)
    parser.add_argument("--publish-policy", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
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
    """Create the SSL context used for Koji web and file requests."""
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


def make_task_output_url(koji_files_url: str, task_id: int, filename: str) -> str:
    """Construct a Koji work/tasks URL without permitting path traversal."""
    path = PurePosixPath(filename)
    if path.name != filename or filename in {".", ".."}:
        raise ValueError(f"Unsafe Koji task output filename: {filename!r}")
    quoted_filename = urllib.parse.quote(filename, safe="")
    return f"{koji_files_url}/work/tasks/{task_id % 10000}/{task_id}/{quoted_filename}"


def _validate_rpm_size(size: int, filename: str) -> None:
    if size > MAX_RPM_SIZE:
        raise RuntimeError(f"Koji RPM exceeds the {MAX_RPM_SIZE}-byte safety limit: {filename}")


def _validate_rpm_magic(chunk: bytes, filename: str) -> None:
    if not chunk.startswith(RPM_MAGIC):
        raise RuntimeError(f"Koji output is not an RPM: {filename}")


def fetch_bytes(url: str, ssl_context: ssl.SSLContext) -> bytes:
    """Fetch one HTTPS resource."""
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "azurelinux-candidate-rpm-acquisition/1"},
    )
    try:
        with urllib.request.urlopen(
            request,
            context=ssl_context,
            timeout=DOWNLOAD_TIMEOUT_SECONDS,
        ) as response:
            content_length = response.headers.get("Content-Length")
            if content_length is not None and int(content_length) > MAX_TASK_PAGE_SIZE:
                raise RuntimeError(f"Koji task page exceeds the size limit: {url}")
            document = response.read(MAX_TASK_PAGE_SIZE + 1)
            if len(document) > MAX_TASK_PAGE_SIZE:
                raise RuntimeError(f"Koji task page exceeds the size limit: {url}")
            return document
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Request failed for {url}: {exc.reason}") from exc


def parse_links(document: bytes) -> list[Link]:
    """Parse links from one UTF-8 Koji task page."""
    parser = TaskPageParser()
    parser.feed(document.decode("utf-8"))
    parser.close()
    return parser.links


def discover_arch_task_ids(document: bytes, architecture: str) -> list[int]:
    """Return buildArch task IDs for the requested architecture."""
    task_ids: set[int] = set()
    for link in parse_links(document):
        if not link["text"].startswith("buildArch") or not link["text"].endswith(
            f", {architecture})"
        ):
            continue
        parsed = urllib.parse.urlsplit(link["href"])
        query = urllib.parse.parse_qs(parsed.query)
        raw_ids = query.get("taskID", [])
        if len(raw_ids) == 1 and raw_ids[0].isdigit():
            task_ids.add(int(raw_ids[0]))
    if not task_ids:
        raise RuntimeError(f"Koji task page exposes no buildArch task for {architecture}")
    return sorted(task_ids)


def discover_rpm_outputs(document: bytes, task_id: int, architecture: str) -> list[str]:
    """Return publishable binary RPM filenames linked by a buildArch task."""
    filenames: set[str] = set()
    accepted_suffixes = (f".{architecture}.rpm", ".noarch.rpm")
    for link in parse_links(document):
        parsed = urllib.parse.urlsplit(link["href"])
        path = urllib.parse.unquote(parsed.path)
        filename = Path(path).name
        if (
            "/kojifiles/work/tasks/" not in path
            or not filename.endswith(accepted_suffixes)
            or filename.endswith(".src.rpm")
            or "-debuginfo-" in filename
            or "-debugsource-" in filename
        ):
            continue
        parts = path.split("/")
        try:
            linked_task_id = int(parts[parts.index("tasks") + 2])
        except (ValueError, IndexError):
            continue
        if linked_task_id == task_id:
            filenames.add(filename)
    return sorted(filenames)


def select_completed_component_tasks(results: dict[str, Any]) -> list[ComponentTask]:
    """Return every unique completed Koji package task in a Control Tower job."""
    build_tasks = results.get("buildTasks")
    if not isinstance(build_tasks, list):
        raise RuntimeError(  # noqa: TRY004 - malformed remote data is operational
            "Control Tower Koji package results do not contain a buildTasks array"
        )

    completed: set[tuple[str, int]] = set()
    for build_task in build_tasks:
        if not isinstance(build_task, dict):
            continue
        koji_info = build_task.get("kojiInfo")
        if not isinstance(koji_info, dict):
            continue
        if str(build_task.get("taskStatus", "")).lower() not in {"completed", "succeeded"}:
            continue
        component = koji_info.get("componentName")
        task_id = koji_info.get("kojiTaskNumber")
        if not isinstance(component, str) or not component or not isinstance(task_id, int):
            raise RuntimeError("Control Tower build task contains malformed Koji component information")
        completed.add((component, task_id))

    if not completed:
        raise RuntimeError("Control Tower job contains no completed Koji package tasks")
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
) -> DownloadedRpm:
    """Download one bounded Koji RPM and return its manifest entry."""
    destination.mkdir(parents=True, exist_ok=True)
    output_path = destination / filename
    url = make_task_output_url(koji_files_url, task_id, filename)
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "azurelinux-candidate-rpm-acquisition/1"},
    )
    digest = hashlib.sha256()
    size = 0
    try:
        with (
            urllib.request.urlopen(
                request,
                context=ssl_context,
                timeout=DOWNLOAD_TIMEOUT_SECONDS,
            ) as response,
            output_path.open("wb") as output,
        ):
            content_length = response.headers.get("Content-Length")
            if content_length is not None:
                _validate_rpm_size(int(content_length), filename)
            first_chunk = True
            while chunk := response.read(DOWNLOAD_CHUNK_SIZE):
                if first_chunk:
                    _validate_rpm_magic(chunk, filename)
                first_chunk = False
                size += len(chunk)
                _validate_rpm_size(size, filename)
                digest.update(chunk)
                output.write(chunk)
    except (OSError, RuntimeError, urllib.error.URLError, ValueError) as exc:
        output_path.unlink(missing_ok=True)
        raise RuntimeError(f"Failed to download {url}: {exc}") from exc

    if size < len(RPM_MAGIC):
        output_path.unlink(missing_ok=True)
        raise RuntimeError(f"Koji output is too short to be an RPM: {filename}")
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


def load_publish_policy(path: Path) -> tuple[set[str], set[str]]:
    """Load component-level base routing and binary SDK carve-outs."""
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
        base_components = data["component-groups"]["base-packages"]["components"]
        sdk_exceptions = data["package-groups"]["exceptions-packages"]["packages"]
    except (KeyError, OSError, TypeError, tomllib.TOMLDecodeError) as exc:
        raise RuntimeError(f"Failed to load publication policy {path}: {exc}") from exc
    if not isinstance(base_components, list) or not all(
        isinstance(value, str) and value for value in base_components
    ):
        raise RuntimeError("Publication policy base component list is malformed")
    if not isinstance(sdk_exceptions, list) or not all(
        isinstance(value, str) and value for value in sdk_exceptions
    ):
        raise RuntimeError("Publication policy package exception list is malformed")
    return set(base_components), set(sdk_exceptions)


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
    base_components, sdk_exceptions = load_publish_policy(publish_policy)
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
            base_components,
            sdk_exceptions,
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
    koji_web_url = validate_https_url("koji-web-url", args.koji_web_url)
    job_id = read_job_id(args.job_id_file)

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
    component_tasks = select_completed_component_tasks(results)

    koji_context = make_koji_ssl_context(args.insecure_koji_tls)
    discovered: list[tuple[str, int, str]] = []
    package_tasks: list[dict[str, Any]] = []
    for component_task in component_tasks:
        component = component_task["component"]
        root_task_id = component_task["rootTaskId"]
        arch_task_ids = discover_arch_task_ids(
            fetch_bytes(f"{koji_web_url}/taskinfo?taskID={root_task_id}", koji_context),
            args.architecture,
        )
        component_output_count = 0
        for task_id in arch_task_ids:
            filenames = discover_rpm_outputs(
                fetch_bytes(f"{koji_web_url}/taskinfo?taskID={task_id}", koji_context),
                task_id,
                args.architecture,
            )
            component_output_count += len(filenames)
            discovered.extend((component, task_id, filename) for filename in filenames)
        if component_output_count == 0:
            raise RuntimeError(
                f"Koji tasks for {component} expose no {args.architecture} or noarch binary RPMs"
            )
        package_tasks.append(
            {
                "architectureTaskIds": arch_task_ids,
                "component": component,
                "rootTaskId": root_task_id,
            }
        )

    filenames = [filename for _, _, filename in discovered]
    if len(filenames) != len(set(filenames)):
        raise RuntimeError("Completed Koji package tasks expose duplicate RPM filenames")

    candidates = [
        download_rpm(
            destination=args.download_directory,
            filename=filename,
            koji_files_url=koji_files_url,
            ssl_context=koji_context,
            source_component=component,
            task_id=task_id,
        )
        for component, task_id, filename in discovered
    ]
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
            "kojiPackageTasks": package_tasks,
            "kojiTlsCertificateVerification": not args.insecure_koji_tls,
            "type": "control-tower-koji",
        },
        "architecture": args.architecture,
        "candidates": candidates,
        "result": "passed",
        "schemaVersion": 1,
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
                "schemaVersion": 1,
            },
        )
        print(f"##vso[task.logissue type=error]{exc}", file=sys.stderr)
        return 1

    write_report(args.report, report)
    print(f"Downloaded and routed {len(report['candidates'])} candidate RPMs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
