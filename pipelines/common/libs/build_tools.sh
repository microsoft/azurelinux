# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

hydrate_artifacts() {
    local exit_code
    local out_dir
    local repo_dir
    local rpms_archive
    local rpms_input
    local rpms_dir
    local srpms_archive
    local srpms_input
    local toolchain_archive
    local toolchain_input
    local toolkit_dir

    local OPTIND
    while getopts "cd:r:s:t:" OPTIONS
    do
        case "${OPTIONS}" in
            c ) rpms_dir="RPMS_DIR=../build/rpms_cache/cache" ;;
            d ) repo_dir="$OPTARG" ;;
            r ) rpms_input="$OPTARG" ;;
            s ) srpms_input="$OPTARG" ;;
            t ) toolchain_input="$OPTARG" ;;

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

    if [[ -z "$toolchain_input" && -z "$rpms_input" && -z "$srpms_input" ]]
    then
        echo "-- ERROR: must specify at least one of the following archives to hydrate: RPMs, SRPMs, or toolchain." >&2
        return 1
    fi

    if [[ -n "$rpms_input" ]]
    then
        rpms_archive="$(resolve_archive "$rpms_input" "*rpms.tar.gz")"
        if [[ ! -f "$rpms_archive" ]]
        then
            echo "ERROR: No RPMs archive found in '$rpms_input'." >&2
            return 1
        fi
    fi

    if [[ -n "$srpms_input" ]]
    then
        srpms_archive="$(resolve_archive "$srpms_input" "*srpms.tar.gz")"
        if [[ ! -f "$srpms_archive" ]]
        then
            echo "ERROR: No SRPMs archive found in '$srpms_input'." >&2
            return 1
        fi
    fi

    if [[ -n "$toolchain_input" ]]
    then
        toolchain_archive="$(resolve_archive "$toolchain_input" "*toolchain_built_rpms_all.tar.gz")"
        if [[ ! -f "$toolchain_archive" ]]
        then
            echo "ERROR: No toolchain archive found in '$toolchain_input'." >&2
            return 1
        fi
    fi

    repo_dir="$(resolve_repo_dir "$repo_dir")"
    out_dir="$repo_dir/out"
    toolkit_dir="$repo_dir/toolkit"

    if [[ -n "$rpms_archive" ]]
    then
        # We put the RPMs into the cache directory, so that the built RPMs directory only contains the built packages.
        echo "-- Hydrating cache of repo '$repo_dir' with RPMs from '$rpms_archive'."

        sudo make -C "$toolkit_dir" -j"$(nproc)" hydrate-rpms PACKAGE_ARCHIVE="$rpms_archive" $rpms_dir
        exit_code=$?
        if [[ $exit_code != 0 ]]; then
            echo "-- ERROR: failed to hydrate repo's RPMs." >&2
            return $exit_code
        fi
    fi

    if [[ -n "$srpms_archive" ]]
    then
        echo "-- Hydrating cache of repo '$repo_dir' with SRPMs from '$srpms_archive'."

        tar --skip-old-files -C "$out_dir" -xf "$srpms_archive"
        exit_code=$?
        if [[ $exit_code != 0 ]]; then
            echo "-- ERROR: failed to hydrate repo's SRPMs." >&2
            return $exit_code
        fi
    fi

    if [[ -n "$toolchain_archive" ]]
    then
        echo "-- Hydrating cache of repo '$repo_dir' with toolchain from '$toolchain_archive'."

        sudo make -C "$toolkit_dir" -j"$(nproc)" toolchain chroot-tools TOOLCHAIN_ARCHIVE="$toolchain_archive"
        exit_code=$?
        if [[ $exit_code != 0 ]]; then
            echo "-- ERROR: failed to hydrate repo's toolchain." >&2
            return $exit_code
        fi
    fi
}

overwrite_toolkit() {
    local repo_dir
    local toolkit_input
    local toolkit_tarball

    local OPTIND
    while getopts "d:t:" OPTIONS
    do
        case "${OPTIONS}" in
            d ) repo_dir="$OPTARG" ;;
            t ) toolkit_input="$OPTARG" ;;

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

    toolkit_tarball="$(resolve_archive "$toolkit_input" "*toolkit-*.tar.gz")"
    if [[ ! -f "$toolkit_tarball" ]]
    then
        echo "ERROR: No toolkit tarball found in '$toolkit_input'." >&2
        return 1
    fi

    repo_dir="$(resolve_repo_dir "$repo_dir")"
    toolkit_dir="$repo_dir/toolkit"

    echo "-- Extracting toolkit from '$toolkit_tarball' into '$repo_dir'."
    rm -rf "$toolkit_dir"
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

    out_dir="$repo_dir/out"
    toolkit_dir="$repo_dir/toolkit"

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

publish_toolkit() {
    local make_status
    local repo_dir
    local toolkit_dir
    local toolkit_publish_dir

    toolkit_publish_dir="$1"
    repo_dir="$(resolve_repo_dir "$2")"

    toolkit_dir="$repo_dir/toolkit"

    echo "-- Packing toolkit."
    sudo make -C "$toolkit_dir" -j"$(nproc)" REBUILD_TOOLS=y package-toolkit
    make_status=$?
    if [[ $make_status != 0 ]]; then
        echo "-- ERROR: failed to pack toolkit." >&2
        return $make_status
    fi

    echo "-- Publishing toolkit to '$toolkit_publish_dir'."
    mkdir -p "$toolkit_publish_dir"
    sudo mv "$repo_dir"/out/toolkit*.tar.gz "$toolkit_publish_dir"
}

resolve_archive() {
    local archive_path
    local archive_pattern

    archive_path="$1"
    archive_pattern="$2"

    archive_path="$(find "$archive_path" -name "$archive_pattern" -type f -print -quit)"

    if [[ -f "$archive_path" ]]
    then
        realpath "$archive_path"
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
