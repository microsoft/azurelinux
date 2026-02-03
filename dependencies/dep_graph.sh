#!/usr/bin/env bash
set -euo pipefail

# Reads the CSV produced by the dependency script:
#   package,dependency
# (one dependency per line; dependency may be empty)
#
# Writes a NEW CSV file where each row is a parent package and we append extra columns
# for any dependency that is also a "top-level" package (i.e., appears in column 1).
#
# Output columns:
#   package,dependencies,child_1,child_1_dependencies,child_2,child_2_dependencies,...
#
# Usage:
#   ./expand_deps_csv.sh dependency_map.csv expanded_dependency_map.csv

in_csv="${1:-dependency_map.csv}"
out_csv="${2:-expanded_dependency_map.csv}"

if [[ ! -f "$in_csv" ]]; then
  echo "Input CSV not found: $in_csv" >&2
  exit 2
fi

python3 - "$in_csv" "$out_csv" <<'PY'
import csv
import sys
from collections import defaultdict

in_path = sys.argv[1]
out_path = sys.argv[2]

# Read input
rows = []
with open(in_path, newline="") as f:
  r = csv.reader(f)
  header = next(r, None)

  # Accept either with header "package,dependency" or headerless
  if header and len(header) >= 2 and header[0].strip() == "package" and header[1].strip() == "dependency":
    for row in r:
      rows.append(row)
  else:
    if header:
      rows.append(header)
    for row in r:
      rows.append(row)

# Build package order and dependency map (dedup while preserving order)
pkg_order = []
pkg_seen = set()

deps_map = defaultdict(list)
deps_seen = defaultdict(set)

for row in rows:
  if not row:
    continue
  pkg = row[0].strip()
  if not pkg:
    continue
  dep = row[1].strip() if len(row) > 1 else ""

  if pkg not in pkg_seen:
    pkg_seen.add(pkg)
    pkg_order.append(pkg)

  if dep and dep not in deps_seen[pkg]:
    deps_seen[pkg].add(dep)
    deps_map[pkg].append(dep)

# Build output rows
out_rows = []
for parent in pkg_order:
  parent_deps = deps_map.get(parent, [])
  children = [d for d in parent_deps if d in pkg_seen]

  row = [parent, "|".join(parent_deps)]
  for child in children:
    row.append(child)
    row.append("|".join(deps_map.get(child, [])))
  out_rows.append(row)

# Dynamic header based on max columns
max_cols = max((len(r) for r in out_rows), default=2)
header = ["package", "dependencies"]
i = 1
while len(header) < max_cols:
  header += [f"child_{i}", f"child_{i}_dependencies"]
  i += 1

# Write output file
with open(out_path, "w", newline="") as f:
  w = csv.writer(f)
  w.writerow(header)
  w.writerows(out_rows)

print(f"Wrote: {out_path}")
PY