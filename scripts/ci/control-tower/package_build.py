"""Shared mechanics for Control Tower package-build entry points."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import TYPE_CHECKING

import client as ct

if TYPE_CHECKING:
    from pathlib import Path

type ScenarioPayload = ct.JsonObject
type ChangeEntry = dict[str, object]


@dataclass(frozen=True, slots=True)
class ScenarioRequest:
    """Describe one caller-selected Control Tower scenario request."""

    context: str
    path: str
    payload: ScenarioPayload


def _load_change_entries(path: Path) -> list[ChangeEntry]:
    """Load and validate an azldev component change-set."""
    known_change_types = {"added", "changed", "unchanged", "deleted"}

    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"##[error]Failed to read --changed-components-file {path!s}: {exc}")
        raise SystemExit(1) from exc

    try:
        raw_entries = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(f"##[error]--changed-components-file {path!s} is not valid JSON: {exc}")
        raise SystemExit(1) from exc

    if not isinstance(raw_entries, list):
        print(
            f"##[error]--changed-components-file {path!s} top-level value "
            f"must be a JSON array (got {type(raw_entries).__name__})."
        )
        raise SystemExit(1)

    entries: list[ChangeEntry] = []
    for index, entry in enumerate(raw_entries):
        if not isinstance(entry, dict):
            print(
                f"##[error]--changed-components-file {path!s} entry {index} "
                f"must be a JSON object (got {type(entry).__name__})."
            )
            raise SystemExit(1)
        change_type = entry.get("changeType")
        if change_type not in known_change_types:
            print(
                f"##[error]--changed-components-file {path!s} has an unrecognized "
                f"changeType {change_type!r} (known: {sorted(known_change_types)}); "
                "refusing to guess the build set."
            )
            raise SystemExit(1)
        entries.append(entry)

    return entries


def load_build_components(path: Path) -> list[str]:
    """Load components that were added or changed from an azldev change-set."""
    build_change_types = {"added", "changed"}
    entries = _load_change_entries(path)

    components: list[str] = []
    for index, entry in enumerate(entries):
        change_type = entry.get("changeType")
        if change_type in build_change_types:
            component = entry.get("component")
            if not isinstance(component, str) or not component:
                print(
                    f"##[error]--changed-components-file {path!s} entry {index} "
                    f"must contain a non-empty string 'component' for changeType {change_type!r}."
                )
                raise SystemExit(1)
            components.append(component)

    return sorted(set(components))


def load_available_components(path: Path) -> set[str]:
    """Load components present in the candidate source tree."""
    entries = _load_change_entries(path)
    available: set[str] = set()
    for index, entry in enumerate(entries):
        change_type = entry["changeType"]
        if change_type == "deleted":
            continue
        component = entry.get("component")
        if not isinstance(component, str) or not component:
            print(
                f"##[error]--changed-components-file {path!s} entry {index} "
                f"must contain a non-empty string 'component' for changeType {change_type!r}."
            )
            raise SystemExit(1)
        available.add(component)
    return available


def load_deleted_components(path: Path) -> set[str]:
    """Load explicitly deleted components without requesting a rebuild."""
    deleted: set[str] = set()
    for index, entry in enumerate(_load_change_entries(path)):
        if entry["changeType"] != "deleted":
            continue
        component = entry.get("component")
        if not isinstance(component, str) or not component:
            print(
                f"##[error]--changed-components-file {path!s} entry {index} "
                "must contain a non-empty string 'component' for a deletion."
            )
            raise SystemExit(1)
        deleted.add(component)
    return deleted


def load_component_names(path: Path) -> list[str]:
    """Load a stable JSON array of unique component names."""
    try:
        raw = path.read_text(encoding="utf-8")
        entries = json.loads(raw)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"##[error]Failed to load component set {path!s}: {exc}")
        raise SystemExit(1) from exc
    if not isinstance(entries, list) or not all(
        isinstance(component, str) and component for component in entries
    ):
        print(f"##[error]Component set {path!s} must be a JSON array of non-empty strings.")
        raise SystemExit(1)
    if len(entries) != len(set(entries)):
        print(f"##[error]Component set {path!s} contains duplicate names.")
        raise SystemExit(1)
    return sorted(entries)


def submit_and_monitor(
    *,
    api_audience: str,
    api_base_url: str,
    request: ScenarioRequest,
    poll_timeout_seconds: int,
    wait_for_completion: bool,
) -> str:
    """Submit one package-build scenario and monitor its initial status."""
    if poll_timeout_seconds <= 0:
        print("##[error]--poll-timeout-seconds must be a positive integer.")
        raise SystemExit(2)

    print(f"Calling Control Tower '{request.context}' endpoint...")
    print("Payload:")
    print(json.dumps(request.payload, indent=2))

    base_url = api_base_url.rstrip("/")
    credential = ct.make_credential()
    token_holder = ct.TokenHolder(token=ct.get_token(credential, api_audience))
    session = ct.make_session()

    try:
        build_response = ct.post_scenario(
            session,
            base_url,
            request.path,
            credential,
            api_audience,
            token_holder,
            request.payload,
            context=request.context,
        )
    except RuntimeError as exc:
        print(f"##[error]{exc}")
        raise SystemExit(1) from exc

    print(f"{request.context} response:")
    print(json.dumps(build_response, indent=2, default=str))

    job_id = build_response.get("jobId")
    if not isinstance(job_id, str) or not job_id:
        print(
            f"##[error]Control Tower '{request.context}' response did not include a 'jobId'. "
            "Cannot confirm job acceptance."
        )
        raise SystemExit(1)

    print(f"Polling job {job_id} for up to {poll_timeout_seconds}s for a terminal status...")
    try:
        final, timed_out = ct.poll_until_terminal(
            session,
            base_url,
            credential,
            api_audience,
            token_holder,
            job_id,
            poll_timeout_seconds,
        )
    except RuntimeError as exc:
        print(f"##[error]{exc}")
        raise SystemExit(1) from exc

    if timed_out:
        last_status = final.get("status", "Unknown")
        if wait_for_completion:
            print(
                f"##[error]Job {job_id} did not reach a terminal state within "
                f"{poll_timeout_seconds}s (last status '{last_status}') -- failing the check."
            )
            raise SystemExit(1)
        print(
            f"Job {job_id} still in non-terminal status '{last_status}' "
            f"after {poll_timeout_seconds}s -- build accepted. "
            "Monitor progress in the Control Tower UI."
        )
        return job_id

    ct.print_final_status(final)

    if final.get("status") == ct.SUCCESS_STATUS:
        print(f"Control Tower build job {job_id} completed successfully.")
        return job_id

    ct.report_failure(final)
    raise SystemExit(1)
