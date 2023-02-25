#!/bin/bash

hydrate_cache() {
    local make_status
    local repo_dir
    local rpms_archive
    local toolchain_archive
    local toolkit_dir

    toolchain_archive="$1"
    rpms_archive="$2"
    repo_dir="$(resolve_repo_dir "$3")"

    toolkit_dir="$repo_dir/toolkit"

    echo "-- Hydrating cache of repo '$repo_dir' with toolchain from '$toolchain_archive'."

    sudo make -C "$toolkit_dir" -j"$(nproc)" toolchain chroot-tools TOOLCHAIN_ARCHIVE="$toolchain_archive"
    make_status=$?
    if [[ $make_status != 0 ]]; then
        echo "-- ERROR: failed to hydrate repo's toolchain." >&2
        return $make_status
    fi

    if [[ -n "$rpms_archive" ]]
    then
        # We put the RPMs into the cache directory, so that the built RPMs directory only contains the built packages.
        echo "-- Hydrating cache of repo '$repo_dir' with RPMS from '$rpms_archive'."

        sudo make -C "$toolkit_dir" -j"$(nproc)" hydrate-rpms PACKAGE_ARCHIVE="$rpms_archive" RPMS_DIR="$repo_dir/build/rpms_cache/cache"
        make_status=$?
        if [[ $make_status != 0 ]]; then
            echo "-- ERROR: failed to hydrate repo's RPMs." >&2
            return $make_status
        fi
    fi
}

overwrite_toolkit() {
    local repo_dir
    local toolkit_tarball

    toolkit_tarball="$1"
    repo_dir="$(resolve_repo_dir "$2")"

    toolkit_dir="$repo_dir/toolkit"

    pushd "$repo_dir" > /dev/null || true

    echo "-- Extracting toolkit from '$toolkit_tarball' into '$repo_dir'."
    rm -rf "$toolkit_dir"
    tar -C "$repo_dir" -xf "$toolkit_tarball"

    popd > /dev/null || true
}

parse_pipeline_boolean() {
    [[ "$1" =~ [Tt]rue ]] && echo true || echo false
}

print_variable() {
    local arg_name
    local padding

    arg_name="$1"
    padding="                                      "

    printf -- "-- %s%s-> %s\n" "$arg_name" "${padding:${#arg_name}}" "${!arg_name}"
}

print_variable_with_check() {
    if [[ -n ${!1} ]]
    then
        print_variable "$arg_name"
    else
        echo "ERROR: Argument '$arg_name' is required." >&2
        return 1
    fi
}

print_variables_with_check() {
    local check_status=0

    for arg_name in "$@"
    do
        if ! print_variable_with_check "$arg_name"
        then
            check_status=1
        fi
    done

    return $check_status
}

publish_build_artifacts() {
    local artifact_publish_dir
    local make_status
    local repo_dir
    local toolkit_dir
    local out_dir

    artifact_publish_dir="$1"
    repo_dir="$(resolve_repo_dir "$2")"

    toolkit_dir="$repo_dir/toolkit"
    out_dir="$repo_dir/out"

    echo "-- Packing built RPMs and SRPMs."
    sudo make -C "$toolkit_dir" -j"$(nproc)" compress-srpms compress-rpms
    make_status=$?
    if [[ $make_status != 0 ]]; then
        echo "-- ERROR: cannot pack built RPMs and SRPMs." >&2
        return $make_status
    fi

    echo "-- Publishing built RPMs and SRPMs to '$artifact_publish_dir'."
    mkdir -p "$artifact_publish_dir"
    sudo mv "$out_dir/"{,s}rpms.tar.gz "$artifact_publish_dir"
}

publish_build_logs() {
    local logs_dir
    local logs_publish_dir
    local package_build_artifacts_dir
    local repo_dir

    logs_publish_dir="$1"
    repo_dir="$(resolve_repo_dir "$2")"

    logs_dir="$repo_dir/build/logs"
    package_build_artifacts_dir="$repo_dir/build/pkg_artifacts"

    mkdir -p "$logs_publish_dir"

    echo "-- Packing package build logs."
    if [[ -d "$logs_dir" ]]
    then
        tar -C "$logs_dir" -czf "$logs_publish_dir/pkggen.logs.tar.gz" .
    else
        echo "-- WARNING: no '$logs_dir' directory found." >&2
    fi

    echo "-- Packing package build artifacts."
    if [[ -d "$package_build_artifacts_dir" ]]
    then
        tar -C "$package_build_artifacts_dir" -czf "$logs_publish_dir/pkg_artifacts.tar.gz" .
    else
        echo "-- WARNING: no '$package_build_artifacts_dir' directory found."
    fi
}

resolve_repo_dir() {
    local repo_dir

    repo_dir="$1"

    if [[ -z "$repo_dir" ]]
    then
        repo_dir="$(git rev-parse --show-toplevel)"
    fi

    realpath "$repo_dir"
}
