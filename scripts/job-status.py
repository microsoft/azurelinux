#!/usr/bin/env python3
"""Analyze job status JSON and provide summary or list failed tasks.

Handles duplicate task sets (e.g. retries submitted as new tasks) by detecting
createTime clusters, and classifies failures as "real" (task ran long enough to
actually build) vs "timeout" (task killed almost instantly, typically from a
dependency cascade or job-level timeout).
"""

import argparse
import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

# Default: tasks that run less than this many seconds are considered
# timeout/cascade failures rather than genuine build failures.
DEFAULT_TIMEOUT_THRESHOLD_SECS = 120.0

# Minimum gap in createTime (seconds) between consecutive tasks (sorted by
# createTime) to consider them part of different sets.
SET_GAP_THRESHOLD_SECS = 300.0  # 5 minutes


def load_job_data(filepath: str) -> dict:
    """Load and parse JSON from file."""
    path = Path(filepath)
    if not path.exists():
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)
    with path.open() as f:
        return json.load(f)


def _parse_time(value: str) -> datetime:
    """Parse an ISO-8601 timestamp string."""
    return datetime.fromisoformat(value)


def _task_duration_secs(task: dict) -> float | None:
    """Return task duration in seconds, or None if times are missing."""
    start = task.get("startTime")
    end = task.get("endTime")
    if not start or not end:
        return None
    return (_parse_time(end) - _parse_time(start)).total_seconds()


def split_task_sets(tasks: list[dict]) -> list[tuple[str, list[dict]]]:
    """Split tasks into sets based on createTime clustering.

    Tasks are sorted by createTime; whenever there is a gap larger than
    SET_GAP_THRESHOLD_SECS between consecutive tasks, a new set begins.
    Returns a list of (label, task_list) tuples.
    """
    if not tasks:
        return []

    sorted_tasks = sorted(tasks, key=lambda t: _parse_time(t["createTime"]))

    sets: list[list[dict]] = [[sorted_tasks[0]]]
    for prev, cur in zip(sorted_tasks, sorted_tasks[1:]):
        gap = (
            _parse_time(cur["createTime"]) - _parse_time(prev["createTime"])
        ).total_seconds()
        if gap > SET_GAP_THRESHOLD_SECS:
            sets.append([])
        sets[-1].append(cur)

    return [(f"Set {i + 1}", s) for i, s in enumerate(sets)]


def classify_task(
    task: dict,
    threshold: float = DEFAULT_TIMEOUT_THRESHOLD_SECS,
) -> str:
    """Classify a task as Completed, Failed (real), or Failed (timeout).

    A failed task whose duration is below *threshold* seconds is considered
    a timeout/cascade failure.
    """
    status = task.get("status", "Unknown")
    if status != "Failed":
        return status

    duration = _task_duration_secs(task)
    if duration is not None and duration < threshold:
        return "Failed (timeout)"
    return "Failed (real)"


def cmd_summary(args: argparse.Namespace) -> None:
    """Print summary of task statuses, broken down by set."""
    data = load_job_data(args.file)
    tasks = data.get("tasks", [])

    print(f"Job: {data.get('jobId', 'N/A')}")
    print(f"Status: {data.get('status', 'N/A')}")

    task_sets = split_task_sets(tasks)

    for label, set_tasks in task_sets:
        classifications = Counter(
            classify_task(t, args.timeout_threshold) for t in set_tasks
        )
        total = len(set_tasks)

        first_create = min(_parse_time(t["createTime"]) for t in set_tasks)
        last_end_times = [
            _parse_time(t["endTime"])
            for t in set_tasks
            if t.get("endTime")
        ]
        last_end = max(last_end_times) if last_end_times else None

        print()
        print(f"--- {label} ({total} tasks) ---")
        print(f"  Created: {first_create:%Y-%m-%d %H:%M:%S}")
        if last_end:
            print(f"  Finished: {last_end:%Y-%m-%d %H:%M:%S}")

        display_order = [
            "Completed",
            "Failed (real)",
            "Failed (timeout)",
            "Running",
            "Pending",
        ]
        for status in display_order:
            if status in classifications:
                print(f"  {status:20} {classifications[status]:>4}")

        # Any other statuses not in the display order
        for status, count in sorted(classifications.items()):
            if status not in display_order:
                print(f"  {status:20} {count:>4}")


def cmd_failed(args: argparse.Namespace) -> None:
    """List failed task names, optionally filtered by set and failure type."""
    data = load_job_data(args.file)
    tasks = data.get("tasks", [])

    task_sets = split_task_sets(tasks)

    # Filter to requested set(s)
    if args.set is not None:
        idx = args.set - 1
        if idx < 0 or idx >= len(task_sets):
            print(
                f"Error: --set {args.set} is out of range "
                f"(have {len(task_sets)} sets)",
                file=sys.stderr,
            )
            sys.exit(1)
        task_sets = [task_sets[idx]]

    found_any = False
    for label, set_tasks in task_sets:
        failed_tasks = [t for t in set_tasks if t.get("status") == "Failed"]

        if args.real_only:
            failed_tasks = [
                t
                for t in failed_tasks
                if classify_task(t, args.timeout_threshold) == "Failed (real)"
            ]
        elif args.timeout_only:
            failed_tasks = [
                t
                for t in failed_tasks
                if classify_task(t, args.timeout_threshold)
                == "Failed (timeout)"
            ]

        if not failed_tasks:
            continue

        found_any = True

        if args.names_only:
            for task in failed_tasks:
                print(task.get("taskName", "Unknown"))
            continue

        if len(task_sets) > 1 or args.set is None:
            print(f"--- {label} ---")

        for task in failed_tasks:
            name = task.get("taskName", "Unknown")
            classification = classify_task(task, args.timeout_threshold)
            tag = "real" if classification == "Failed (real)" else "timeout"
            duration = _task_duration_secs(task)
            dur_str = f"{duration:.0f}s" if duration is not None else "?"
            print(f"  {name:<50} ({tag}, {dur_str})")

    if not found_any:
        print("No matching failed tasks.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze job status JSON")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # summary subcommand
    p_summary = subparsers.add_parser("summary", help="Show task status summary")
    p_summary.add_argument("file", help="Path to job status JSON file")
    p_summary.add_argument(
        "--timeout-threshold",
        type=float,
        default=DEFAULT_TIMEOUT_THRESHOLD_SECS,
        metavar="SECS",
        help=(
            "Duration threshold in seconds for classifying failures "
            f"(default: {DEFAULT_TIMEOUT_THRESHOLD_SECS})"
        ),
    )
    p_summary.set_defaults(func=cmd_summary)

    # failed subcommand
    p_failed = subparsers.add_parser("failed", help="List failed tasks")
    p_failed.add_argument("file", help="Path to job status JSON file")
    p_failed.add_argument(
        "--set",
        type=int,
        default=None,
        help="Only show failures from this set number (1-based)",
    )
    p_failed.add_argument(
        "--timeout-threshold",
        type=float,
        default=DEFAULT_TIMEOUT_THRESHOLD_SECS,
        metavar="SECS",
        help=(
            "Duration threshold in seconds for classifying failures "
            f"(default: {DEFAULT_TIMEOUT_THRESHOLD_SECS})"
        ),
    )
    filter_group = p_failed.add_mutually_exclusive_group()
    filter_group.add_argument(
        "--real-only",
        action="store_true",
        help="Only show real build failures (duration >= threshold)",
    )
    filter_group.add_argument(
        "--timeout-only",
        action="store_true",
        help="Only show timeout/cascade failures (duration < threshold)",
    )
    p_failed.add_argument(
        "--names-only",
        action="store_true",
        help="Output a flat list of task names only (no type or duration)",
    )
    p_failed.set_defaults(func=cmd_failed)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
