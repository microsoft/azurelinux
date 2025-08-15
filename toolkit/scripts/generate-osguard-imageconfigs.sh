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

declare -A AMD_VARS=(
	[delta_name]="osguard amd64"
    [base_tpl]="../imageconfigs/templates/osguard-base.yaml"
    [delta_tpl]="../imageconfigs/templates/osguard-no-ci-delta.yaml"
    [out_name]="osguard-amd64.yaml"
)

declare -A ARM_VARS=(
	[delta_name]="osguard arm64"
	[base_tpl]="../imageconfigs/templates/osguard-base.yaml"
	[delta_tpl]="../imageconfigs/templates/osguard-arm64-delta.yaml"
	[out_name]="osguard-arm64.yaml"
)


run_generate() {
	local out_dir="$1"
	mkdir -p "$out_dir"
	local out_std="$out_dir/${OUT_NAME}"
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
	generated_file="$tmp_out_dir/${OUT_NAME}"
	default_file="../imageconfigs/${OUT_NAME}"

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
		echo "Error: Generated ${DELTA_NAME} imageconfig differs from the committed default." >&2
		exit 1
	fi
	echo "Success: Generated ${DELTA_NAME} imageconfig matches the committed default."
}

main() {

	for arr in AMD_VARS ARM_VARS; do
		declare -n vars="$arr"  # 'vars' now refers to the current array

		BASE_TPL="${vars[base_tpl]}"
		DELTA_TPL="${vars[delta_tpl]}"
		OUT_NAME="${vars[out_name]}"
		DELTA_NAME="${vars[delta_name]}"

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
	done
}

main "$@"
