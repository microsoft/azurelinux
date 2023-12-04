#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -x
set -e

# $1 = TARGET_SPEC
function copy_local_tarball {
    DESTINATION_FOLDER=$(dirname $1)
    cp $DOWNLOAD_FILE_PATH $DESTINATION_FOLDER
}

# $1 = spec name
function remove_local_tarball {
    rm $WORKSPACE/SPECS/$1/$TARBALL_NAME
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
    NEW_CHANGELOG_ENTRY="- Update source to $VERSION"
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
    FILE=$WORKSPACE/SPECS/kernel/kernel.spec
    LINE=$(grep "Version:" $FILE)
    OLD_VERSION=${LINE:16}
}

function update_configs {
    CONFIG_FILE="kernel/config kernel/config_aarch64 kernel-hci/config"
    for configfile in $CONFIG_FILE
    do
        FILE=$WORKSPACE/SPECS/$configfile
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

function update_toolchain_pkglist {
    PKGLIST_FOLDER=$WORKSPACE/toolkit/resources/manifests/package/
    PKGLIST="pkggen_core_aarch64.txt pkggen_core_x86_64.txt toolchain_aarch64.txt toolchain_x86_64.txt"
    for pkg in $PKGLIST
    do
        file=$PKGLIST_FOLDER/$pkg
        PATTERN="kernel-headers-.*"
        REPLACE="kernel-headers-$VERSION-1.azl3.noarch.rpm"
        sed -i "s/$PATTERN/$REPLACE/" $file
    done
}

function update_toolchain {
    #update_toolchain_md5sum
    update_toolchain_sha256sum
    update_toolchain_scripts
    update_toolchain_pkglist
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


function usage() { 
    echo "Update sources for kernel" 
    echo "v : Version you are updating to (ex. 5.10.37.1)" 
    echo "u : Your name"
    echo "e : Your email"
    echo "w : Absoulte path to your workspace for your update - no quotes\n"

    echo "example usage: ./toolkit/scripts/update_kernel.sh -v 5.15.34.1 -u 'Cameron Baird' -e 'cameronbaird@microsoft.com' -w \$(pwd)"

    exit 1 
}


##### MAIN #####

#TODO
# error checking : bad tag on cbl-mariner-linux-kernel,
# trigger build or config checker?
# replace old version
# handle kernel-rt patch automatically

# Take arguments
#WORKSPACE=~/repos/CBL-Mariner-Kernel
while getopts "v:u:e:w:" OPTIONS; do
  case "${OPTIONS}" in
    v ) VERSION=$OPTARG ;;
    u ) USER_NAME=$OPTARG ;;
    e ) USER_EMAIL=$OPTARG ;;
    w ) WORKSPACE=$OPTARG ;;
    * ) usage 
        ;;
  esac
done

if [[ -z $VERSION ]]; then
    echo "Missing -v"
    usage
fi
if [[ -z $USER_NAME ]]; then
    echo "Missing -u"
    usage
fi
if [[ -z $USER_EMAIL ]]; then
    echo "Missing -e"
    usage
fi
if [[ -z $WORKSPACE ]]; then
    echo "Missing -w"
    usage
fi

# Create globals
TAG="rolling-lts/mariner-2/$VERSION"
TMPDIR="tmp-dir"
SPECS="kernel-headers kernel hyperv-daemons"
DEFAULT_URL="https://github.com/microsoft/CBL-Mariner-Linux-Kernel/archive/"
DEFAULT_EXTENSION=".tar.gz"
FULL_URL=$DEFAULT_URL$TAG$DEFAULT_EXTENSION
TARBALL_NAME="kernel-$VERSION$DEFAULT_EXTENSION"
DOWNLOAD_FILE_PATH=$TMPDIR/$TARBALL_NAME
SPECS="kernel-headers kernel hyperv-daemons"
SIGNED_SPECS="kernel-signed"
NEW_RELEASE_NUMBER="Release:        1%{?dist}"
CHANGELOG_ENTRY="Update source to $NEW_KERNEL_VERSION"
FILE_SIGNATURE_PATTERN="kernel-"

# Go through needed specs
find_old_version
download
if [ $? -gt 0 ]; then
    return
fi

for spec in $SPECS
do
    TARGET_SPEC=$WORKSPACE/SPECS/$spec/$spec.spec
    TARGET_SIGNATUREJSON=$WORKSPACE/SPECS/$spec/$spec.signatures.json
    copy_local_tarball $TARGET_SPEC
    update_spec $TARGET_SPEC
    update_signature $TARGET_SIGNATUREJSON
done
for spec in $SIGNED_SPECS
do
    TARGET_SPEC=$WORKSPACE/SPECS-SIGNED/$spec/$spec.spec
    update_spec $TARGET_SPEC
done
update_configs

# Update toolchain related files
update_toolchain
update_cgmanifest
print_metadata
#clean

echo "WARNING: update is not complete; this script does not update the rt patch in kernel-rt.spec, you must do this manually!"
