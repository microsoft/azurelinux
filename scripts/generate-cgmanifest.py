# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""Generate a Component Governance manifest from Azure Linux RPM spec files."""

# ruff: noqa: INP001 — standalone repository utility, not an importable package.

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

MACRO_RE = re.compile(r"^%(?:global|define)\s+(\S+)(?:\s+(.*))?", re.MULTILINE)
TAG_RE = re.compile(
    r"^[ \t]*(Name|Version|URL|Source0?|Source)[ \t]*:[ \t]*([^\r\n]*?)[ \t]*$",
    re.IGNORECASE | re.MULTILINE,
)


def _expand_macros(value: str, macros: dict[str, str]) -> str:
    """Expand common RPM macros used in Name, Version, and URL tags."""
    expanded = value

    for _ in range(20):
        previous = expanded

        for macro_name, macro_value in sorted(macros.items(), key=lambda item: -len(item[0])):
            expanded = re.sub(rf"%\{{\?{re.escape(macro_name)}\}}", lambda _match, value=macro_value: value, expanded)
            expanded = re.sub(rf"%\{{!{re.escape(macro_name)}\}}", lambda _match: "", expanded)
            expanded = re.sub(rf"%\{{{re.escape(macro_name)}\}}", lambda _match, value=macro_value: value, expanded)
            expanded = re.sub(rf"(?<!%)%{re.escape(macro_name)}\b", lambda _match, value=macro_value: value, expanded)

        expanded = re.sub(r"%\{\?[^}]+\}", "", expanded)
        expanded = re.sub(r"%\{!?[^}]+\}", "", expanded)

        if expanded == previous:
            break

    expanded = re.sub(r"%\{nil\}|%nil", "", expanded)
    expanded = re.sub(r"%\{[^}]+\}", "", expanded)

    return expanded.strip()


def _collect_macros(text: str, spec_path: Path) -> dict[str, str]:
    """Collect spec macros and assignments from companion macro files."""
    macros: dict[str, str] = {}
    for match in MACRO_RE.finditer(text):
        macro_name = match.group(1)
        if "(" in macro_name:
            macro_name = macro_name.split("(", 1)[0]
        macros[macro_name] = (match.group(2) or "").strip()

    for macro_file in spec_path.parent.glob("*macros*"):
        if macro_file.is_file():
            for line in macro_file.read_text(encoding="utf-8", errors="replace").splitlines():
                match = re.match(r"^%([A-Za-z_][A-Za-z0-9_]*)\s+(.+?)\s*$", line)
                if match:
                    macros[match.group(1)] = match.group(2)
    return macros


def _collect_tags(text: str) -> dict[str, str]:
    """Collect supported RPM tags from a spec."""
    tags: dict[str, str] = {}
    for match in TAG_RE.finditer(text):
        tags.setdefault(match.group(1).lower(), match.group(2).strip())
    return tags


def _derive_gourl(macros: dict[str, str]) -> None:
    """Derive gourl from forgeurl or common Go repository paths."""
    if "gourl" not in macros and "forgeurl" in macros:
        macros["gourl"] = macros["forgeurl"]
        return

    goipath = macros.get("goipath", macros.get("goipath0", ""))
    if "gourl" not in macros and goipath.startswith(("github.com/", "bitbucket.org/")):
        macros["gourl"] = "https://" + goipath


def extract_spec_metadata(spec_path: Path) -> dict[str, str]:
    """Extract Name, Version, and URL metadata from an RPM spec."""
    text = spec_path.read_text(encoding="utf-8", errors="replace")

    macros = _collect_macros(text, spec_path)
    _derive_gourl(macros)
    tags = _collect_tags(text)

    name = _fallback_name(tags.get("name", ""), spec_path, {**macros, **tags})
    version = _fallback_version(tags.get("version", ""), macros)

    url = tags.get("url", "")
    source = tags.get("source0", tags.get("source", ""))
    download_url = _expand_macros(url, {**macros, **tags, "name": name, "version": version})

    compliant_protocol = ("http://", "https://", "ftp://", "ftps://")
    if not download_url or "%{" in download_url or not download_url.startswith(compliant_protocol):
        source_url = _expand_macros(source, {**macros, **tags, "name": name, "version": version})
        download_url = source_url if source_url.startswith(compliant_protocol) else ""

    return {
        "name": name,
        "version": version,
        "downloadUrl": download_url,
    }


def validate_spec_metadata(metadata: dict[str, str], *, url_found: bool = True) -> list[str]:
    """Return validation failures for extracted spec metadata."""
    failures: list[str] = []

    if not metadata["name"]:
        failures.append("name cannot be empty")

    if not metadata["version"]:
        failures.append("version cannot be empty")

    download_url = metadata["downloadUrl"]
    if not url_found:
        failures.append("URL field not found")
    elif not download_url:
        failures.append("downloadUrl cannot be empty")
    elif not download_url.startswith(("http://", "https://", "ftp://", "ftps://")):
        failures.append(f"invalid source url - found ({download_url})")

    return failures


def build_registrations(root_folder: Path) -> tuple[list[dict[str, Any]], int, dict[str, list[Path]]]:
    """Build registrations and return counts plus failures grouped by error."""
    registrations: list[dict[str, Any]] = []
    failure_count = 0
    failures_by_error: dict[str, list[Path]] = {}

    for spec_path in sorted(root_folder.rglob("*.spec"), key=lambda path: str(path).lower()):
        metadata = extract_spec_metadata(spec_path)
        url_found = url_field_found(spec_path)
        failures = validate_spec_metadata(metadata, url_found=url_found)
        if failures:
            failure_count += 1
            for failure in failures:
                failures_by_error.setdefault(failure, []).append(spec_path)
            continue

        registrations.append(
            {
                "component": {
                    "type": "other",
                    "other": metadata,
                }
            }
        )

    return registrations, failure_count, failures_by_error


def generate_manifest(root_folder: Path, output_file: Path) -> tuple[int, int, dict[str, list[Path]]]:
    """Generate the manifest and return counts plus grouped failures."""
    registrations, failure_count, failures_by_error = build_registrations(root_folder)
    manifest = {
        "Registrations": registrations,
        "Version": 1,
    }

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return len(registrations), failure_count, failures_by_error


def parse_args(argv: list[str]) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate cgmanifest.json entries from RPM spec files.",
    )
    parser.add_argument("root_folder", nargs="?", help="folder to scan (default: specs)")
    parser.add_argument("output_file", nargs="?", help="output JSON file")
    parser.add_argument("-r", "--root", dest="root_option", help="folder to scan")
    parser.add_argument("-o", "--output", dest="output_option", help="output JSON file")

    args = parser.parse_args(argv)

    if args.output_option:
        args.output_file = args.output_option
    elif args.output_file is None:
        if args.root_folder is None:
            parser.error("an output JSON file is required")
        args.output_file = args.root_folder
        args.root_folder = None

    if args.root_option:
        args.root_folder = args.root_option

    args.root_folder = args.root_folder or "specs"
    return args


def url_field_found(spec_path: Path) -> bool:
    """Return whether the spec provides a URL or protocol-based Source fallback."""
    text = spec_path.read_text(encoding="utf-8", errors="replace")
    for match in TAG_RE.finditer(text):
        tag_name = match.group(1).lower()
        value = match.group(2).strip()
        if tag_name == "url":
            return True
        if tag_name in ("source", "source0") and value.startswith(("http://", "https://", "ftp://", "ftps://")):
            return True
    return False


def _fallback_name(raw_name: str, spec_path: Path, macros: dict[str, str]) -> str:
    """Resolve a Name value, falling back to the spec filename stem."""
    expanded = _expand_macros(raw_name, macros)
    if expanded and "%{" not in expanded:
        return expanded

    for macro_name in ("goname", "orig_name", "module", "base_name"):
        candidate = _expand_macros(macros.get(macro_name, ""), macros)
        if candidate and "%{" not in candidate:
            return candidate

    return spec_path.stem


def _fallback_version(raw_version: str, macros: dict[str, str]) -> str:
    """Resolve a Version value using common upstream version variables."""
    expanded = _expand_macros(raw_version, macros)
    if expanded and "%{" not in expanded and not expanded.startswith("%{lua:"):
        return expanded

    conditional_fallback = re.search(r":([0-9][^}]*)\}", raw_version)
    if conditional_fallback:
        return conditional_fallback.group(1).strip()

    for macro_name in (
        "upstream_version",
        "upstream_ver",
        "version0",
        "pkg_version",
        "baseversion",
        "version_alsa_lib",
        "lib_version",
        "antlr_version",
        "brzmajor",
        "branch",
    ):
        candidate = _expand_macros(macros.get(macro_name, ""), macros)
        if candidate and "%{" not in candidate:
            if macro_name in ("upstream_ver", "upstream_version"):
                candidate = candidate.replace("-", ".")
            return candidate

    return ""


def main(argv: list[str] | None = None) -> int:
    """Run the manifest generator."""
    args = parse_args(sys.argv[1:] if argv is None else argv)
    root_folder = Path(args.root_folder)
    output_file = Path(args.output_file)

    if not root_folder.is_dir():
        print(f"error: root folder does not exist or is not a directory: {root_folder}", file=sys.stderr)
        return 1

    count, failure_count, failures_by_error = generate_manifest(root_folder, output_file)
    print(f"Generated {count} registrations in {output_file}")
    print(f"Spec files with failures: {failure_count}")

    for error, spec_paths in sorted(failures_by_error.items(), key=lambda item: item[0]):
        print(f"\n{error}: {len(spec_paths)}", file=sys.stderr)
        for spec_path in spec_paths:
            print(f"  {spec_path}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
