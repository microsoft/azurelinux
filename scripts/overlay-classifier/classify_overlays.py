# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""Heuristic overlay classifier — applies taxonomy rules to extracted overlay data.

Reads the JSON output of extract_overlays.py, applies deterministic signal-pattern
rules from taxonomy.py, and outputs classified results with confidence scores.
Supports a classification cache for consistency across runs.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from taxonomy import RULES, Rule, Signal

# ---------------------------------------------------------------------------
# Text corpus construction
# ---------------------------------------------------------------------------


def _build_text_fields(entry: dict[str, Any]) -> dict[str, str]:
    """Build the searchable text fields for an overlay entry."""
    description = str(entry.get("description", ""))
    comments = str(entry.get("context_comments", ""))
    group_desc = str(entry.get("group_description", ""))

    git = entry.get("git", {})
    commit_header = str(git.get("commit_header", "")) if isinstance(git, dict) else ""
    commit_body = str(git.get("commit_body", "")) if isinstance(git, dict) else ""

    all_text = f"{description}\n{comments}\n{group_desc}\n{commit_header}\n{commit_body}"

    # Also expose overlay-specific fields for pattern matching
    overlay_type = str(entry.get("type", ""))
    tag = str(entry.get("tag", ""))
    value = str(entry.get("value", ""))
    regex = str(entry.get("regex", ""))
    replacement = str(entry.get("replacement", ""))

    return {
        "description": description,
        "comments": comments,
        "commit_header": commit_header,
        "commit_body": commit_body,
        "all_text": all_text,
        "overlay_type": overlay_type,
        "tag": tag,
        "value": value,
        "regex": regex,
        "replacement": replacement,
    }


# ---------------------------------------------------------------------------
# Structural checks
# ---------------------------------------------------------------------------


_STRUCTURAL_CHECKS: dict[str, object] = {}


def _register_check(name: str):  # noqa: ANN202
    """Register a structural check function by name."""

    def decorator(func):  # noqa: ANN001, ANN202
        _STRUCTURAL_CHECKS[name] = func
        return func

    return decorator


@_register_check("patch_add_without_fedora_url")
def _check_patch_add(_entry: dict[str, Any], text_fields: dict[str, str], _ctx: dict[str, Any]) -> bool:
    return text_fields["overlay_type"] == "patch-add" and "src.fedoraproject.org" not in text_fields["all_text"]


@_register_check("fix_header_without_azl_keywords")
def _check_fix_header(_entry: dict[str, Any], text_fields: dict[str, str], _ctx: dict[str, Any]) -> bool:
    header = text_fields["commit_header"].lower()
    if not header.startswith("fix("):
        return False
    azl_keywords = (
        "azure linux",
        "azurelinux",
        "azl",
        "not available",
        "not shipped",
        "disable",
        "remove",
    )
    return not any(kw in text_fields["all_text"].lower() for kw in azl_keywords)


@_register_check("remove_dep_tag")
def _check_remove_dep(_entry: dict[str, Any], text_fields: dict[str, str], _ctx: dict[str, Any]) -> bool:
    return text_fields["overlay_type"] == "spec-remove-tag" and text_fields["tag"] in ("BuildRequires", "Requires")


@_register_check("has_build_without")
def _check_build_without(_entry: dict[str, Any], _text_fields: dict[str, str], ctx: dict[str, Any]) -> bool:
    return bool(ctx.get("build_without"))


@_register_check("in_mingw_group")
def _check_mingw_group(entry: dict[str, Any], _text_fields: dict[str, str], _ctx: dict[str, Any]) -> bool:
    return entry.get("group") == "mingw-disabled"


@_register_check("in_check_skip_group")
def _check_skip_group(entry: dict[str, Any], _text_fields: dict[str, str], _ctx: dict[str, Any]) -> bool:
    return entry.get("group") == "check-skip-initial-failures"


@_register_check("has_check_skip")
def _check_has_skip(entry: dict[str, Any], _text_fields: dict[str, str], ctx: dict[str, Any]) -> bool:
    if ctx.get("check_skip"):
        return True
    config_applied = entry.get("config_applied", {})
    if isinstance(config_applied, dict):
        build = config_applied.get("build", {})
        if isinstance(build, dict):
            chk = build.get("check", {})
            if isinstance(chk, dict) and chk.get("skip"):
                return True
    return False


@_register_check("is_release_tag_overlay")
def _check_release_tag(_entry: dict[str, Any], text_fields: dict[str, str], _ctx: dict[str, Any]) -> bool:
    return text_fields["tag"] == "Release"


@_register_check("has_rhel_define")
def _check_rhel_define(_entry: dict[str, Any], _text_fields: dict[str, str], ctx: dict[str, Any]) -> bool:
    defines = ctx.get("build_defines", {})
    return isinstance(defines, dict) and "rhel" in defines


def _check_structural(
    signal: Signal,
    entry: dict[str, Any],
    text_fields: dict[str, str],
) -> bool:
    """Evaluate a structural (non-regex) signal check."""
    check = signal.structural_check
    if check is None:
        return False

    ctx = entry.get("component_context", {})
    if not isinstance(ctx, dict):
        ctx = {}

    check_fn = _STRUCTURAL_CHECKS.get(check)
    if check_fn is None:
        return False
    return check_fn(entry, text_fields, ctx)


# ---------------------------------------------------------------------------
# Signal evaluation
# ---------------------------------------------------------------------------


def _evaluate_signal(
    signal: Signal,
    entry: dict[str, Any],
    text_fields: dict[str, str],
) -> bool:
    """Check if a single signal matches the given overlay entry."""
    # Structural check
    if signal.structural_check:
        return _check_structural(signal, entry, text_fields)

    # Regex pattern check against specified fields
    if signal.pattern is None:
        return False

    for field_name in signal.fields:
        text = text_fields.get(field_name, "")
        if text and signal.pattern.search(text):
            return True

    return False


# ---------------------------------------------------------------------------
# Classification engine
# ---------------------------------------------------------------------------


def classify_entry(
    entry: dict[str, Any],
) -> dict[str, Any]:
    """Classify a single overlay or group entry using heuristic rules.

    Returns a classification dict with top_level, sub_category, confidence, matched_rules.
    """
    text_fields = _build_text_fields(entry)
    matched: list[tuple[Rule, str]] = []

    for rule in RULES:
        matched.extend((rule, signal.name) for signal in rule.signals if _evaluate_signal(signal, entry, text_fields))

    if not matched:
        return {
            "top_level": None,
            "sub_category": None,
            "confidence": "low",
            "classified_by": "heuristic",
            "matched_rules": [],
            "rationale": "No heuristic signals matched",
        }

    # Group matched rules by top-level priority
    best_rule = matched[0][0]
    matched_rule_names = list(dict.fromkeys(f"{r.name}:{s}" for r, s in matched))

    # Determine confidence (3-tier):
    #   high — single top-level + single (or no) sub-category
    #   medium — single top-level but conflicting sub-categories
    #   low — conflicting top-level signals
    top_levels = {r.top_level for r, _ in matched}
    if len(top_levels) > 1:
        confidence = "low"
    elif len(matched) == 1:
        confidence = "high"
    else:
        sub_cats = {r.sub_category for r, _ in matched if r.sub_category}
        confidence = "medium" if len(sub_cats) > 1 else "high"

    result: dict[str, Any] = {
        "top_level": best_rule.top_level.value,
        "sub_category": best_rule.sub_category.value if best_rule.sub_category else None,
        "confidence": confidence,
        "classified_by": "heuristic",
        "matched_rules": matched_rule_names,
    }

    # Build rationale from matched signals
    descriptions = []
    for rule, signal_name in matched[:3]:
        desc = f"{rule.name} (signal: {signal_name})"
        descriptions.append(desc)
    result["rationale"] = "; ".join(descriptions)

    return result


# ---------------------------------------------------------------------------
# Cache management
# ---------------------------------------------------------------------------


def _compute_fingerprint(entry: dict[str, Any]) -> str:
    """Compute a stable fingerprint for an overlay entry."""
    parts = [
        str(entry.get("component", "")),
        str(entry.get("overlay_index", "")),
        str(entry.get("description", "")),
        str(entry.get("type", "")),
        str(entry.get("group", "")),
    ]
    git = entry.get("git", {})
    if isinstance(git, dict):
        parts.append(str(git.get("commit_sha", "")))
    return hashlib.sha256("|".join(parts).encode()).hexdigest()[:16]


def _load_cache(cache_path: Path) -> dict[str, dict[str, Any]]:
    """Load classification cache. Returns fingerprint -> classification dict."""
    if not cache_path.exists():
        return {}
    try:
        data = json.loads(cache_path.read_text())
        if isinstance(data, dict):
            return data
    except (json.JSONDecodeError, OSError):
        pass
    return {}


def _save_cache(cache_path: Path, cache: dict[str, dict[str, Any]]) -> None:
    """Save classification cache."""
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(json.dumps(cache, indent=2, sort_keys=True) + "\n")


# ---------------------------------------------------------------------------
# Main classification pipeline
# ---------------------------------------------------------------------------


def classify_all(
    input_path: Path,
    output_path: Path,
    cache_path: Path | None = None,
    *,
    force_reclassify: bool = False,
) -> dict[str, Any]:
    """Run the full heuristic classification pipeline."""
    data = json.loads(input_path.read_text())

    cache: dict[str, dict[str, Any]] = {}
    if cache_path and not force_reclassify:
        cache = _load_cache(cache_path)

    stats = {
        "from_cache": 0,
        "heuristic_high": 0,
        "heuristic_medium": 0,
        "heuristic_low": 0,
    }

    # Classify overlays
    for entry in data.get("overlays", []):
        fp = _compute_fingerprint(entry)
        entry["fingerprint"] = fp

        if fp in cache and not force_reclassify:
            entry["classification"] = cache[fp]
            entry["classification"]["classified_by"] = "cache"
            stats["from_cache"] += 1
        else:
            classification = classify_entry(entry)
            entry["classification"] = classification
            cache[fp] = classification
            conf = classification["confidence"]
            stats[f"heuristic_{conf}"] += 1

    # Classify group entries
    for entry in data.get("group_entries", []):
        fp = _compute_fingerprint(entry)
        entry["fingerprint"] = fp

        if fp in cache and not force_reclassify:
            entry["classification"] = cache[fp]
            entry["classification"]["classified_by"] = "cache"
            stats["from_cache"] += 1
        else:
            classification = classify_entry(entry)
            entry["classification"] = classification
            cache[fp] = classification
            conf = classification["confidence"]
            stats[f"heuristic_{conf}"] += 1

    # Compute summary
    all_entries = data.get("overlays", []) + data.get("group_entries", [])
    by_top_level: dict[str, int] = {}
    by_sub_category: dict[str, int] = {}
    by_confidence: dict[str, int] = {}

    for entry in all_entries:
        cl = entry.get("classification", {})
        tl = cl.get("top_level") or "unclassified"
        sc = cl.get("sub_category") or "none"
        conf = cl.get("confidence") or "unknown"
        by_top_level[tl] = by_top_level.get(tl, 0) + 1
        by_sub_category[sc] = by_sub_category.get(sc, 0) + 1
        by_confidence[conf] = by_confidence.get(conf, 0) + 1

    data["summary"] = {
        "by_top_level": dict(sorted(by_top_level.items())),
        "by_sub_category": dict(sorted(by_sub_category.items())),
        "by_confidence": dict(sorted(by_confidence.items())),
        "pipeline_stats": stats,
    }

    # Write output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(data, indent=2) + "\n")

    # Update cache
    if cache_path:
        _save_cache(cache_path, cache)

    return data


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    """CLI entry point for the overlay classifier."""
    parser = argparse.ArgumentParser(description="Classify overlays using heuristic rules")
    parser.add_argument(
        "--input",
        "-i",
        type=Path,
        required=True,
        help="Input JSON file from extract_overlays.py",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        required=True,
        help="Output JSON file with classifications",
    )
    parser.add_argument(
        "--cache",
        type=Path,
        default=None,
        help="Path to classification cache file (for consistency across runs)",
    )
    parser.add_argument(
        "--force-reclassify",
        action="store_true",
        help="Ignore cache and reclassify all entries",
    )
    args = parser.parse_args()

    data = classify_all(args.input, args.output, args.cache, force_reclassify=args.force_reclassify)

    summary = data["summary"]
    print("\n=== Classification Summary ===", file=sys.stderr)
    print("\nBy top-level label:", file=sys.stderr)
    for label, count in sorted(summary["by_top_level"].items(), key=lambda x: -x[1]):
        print(f"  {label}: {count}", file=sys.stderr)
    print("\nBy sub-category:", file=sys.stderr)
    for cat, count in sorted(summary["by_sub_category"].items(), key=lambda x: -x[1]):
        if cat != "none":
            print(f"  {cat}: {count}", file=sys.stderr)
    print("\nBy confidence:", file=sys.stderr)
    for conf, count in sorted(summary["by_confidence"].items()):
        print(f"  {conf}: {count}", file=sys.stderr)
    print(f"\nPipeline stats: {json.dumps(summary['pipeline_stats'])}", file=sys.stderr)


if __name__ == "__main__":
    main()
