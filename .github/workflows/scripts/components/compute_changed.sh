#!/usr/bin/env bash
# Compute the set of changed components between source and target commits.
#
# Writes one JSON entry per component to <output-file>, with fields:
#   - component:     name
#   - changeType:    'added' | 'changed' | 'unchanged' | 'deleted'
#   - sourcesChange: bool (rendered 'sources' file differs across commits)
#
# azldev hard-fails if any component has sourcesChange == true without a
# corresponding identity change (added/changed/deleted) -- supply-chain
# drift protection.
#
# Callers are responsible for log grouping and artifact publication.
# `azldev` is invoked with an inline `AZLDEV_ALLOW_ROOT=1` prefix so CI
# agents running as root work without callers having to lift the
# restriction at step scope (see
# .github/instructions/ado-pipeline.instructions.md).

set -euo pipefail

usage() { echo "Usage: $0 --output-file FILE --source-commit SHA --target-commit SHA" >&2; exit 1; }

while [[ $# -gt 0 ]]; do
  case "$1" in
    --output-file)    output_file="$2"; shift 2 ;;
    --source-commit)  source_commit="$2"; shift 2 ;;
    --target-commit)  target_commit="$2"; shift 2 ;;
    *) usage ;;
  esac
done
[[ -z "${output_file:-}" || -z "${source_commit:-}" || -z "${target_commit:-}" ]] && usage

mkdir -p "$(dirname "$output_file")"

AZLDEV_ALLOW_ROOT=1 azldev component changed --from "$target_commit" --to "$source_commit" -a --include-unchanged -O json > "$output_file"

echo "Changed components (non-unchanged):"
jq -r '.[] | select(.changeType != "unchanged") | "  \(.changeType)\t\(.component)"' "$output_file" | sort
