#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e

temp_dir=$(mktemp -d)
function clean-up {
    rm -rf "$temp_dir"
}
trap clean-up EXIT

tarball_name=$1

cache_name=${tarball_name%.*}
if [[ "$cache_name" =~ \.tar$ ]]
then
    cache_name=${cache_name%.*}
fi

cache_tarball_name="$cache_name-cargo.tar.gz"

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
    wget -q "https://cblmarinerstorage.blob.core.windows.net/sources/core/$tarball_name" -O "$temp_dir/$tarball_name"
    echo "Download successful."
fi

pushd "$temp_dir" &> /dev/null
    echo "Extracting $tarball_name."
    tar -xf "$tarball_name"
    
    pushd "$directory_name" &> /dev/null
        echo "Fetching dependencies to a temporary cache."
        CARGO_HOME=$(pwd)/.cargo cargo fetch

        echo "Compressing the cache."
        tar --sort=name --mtime="2021-04-26 00:00Z" --owner=0 --group=0 --numeric-owner --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime -cf "$cache_tarball_name" .cargo
    popd &> /dev/null
popd &> /dev/null

mv "$temp_dir/$directory_name/$cache_tarball_name" .

echo "Done:"
sha256sum "$cache_tarball_name"
