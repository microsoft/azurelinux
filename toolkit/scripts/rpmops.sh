#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Helper functions for working with RPM tools in Azure Linux's context.

REPO_ROOT="$(git rev-parse --show-toplevel)"

RPM_SHELL="$(readlink /bin/sh)"
if [[ "$RPM_SHELL" != "bash" ]]
then
    echo "WARNING: host system's '/bin/sh' links to '$RPM_SHELL'. Azure Linux specs require 'bash'. Parsing specs may fail or generate unpredictable results." >&2
fi

# Additional macros required to parse spec files.
DIST_TAG=$(make -s -f $REPO_ROOT/toolkit/Makefile get-dist-tag)
DISTRO_MACRO="$(make -s -f $REPO_ROOT/toolkit/Makefile printvar-DIST_VERSION_MACRO)"

DEFINES=(-D "with_check 1" -D "dist $DIST_TAG" -D "$DISTRO_MACRO")

SPECS_DIR="$REPO_ROOT/SPECS"
rpm_package_macros_file_path=""

# Check if the MACROS_FILE_PATH is already defined, and the directory exists
if [[ -z "$RPM_OPS_MACROS_DIRECTORY" ]] || [[ ! -d "$RPM_OPS_MACROS_DIRECTORY" ]]
then
    # Create a temporary directory to store the macros file, we don't want to use ./build since that is likely owned by root, but we also
    # want to re-use the same macro files if possible to avoid downloads and handle multiple concurrent versions.
    RPM_OPS_MACROS_DIRECTORY="$(mktemp -d)"
    export RPM_OPS_MACROS_DIRECTORY
fi

# We do not want to use the host's default macros. Scan the toolchain manifest for rpm-libs and use it instead.
# If this fails use the built-in macros from the host. This is the fallback option if the above generate an error.
# Note: There is a limitation. In the event that the rpm-libs package itself is updated, the macros file will still
# be the old one.
arch="$(make -s -f $REPO_ROOT/toolkit/Makefile printvar-build_arch)"
if [[ -f "$REPO_ROOT/toolkit/resources/manifests/package/toolchain_$arch.txt" ]]
then
    MACROS_PACKAGE_NAME=$(grep "rpm-libs" "$REPO_ROOT/toolkit/resources/manifests/package/toolchain_$arch.txt") || MACROS_PACKAGE_NAME=""
fi

if [[ -n $MACROS_PACKAGE_NAME ]]
then
    source_url=( $(make -s -f $REPO_ROOT/toolkit/Makefile printvar-PACKAGE_URL_LIST) )
    # We assume the 1st entry will contain the correct URL
    source_url_full=${source_url[0]}/$MACROS_PACKAGE_NAME
    # To try and disambiguate different versions of the macros files, hash the url.
    url_hash=$(echo $source_url_full | sha256sum | awk '{print $1}')
    temp_macros_file_path="$RPM_OPS_MACROS_DIRECTORY/$url_hash"

    # Check if we have the file already extracted
    if [[ ! -f "$temp_macros_file_path" ]]
    then
        echo "Downloading and extracting macros file from package '$source_url_full' to '$temp_macros_file_path'" >&2
        # Extract the macros file from the package into the macros file path.
        # Use a temporary file to avoid partial writes if the download/extract fails.
        curl -s "$source_url_full" | rpm2cpio - | cpio --quiet -i --to-stdout ./usr/lib/rpm/macros > "$temp_macros_file_path".tmp && \
            mv "$temp_macros_file_path".tmp "$temp_macros_file_path" || \
            temp_macros_file_path=""
        if [[ -z "$temp_macros_file_path" ]]
        then
            echo "Warning: Failed to extract macros file from package $MACROS_PACKAGE_NAME", using built-in defaults >&2
        fi

    fi
    rpm_package_macros_file_path="$temp_macros_file_path"
fi

# Azure Linux macro files used during spec parsing.
MACROS=()
# If we have a package macros file, we will use it for parsing the spec files instead of the built-in macros
if [[ -n $rpm_package_macros_file_path ]]
then
    # --macros is set to empty to clear the default macros, the first --load will load a replacement from $rpm_package_macros_file_path
    MACROS+=("--macros=''")
fi

# Add all macro files we know about to the list of macros to load, except cmake where we need to use the custom one.
for macro_file in $rpm_package_macros_file_path "$SPECS_DIR"/azurelinux-rpm-macros/macros* "$SPECS_DIR"/pyproject-rpm-macros/macros.pyproject "$SPECS_DIR"/perl/macros.perl
do
  MACROS+=("--load=$macro_file")
done

function azl_rpmspec {
    # Looking for spec path in the argument list to extract its directory.
    local sourcedir

    for arg in "$@"
    do
        if [[ "$arg" == *.spec && -f "$arg" ]]
        then
            sourcedir="$(dirname "$arg")"
            break
        fi
    done

    if [[ -z $sourcedir ]]
    then
        echo "Must pass valid spec path to 'azl_rpmspec'!" >&2
        return 1
    fi

    rpmspec "${MACROS[@]}" "${DEFINES[@]}" -D "_sourcedir $sourcedir" "$@"
}

function azl_rpm {
    rpm "${MACROS[@]}" "${DEFINES[@]}" "$@"
}
