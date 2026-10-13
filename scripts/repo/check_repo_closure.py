#!/usr/bin/env python3
"""Check base and base+SDK closure with locally available candidate RPMs."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import ssl
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, TypedDict

DOWNLOAD_TIMEOUT_SECONDS = 300
DNF_COMMAND = shutil.which("dnf") or shutil.which("dnf5") or shutil.which("dnf4") or "dnf"
DNF4_MAJOR_VERSION = 4
DNF5_MAJOR_VERSION = 5
NEVRA_COMPONENT_COUNT = 3
REPOQUERY_FIELD_SEPARATOR_COUNT = 3
RPM_MAGIC = b"\xed\xab\xee\xdb"
ClosureIssues = dict[tuple[str, str], str]


class CandidateInput(TypedDict):
    """One local binary RPM and its intended candidate repository."""

    path: Path
    repository: str


class CandidateRpm(TypedDict):
    """One validated and routed candidate RPM."""

    architecture: str
    filename: str
    name: str
    path: str
    repository: str
    sha256: str
    size: int


class ClosureIssue(TypedDict):
    """One unresolved dependency reported for a package."""

    dependency: str
    package: str


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--candidate-base-dir",
        type=Path,
        help="Directory containing binary RPMs to overlay onto base.",
    )
    parser.add_argument(
        "--candidate-sdk-dir",
        type=Path,
        help="Directory containing binary RPMs to overlay onto SDK/builddeps.",
    )
    parser.add_argument("--architecture", default="x86_64")
    parser.add_argument("--base-repo-url", required=True)
    parser.add_argument("--output-directory", required=True, type=Path)
    parser.add_argument("--sdk-repo-url", required=True)
    return parser.parse_args()


def validate_https_url(name: str, value: str) -> str:
    """Validate a credential-free HTTPS repository URL."""
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


def collect_candidate_inputs(
    candidate_base_dir: Path | None,
    candidate_sdk_dir: Path | None,
) -> list[CandidateInput]:
    """Collect already-routed binary RPMs from candidate input directories."""
    if (
        candidate_base_dir is not None
        and candidate_sdk_dir is not None
        and candidate_base_dir.resolve() == candidate_sdk_dir.resolve()
    ):
        raise RuntimeError("Candidate base and SDK directories must be different")
    inputs: list[CandidateInput] = []
    for directory, repository in (
        (candidate_base_dir, "candidate-base"),
        (candidate_sdk_dir, "candidate-sdk"),
    ):
        if directory is None:
            continue
        if not directory.is_dir():
            raise RuntimeError(f"Candidate RPM directory does not exist: {directory}")
        inputs.extend(
            {"path": path.resolve(), "repository": repository}
            for path in sorted(directory.glob("*.rpm"))
            if path.is_file()
        )
    if not inputs:
        raise RuntimeError("Candidate base and SDK directories contain no RPMs")
    return inputs


def run_command(
    command: list[str],
    *,
    log_path: Path,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    """Run one tool, persist combined output, and optionally fail loudly."""
    result = subprocess.run(
        command,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(result.stdout, encoding="utf-8")
    if check and result.returncode != 0:
        rendered = " ".join(command)
        raise RuntimeError(f"Command failed with exit code {result.returncode}: {rendered}")
    return result


def query_candidate_header(rpm_path: Path, log_directory: Path) -> tuple[str, str]:
    """Read binary name and architecture from one candidate RPM header."""
    if not rpm_path.is_file():
        raise RuntimeError(f"Candidate RPM does not exist: {rpm_path}")
    with rpm_path.open("rb") as stream:
        if stream.read(len(RPM_MAGIC)) != RPM_MAGIC:
            raise RuntimeError(f"Candidate file is not an RPM: {rpm_path}")
    result = run_command(
        ["rpm", "-qp", "--qf", "%{NAME}|%{ARCH}\\n", str(rpm_path)],
        log_path=log_directory / f"rpm-query-{rpm_path.name}.log",
    )
    rows = [line.split("|", maxsplit=1) for line in result.stdout.splitlines() if line.count("|") == 1]
    if len(rows) != 1 or not all(rows[0]):
        raise RuntimeError(f"Candidate RPM header must expose exactly one name and architecture: {rpm_path}")
    return rows[0][0], rows[0][1]


def hash_file(path: Path) -> tuple[str, int]:
    """Return SHA-256 and size for one local file."""
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
            size += len(chunk)
    return digest.hexdigest(), size


def reset_directory(path: Path) -> None:
    """Create one empty generated-output directory."""
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True)


def prepare_candidate_repositories(
    *,
    architecture: str,
    candidates: list[CandidateInput],
    output_directory: Path,
) -> tuple[Path, Path, list[CandidateRpm], dict[str, str]]:
    """Validate already-routed RPMs and build both candidate repositories."""
    candidate_base_repo = output_directory / "candidate-base"
    candidate_sdk_repo = output_directory / "candidate-sdk"
    generated_repositories = {
        candidate_base_repo.resolve(),
        candidate_sdk_repo.resolve(),
    }
    for candidate in candidates:
        candidate_path = candidate["path"].resolve()
        if any(
            candidate_path == repository or repository in candidate_path.parents
            for repository in generated_repositories
        ):
            raise RuntimeError(
                f"Candidate RPM cannot be inside a generated repository: {candidate_path}"
            )
    reset_directory(candidate_base_repo)
    reset_directory(candidate_sdk_repo)

    package_repositories: dict[str, str] = {}
    manifest: list[CandidateRpm] = []
    seen_filenames: set[str] = set()
    for candidate in candidates:
        source_path = candidate["path"]
        package_name, package_architecture = query_candidate_header(
            source_path,
            output_directory / "rpm-queries",
        )
        if package_architecture not in {architecture, "noarch"}:
            raise RuntimeError(
                f"Candidate {package_name} has architecture {package_architecture}, expected {architecture} or noarch"
            )
        if package_name in package_repositories:
            raise RuntimeError(f"Candidate set contains duplicate package name: {package_name}")
        if source_path.name in seen_filenames:
            raise RuntimeError(f"Candidate set contains duplicate RPM filename: {source_path.name}")
        seen_filenames.add(source_path.name)

        repository = candidate["repository"]
        package_repositories[package_name] = repository
        destination_directory = (
            candidate_base_repo if repository == "candidate-base" else candidate_sdk_repo
        )
        destination_path = destination_directory / source_path.name
        shutil.copy2(source_path, destination_path)
        sha256, size = hash_file(destination_path)
        manifest.append(
            {
                "architecture": package_architecture,
                "filename": source_path.name,
                "name": package_name,
                "path": str(destination_path),
                "repository": repository,
                "sha256": sha256,
                "size": size,
            }
        )

    run_command(
        ["createrepo_c", str(candidate_base_repo)],
        log_path=output_directory / "createrepo-base.log",
    )
    run_command(
        ["createrepo_c", str(candidate_sdk_repo)],
        log_path=output_directory / "createrepo-sdk.log",
    )
    return candidate_base_repo, candidate_sdk_repo, manifest, package_repositories


def write_dnf_config(
    *,
    base_repo_url: str,
    candidate_base_repo: Path,
    candidate_sdk_repo: Path,
    config_path: Path,
    excluded_baseline_packages: list[str],
    include_candidates: bool,
    include_sdk: bool,
    sdk_repo_url: str,
) -> None:
    """Write an isolated DNF configuration for one logical repository view."""
    baseline_excludes = ""
    if excluded_baseline_packages:
        baseline_excludes = f"excludepkgs={','.join(sorted(excluded_baseline_packages))}\n"
    candidate_base = ""
    if include_candidates:
        candidate_base = f"""
[candidate-base]
name=Fresh base candidate RPMs
baseurl={candidate_base_repo.resolve().as_uri()}
enabled=1
gpgcheck=0
repo_gpgcheck=0
cost=100
"""
    sdk = ""
    if include_sdk:
        candidate_sdk = ""
        if include_candidates:
            candidate_sdk = f"""
[candidate-sdk]
name=Fresh SDK candidate RPMs
baseurl={candidate_sdk_repo.resolve().as_uri()}
enabled=1
gpgcheck=0
repo_gpgcheck=0
cost=100
"""
        sdk = f"""
{candidate_sdk}

[baseline-sdk]
name=Azure Linux SDK baseline
baseurl={sdk_repo_url}
enabled=1
gpgcheck=0
repo_gpgcheck=0
{baseline_excludes}"""
    config_path.write_text(
        f"""[main]
cachedir={config_path.parent / "cache"}
persistdir={config_path.parent / "persist"}
reposdir=/dev/null
plugins=1
keepcache=1
metadata_expire=-1
best=1

{candidate_base}

[baseline-base]
name=Azure Linux base baseline
baseurl={base_repo_url}
enabled=1
gpgcheck=0
repo_gpgcheck=0
cost=1000
{baseline_excludes}
{sdk}""",
        encoding="utf-8",
    )


def dnf_prefix(config_path: Path, architecture: str) -> list[str]:
    """Return arguments shared by isolated DNF invocations."""
    return [
        DNF_COMMAND,
        "-q",
        "-c",
        str(config_path),
        "--releasever=4.0",
        f"--forcearch={architecture}",
    ]


def detect_dnf_major_version(log_path: Path) -> int:
    """Return the supported DNF major version selected by the environment."""
    result = run_command([DNF_COMMAND, "--version"], log_path=log_path)
    first_line = result.stdout.splitlines()[0] if result.stdout else ""
    if first_line.startswith("4."):
        return DNF4_MAJOR_VERSION
    if first_line.startswith("dnf5 version 5."):
        return DNF5_MAJOR_VERSION
    raise RuntimeError(f"Repository closure requires DNF 4 or 5; reported {first_line!r}")


def dnf_list_option(name: str, values: list[str], dnf_major_version: int) -> list[str]:
    """Render list options using the syntax expected by each DNF generation."""
    if dnf_major_version == DNF5_MAJOR_VERSION:
        return [f"--{name}={','.join(values)}"]
    return [f"--{name}={value}" for value in values]


def assert_candidate_selected(
    *,
    architecture: str,
    config_path: Path,
    expected_repositories: dict[str, str],
    log_directory: Path,
) -> list[dict[str, str]]:
    """Require the newest package for every candidate name to come from its overlay."""
    selected: list[dict[str, str]] = []
    for package_name, expected_repository in sorted(expected_repositories.items()):
        result = run_command(
            [
                *dnf_prefix(config_path, architecture),
                "repoquery",
                "--latest-limit=1",
                "--qf",
                "%{name}|%{evr}|%{arch}|%{repoid}",
                package_name,
            ],
            log_path=log_directory / f"repoquery-{package_name}.log",
        )
        rows = [
            line.split("|", maxsplit=3)
            for line in result.stdout.splitlines()
            if line.count("|") == REPOQUERY_FIELD_SEPARATOR_COUNT
        ]
        if not rows:
            raise RuntimeError(f"DNF found no package named {package_name}")
        if any(row[3] != expected_repository for row in rows):
            repositories = ", ".join(sorted({row[3] for row in rows}))
            raise RuntimeError(
                f"Newest {package_name} was not selected exclusively from {expected_repository} "
                f"(selected repositories: {repositories})"
            )
        selected.extend(
            {"architecture": row[2], "evr": row[1], "name": row[0], "repository": row[3]}
            for row in rows
        )
    return selected


def fetch_bytes(url: str) -> bytes:
    """Fetch one public HTTPS resource."""
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "azurelinux-repository-closure/1"},
    )
    try:
        with urllib.request.urlopen(
            request,
            context=ssl.create_default_context(),
            timeout=DOWNLOAD_TIMEOUT_SECONDS,
        ) as response:
            return response.read()
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Request failed for {url}: {exc.reason}") from exc


def repomd_checksum(repo_url: str) -> dict[str, str]:
    """Hash the exact repository metadata root used by the check."""
    url = f"{repo_url.rstrip('/')}/repodata/repomd.xml"
    content = fetch_bytes(url)
    return {"sha256": hashlib.sha256(content).hexdigest(), "url": url}


def package_identity(package: str) -> str:
    """Return stable name.arch identity from a repoclosure NEVRA."""
    name_version_release, separator, architecture = package.rpartition(".")
    if not separator:
        raise RuntimeError(f"Repoclosure returned malformed package identity: {package}")
    parts = name_version_release.rsplit("-", maxsplit=2)
    if len(parts) != NEVRA_COMPONENT_COUNT or not parts[0]:
        raise RuntimeError(f"Repoclosure returned malformed package identity: {package}")
    return f"{parts[0]}.{architecture}"


def parse_repoclosure_issues(output: str) -> ClosureIssues:
    """Parse unresolved package/dependency pairs from DNF repoclosure output."""
    issues: ClosureIssues = {}
    package: str | None = None
    for line in output.splitlines():
        if line.startswith("package: "):
            package_with_repository = line.removeprefix("package: ")
            package = package_with_repository.rsplit(" from ", maxsplit=1)[0]
        elif package is not None and line.startswith("    "):
            dependency = line.strip()
            if dependency:
                issues[(package_identity(package), dependency)] = package
    return issues


def closure_issue_report(
    issues: ClosureIssues,
    keys: set[tuple[str, str]] | None = None,
) -> list[ClosureIssue]:
    """Render closure issues in stable report order."""
    selected_keys = set(issues) if keys is None else keys
    return [
        {"dependency": dependency, "package": issues[(identity, dependency)]}
        for identity, dependency in sorted(selected_keys)
    ]


def run_repoclosure(
    *,
    architecture: str,
    config_path: Path,
    dnf_major_version: int,
    log_path: Path,
    repositories: list[str],
) -> tuple[int, ClosureIssues]:
    """Run DNF repoclosure and distinguish dependency failures from tool errors."""
    command = [
        *dnf_prefix(config_path, architecture),
        "repoclosure",
        *dnf_list_option("arch", [architecture, "noarch"], dnf_major_version),
        "--newest",
        *dnf_list_option("check", repositories, dnf_major_version),
    ]
    result = run_command(command, log_path=log_path, check=False)
    issues = parse_repoclosure_issues(result.stdout)
    dependency_failure = "Repoclosure ended with unresolved dependencies" in result.stdout
    if result.returncode != 0 and not dependency_failure:
        rendered = " ".join(command)
        raise RuntimeError(
            f"Repoclosure command failed with exit code {result.returncode}: {rendered}"
        )
    if result.returncode == 0 and issues:
        raise RuntimeError("Repoclosure reported unresolved dependencies but returned success")
    return result.returncode, issues


def run_closure_view(
    *,
    architecture: str,
    base_repo_url: str,
    candidate_base_repo: Path,
    candidate_sdk_repo: Path,
    dnf_major_version: int,
    expected_repositories: dict[str, str],
    include_sdk: bool,
    output_directory: Path,
    sdk_repo_url: str,
    view_name: str,
) -> dict[str, Any]:
    """Compare baseline and candidate closure for one repository view."""
    view_directory = output_directory / "views" / view_name
    reset_directory(view_directory)
    baseline_config_path = view_directory / "baseline-dnf.conf"
    write_dnf_config(
        base_repo_url=base_repo_url,
        candidate_base_repo=candidate_base_repo,
        candidate_sdk_repo=candidate_sdk_repo,
        config_path=baseline_config_path,
        excluded_baseline_packages=[],
        include_candidates=False,
        include_sdk=include_sdk,
        sdk_repo_url=sdk_repo_url,
    )
    run_command(
        [*dnf_prefix(baseline_config_path, architecture), "makecache"],
        log_path=view_directory / "baseline-makecache.log",
    )
    baseline_repositories = ["baseline-base"]
    if include_sdk:
        baseline_repositories.append("baseline-sdk")
    baseline_exit_code, baseline_issues = run_repoclosure(
        architecture=architecture,
        config_path=baseline_config_path,
        dnf_major_version=dnf_major_version,
        log_path=view_directory / "baseline-repoclosure.log",
        repositories=baseline_repositories,
    )

    selection_config_path = view_directory / "selection-dnf.conf"
    write_dnf_config(
        base_repo_url=base_repo_url,
        candidate_base_repo=candidate_base_repo,
        candidate_sdk_repo=candidate_sdk_repo,
        config_path=selection_config_path,
        excluded_baseline_packages=[],
        include_candidates=True,
        include_sdk=include_sdk,
        sdk_repo_url=sdk_repo_url,
    )
    selected = assert_candidate_selected(
        architecture=architecture,
        config_path=selection_config_path,
        expected_repositories=expected_repositories,
        log_directory=view_directory,
    )

    candidate_config_path = view_directory / "candidate-dnf.conf"
    write_dnf_config(
        base_repo_url=base_repo_url,
        candidate_base_repo=candidate_base_repo,
        candidate_sdk_repo=candidate_sdk_repo,
        config_path=candidate_config_path,
        excluded_baseline_packages=list(expected_repositories),
        include_candidates=True,
        include_sdk=include_sdk,
        sdk_repo_url=sdk_repo_url,
    )
    run_command(
        [*dnf_prefix(candidate_config_path, architecture), "makecache"],
        log_path=view_directory / "candidate-makecache.log",
    )
    candidate_repositories = [*baseline_repositories, "candidate-base"]
    if include_sdk:
        candidate_repositories.append("candidate-sdk")
    candidate_exit_code, candidate_issues = run_repoclosure(
        architecture=architecture,
        config_path=candidate_config_path,
        dnf_major_version=dnf_major_version,
        log_path=view_directory / "candidate-repoclosure.log",
        repositories=candidate_repositories,
    )
    new_issue_keys = set(candidate_issues) - set(baseline_issues)
    return {
        "baselineRepoclosureExitCode": baseline_exit_code,
        "baselineUnresolvedDependencies": closure_issue_report(baseline_issues),
        "candidateRepoclosureExitCode": candidate_exit_code,
        "candidateSelection": selected,
        "candidateUnresolvedDependencies": closure_issue_report(candidate_issues),
        "name": view_name,
        "newUnresolvedDependencies": closure_issue_report(candidate_issues, new_issue_keys),
        "result": "passed" if not new_issue_keys else "failed",
    }


def run_check(args: argparse.Namespace) -> dict[str, Any]:
    """Prepare candidate repositories and run both closure views."""
    base_repo_url = validate_https_url("base-repo-url", args.base_repo_url)
    sdk_repo_url = validate_https_url("sdk-repo-url", args.sdk_repo_url)
    architecture: str = args.architecture
    candidates = collect_candidate_inputs(
        args.candidate_base_dir,
        args.candidate_sdk_dir,
    )
    output_directory: Path = args.output_directory
    output_directory.mkdir(parents=True, exist_ok=True)
    dnf_major_version = detect_dnf_major_version(output_directory / "dnf-version.log")

    candidate_base_repo, candidate_sdk_repo, candidate_rpms, package_repositories = (
        prepare_candidate_repositories(
            architecture=architecture,
            candidates=candidates,
            output_directory=output_directory,
        )
    )
    baselines = {
        "base": repomd_checksum(base_repo_url),
        "sdk": repomd_checksum(sdk_repo_url),
    }
    base_candidates = {
        name: repository
        for name, repository in package_repositories.items()
        if repository == "candidate-base"
    }
    views = [
        run_closure_view(
            architecture=architecture,
            base_repo_url=base_repo_url,
            candidate_base_repo=candidate_base_repo,
            candidate_sdk_repo=candidate_sdk_repo,
            dnf_major_version=dnf_major_version,
            expected_repositories=base_candidates,
            include_sdk=False,
            output_directory=output_directory,
            sdk_repo_url=sdk_repo_url,
            view_name="base",
        ),
        run_closure_view(
            architecture=architecture,
            base_repo_url=base_repo_url,
            candidate_base_repo=candidate_base_repo,
            candidate_sdk_repo=candidate_sdk_repo,
            dnf_major_version=dnf_major_version,
            expected_repositories=package_repositories,
            include_sdk=True,
            output_directory=output_directory,
            sdk_repo_url=sdk_repo_url,
            view_name="base-plus-sdk",
        ),
    ]
    result = "passed" if all(view["result"] == "passed" for view in views) else "failed"
    return {
        "architecture": architecture,
        "baselines": baselines,
        "candidatePackageRepositories": package_repositories,
        "candidateRpms": candidate_rpms,
        "result": result,
        "schemaVersion": 1,
        "views": views,
    }


def write_report(path: Path, report: dict[str, Any]) -> None:
    """Write a stable machine-readable report."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def format_new_closure_failures(report: dict[str, Any]) -> list[str]:
    """Render newly introduced closure failures for CI logs."""
    lines: list[str] = []
    for view in report["views"]:
        issues = view["newUnresolvedDependencies"]
        if not issues:
            continue
        lines.append(f"New closure failures in {view['name']}:")
        lines.extend(
            f"  {issue['package']} requires {issue['dependency']}" for issue in issues
        )
    return lines


def main() -> int:
    """Run the closure check and always preserve a report for triage."""
    args = _parse_args()
    report_path = args.output_directory / "repository-closure.json"
    try:
        report = run_check(args)
    except (OSError, RuntimeError, TypeError, ValueError) as exc:
        report = {
            "error": str(exc),
            "result": "failed",
            "schemaVersion": 1,
        }
        write_report(report_path, report)
        print(f"Repository closure check failed: {exc}", file=sys.stderr)
        return 1

    write_report(report_path, report)
    if report["result"] != "passed":
        for line in format_new_closure_failures(report):
            print(line, file=sys.stderr)
        print(f"Full repository closure report: {report_path}", file=sys.stderr)
        return 1
    print("Candidate RPMs introduce no new closure failures for base or base+SDK.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
