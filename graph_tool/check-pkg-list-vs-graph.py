#!/usr/bin/env python3
"""
Check which packages in packages.txt are missing from the first column ("package")
of graph.csv.

Usage:
  python3 check_packages_txt_vs_graph_csv.py packages.txt graph.csv [missing.txt]

- packages.txt: one package name per line
- graph.csv: CSV produced by parse_graph_dot_to_csv.py (header must include "package")
- missing.txt (optional): file to write missing package names (one per line).
  If not provided, prints missing packages to stdout.
Exit codes:
  0: no missing packages
  1: missing packages found
  2: usage / input error
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path


def read_packages_txt(path: Path) -> list[str]:
    pkgs: list[str] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        pkgs.append(s)
    return pkgs


def read_graph_packages_csv(path: Path) -> set[str]:
    with path.open("r", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        if not r.fieldnames or "package" not in r.fieldnames:
            raise ValueError(f'CSV {path} must have a "package" column; got: {r.fieldnames}')
        out: set[str] = set()
        for row in r:
            name = (row.get("package") or "").strip()
            if name:
                out.add(name)
        return out


def main() -> int:
    if len(sys.argv) < 3:
        print(
            "Usage: python3 check_packages_txt_vs_graph_csv.py packages.txt graph.csv [missing.txt]",
            file=sys.stderr,
        )
        return 2

    packages_txt = Path(sys.argv[1])
    graph_csv = Path(sys.argv[2])
    missing_out = Path(sys.argv[3]) if len(sys.argv) >= 4 else None

    if not packages_txt.exists():
        print(f"Not found: {packages_txt}", file=sys.stderr)
        return 2
    if not graph_csv.exists():
        print(f"Not found: {graph_csv}", file=sys.stderr)
        return 2

    pkgs = read_packages_txt(packages_txt)
    graph_pkgs = read_graph_packages_csv(graph_csv)

    missing = [p for p in pkgs if p not in graph_pkgs]

    if missing_out:
        missing_out.write_text("\n".join(missing) + ("\n" if missing else ""), encoding="utf-8")
        print(f"Wrote missing list to {missing_out} ({len(missing)} missing)", file=sys.stderr)
    else:
        for p in missing:
            print(p)

    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())