#!/bin/bash

set -x
set -e

MARINER_BRANCH=$1
OUTPUT_DIR=$2
ROOT_FOLDER=/home/george/git/argus-toolkit
PROV_BUILDER_DIR=$ROOT_FOLDER/prov-builder

function ValidateInitrdSize() {
  fileName=$1
  maxSizeInMBs=$2
  maxSizeInBytes=$(($maxSizeInMBs * 1024 * 1024))

  actualSize=$(ls -la $fileName | awk '{print $5}')

  if (( $actualSize > $maxSizeInBytes )); then
      echo "Error: $fileName cannot be greater than $maxSizeInMBs MBs."
      exit 2
  fi
}

function CaptureInitrdAndVmlinuz() {
  local OUTPUT_DIR=$1

  GENERATED_INITRD=../out/images/iso_initrd/iso-initrd.img
  GENERATED_VMLINUZ=$(sudo find ../build/imagegen/iso_initrd/imager_output/rootfs/boot -name "vmlinuz-*")

  ValidateInitrdSize $GENERATED_INITRD 300

  Copy the ISO to build directory
  cp $GENERATED_INITRD $OUTPUT_DIR/
  sudo cp $GENERATED_VMLINUZ $OUTPUT_DIR/vmlinuz
  sudo chmod 644 $OUTPUT_DIR/vmlinuz
}

function CaptureIso() {
  local OUTPUT_ISO=$1

  BUILT_ISO_FILE=$(find ../out/images/cdrom -name "cdrom-*.iso")
  cp $BUILT_ISO_FILE $OUTPUT_ISO
}

# -----------------------------------------------------------------------------
# main()
#
pushd $ROOT_FOLDER

mkdir -p $OUTPUT_DIR
sudo rm -f $OUTPUT_DIR/iso-initrd.img
sudo rm -f $OUTPUT_DIR/vmlinuz
sudo rm -f $OUTPUT_DIR/baremetal.iso

pushd $ROOT_FOLDER/CBL-Mariner

sudo git checkout $MARINER_BRANCH
sudo git pull

sudo rm -rf ./out/images/cdrom
sudo rm -rf ./out/images/iso_initrd
sudo rm -rf ./build/imagegen/iso_initrd

pushd toolkit
sudo make -j 8 iso \
  REBUILD_TOOLS=y \
  REBUILD_PACKAGES=n \
  CONFIG_FILE=$PROV_BUILDER_DIR/cdrom.json \
  initrd_config_json=$PROV_BUILDER_DIR/iso_initrd.json

# CaptureInitrdAndVmlinuz $OUTPUT_DIR
CaptureIso $OUTPUT_DIR/baremetal.iso

popd
popd

