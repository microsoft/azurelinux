#!/usr/bin/env bash
# Render changed specs and verify the rendered tree is clean.

set -euo pipefail

usage() { echo "Usage: $0 --output-dir DIR --changed-components-file FILE --source-commit SHA --target-commit SHA" >&2; exit 1; }

while [[ $# -gt 0 ]]; do
  case "$1" in
    --output-dir)              output_dir="$2"; shift 2 ;;
    --changed-components-file) changed_components_file="$2"; shift 2 ;;
    --source-commit)           source_commit="$2"; shift 2 ;;
    --target-commit)           target_commit="$2"; shift 2 ;;
    *) usage ;;
  esac
done
[[ -z "${output_dir:-}" || -z "${changed_components_file:-}" || -z "${source_commit:-}" || -z "${target_commit:-}" ]] && usage

# azldev's renderedSpecsDir is absolute. Translate to repo-relative
# so it matches git's output ('git diff --name-only' always emits
# repo-relative paths regardless of the path arg form).
specs_dir_abs="$(AZLDEV_ALLOW_ROOT=1 azldev config dump -q -f json | jq -r '.project.renderedSpecsDir')"
specs_dir="$(realpath --relative-to="$(pwd)" "$specs_dir_abs")"

# Capture git diff under the specs tree so the render set can
# include components whose specs were edited directly (which
# azldev's input-fingerprint view of "changed" would miss).
# --no-renames prevents collapse of delete+add into a rename
# entry which would lose the old path. The Python script
# filters out deleted/unknown components using the full
# changed-components JSON.
mkdir -p "$output_dir"
specs_diff_file="$output_dir/specs-diff.txt"
git diff --no-renames --name-only "$target_commit" "$source_commit" -- "$specs_dir" > "$specs_diff_file"

# Render set is the union of:
#   - components flagged by 'azldev component changed' (inputs differ)
#   - components whose spec tree was touched directly in the PR
changed=$(python3 .github/workflows/scripts/components/compute_render_set.py \
  --changed-components-file "$changed_components_file" \
  --specs-diff-file "$specs_diff_file" \
  --specs-dir "$specs_dir")

if [[ -z "$changed" ]]; then
  echo "No changed components -- skipping render."
else
  changed_count=$(echo "$changed" | wc -l)
  echo "Rendering $changed_count component(s) (azldev dedupes internally)..."
  echo "##[group]Render set"
  # shellcheck disable=SC2001
  echo "$changed" | sed 's/^/  - /'
  echo "##[endgroup]"
  echo "##[group]Specs rendering + verification"
  # --check-only renders to a staging area and diffs against on-disk specs.
  # Exits nonzero if any rendered file differs from what's committed.
  printf '%s\n' "$changed" | xargs -d '\n' env AZLDEV_ALLOW_ROOT=1 azldev component render --check-only --
  echo "##[endgroup]"
fi
