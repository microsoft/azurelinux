#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e

REPO_ROOT="$(git rev-parse --show-toplevel)"
COMMON_SCRIPTS_FOLDER="$REPO_ROOT/toolkit/scripts"
SCRIPT_FOLDER="$(realpath "$(dirname "${BASH_SOURCE[0]}")")"

export PATH="$PATH:$COMMON_SCRIPTS_FOLDER"

# shellcheck source=../../../toolkit/scripts/specs/specs_tools.sh
source "$COMMON_SCRIPTS_FOLDER/specs/specs_tools.sh"

function copy_kernel_sources {
    echo "Copying kernel config ($LIVEPATCH_CONFIG_FILE) and trusted key ($LIVEPATCH_PUBLIC_KEY_FILE)."

    cp "$KERNEL_CONFIG_PATH" "$LIVEPATCH_SPECS_DIR/$LIVEPATCH_CONFIG_FILE"
    cp "$KERNEL_PUBLIC_KEY_PATH" "$LIVEPATCH_SPECS_DIR/$LIVEPATCH_PUBLIC_KEY_FILE"
}

function generate_livepatch_signatures {
    local config_hash
    local kernel_hash
    local kernel_tarball_file
    local public_key_hash

    echo "Generating livepatch signatures."

    config_hash="$(jq -r ".Signatures.config" "$KERNEL_SIGNATURES_PATH")"
    kernel_tarball_file="kernel-$KERNEL_VERSION.tar.gz"
    kernel_hash="$(jq -r ".Signatures.\"$kernel_tarball_file\"" "$KERNEL_SIGNATURES_PATH")"
    public_key_hash="$(jq -r ".Signatures.\"$KERNEL_PUBLIC_KEY_FILE\"" "$KERNEL_SIGNATURES_PATH")"

    jq -n \
        --arg config_hash "$config_hash" \
        --arg config_name "$LIVEPATCH_CONFIG_FILE" \
        --arg kernel_hash "$kernel_hash" \
        --arg kernel_name "$kernel_tarball_file" \
        --arg pem_hash "$public_key_hash" \
        --arg pem_name "$LIVEPATCH_PUBLIC_KEY_FILE" \
        '{"Signatures": {($config_name): $config_hash, ($kernel_name): $kernel_hash, ($pem_name): $pem_hash}}' \
        > "$LIVEPATCH_SPECS_DIR/$LIVEPATCH_NAME.signatures.json"
}

function generate_livepatch_spec {
    local -A template_placeholders
    local latest_existing_release
    local patches
    local same_version_livepatches

    same_version_livepatches="$(find "$LIVEPATCH_SPECS_DIR" -name "livepatch-$KERNEL_VERSION*spec")"
    if [[ -n "$same_version_livepatches" ]]
    then
        echo "Detected older livepatch for the current kernel version - re-using any existing patches."

        latest_existing_release=$(find "$LIVEPATCH_SPECS_DIR" -name "livepatch-$KERNEL_VERSION*spec" | grep -oP "(?<=$KERNEL_VERSION-)\d+" | sort -n | tail -1)
        patches="$(grep -P "^\s*Patch\d*:.*" "$LIVEPATCH_SPECS_DIR/livepatch-$KERNEL_VERSION-$latest_existing_release".cm*spec)"
    fi

    # shellcheck disable=SC2034  # Variable used indirectly inside 'create_new_file_from_template'.
    template_placeholders=(
        ["@KERNEL_VERSION_RELEASE@"]="$KERNEL_VERSION_RELEASE"
        ["@PATCHES@"]="$patches"
    )
    create_new_file_from_template "$SCRIPT_FOLDER/template_livepatch.spec" "$LIVEPATCH_SPEC_PATH" template_placeholders

    update_spec.sh "Original version for Azure Linux.\n- License verified." "$LIVEPATCH_SPEC_PATH" 1>/dev/null
}

KERNEL_SPECS_DIR="$REPO_ROOT/SPECS/kernel"
KERNEL_CONFIG_PATH="$KERNEL_SPECS_DIR/config"
KERNEL_PUBLIC_KEYS=("$KERNEL_SPECS_DIR"/cbl-mariner-ca-*.pem)
KERNEL_PUBLIC_KEY_PATH="${KERNEL_PUBLIC_KEYS[0]}"
KERNEL_PUBLIC_KEY_FILE="$(basename "$KERNEL_PUBLIC_KEY_PATH")"
KERNEL_SIGNATURES_PATH="$KERNEL_SPECS_DIR/kernel.signatures.json"
KERNEL_SPEC_PATH="$KERNEL_SPECS_DIR/kernel.spec"

KERNEL_VERSION="$(spec_read_version "$KERNEL_SPEC_PATH")"
KERNEL_VERSION_RELEASE="$(spec_query_srpm "$KERNEL_SPEC_PATH" "%{VERSION}-%{RELEASE}\n")"

LIVEPATCH_CONFIG_FILE="config-$KERNEL_VERSION_RELEASE"
LIVEPATCH_PUBLIC_KEY_FILE="mariner-$KERNEL_VERSION_RELEASE.pem"
LIVEPATCH_NAME="livepatch-$KERNEL_VERSION_RELEASE"
LIVEPATCH_SPECS_DIR="$REPO_ROOT/SPECS/$LIVEPATCH_NAME"
LIVEPATCH_SPEC_PATH="$LIVEPATCH_SPECS_DIR/$LIVEPATCH_NAME.spec"

if [[ -f "$LIVEPATCH_SPEC_PATH" ]]
then
    echo "Livepatch spec ($LIVEPATCH_SPEC_PATH) already exists. Exiting."
    exit 0
fi

echo "Generating empty livepatch spec for kernel ($KERNEL_VERSION_RELEASE) under ($LIVEPATCH_SPEC_PATH)."

mkdir -p "$LIVEPATCH_SPECS_DIR"

copy_kernel_sources
generate_livepatch_signatures
generate_livepatch_spec

echo "Updating licensing info."

license_map.py --no_check --update \
    LICENSES-AND-NOTICES/SPECS/data/licenses.json \
    LICENSES-AND-NOTICES/SPECS/LICENSES-MAP.md \
    "$LIVEPATCH_SPEC_PATH"

echo "Updating the cgmanifest.json."

update_cgmanifest.py last "$REPO_ROOT/cgmanifest.json" "$LIVEPATCH_SPEC_PATH"
