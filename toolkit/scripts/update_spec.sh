#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Best effort tool to update provides spec files with a changelog message.
# The tool read the user name and e-mail from their git configuration.

# $1 - Changelog message.
# ${@:2} - Paths to spec files to update.

# shellcheck source=../../toolkit/scripts/rpmops.sh
source "$(git rev-parse --show-toplevel)"/toolkit/scripts/rpmops.sh

changelog_message="$1"

if [[ $# -lt 2 ]]
then
    echo "ERROR: must provide at least two arguments: changelog message and the spec path(s)." >&2
    exit 1
fi

user_email="$(git config user.email)"
user_name="$(git config user.name)"

if [[ -z $user_email ]]
then
    echo "ERROR: must set git user e-mail. Try running 'git config --local user.email [user_email]'." >&2
    exit 1
fi

if [[ -z $user_name ]]
then
    echo "ERROR: must set git user name. Try running 'git config --local user.name [user_name]'." >&2
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

    release=$(grep -oP "^Release:\s*\d+" "$spec_path" | grep -oP "\d+$")
    release=$((release+1))
    version=$(mariner_rpmspec --srpm -q "$spec_path" --qf "%{VERSION}\n" 2>/dev/null)

    epoch="$(mariner_rpmspec --srpm -q "$spec_path" --qf "%{EPOCH}\n" 2>/dev/null):"
    if [[ "$epoch" == "(none):" ]]
    then
        epoch=""
    fi

    sed -i -E "s/^(Release:\s*).*/\1$release%{?dist}/" "$spec_path"
    changelog_header=$(date "+%a %b %d %Y $user_name <$user_email> - $epoch$version-$release")
    changelog_indents=$(grep -m 1 -P "^\*.*@.*>" "$spec_path" | sed -E "s/^\*(\s+).*/\1/")
    if [[ -z "$changelog_indents" ]]
    then
        changelog_indents=" "
    fi
    sed -i -E "/\s*^%changelog.*/a *$changelog_indents$changelog_header\n-$changelog_indents$changelog_message\n" "$spec_path"
done
