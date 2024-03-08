#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -x
set -e

echo Begin building Azure Linux toolchain
echo Parameters passed: $@

MARINER_DIST_TAG=$1
MARINER_DIST_MACRO=$2
MARINER_BUILD_NUMBER=$3
MARINER_RELEASE_VERSION=$4
MARINER_BUILD_DIR=$5
MARINER_RPM_DIR=$6
MARINER_SPECS_DIR=$7
RUN_CHECK=$8
MARINER_TOOLCHAIN_MANIFESTS_DIR=$9
INCREMENTAL_TOOLCHAIN=${10:-n}
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
    "$MARINER_DIST_MACRO" \
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
    "$BLDTRACKER" \
    "$TIMESTAMP_FILE_PATH"

# Output:
# out/toolchain/built_rpms
# out/toolchain/toolchain_built_rpms.tar.gz

echo Full Azure Linux toolchain build complete
rm -rvf $MARINER_BUILD_DIR/toolchain/built_rpms_all
mv -v $MARINER_BUILD_DIR/toolchain/built_rpms/ $MARINER_BUILD_DIR/toolchain/built_rpms_all
pushd $MARINER_BUILD_DIR/toolchain
tar cvf toolchain_built_rpms_all.tar.gz built_rpms_all
popd
# Output:
# out/toolchain/built_rpms_all
# out/toolchain/toolchain_built_rpms_all.tar.gz

echo Creating toolchain source RPM archive
pushd $MARINER_BUILD_DIR/toolchain
tar -C ./populated_toolchain/usr/src/azl -cvf toolchain_built_srpms_all.tar.gz SRPMS
popd

if [ "$INCREMENTAL_TOOLCHAIN" = "y" ]; then
    echo "Creating delta toolchain RPMs tarball."

    tar -C "$MARINER_BUILD_DIR"/toolchain/built_rpms_all \
        -T "$MARINER_BUILD_DIR"/logs/toolchain/built_rpms_list.txt \
        -czvf "$MARINER_BUILD_DIR"/toolchain/toolchain_built_rpms_delta.tar.gz
fi

echo Printing list of built toolchain RPMS:
ls -la $MARINER_BUILD_DIR/toolchain/built_rpms_all
ls -la $MARINER_BUILD_DIR/toolchain/built_rpms_all | wc
