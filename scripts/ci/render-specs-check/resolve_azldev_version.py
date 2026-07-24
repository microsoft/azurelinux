"""Resolve the selected azldev Go module to an immutable Git hash.

Resolved values are printed as ``key=value`` records; diagnostics go to stderr.
The ``hash`` command prints only the hash for local and non-PR callers.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path

VERSION_RE = re.compile(r"[0-9A-Za-z._+-]+")
REPO_RE = re.compile(r"[A-Za-z0-9._-]+/[A-Za-z0-9._-]+")
SHA_RE = re.compile(r"[0-9a-f]{40}")
AZLDEV_MODULE = "github.com/microsoft/azure-linux-dev-tools"
AZLDEV_REPOSITORY = f"https://{AZLDEV_MODULE}"
MERGE_ATTEMPTS = 30
CONTENT_ATTEMPTS = 5
RETRY_SECONDS = 4
GH_API_TIMEOUT_SECONDS = 15
GO_COMMAND_TIMEOUT_SECONDS = 60
GITHUB_API_VERSION = "2026-03-10"
PR_FIELD_COUNT = 4


@dataclass(frozen=True, slots=True)
class PullRequest:
    """Expected pull request snapshot."""

    repo: str
    number: int
    head_sha: str
    base_sha: str


class ResolutionError(RuntimeError):
    """Raised when the post-merge version cannot be resolved safely."""


class GitHubApiError(ResolutionError):
    """Raised when a GitHub API request fails."""


def _log(message: str) -> None:
    """Print a diagnostic without contaminating machine-readable stdout."""
    print(message, file=sys.stderr)


def validate_version(value: str, source: str) -> str:
    """Return a validated, single-token azldev version."""
    version = value.rstrip("\r\n")
    if not VERSION_RE.fullmatch(version):
        message = f"{source} is empty or contains unexpected characters"
        raise ResolutionError(message)
    return version


def _run_go(*args: str, cwd: Path | None = None) -> str:
    """Run Go without ambient workspace or toolchain selection and return stdout."""
    environment = os.environ.copy()
    environment["GOFLAGS"] = ""
    environment["GOTOOLCHAIN"] = "local"
    environment["GOWORK"] = "off"
    try:
        result = subprocess.run(
            ["go", *args],
            capture_output=True,
            text=True,
            check=False,
            cwd=cwd,
            timeout=GO_COMMAND_TIMEOUT_SECONDS,
            env=environment,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        message = f"could not run go {' '.join(args)}: {error}"
        raise ResolutionError(message) from error
    if result.returncode != 0:
        detail = "\n".join(output for output in (result.stdout.strip(), result.stderr.strip()) if output)
        detail = detail or f"go exited with {result.returncode}"
        message = f"go {' '.join(args)} failed: {detail}"
        raise ResolutionError(message)
    return result.stdout


def _validated_module_path(path: Path) -> Path:
    """Return an absolute regular module file without symlinked components."""
    absolute_path = path.absolute()
    for component in (absolute_path, *absolute_path.parents):
        if component.is_symlink():
            message = f"{path} must not use a symlinked path component, but {component} is a symlink"
            raise ResolutionError(message)
    if not absolute_path.is_file():
        message = f"{path} must be a regular file"
        raise ResolutionError(message)
    return absolute_path


def read_version(path: Path) -> str:
    """Read the direct azldev requirement from one validated module file."""
    module_path = _validated_module_path(path)
    try:
        module = json.loads(_run_go("mod", "edit", "-json", str(module_path)))
    except (json.JSONDecodeError, ResolutionError) as error:
        message = f"could not parse {path}: {error}"
        raise ResolutionError(message) from error
    requires = module.get("Require", []) if isinstance(module, dict) else []
    direct_requirements = [
        requirement
        for requirement in requires
        if isinstance(requirement, dict)
        and requirement.get("Path") == AZLDEV_MODULE
        and requirement.get("Indirect", False) is False
    ]
    if len(direct_requirements) != 1:
        message = f"{path} must contain exactly one direct azldev requirement, but has {len(direct_requirements)}"
        raise ResolutionError(message)
    version = direct_requirements[0].get("Version")
    if not isinstance(version, str):
        message = (
            f"{path} direct azldev requirement has version with type {type(version).__name__} and value {version!r}"
        )
        raise ResolutionError(message)
    return validate_version(version, f"{path} azldev version")


def _version_from_content(content: str, source: str) -> str:
    """Parse an API-provided go.mod through Go and return its azldev version."""
    try:
        with tempfile.TemporaryDirectory() as directory:
            modfile = Path(directory, "go.mod")
            modfile.write_text(content, encoding="utf-8")
            return read_version(modfile)
    except OSError as error:
        message = f"could not parse {source}: {error}"
        raise ResolutionError(message) from error


def resolve_hash(version: str) -> str:
    """Resolve an azldev module version to its full Microsoft Git revision."""
    version = validate_version(version, "azldev version")
    try:
        module = json.loads(_run_go("mod", "download", "-json", f"{AZLDEV_MODULE}@{version}"))
    except json.JSONDecodeError as error:
        message = f"go returned invalid JSON while resolving {AZLDEV_MODULE}@{version}"
        raise ResolutionError(message) from error
    origin = module.get("Origin", {}) if isinstance(module, dict) else {}
    if not isinstance(origin, dict) or origin.get("VCS") != "git" or origin.get("URL") != AZLDEV_REPOSITORY:
        message = f"Go resolved {AZLDEV_MODULE}@{version} from an unexpected source"
        raise ResolutionError(message)
    revision = origin.get("Hash", "")
    if not isinstance(revision, str) or not SHA_RE.fullmatch(revision):
        message = f"Go did not resolve {AZLDEV_MODULE}@{version} to a full Git hash"
        raise ResolutionError(message)
    return revision


def validate_inputs(pull_request: PullRequest) -> None:
    """Validate values used in API paths and workflow output."""
    if not REPO_RE.fullmatch(pull_request.repo):
        message = f"repo is not a valid owner/repo: {pull_request.repo!r}"
        raise ResolutionError(message)
    if pull_request.number < 1:
        message = f"pr-number is not a positive integer: {pull_request.number!r}"
        raise ResolutionError(message)
    if not SHA_RE.fullmatch(pull_request.head_sha):
        message = f"head-sha is not a 40-character lowercase hex SHA: {pull_request.head_sha!r}"
        raise ResolutionError(message)
    if not SHA_RE.fullmatch(pull_request.base_sha):
        message = f"base-sha is not a 40-character lowercase hex SHA: {pull_request.base_sha!r}"
        raise ResolutionError(message)


def github_api(endpoint: str, *options: str) -> str:
    """Call GitHub through the authenticated gh CLI and return stdout."""
    command = ["gh", "api", "-H", f"X-GitHub-Api-Version: {GITHUB_API_VERSION}", endpoint, *options]
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
            timeout=GH_API_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired as error:
        message = f"gh api timed out after {GH_API_TIMEOUT_SECONDS} seconds"
        raise GitHubApiError(message) from error
    if result.returncode != 0:
        detail = result.stderr.strip() or f"gh api exited with {result.returncode}"
        raise GitHubApiError(detail)
    return result.stdout


def _validate_pr_snapshot(fields: list[str], pull_request: PullRequest) -> tuple[str, str]:
    """Validate live PR fields against the trusted workflow snapshot."""
    if len(fields) != PR_FIELD_COUNT:
        message = "GitHub returned an invalid PR response"
        raise ResolutionError(message)
    polled_head, polled_base, mergeable, merge_commit_sha = fields
    if polled_head != pull_request.head_sha:
        message = f"PR head advanced from {pull_request.head_sha!r} to {polled_head!r}; a newer run supersedes this one"
        raise ResolutionError(message)
    if polled_base != pull_request.base_sha:
        message = f"PR base advanced from {pull_request.base_sha!r} to {polled_base!r}; a newer run must validate it"
        raise ResolutionError(message)
    return mergeable, merge_commit_sha


def _wait_for_merge_commit(pull_request: PullRequest, *, wait_for_merge: bool) -> str:
    """Validate the live PR snapshot and return its immutable test-merge SHA."""
    endpoint = f"repos/{pull_request.repo}/pulls/{pull_request.number}"
    query = '[.head.sha, .base.sha, (.mergeable | tostring), (.merge_commit_sha // "")] | @tsv'
    last_error: GitHubApiError | None = None
    for attempt in range(1, MERGE_ATTEMPTS + 1):
        try:
            fields = github_api(endpoint, "--jq", query).rstrip("\r\n").split("\t")
        except GitHubApiError as error:
            last_error = error
            _log(f"PR API call failed ({attempt}/{MERGE_ATTEMPTS}): {error}; retrying...")
        else:
            last_error = None
            mergeable, merge_commit_sha = _validate_pr_snapshot(fields, pull_request)
            if not wait_for_merge:
                return merge_commit_sha
            if mergeable == "false":
                message = "PR conflicts with the base branch"
                raise ResolutionError(message)
            if mergeable == "true" and SHA_RE.fullmatch(merge_commit_sha):
                return merge_commit_sha
            _log(f"Waiting for GitHub to publish the test-merge commit ({attempt}/{MERGE_ATTEMPTS})...")
        if attempt < MERGE_ATTEMPTS:
            time.sleep(RETRY_SECONDS)

    message = (
        f"GitHub API failed after {MERGE_ATTEMPTS} attempts: {last_error}"
        if last_error
        else f"GitHub did not publish a valid test-merge commit after {MERGE_ATTEMPTS} attempts"
    )
    raise ResolutionError(message)


def _read_merged_version(pull_request: PullRequest, modfile: Path, merge_commit_sha: str) -> str:
    """Read the azldev pin from an immutable test-merge commit."""
    modfile_path = modfile.as_posix()
    endpoint = f"repos/{pull_request.repo}/contents/{modfile_path}?ref={merge_commit_sha}"
    last_error: GitHubApiError | None = None
    for attempt in range(1, CONTENT_ATTEMPTS + 1):
        try:
            content = github_api(endpoint, "-H", "Accept: application/vnd.github.raw")
        except GitHubApiError as error:
            last_error = error
            _log(f"Could not read post-merge {modfile_path} ({attempt}/{CONTENT_ATTEMPTS}): {error}; retrying...")
            if attempt < CONTENT_ATTEMPTS:
                time.sleep(RETRY_SECONDS)
        else:
            return _version_from_content(content, f"post-merge {modfile_path}")

    message = f"could not read {modfile_path} from test-merge commit {merge_commit_sha}: {last_error}"
    raise ResolutionError(message)


def resolve_version(
    base_version: str,
    head_version: str,
    *,
    pull_request: PullRequest,
    merged_modfile: Path = Path("go.mod"),
) -> tuple[str, bool]:
    """Return the post-merge version and whether all specs must be rendered."""
    validate_inputs(pull_request)
    base_version = validate_version(base_version, "base version")
    head_version = validate_version(head_version, "PR-head version")

    versions_differ = head_version != base_version
    merge_commit_sha = _wait_for_merge_commit(pull_request, wait_for_merge=versions_differ)
    if not versions_differ:
        return base_version, False

    merged_version = _read_merged_version(pull_request, merged_modfile, merge_commit_sha)
    return merged_version, merged_version != base_version


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    hash_parser = commands.add_parser("hash", help="resolve one go.mod to an azldev hash")
    hash_parser.add_argument("modfile", type=Path)

    post_merge_parser = commands.add_parser("post-merge", help="resolve the hash after a pull request merges")
    post_merge_parser.add_argument("--repo", required=True, help="GitHub owner/repository")
    post_merge_parser.add_argument("--pr-number", required=True, type=int, help="pull request number")
    post_merge_parser.add_argument("--head-sha", required=True, help="expected PR head commit")
    post_merge_parser.add_argument("--base-sha", required=True, help="trusted base commit")
    post_merge_parser.add_argument("--base-modfile", required=True, type=Path, help="base Go module file")
    post_merge_parser.add_argument("--head-modfile", required=True, type=Path, help="PR-head Go module file")
    return parser.parse_args()


def main() -> int:
    """Resolve the version and emit machine-readable output."""
    args = parse_args()
    try:
        if args.command == "hash":
            print(resolve_hash(read_version(args.modfile)))
            return 0

        pull_request = PullRequest(
            repo=args.repo,
            number=args.pr_number,
            head_sha=args.head_sha,
            base_sha=args.base_sha,
        )
        base_version = read_version(args.base_modfile)
        head_version = read_version(args.head_modfile)
        version, render_all = resolve_version(
            base_version=base_version,
            head_version=head_version,
            pull_request=pull_request,
            merged_modfile=args.base_modfile,
        )
        revision = resolve_hash(version)
        _log(
            f"Resolved azldev version: {version} ({revision}); render all: {str(render_all).lower()} "
            f"(base: {base_version}, PR head: {head_version})"
        )
        print(f"azldev-hash={revision}")
        print(f"render-all={str(render_all).lower()}")
    except ResolutionError as error:
        _log(f"Error: {error}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
