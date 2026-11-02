# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
"""Require newly Base-routed components in a PR to enter the build set."""

from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
import tomllib
from pathlib import Path

PUBLISH_CHANNELS_PATH = "base/comps/components-publish-channels.toml"
BUILD_CHANGE_TYPES = {"added", "changed"}
KNOWN_CHANGE_TYPES = BUILD_CHANGE_TYPES | {"unchanged", "deleted"}


def _git(*args: str) -> str:
    """Read committed data without executing diff drivers or checking out refs."""
    return subprocess.run(
        ["git", *args],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout


def base_components_at(ref: str) -> set[str]:
    """Read Base membership from the committed TOML at one ref."""
    commit = _git("rev-parse", "--verify", "--end-of-options", f"{ref}^{{commit}}").strip()
    config = tomllib.loads(_git("show", f"{commit}:{PUBLISH_CHANNELS_PATH}"))
    try:
        members = config["component-groups"]["base-packages"]["components"]
    except (KeyError, TypeError) as error:
        raise ValueError(
            f"{ref}:{PUBLISH_CHANNELS_PATH} must define [component-groups.base-packages].components"
        ) from error
    if not isinstance(members, list) or any(not isinstance(name, str) or not name for name in members):
        raise ValueError(f"{ref}:{PUBLISH_CHANNELS_PATH}: Base components must be an array of non-empty strings")
    return set(members)


def load_change_types(path: Path) -> dict[str, str]:
    """Validate the existing azldev change-set rather than trusting touched paths."""
    entries = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(entries, list):
        raise TypeError(f"{path}: changed components must be a JSON array")
    changes: dict[str, str] = {}
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise TypeError(f"{path}: entry {index} must be a JSON object")
        name = entry.get("component")
        change_type = entry.get("changeType")
        if not isinstance(name, str) or not name:
            raise ValueError(f"{path}: entry {index} must have a non-empty component name")
        if not isinstance(change_type, str) or change_type not in KNOWN_CHANGE_TYPES:
            raise ValueError(f"{path}: entry {index} has an unknown changeType {change_type!r}")
        if name in changes:
            raise ValueError(f"{path}: duplicate component {name!r}")
        changes[name] = change_type
    return changes


def check_base_promotions(
    from_ref: str,
    to_ref: str,
    changed_components_file: Path,
) -> None:
    """Reject PR promotions that would not select a component build."""
    additions = base_components_at(to_ref) - base_components_at(from_ref)
    changes = load_change_types(changed_components_file)
    missing = sorted(name for name in additions if changes.get(name) not in BUILD_CHANGE_TYPES)
    if missing:
        commands = "\n".join(f"  azldev comp update -p {shlex.quote(name)} --bump" for name in missing)
        message = (
            "new Base components are not selected for a build: "
            f"{', '.join(repr(name) for name in missing)}.\n"
            "Channel changes only route future builds; they do not republish existing RPMs.\n"
            "Bump otherwise unchanged components:\n"
            f"{commands}\n"
            'For release.calculation = "manual", also advance the release in the component source/config.\n'
            "Then render and commit the locks/specs, re-render after committing, and stage the result "
            "for an amend. See DEVELOPING.md#package-publishing-channels."
        )
        raise ValueError(message)
    print(f"Base promotion check passed: {len(additions)} newly listed component(s) selected for a build.")


def main() -> int:
    """Check the same committed range and JSON consumed by package-build CI."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--from-commit", required=True)
    parser.add_argument("--to-commit", required=True)
    parser.add_argument("--changed-components-file", type=Path, required=True)
    args = parser.parse_args()
    try:
        check_base_promotions(
            args.from_commit,
            args.to_commit,
            args.changed_components_file,
        )
    except subprocess.CalledProcessError as error:
        print(f"ERROR: Base promotion check could not read git data: {error.stderr.strip()}", file=sys.stderr)
        return 1
    except (OSError, TypeError, ValueError) as error:
        print(f"ERROR: Base promotion check failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
