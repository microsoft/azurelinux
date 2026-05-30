"""Call the Control Tower 'prcheck' API and wait for the resulting job to finish.

Flow:
    1. POST ``/api/Scenario/prcheck`` with the PR context. The service responds
       with a ``WorkflowJobStatusDto`` describing the job it just queued.
    2. Poll ``/api/Workflow/jobs/status/{jobId}`` until the job reaches a
       terminal state (Completed / Failed / Cancelled / CancelledByAdmin /
       TimedOut / Unknown) or the local poll timeout elapses.
    3. Exit 0 only if the terminal status is ``Completed``; otherwise surface
       the error details from the job status payload and exit 1.

Component selection:
    Pass either ``--components`` (comma-separated names) OR
    ``--changed-components-file`` (path to the raw JSON output of
    ``azldev component changed -a -O json``). With the file form, only
    components whose ``sourcesChange`` is ``true`` and ``changeType`` is
    in ``{added, changed}`` are forwarded -- those are the ones whose
    lookaside tarballs need to be (re-)uploaded.
"""

import argparse
import json
import sys
from pathlib import Path

from azure.identity import DefaultAzureCredential

import client as ct


def _parse_components(value: str) -> list[str]:
    """Parse a comma-separated string into a list of stripped, non-empty names."""
    return [c.strip() for c in value.split(",") if c.strip()]


def _load_components_from_file(path: Path) -> list[str]:
    """Filter the raw ``azldev component changed`` JSON down to the upload set.

    The "upload set" is every component whose rendered ``sources`` file
    changed between the two refs (``sourcesChange == true``) AND whose
    ``changeType`` is in the allow-list ``{added, changed}``. Using an
    allow-list (rather than just excluding ``deleted``) mirrors the
    pipeline's consistency tripwire and ensures any future unknown
    ``changeType`` value fails closed rather than being forwarded to
    Control Tower.
    """
    ALLOWED_UPLOAD_TYPES = {"added", "changed"}

    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise SystemExit(f"##[error]Failed to read --changed-components-file {path!s}: {exc}") from exc

    try:
        entries = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"##[error]--changed-components-file {path!s} is not valid JSON: {exc}") from exc

    if not isinstance(entries, list):
        raise SystemExit(
            f"##[error]--changed-components-file {path!s} top-level value "
            f"must be a JSON array (got {type(entries).__name__})."
        )

    components: list[str] = []
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        if entry.get("changeType") not in ALLOWED_UPLOAD_TYPES:
            continue
        if entry.get("sourcesChange") is True:
            name = entry.get("component")
            if isinstance(name, str) and name:
                components.append(name)

    return sorted(set(components))


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Call the Control Tower prcheck API and wait for the job to finish.",
    )
    parser.add_argument(
        "--api-audience",
        required=True,
        help="Entra ID audience URI (e.g. api://<client-id>)",
    )
    parser.add_argument("--api-base-url", required=True, help="Base URL of the Control Tower service")
    parser.add_argument(
        "--build-reason",
        required=True,
        help="ADO build reason (PullRequest, IndividualCI, …)",
    )

    components_group = parser.add_mutually_exclusive_group(required=True)
    components_group.add_argument(
        "--components",
        type=_parse_components,
        help="Comma-separated list of affected component names",
    )
    components_group.add_argument(
        "--changed-components-file",
        type=Path,
        help=(
            "Path to the raw JSON output of 'azldev component changed -a -O json'. "
            "Forwards only entries with sourcesChange == true and "
            "changeType in {added, changed}."
        ),
    )

    parser.add_argument("--source-commit", default=None, help="Source commit SHA")
    parser.add_argument(
        "--source-branch",
        default=None,
        help="Source branch name (alternative to --source-commit)",
    )
    parser.add_argument("--target-commit", default=None, help="Target commit SHA")
    parser.add_argument(
        "--target-branch",
        default=None,
        help="Target branch name (alternative to --target-commit)",
    )
    parser.add_argument("--repo-uri", required=True, help="Upstream repository URI")
    parser.add_argument(
        "--poll-interval-seconds",
        type=int,
        default=10,
        help="How often to poll the job status endpoint (default: 10).",
    )
    parser.add_argument(
        "--poll-timeout-seconds",
        type=int,
        default=7200,
        help="Maximum time to wait for the job to reach a terminal state (default: 7200 = 2h).",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()

    if args.poll_interval_seconds <= 0:
        print("##[error]--poll-interval-seconds must be a positive integer.")
        sys.exit(2)
    if args.poll_timeout_seconds <= 0:
        print("##[error]--poll-timeout-seconds must be a positive integer.")
        sys.exit(2)

    components: list[str]
    if args.changed_components_file is not None:
        components = _load_components_from_file(args.changed_components_file)
    else:
        components = args.components

    # Normalize the base URL to avoid accidental double slashes if it was
    # configured with a trailing '/'.
    base_url = args.api_base_url.rstrip("/")

    # ── Build payload ────────────────────────────────────────────────
    payload: dict = {
        "components": components,
        "buildReason": args.build_reason,
        "repoUri": args.repo_uri,
    }
    if args.source_commit is not None:
        payload["sourceCommitSha"] = args.source_commit
    if args.source_branch is not None:
        payload["sourceBranch"] = args.source_branch
    if args.target_commit is not None:
        payload["targetCommitSha"] = args.target_commit
    if args.target_branch is not None:
        payload["targetBranch"] = args.target_branch

    print("Calling Control Tower 'prcheck' endpoint...")
    print("Payload:")
    print(json.dumps(payload, indent=2))

    if args.build_reason == "PullRequest":
        print("Skipping Control Tower call - pull request triggers are not supported, yet.")
        return

    if not components:
        print("No affected components detected between source and target commits; skipping Control Tower call.")
        return

    # ── Acquire bearer token ─────────────────────────────────────────
    credential = DefaultAzureCredential()
    token_holder = ct.TokenHolder(token=ct.get_token(credential, args.api_audience))

    session = ct.make_session()

    # ── Call prcheck API ─────────────────────────────────────────────
    try:
        prcheck_response = ct.post_scenario(
            session,
            base_url,
            "/api/Scenario/prcheck",
            credential,
            args.api_audience,
            token_holder,
            payload,
            context="prcheck",
        )
    except RuntimeError as exc:
        print(f"##[error]{exc}")
        sys.exit(1)

    print("prcheck response:")
    print(json.dumps(prcheck_response, indent=2, default=str))

    job_id = prcheck_response.get("jobId")
    if not job_id:
        print("##[error]Control Tower 'prcheck' response did not include a 'jobId'. Cannot poll for job status.")
        sys.exit(1)

    # ── Poll for job completion ──────────────────────────────────────
    print(f"Polling job {job_id} every {args.poll_interval_seconds}s (timeout {args.poll_timeout_seconds}s)...")
    try:
        final, timed_out = ct.poll_until_terminal(
            session,
            base_url,
            credential,
            args.api_audience,
            token_holder,
            job_id,
            args.poll_interval_seconds,
            args.poll_timeout_seconds,
        )
    except RuntimeError as exc:
        print(f"##[error]{exc}")
        sys.exit(1)

    if timed_out:
        # prcheck must run to terminal; timeout = failure regardless of last status.
        last_status = final.get("status", "Unknown")
        print(
            f"##[error]Timed out locally after {args.poll_timeout_seconds}s "
            f"waiting for job {job_id} to finish (last status: {last_status}). "
            f"Inspect the job in Control Tower."
        )
        sys.exit(1)

    ct.print_final_status(final)

    status = final.get("status")
    if status == ct.SUCCESS_STATUS:
        print(f"Control Tower job {job_id} completed successfully.")
        return

    ct.report_failure(final)
    sys.exit(1)


if __name__ == "__main__":
    main()
