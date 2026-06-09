"""Resolve the ``(target, source)`` commit range for a post-merge delta build.

Strategy (see ``.github/workflows/ado/templates/sources-upload-stages.yml``):

* ``source`` is the commit that triggered this run (``Build.SourceVersion``).
* ``target`` is the ``sourceVersion`` of the immediately-preceding CI build of
  this pipeline definition on the same branch, selected by build id —
  regardless of that build's result.

Selecting the immediately-preceding build *by id* (not by success) is what
keeps concurrent runs from overlapping: build N always pairs with build N-1, so
successive merges produce ADJACENT, non-overlapping commit ranges even when an
earlier run is still in flight or has failed. A failed/cancelled run still
"claims" its range — those commits are skipped until the weekly true-up job —
which is the accepted bias-to-miss tradeoff. Overlapping ranges would cause
NEVR collisions in the build system, which is far worse than a transient gap.

Rebase-merge aware: because the range is a two-commit span (previous tip →
current tip), it captures EVERY commit a rebase merge appends, not just the
tip. ``azldev component changed`` then tree-diffs the two endpoints.

Fallback (first run, or no prior CI build found): ``target = source^1`` with a
warning. That run only builds the single tip commit's components, self-
correcting on the next push.

The resolved hashes are printed to stdout as two ``key=value`` lines
(``sourceCommit=<sha>`` and ``targetCommit=<sha>``). The calling pipeline step
reads them and sets the corresponding ADO pipeline variables, so the
variable wiring stays visible in the YAML rather than hidden here. All
diagnostic output goes to stderr to keep stdout machine-readable.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys

import ado_rest

# A build is eligible as a baseline only if it was itself a CI build of the
# branch. Manual / PR / scheduled runs are excluded so that a one-off manual
# test run of this pipeline cannot become the baseline for the next real CI
# build (which would skip everything in between).
_BASELINE_REASONS = frozenset({"individualCI", "batchedCI"})

_SHA_RE = re.compile(r"^[0-9a-f]{40}$")


def _log(message: str) -> None:
    """Print a diagnostic message to stderr, keeping stdout machine-readable."""
    print(message, file=sys.stderr)


def _emit_range(source_commit: str, target_commit: str) -> None:
    """Print the resolved range to stdout as ``key=value`` lines.

    The calling pipeline step parses these two lines and sets the
    ``sourceCommit`` / ``targetCommit`` pipeline variables, so the
    variable wiring lives in the YAML rather than in this script.
    """
    _log(f"Resolved range: target={target_commit} source={source_commit}")
    print(f"sourceCommit={source_commit}")
    print(f"targetCommit={target_commit}")


def _run_git(args: list[str]) -> subprocess.CompletedProcess[str]:
    """Run a ``git`` command, capturing text output without raising on failure."""
    return subprocess.run(["git", *args], check=False, capture_output=True, text=True)


def _commit_present(commit: str) -> bool:
    """Return whether ``commit`` exists as a commit object in the local clone."""
    return _run_git(["cat-file", "-e", f"{commit}^{{commit}}"]).returncode == 0


def _ensure_commit(commit: str, repo_uri: str) -> bool:
    """Make ``commit`` available locally, fetching it if necessary.

    The OneBranch checkout may be shallow, so fetch the single commit object
    (depth 1 — its tree and blobs, with no ancestors, which is all a two-point
    tree diff needs).

    Args:
        commit: 40-hex commit SHA to ensure is present.
        repo_uri: Remote URL to fetch from.

    Returns:
        True if the commit is present afterwards, False otherwise.
    """
    if _commit_present(commit):
        return True
    fetch = _run_git(["fetch", "--no-tags", "--depth=1", repo_uri, commit])
    if fetch.returncode != 0:
        _log(f"WARNING: Failed to fetch commit {commit}: {fetch.stderr.strip()}")
        return False
    return _commit_present(commit)


def _parent_commit(commit: str, repo_uri: str) -> str | None:
    """Return ``commit^1`` (40-hex), fetching depth 2 so the parent is present."""
    _run_git(["fetch", "--no-tags", "--depth=2", repo_uri, commit])
    result = _run_git(["rev-parse", "--verify", "--quiet", f"{commit}^1"])
    parent = result.stdout.strip()
    if result.returncode != 0 or not _SHA_RE.match(parent):
        return None
    return parent


def _select_baseline(builds: list[object], current_build_id: int) -> str | None:
    """Pick the source commit of the immediately-preceding eligible CI build.

    Args:
        builds: Raw build objects from ``ado_rest.list_builds``.
        current_build_id: Id of the running build; only earlier builds qualify.

    Returns:
        The ``sourceVersion`` of the highest-id eligible build, or None.
    """
    candidates: list[tuple[int, str]] = []
    for build in builds:
        if not isinstance(build, dict):
            continue
        build_id = build.get("id")
        if not isinstance(build_id, int) or build_id >= current_build_id:
            continue
        if build.get("reason") not in _BASELINE_REASONS:
            continue
        source_version = build.get("sourceVersion")
        if isinstance(source_version, str) and _SHA_RE.match(source_version.lower()):
            candidates.append((build_id, source_version.lower()))
    if not candidates:
        return None
    return max(candidates, key=lambda item: item[0])[1]


def _parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Resolve the post-merge delta build commit range.")
    parser.add_argument("--definition-id", type=int, required=True, help="Build definition (pipeline) id.")
    parser.add_argument("--current-build-id", type=int, required=True, help="Id of the running build.")
    parser.add_argument("--branch", required=True, help="Full source branch ref, e.g. refs/heads/4.0.")
    parser.add_argument("--source-commit", required=True, help="The triggering commit SHA (Build.SourceVersion).")
    parser.add_argument("--repo-uri", required=True, help="Remote URL to fetch commit objects from.")
    parser.add_argument("--top", type=int, default=20, help="How many recent builds to inspect.")
    return parser.parse_args()


def main() -> int:
    """Resolve the range, print it to stdout, and return a process exit code."""
    args = _parse_args()

    source_commit = str(args.source_commit).strip().lower()
    if not _SHA_RE.match(source_commit):
        _log(f"ERROR: --source-commit is not a 40-character hex SHA: {source_commit!r}")
        return 1

    repo_uri = str(args.repo_uri)
    target_commit: str | None = None

    try:
        conn = ado_rest.AdoConnection.from_env()
        builds = ado_rest.list_builds(
            conn,
            definition_id=args.definition_id,
            branch_name=args.branch,
            top=args.top,
        )
        target_commit = _select_baseline(builds, args.current_build_id)
    except ado_rest.AdoRestError as exc:
        _log(f"WARNING: Could not query previous builds ({exc}); falling back to source^1.")

    if target_commit is None:
        _log(
            "WARNING: No previous CI build found for this branch; building only "
            "the tip commit (target = source^1). The weekly true-up job covers "
            "any gap."
        )
        target_commit = _parent_commit(source_commit, repo_uri)
        if target_commit is None:
            _log("ERROR: Unable to determine a parent of the source commit; cannot compute a build range.")
            return 1
        _emit_range(source_commit, target_commit)
        return 0

    # Make both endpoints available for the downstream tree diff in the
    # change-set step. Best-effort: a fetch failure is surfaced as a warning
    # rather than failing this best-effort pipeline outright.
    if not _ensure_commit(target_commit, repo_uri) or not _ensure_commit(source_commit, repo_uri):
        _log(
            f"WARNING: Could not make both commits available locally (target={target_commit}, "
            f"source={source_commit}); the change-set step may be unable to diff them."
        )

    _emit_range(source_commit, target_commit)
    return 0


if __name__ == "__main__":
    sys.exit(main())
