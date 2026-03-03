#!/usr/bin/env python3
"""Manage the Azure Linux components list.

Subcommands:
  add-missing  Find missing components from a kiwi image's .packages file and
               add them to components.toml.
  update       Sync the components tree against a source-packages list: prune
               stale dedicated component dirs and append new entries to an
               output file.
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Callable

DEFAULT_REPO_ROOT = Path(__file__).resolve().parent.parent

# Characters that are safe to use as a bare TOML key (alphanumeric, hyphen,
# underscore).  Anything else requires single-quoting.
_BARE_KEY_RE = re.compile(r"^[A-Za-z0-9_-]+$")


def toml_component_key(name: str) -> str:
    """Return a TOML table header for a component, quoting if necessary.

    Bare keys are used when the name contains only alphanumerics, hyphens, and
    underscores.  Otherwise the name is single-quoted.

    Examples:
        >>> toml_component_key("python")
        '[components.python]'
        >>> toml_component_key("python3.14")
        "[components.'python3.14']"
        >>> toml_component_key("g++")
        "[components.'g++']"
    """
    if _BARE_KEY_RE.match(name):
        return f"[components.{name}]"
    return f"[components.'{name}']"


def component_name_from_header(line: str) -> str:
    """Extract a component name from a ``[components.NAME]`` header line."""
    return line.removeprefix("[components.").removesuffix("]").strip("'\"")


def resolve_source_packages(packages_file: Path) -> set[str]:
    """Map binary package names from a .packages file to source package names."""
    names = [
        l.split("|")[0].strip()
        for l in packages_file.read_text().splitlines()
        if l.strip()
    ]
    r = subprocess.run(
        [
            "xargs",
            "dnf",
            "repoquery",
            "-q",
            "-y",
            "--srpm",
            "--queryformat",
            "%{name}\n",
        ],
        input="\n".join(names),
        capture_output=True,
        text=True,
    )
    if r.returncode != 0:
        print(f"Warning: dnf repoquery exited {r.returncode}", file=sys.stderr)
    return {l.strip() for l in r.stdout.splitlines() if l.strip()}


def get_existing_components() -> set[str]:
    """Get all components already defined in the project."""
    r = subprocess.run(
        ["azldev", "comp", "list", "-a", "-O", "json"],
        capture_output=True,
        text=True,
        check=True,
    )
    return {c["name"] for c in json.loads(r.stdout)}


def read_sources_list(sources_file: Path) -> set[str]:
    """Read a newline-delimited list of source package names."""
    return {l.strip() for l in sources_file.read_text().splitlines() if l.strip()}


def parse_inline_components(components_toml: Path) -> set[str]:
    """Return the set of component names defined in *components_toml*.

    Only considers ``[components.NAME]`` lines; ignores ``includes`` and
    comments.
    """
    names: set[str] = set()
    for line in components_toml.read_text().splitlines():
        stripped = line.strip()
        if stripped.startswith("[components.") and stripped.endswith("]"):
            names.add(component_name_from_header(stripped))
    return names


def parse_dedicated_components(components_root: Path) -> dict[str, Path]:
    """Return ``{name: comp_toml_dir}`` for every ``**/*.comp.toml`` file."""
    result: dict[str, Path] = {}
    for p in components_root.glob("**/*.comp.toml"):
        name = p.name.removesuffix(".comp.toml")
        result[name] = p.parent
    return result


# ---------------------------------------------------------------------------
# add-missing subcommand
# ---------------------------------------------------------------------------


def add_and_sort_components(components_toml: Path, new: list[str]) -> None:
    """Append new components to components.toml, dedup, and sort."""
    lines = components_toml.read_text().splitlines()

    # Split into header (before first component) and component lines
    header: list[str] = []
    comps: list[str] = []
    for line in lines:
        (comps if comps or line.startswith("[components.") else header).append(line)

    # Add new entries, dedup, sort case-insensitively
    for c in new:
        comps.append(toml_component_key(c))
    comps = sorted(
        set(comps),
        key=lambda l: component_name_from_header(l).casefold(),
    )

    components_toml.write_text("\n".join(header + comps) + "\n")


def cmd_add_missing(args: argparse.Namespace) -> int:
    """Handler for the ``add-missing`` subcommand."""
    repo_root = args.repo_root.resolve()
    components_toml = (
        args.components_toml or repo_root / "base" / "comps" / "components.toml"
    ).resolve()

    if not args.packages_file.is_file():
        sys.exit(f"Error: Packages file not found: {args.packages_file}")
    if not components_toml.is_file():
        sys.exit(f"Error: components.toml not found: {components_toml}")

    print("Finding missing components...")
    missing = sorted(
        resolve_source_packages(args.packages_file) - get_existing_components()
    )

    if not missing:
        print("No missing components found!")
        return 0

    print("Missing components found:")
    for c in missing:
        print(f"  {c}")

    if args.dry_run:
        print(f"\nDry run — no changes written to {components_toml}.")
        return 0

    add_and_sort_components(components_toml, missing)
    print()
    for c in missing:
        print(f"Added: {c}")

    print("\nSorting components.toml...")
    print("Done! Components added and file sorted.")
    try:
        rel = components_toml.relative_to(repo_root)
    except ValueError:
        rel = components_toml
    print(f"\nRun 'git diff {rel}' to see the changes.")
    return 0


def cmd_update(args: argparse.Namespace) -> int:
    """Handler for the ``update`` subcommand.

    Default (full-sync) workflow:
      0.  Read the sources list to get the desired set of package names.
      1.  Optionally compare against ``get_existing_components()`` (info).
      2.  Parse top-level ``components.toml`` — left untouched.
      3.  Scan ``components_root/**/*.comp.toml`` for dedicated component dirs.
          Keep if the package is in the new list, otherwise remove the dir.
      4.  Write remaining new packages to *output_file*.

    With ``--add-only``:
      Skips step 3 (no pruning).  Reads the existing *output_file* (if any),
      merges the new entries in sorted order, and writes the result back.
    """
    components_root = args.components_root.resolve()
    components_toml = (components_root / "components.toml").resolve()

    if not args.sources_list.is_file():
        sys.exit(f"Error: Sources list not found: {args.sources_list}")
    if not components_root.is_dir():
        sys.exit(f"Error: Components root not found: {components_root}")
    if not components_toml.is_file():
        sys.exit(f"Error: components.toml not found: {components_toml}")

    # 0. Read desired source packages
    new_packages = read_sources_list(args.sources_list)
    print(f"Read {len(new_packages)} package(s) from {args.sources_list}")

    # 1. Informational
    existing = get_existing_components()
    print(f"Found {len(existing)} existing component(s) via azldev")

    # 2. Parse inline components (these stay untouched)
    inline_names = parse_inline_components(components_toml)
    print(f"Found {len(inline_names)} inline component(s) in {components_toml.name}")

    # 3. Scan dedicated component dirs
    dedicated = parse_dedicated_components(components_root)
    print(f"Found {len(dedicated)} dedicated component dir(s)")

    removed: list[str] = []
    if args.add_only:
        # --add-only: skip pruning entirely
        print("\n--add-only: skipping removal of stale component dirs")
    else:
        kept: list[str] = []
        for name, comp_dir in sorted(dedicated.items()):
            if name in new_packages:
                kept.append(name)
            else:
                removed.append(name)
                if not args.dry_run:
                    shutil.rmtree(comp_dir)

        if kept:
            print(
                f"\nKept {len(kept)} dedicated component dir(s) "
                f"(present in sources list)"
            )
        if removed:
            verb = "Would remove" if args.dry_run else "Removed"
            print(f"\n{verb} {len(removed)} stale dedicated component dir(s):")
            for name in removed:
                print(f"  {name}")

    # 4. Determine which packages still need to be added
    already_defined = inline_names | set(dedicated.keys())
    already_defined -= set(removed)
    to_add = sorted(new_packages - already_defined)

    if not to_add:
        print("\nNo new components to add.")
        return 0

    print(f"\n{len(to_add)} new component(s) to add:")
    for c in to_add:
        print(f"  {c}")

    if args.dry_run:
        print(f"\nDry run — no output written to {args.output_file}.")
        return 0

    output = args.output_file.resolve()

    if args.add_only and output.is_file():
        # Merge into existing output file, preserving header and sorting
        add_and_sort_components(output, to_add)
        print(f"\nMerged {len(to_add)} new component(s) into {output}")
    else:
        entries = [toml_component_key(c) for c in to_add]
        output.write_text("\n".join(entries) + "\n")
        print(f"\nWrote {len(to_add)} component entries to {output}")
    return 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Manage the Azure Linux components list.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_missing = subparsers.add_parser(
        "add-missing",
        help="Find missing components from a .packages file and add them to components.toml.",
    )
    add_missing.add_argument(
        "-p",
        "--packages-file",
        type=Path,
        required=True,
        help="Path to the .packages file "
        "(e.g. ./base/out/images/vm-base/azl4-vm-base.x86_64-0.1.packages)",
    )
    add_missing.add_argument(
        "-r",
        "--repo-root",
        type=Path,
        default=DEFAULT_REPO_ROOT,
        help=f"Path to the repository root (default: {DEFAULT_REPO_ROOT})",
    )
    add_missing.add_argument(
        "-c",
        "--components-toml",
        type=Path,
        default=None,
        help="Path to components.toml (default: <repo-root>/base/comps/components.toml)",
    )
    add_missing.add_argument(
        "--dry-run",
        action="store_true",
        help="List missing components without modifying components.toml",
    )

    update = subparsers.add_parser(
        "update",
        help="Sync the components tree against a source-packages list.",
    )
    update.add_argument(
        "-s",
        "--sources-list",
        type=Path,
        required=True,
        help="Path to a text file with one source package name per line",
    )
    update.add_argument(
        "-r",
        "--repo-root",
        type=Path,
        default=DEFAULT_REPO_ROOT,
        help=f"Path to the repository root (default: {DEFAULT_REPO_ROOT})",
    )
    update.add_argument(
        "-d",
        "--components-root",
        type=Path,
        default=None,
        help="Path to the folder containing component definitions "
        "(default: <repo-root>/base/comps)",
    )
    update.add_argument(
        "-o",
        "--output-file",
        type=Path,
        required=True,
        help="Where to write the new component entries",
    )
    update.add_argument(
        "--add-only",
        action="store_true",
        help="Only add missing packages to the output file (no pruning of "
        "stale component dirs). If the output file already exists, new "
        "entries are merged in sorted order.",
    )
    update.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would happen without making changes",
    )

    args = parser.parse_args(argv)

    # Resolve components_root default after parsing so --repo-root is honoured
    if args.command == "update" and args.components_root is None:
        args.components_root = args.repo_root / "base" / "comps"

    return args


_COMMAND_HANDLERS: dict[str, Callable] = {
    "add-missing": cmd_add_missing,
    "update": cmd_update,
}


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    handler = _COMMAND_HANDLERS[args.command]
    return handler(args)


if __name__ == "__main__":
    sys.exit(main())
