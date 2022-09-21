#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e

REPO_ROOT="$(git rev-parse --show-toplevel)"
SCRIPT_FOLDER="$(realpath "$(dirname "${BASH_SOURCE[0]}")")"
COMMON_SCRIPTS_FOLDER="$REPO_ROOT/toolkit/scripts"

# shellcheck source=../../../toolkit/scripts/rpmops.sh
source "$REPO_ROOT/toolkit/scripts/rpmops.sh"

KERNEL_SPECS_DIR="$REPO_ROOT/SPECS/kernel"
KERNEL_CONFIG_PATH="$KERNEL_SPECS_DIR/config"
KERNEL_PUBLIC_KEYS=("$KERNEL_SPECS_DIR"/cbl-mariner-ca-*.pem)
KERNEL_PUBLIC_KEY_PATH="${KERNEL_PUBLIC_KEYS[0]}"
KERNEL_PUBLIC_KEY_FILE="$(basename "$KERNEL_PUBLIC_KEY_PATH")"
KERNEL_SIGNATURES_PATH="$KERNEL_SPECS_DIR/kernel.signatures.json"
KERNEL_SPEC_PATH="$KERNEL_SPECS_DIR/kernel.spec"

LIVEPATCH_SPECS_DIR="$REPO_ROOT/SPECS/livepatch"

KERNEL_VERSION="$(mariner_rpmspec -q --queryformat="%{VERSION}\n" --srpm "$KERNEL_SPEC_PATH" 2>/dev/null)"
KERNEL_VERSION_RELEASE="$(mariner_rpmspec -q --queryformat="%{VERSION}-%{RELEASE}\n" --srpm "$KERNEL_SPEC_PATH" 2>/dev/null)"

echo "Generating empty livepatch spec for kernel ($KERNEL_VERSION_RELEASE) under ($LIVEPATCH_SPECS_DIR)."

mkdir -p "$REPO_ROOT/SPECS/livepatch"

LIVEPATCH_CONFIG_FILE_NAME="config-$KERNEL_VERSION_RELEASE"
LIVEPATCH_PUBLIC_KEY_FILE="mariner-$KERNEL_VERSION_RELEASE.pem"

echo "Copying kernel config ($LIVEPATCH_CONFIG_FILE_NAME) and trusted key ($LIVEPATCH_PUBLIC_KEY_FILE)."

cp "$KERNEL_CONFIG_PATH" "$LIVEPATCH_SPECS_DIR/$LIVEPATCH_CONFIG_FILE_NAME"
cp "$KERNEL_PUBLIC_KEY_PATH" "$LIVEPATCH_SPECS_DIR/$LIVEPATCH_PUBLIC_KEY_FILE"

echo "Generating signatures."

KERNEL_TARBALL_FILE="kernel-$KERNEL_VERSION.tar.gz"
CONFIG_HASH="$(jq -r ".Signatures.config" "$KERNEL_SIGNATURES_PATH")"
KERNEL_HASH="$(jq -r ".Signatures.\"$KERNEL_TARBALL_FILE\"" "$KERNEL_SIGNATURES_PATH")"
PUBLIC_KEY_HASH="$(jq -r ".Signatures.\"$KERNEL_PUBLIC_KEY_FILE\"" "$KERNEL_SIGNATURES_PATH")"
jq -n \
    --arg config_hash "$CONFIG_HASH" \
    --arg config_name "$LIVEPATCH_CONFIG_FILE_NAME" \
    --arg kernel_hash "$KERNEL_HASH" \
    --arg kernel_name "$KERNEL_TARBALL_FILE" \
    --arg pem_hash "$PUBLIC_KEY_HASH" \
    --arg pem_name "$LIVEPATCH_PUBLIC_KEY_FILE" \
    '{"Signatures": {($config_name): $config_hash, ($kernel_name): $kernel_hash, ($pem_name): $pem_hash}}' \
    > "$LIVEPATCH_SPECS_DIR/livepatch-$KERNEL_VERSION_RELEASE.signatures.json"

LIVEPATCH_SPEC_NAME="livepatch-$KERNEL_VERSION_RELEASE.spec"
LIVEPATCH_SPEC_PATH="$LIVEPATCH_SPECS_DIR/$LIVEPATCH_SPEC_NAME"

echo "Generating the new livepatch spec ($LIVEPATCH_SPEC_NAME)."

sed "s/@KERNEL_VERSION_RELEASE@/$KERNEL_VERSION_RELEASE/" "$SCRIPT_FOLDER/template_livepatch.spec" > "$LIVEPATCH_SPEC_PATH"
"$COMMON_SCRIPTS_FOLDER"/update_spec.sh "Original version for CBL-Mariner.\n- License verified." "$LIVEPATCH_SPEC_PATH" 1>/dev/null
