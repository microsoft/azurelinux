#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e

REPO_ROOT="$(git rev-parse --show-toplevel)"
COMMON_SCRIPTS_FOLDER="$REPO_ROOT/toolkit/scripts"

export PATH="$PATH:$COMMON_SCRIPTS_FOLDER"

# shellcheck source=../../toolkit/scripts/specs/specs_tools.sh
source "$COMMON_SCRIPTS_FOLDER/specs/specs_tools.sh"

function update_manifests {
    local kernel_release_number
    local package_manifests_dir

    kernel_release_number="$1"

    echo "Updating package manifests."

    package_manifests_dir="$REPO_ROOT/toolkit/resources/manifests/package"
    sed -i -E "s/(kernel-headers-.*-)[0-9]+(\.cm.*)/\1$kernel_release_number\2/" "$package_manifests_dir"/{pkggen,toolchain}*.txt
}

function bump_spec_releases {
    local kernel_release_number
    local specs_dir_path
    local specs_signed_dir_path
    local specs_to_bump

    kernel_release_number="$1"

    echo "Bumping kernel specs releases to ($kernel_release_number)."

    specs_dir_path="$REPO_ROOT/SPECS"
    specs_signed_dir_path="$REPO_ROOT/SPECS-SIGNED"

    specs_to_bump="$specs_dir_path/kernel-headers/kernel-headers.spec $specs_signed_dir_path/kernel-signed/kernel-signed.spec"
    for spec_to_bump in $specs_to_bump
    do
        spec_release_number="$(spec_read_release_number "$spec_to_bump")"
        if [[ "$kernel_release_number" != "$spec_release_number" ]]
        then
            update_spec.sh "Bump release number to match kernel release." "$spec_to_bump"
        fi
    done
}

KERNEL_RELEASE_NUMBER="$(spec_read_release_number "$REPO_ROOT/SPECS/kernel/kernel.spec")"

bump_spec_releases "$KERNEL_RELEASE_NUMBER"
update_manifests "$KERNEL_RELEASE_NUMBER"
"$COMMON_SCRIPTS_FOLDER"/livepatching/update_livepatches.sh
