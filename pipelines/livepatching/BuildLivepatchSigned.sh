#!/bin/bash

set -e

ROOT_DIR="$(git rev-parse --show-toplevel)"

# shellcheck source=../common/libs/build_tools.sh
source "$ROOT_DIR/pipelines/common/libs/build_tools.sh"

# shellcheck source=../common/libs/file_tools.sh
source "$ROOT_DIR/pipelines/common/libs/file_tools.sh"

build_package_signed() {
    local package_name

    package_name="$1"

    sudo make -C "toolkit" -j"$(nproc)" build-packages \
        CONFIG_FILE= \
        REBUILD_TOOLS=y \
        PACKAGE_BUILD_LIST="$package_name" \
        SRPM_PACK_LIST="$package_name-signed" \
        SRPM_FILE_SIGNATURE_HANDLING=update \
        SPECS_DIR="SPECS-SIGNED" \
        LOG_LEVEL=info
}

hydrate_built_rpms() {
    local artifacts_dir
    local rpms_archive

    artifacts_dir="$1"

    rpms_archive="$(find "$artifacts_dir" -name '*rpms.tar.gz' -type f -print -quit)"
    if [[ ! -f "$rpms_archive" ]]
    then
        echo "ERROR: No RPMs archive found in '$artifacts_dir'." >&2
        return 1
    fi

    sudo make -C "toolkit" -j"$(nproc)" hydrate-rpms PACKAGE_ARCHIVE="$rpms_archive"
}

hydrate_signed_sources() {
    local kernel_modules_dir
    local livepatch_folder

    livepatch_folder="livepatch-$1"
    kernel_modules_dir="$2"
    
    cp "$kernel_modules_dir/$livepatch_folder"/*.ko SPECS-SIGNED/"$livepatch_folder-signed"
}

verify_built_package() {
    local kernel_version
    local result=0
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
            result=1
        fi

        if ! command_diff "rpm -qp --provides" "$unsigned_rpm_path" "$signed_rpm_path" || \
           ! command_diff "rpm -qp --requires" "$unsigned_rpm_path" "$signed_rpm_path" || \
           ! command_diff "rpm -qlp" "$unsigned_rpm_path" "$signed_rpm_path"
        then
            result=1
        fi
    done < <(find "out" -name "livepatch-$kernel_version*.rpm" -and -not -name "*debuginfo*" -print0)

    return "$result"
}

# Script parameters:
#
# -a -> input artifacts directory path
# -k -> kernel version to be livepatched
# -l -> published logs directory path
# -m -> signed kernel modules directory path
# -p -> published artifacts directory path
while getopts "a:k:l:m:p:" OPTIONS
do
  case "${OPTIONS}" in
    a ) ARTIFACTS_DIR=$OPTARG ;;
    k ) KERNEL_VERSION=$OPTARG ;;
    l ) LOG_PUBLISH_DIR=$OPTARG ;;
    m ) KERNEL_MODULES_DIR=$OPTARG ;;
    p ) ARTIFACTS_PUBLISH_DIR=$OPTARG ;;

    \? )
        echo "Error - Invalid Option: -$OPTARG" 1>&2
        exit 1
        ;;
    : )
        echo "Error - Invalid Option: -$OPTARG requires an argument" 1>&2
        exit 1
        ;;
  esac
done

print_variables_with_check ARTIFACTS_DIR KERNEL_VERSION LOG_PUBLISH_DIR ARTIFACTS_PUBLISH_DIR

tmpdir=$(mktemp -d)
function cleanup {
    echo "Cleaning up '$tmpdir'."
    rm -rf "$tmpdir"
}
trap cleanup EXIT

hydrate_built_rpms "$ARTIFACTS_DIR"

# Saving the unsigned version for the sake of comparing with the signed one after it's built.
find "out" -name "livepatch-$KERNEL_VERSION*.rpm" -and -not -name "*debuginfo*" -exec mv {} "$tmpdir" \;

hydrate_signed_sources "$KERNEL_VERSION" "$KERNEL_MODULES_DIR"

# Making sure we publish build logs even if the build fails.
build_package_signed "livepatch-$KERNEL_VERSION" || BUILD_SUCCEEDED=false

publish_build_logs "$LOG_PUBLISH_DIR"

publish_build_artifacts "$ARTIFACTS_PUBLISH_DIR"

${BUILD_SUCCEEDED:-true}

verify_built_package "$KERNEL_VERSION" "$tmpdir"
