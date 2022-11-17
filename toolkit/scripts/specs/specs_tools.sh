#!/bin/bash

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e

# shellcheck source=../../../toolkit/scripts/rpmops.sh
source "$(git rev-parse --show-toplevel)"/toolkit/scripts/rpmops.sh

init() {
    local init_failed=false

    if [[ -z $USER_EMAIL ]]
    then
        USER_EMAIL="$(git config user.email)"
    fi

    if [[ -z $USER_NAME ]]
    then
        USER_NAME="$(git config user.name)"
    fi

    if [[ -z $USER_EMAIL ]]
    then
        echo "ERROR: must set git user e-mail. Try running 'git config --local user.email [USER_EMAIL]'." >&2
        init_failed=true
    fi

    if [[ -z $USER_NAME ]]
    then
        echo "ERROR: must set git user name. Try running 'git config --local user.name [USER_NAME]'." >&2
        init_failed=true
    fi

    if $init_failed
    then
        exit 1
    fi
}

add_changelog_entry() {
    local changelog_header
    local changelog_indents
    local changelog_message
    local epoch
    local next_release
    local spec_path
    local version

    spec_path="$1"
    changelog_message="$2"

    next_release=$(spec_read_release_number "$spec_path")
    next_release=$((next_release+1))

    version=$(spec_read_version "$spec_path")

    epoch="$(spec_read_epoch "$spec_path"):"
    if [[ "$epoch" == "(none):" ]]
    then
        epoch=""
    fi

    changelog_header=$(date "+%a %b %d %Y $USER_NAME <$USER_EMAIL> - $epoch$version-$next_release")

    changelog_indents=$(grep -m 1 -P "^\*.*@.*>" "$spec_path" | sed -E "s/^\*(\s+).*/\1/")
    if [[ -z "$changelog_indents" ]]
    then
        changelog_indents=" "
    fi

    spec_set_release_number "$spec_path" $next_release
    sed -i -E "/\s*^%changelog.*/a *$changelog_indents$changelog_header\n-$changelog_indents$changelog_message\n" "$spec_path"
    # Remove excessive empty lines, if present.
    sed -i -e :a -e '/^\n*$/{$d;N;ba' -e '}' "$spec_path"
}

create_new_file_from_template() {
    local -n placeholders
    local key
    local target_path
    local template_path
    local value

    template_path="$1"
    target_path="$2"
    placeholders="$3"

    echo "Creating a new file under \"$target_path\" from template \"$template_path\"."

    mkdir -p "$(dirname "$target_path")"

    cp "$template_path" "$target_path"

    for key in "${!placeholders[@]}"
    do
        value="${placeholders[$key]}"
        awk -i inplace -v r="$value" "{gsub(/$key/,r)}1" "$target_path"
    done
}

dump_changelog() {
    local spec_path

    spec_path="$1"

    sed -n '/%changelog/,$p' "$spec_path"
}

parsed_spec_read_patches() {
    parsed_spec_read_tags "$1" "Patch" "$2"
}

parsed_spec_read_tag() {
    local spec_path
    local tag

    spec_path="$1"
    tag="$2"

    mariner_rpmspec --query --queryformat="%{$tag}\n" --srpm "$spec_path"
}

parsed_spec_read_tags() {
    local -n results_array
    local spec_path
    local tag

    spec_path="$1"
    tag="$2"
    results_array="$3"

    for result in $(mariner_rpmspec --query --queryformat="[%{$tag}\n]" --srpm "$spec_path" | tac)
    do
        results_array+=("$result")
    done
}

spec_query_srpm() {
    local query_format
    local spec_path

    spec_path="$1"
    query_format="$2"

    mariner_rpmspec -q --queryformat="$query_format" --srpm "$spec_path"
}

spec_read_release_number() {
    spec_read_tag_skip_macros "$1" "Release"
}

spec_read_release_tag() {
    spec_read_tag "$1" "Release"
}

spec_read_tag() {
    local spec_path
    local tag

    spec_path="$1"
    tag="$2"

    grep "^$tag:" "$spec_path" | sed -E "s/$tag:\s+([^#]+)/\1/"
}

spec_read_tag_skip_macros() {
    local spec_path
    local tag

    spec_path="$1"
    tag="$2"

    spec_read_tag "$spec_path" "$tag" | grep -oP "^[^%]+"
}

spec_read_epoch() {
    parsed_spec_read_tag "$1" "Epoch"
}

spec_read_version() {
    parsed_spec_read_tag "$1" "Version"
}

spec_set_tag() {
    local spec_path
    local tag
    local value

    spec_path="$1"
    tag="$2"
    value="$3"

    sed -i -E "s/($tag:\s+).*/\1$value/" "$spec_path"
}

spec_set_release_number() {
    local spec_path
    local value

    spec_path="$1"
    value="$2"

    spec_set_tag "$spec_path" "Release" "$value%{?dist}"
}

spec_set_version() {
    local spec_path
    local value

    spec_path="$1"
    value="$2"

    spec_set_tag "$spec_path" "Version" "$value"
}

init
