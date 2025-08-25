#!/usr/bin/env bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Generates osguard image configurations by merging base + delta YAML templates.
# This script can be run from any directory - it automatically finds the
# required files based on its own location.
#
# Usage:
#   ./generate-osguard-imageconfigs.sh
#   ./generate-osguard-imageconfigs.sh test
#     test: generate into a temporary directory and compare all configured
#       outputs with the committed defaults, failing if they differ
#       (ignores the '# Sources:' header).
#
# To add a new output:
#   1) Create a base and delta template under "$TPL_DIR".
#   2) Add a new entry to GEN_JOBS in the form:
#        "<base-template>|<delta-template>|<output-filename>"
#      Example:
#        GEN_JOBS+=("osguard-base.yaml|osguard-myvariant-delta.yaml|osguard-myvariant-amd64.yaml")
#
# Optional env:
#   PYTHON   - Python executable to use (default: python3)
#
set -euo pipefail

# This script determines paths based on its own location, making it
# CWD-independent.

PYTHON_BIN=${PYTHON:-python3}

# Determine the script's directory and calculate paths relative to it
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT_DIR_DEFAULT="$SCRIPT_DIR/../imageconfigs"
TPL_DIR="$SCRIPT_DIR/../imageconfigs/templates"
MERGE_YAML_PATH="$SCRIPT_DIR/merge_yaml.py"

# Ensure merge_yaml.py is available
if [[ ! -f "$MERGE_YAML_PATH" ]]; then
	echo "Error: merge_yaml.py not found at expected location: $MERGE_YAML_PATH" >&2
	echo "Expected structure: toolkit/scripts/merge_yaml.py" >&2
	exit 2
fi

# Validate that the template directory exists
if [[ ! -d "$TPL_DIR" ]]; then
	echo "Error: Template directory not found: $TPL_DIR" >&2
	echo "Expected structure: toolkit/imageconfigs/templates/" >&2
	exit 2
fi

# List of generation jobs:
#   "<base-template-filename>|<delta-template-filename>|<output-filename>"
# Add new entries here to support additional outputs.
GEN_JOBS=(
	"osguard-base.yaml|osguard-no-ci-delta.yaml|osguard-amd64.yaml"
	"osguard-base.yaml|osguard-ci-delta.yaml|osguard-ci-amd64.yaml"
	"osguard-base.yaml|osguard-arm64-delta.yaml|osguard-arm64.yaml"
	"osguard-base.yaml|osguard-ci-arm64-delta.yaml|osguard-ci-arm64.yaml"
)

run_generate() {
	local out_dir="$1"
	mkdir -p "$out_dir"
	echo "Generating osguard configs..."
	echo "Output directory: $out_dir"

	local wrote_any=false
	local entry base_fn delta_fn out_fn base_path delta_path out_path
	for entry in "${GEN_JOBS[@]}"; do
		IFS='|' read -r base_fn delta_fn out_fn <<<"$entry"

		if [[ -z "$base_fn" || -z "$delta_fn" || -z "$out_fn" ]]; then
			echo "Error: GEN_JOBS entry must be 'base|delta|output', got: '$entry'" >&2
			exit 2
		fi

		# Enforce that base and delta live under TPL_DIR
		if [[ "$base_fn" = /* || "$delta_fn" = /* ]]; then
			echo "Error: base and delta template filenames must be relative to TPL_DIR ($TPL_DIR). Entry: '$entry'" >&2
			exit 2
		fi
		base_path="$TPL_DIR/$base_fn"
		delta_path="$TPL_DIR/$delta_fn"
		out_path="$out_dir/$out_fn"

		# Validate base exists
		if [[ ! -f "$base_path" ]]; then
			echo "Error: Base template not found: $base_path (job: $entry)" >&2
			exit 2
		fi
		# Warn if delta missing and skip
		if [[ ! -f "$delta_path" ]]; then
			echo "Warning: Delta template not found, skipping: $delta_path" >&2
			continue
		fi

		"$PYTHON_BIN" "$MERGE_YAML_PATH" "$base_path" "$delta_path" -o "$out_path"
		echo "  Wrote: $out_path"
		wrote_any=true
	done

	if [[ "$wrote_any" != true ]]; then
		echo "Error: No outputs were generated. Check templates list and paths." >&2
		exit 3
	fi
}

run_test() {
	echo "Running test: generate into temp dir and compare with defaults (ignoring '# Sources:' header)"
	local tmp_out_dir
	tmp_out_dir="$(mktemp -d)"
	run_generate "$tmp_out_dir"

	local entry base_fn delta_fn out_fn generated_file default_file filt_gen filt_def any_diff=false
	for entry in "${GEN_JOBS[@]}"; do
		IFS='|' read -r base_fn delta_fn out_fn <<<"$entry"
		if [[ -z "$base_fn" || -z "$delta_fn" || -z "$out_fn" ]]; then
			echo "Error: GEN_JOBS entry must be 'base|delta|output', got: '$entry'" >&2
			exit 2
		fi
		generated_file="$tmp_out_dir/$out_fn"
		default_file="$OUT_DIR_DEFAULT/$out_fn"

		if [[ ! -f "$default_file" ]]; then
			echo "Warning: Default file to compare not found, skipping: $default_file" >&2
			continue
		fi

		echo "Comparing:"
		echo "  Generated: $generated_file"
		echo "  Default:   $default_file"

		filt_gen="$(mktemp)"
		filt_def="$(mktemp)"
		grep -v '^# Sources:' "$generated_file" > "$filt_gen"
		grep -v '^# Sources:' "$default_file" > "$filt_def"

		if ! diff -u "$filt_gen" "$filt_def"; then
			any_diff=true
		fi
	done

	if [[ "$any_diff" == true ]]; then
		echo "Error: One or more generated imageconfigs differ from the committed defaults." >&2
		exit 1
	fi
	echo "Success: All generated imageconfigs match the committed defaults."
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
