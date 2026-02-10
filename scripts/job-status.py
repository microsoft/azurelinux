#!/usr/bin/env python3
"""Analyze job status JSON and provide summary or list failed tasks."""

import argparse
import json
import sys
from collections import Counter
from pathlib import Path


def load_job_data(filepath: str) -> dict:
    """Load and parse JSON from file."""
    path = Path(filepath)
    if not path.exists():
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)
    with path.open() as f:
        return json.load(f)


def cmd_summary(args: argparse.Namespace) -> None:
    """Print summary of task statuses."""
    data = load_job_data(args.file)
    tasks = data.get("tasks", [])

    status_counts = Counter(task.get("status", "Unknown") for task in tasks)
    total = len(tasks)

    print(f"Job: {data.get('jobId', 'N/A')}")
    print(f"Status: {data.get('status', 'N/A')}")
    print()
    print(f"Total tasks: {total}")

    # Show counts in a consistent order
    for status in ["Completed", "Failed", "Running", "Pending"]:
        if status in status_counts:
            print(f"  {status:12} {status_counts[status]:>4}")

    # Show any other statuses
    for status, count in sorted(status_counts.items()):
        if status not in ["Completed", "Failed", "Running", "Pending"]:
            print(f"  {status:12} {count:>4}")


def cmd_failed(args: argparse.Namespace) -> None:
    """List all failed task names."""
    data = load_job_data(args.file)
    tasks = data.get("tasks", [])

    failed = [task.get("taskName", "Unknown") for task in tasks if task.get("status") == "Failed"]

    if not failed:
        print("No failed tasks.")
        return

    for name in failed:
        print(name)


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze job status JSON")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # summary subcommand
    p_summary = subparsers.add_parser("summary", help="Show task status summary")
    p_summary.add_argument("file", help="Path to job status JSON file")
    p_summary.set_defaults(func=cmd_summary)

    # failed subcommand
    p_failed = subparsers.add_parser("failed", help="List failed tasks")
    p_failed.add_argument("file", help="Path to job status JSON file")
    p_failed.set_defaults(func=cmd_failed)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
