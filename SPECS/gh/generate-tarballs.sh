#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
#
# This script downloads the source tarball and uses it to generate the
# vendor tarball for the gh package. It also updates the package's
# signatures.json file for both tarballs, although it doesn't account for
# version changes.
#
# Notes:
# - You require GNU tar version 1.28+.
# - The additional options passed to tar enable generation of a tarball
#   with the same hash every time regardless of the environment. See:
#   https://reproducible-builds.org/docs/archives/
# - For the value of "--mtime" we use the date "2021-04-26 00:00Z" to
#   simplify future updates.
set -eux

# get_spec_value extracts the parsed value of a tag from a spec file.
# - spec: The path to the spec file.
# - tag: The tag whose value is extracted.
# The extracted value is returned via stdout.
get_spec_value() {
    local spec="$1"
    local tag="$2"
    local tmp=$(mktemp)
    rpmspec -P "$spec" > "$tmp"
    grep -E "^${tag}:" "$tmp" | sed -E "s/^$tag:\s*//"
    rm "$tmp"
}

# set_signature_value adds or updates the value of a signature in the
# signatures.json file.
# - signatures_json: The path to the signatures.json file.
# - path: The path to the file whose signature is updated.
set_signature_value() {
    local signatures_json="$1"
    local path="$2"
    local name=$(basename "$path")
    local sum=$(sha256sum "$path" | cut -d' ' -f1)
    signatures_tmp=$(mktemp)
    jq --indent 1 ".Signatures.\"$name\" = \"$sum\"" "$signatures_json" > "$signatures_tmp"
    mv "$signatures_tmp" "$signatures_json"
}

script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
spec_file=$(ls "$script_dir"/*.spec)
signatures_file=$(ls "$script_dir"/*.signatures.json)

name=$(get_spec_value "$spec_file" "Name")
if [[ -z "$name" ]]; then
    echo "Error: Unable to determine the package name from the spec file."
    exit 1
fi

version=$(get_spec_value "$spec_file" "Version")
if [[ -z "$version" ]]; then
    echo "Error: Unable to determine the package version from the spec file."
    exit 1
fi

source_url=$(get_spec_value "$spec_file" "Source0")
if [[ -z "$source_url" ]]; then
    echo "Error: Unable to determine the source0 URL from the spec file."
    exit 1
fi

source_tarball_name=$(echo "$source_url" | grep -oP '(?<=#/)[^/]+')
if [[ -z "$source_tarball_name" ]]; then
    echo "Error: Unable to determine the source0 tarball name from the source URL."
    exit 1
fi

vendor_tarball_name=$(get_spec_value "$spec_file" "Source1")
if [[ -z "$vendor_tarball_name" ]]; then
    echo "Error: Unable to determine the source1 tarball name from the spec file."
    exit 1
fi

source_tarball="$script_dir/$source_tarball_name"
vendor_tarball="$script_dir/$vendor_tarball_name"

# Download the source tarball and calculate its sha256 sum
wget -O "$source_tarball" "$source_url"
set_signature_value "$signatures_file" "$source_tarball"

# Extract the source tarball and generate the vendor tarball and its sha256 sum
source_dir=$(mktemp -d)
trap "rm -rf '$source_dir'" EXIT
tar -C "$source_dir" -xf "$source_tarball"
cd "$source_dir"/*
go mod vendor
tar --sort=name \
    --mtime="2021-04-26 00:00Z" \
    --owner=0 \
    --group=0 \
    --numeric-owner \
    --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
    -c \
    -f "$vendor_tarball" \
    vendor
set_signature_value "$signatures_file" "$vendor_tarball"
