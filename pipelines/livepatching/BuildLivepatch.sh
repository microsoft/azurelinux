#!/bin/bash

set -e

ROOT_DIR="$(git rev-parse --show-toplevel)"

# shellcheck source=../common/utilities/build_tools.sh
source "$ROOT_DIR/pipelines/common/utilities/build_tools.sh"

build_package() {
    local repo_dir
    local package_name
    local package_cache_summary
    local toolkit_dir
    local use_rpms_snapshot

    repo_dir="$1"
    package_name="$2"
    use_rpms_snapshot="$3"

    toolkit_dir="$repo_dir/toolkit"

    if $use_rpms_snapshot
    then
        package_cache_summary="$toolkit_dir/rpms_snapshot.json"
        echo "-- Using RPMs snapshot as package cache summary."
    fi

    sudo make -C "$toolkit_dir" -j"$(nproc)" build-packages \
        CONFIG_FILE= \
        REBUILD_TOOLS=y \
        PACKAGE_BUILD_LIST="$package_name" \
        PACKAGE_CACHE_SUMMARY="$package_cache_summary" \
        SRPM_PACK_LIST="$package_name" \
        LOG_LEVEL=info
}

hydrate_build_artifacts() {
    local artifacts_dir
    local repo_dir
    local rpms_archive
    local toolchain_archive
    local toolkit_archive

    repo_dir="$1"
    artifacts_dir="$2"

    rpms_archive="$(find "$artifacts_dir" -name '*rpms.tar.gz' -type f -print -quit)"
    if [[ ! -f "$rpms_archive" ]]
    then
        echo "ERROR: No RPMs archive found in '$artifacts_dir'." >&2
        return 1
    fi

    toolchain_archive="$(find "$artifacts_dir" -name '*toolchain_built_rpms_all.tar.gz' -type f -print -quit)"
    if [[ ! -f "$toolchain_archive" ]]
    then
        echo "ERROR: No toolchain archive found in '$artifacts_dir'." >&2
        return 1
    fi

    toolkit_archive="$(find "$artifacts_dir" -name '*toolkit-*.tar.gz' -type f -print -quit)"
    if [[ ! -f "$toolkit_archive" ]]
    then
        echo "ERROR: No toolkit tarball found in '$artifacts_dir'." >&2
        return 1
    fi

    overwrite_toolkit "$repo_dir" "$toolkit_archive"
    hydrate_cache "$repo_dir" "$toolchain_archive" "$rpms_archive"
}

MARINER_REPO_DIR="CBL-Mariner"

# Script parameters:
#
# -a -> input artifacts directory path
# -b -> git branch to build from
# -k -> kernel version to be livepatched
# -l -> published logs directory path
# -p -> published artifacts directory path
# -s -> use toolkit's RPMs snapshot to populate the packages cache
while getopts "a:b:k:l:p:s:" OPTIONS; do
  case "${OPTIONS}" in
    a ) ARTIFACTS_DIR=$OPTARG ;;
    b ) GIT_BRANCH=$OPTARG ;;
    k ) KERNEL_VERSION=$OPTARG ;;
    l ) LOG_PUBLISH_DIR=$OPTARG ;;
    p ) ARTIFACT_PUBLISH_DIR=$OPTARG ;;
    s ) USE_RPMS_SNAPSHOT="$(parse_pipeline_boolean "$OPTARG")" ;;

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

print_variables_with_check ARTIFACTS_DIR GIT_BRANCH KERNEL_VERSION LOG_PUBLISH_DIR ARTIFACT_PUBLISH_DIR USE_RPMS_SNAPSHOT

change_github_branch "$GIT_BRANCH"

hydrate_build_artifacts . "$ARTIFACTS_DIR"

# Making sure we publish build logs even if the build fails.
build_package . "livepatch-$KERNEL_VERSION" "$USE_RPMS_SNAPSHOT" || BUILD_SUCCEEDED=false

publish_build_logs . "$LOG_PUBLISH_DIR"

publish_build_artifacts . "$ARTIFACT_PUBLISH_DIR"

${BUILD_SUCCEEDED:-true}
