#!/usr/bin/env python3
"""
Parse a Graphviz DOT file in the style:

digraph packages {
  "pkg";
  "pkg" -> {
    "dep1"
    "dep2"
  };
}

and generate a CSV with:
  package,dependencies,dep_count

- dependencies are pipe-separated (dep1|dep2|...)
- dep_count is the number of dependencies (direct deps only)
- packages with no "->" block get empty deps and count 0

Usage:
  python3 parse_graph_dot_to_csv.py graph.dot output.csv
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path
from typing import Dict, List


PKG_ONLY_RE = re.compile(r'^\s*"([^"]+)"\s*;\s*$')
EDGE_START_RE = re.compile(r'^\s*"([^"]+)"\s*->\s*\{\s*$')
QUOTED_NAME_RE = re.compile(r'^\s*"([^"]+)"\s*$')
EDGE_END_RE = re.compile(r'^\s*\}\s*;\s*$')


def parse_dot(text: str) -> Dict[str, List[str]]:
    deps: Dict[str, List[str]] = {}
    in_block = False
    cur_pkg = None

    for raw_line in text.splitlines():
        line = raw_line.strip()

        if not line:
            continue
        if line.startswith("//"):
            continue
        if line.startswith("digraph "):
            continue
        if line == "{":
            continue
        if line == "}":
            continue

        if not in_block:
            m_edge = EDGE_START_RE.match(raw_line)
            if m_edge:
                cur_pkg = m_edge.group(1)
                deps.setdefault(cur_pkg, [])
                in_block = True
                continue

            m_pkg = PKG_ONLY_RE.match(raw_line)
            if m_pkg:
                pkg = m_pkg.group(1)
                deps.setdefault(pkg, [])
                continue

            # ignore anything else (e.g., attributes)
            continue
        else:
            if EDGE_END_RE.match(raw_line):
                in_block = False
                cur_pkg = None
                continue

            m_dep = QUOTED_NAME_RE.match(raw_line)
            if m_dep and cur_pkg is not None:
                dep = m_dep.group(1)
                deps.setdefault(cur_pkg, [])
                deps[cur_pkg].append(dep)
                continue

            # ignore unexpected lines inside block

    # De-dup deps per package (preserve order)
    for pkg, dlist in deps.items():
        seen = set()
        out = []
        for d in dlist:
            if d not in seen:
                seen.add(d)
                out.append(d)
        deps[pkg] = out

    return deps


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python3 parse_graph_dot_to_csv.py graph.dot [output.csv]", file=sys.stderr)
        return 2

    dot_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2]) if len(sys.argv) >= 3 else Path("graph.csv")

    text = dot_path.read_text(encoding="utf-8", errors="replace")
    deps = parse_dot(text)

    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["package", "dependencies", "dep_count"])
        for pkg in sorted(deps.keys()):
            dlist = deps[pkg]
            w.writerow([pkg, "|".join(dlist), len(dlist)])

    print(f"Wrote {out_path} ({len(deps)} packages)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())