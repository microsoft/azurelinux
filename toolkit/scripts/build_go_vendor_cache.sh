#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e

temp_dir=$(mktemp -d)
echo "Working in temporary directory '$temp_dir'."
function clean-up {
    echo "Cleaning up temporary directory '$temp_dir'."
    rm -rf "$temp_dir"
}
trap clean-up EXIT

tarball_name=$1

cache_name=${tarball_name%.*}
if [[ "$cache_name" =~ \.tar$ ]]
then
    cache_name=${cache_name%.*}
fi

cache_tarball_name="$cache_name-vendor.tar.gz"

if [[ $# -ge 2 ]]
then
    directory_name=$2
else
    directory_name=$cache_name
fi

if [[ -f "$tarball_name" ]]
then
    cp "$tarball_name" "$temp_dir"
else
    echo "Tarball '$tarball_name' doesn't exist. Will attempt to download from blobstorage."
    if ! wget -q "https://azurelinuxsrcstorage.blob.core.windows.net/sources/core/$tarball_name" -O "$temp_dir/$tarball_name"
    then
        echo "ERROR: failed to download the source tarball."
        exit 1
    fi
    echo "Download successful."
fi

pushd "$temp_dir" &> /dev/null
    echo "Extracting $tarball_name."
    tar -xf "$tarball_name"
    
    pushd "$directory_name" &> /dev/null
        echo "Fetching dependencies to a temporary cache."
        go mod vendor

        echo "Compressing the cache."
        tar --sort=name --mtime="2021-04-26 00:00Z" --owner=0 --group=0 --numeric-owner --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime -cf "$cache_tarball_name" vendor
    popd &> /dev/null
popd &> /dev/null

mv "$temp_dir/$directory_name/$cache_tarball_name" .

echo "Done:"
sha256sum "$cache_tarball_name"
