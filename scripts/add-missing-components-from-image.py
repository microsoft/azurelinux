#!/usr/bin/env python3
"""Find missing components from a kiwi image's .packages file and add them to components.toml."""

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
COMPONENTS_TOML = REPO_ROOT/"base"/"comps"/"components.toml"


def resolve_source_packages(packages_file: Path) -> set[str]:
    """Map binary package names from a .packages file to source package names."""
    names = [l.split("|")[0].strip() for l in packages_file.read_text().splitlines() if l.strip()]
    r = subprocess.run(
        ["xargs", "dnf", "repoquery", "-q", "-y", "--srpm", "--queryformat", "%{name}\n"],
        input="\n".join(names), capture_output=True, text=True,
    )
    if r.returncode != 0:
        print(f"Warning: dnf repoquery exited {r.returncode}", file=sys.stderr)
    return {l.strip() for l in r.stdout.splitlines() if l.strip()}


def get_existing_components() -> set[str]:
    """Get all components already defined in the project."""
    r = subprocess.run(["azldev", "comp", "list", "-a", "-O", "json"],
                       capture_output=True, text=True, check=True)
    return {c["name"] for c in json.loads(r.stdout)}


def add_and_sort_components(new: list[str]) -> None:
    """Append new components to components.toml, dedup, and sort."""
    lines = COMPONENTS_TOML.read_text().splitlines()

    # Split into header (before first component) and component lines
    header, comps = [], []
    for line in lines:
        (comps if comps or line.startswith("[components.") else header).append(line)

    # Add new entries, dedup, sort case-insensitively
    for c in new:
        comps.append(f"[components.{c}]")
    comps = sorted(set(comps),
                   key=lambda l: l.removeprefix("[components.").removesuffix("]").strip("'\"").casefold())

    COMPONENTS_TOML.write_text("\n".join(header + comps) + "\n")


def main() -> int:
    if len(sys.argv) < 2:
        name = Path(sys.argv[0]).name
        print(f"Usage: {name} <packages-file>\n")
        print(f"Example: {name} ./base/out/images/vm-base/azl4-vm-base.x86_64-0.1.packages")
        return 1

    packages_file = Path(sys.argv[1])
    if not packages_file.is_file():
        sys.exit(f"Error: Packages file not found: {packages_file}")
    if not COMPONENTS_TOML.is_file():
        sys.exit(f"Error: components.toml not found: {COMPONENTS_TOML}")

    print("Finding missing components...")
    missing = sorted(resolve_source_packages(packages_file) - get_existing_components())

    if not missing:
        print("No missing components found!")
        return 0

    print("Missing components found:")
    for c in missing:
        print(f"  {c}")

    add_and_sort_components(missing)
    print()
    for c in missing:
        print(f"Added: {c}")

    print(f"\nSorting components.toml...")
    print(f"Done! Components added and file sorted.")
    print(f"\nRun 'git diff {COMPONENTS_TOML.relative_to(REPO_ROOT)}' to see the changes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
