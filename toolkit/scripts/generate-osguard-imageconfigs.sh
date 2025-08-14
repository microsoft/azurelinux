#!/usr/bin/env bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Generates osguard image configurations by merging base + delta YAML templates.
# Usage:
#   ./generate-osguard-imageconfigs.sh [output-directory]
#     output-directory (optional): directory to write the generated files into.
#       If omitted, defaults to ../imageconfigs relative to this script's CWD.
#
# Optional env:
#   PYTHON   - Python executable to use (default: python3)
#
set -euo pipefail

# This script uses relative paths from the current working directory.
# Run it from toolkit/scripts.

PYTHON_BIN=${PYTHON:-python3}

# Optional first arg: override output directory
OUT_DIR_DEFAULT="../imageconfigs"
OUT_DIR="${1:-$OUT_DIR_DEFAULT}"

# Ensure merge_yaml.py is available in the current directory
if [[ ! -f ./merge_yaml.py ]]; then
	echo "Error: merge_yaml.py not found in the current directory." >&2
	echo "Hint: run this script from the directory containing merge_yaml.py (e.g., toolkit/scripts)." >&2
	exit 2
fi

BASE_TPL="../imageconfigs/templates/osguard-base.yaml"
DELTA_TPL="../imageconfigs/templates/osguard-no-ci-delta.yaml"

# Ensure output directory exists
mkdir -p "$OUT_DIR"

OUT_STD="$OUT_DIR/osguard-amd64.yaml"

echo "Generating osguard configs..."
echo "Output directory: $OUT_DIR"
"$PYTHON_BIN" ./merge_yaml.py "$BASE_TPL" "$DELTA_TPL" -o "$OUT_STD"

echo "Done. Wrote:"
echo "  $OUT_STD"
