"""Submit a package-build job to the Control Tower service and wait briefly.

Flow:
    1. Read the changed-components JSON; an unrecognized ``changeType`` fails
       the check closed.
    2. Filter to the build set: ``changeType in {added, changed}`` -- any
       component whose inputs changed needs a rebuild, regardless of whether
       its ``sourcesChange`` flag is set.
    3. POST ``/api/Scenario/package`` with the build request.
    4. Poll until the job reaches a terminal state (success or failure) or the
       poll timeout expires. Two modes:
         * default (acceptance): poll briefly just to catch jobs that fail on
           submission; a non-terminal status at timeout is treated as
           acceptance and the build continues asynchronously.
         * --wait-for-completion: poll for the full build; a non-terminal
           status at timeout is a failure (for gating checks that must see the
           build verdict before passing).
    5. Exit 0 on success (or acceptance in the default mode); exit 1 on
       submission failure, terminal build failure, or -- with
       --wait-for-completion -- if the build does not finish within the timeout.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import client as ct
from azure.identity import DefaultAzureCredential


def _load_build_components(path: Path) -> list[str]:
    """Filter the ``azldev component changed`` JSON to the build set.

    The build set is every component with ``changeType`` in ``{added, changed}``
    -- these are the components whose inputs differ between source and target
    and therefore need a rebuild. Unlike the upload set, we do NOT filter on
    ``sourcesChange`` here: a component can need a rebuild even if its source
    tarballs didn't change (e.g. an overlay or build-config change).

    Deleted components are excluded — there is nothing to build.
    """
    known_change_types = {"added", "changed", "unchanged", "deleted"}
    build_change_types = {"added", "changed"}

    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"##[error]Failed to read --changed-components-file {path!s}: {exc}")
        raise SystemExit(1) from exc

    try:
        entries = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(f"##[error]--changed-components-file {path!s} is not valid JSON: {exc}")
        raise SystemExit(1) from exc

    if not isinstance(entries, list):
        print(
            f"##[error]--changed-components-file {path!s} top-level value "
            f"must be a JSON array (got {type(entries).__name__})."
        )
        raise SystemExit(1)

    components: list[str] = []
    for entry in entries:
        change_type = entry.get("changeType")
        if change_type not in known_change_types:
            print(
                f"##[error]--changed-components-file {path!s} has an unrecognized "
                f"changeType {change_type!r} (known: {sorted(known_change_types)}); "
                "refusing to guess the build set."
            )
            raise SystemExit(1)
        if change_type in build_change_types:
            components.append(entry["component"])

    return sorted(set(components))


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Submit a package-build job to the Control Tower service.",
    )
    parser.add_argument(
        "--api-audience",
        required=True,
        help="Entra ID audience URI (e.g. api://<client-id>)",
    )
    parser.add_argument(
        "--api-base-url",
        required=True,
        help="Base URL of the Control Tower service",
    )
    parser.add_argument(
        "--build-reason",
        required=True,
        help="ADO build reason (PullRequest, IndividualCI, ...). A PullRequest "
        "may submit a SCRATCH build, but an official (persisted) build is "
        "refused for a PullRequest.",
    )
    parser.add_argument(
        "--changed-components-file",
        required=True,
        type=Path,
        help="Path to the raw JSON output of 'azldev component changed -a -O json'.",
    )
    parser.add_argument(
        "--package-target",
        required=True,
        help="Package target identifier (e.g. 'azl4').",
    )
    parser.add_argument(
        "--repo-uri",
        required=True,
        help="Upstream repository URI.",
    )
    parser.add_argument(
        "--commit-sha",
        default=None,
        help="Source commit SHA to build from.",
    )
    parser.add_argument(
        "--branch",
        default=None,
        help="Source branch name (alternative to --commit-sha).",
    )
    parser.add_argument(
        "--official-build",
        action="store_true",
        default=False,
        help="Submit as a non-scratch (official, persisted) build. The default "
        "is to submit a scratch build -- official is opt-in so the caller has "
        "to explicitly say they want a persisted artifact. Official builds are "
        "rejected for PullRequest triggers (unmerged code must never persist).",
    )
    parser.add_argument(
        "--poll-timeout-seconds",
        type=int,
        default=600,
        help=(
            "Maximum time to wait for the job to reach a terminal state "
            "(default: 600 = 10 min). In the default acceptance mode this just "
            "catches jobs that fail immediately on submission. With "
            "--wait-for-completion, set this to the full build budget -- a "
            "non-terminal status at timeout then fails the run."
        ),
    )
    parser.add_argument(
        "--wait-for-completion",
        action="store_true",
        default=False,
        help="Block until the build reaches a terminal state (success or "
        "failure) and exit accordingly; a non-terminal status at "
        "--poll-timeout-seconds becomes a failure. Used by gating checks (the "
        "PR package-build pipeline). The default fire-and-forget mode instead "
        "treats a timeout as acceptance.",
    )
    return parser.parse_args()


def _build_payload(args: argparse.Namespace, components: list[str]) -> dict[str, object]:
    """Assemble the Control Tower ``package`` scenario request body."""
    payload: dict[str, object] = {
        "repoUri": args.repo_uri,
        "packageTarget": args.package_target,
        "packages": components,
        "isScratchBuild": not args.official_build,
        "buildReason": args.build_reason,
    }
    if args.commit_sha is not None:
        payload["commitSha"] = args.commit_sha
    if args.branch is not None:
        payload["branch"] = args.branch
    return payload


def _handle_non_terminal(args: argparse.Namespace, job_id: str, final: dict[str, object]) -> None:
    """Handle a poll that ended before the job reached a terminal state.

    With --wait-for-completion this is a failure (a gating run must see the
    build verdict); otherwise the non-terminal status is treated as acceptance
    and the build continues asynchronously.
    """
    last_status = final.get("status", "Unknown")
    if args.wait_for_completion:
        print(
            f"##[error]Job {job_id} did not reach a terminal state within "
            f"{args.poll_timeout_seconds}s (last status '{last_status}') -- failing the check."
        )
        sys.exit(1)
    print(
        f"Job {job_id} still in non-terminal status '{last_status}' "
        f"after {args.poll_timeout_seconds}s -- build accepted. "
        f"Monitor progress in the Control Tower UI."
    )


def main() -> None:
    """Submit a package build to Control Tower and (optionally) wait for the verdict."""
    args = _parse_args()

    if args.poll_timeout_seconds <= 0:
        print("##[error]--poll-timeout-seconds must be a positive integer.")
        sys.exit(2)

    components = _load_build_components(args.changed_components_file)

    base_url = args.api_base_url.rstrip("/")

    # Unmerged PR code may only produce a throwaway scratch build; an official
    # (persisted) build of a pull request must never happen. Scratch PR builds
    # ARE allowed -- the PR package-build check relies on them, and capacity is
    # bounded by the reviewer-gated pipeline trigger, not here.
    if args.build_reason == "PullRequest" and args.official_build:
        print(
            "##[error]Refusing to submit an official (persisted) build for a "
            "pull request -- unmerged code must never produce official artifacts."
        )
        sys.exit(1)

    if not components:
        print("No components need a rebuild -- skipping package-build submission.")
        return

    # ── Build payload ────────────────────────────────────────────────
    payload = _build_payload(args, components)

    print("Calling Control Tower 'package' endpoint...")
    print("Payload:")
    print(json.dumps(payload, indent=2))

    # ── Acquire bearer token ─────────────────────────────────────────
    credential = DefaultAzureCredential()
    token_holder = ct.TokenHolder(token=ct.get_token(credential, args.api_audience))

    session = ct.make_session()

    # ── Submit build ─────────────────────────────────────────────────
    try:
        build_response = ct.post_scenario(
            session,
            base_url,
            "/api/Scenario/package",
            credential,
            args.api_audience,
            token_holder,
            payload,
            context="package-build",
        )
    except RuntimeError as exc:
        print(f"##[error]{exc}")
        sys.exit(1)

    print("package-build response:")
    print(json.dumps(build_response, indent=2, default=str))

    job_id = build_response.get("jobId")
    if not job_id:
        print("##[error]Control Tower 'package' response did not include a 'jobId'. Cannot confirm job acceptance.")
        sys.exit(1)

    # ── Poll for a terminal status ─────────────────────────────────
    print(f"Polling job {job_id} for up to {args.poll_timeout_seconds}s for a terminal status...")
    try:
        final, timed_out = ct.poll_until_terminal(
            session,
            base_url,
            credential,
            args.api_audience,
            token_holder,
            job_id,
            args.poll_timeout_seconds,
        )
    except RuntimeError as exc:
        print(f"##[error]{exc}")
        sys.exit(1)

    if timed_out:
        _handle_non_terminal(args, job_id, final)
        return

    ct.print_final_status(final)

    status = final.get("status")
    if status == ct.SUCCESS_STATUS:
        print(f"Control Tower build job {job_id} completed successfully.")
        return

    # Terminal failure -- the job was accepted but failed immediately.
    ct.report_failure(final)
    sys.exit(1)


if __name__ == "__main__":
    main()
