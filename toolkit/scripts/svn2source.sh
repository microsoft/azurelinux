#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Best effort tool to convert SVN tags into source tarballs.

# $1 - SVN tag URL.
# $2 - Tarball name.

set -e

if [ "$1" = "" ] || [ "$2" = "" ]; then
      echo "Usage: $0 REPO_URL TARBALL_NAME"
      exit 1
fi

REPO="$1"
EXPORT_DIR="$2"
TARBALL_NAME="$EXPORT_DIR.tar.gz"
MANIFEST="$(mktemp -t)"

function clean_up {
    rm -rf "$EXPORT_DIR"
    rm -f "$MANIFEST"
}
trap clean_up EXIT SIGINT SIGTERM

umask 000

svn export "$REPO" "$EXPORT_DIR"
find "$EXPORT_DIR" -type f | sed 's/^\.*\/*//'| sort > "$MANIFEST"
tar -cf "$TARBALL_NAME" \
    --sort=name \
    --mtime="2021-04-26 00:00Z" \
    --owner 0 --group 0 --numeric-owner \
    --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
    --files-from "$MANIFEST"

echo "Packed '$TARBALL_NAME'."
sha256sum "$TARBALL_NAME"
