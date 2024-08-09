#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Best effort tool to update provides spec files with a changelog message.
# The tool read the user name and e-mail from their git configuration.

# $1 - Changelog message.
# ${@:2} - Paths to spec files to update.

REPO_ROOT="$(git rev-parse --show-toplevel)"

# shellcheck source=../../toolkit/scripts/specs/specs_tools.sh
source "$REPO_ROOT"/toolkit/scripts/specs/specs_tools.sh

changelog_message="$1"

if [[ $# -lt 2 ]]
then
    echo "ERROR: must provide at least two arguments: changelog message and the spec path(s)." >&2
    exit 1
fi

for spec_path in "${@:2}"
do
    if [[ ! -f "$spec_path" ]]
    then
        echo "ERROR: path '$spec_path' is not a file." >&2
        exit 1
    fi

    echo "Updating '$spec_path'."

    add_changelog_entry "$spec_path" "$changelog_message"
done
