#!/usr/bin/env bash
set -euo pipefail

# Output CSV columns:
#   package,direct_dependencies,dep_count_all
#
# Compatible with dnf5 repoquery (no --resolve/--alldeps needed).
#
# How it works:
# 1) Read package list from KIWI XML.
# 2) For each package:
#    - Ensure it is installed (install if missing) so rpm can query requires quickly.
#    - Direct deps:
#        rpm -qR <pkg>  -> required capabilities
#        resolve each capability to provider package name (prefer rpm --whatprovides for installed pkgs,
#        fallback to dnf repoquery --whatprovides for repo).
#    - Recursive deps: BFS using the direct-deps function over provider package names.
#
# Usage:
#   ./kiwi_dep_and_count.sh kiwi.xml [out.csv]
#
# Optional env vars:
#   TIMEOUT_SECS=30      # timeout for each dnf repoquery call
#   MAX_NODES=5000       # guardrail for recursion
#   AUTO_INSTALL=1       # install missing packages to enable rpm -qR (default 1)

in_xml="${1:-kiwi.xml}"
out_csv="${2:-kiwi_deps.csv}"

TIMEOUT_SECS="${TIMEOUT_SECS:-30}"
MAX_NODES="${MAX_NODES:-5000}"
AUTO_INSTALL="${AUTO_INSTALL:-1}"

need_cmd() { command -v "$1" >/dev/null 2>&1 || { echo "Missing required command: $1" >&2; exit 2; }; }
need_cmd python3
need_cmd rpm
need_cmd dnf
need_cmd timeout

if [[ ! -f "$in_xml" ]]; then
  echo "KIWI XML not found: $in_xml" >&2
  exit 2
fi

# Extract unique package names from kiwi.xml, preserving first-seen order.
mapfile -t pkgs < <(
  python3 - "$in_xml" <<'PY'
import sys, xml.etree.ElementTree as ET
root = ET.parse(sys.argv[1]).getroot()
seen=set(); out=[]
for p in root.findall(".//package"):
    n=(p.get("name") or "").strip()
    if n and n not in seen:
        seen.add(n); out.append(n)
print("\n".join(out))
PY
)

csv_escape() {
  local s="$1"
  s="${s//$'\r'/}"
  if [[ "$s" == *['",\n']* ]]; then
    s="${s//\"/\"\"}"
    printf '"%s"' "$s"
  else
    printf '%s' "$s"
  fi
}

# Strip version constraints from a requires line, keep the capability token.
strip_req_version() {
  sed -E 's/^[[:space:]]+|[[:space:]]+$//g; s/[[:space:]]+(>=|<=|=|<|>)[[:space:]].*$//'
}

# Cache: capability -> providers (newline-separated package names)
declare -A CAP_PROVIDERS_CACHE
# Cache: package -> direct deps (newline-separated package names)
declare -A PKG_DIRECT_CACHE

ensure_installed() {
  local pkg="$1"
  if rpm -q "$pkg" >/dev/null 2>&1; then
    return 0
  fi
  if [[ "$AUTO_INSTALL" != "1" ]]; then
    return 1
  fi
  # Best effort install (avoid docs for speed)
  sudo dnf -y install --setopt=install_weak_deps=False --setopt=tsflags=nodocs "$pkg" >/dev/null 2>&1 || return 1
}

dnf_whatprovides() {
  local cap="$1"
  timeout "$TIMEOUT_SECS" dnf -q repoquery --whatprovides "$cap" 2>/dev/null || true
}

providers_for_capability() {
  local cap="$1"

  if [[ -n "${CAP_PROVIDERS_CACHE[$cap]+x}" ]]; then
    printf '%s\n' "${CAP_PROVIDERS_CACHE[$cap]}"
    return 0
  fi

  # Prefer installed providers (fast, no network)
  local prov=""
  prov="$(
    rpm -q --whatprovides "$cap" 2>/dev/null \
      | sed '/^no package provides /d' \
      | sed '/^$/d' \
      | sed -E 's/-[0-9].*$//' \
      | sort -u || true
  )"

  # Fallback to repo providers (slower)
  if [[ -z "$prov" ]]; then
    prov="$(
      dnf_whatprovides "$cap" \
        | sed '/^$/d' \
        | sed -E 's/-[0-9].*$//' \
        | sort -u || true
    )"
  fi

  CAP_PROVIDERS_CACHE["$cap"]="$prov"
  printf '%s\n' "$prov"
}

direct_deps_for_pkg() {
  local pkg="$1"

  if [[ -n "${PKG_DIRECT_CACHE[$pkg]+x}" ]]; then
    printf '%s\n' "${PKG_DIRECT_CACHE[$pkg]}"
    return 0
  fi

  if ! ensure_installed "$pkg"; then
    PKG_DIRECT_CACHE["$pkg"]=""
    printf '\n'
    return 0
  fi

  # Get required capabilities from installed rpm, then map to provider package names
  local deps=""
  deps="$(
    rpm -qR "$pkg" 2>/dev/null \
      | sed '/^$/d' \
      | grep -v '^rpmlib(' \
      | strip_req_version \
      | sed '/^$/d' \
      | sort -u \
      | while IFS= read -r cap; do
          providers_for_capability "$cap"
        done \
      | sed '/^$/d' \
      | sort -u \
      | grep -vxF "$pkg" || true
  )"

  PKG_DIRECT_CACHE["$pkg"]="$deps"
  printf '%s\n' "$deps"
}

recursive_dep_count_for_pkg() {
  local root="$1"

  declare -A seen=()
  declare -a queue=()
  local qh=0
  local nodes=0

  while IFS= read -r dep; do
    [[ -z "$dep" ]] && continue
    if [[ -z "${seen[$dep]+x}" ]]; then
      seen["$dep"]=1
      queue+=("$dep")
    fi
  done < <(direct_deps_for_pkg "$root")

  while (( qh < ${#queue[@]} )); do
    local cur="${queue[$qh]}"
    ((qh++))

    nodes=$((nodes + 1))
    if (( nodes > MAX_NODES )); then
      # guardrail: prevent runaway in weird provider graphs
      break
    fi

    while IFS= read -r dep; do
      [[ -z "$dep" ]] && continue
      if [[ -z "${seen[$dep]+x}" ]]; then
        seen["$dep"]=1
        queue+=("$dep")
      fi
    done < <(direct_deps_for_pkg "$cur")
  done

  echo "${#seen[@]}"
}

# Write CSV
: > "$out_csv"
printf "package,direct_dependencies,dep_count_all\n" >> "$out_csv"

for pkg in "${pkgs[@]}"; do
  echo "Processing: $pkg" >&2

  mapfile -t direct < <(direct_deps_for_pkg "$pkg")

  direct_joined=""
  if [[ ${#direct[@]} -gt 0 ]]; then
    # remove empties
    tmp=()
    for d in "${direct[@]}"; do [[ -n "$d" ]] && tmp+=("$d"); done
    if [[ ${#tmp[@]} -gt 0 ]]; then
      direct_joined="$(IFS='|'; echo "${tmp[*]}")"
    fi
  fi

  dep_count_all="$(recursive_dep_count_for_pkg "$pkg")"

  printf "%s,%s,%s\n" \
    "$(csv_escape "$pkg")" \
    "$(csv_escape "$direct_joined")" \
    "$(csv_escape "$dep_count_all")" \
    >> "$out_csv"
done

echo "Wrote: $out_csv" >&2
echo "Packages processed: ${#pkgs[@]}" >&2