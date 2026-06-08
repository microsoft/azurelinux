# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""Extract overlay data from all .comp.toml and group TOML files in base/comps/.

Collects three data sources per overlay:
1. TOML-parsed fields (type, description, tag, value, etc.)
2. TOML comments above the overlay block
3. Git commit history (blame SHA, commit header, commit body, author, date)

Outputs a structured JSON file for consumption by classify_overlays.py.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tomllib
from pathlib import Path

# ---------------------------------------------------------------------------
# Git helpers
# ---------------------------------------------------------------------------


def _run_git(args: list[str], cwd: Path) -> str:
    """Run a git command and return stdout."""
    result = subprocess.run(
        ["git", "--no-pager", *args],
        capture_output=True,
        text=True,
        cwd=cwd,
        check=False,
    )
    if result.returncode != 0:
        print(f"WARNING: git {' '.join(args[:3])}... failed: {result.stderr.strip()}", file=sys.stderr)
        return ""
    return result.stdout


def _git_blame_porcelain(file_path: Path, repo_root: Path) -> dict[int, dict[str, str]]:
    """Run git blame --porcelain on a file and return line_number -> {sha, summary}."""
    rel_path = file_path.relative_to(repo_root)
    output = _run_git(["blame", "--porcelain", str(rel_path)], cwd=repo_root)
    if not output:
        return {}

    result: dict[int, dict[str, str]] = {}
    # Track summary per SHA (porcelain only emits headers for the first line in a group)
    sha_summaries: dict[str, str] = {}
    current_sha = ""
    current_line = 0

    for line in output.splitlines():
        # SHA line: 40-hex-char SHA followed by original-line result-line [group-count]
        sha_match = re.match(r"^([0-9a-f]{40})\s+(\d+)\s+(\d+)", line)
        if sha_match:
            current_sha = sha_match.group(1)
            current_line = int(sha_match.group(3))
            # Record entry immediately with whatever summary we know so far
            result[current_line] = {
                "sha": current_sha,
                "summary": sha_summaries.get(current_sha, ""),
            }
            continue

        if line.startswith("summary "):
            summary = line[8:]
            sha_summaries[current_sha] = summary
            # Update the current line's entry with the summary
            if current_line in result:
                result[current_line]["summary"] = summary

    return result


_MIN_COMMIT_FIELDS = 4


def _batch_fetch_commits(shas: set[str], repo_root: Path) -> dict[str, dict[str, str]]:
    """Fetch full commit info for a set of SHAs. Returns sha -> {header, body, author, date}."""
    commits: dict[str, dict[str, str]] = {}
    if not shas:
        return commits

    for sha in shas:
        output = _run_git(
            ["log", "-1", "--format=%H%n%s%n%an%n%aI%n%b", sha],
            cwd=repo_root,
        )
        if not output:
            continue
        lines = output.split("\n", _MIN_COMMIT_FIELDS)
        if len(lines) >= _MIN_COMMIT_FIELDS:
            commits[sha] = {
                "commit_sha": lines[0],
                "commit_header": lines[1],
                "author": lines[2],
                "date": lines[3],
                "commit_body": (lines[_MIN_COMMIT_FIELDS].strip() if len(lines) > _MIN_COMMIT_FIELDS else ""),
            }
    return commits


# ---------------------------------------------------------------------------
# TOML comment extraction
# ---------------------------------------------------------------------------


def _extract_comments_above_line(lines: list[str], target_line: int) -> str:
    """Extract consecutive comment lines immediately above target_line (0-indexed)."""
    comments: list[str] = []
    idx = target_line - 1
    while idx >= 0:
        stripped = lines[idx].strip()
        if stripped.startswith("#"):
            comments.append(stripped)
            idx -= 1
        elif stripped == "":
            # Allow blank lines between comments
            idx -= 1
        else:
            break
    comments.reverse()
    return "\n".join(comments)


def _find_overlay_line_numbers(raw_lines: list[str], component_name: str) -> list[int]:
    """Find 0-indexed line numbers of [[components.<name>.overlays]] headers."""
    pattern = re.compile(
        rf"^\s*\[\[components\.{re.escape(component_name)}\.overlays\]\]",
    )
    return [i for i, line in enumerate(raw_lines) if pattern.match(line)]


def _find_description_line(raw_lines: list[str], start_line: int) -> int | None:
    """Find the line number of the description field within an overlay block starting at start_line."""
    # Start from the line after the header
    for i in range(start_line + 1, min(start_line + 30, len(raw_lines))):
        stripped = raw_lines[i].strip()
        if stripped.startswith("description"):
            return i
        # Stop at next section header
        if stripped.startswith("[[") or (stripped.startswith("[") and not stripped.startswith("[[")):
            break
    return None


def _find_group_component_lines(raw_lines: list[str]) -> dict[str, int]:
    """Find line numbers for component entries in a group's components list."""
    result: dict[str, int] = {}
    in_components = False
    for i, line in enumerate(raw_lines):
        stripped = line.strip()
        if "components" in stripped and "=" in stripped and "[" in stripped:
            in_components = True
            continue
        if in_components:
            if stripped == "]":
                break
            # Match quoted component names
            match = re.match(r'^\s*"([^"]+)"', stripped)
            if match:
                result[match.group(1)] = i
    return result


# ---------------------------------------------------------------------------
# Overlay extraction
# ---------------------------------------------------------------------------


def _extract_component_context(comp_config: dict[str, object]) -> dict[str, object]:  # noqa: C901
    """Extract component-level context fields."""
    context: dict[str, object] = {}

    spec = comp_config.get("spec", {})
    if isinstance(spec, dict):
        if "upstream-commit" in spec:
            context["upstream_commit"] = spec["upstream-commit"]
        if "upstream-distro" in spec:
            context["upstream_distro"] = spec["upstream-distro"]
        if "upstream-name" in spec:
            context["upstream_name"] = spec["upstream-name"]

    build = comp_config.get("build", {})
    if isinstance(build, dict):
        if "with" in build:
            context["build_with"] = build["with"]
        if "without" in build:
            context["build_without"] = build["without"]
        if "defines" in build:
            context["build_defines"] = build["defines"]
        check = build.get("check", {})
        if isinstance(check, dict) and check.get("skip"):
            context["check_skip"] = True

    release = comp_config.get("release", {})
    if isinstance(release, dict) and "calculation" in release:
        context["release_calculation"] = release["calculation"]

    return context


def _extract_overlay_fields(overlay: dict[str, object]) -> dict[str, object]:
    """Extract all overlay fields into a flat dict."""
    fields: dict[str, object] = {}
    for key in (
        "type",
        "description",
        "tag",
        "value",
        "regex",
        "replacement",
        "section",
        "package",
        "file",
        "lines",
        "source",
    ):
        if key in overlay:
            fields[key] = overlay[key]
    return fields


# ---------------------------------------------------------------------------
# Patch file header parsing
# ---------------------------------------------------------------------------

# Patterns for extracting metadata from patch file headers
_RE_PR_URL = re.compile(
    r"https?://github\.com/[^\s/]+/[^\s/]+/(?:pull|issues)/\d+",
)
_RE_CLOSES_REF = re.compile(
    r"(?:closes|fixes|resolves|refs?)[:\s]*#?(\d+)",
    re.IGNORECASE,
)
_RE_BUG_ID = re.compile(
    r"\b(?:[A-Z]{2,10}-\d+|bz#?\d+|GH-\d+|rhbz#?\d+)\b",
)
_RE_PATCH_AUTHOR = re.compile(r"^From:\s*(.+?)(?:\s*<[^>]+>)?\s*$", re.MULTILINE)
_RE_PATCH_SUBJECT = re.compile(
    r"^Subject:\s*(?:\[PATCH[^\]]*\]\s*)?(.+?)(?:\n\s+(.+))*$",
    re.MULTILINE,
)

# How many bytes of a patch file to read (header + commit message are at the top)
_PATCH_HEADER_BYTES = 4096


def _parse_patch_header(patch_path: Path) -> dict[str, object] | None:
    """Parse a .patch/.diff file header and extract metadata.

    Returns a dict with author, subject, pr_urls, bug_ids, and close_refs,
    or None if the file cannot be read or is not a git-format patch.
    """
    if not patch_path.exists():
        return None

    suffix = patch_path.suffix.lower()
    if suffix not in (".patch", ".diff"):
        return None

    try:
        header = patch_path.read_bytes()[:_PATCH_HEADER_BYTES].decode("utf-8", errors="replace")
    except OSError:
        return None

    result: dict[str, object] = {}

    author_match = _RE_PATCH_AUTHOR.search(header)
    if author_match:
        result["patch_author"] = author_match.group(1).strip()

    subject_match = _RE_PATCH_SUBJECT.search(header)
    if subject_match:
        subject = subject_match.group(1).strip()
        # Multi-line subjects have continuation lines
        if subject_match.group(2):
            subject += " " + subject_match.group(2).strip()
        result["patch_subject"] = subject

    pr_urls = _RE_PR_URL.findall(header)
    if pr_urls:
        result["pr_urls"] = list(dict.fromkeys(pr_urls))  # dedupe, preserve order

    bug_ids = _RE_BUG_ID.findall(header)
    if bug_ids:
        result["bug_ids"] = list(dict.fromkeys(bug_ids))

    close_refs = _RE_CLOSES_REF.findall(header)
    if close_refs:
        result["close_refs"] = [f"#{ref}" for ref in dict.fromkeys(close_refs)]

    return result or None


def _enrich_with_patch_metadata(
    entry: dict[str, object],
    comp_dir: Path,
) -> None:
    """If entry is a file-add/patch-add for a .patch/.diff, parse its header."""
    overlay_type = entry.get("type", "")
    if overlay_type not in ("file-add", "patch-add"):
        return

    source = entry.get("source")
    if not isinstance(source, str):
        return

    if not source.lower().endswith((".patch", ".diff")):
        return

    patch_path = comp_dir / source
    metadata = _parse_patch_header(patch_path)
    if metadata:
        entry["patch_metadata"] = metadata


def extract_overlays(comps_dir: Path, repo_root: Path) -> dict[str, object]:  # noqa: C901, PLR0912, PLR0915
    """Extract all overlays from comp.toml and group files.

    Returns the full output structure ready for JSON serialization.
    """
    all_overlays: list[dict[str, object]] = []
    all_group_entries: list[dict[str, object]] = []
    all_shas: set[str] = set()
    comp_files_scanned = 0

    # -- Per-component overlays from .comp.toml files --
    toml_files = sorted(comps_dir.rglob("*.comp.toml"))
    for toml_file in toml_files:
        comp_files_scanned += 1
        raw_text = toml_file.read_text()
        raw_lines = raw_text.splitlines()

        try:
            data = tomllib.loads(raw_text)
        except tomllib.TOMLDecodeError as e:
            print(f"WARNING: Failed to parse {toml_file}: {e}", file=sys.stderr)
            continue

        components = data.get("components", {})
        if not isinstance(components, dict):
            continue

        # Get blame data for this file
        blame_data = _git_blame_porcelain(toml_file, repo_root)

        for comp_name, comp_config in components.items():
            if not isinstance(comp_config, dict):
                continue

            overlays = comp_config.get("overlays", [])
            if not overlays:
                continue

            # Find overlay header lines in raw text
            overlay_lines = _find_overlay_line_numbers(raw_lines, comp_name)
            comp_context = _extract_component_context(comp_config)

            for idx, overlay in enumerate(overlays):
                if not isinstance(overlay, dict):
                    continue

                entry: dict[str, object] = {
                    "component": comp_name,
                    "file": str(toml_file.relative_to(repo_root)),
                    "overlay_index": idx,
                }
                entry.update(_extract_overlay_fields(overlay))
                entry["component_context"] = comp_context

                # Extract comments above overlay header
                if idx < len(overlay_lines):
                    header_line = overlay_lines[idx]
                    entry["context_comments"] = _extract_comments_above_line(raw_lines, header_line)

                    # Find description line for git blame
                    desc_line = _find_description_line(raw_lines, header_line)
                    if desc_line is not None:
                        # Use 1-indexed line number for blame lookup
                        blame_line = desc_line + 1
                        if blame_line in blame_data:
                            sha = blame_data[blame_line]["sha"]
                            entry["git_blame_sha"] = sha
                            entry["git_blame_summary"] = blame_data[blame_line]["summary"]
                            all_shas.add(sha)
                else:
                    entry["context_comments"] = ""

                # Parse patch file headers for file-add/patch-add overlays
                _enrich_with_patch_metadata(entry, toml_file.parent)

                all_overlays.append(entry)

    # -- Also scan inline overlays in components.toml --
    components_toml = comps_dir / "components.toml"
    if components_toml.exists():
        comp_files_scanned += 1
        raw_text = components_toml.read_text()
        raw_lines = raw_text.splitlines()
        try:
            data = tomllib.loads(raw_text)
        except tomllib.TOMLDecodeError as e:
            print(f"WARNING: Failed to parse {components_toml}: {e}", file=sys.stderr)
        else:
            components = data.get("components", {})
            if isinstance(components, dict):
                blame_data = _git_blame_porcelain(components_toml, repo_root)
                for comp_name, comp_config in components.items():
                    if not isinstance(comp_config, dict):
                        continue
                    overlays = comp_config.get("overlays", [])
                    if not overlays:
                        continue
                    overlay_lines = _find_overlay_line_numbers(raw_lines, comp_name)
                    comp_context = _extract_component_context(comp_config)
                    for idx, overlay in enumerate(overlays):
                        if not isinstance(overlay, dict):
                            continue
                        entry = {
                            "component": comp_name,
                            "file": str(components_toml.relative_to(repo_root)),
                            "overlay_index": idx,
                        }
                        entry.update(_extract_overlay_fields(overlay))
                        entry["component_context"] = comp_context
                        if idx < len(overlay_lines):
                            entry["context_comments"] = _extract_comments_above_line(raw_lines, overlay_lines[idx])
                            desc_line = _find_description_line(raw_lines, overlay_lines[idx])
                            if desc_line is not None:
                                blame_line = desc_line + 1
                                if blame_line in blame_data:
                                    sha = blame_data[blame_line]["sha"]
                                    entry["git_blame_sha"] = sha
                                    entry["git_blame_summary"] = blame_data[blame_line]["summary"]
                                    all_shas.add(sha)
                        else:
                            entry["context_comments"] = ""

                        # Parse patch file headers for file-add/patch-add overlays
                        # Inline overlays: patch files are in base/comps/<comp_name>/
                        _enrich_with_patch_metadata(entry, comps_dir / comp_name)

                        all_overlays.append(entry)

    # -- Group overlays --
    group_files = [
        comps_dir / "component-check-disablement.toml",
        comps_dir / "component-mingw-disablement.toml",
    ]
    for group_file in group_files:
        if not group_file.exists():
            continue

        raw_text = group_file.read_text()
        raw_lines = raw_text.splitlines()
        try:
            data = tomllib.loads(raw_text)
        except tomllib.TOMLDecodeError as e:
            print(f"WARNING: Failed to parse {group_file}: {e}", file=sys.stderr)
            continue

        blame_data = _git_blame_porcelain(group_file, repo_root)
        comp_line_map = _find_group_component_lines(raw_lines)

        groups = data.get("component-groups", {})
        if not isinstance(groups, dict):
            continue

        for group_name, group_config in groups.items():
            if not isinstance(group_config, dict):
                continue

            group_desc = group_config.get("description", "")
            components_list = group_config.get("components", [])
            default_config = group_config.get("default-component-config", {})

            for comp_name in components_list:
                entry: dict[str, object] = {
                    "group": group_name,
                    "file": str(group_file.relative_to(repo_root)),
                    "component": comp_name,
                    "group_description": group_desc,
                    "config_applied": default_config,
                }

                # Git blame for the component list entry line
                if comp_name in comp_line_map:
                    blame_line = comp_line_map[comp_name] + 1  # 1-indexed
                    if blame_line in blame_data:
                        sha = blame_data[blame_line]["sha"]
                        entry["git_blame_sha"] = sha
                        entry["git_blame_summary"] = blame_data[blame_line]["summary"]
                        all_shas.add(sha)

                all_group_entries.append(entry)

    # -- Batch fetch full commit messages --
    print(f"Fetching {len(all_shas)} unique commit messages...", file=sys.stderr)
    commit_data = _batch_fetch_commits(all_shas, repo_root)

    # Enrich overlays with full commit data
    for entry in all_overlays:
        sha = entry.get("git_blame_sha")
        if isinstance(sha, str) and sha in commit_data:
            entry["git"] = commit_data[sha]
            del entry["git_blame_sha"]
            if "git_blame_summary" in entry:
                del entry["git_blame_summary"]
        elif isinstance(sha, str):
            entry["git"] = {
                "commit_sha": sha,
                "commit_header": entry.get("git_blame_summary", ""),
                "commit_body": "",
                "author": "",
                "date": "",
            }
            if "git_blame_sha" in entry:
                del entry["git_blame_sha"]
            if "git_blame_summary" in entry:
                del entry["git_blame_summary"]

    for entry in all_group_entries:
        sha = entry.get("git_blame_sha")
        if isinstance(sha, str) and sha in commit_data:
            entry["git"] = commit_data[sha]
            del entry["git_blame_sha"]
            if "git_blame_summary" in entry:
                del entry["git_blame_summary"]
        elif isinstance(sha, str):
            entry["git"] = {
                "commit_sha": sha,
                "commit_header": entry.get("git_blame_summary", ""),
                "commit_body": "",
                "author": "",
                "date": "",
            }
            if "git_blame_sha" in entry:
                del entry["git_blame_sha"]
            if "git_blame_summary" in entry:
                del entry["git_blame_summary"]

    return {
        "metadata": {
            "comp_toml_files_scanned": comp_files_scanned,
            "total_overlays": len(all_overlays),
            "total_group_entries": len(all_group_entries),
            "unique_commits_analyzed": len(commit_data),
        },
        "overlays": all_overlays,
        "group_entries": all_group_entries,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    """CLI entry point for the overlay extractor."""
    parser = argparse.ArgumentParser(description="Extract overlay data from comp.toml files")
    parser.add_argument(
        "--comps-dir",
        type=Path,
        default=Path("base/comps"),
        help="Path to the comps directory (default: base/comps)",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="Git repository root (default: auto-detect)",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        required=True,
        help="Output JSON file path",
    )
    args = parser.parse_args()

    repo_root = args.repo_root
    if repo_root is None:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True,
        )
        repo_root = Path(result.stdout.strip())

    comps_dir = repo_root / args.comps_dir if not args.comps_dir.is_absolute() else args.comps_dir

    print(f"Scanning {comps_dir} ...", file=sys.stderr)
    data = extract_overlays(comps_dir, repo_root)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, indent=2) + "\n")

    meta = data["metadata"]
    print(
        f"Done: {meta['total_overlays']} overlays + {meta['total_group_entries']} group entries "
        f"from {meta['comp_toml_files_scanned']} files, "
        f"{meta['unique_commits_analyzed']} unique commits.",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
