#!/usr/bin/env bash
# Compute the set of changed components between source and target commits.
#
# Writes the JSON to <output-file> and copies it into <publish-dir>/changed-components/
# for triage artifact publication.
#
# 'azldev component changed' compares the source and target commits and emits
# one entry per component with its 'changeType' ('added', 'changed',
# 'unchanged', or 'deleted') plus a 'sourcesChange' flag indicating whether
# the rendered 'sources' file differs between commits.
#
# azldev hard-fails if any component has sourcesChange == true without a
# corresponding identity change (added/changed/deleted) -- supply-chain
# drift protection.
#
# Only components with sourcesChange == true AND changeType in {added, changed}
# are forwarded to Control Tower for upload.

set -euo pipefail

usage() { echo "Usage: $0 --output-file FILE --publish-dir DIR --source-commit SHA --target-commit SHA" >&2; exit 1; }

while [[ $# -gt 0 ]]; do
  case "$1" in
    --output-file)    output_file="$2"; shift 2 ;;
    --publish-dir)    publish_dir="$2"; shift 2 ;;
    --source-commit)  source_commit="$2"; shift 2 ;;
    --target-commit)  target_commit="$2"; shift 2 ;;
    *) usage ;;
  esac
done
[[ -z "${output_file:-}" || -z "${publish_dir:-}" || -z "${source_commit:-}" || -z "${target_commit:-}" ]] && usage

mkdir -p "$(dirname "$output_file")"

# Publish the changed-components JSON for post-mortem triage on EVERY exit
# path, not just success -- if azldev hard-fails on a consistency tripwire
# the partial JSON is exactly what an operator needs to investigate.
publish_artifact() {
  if [[ -s "$output_file" ]]; then
    mkdir -p "$publish_dir/changed-components"
    cp "$output_file" "$publish_dir/changed-components/" || true
  fi
}
trap publish_artifact EXIT

echo "##[group]Computing changed components"
AZLDEV_ALLOW_ROOT=1 azldev component changed --from "$target_commit" --to "$source_commit" -a --include-unchanged -O json > "$output_file"
echo "##[endgroup]"

echo "##[group]Changed components (non-unchanged only)"
jq '[.[] | select(.changeType != "unchanged")]' "$output_file"
echo "##[endgroup]"

echo "##[group]Upload set (sourcesChange == true, changeType in {added, changed})"
upload_count=$(jq -r '[.[] | select(.sourcesChange == true and (.changeType | IN("added", "changed")))] | length' "$output_file")
jq -r '.[] | select(.sourcesChange == true and (.changeType | IN("added", "changed"))) | .component' "$output_file" | sort
echo "Total: $upload_count component(s) to upload."
echo "##[endgroup]"
