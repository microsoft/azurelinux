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
  echo "Usage: $0 --output-dir DIR --source-commit SHA --target-commit SHA" >&2
  exit 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --output-dir)     output_dir="$2"; shift 2 ;;
    --source-commit)  source_commit="$2"; shift 2 ;;
    --target-commit)  target_commit="$2"; shift 2 ;;
    *) usage ;;
  esac
done
[[ -z "${output_dir:-}" || -z "${source_commit:-}" || -z "${target_commit:-}" ]] && usage

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

changed_file="$output_dir/changed-components.json"
specs_diff_file="$output_dir/specs-diff.txt"
render_set_file="$output_dir/render-set.txt"

"$script_dir/compute_changed.sh" \
  --output-file "$changed_file" \
  --source-commit "$source_commit" \
  --target-commit "$target_commit"

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
git diff --no-renames --name-only "$target_commit" "$source_commit" \
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
