"""Resolve the ``(base, source)`` commit range for a post-merge delta build.

Strategy (see ``.github/workflows/ado/templates/steps/commit-range-postmerge.yml``):

* ``source`` is the commit that triggered this run (``Build.SourceVersion``).
* ``base`` is the ``sourceVersion`` of the immediately-preceding CI build of
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

Fallback (first run, or no prior CI build found): ``base = source^1``. That
run only builds the single tip commit's components, self-correcting on the next
push. Two distinct situations trigger this fallback and are NOT treated the
same: a successful query that simply found no prior build (benign -- a genuine
first run) is logged at INFO, whereas a query that *failed* (auth / network /
SDK misconfig) is actionable -- it would otherwise silently degrade every run to
a single-commit delta -- so it additionally emits ``baselineQueryFailed=true``
and the calling step raises a visible pipeline warning.

The resolved hashes are printed to stdout as two ``key=value`` lines
(``sourceCommit=<sha>`` and ``baseCommit=<sha>``), plus an optional
``baselineQueryFailed=true`` line when the build-history query failed. The
calling pipeline step reads them, sets the corresponding ADO pipeline variables,
and raises a warning on query failure -- so the variable wiring and the warning
both stay visible in the YAML rather than hidden here. All other diagnostic
output goes to stderr to keep stdout machine-readable.

This script is read-only with respect to git: it assumes the full history is
already present (the pipeline fetches it up front in a single "Ensure full git
history" step) and never fetches itself. A ``git fetch --depth=N`` here would
re-shallow a full clone -- a footgun, especially when running locally.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys

from azure.devops.connection import Connection  # pyright: ignore[reportMissingTypeStubs]
from azure.devops.exceptions import ClientException  # pyright: ignore[reportMissingTypeStubs]
from msrest.authentication import BasicAuthentication

# ADO predefined variables required to reach the control-plane REST API, read
# from the step environment.
_ENV_COLLECTION_URI = "SYSTEM_COLLECTIONURI"
_ENV_PROJECT = "SYSTEM_TEAMPROJECT"
_ENV_TOKEN = "SYSTEM_ACCESSTOKEN"  # noqa: S105 - env var NAME, not a secret value

# A build is eligible as a baseline only if it was itself a CI build of the
# branch. Manual / PR / scheduled runs are excluded so that a one-off manual
# test run of this pipeline cannot become the baseline for the next real CI
# build (which would skip everything in between).
_BASELINE_REASONS = frozenset({"individualCI", "batchedCI"})

_SHA_RE = re.compile(r"^[0-9a-f]{40}$")


def _log(message: str) -> None:
    """Print a diagnostic message to stderr, keeping stdout machine-readable."""
    print(message, file=sys.stderr)


def _emit_range(source_commit: str, base_commit: str, *, query_failed: bool = False) -> None:
    """Print the resolved range to stdout as ``key=value`` lines.

    The calling pipeline step parses these lines and sets the ``sourceCommit`` /
    ``baseCommit`` pipeline variables, so the variable wiring lives in the YAML
    rather than in this script. When ``query_failed`` is True an extra
    ``baselineQueryFailed=true`` line is emitted so the caller can raise a
    pipeline warning -- this marks the actionable "Builds API query failed" case
    and is deliberately NOT emitted for a benign "no prior build" first run.
    """
    _log(f"Resolved range: base={base_commit} source={source_commit}")
    print(f"sourceCommit={source_commit}")
    print(f"baseCommit={base_commit}")
    if query_failed:
        print("baselineQueryFailed=true")


def _run_git(args: list[str]) -> subprocess.CompletedProcess[str]:
    """Run a ``git`` command, capturing text output without raising on failure."""
    return subprocess.run(["git", *args], check=False, capture_output=True, text=True)


def _commit_present(commit: str) -> bool:
    """Return whether ``commit`` exists as a commit object in the local clone."""
    return _run_git(["cat-file", "-e", f"{commit}^{{commit}}"]).returncode == 0


def _parent_commit(commit: str) -> str | None:
    """Return ``commit^1`` (40-hex), or None if it cannot be resolved.

    Assumes full history is present (the pipeline fetches it up front), so no
    fetch is performed here.
    """
    result = _run_git(["rev-parse", "--verify", "--quiet", f"{commit}^1"])
    parent = result.stdout.strip()
    if result.returncode != 0 or not _SHA_RE.match(parent):
        return None
    return parent


def _fetch_recent_builds(*, definition_id: int, branch: str, top: int) -> list[object]:
    """Return recent builds for ``definition_id`` on ``branch`` via the ADO SDK.

    Authenticates with the pipeline's ``System.AccessToken`` (read from the
    environment) using the SDK's documented ``BasicAuthentication`` pattern; the
    Azure DevOps REST API accepts the job access token as a PAT-equivalent
    credential. This reads the pipeline's own build history on the ADO control
    plane, so the default project job-authorization scope is sufficient and the
    Workload Identity Federation service-connection rule does not apply.

    Args:
        definition_id: Build definition (pipeline) id to filter by.
        branch: Full source branch ref, e.g. ``refs/heads/4.0``.
        top: Maximum number of builds to return (most recent first).

    Returns:
        The list of ``Build`` objects returned by the SDK.

    Raises:
        RuntimeError: If a required environment variable is missing or empty.
    """
    missing = [name for name in (_ENV_COLLECTION_URI, _ENV_PROJECT, _ENV_TOKEN) if not os.environ.get(name)]
    if missing:
        msg = f"Missing required ADO environment variable(s): {', '.join(missing)}."
        raise RuntimeError(msg)
    credentials = BasicAuthentication("", os.environ[_ENV_TOKEN])
    connection = Connection(base_url=os.environ[_ENV_COLLECTION_URI], creds=credentials)
    build_client = connection.clients.get_build_client()
    return build_client.get_builds(
        os.environ[_ENV_PROJECT],
        definitions=[definition_id],
        branch_name=branch,
        top=top,
        query_order="queueTimeDescending",
    )


def _select_baseline(builds: list[object], current_build_id: int) -> str | None:
    """Pick the source commit of the immediately-preceding eligible CI build.

    Args:
        builds: ``Build`` objects from :func:`_fetch_recent_builds`.
        current_build_id: Id of the running build; only earlier builds qualify.

    Returns:
        The ``source_version`` of the highest-id eligible build, or None.
    """
    candidates: list[tuple[int, str]] = []
    for build in builds:
        build_id = getattr(build, "id", None)
        if not isinstance(build_id, int) or build_id >= current_build_id:
            continue
        if getattr(build, "reason", None) not in _BASELINE_REASONS:
            continue
        source_version = getattr(build, "source_version", None)
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
    parser.add_argument("--top", type=int, default=100, help="How many recent builds to inspect.")
    return parser.parse_args()


def main() -> int:
    """Resolve the range, print it to stdout, and return a process exit code."""
    args = _parse_args()

    source_commit = str(args.source_commit).strip().lower()
    if not _SHA_RE.match(source_commit):
        _log(f"ERROR: --source-commit is not a 40-character hex SHA: {source_commit!r}")
        return 1

    base_commit: str | None = None
    # Distinguish a *failed* build-history query (actionable) from a successful
    # query that simply found no prior build (benign). Only the former sets this.
    query_failed = False

    try:
        builds = _fetch_recent_builds(
            definition_id=args.definition_id,
            branch=args.branch,
            top=args.top,
        )
        base_commit = _select_baseline(builds, args.current_build_id)
    except (ClientException, OSError, RuntimeError) as exc:
        # The query itself failed (bad token scope, network, SDK misconfig).
        # Fall back to a single-commit delta so the run still makes progress,
        # but flag it so the caller surfaces a pipeline warning -- a broken
        # token would otherwise degrade EVERY run this way, silently.
        query_failed = True
        _log(f"WARNING: Could not query previous builds ({exc}); falling back to source^1.")

    if base_commit is None:
        if not query_failed:
            # Benign: the query succeeded but there is genuinely no prior CI
            # build (e.g. the first run on a new branch).
            _log(
                "INFO: No previous CI build found for this branch; building only "
                "the tip commit (base = source^1). The weekly true-up job covers "
                "any gap."
            )
        base_commit = _parent_commit(source_commit)
        if base_commit is None:
            _log("ERROR: Unable to determine a parent of the source commit; cannot compute a build range.")
            return 1
        _emit_range(source_commit, base_commit, query_failed=query_failed)
        return 0

    # Both endpoints must be present for the downstream tree diff in the
    # change-set step. Full history is fetched once by the pipeline before this
    # step runs, so we only sanity-check presence here (no fetching).
    missing = [commit for commit in (base_commit, source_commit) if not _commit_present(commit)]
    if missing:
        _log(
            f"WARNING: commit(s) not present locally: {', '.join(missing)}; the change-set step may be "
            "unable to diff them. Ensure the full git history was fetched before this step."
        )

    _emit_range(source_commit, base_commit)
    return 0


if __name__ == "__main__":
    sys.exit(main())
