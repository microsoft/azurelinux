"""Shared HTTP client for Azure Linux Control Tower scenario calls.

Provides:
    * A retry-aware ``requests.Session``.
    * Bearer-token acquisition + transparent single-shot refresh on 401.
    * POST helpers for ``/api/Scenario/*`` endpoints.
    * Job-status polling against ``/api/Workflow/jobs/status/{jobId}``.
    * Diagnostic formatting that tolerates the three error shapes Control
      Tower returns (middleware, controller, ASP.NET validation).

Authentication:
    Requires an active Azure CLI session (e.g. via an ``AzureCLI@2`` pipeline
    task with a Workload Identity Federation service connection).
    ``DefaultAzureCredential`` discovers the session automatically.
"""

from __future__ import annotations

import json
import time
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from http import HTTPStatus
from typing import TYPE_CHECKING, cast

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

if TYPE_CHECKING:
    from azure.identity import DefaultAzureCredential

type JsonValue = None | bool | int | float | str | Sequence[JsonValue] | Mapping[str, JsonValue]
type JsonObject = dict[str, JsonValue]

# JobStatus values from the Control Tower service
# (azl-ControlTower/ControlTower/Shared/Models/Jobs/JobStatus.cs).
NON_TERMINAL_STATUSES = frozenset({"Queued", "Pending", "Running"})
SUCCESS_STATUS = "Completed"
TERMINAL_FAILURE_STATUSES = frozenset({"Failed", "Cancelled", "CancelledByAdmin", "Unknown", "TimedOut"})
# Statuses that END the poll. The poll exits ONLY on a status in this set;
# anything else is treated as still in progress (keep polling until a known
# terminal status or the local timeout). This way a newly-introduced Control
# Tower intermediate status (e.g. a future "Validating") is not misread as
# terminal and used to fail a build that is actually still starting. "Unknown"
# stays terminal on purpose: a missing/blank status is a real problem, not an
# unrecognized-but-valid new state.
TERMINAL_STATUSES = TERMINAL_FAILURE_STATUSES | {SUCCESS_STATUS}
_MAX_ERROR_BODY_CHARS = 4000


@dataclass
class TokenHolder:
    """Mutable bearer-token holder so helpers can observe in-place refreshes."""

    token: str


def make_session() -> requests.Session:
    """Create a ``requests.Session`` with retries for idempotent GETs only.

    6 retries with exponential backoff (0+4+8+16+32+64 = ~124 s, ~2 min worst
    case; Retry-After honored).
    """
    session = requests.Session()
    retry = Retry(
        total=6,
        connect=6,
        read=6,
        status=6,
        backoff_factor=2.0,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset({"GET"}),
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def get_token(credential: DefaultAzureCredential, audience: str) -> str:
    """Acquire a bearer token for the given audience."""
    return credential.get_token(f"{audience}/.default").token


def _auth_headers(token: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def _append_validation_errors(lines: list[str], errors: object) -> bool:
    """Append ASP.NET validation errors and report whether any were found."""
    if not isinstance(errors, dict) or not errors:
        return False

    lines.append("  validation errors:")
    for field, messages in errors.items():
        if isinstance(messages, list):
            lines.extend(f"    - {field}: {message}" for message in messages)
        else:
            lines.append(f"    - {field}: {messages}")
    return True


def format_error(response: requests.Response) -> str:
    """Render a detailed diagnostic string for a failed CT response.

    Tolerates the three error shapes used by Control Tower:
      * Global middleware: ``{"error", "correlationId", "timestamp"}``
      * Controller-returned errors: ``{"message": "..."}``
      * ASP.NET validation: ``{"title", "errors": {field: [msg, ...]}}``
    """
    method = response.request.method if response.request is not None else "?"
    lines: list[str] = [f"HTTP {response.status_code} {response.reason} from {method} {response.url}"]

    body: object
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
        if _append_validation_errors(lines, body.get("errors")):
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
            truncated = raw if len(raw) <= _MAX_ERROR_BODY_CHARS else raw[:_MAX_ERROR_BODY_CHARS] + "... [truncated]"
            lines.append("  raw body:")
            lines.extend(f"    {raw_line}" for raw_line in (truncated.splitlines() or [truncated]))

    return "\n".join(lines)


def _request_with_refresh(
    session: requests.Session,
    method: str,
    url: str,
    credential: DefaultAzureCredential,
    audience: str,
    token_holder: TokenHolder,
    *,
    json_payload: JsonObject | None = None,
) -> requests.Response:
    """Issue a request. On a 401, refresh the bearer token once and retry."""
    response = session.request(
        method,
        url,
        headers=_auth_headers(token_holder.token),
        json=json_payload,
        timeout=(10, 60),
    )
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        print(
            "Bearer token rejected (401) — refreshing and retrying once...",
            flush=True,
        )
        token_holder.token = get_token(credential, audience)
        response = session.request(
            method,
            url,
            headers=_auth_headers(token_holder.token),
            json=json_payload,
            timeout=(10, 60),
        )
    return response


def _parse_json_object(response: requests.Response, context: str) -> JsonObject:
    """Parse ``response`` body as a JSON object, raising on non-object payloads."""
    try:
        body = response.json()
    except ValueError as exc:
        message = f"{context} returned HTTP {response.status_code} but the body was not valid JSON:\n{response.text}"
        raise RuntimeError(message) from exc
    if not isinstance(body, dict):
        message = (
            f"{context} returned HTTP {response.status_code} with a non-object "
            f"JSON body (expected an object):\n{response.text}"
        )
        raise RuntimeError(message)  # noqa: TRY004 - a malformed remote response is an operational failure
    return cast("JsonObject", body)


def post_scenario(
    session: requests.Session,
    base_url: str,
    path: str,
    credential: DefaultAzureCredential,
    audience: str,
    token_holder: TokenHolder,
    payload: JsonObject,
    *,
    context: str,
) -> JsonObject:
    """POST a scenario request and return the parsed response dict.

    ``path`` is the API path (e.g. ``/api/Scenario/prcheck``) appended to
    ``base_url``. A leading ``/`` is added if missing. ``context`` is used in
    error messages to identify the call.
    """
    if not path.startswith("/"):
        path = "/" + path
    url = f"{base_url}{path}"
    response = _request_with_refresh(
        session,
        "POST",
        url,
        credential,
        audience,
        token_holder,
        json_payload=payload,
    )
    if not response.ok:
        raise RuntimeError(f"Control Tower '{context}' request failed.\n" + format_error(response))
    return _parse_json_object(response, f"Control Tower '{context}'")


def get_job_status(
    session: requests.Session,
    base_url: str,
    credential: DefaultAzureCredential,
    audience: str,
    token_holder: TokenHolder,
    job_id: str,
) -> JsonObject:
    """GET the job status. Refreshes the bearer token on 401 and retries once."""
    url = f"{base_url}/api/Workflow/jobs/status/{job_id}"
    response = _request_with_refresh(session, "GET", url, credential, audience, token_holder)
    if not response.ok:
        raise RuntimeError("Control Tower job status request failed.\n" + format_error(response))
    return _parse_json_object(response, "Control Tower job status")


def _summarize_tasks(tasks: object) -> str:
    """Return a compact one-line summary of task statuses (e.g. ``3/5 Completed``)."""
    if not isinstance(tasks, list) or not tasks:
        return ""
    total = len(tasks)
    counts: dict[str, int] = {}
    for task in tasks:
        if isinstance(task, dict):
            raw_status = task.get("status")
            status = raw_status if isinstance(raw_status, str) else "Unknown"
            counts[status] = counts.get(status, 0) + 1
    parts = ", ".join(f"{count} {status}" for status, count in sorted(counts.items()))
    return f"{total} tasks ({parts})"


# Adaptive poll cadence: (elapsed-seconds threshold, interval-seconds). Tight
# early so short jobs stay responsive; backs off for long builds so a multi-hour
# build does not flood the logs with heartbeats (a fixed 10s interval would be
# ~2160 polls over 6h). Beyond the last threshold, _POLL_MAX_INTERVAL_SECONDS.
_POLL_SCHEDULE: tuple[tuple[int, int], ...] = (
    (600, 10),  # first 10 min: every 10s
    (1200, 30),  # 10-20 min: every 30s
    (3600, 60),  # 20-60 min: every 60s
)
_POLL_MAX_INTERVAL_SECONDS = 120  # beyond 1 h: every 2 min


def _poll_interval_seconds(elapsed_seconds: float) -> int:
    """Return the poll interval for the given elapsed time (adaptive backoff)."""
    for threshold_seconds, interval_seconds in _POLL_SCHEDULE:
        if elapsed_seconds < threshold_seconds:
            return interval_seconds
    return _POLL_MAX_INTERVAL_SECONDS


def poll_until_terminal(
    session: requests.Session,
    base_url: str,
    credential: DefaultAzureCredential,
    audience: str,
    token_holder: TokenHolder,
    job_id: str,
    poll_timeout_seconds: int,
) -> tuple[JsonObject, bool]:
    """Poll the job status until it reaches a terminal state or the timeout expires.

    Returns ``(last_status_dict, timed_out)``:
      - ``timed_out == False``: the job reached a terminal state, last_status_dict
        is that final state.
      - ``timed_out == True``: the local timeout expired first, last_status_dict
        is the most recent non-terminal observation (caller can inspect
        ``status`` to distinguish "still Queued" from "Running").
    """
    start = time.monotonic()
    deadline = start + poll_timeout_seconds
    previous_status: str | None = None
    job_status_object: JsonObject = {}

    while True:
        job_status_object = get_job_status(session, base_url, credential, audience, token_holder, job_id)
        raw_status = job_status_object.get("status")
        current_status = raw_status if isinstance(raw_status, str) else "Unknown"
        elapsed = int(time.monotonic() - start)

        if current_status != previous_status:
            task_summary = _summarize_tasks(job_status_object.get("tasks"))
            transition = f"{previous_status} -> {current_status}" if previous_status is not None else current_status
            suffix = f" | {task_summary}" if task_summary else ""
            print(
                f"Job {job_id} status: {transition} (elapsed {elapsed}s){suffix}",
                flush=True,
            )
            # Surface schema drift: a status that is neither known-terminal nor
            # known-non-terminal means Control Tower introduced a state this
            # script doesn't know about. We keep polling (treat it as
            # non-terminal) so an in-flight build isn't failed, but warn so the
            # gap gets closed.
            if current_status not in TERMINAL_STATUSES and current_status not in NON_TERMINAL_STATUSES:
                print(
                    f"##[warning]Unrecognized job status '{current_status}' for job {job_id}; "
                    "treating it as non-terminal and continuing to poll. If Control Tower added a "
                    "new status, update NON_TERMINAL_STATUSES / TERMINAL_* in client.py.",
                    flush=True,
                )
            previous_status = current_status
        else:
            # Heartbeat so the user can see the script is alive and still polling.
            print(
                f"[heartbeat] waiting on job {job_id}, status={current_status}, elapsed={elapsed}s",
                flush=True,
            )

        # Exit ONLY on a known terminal status. An unrecognized status falls
        # through and keeps polling (bounded by the timeout) rather than being
        # misread as terminal -- which previously turned a still-starting build
        # red the moment Control Tower reported a status we didn't enumerate.
        if current_status in TERMINAL_STATUSES:
            return job_status_object, False

        remaining = deadline - time.monotonic()
        if remaining <= 0:
            print(
                f"##[warning]Local poll timeout of {poll_timeout_seconds}s reached "
                f"while job {job_id} was still in status '{current_status}'."
            )
            return job_status_object, True

        interval_seconds = _poll_interval_seconds(elapsed)
        time.sleep(min(interval_seconds, max(1, int(remaining))))


def print_final_status(final: JsonObject) -> None:
    """Pretty-print the final job status payload."""
    print("Final job status payload:")
    print(json.dumps(final, indent=2, default=str))


def report_failure(final: JsonObject) -> None:
    """Emit ADO-style error lines with the most actionable fields from ``final``."""
    status = final.get("status", "Unknown")
    error_message = final.get("errorMessage")
    job_id = final.get("jobId")

    print(f"##[error]Control Tower job {job_id} finished with status '{status}'.")
    if error_message:
        print(f"##[error]errorMessage: {error_message}")

    tasks = final.get("tasks")
    if isinstance(tasks, list):
        failed = [t for t in tasks if isinstance(t, dict) and t.get("status") in TERMINAL_FAILURE_STATUSES]
        for task in failed:
            name = task.get("taskName") or task.get("taskId")
            print(f"##[error]task '{name}' status={task.get('status')} attempt={task.get('attemptNumber')}")
