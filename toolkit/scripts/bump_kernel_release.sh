#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e

REPO_ROOT="$(git rev-parse --show-toplevel)"
COMMON_SCRIPTS_FOLDER="$REPO_ROOT/toolkit/scripts"

export PATH="$PATH:$COMMON_SCRIPTS_FOLDER"

# shellcheck source=../../toolkit/scripts/specs/specs_tools.sh
source "$COMMON_SCRIPTS_FOLDER/specs/specs_tools.sh"

# $1 = TARGET_SPEC
function copy_local_tarball {
    DESTINATION_FOLDER=$(dirname $1)
    cp $DOWNLOAD_FILE_PATH $DESTINATION_FOLDER
}

# $1 = spec name
function remove_local_tarball {
    rm $SPECS_DIR/$1/$TARBALL_NAME
}

function clean {
    rm -rf $TMPDIR
    for spec in $SPECS
    do
        remove_local_tarball $spec
    done
}

function download {
    mkdir -p $TMPDIR
    pushd $TMPDIR
    echo Downloading $FULL_URL
    wget $FULL_URL -O $TARBALL_NAME
    # if [ $? -gt 0 ]; then
    #     echo "$FULL_URL failed to be reached. Does the version exist on CBL-Mariner-Linux-Kernel?"
    #     return 1
    #     exit 1
    # fi
    popd
    return 0
}

# $1 = path to spec
# $2 = changelog entry text
function create_new_changelog_entry {
    CHANGELOG_LINE=$(grep -n %changelog $1 | tail -1 | cut -f1 -d:)
    NEW_CHANGELOG_LINE=$((CHANGELOG_LINE+1))
    NEW_CHANGELOG_DATE=$(date +"%a %b %d %Y")
    NEW_CHANGELOG_HEADER="* $NEW_CHANGELOG_DATE $USER_NAME <$USER_EMAIL> - $VERSION-1"
    NEW_CHANGELOG_ENTRY="- Bump release number to match kernel release"
    FULL_CHANGELOG_ENTRY="$NEW_CHANGELOG_HEADER\n$NEW_CHANGELOG_ENTRY\n"
    sed -i "${NEW_CHANGELOG_LINE}i${FULL_CHANGELOG_ENTRY}" $1
}

# $1 = TARGET_SPEC
function update_spec {
    sed -i "s/Version:.*/Version:        $VERSION/" $1
    sed -i "s/Release:.*/$NEW_RELEASE_NUMBER/" $1
    create_new_changelog_entry $1
}

function find_old_version {
    FILE=$SPECS_DIR/kernel/kernel.spec
    LINE=$(grep "Version:" $FILE)
    OLD_VERSION=${LINE:16}
}

function update_configs {
    CONFIG_FILE="kernel/config kernel/config_aarch64 kernel-rt/config kernel-hci/config"
    for configfile in $CONFIG_FILE
    do
        FILE=$SPECS_DIR/$configfile
        BASE=${FILE%/*}
        SPEC=${configfile%/*}
        SIGNATURE_FILE="$BASE/$SPEC.signatures.json"
        PATTERN="$OLD_VERSION Kernel Configuration"
        REPLACE="$VERSION Kernel Configuration"
        sed -i "s#$PATTERN#$REPLACE#" $FILE
        SHA256="$(sha256sum $FILE | awk '{print $1;}')"
        #CONFIG_ONLY=$($FILE | cut -d'/' -f2-)
        CONFIG_ONLY=${FILE##*/}
        FULL_SIGNATURE_ENTRY="  \"$CONFIG_ONLY\": \"$SHA256\""
        FILE_PATTERN=$CONFIG_ONLY
        sed -i "s/  \"$FILE_PATTERN\": \".*\"/$FULL_SIGNATURE_ENTRY/" $SIGNATURE_FILE
    done
}

function update_livepatches {
    "$LIVEPATCHING_SCRIPTS_DIR"/generate_livepatch_spec.sh

    update_livepatches_signed
}

function update_livepatches_signed {
    for livepatch_spec in "$SPECS_DIR/livepatch/"livepatch-*.spec
    do
        "$LIVEPATCHING_SCRIPTS_DIR"/generate_livepatch-signed_spec.sh "$livepatch_spec"
    done
}

# $1 = TARGET_SIGNATUREJSON
function update_signature {
    SPEC_DIR=$(dirname $1)
    SHA256="$(sha256sum $SPEC_DIR/$TARBALL_NAME | awk '{print $1;}')"
    FULL_SIGNATURE_ENTRY="  \"$TARBALL_NAME\": \"$SHA256\""
    sed -i "s/  \"$FILE_SIGNATURE_PATTERN.*\": \".*\"/$FULL_SIGNATURE_ENTRY/" $1
}

function update_toolchain_md5sum {
    MD5SUM_FILE=$WORKSPACE/toolkit/scripts/toolchain/container/toolchain-md5sums
    MD5="$(md5sum $DOWNLOAD_FILE_PATH | awk '{print $1;}')"
    FULL_MD5SUM_ENTRY="$MD5  $TARBALL_NAME"
    sed -i "s/.*$FILE_SIGNATURE_PATTERN.*/$FULL_MD5SUM_ENTRY/" $MD5SUM_FILE
}

function update_toolchain_sha256sum {
    SHA256SUM_FILE=$WORKSPACE/toolkit/scripts/toolchain/container/toolchain-sha256sums
    SHA256="$(sha256sum $DOWNLOAD_FILE_PATH | awk '{print $1;}')"
    FULL_SHA256SUM_ENTRY="$SHA256  $TARBALL_NAME"
    sed -i "s/.*$FILE_SIGNATURE_PATTERN.*/$FULL_SHA256SUM_ENTRY/" $SHA256SUM_FILE
}

function update_toolchain_scripts {
    TOOLCHAIN_FOLDER=$WORKSPACE/toolkit/scripts/toolchain/
    TOOLCHAIN_SCRIPTS="toolchain_build_in_chroot.sh toolchain_build_temp_tools.sh"
    for script in $TOOLCHAIN_SCRIPTS
    do
        file=$TOOLCHAIN_FOLDER/container/$script
        PATTERN="KERNEL_VERSION=\"$OLD_VERSION\""
        REPLACE="KERNEL_VERSION=\"$VERSION\""
        sed -i "s/$PATTERN/$REPLACE/" $file
    done
}

function update_toolchain_wget_url {
    FILE=$WORKSPACE/toolkit/scripts/toolchain/container/toolchain-remote-wget-list
    PATTERN="$DEFAULT_URL.*"
    REPLACE="$FULL_URL"
    sed -i "s#$PATTERN#$REPLACE#" $FILE
}

function update_toolchain_dockerfile {
    FILE=$WORKSPACE/toolkit/scripts/toolchain/container/Dockerfile
    PATTERN="$DEFAULT_URL.* -O"
    REPLACE="$FULL_URL -O"
    sed -i "s#$PATTERN#$REPLACE#" $FILE
    PATTERN="kernel-.*.tar.gz"
    REPLACE="$TARBALL_NAME"
    sed -i "s#$PATTERN#$REPLACE#" $FILE
}

function update_manifests {
    local kernel_release_number
    local kernel_spec_path
    local package_manifests_dir

    echo "Updating package manifests."

    kernel_spec_path="$REPO_ROOT/SPECS/kernel/kernel.spec"
    kernel_release_number="$(spec_read_release_number "$kernel_spec_path")"
    package_manifests_dir="$REPO_ROOT/toolkit/resources/manifests/package"
    sed -i -E "s/(kernel-headers-.*)\d+(\.cm.*)/\1$kernel_release_number\2/" "$package_manifests_dir"/{pkggen,toolchain}*.txt
}

function update_toolchain {
    #update_toolchain_md5sum
    update_toolchain_sha256sum
    update_toolchain_scripts
    update_manifests
    update_toolchain_dockerfile
}

function replace_cgversion {
    for spec in $SPECS
    do
        PATTERN="\"name\": \"$spec\","
        REPLACE="\ \ \ \ \ \ \ \ \ \ \"version\": \"$VERSION\","
        sed -i "/$PATTERN/!b;n;c$REPLACE" $1
    done
}

function update_cgmanifest {
    CGMANIFEST_FILE=$WORKSPACE/cgmanifest.json
    # Replace URL
    PATTERN="$DEFAULT_URL.*"
    REPLACE="$FULL_URL\""
    sed -i "s#$PATTERN#$REPLACE#" $CGMANIFEST_FILE
    # Replace version
    replace_cgversion $CGMANIFEST_FILE
}

function print_metadata {
    MD5="$(md5sum $DOWNLOAD_FILE_PATH | awk '{print $1;}')"
    SHA256="$(sha256sum $DOWNLOAD_FILE_PATH | awk '{print $1;}')"
    echo md5sum = $MD5
    echo sha256 = $SHA256
}

SPECS_DIR_PATH="$REPO_ROOT/SPECS"
SPECS_SIGNED_DIR_PATH="$REPO_ROOT/SPECS-SIGNED"
SPECS_TO_BUMP="$SPECS_DIR_PATH/kernel-headers/kernel-headers.spec $SPECS_SIGNED_DIR_PATH/kernel-signed/kernel-signed.spec"

for spec_to_bump in $SPECS_TO_BUMP
do
    update_spec.sh "Bump release number to match kernel release." "$spec_to_bump"
done

update_manifests
"$COMMON_SCRIPTS_FOLDER"/livepatching/update_livepatches.sh
