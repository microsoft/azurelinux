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
set -eu

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

exit_usage() {
    echo "Usage: $0 [flags]"
    echo ""
    echo "Flags:"
    echo "  --srcTarball    src tarball file. If not provided, it will be downloaded according to the spec file."
    echo "  --outFolder     folder where to copy the new tarball(s). If not provided, the tarballs will be copied to the same folder as the script."
    echo "  --pkgVersion    package version. If not provided, it will be extracted from the spec file."
    echo "  --setSignature  set the signature of the tarball(s) in the signatures.json file."
    exit 2
}

arg_out_folder=""
arg_src_tarball=""
arg_pkg_version=""
arg_set_signatures=0
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            exit_usage
            ;;
        --outFolder)
            # Convert to absolute path
            arg_out_folder=$(readlink -f "$2")
            shift
            ;;
        --srcTarball)
            arg_src_tarball="$2"
            shift
            ;;
        --pkgVersion)
            arg_pkg_version="$2"
            shift
            ;;
        --setSignature)
            arg_set_signatures=1
            ;;
        -*)
            echo "Error: Unknown option: $1"
            exit_usage
            ;;
        *)
            echo "Error: Unknown argument: $1"
            exit_usage
            ;;
    esac

    shift
done

script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

out_folder="$arg_out_folder"
if [[ -z "$out_folder" ]]; then
    out_folder="$script_dir"
elif [[ ! -d "$out_folder" ]]; then
    echo "Error: The output folder does not exist."
    exit 1
fi

spec_file=$(ls "$script_dir"/*.spec)

src_tarball="$arg_src_tarball"
if [[ -z "$src_tarball" ]]; then
    src_url=$(get_spec_value "$spec_file" "Source0")
    if [[ -z "$src_url" ]]; then
        echo "Error: Unable to determine the source0 URL from the spec file."
        exit 1
    fi

    src_tarball_name=$(echo "$src_url" | grep -oP '(?<=#/)[^/]+')
    if [[ -z "$src_tarball_name" ]]; then
        echo "Error: Unable to determine the source0 tarball name from the source URL."
        exit 1
    fi

    src_tarball="$script_dir/$src_tarball_name"
    if [[ ! -f "$src_tarball" ]]; then
        wget -O "$src_tarball" "$src_url"
    fi
elif [[ ! -f "$src_tarball" ]]; then
    echo "Error: The source tarball file does not exist."
    exit 1
fi

pkg_name=$(get_spec_value "$spec_file" "Name")
if [[ -z "$pkg_name" ]]; then
    echo "Error: Unable to determine the package name from the spec file."
    exit 1
fi

pkg_version="$arg_pkg_version"
if [[ -z "$pkg_version" ]]; then
    pkg_version=$(get_spec_value "$spec_file" "Version")
    if [[ -z "$pkg_version" ]]; then
        echo "Error: Unable to determine the package version from the spec file."
        exit 1
    fi
fi

# Extract the source tarball and generate the vendor tarball.
source_dir=$(mktemp -d)
trap "rm -rf '$source_dir'" EXIT
tar -C "$source_dir" -xf "$src_tarball"
cd "$source_dir"/*
go mod vendor
vendor_tarball="$out_folder/$pkg_name-$pkg_version-vendor.tar.gz"
tar --sort=name \
    --mtime="2021-04-26 00:00Z" \
    --owner=0 \
    --group=0 \
    --numeric-owner \
    --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
    -c \
    -f "$vendor_tarball" \
    vendor

if [[ $arg_set_signatures -eq 1 ]]; then
    signatures_file=$(ls "$script_dir"/*.signatures.json)
    set_signature_value "$signatures_file" "$src_tarball"
    set_signature_value "$signatures_file" "$vendor_tarball"
fi

echo "Vendor tarball generated: $vendor_tarball"
