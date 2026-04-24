"""Call the Control Tower prcheck API and wait for the resulting job to finish.

Flow:
    1. POST ``/api/Scenario/prcheck`` with the PR context. The service responds
       with a ``WorkflowJobStatusDto`` describing the job it just queued.
    2. Poll ``/api/Workflow/jobs/status/{jobId}`` until the job reaches a
       terminal state (Completed / Failed / Cancelled / CancelledByAdmin /
       TimedOut / Unknown) or the local poll timeout elapses.
    3. Exit 0 only if the terminal status is ``Completed``; otherwise surface
       the error details from the job status payload and exit 1.

Authentication:
    Requires an active Azure CLI session (e.g. via an AzureCLI@2 pipeline
    task with a Workload Identity Federation service connection).
    ``DefaultAzureCredential`` discovers the session automatically.
"""

import argparse
import json
import sys
import time
from dataclasses import dataclass
from typing import Any, Optional

import requests
from azure.identity import DefaultAzureCredential
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# JobStatus values from the Control Tower service
# (azl-ControlTower/ControlTower/Shared/Models/Jobs/JobStatus.cs).
_NON_TERMINAL_STATUSES = frozenset({"Queued", "Pending", "Running"})
_SUCCESS_STATUS = "Completed"
_TERMINAL_FAILURE_STATUSES = frozenset(
    {"Failed", "Cancelled", "CancelledByAdmin", "Unknown", "TimedOut"}
)


@dataclass
class _TokenHolder:
    """Mutable bearer-token holder so helpers can observe in-place refreshes."""

    token: str


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


def _make_session() -> requests.Session:
    """Create a ``requests.Session`` with retries for idempotent GETs only.

    Retry budget is tuned to complete quickly relative to the 10s default poll
    interval: worst case ~7s of backoff (0.5 + 1 + 2 + 4s capped) across 3
    attempts on 429/5xx.
    """
    session = requests.Session()
    retry = Retry(
        total=3,
        connect=3,
        read=3,
        status=3,
        backoff_factor=0.5,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset({"GET"}),
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def _get_token(credential: DefaultAzureCredential, audience: str) -> str:
    """Acquire a bearer token for the given audience."""
    return credential.get_token(f"{audience}/.default").token


def _auth_headers(token: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def _format_error(response: requests.Response) -> str:
    """Render a detailed diagnostic string for a failed CT response.

    Tolerates the three error shapes used by Control Tower:
      * Global middleware: ``{"error", "correlationId", "timestamp"}``
      * Controller-returned errors: ``{"message": "..."}``
      * ASP.NET validation: ``{"title", "errors": {field: [msg, ...]}}``
    """
    method = response.request.method if response.request is not None else "?"
    lines: list[str] = [
        f"HTTP {response.status_code} {response.reason} from {method} {response.url}"
    ]

    body: Any
    try:
        body = response.json()
    except ValueError:
        body = None

    matched_known_key = False
    if isinstance(body, dict):
        # Middleware shape.
        if "error" in body:
            lines.append(f"  error: {body['error']}")
            matched_known_key = True
        # Controller NotFound / explicit errors.
        if "message" in body:
            lines.append(f"  message: {body['message']}")
            matched_known_key = True
        # Validation errors.
        if "title" in body and body.get("title") != body.get("error"):
            lines.append(f"  title: {body['title']}")
            matched_known_key = True
        errors = body.get("errors")
        if isinstance(errors, dict) and errors:
            lines.append("  validation errors:")
            for field, messages in errors.items():
                if isinstance(messages, list):
                    for msg in messages:
                        lines.append(f"    - {field}: {msg}")
                else:
                    lines.append(f"    - {field}: {messages}")
            matched_known_key = True
        correlation_id = body.get("correlationId") or body.get("traceId")
        if correlation_id:
            lines.append(f"  correlationId: {correlation_id}")

    # Only dump the raw body when structured parsing found nothing useful —
    # this keeps logs readable in the common case while preserving forensics
    # when CT returns an unexpected shape.
    if not matched_known_key:
        raw = response.text or ""
        if raw:
            truncated = raw if len(raw) <= 4000 else raw[:4000] + "... [truncated]"
            lines.append("  raw body:")
            for raw_line in truncated.splitlines() or [truncated]:
                lines.append(f"    {raw_line}")

    return "\n".join(lines)


def _request_with_refresh(
    session: requests.Session,
    method: str,
    url: str,
    credential: DefaultAzureCredential,
    audience: str,
    token_holder: _TokenHolder,
    *,
    json_payload: Optional[dict] = None,
) -> requests.Response:
    """Issue a request. On a 401, refresh the bearer token once and retry."""
    response = session.request(
        method,
        url,
        headers=_auth_headers(token_holder.token),
        json=json_payload,
        timeout=(10, 60),
    )
    if response.status_code == 401:
        print(
            "Bearer token rejected (401) — refreshing and retrying once...", flush=True
        )
        token_holder.token = _get_token(credential, audience)
        response = session.request(
            method,
            url,
            headers=_auth_headers(token_holder.token),
            json=json_payload,
            timeout=(10, 60),
        )
    return response


def _parse_json_object(response: requests.Response, context: str) -> dict:
    """Parse ``response`` body as a JSON object, raising on non-object payloads."""
    try:
        body = response.json()
    except ValueError as exc:
        raise RuntimeError(
            f"{context} returned HTTP {response.status_code} "
            f"but the body was not valid JSON:\n{response.text}"
        ) from exc
    if not isinstance(body, dict):
        raise RuntimeError(
            f"{context} returned HTTP {response.status_code} with a non-object "
            f"JSON body (expected an object):\n{response.text}"
        )
    return body


def _post_prcheck(
    session: requests.Session,
    base_url: str,
    credential: DefaultAzureCredential,
    audience: str,
    token_holder: _TokenHolder,
    payload: dict,
) -> dict:
    """POST the prcheck request and return the parsed response dict."""
    url = f"{base_url}/api/Scenario/prcheck"
    response = _request_with_refresh(
        session, "POST", url, credential, audience, token_holder, json_payload=payload
    )
    if not response.ok:
        raise RuntimeError(
            "Control Tower 'prcheck' request failed.\n" + _format_error(response)
        )
    return _parse_json_object(response, "Control Tower 'prcheck'")


def _get_job_status(
    session: requests.Session,
    base_url: str,
    credential: DefaultAzureCredential,
    audience: str,
    token_holder: _TokenHolder,
    job_id: str,
) -> dict:
    """GET the job status. Refreshes the bearer token on 401 and retries once."""
    url = f"{base_url}/api/Workflow/jobs/status/{job_id}"
    response = _request_with_refresh(
        session, "GET", url, credential, audience, token_holder
    )
    if not response.ok:
        raise RuntimeError(
            "Control Tower job status request failed.\n" + _format_error(response)
        )
    return _parse_json_object(response, "Control Tower job status")


def _summarize_tasks(tasks: Any) -> str:
    """Return a compact one-line summary of task statuses (e.g. ``3/5 Completed``)."""
    if not isinstance(tasks, list) or not tasks:
        return ""
    total = len(tasks)
    counts: dict[str, int] = {}
    for task in tasks:
        if isinstance(task, dict):
            status = task.get("status", "Unknown")
            counts[status] = counts.get(status, 0) + 1
    parts = ", ".join(f"{count} {status}" for status, count in sorted(counts.items()))
    return f"{total} tasks ({parts})"


def _poll_job_until_terminal(
    session: requests.Session,
    base_url: str,
    credential: DefaultAzureCredential,
    audience: str,
    token_holder: _TokenHolder,
    job_id: str,
    poll_interval_seconds: int,
    poll_timeout_seconds: int,
) -> Optional[dict]:
    """Poll the job status until it reaches a terminal state or the timeout expires.

    Returns the final status dict, or ``None`` if the local timeout was hit
    before the job reached a terminal state.
    """
    start = time.monotonic()
    deadline = start + poll_timeout_seconds
    previous_status: Optional[str] = None
    job_status_object: Optional[dict] = None

    while True:
        job_status_object = _get_job_status(
            session, base_url, credential, audience, token_holder, job_id
        )
        current_status = job_status_object.get("status", "Unknown")
        elapsed = int(time.monotonic() - start)

        if current_status != previous_status:
            task_summary = _summarize_tasks(job_status_object.get("tasks"))
            transition = (
                f"{previous_status} -> {current_status}" if previous_status is not None else current_status
            )
            suffix = f" | {task_summary}" if task_summary else ""
            print(
                f"Job {job_id} status: {transition} (elapsed {elapsed}s){suffix}",
                flush=True,
            )
            previous_status = current_status
        else:
            # Heartbeat so the user can see the script is alive and still polling.
            print(
                f"[heartbeat] waiting on job {job_id}, status={current_status}, elapsed={elapsed}s",
                flush=True,
            )

        if current_status not in _NON_TERMINAL_STATUSES:
            return job_status_object

        remaining = deadline - time.monotonic()
        if remaining <= 0:
            print(
                f"##[warning]Local poll timeout of {poll_timeout_seconds}s reached "
                f"while job {job_id} was still in status '{current_status}'."
            )
            return None

        time.sleep(min(poll_interval_seconds, max(1, int(remaining))))


def _print_final_status(final: dict) -> None:
    """Pretty-print the final job status payload."""
    print("Final job status payload:")
    print(json.dumps(final, indent=2, default=str))


def _report_failure(final: dict) -> None:
    """Emit ADO-style error lines with the most actionable fields from ``final``."""
    status = final.get("status", "Unknown")
    error_message = final.get("errorMessage")
    job_id = final.get("jobId")

    print(f"##[error]Control Tower job {job_id} finished with status '{status}'.")
    if error_message:
        print(f"##[error]errorMessage: {error_message}")

    tasks = final.get("tasks")
    if isinstance(tasks, list):
        failed = [
            t
            for t in tasks
            if isinstance(t, dict) and t.get("status") in _TERMINAL_FAILURE_STATUSES
        ]
        for task in failed:
            name = task.get("taskName") or task.get("taskId")
            print(
                f"##[error]task '{name}' status={task.get('status')} "
                f"attempt={task.get('attemptNumber')}"
            )


def main() -> None:
    args = _parse_args()

    if args.poll_interval_seconds <= 0:
        print("##[error]--poll-interval-seconds must be a positive integer.")
        sys.exit(2)
    if args.poll_timeout_seconds <= 0:
        print("##[error]--poll-timeout-seconds must be a positive integer.")
        sys.exit(2)

    # Normalize base URL to avoid accidental double slashes if the operator
    # configured `ApiBaseUrl` with a trailing '/'.
    base_url = args.api_base_url.rstrip("/")

    # ── Build payload ────────────────────────────────────────────────
    payload: dict = {
        "components": args.components,
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

    if not args.components:
        print(
            "No affected components detected between source and target commits; "
            "skipping Control Tower call."
        )
        return

    # ── Acquire bearer token ─────────────────────────────────────────
    credential = DefaultAzureCredential()
    token_holder = _TokenHolder(token=_get_token(credential, args.api_audience))

    session = _make_session()

    # ── Call prcheck API ─────────────────────────────────────────────
    try:
        prcheck_response = _post_prcheck(
            session, base_url, credential, args.api_audience, token_holder, payload
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
        final = _poll_job_until_terminal(
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

    _print_final_status(final)

    status = final.get("status")
    if status == _SUCCESS_STATUS:
        print(f"Control Tower job {job_id} completed successfully.")
        return

    _report_failure(final)
    sys.exit(1)


if __name__ == "__main__":
    main()
