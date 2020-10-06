#!/bin/bash

set -e

TOOLCHAIN_BUILD_FILE=$1
OUTPUT_FILE=$2

# Extract the specs built from toolkit/scripts/toolchain/build_official_toolchain_rpms.sh
# Each spec that is built will be on its own line in the following format:
#
# build_rpm_in_chroot_no_install foo
#
# The below sed command will extract every spec name that follows the above pattern and place it in $OUTPUT_FILE.
sed -nE 's/^\s*build_rpm_in_chroot_no_install\s+(\w+)/\1/p' $TOOLCHAIN_BUILD_FILE > $OUTPUT_FILE