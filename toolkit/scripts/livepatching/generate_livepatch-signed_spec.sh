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

LIVEPATCH_SPEC_PATH="$1"

if [[ ! -f "$LIVEPATCH_SPEC_PATH" ]]
then
    echo "Must provide a livepatch spec file as first argument." >&2
    exit 1
fi

if ! grep -qP "Patch.*:.*CVE.*\.patch$" "$LIVEPATCH_SPEC_PATH"
then
    echo "Spec ($LIVEPATCH_SPEC_PATH) doesn't build any patch modules. Skipping signed spec generation."
    exit 0
fi

echo "Generating signed spec for ($LIVEPATCH_SPEC_PATH)."

KERNEL_VERSION_RELEASE="$(grep -oP "(?<=define kernel_version_release ).*" "$LIVEPATCH_SPEC_PATH")"

DESCRIPTION="$(spec_query_srpm "$LIVEPATCH_SPEC_PATH" "%{DESCRIPTION}\n")"

RELEASE_TAG="$(spec_read_release_tag "$LIVEPATCH_SPEC_PATH")"

CHANGELOG="$(dump_changelog "$LIVEPATCH_SPEC_PATH")"

# shellcheck disable=SC2034  # Variable used indirectly inside 'create_new_file_from_template'.
declare -A TEMPLATE_PLACEHOLDERS=(
    ["@KERNEL_VERSION_RELEASE@"]="$KERNEL_VERSION_RELEASE"
    ["@DESCRIPTION@"]="$DESCRIPTION"
    ["@RELEASE_TAG@"]="$RELEASE_TAG"
    ["@CHANGELOG@"]="$CHANGELOG"
)

LIVEPATCH_SIGNED_NAME="livepatch-$KERNEL_VERSION_RELEASE-signed"
LIVEPATCH_SIGNED_SPEC_PATH="$REPO_ROOT/SPECS-SIGNED/$LIVEPATCH_SIGNED_NAME/$LIVEPATCH_SIGNED_NAME.spec"
create_new_file_from_template "$SCRIPT_FOLDER/template_livepatch-signed.spec" "$LIVEPATCH_SIGNED_SPEC_PATH" TEMPLATE_PLACEHOLDERS

# Cgmanifest.json update skipped - already handled by the unsigned version.

echo "Updating licensing info."

license_map.py --no_check --update \
    LICENSES-AND-NOTICES/SPECS/data/licenses.json \
    LICENSES-AND-NOTICES/SPECS/LICENSES-MAP.md \
    "$LIVEPATCH_SIGNED_SPEC_PATH"
