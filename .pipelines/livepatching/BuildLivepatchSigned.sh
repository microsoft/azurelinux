#!/bin/bash

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e

ROOT_DIR="$(git rev-parse --show-toplevel)"

# shellcheck source=../common/libs/build_tools.sh
source "$ROOT_DIR/pipelines/common/libs/build_tools.sh"

# shellcheck source=../common/libs/file_tools.sh
source "$ROOT_DIR/pipelines/common/libs/file_tools.sh"

build_package_signed() {
    local package_cache_summary
    local package_name
    local toolkit_dir
    local use_rpms_snapshot

    package_name="$1"
    use_rpms_snapshot="$2"

    toolkit_dir="toolkit"

    if $use_rpms_snapshot
    then
        package_cache_summary="$toolkit_dir/rpms_snapshot.json"
        echo "-- Using RPMs snapshot as package cache summary."
    fi

    sudo make -C "toolkit" -j"$(nproc)" build-packages \
        CONFIG_FILE= \
        REBUILD_TOOLS=y \
        PACKAGE_BUILD_LIST="$package_name" \
        PACKAGE_CACHE_SUMMARY="$package_cache_summary" \
        SRPM_PACK_LIST="$package_name-signed" \
        SRPM_FILE_SIGNATURE_HANDLING=update \
        SPECS_DIR="../SPECS-SIGNED" \
        LOG_LEVEL=info
}

hydrate_signed_sources() {
    local kernel_modules_dir
    local livepatch_folder

    livepatch_folder="livepatch-$1"
    kernel_modules_dir="$2"
    
    cp "$kernel_modules_dir/$livepatch_folder"*/*.ko SPECS-SIGNED/"$livepatch_folder-signed"
}

verify_built_package() {
    local kernel_version
    local no_errors
    local rpm_name
    local signed_rpm_path
    local tmpdir
    local unsigned_rpm_path

    kernel_version="$1"
    tmpdir="$2"

    while IFS= read -r -d '' signed_rpm_path
    do
        rpm_name="$(basename "$signed_rpm_path")"

        echo "Verifying RPM ($rpm_name)."

        unsigned_rpm_path="$(find "$tmpdir" -name "$rpm_name" -print -quit)"
        if [[ -z "$unsigned_rpm_path" ]]
        then
            echo "ERROR: RPM ($rpm_name) not found in the unsigned version." >&2
            no_errors=false
            continue
        fi

        if ! command_diff "rpm -qp --provides" "$unsigned_rpm_path" "$signed_rpm_path" || \
           ! command_diff "rpm -qp --requires" "$unsigned_rpm_path" "$signed_rpm_path" || \
           ! command_diff "rpm -qlp" "$unsigned_rpm_path" "$signed_rpm_path"
        then
            no_errors=false
        fi
    done < <(find "out/RPMS" -name "livepatch-$kernel_version*.rpm" -and -not -name "*debuginfo*" -print0)

    ${no_errors:-true}
}

# Script parameters:
#
# -a -> input artifacts directory path
# -k -> kernel version to be livepatched
# -l -> published logs directory path
# -o -> built artifacts' output directory path
# -s -> use toolkit's RPMs snapshot to populate the packages cache
while getopts "a:k:l:o:s:" OPTIONS
do
  case "${OPTIONS}" in
    a ) ARTIFACTS_DIR=$OPTARG ;;
    k ) KERNEL_VERSION=$OPTARG ;;
    l ) LOG_PUBLISH_DIR=$OPTARG ;;
    o ) ARTIFACTS_OUTPUT_DIR=$OPTARG ;;
    s ) USE_RPMS_SNAPSHOT="$(parse_pipeline_boolean "$OPTARG")" ;;

    \? )
        echo "ERROR: Invalid Option: -$OPTARG" 1>&2
        exit 1
        ;;
    : )
        echo "ERROR: Invalid Option: -$OPTARG requires an argument" 1>&2
        exit 1
        ;;
  esac
done

print_variables_with_check ARTIFACTS_DIR KERNEL_VERSION LOG_PUBLISH_DIR ARTIFACTS_OUTPUT_DIR USE_RPMS_SNAPSHOT

TEMP_DIR="$(mktemp -d)"
trap temp_dir_cleanup EXIT

overwrite_toolkit -t "$ARTIFACTS_DIR"

hydrate_artifacts -r "$ARTIFACTS_DIR" -s "$ARTIFACTS_DIR"

# Saving the unsigned version for the sake of comparing with the signed one after it's built.
find "out/RPMS" -name "livepatch-$KERNEL_VERSION*.rpm" -and -not -name "*debuginfo*" -exec mv {} "$TEMP_DIR" \;

hydrate_signed_sources "$KERNEL_VERSION" "$ARTIFACTS_DIR"

# Making sure we publish build logs even if the build fails.
build_package_signed "livepatch-$KERNEL_VERSION" "$USE_RPMS_SNAPSHOT" || BUILD_SUCCEEDED=false

publish_build_logs "$LOG_PUBLISH_DIR"

publish_build_artifacts "$ARTIFACTS_OUTPUT_DIR"

${BUILD_SUCCEEDED:-true}

verify_built_package "$KERNEL_VERSION" "$TEMP_DIR"
