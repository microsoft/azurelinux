#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Helper functions for working with RPM tools in Mariner's context.

REPO_ROOT="$(git rev-parse --show-toplevel)"

RPM_SHELL="$(readlink /bin/sh)"
if [[ "$RPM_SHELL" != "bash" ]]
then
    echo "WARNING: host system's '/bin/sh' links to '$RPM_SHELL'. Mariner specs require 'bash'. Parsing specs may fail or generate unpredictable results." >&2
fi

# Additional macros required to parse spec files.
DIST_TAG=$(make -s -f $REPO_ROOT/toolkit/Makefile get-dist-tag)
RELEASE_NUM=$(make -s -f $REPO_ROOT/toolkit/Makefile get-release-major)

# Define 'azl <ver>' macro for use in spec files. Normally they would be defined in the 'azurelinux-release' package.
# Dist tag will be of the form '.<distro><ver>', e.g. '.azl3'., rease number will be of the form '3.0'.

# 'azl <ver>': Strip the leading '.' and the trailing number from the DIST_TAG
distro_name="$(echo ${DIST_TAG#.} | sed 's/[0-9]\+$//')"
distro_majver="${RELEASE_NUM%%.*}"
distro_ver="${distro_name} ${distro_majver}"

DEFINES=(-D "with_check 1" -D "dist $DIST_TAG" -D "$distro_ver")

SPECS_DIR="$REPO_ROOT/SPECS"

# Mariner macro files used during spec parsing.
MACROS=()
for macro_file in "$SPECS_DIR"/mariner-rpm-macros/macros* "$SPECS_DIR"/pyproject-rpm-macros/macros.pyproject "$SPECS_DIR"/perl/macros.perl
do
  MACROS+=("--load=$macro_file")
done

function mariner_rpmspec {
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
        echo "Must pass valid spec path to 'mariner_rpmspec'!" >&2
        return 1
    fi

    rpmspec "${MACROS[@]}" "${DEFINES[@]}" -D "_sourcedir $sourcedir" "$@"
}
