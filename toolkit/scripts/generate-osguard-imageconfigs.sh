#!/usr/bin/env bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Generates osguard image configurations by merging base + delta YAML templates.
# Usage:
#   ./generate-osguard-imageconfigs.sh
#   ./generate-osguard-imageconfigs.sh test
#     test: generate into a temporary directory and compare with the default
#       committed file, failing if they differ (ignores the '# Sources:' header).
#
# Optional env:
#   PYTHON   - Python executable to use (default: python3)
#
set -euo pipefail

# This script uses relative paths from the current working directory.
# Run it from toolkit/scripts.

PYTHON_BIN=${PYTHON:-python3}

# Default output directory (relative to this script's CWD)
OUT_DIR_DEFAULT="../imageconfigs"


# Ensure merge_yaml.py is available in the current directory
if [[ ! -f ./merge_yaml.py ]]; then
	echo "Error: merge_yaml.py not found in the current directory." >&2
	echo "Hint: run this script from the directory containing merge_yaml.py (e.g., toolkit/scripts)." >&2
	exit 2
fi

BASE_TPL="../imageconfigs/templates/osguard-base.yaml"
DELTA_TPL="../imageconfigs/templates/osguard-no-ci-delta.yaml"

run_generate() {
	local out_dir="$1"
	mkdir -p "$out_dir"
	local out_std="$out_dir/osguard-amd64.yaml"
	echo "Generating osguard configs..."
	echo "Output directory: $out_dir"
	"$PYTHON_BIN" ./merge_yaml.py "$BASE_TPL" "$DELTA_TPL" -o "$out_std"
	echo "Done. Wrote:"
	echo "  $out_std"
}

run_test() {
	echo "Running test: generate into temp dir and compare with default (ignoring '# Sources:' header)"
	local tmp_out_dir
	tmp_out_dir="$(mktemp -d)"
	run_generate "$tmp_out_dir"

	local generated_file default_file
	generated_file="$tmp_out_dir/osguard-amd64.yaml"
	default_file="../imageconfigs/osguard-amd64.yaml"

	echo "Comparing:"
	echo "  Generated: $generated_file"
	echo "  Default:   $default_file"

	# Filter out the variable header line that lists source paths
	local filt_gen filt_def
	filt_gen="$(mktemp)"
	filt_def="$(mktemp)"
	grep -v '^# Sources:' "$generated_file" > "$filt_gen"
	grep -v '^# Sources:' "$default_file" > "$filt_def"

	if ! diff -u "$filt_gen" "$filt_def"; then
		echo "Error: Generated osguard imageconfig differs from the committed default." >&2
		exit 1
	fi
	echo "Success: Generated osguard imageconfig matches the committed default."
}

main() {
	case "${1:-}" in
		"" )
			run_generate "$OUT_DIR_DEFAULT"
			;;
		test|--test )
			run_test
			;;
		* )
			echo "Usage: $0 [test]" >&2
			exit 2
			;;
	esac
}

main "$@"
