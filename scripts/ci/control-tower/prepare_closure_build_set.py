#!/usr/bin/env python3
"""Prepare the component set whose candidate RPMs can affect closure."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import package_build
from publication_policy import PublicationPolicy, parse_publication_policy

DEFAULT_POLICY_PATH = Path("base/comps/components-publish-channels.toml")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-commit", required=True)
    parser.add_argument("--changed-components-file", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--replaced-components-output", required=True, type=Path)
    parser.add_argument("--policy-path", default=DEFAULT_POLICY_PATH, type=Path)
    parser.add_argument("--source-commit", required=True)
    return parser.parse_args()


def read_policy_at_commit(commit: str, path: Path) -> PublicationPolicy:
    """Read one committed policy without trusting mutable working-tree state."""
    result = subprocess.run(
        ["git", "show", f"{commit}:{path.as_posix()}"],
        capture_output=True,
        check=False,
        text=True,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or "git show returned no diagnostic"
        raise RuntimeError(f"Failed to read {path} at {commit}: {detail}")
    return parse_publication_policy(result.stdout, source=f"{commit}:{path}")


def policy_impacted_components(
    baseline: PublicationPolicy,
    candidate: PublicationPolicy,
) -> set[str]:
    """Return source components whose candidate publication route changed."""
    impacted = set(baseline.base_components ^ candidate.base_components)
    changed_exceptions = (
        set(baseline.sdk_exception_sources) ^ set(candidate.sdk_exception_sources)
    )
    changed_exceptions.update(
        package
        for package in set(baseline.sdk_exception_sources)
        & set(candidate.sdk_exception_sources)
        if baseline.sdk_exception_sources[package]
        != candidate.sdk_exception_sources[package]
    )
    for package in changed_exceptions:
        old_source = baseline.sdk_exception_sources.get(package)
        new_source = candidate.sdk_exception_sources.get(package)
        impacted.update(source for source in (old_source, new_source) if source is not None)
    return impacted


def prepare_build_set(
    *,
    base_commit: str,
    changed_components_file: Path,
    policy_path: Path,
    source_commit: str,
) -> list[str]:
    """Combine source changes with components affected only by policy changes."""
    build_components = set(package_build.load_build_components(changed_components_file))
    available_components = package_build.load_available_components(changed_components_file)
    baseline_policy = read_policy_at_commit(base_commit, policy_path)
    candidate_policy = read_policy_at_commit(source_commit, policy_path)
    policy_components = policy_impacted_components(baseline_policy, candidate_policy)
    deleted_components = package_build.load_deleted_components(changed_components_file)

    unavailable = policy_components - available_components - deleted_components
    if unavailable:
        raise RuntimeError(
            "Publication policy changes affect components absent from the candidate source: "
            f"{sorted(unavailable)}"
        )
    return sorted(build_components | (policy_components - deleted_components))


def write_component_names(path: Path, components: list[str]) -> None:
    """Write a stable JSON component-name array."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(components, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    """Prepare and persist the closure build set."""
    args = _parse_args()
    try:
        components = prepare_build_set(
            base_commit=args.base_commit,
            changed_components_file=args.changed_components_file,
            policy_path=args.policy_path,
            source_commit=args.source_commit,
        )
        write_component_names(args.output, components)
        replaced_components = set(components) | package_build.load_deleted_components(
            args.changed_components_file
        )
        write_component_names(args.replaced_components_output, sorted(replaced_components))
        print(
            "##vso[task.setvariable variable=hasCandidateClosureChanges]"
            f"{str(bool(replaced_components)).lower()}"
        )
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"##vso[task.logissue type=error]{exc}", file=sys.stderr)
        return 1

    print(f"Closure build set contains {len(components)} component(s):")
    for component in components:
        print(component)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
