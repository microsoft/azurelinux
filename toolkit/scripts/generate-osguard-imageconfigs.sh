#!/usr/bin/env bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Generates osguard image configurations by merging base + delta YAML templates.
# Usage:
#   ./generate_osguard_configs.sh
#
# Optional env:
#   PYTHON   - Python executable to use (default: python3)
#
set -euo pipefail

# This script uses relative paths from the current working directory.
# Run it from toolkit/scripts.

PYTHON_BIN=${PYTHON:-python3}

# Ensure merge_yaml.py is available in the current directory
if [[ ! -f ./merge_yaml.py ]]; then
	echo "Error: merge_yaml.py not found in the current directory." >&2
	echo "Hint: run this script from the directory containing merge_yaml.py (e.g., toolkit/scripts)." >&2
	exit 2
fi

BASE_TPL="../imageconfigs/templates/osguard-base.yaml"
DELTA_TPL="../imageconfigs/templates/osguard-no-ci-delta.yaml"
CI_DELTA_TPL="../imageconfigs/templates/osguard-ci-delta.yaml"

OUT_STD="../imageconfigs/osguard-amd64.yaml"
OUT_CI="../imageconfigs/osguard-ci-amd64.yaml"

echo "Generating osguard configs..."
"$PYTHON_BIN" ./merge_yaml.py "$BASE_TPL" "$DELTA_TPL" -o "$OUT_STD"
"$PYTHON_BIN" ./merge_yaml.py "$BASE_TPL" "$CI_DELTA_TPL" -o "$OUT_CI"

echo "Done. Wrote:"
echo "  $OUT_STD"
echo "  $OUT_CI"
