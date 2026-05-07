"""Compute the render set: components flagged by `azldev component changed`
plus components whose spec tree was touched directly in the PR.

Emits one component name per line on stdout (azldev dedupes internally).
"""

import argparse
import json
from pathlib import Path


def _load_entries(path: Path) -> list[dict]:
    """Load the changed-components JSON."""
    return json.loads(path.read_text(encoding="utf-8"))


def _renderable_components(entries: list[dict]) -> set[str]:
    """Component names that azldev can still render (everything except deleted)."""
    return {e["component"] for e in entries if e.get("changeType") != "deleted"}


def from_changed(entries: list[dict]) -> list[str]:
    """Components from `azldev component changed` JSON.

    Includes anything that is not 'deleted' and either has a non-'unchanged'
    changeType or has sourcesChange=true (safety net).
    """
    out = []
    for e in entries:
        change_type = e.get("changeType")
        sources_change = e.get("sourcesChange") is True
        if change_type == "deleted":
            continue
        if change_type == "unchanged" and not sources_change:
            continue
        out.append(e["component"])
    return out


def from_specs_diff(path: Path, specs_dir: Path, renderable: set[str]) -> list[str]:
    """Components with any modified file under specs_dir.

    Spec layout is rigid: <specs_dir>/<first-char>/<component>/...
    so the component name is the second segment under specs_dir.

    Only components in ``renderable`` are included -- a deleted component's
    .comp.toml is gone so ``azldev component render`` would fail, and a
    path that doesn't map to any known component is noise.
    """
    prefix = str(specs_dir).rstrip("/") + "/"
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith(prefix):
            continue
        parts = line[len(prefix) :].split("/", 2)
        if len(parts) >= 2 and parts[1]:
            name = parts[1]
            if name in renderable:
                out.append(name)
    return out


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--changed-components-file", type=Path, required=True)
    p.add_argument("--specs-diff-file", type=Path, required=True)
    p.add_argument("--specs-dir", type=Path, required=True)
    args = p.parse_args()

    entries = _load_entries(args.changed_components_file)
    renderable = _renderable_components(entries)

    # Dedupe across both sources -- a component appearing in azldev's
    # changed list AND with hand-edited specs would otherwise print twice,
    # and a component with N modified spec files would print N times.
    # dict.fromkeys preserves first-seen order.
    names = dict.fromkeys([
        *from_changed(entries),
        *from_specs_diff(args.specs_diff_file, args.specs_dir, renderable),
    ])
    for name in names:
        print(name)


if __name__ == "__main__":
    main()
