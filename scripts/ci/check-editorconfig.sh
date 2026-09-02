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

args=()
if [[ "${GITHUB_ACTIONS:-}" == "true" ]]; then
  args+=(-format github-actions)
fi

editorconfig-checker "${args[@]}" -- "${toml_files[@]}"
