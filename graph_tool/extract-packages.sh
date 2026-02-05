#!/usr/bin/env bash
set -euo pipefail

kiwi_xml="${1:-kiwi.xml}"
out="${2:-packages.txt}"

python3 - "$kiwi_xml" > "$out" <<'PY'
import sys
import xml.etree.ElementTree as ET

path = sys.argv[1]
root = ET.parse(path).getroot()

seen = set()
for p in root.findall(".//package"):
    name = (p.get("name") or "").strip()
    if not name or name in seen:
        continue
    seen.add(name)
    print(name)
PY