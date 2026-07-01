#!/usr/bin/env bash
# Compute a per-PR "change set" of components: the union of components
# flagged by `azldev component changed` (input fingerprint differs) and
# components whose rendered spec tree was hand-edited.
#
# Writes three files into <output-dir>:
#   changed-components.json  - full output of `azldev component changed`
#   specs-diff.txt           - `git diff --name-only` under the rendered specs dir
#   render-set.txt           - newline-delimited component names (the union,
#                              minus deleted components; azldev dedupes
#                              internally if a caller passes duplicates).
#
# Intended to run inside an azldev container with the PR head checked out
# at the current working directory. Callers handle log grouping and
# artifact publication. `azldev` is invoked with inline `AZLDEV_ALLOW_ROOT=1`
# prefixes so CI agents running as root are accommodated without callers
# having to lift the restriction at step scope (see
# .github/instructions/ado-pipeline.instructions.md).

set -euo pipefail

# Ensure we run from repo root -- realpath --relative-to below and git diff
# --name-only both assume repo-root-relative paths.
cd "$(git rev-parse --show-toplevel)"

usage() {
  echo "Usage: $0 --output-dir DIR --from-commit SHA --to-commit SHA \\" >&2
  echo "          [--changed-components-file NAME] [--specs-diff-file NAME] [--render-set-file NAME]" >&2
  echo "  --from-commit  baseline commit (merge-base / fork point)" >&2
  echo "  --to-commit    newer commit (e.g. PR head)" >&2
  exit 1
}

# Output file names default to the canonical set but can be overridden by a
# caller that needs to control them (e.g. to stage several change sets side by
# side). Only the names are configurable; they always land under --output-dir.
changed_components_file_name="changed-components.json"
specs_diff_file_name="specs-diff.txt"
render_set_file_name="render-set.txt"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --output-dir)              output_dir="$2"; shift 2 ;;
    --from-commit)             from_commit="$2"; shift 2 ;;
    --to-commit)               to_commit="$2"; shift 2 ;;
    --changed-components-file) changed_components_file_name="$2"; shift 2 ;;
    --specs-diff-file)         specs_diff_file_name="$2"; shift 2 ;;
    --render-set-file)         render_set_file_name="$2"; shift 2 ;;
    *) usage ;;
  esac
done
[[ -z "${output_dir:-}" || -z "${from_commit:-}" || -z "${to_commit:-}" ]] && usage

# Defensive guard: the script owns --output-dir exclusively for the duration
# of the invocation (it does `rm -rf` below to clean up stale state). Refuse
# obviously-dangerous paths so a future caller passing an empty-after-
# expansion var (e.g. `${ADO_VAR:-}`) or a typoed path can't wipe something
# they didn't mean to. Today's callers (GH:/output/change-set,
# CT:$(Build.ArtifactStagingDirectory)/change-set) are safe; this is
# hygiene for the next caller.
case "$output_dir" in
  /|/usr|/etc|/var|/home|/root|/boot|/bin|/sbin|/lib|/lib64|/opt|/srv|/tmp|.|..|"")
    echo "refusing dangerous --output-dir: '$output_dir'" >&2
    exit 2
    ;;
esac

# Clean the output dir up front so a partial previous run cannot mix its
# stale specs-diff.txt or render-set.txt into this invocation. CI gets a
# fresh container per run, but local-dev / ADO agent retries can hit this.
rm -rf "$output_dir"
mkdir -p "$output_dir"

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

changed_file="$output_dir/$changed_components_file_name"
specs_diff_file="$output_dir/$specs_diff_file_name"
render_set_file="$output_dir/$render_set_file_name"

# Compute the set of changed components between two commits. Writes one JSON
# entry per component to $out_file with fields: component, changeType,
# sourcesChange. azldev hard-fails if any component has sourcesChange == true
# without a corresponding identity change (added/changed/deleted) -- a
# supply-chain drift guard. Inline AZLDEV_ALLOW_ROOT=1 so CI agents running as
# root work without lifting the restriction at step scope (see
# .github/instructions/ado-pipeline.instructions.md).
compute_changed() {
  local out_file="$1" from="$2" to="$3"
  mkdir -p "$(dirname "$out_file")"
  AZLDEV_ALLOW_ROOT=1 azldev component changed --from "$from" --to "$to" \
    -a --include-unchanged -O json > "$out_file"
  echo "Changed components (non-unchanged):"
  jq -r '.[] | select(.changeType != "unchanged") | "  \(.changeType)\t\(.component)"' "$out_file" | sort
}

compute_changed "$changed_file" "$from_commit" "$to_commit"

# azldev's renderedSpecsDir is absolute. Translate to repo-relative so it
# matches git's output (`git diff --name-only` always emits repo-relative
# paths regardless of the path-arg form).
specs_dir_abs="$(AZLDEV_ALLOW_ROOT=1 azldev config dump -q -f json | jq -r '.project.renderedSpecsDir')"
specs_dir="$(realpath --relative-to="$(pwd)" "$specs_dir_abs")"

# Capture the spec-tree diff so the render set can include components whose
# rendered specs were edited directly (which the input-fingerprint view in
# `azldev component changed` misses). --no-renames prevents collapse of
# delete+add into a rename entry, which would lose the old path; the
# Python script filters out deleted/unknown components.
git diff --no-renames --name-only "$from_commit" "$to_commit" \
  -- "$specs_dir" > "$specs_diff_file"

python3 "$script_dir/compute_render_set.py" \
  --changed-components-file "$changed_file" \
  --specs-diff-file "$specs_diff_file" \
  --specs-dir "$specs_dir" \
  > "$render_set_file"

count=$(wc -l < "$render_set_file" | tr -d ' ')
echo "Render set: $count component(s)"
if [[ "$count" -gt 0 ]]; then
  sed 's/^/  - /' "$render_set_file"
fi
