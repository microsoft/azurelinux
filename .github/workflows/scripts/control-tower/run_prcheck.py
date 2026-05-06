"""Call the Control Tower 'prcheck' API and wait for the resulting job to finish.

Flow:
    1. POST ``/api/Scenario/prcheck`` with the PR context. The service responds
       with a ``WorkflowJobStatusDto`` describing the job it just queued.
    2. Poll ``/api/Workflow/jobs/status/{jobId}`` until the job reaches a
       terminal state (Completed / Failed / Cancelled / CancelledByAdmin /
       TimedOut / Unknown) or the local poll timeout elapses.
    3. Exit 0 only if the terminal status is ``Completed``; otherwise surface
       the error details from the job status payload and exit 1.
"""

import argparse
import json
import sys

from azure.identity import DefaultAzureCredential

import client as ct


def _parse_components(value: str) -> list[str]:
    """Parse a comma-separated string into a list of stripped, non-empty names."""
    return [c.strip() for c in value.split(",") if c.strip()]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Call the Control Tower prcheck API and wait for the job to finish.",
    )
    parser.add_argument(
        "--api-audience",
        required=True,
        help="Entra ID audience URI (e.g. api://<client-id>)",
    )
    parser.add_argument(
        "--api-base-url", required=True, help="Base URL of the Control Tower service"
    )
    parser.add_argument(
        "--build-reason",
        required=True,
        help="ADO build reason (PullRequest, IndividualCI, …)",
    )

    parser.add_argument(
        "--components",
        required=True,
        type=_parse_components,
        help="Comma-separated list of affected component names",
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

    components: list[str] = args.components

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
        print(
            "Skipping Control Tower call - pull request triggers are not supported, yet."
        )
        return

    if not components:
        print(
            "No affected components detected between source and target commits; "
            "skipping Control Tower call."
        )
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
        print(
            "##[error]Control Tower 'prcheck' response did not include a 'jobId'. "
            "Cannot poll for job status."
        )
        sys.exit(1)

    # ── Poll for job completion ──────────────────────────────────────
    print(
        f"Polling job {job_id} every {args.poll_interval_seconds}s "
        f"(timeout {args.poll_timeout_seconds}s)..."
    )
    try:
        final = ct.poll_until_terminal(
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

    if final is None:
        # Local timeout — job may still be running on the service side.
        print(
            f"##[error]Timed out locally after {args.poll_timeout_seconds}s "
            f"waiting for job {job_id} to finish. Inspect the job in Control Tower."
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
