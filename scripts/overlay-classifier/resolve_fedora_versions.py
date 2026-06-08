# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""Resolve Fedora package versions for Backport-fedora overlays.

For each overlay classified as Backport-fedora, queries Fedora Koji to find:
- The current NVR in AZL's tracked Fedora branch (f43)
- The NVR that contains the backported fix (earliest Fedora tag with the fix)

This helps teams know when an overlay can be safely removed — i.e., when AZL
bumps its upstream pin to a Fedora version that already includes the fix.

Reads classified JSON (from classify_overlays.py or final_report.json) and
writes an enriched copy with a ``fedora_fix_info`` field on Backport-fedora entries.

Usage:
    python resolve_fedora_versions.py -i classified_overlays.json -o enriched.json
    python resolve_fedora_versions.py -i classified_overlays.json -o enriched.json --azl-fedora-version 43
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import xmlrpc.client
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Fedora dist-git URL extractor
# ---------------------------------------------------------------------------

_RE_FEDORA_COMMIT = re.compile(
    r"src\.fedoraproject\.org/rpms/([^/\s]+)/c(?:ommit)?/([0-9a-f]{7,40})"
)

# NVR pattern: name-version-release.fcNN or name-version-release.elNN etc.
_RE_NVR = re.compile(r"\b([a-zA-Z][\w.+-]+-\d[\d.]+-\d+(?:\.\w+)*)\b")


# ---------------------------------------------------------------------------
# Koji helpers
# ---------------------------------------------------------------------------

# Fedora tags to search, in order of increasing release distance.
# f{N} = the compose tag for Fedora N; f{N}-updates = stable updates.
_TAG_TEMPLATE = "f{ver}"
_TAG_UPDATES_TEMPLATE = "f{ver}-updates"

# Koji XML-RPC listTagged positional args:
#   tag, event, inherit, prefix, latest, package
_LIST_TAGGED_POS = (None, False, None, True)  # event, inherit, prefix, latest=True


def _koji_proxy() -> xmlrpc.client.ServerProxy:
    """Create a Koji XML-RPC proxy (lazy, module-level)."""
    return xmlrpc.client.ServerProxy(
        "https://koji.fedoraproject.org/kojihub",
        allow_none=True,
    )


def _get_latest_nvr(koji: xmlrpc.client.ServerProxy, package: str, tag: str) -> str | None:
    """Get the latest NVR for a package in a Koji tag. Returns None if not found."""
    try:
        builds = koji.listTagged(tag, *_LIST_TAGGED_POS, package)
        if builds:
            return str(builds[0]["nvr"])
    except Exception as exc:  # noqa: BLE001
        print(f"  WARNING: Koji query failed for {package} in {tag}: {exc}", file=sys.stderr)
    return None


def _find_fix_nvr(
    koji: xmlrpc.client.ServerProxy,
    package: str,
    azl_ver: int,
    *,
    max_search: int = 5,
) -> dict[str, str | None]:
    """Find the earliest Fedora tag that has a newer build than AZL's tracked version.

    Returns a dict with:
      - azl_tag: the tag AZL tracks (e.g. "f43")
      - azl_nvr: NVR in that tag (or None)
      - fix_tag: earliest tag with a different (newer) NVR (or None)
      - fix_nvr: NVR in fix_tag (or None)
    """
    azl_tag = _TAG_TEMPLATE.format(ver=azl_ver)
    azl_nvr = _get_latest_nvr(koji, package, azl_tag)

    result: dict[str, str | None] = {
        "azl_tag": azl_tag,
        "azl_nvr": azl_nvr,
        "fix_tag": None,
        "fix_nvr": None,
    }

    # Search forward from azl_ver+1 to find the first tag with a different build
    for offset in range(1, max_search + 1):
        check_ver = azl_ver + offset
        for tag in [
            _TAG_TEMPLATE.format(ver=check_ver),
            _TAG_UPDATES_TEMPLATE.format(ver=check_ver),
        ]:
            nvr = _get_latest_nvr(koji, package, tag)
            if nvr and nvr != azl_nvr:
                result["fix_tag"] = tag
                result["fix_nvr"] = nvr
                return result

    return result


# ---------------------------------------------------------------------------
# Per-entry resolution
# ---------------------------------------------------------------------------


def _extract_package_name(entry: dict[str, Any]) -> str:
    """Best-effort extraction of the Fedora package name from an overlay entry.

    Prefers the component name; falls back to the Fedora commit URL package name.
    """
    # Component name is typically the Fedora package name
    return str(entry.get("component", ""))


def _extract_fedora_commits(entry: dict[str, Any]) -> list[tuple[str, str]]:
    """Extract (package, commit_hash) pairs from all text fields."""
    desc = str(entry.get("description", ""))
    body = ""
    git = entry.get("git")
    if isinstance(git, dict):
        body = str(git.get("commit_body", ""))
    comments = str(entry.get("context_comments", ""))
    all_text = f"{desc}\n{body}\n{comments}"
    return _RE_FEDORA_COMMIT.findall(all_text)


def _extract_mentioned_nvrs(entry: dict[str, Any]) -> list[str]:
    """Extract NVR-like strings mentioned in overlay text."""
    desc = str(entry.get("description", ""))
    body = ""
    git = entry.get("git")
    if isinstance(git, dict):
        body = str(git.get("commit_body", ""))
    all_text = f"{desc}\n{body}"
    return _RE_NVR.findall(all_text)


def resolve_entry(
    entry: dict[str, Any],
    koji: xmlrpc.client.ServerProxy,
    azl_ver: int,
) -> dict[str, Any] | None:
    """Resolve Fedora fix version info for a single Backport-fedora entry.

    Returns a ``fedora_fix_info`` dict or None if resolution fails.
    """
    package = _extract_package_name(entry)
    if not package:
        return None

    info: dict[str, Any] = {"package": package}

    # Collect any Fedora commit references
    fedora_commits = _extract_fedora_commits(entry)
    if fedora_commits:
        info["fedora_commits"] = [
            {"package": pkg, "commit": sha} for pkg, sha in fedora_commits
        ]

    # Collect mentioned NVRs
    mentioned_nvrs = _extract_mentioned_nvrs(entry)
    if mentioned_nvrs:
        info["mentioned_nvrs"] = mentioned_nvrs

    # Query Koji for version comparison
    fix_info = _find_fix_nvr(koji, package, azl_ver)
    info.update(fix_info)

    # Build human-readable summary
    if fix_info["fix_nvr"]:
        info["removable_when"] = (
            f"Overlay can be removed when AZL updates past {fix_info['azl_tag']} "
            f"to pick up {fix_info['fix_nvr']} (available in {fix_info['fix_tag']})"
        )
    elif fix_info["azl_nvr"]:
        info["removable_when"] = (
            "Fix version not found in checked Fedora tags — "
            "may need manual verification or the fix is only in rawhide"
        )
    else:
        info["removable_when"] = (
            f"Package '{package}' not found in {fix_info['azl_tag']} — "
            "check upstream-name or package mapping"
        )

    return info


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------


def resolve_all(
    input_path: Path,
    output_path: Path,
    azl_ver: int = 43,
) -> dict[str, Any]:
    """Enrich all Backport-fedora entries with Fedora version info."""
    data = json.loads(input_path.read_text())
    koji = _koji_proxy()

    resolved_count = 0
    skipped_count = 0

    for collection_key in ("overlays", "group_entries"):
        for entry in data.get(collection_key, []):
            cl = entry.get("classification", {})
            if cl.get("top_level") != "Backport-fedora":
                continue

            print(f"Resolving: {entry.get('component', '?')} ...", file=sys.stderr)
            fix_info = resolve_entry(entry, koji, azl_ver)
            if fix_info:
                entry["fedora_fix_info"] = fix_info
                resolved_count += 1
            else:
                skipped_count += 1

    print(
        f"\nResolved {resolved_count} entries, skipped {skipped_count}",
        file=sys.stderr,
    )

    # Write enriched output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(data, indent=2) + "\n")

    return data


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Resolve Fedora package versions for Backport-fedora overlays",
    )
    parser.add_argument(
        "--input", "-i",
        type=Path,
        required=True,
        help="Classified JSON input (from classify_overlays.py or final_report.json)",
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        required=True,
        help="Output JSON with fedora_fix_info added to Backport-fedora entries",
    )
    parser.add_argument(
        "--azl-fedora-version",
        type=int,
        default=43,
        help="Fedora version AZL currently tracks (default: 43, from distro/fedora.distro.toml)",
    )
    args = parser.parse_args()
    resolve_all(args.input, args.output, args.azl_fedora_version)


if __name__ == "__main__":
    main()
