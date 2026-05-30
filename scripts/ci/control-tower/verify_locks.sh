#!/usr/bin/env bash
# Verify all lock files are up to date.
#
# Writes the lock-update JSON to <output-file> and copies it into <publish-dir>/lock-update/
# for triage artifact publication. Exits nonzero if any lock would change.

set -euo pipefail

usage() { echo "Usage: $0 --output-file FILE --publish-dir DIR" >&2; exit 1; }

while [[ $# -gt 0 ]]; do
  case "$1" in
    --output-file)  output_file="$2"; shift 2 ;;
    --publish-dir)  publish_dir="$2"; shift 2 ;;
    *) usage ;;
  esac
done
[[ -z "${output_file:-}" || -z "${publish_dir:-}" ]] && usage

# Workaround for an ADO git config error.
# The config key may not be present on every agent image, so tolerate its absence.
git config --unset extensions.worktreeConfig || true

# Full history is needed for lock resolution and spec rendering.
if [ "$(git rev-parse --is-shallow-repository)" = "true" ]; then
  echo "##[group]Fetching full git history"
  git fetch --unshallow
  echo "##[endgroup]"
fi

mkdir -p "$(dirname "$output_file")"

# Publish the lock-update JSON for post-mortem triage on EVERY exit path,
# not just success -- the failure case is exactly when this artifact
# matters most.
publish_artifact() {
  if [[ -s "$output_file" ]]; then
    mkdir -p "$publish_dir/lock-update"
    cp "$output_file" "$publish_dir/lock-update/" || true
  fi
}
trap publish_artifact EXIT

echo "##[group]Verifying lock files"
# --check-only exits nonzero if any lock is stale, without modifying the tree.
if ! AZLDEV_ALLOW_ROOT=1 azldev component update --check-only -a -q -O json > "$output_file"; then
  echo "##[endgroup]"
  echo "##[error]Lock file(s) are not up to date. Run 'azldev component update -a' and commit the result."
  echo "##[group]Drifted components"
  jq -r '.[] | select(.changed == true) | .component' "$output_file"
  echo "##[endgroup]"
  exit 1
fi
echo "##[endgroup]"
