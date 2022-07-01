#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Helper functions for working with RPM tools in Mariner's context.

REPO_ROOT="$(git rev-parse --show-toplevel)"

# Additional macros required to parse spec files.
DEFINES=(-D "with_check 1" -D "dist $(grep -P "DIST_TAG" "$REPO_ROOT"/toolkit/Makefile | grep -oP "\.cm\d+")")

# Mariner macro files used during spec parsing.
MACROS=()
for macro_file in "$REPO_ROOT"/SPECS/mariner-rpm-macros/macros*
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
        echo "Must pass valid spec path to 'mariner_rpmspec'!"
        return 1
    fi

    rpmspec "${DEFINES[@]}" -D "_sourcedir $sourcedir" "${MACROS[@]}" "$@"
}
