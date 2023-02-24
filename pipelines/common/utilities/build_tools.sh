#!/bin/bash

change_github_branch() {
    local git_branch
    local pr_number
    local repo_dir

    git_branch="$1"
    repo_dir="$2"

    if [[ -z "$repo_dir" ]]
    then
        repo_dir="."
    fi

    if [[ $git_branch == PR-* ]]
    then
        pr_number=${git_branch#"PR-"}
        git_branch="refs/pull/${pr_number}/head"
    fi

    echo "-- Changing branch to '$git_branch'."

    git -C "$repo_dir" fetch --depth 1 origin "$git_branch"
    git -C "$repo_dir" checkout FETCH_HEAD

    # Display the current commit
    git -C "$repo_dir" log -1
}

clone_github_repo() {
    local git_branch
    local git_url
    local pr_number
    local repo_dir

    git_branch="$1"
    git_url="$2"
    repo_dir="$3"

    if [[ -z "$repo_dir" ]]
    then
        repo_dir="$(basename "$git_url" .git)"
    fi

    echo "-- Cloning '$git_branch' from '$git_url'."

    git clone --depth 1 "$git_url" "$repo_dir"

    change_github_branch "$git_branch" "$repo_dir"
}

hydrate_cache() {
    local make_status
    local repo_dir
    local rpms_archive
    local toolchain_archive
    local toolkit_dir

    repo_dir="$1"
    toolchain_archive="$2"
    rpms_archive="$3"

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

    repo_dir="$1"
    toolkit_tarball="$2"

    echo "-- Extracting toolkit from '$toolkit_tarball' into '$repo_dir'."
    rm -rf "$repo_dir/toolkit"
    tar -C "$repo_dir" -xf "$toolkit_tarball"
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

print_variables_with_check() {
    for arg_name in "$@"
    do
        if [[ -n ${!arg_name} ]]
        then
            print_variable "$arg_name"
        else
            echo "ERROR: Argument '$arg_name' is required." >&2
            return 1
        fi
    done
}

publish_build_artifacts() {
    local artifact_publish_dir
    local make_status
    local repo_dir
    local toolkit_dir
    local out_dir

    repo_dir="$1"
    artifact_publish_dir="$2"

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

    repo_dir="$1"
    logs_publish_dir="$2"

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
