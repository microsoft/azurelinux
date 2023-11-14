#!/bin/bash

set -x
set -e

# -----------------------------------------------------------------------------
# [placeholder] build/customize rootfs initrd
#

# -----------------------------------------------------------------------------
# Build the initrd
#
export trident_rpms_path=/home/george/git/argus-toolkit/trident_rpms/
export build_output=/home/george/git/argus-toolkit/build-output
export mariner_branch=2.0-stable

mkdir -p $build_output

# CONFIG_FILE=~/git/argus-toolkit/prov-builder/cdrom.json \
# initrd_config_json=~/git/argus-toolkit/prov-builder/iso_initrd.json

sudo /home/george/git/argus-toolkit/prov-builder/build.sh \
  $trident_rpms_path \
  $build_output \
  $mariner_branch

# -----------------------------------------------------------------------------
# validate iso initrd size...
#
# ./validation/validate-file-size.sh $INITRD_FILE_PATH $INITRD_MAX_SIZE_IN_MBS
