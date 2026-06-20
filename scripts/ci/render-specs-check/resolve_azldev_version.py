"""Resolve the azldev version that will be present after a PR merges.

Resolved values are printed as ``key=value`` records; diagnostics go to stderr.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

VERSION_RE = re.compile(r"[0-9A-Za-z._+-]+")
REPO_RE = re.compile(r"[A-Za-z0-9._-]+/[A-Za-z0-9._-]+")
SHA_RE = re.compile(r"[0-9a-f]{40}")
MERGE_ATTEMPTS = 30
CONTENT_ATTEMPTS = 5
RETRY_SECONDS = 4
GH_API_TIMEOUT_SECONDS = 15
GITHUB_API_VERSION = "2026-03-10"
PR_FIELD_COUNT = 3


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


def _validate_version(value: str, source: str) -> str:
    """Return a validated, single-token azldev version."""
    version = value.rstrip("\r\n")
    if not VERSION_RE.fullmatch(version):
        message = f"{source} is empty or contains unexpected characters"
        raise ResolutionError(message)
    return version


def _read_version(path: Path) -> str:
    """Read a version file without following an untrusted symlink."""
    if path.is_symlink():
        message = f"{path} must be a regular file, not a symlink"
        raise ResolutionError(message)
    try:
        value = path.read_text(encoding="ascii")
    except (OSError, UnicodeError) as error:
        message = f"could not read {path}: {error}"
        raise ResolutionError(message) from error
    return _validate_version(value, str(path))


def _validate_inputs(pull_request: PullRequest) -> None:
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


def _github_api(endpoint: str, *options: str) -> str:
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


def _validate_pr_snapshot(fields: list[str], pull_request: PullRequest) -> str:
    """Validate live PR fields against the trusted workflow snapshot."""
    if len(fields) != PR_FIELD_COUNT:
        message = "GitHub returned an invalid PR response"
        raise ResolutionError(message)
    polled_head, polled_base, mergeable = fields
    if polled_head != pull_request.head_sha:
        message = f"PR head advanced from {pull_request.head_sha!r} to {polled_head!r}; a newer run supersedes this one"
        raise ResolutionError(message)
    if polled_base != pull_request.base_sha:
        message = f"PR base advanced from {pull_request.base_sha!r} to {polled_base!r}; a newer run must validate it"
        raise ResolutionError(message)
    return mergeable


def _wait_for_merge_ref(pull_request: PullRequest, *, wait_for_merge: bool) -> None:
    """Validate the live PR snapshot and optionally wait for its merge ref."""
    endpoint = f"repos/{pull_request.repo}/pulls/{pull_request.number}"
    query = "[.head.sha, .base.sha, (.mergeable | tostring)] | @tsv"
    last_error: GitHubApiError | None = None
    for attempt in range(1, MERGE_ATTEMPTS + 1):
        try:
            fields = _github_api(endpoint, "--jq", query).rstrip("\r\n").split("\t")
        except GitHubApiError as error:
            last_error = error
            _log(f"PR API call failed ({attempt}/{MERGE_ATTEMPTS}): {error}; retrying...")
        else:
            last_error = None
            mergeable = _validate_pr_snapshot(fields, pull_request)
            if not wait_for_merge:
                return
            if mergeable == "false":
                message = "PR conflicts with the base branch"
                raise ResolutionError(message)
            if mergeable == "true":
                return
            _log(f"Waiting for GitHub to publish the merge ref ({attempt}/{MERGE_ATTEMPTS})...")
        if attempt < MERGE_ATTEMPTS:
            time.sleep(RETRY_SECONDS)

    message = (
        f"GitHub API failed after {MERGE_ATTEMPTS} attempts: {last_error}"
        if last_error
        else f"GitHub did not publish the merge ref after {MERGE_ATTEMPTS} attempts"
    )
    raise ResolutionError(message)


def _read_merged_version(pull_request: PullRequest) -> str:
    """Read the azldev pin from the pull request merge ref."""
    # A moving merge ref matters only if another pin change lands; that supersedes this run or conflicts.
    merge_ref = f"refs/pull/{pull_request.number}/merge"
    endpoint = f"repos/{pull_request.repo}/contents/.azldev-version?ref={merge_ref}"
    last_error: GitHubApiError | None = None
    for attempt in range(1, CONTENT_ATTEMPTS + 1):
        try:
            content = _github_api(endpoint, "-H", "Accept: application/vnd.github.raw")
        except GitHubApiError as error:
            last_error = error
            _log(f"Could not read the post-merge .azldev-version ({attempt}/{CONTENT_ATTEMPTS}): {error}; retrying...")
            if attempt < CONTENT_ATTEMPTS:
                time.sleep(RETRY_SECONDS)
        else:
            return _validate_version(content, "post-merge .azldev-version")

    message = f"could not read .azldev-version from the pull request merge ref: {last_error}"
    raise ResolutionError(message)


def resolve_version(
    base_version: str,
    head_version: str,
    *,
    pull_request: PullRequest,
) -> tuple[str, bool]:
    """Return the post-merge version and whether all specs must be rendered."""
    _validate_inputs(pull_request)
    base_version = _validate_version(base_version, "base version")
    head_version = _validate_version(head_version, "PR-head version")

    versions_differ = head_version != base_version
    _wait_for_merge_ref(pull_request, wait_for_merge=versions_differ)
    if not versions_differ:
        return base_version, False

    merged_version = _read_merged_version(pull_request)
    return merged_version, merged_version != base_version


def _parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, help="GitHub owner/repository")
    parser.add_argument("--pr-number", required=True, type=int, help="pull request number")
    parser.add_argument("--head-sha", required=True, help="expected PR head commit")
    parser.add_argument("--base-sha", required=True, help="trusted base commit")
    parser.add_argument("--base-version-file", required=True, type=Path, help="base azldev version file")
    parser.add_argument("--head-version-file", required=True, type=Path, help="PR-head azldev version file")
    return parser.parse_args()


def main() -> int:
    """Resolve the version and emit machine-readable output."""
    args = _parse_args()
    try:
        base_version = _read_version(args.base_version_file)
        head_version = _read_version(args.head_version_file)
        pull_request = PullRequest(
            repo=args.repo,
            number=args.pr_number,
            head_sha=args.head_sha,
            base_sha=args.base_sha,
        )
        version, render_all = resolve_version(
            base_version=base_version,
            head_version=head_version,
            pull_request=pull_request,
        )
        _log(
            f"Resolved azldev version: {version}; render all: {str(render_all).lower()} "
            f"(base: {base_version}, PR head: {head_version})"
        )
        print(f"azldev-version={version}")
        print(f"render-all={str(render_all).lower()}")
    except ResolutionError as error:
        _log(f"Error: {error}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
