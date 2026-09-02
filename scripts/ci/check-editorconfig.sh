#!/usr/bin/env bash

set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$(git -C "$script_dir" rev-parse --show-toplevel)"

if ! command -v editorconfig-checker >/dev/null 2>&1; then
  version="$(<.editorconfig-checker-version)"
  echo "editorconfig-checker is required; install it with:" >&2
  echo "  go install github.com/editorconfig-checker/editorconfig-checker/v3/cmd/editorconfig-checker@${version}" >&2
  exit 1
fi

mapfile -d '' -t toml_files < <(git ls-files -z -- '*.toml')
if [[ ${#toml_files[@]} -eq 0 ]]; then
  echo "No tracked TOML files found."
  exit 0
fi

if [[ "${GITHUB_ACTIONS:-}" == "true" ]]; then
  # GitHub hides the annotation's file metadata in its condensed error list.
  # Repeat the path in the message so each visible error identifies its file.
  editorconfig-checker -format github-actions -- "${toml_files[@]}" |
    sed -E \
      -e 's|^::error file=([^,]+),line=([0-9]+)::|::error file=\1,line=\2::\1:\2: |' \
      -e 's|^::error file=([^:]+)::|::error file=\1::\1: |'
else
  editorconfig-checker -- "${toml_files[@]}"
fi
