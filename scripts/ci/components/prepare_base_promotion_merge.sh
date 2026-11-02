#!/usr/bin/env bash
# Prepare the prospective merged checkout used only by the Base promotion gate.
set -euo pipefail

if [[ $# -ne 2 ]]; then
  echo "Usage: $0 BASE_COMMIT PR_HEAD_COMMIT" >&2
  exit 1
fi

base=$(git rev-parse --verify --end-of-options "$1^{commit}")
head=$(git rev-parse --verify --end-of-options "$2^{commit}")

if ! tree=$(git merge-tree --write-tree "$base" "$head"); then
  echo "ERROR: Cannot prepare the Base promotion comparison: PR does not merge cleanly with the captured target." >&2
  printf '%s\n' "$tree" >&2
  exit 1
fi

merged=$(printf '%s\n' "Temporary merge for Base promotion validation" |
  git -c user.name="Tobias Brick" -c user.email="tobiasb@microsoft.com" \
    commit-tree "$tree" -p "$base" -p "$head")
git -c core.hooksPath=/dev/null checkout --detach "$merged" >&2
printf '%s\n' "$merged"
