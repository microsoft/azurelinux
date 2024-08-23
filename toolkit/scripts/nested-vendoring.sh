#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Certain go packages contain nested modules, each with their own set of vendored dependencies.
# To ease updating the vendored sources for these nested modules, this script is used. It will
# recursively detect nested modules and vendor them all, rolling them up into one nested vendor tarball. 

set -e

# Takes two arguments: $1 - directory to search for vendors; $2 - output directory to 
# place new vendored packages in.
function vendor_all() {
  # Make output directory if needed
  if [ ! -d "$2" ]; then 
    mkdir -p "$2"
  fi
  if [ -d "$1" ]; then
    pushd "$1"
    # Loop through all the go.mod files in the current directory and its subdirectories
    for f in $(find . -name "go.mod"); do
      rel_path=$(dirname $f)
      pushd $rel_path > /dev/null
      mkdir -p "$2/$rel_path/vendor"
      go mod vendor -o "$2/$rel_path/vendor"
      popd > /dev/null
    done
    # Restore the original directory
    popd
  else
    echo "Invalid directory: $1"
    return 1
  fi
}

function show_help() {
  echo "First, wget and unpack the new source tar in the destination folder (e.g. SPECS/cert-manager)"
  echo "sudo ./toolkit/scripts/nested-vendoring -n cert-manager -v 1.13.3 -d ./SPECS/cert-manager"
}

# defaults from original package that needed it
PKG_NAME=""
DESIRED_VERSION=""
LOCATION=""

while getopts "hv:n:d:" opt; do
  case "$opt" in
    h)
      show_help
      exit 0
      ;;
    v)  DESIRED_VERSION=$OPTARG
      ;;
    n)  PKG_NAME=$OPTARG
      ;;
    d)  LOCATION=$(readlink -f $OPTARG)
      ;;
  esac
done

if [ -z "$PKG_NAME" ] || [ -z "$DESIRED_VERSION" ] || [ -z "$LOCATION" ]; then
  show_help
  exit 1
fi

vendor_all "${LOCATION}/${PKG_NAME}-${DESIRED_VERSION}" "${LOCATION}/${PKG_NAME}-${DESIRED_VERSION}-govendor"
# output vendor tar
tar --sort=name --mtime="$(date -u +"%Y-%m-%d %H:%MZ")" \
    --owner=0 --group=0 --numeric-owner \
    --pax-option="exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime" \
    -cf "${LOCATION}/${PKG_NAME}-${DESIRED_VERSION}-govendor.tar.gz" \
    -C "${LOCATION}/${PKG_NAME}-${DESIRED_VERSION}-govendor" .

if [ $? -eq 0 ]; then
    echo "Produced vendor tar: ${LOCATION}/${PKG_NAME}-${DESIRED_VERSION}-govendor.tar.gz"
    echo "sha256sum: $(sha256sum ${LOCATION}/${PKG_NAME}-${DESIRED_VERSION}-govendor.tar.gz)"
else
    echo "failure"
fi

# cleanup
rm -r "${LOCATION}/${PKG_NAME}-${DESIRED_VERSION}-govendor"
