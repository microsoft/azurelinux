#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -x
set -e

echo Begin building CBL-Mariner toolchain
echo Parameters passed: $@

MARINER_DIST_TAG=$1
MARINER_BUILD_NUMBER=$2
MARINER_RELEASE_VERSION=$3
MARINER_BUILD_DIR=$4
MARINER_RPM_DIR=$5
MARINER_SPECS_DIR=$6
RUN_CHECK=$7
MARINER_TOOLCHAIN_MANIFESTS_DIR=$8
INCREMENTAL_TOOLCHAIN=${9:-n}
ARCHIVE_TOOL=${10}
MARINER_INPUT_SRPMS_DIR=${11}
MARINER_OUTPUT_SRPMS_DIR=${12}
MARINER_REHYDRATED_RPMS_DIR=${13}
MARINER_TOOLCHAIN_MANIFESTS_FILE=${14}
#  Time stamp components
# =====================================================
BLDTRACKER=${15}
TIMESTAMP_FILE_PATH=${16}
# =====================================================

# Create toolchain subdirectory in out folder
mkdir -pv $MARINER_BUILD_DIR/toolchain
mkdir -pv $MARINER_RPM_DIR/noarch
mkdir -pv $MARINER_RPM_DIR/$(uname -m)

./build_official_toolchain_rpms.sh \
    "$MARINER_DIST_TAG" \
    "$MARINER_BUILD_NUMBER" \
    "$MARINER_RELEASE_VERSION" \
    "$MARINER_BUILD_DIR" \
    "$MARINER_SPECS_DIR" \
    "$RUN_CHECK" \
    "$MARINER_TOOLCHAIN_MANIFESTS_DIR" \
    "$INCREMENTAL_TOOLCHAIN" \
    "$MARINER_INPUT_SRPMS_DIR" \
    "$MARINER_OUTPUT_SRPMS_DIR" \
    "$MARINER_REHYDRATED_RPMS_DIR" \
    "$MARINER_TOOLCHAIN_MANIFESTS_FILE" \
    "$ARCHIVE_TOOL" \
    "$BLDTRACKER" \
    "$TIMESTAMP_FILE_PATH"

# Output:
# out/toolchain/built_rpms
# out/toolchain/toolchain_built_rpms.tar.gz

echo Full CBL-Mariner toolchain build complete
rm -rvf $MARINER_BUILD_DIR/toolchain/built_rpms_all
mv -v $MARINER_BUILD_DIR/toolchain/built_rpms/ $MARINER_BUILD_DIR/toolchain/built_rpms_all
pushd $MARINER_BUILD_DIR/toolchain
tar -I "$ARCHIVE_TOOL" -cvf toolchain_built_rpms_all.tar.gz built_rpms_all
popd
# Output:
# out/toolchain/built_rpms_all
# out/toolchain/toolchain_built_rpms_all.tar.gz

echo Creating toolchain source RPM archive
pushd $MARINER_BUILD_DIR/toolchain
tar -I "$ARCHIVE_TOOL" -C ./populated_toolchain/usr/src/mariner -cvf toolchain_built_srpms_all.tar.gz SRPMS
popd

if [ "$INCREMENTAL_TOOLCHAIN" = "y" ]; then
    echo "Creating delta toolchain RPMs tarball."

    tar -I "$ARCHIVE_TOOL" -C "$MARINER_BUILD_DIR"/toolchain/built_rpms_all \
        -T "$MARINER_BUILD_DIR"/logs/toolchain/built_rpms_list.txt \
        -cvf "$MARINER_BUILD_DIR"/toolchain/toolchain_built_rpms_delta.tar.gz
fi

echo Printing list of built toolchain RPMS:
ls -la $MARINER_BUILD_DIR/toolchain/built_rpms_all
ls -la $MARINER_BUILD_DIR/toolchain/built_rpms_all | wc
