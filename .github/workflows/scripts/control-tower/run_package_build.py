"""Submit a package-build job to the Control Tower service and wait briefly.

Flow:
    1. Read the changed-components JSON.
    2. Filter to the build set: ``changeType in {added, changed}`` -- any
       component whose inputs changed needs a rebuild, regardless of whether
       its ``sourcesChange`` flag is set.
    3. POST ``/api/Scenario/package`` with the build request.
    4. Poll briefly (default 5 min) until the job reaches a terminal state
       (success or failure) or the local timeout expires. The goal is to
       catch jobs that fail immediately on submission, not to wait for the
       full build -- a non-terminal status at timeout is treated as
       acceptance and the build continues async.
    5. Exit 0 if the job started (or completed). Exit 1 only on submission
       failure or immediate terminal failure.
"""

import argparse
import json
import sys
from pathlib import Path

from azure.identity import DefaultAzureCredential

import client as ct


def _load_build_components(path: Path) -> list[str]:
    """Filter the ``azldev component changed`` JSON to the build set.

    The build set is every component with ``changeType`` in ``{added, changed}``
    — these are the components whose inputs differ between source and target
    and therefore need a rebuild. Unlike the upload set, we do NOT filter on
    ``sourcesChange`` here: a component can need a rebuild even if its source
    tarballs didn't change (e.g. an overlay or build-config change).

    Deleted components are excluded — there is nothing to build.
    """
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

    build_change_types = {"added", "changed"}
    components: list[str] = []
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        if entry.get("changeType") in build_change_types:
            name = entry.get("component")
            if isinstance(name, str) and name:
                components.append(name)

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
        help="ADO build reason (PullRequest, IndividualCI, ...). Used for the "
        "local skip guard -- package builds are not submitted for PR triggers.",
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
        "to explicitly say they want a persisted artifact.",
    )
    parser.add_argument(
        "--poll-interval-seconds",
        type=int,
        default=10,
        help="How often to poll the job status endpoint (default: 10).",
    )
    parser.add_argument(
        "--poll-timeout-seconds",
        type=int,
        default=600,
        help=(
            "Maximum time to wait for the job to reach a terminal state "
            "(default: 600 = 10 min). This is NOT the build timeout -- we "
            "just want to catch jobs that fail immediately on submission. "
            "A non-terminal status at timeout is treated as acceptance."
        ),
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

    components = _load_build_components(args.changed_components_file)

    base_url = args.api_base_url.rstrip("/")

    if args.build_reason == "PullRequest":
        print(
            "Skipping Control Tower call -- pull request triggers do not submit "
            "package builds (unmerged code should not consume build capacity)."
        )
        return

    if not components:
        print("No components need a rebuild -- skipping package-build submission.")
        return

    # ── Build payload ────────────────────────────────────────────────
    payload: dict = {
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

    # ── Brief poll — just confirm the job was accepted ───────────────
    print(
        f"Polling job {job_id} for up to {args.poll_timeout_seconds}s to confirm "
        f"acceptance (not waiting for full build completion)..."
    )
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
        # We don't wait for full build completion -- the goal of this poll
        # is just to surface a fast-failing job. A non-terminal status at
        # the timeout is acceptance enough; the build continues async and
        # is monitored in the Control Tower UI.
        last_status = final.get("status", "Unknown")
        print(
            f"Job {job_id} still in non-terminal status '{last_status}' "
            f"after {args.poll_timeout_seconds}s -- build accepted. "
            f"Monitor progress in the Control Tower UI."
        )
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
