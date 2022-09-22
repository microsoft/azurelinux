#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e

REPO_ROOT="$(git rev-parse --show-toplevel)"
SCRIPT_FOLDER="$(realpath "$(dirname "${BASH_SOURCE[0]}")")"

# shellcheck source=../../../toolkit/scripts/specs/specs_tools.sh
source "$REPO_ROOT/toolkit/scripts/specs/specs_tools.sh"

LIVEPATCH_SPEC_PATH="$1"

if [[ ! -f "$LIVEPATCH_SPEC_PATH" ]]
then
    echo "Must provide a livepatch spec file as first argument." >&2
    exit 1
fi

KERNEL_VERSION_RELEASE="$(grep -oP "(?<=kernel_version_release ).*" "$LIVEPATCH_SPEC_PATH")"

declare -a PATCHED_CVES
parsed_spec_read_patches "$LIVEPATCH_SPEC_PATH" PATCHED_CVES

RELEASE_TAG="$(spec_read_release_tag "$LIVEPATCH_SPEC_PATH")"

CHANGELOG="$(dump_changelog "$LIVEPATCH_SPEC_PATH")"

# shellcheck disable=SC2034  # Variable used indirectly inside 'create_new_file_from_template'.
declare -A TEMPLATE_PLACEHOLDERS=(
    ["@KERNEL_VERSION_RELEASE@"]="$KERNEL_VERSION_RELEASE"
    ["@PATCHED_CVES@"]="${PATCHED_CVES[@]}"
    ["@RELEASE_TAG@"]="$RELEASE_TAG"
    ["@CHANGELOG@"]="$CHANGELOG"
)

LIVEPATCH_SIGNED_SPEC_PATH="$REPO_ROOT/SPECS-SIGNED/livepatch-signed/livepatch-signed-$KERNEL_VERSION_RELEASE.spec"
create_new_file_from_template "$SCRIPT_FOLDER/template_livepatch-signed.spec" "$LIVEPATCH_SIGNED_SPEC_PATH" TEMPLATE_PLACEHOLDERS
