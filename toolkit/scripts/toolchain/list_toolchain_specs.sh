#!/bin/bash

set -e

TOOLCHAIN_BUILD_FILE=$1
OUTPUT_FILE=$2

# Extract the specs built from toolkit/scripts/toolchain/build_official_toolchain_rpms.sh
# Each spec that is built will be on its own line in the following formats:
#
# build_rpm_in_chroot_no_install foo-spec-name
# build_rpm_in_chroot_no_install foo-spec-name qualified-foo-rpm-name
#
# In both cases, the first entry is the actual spec name to extract.
# The below sed command will extract every spec name that follows the above pattern and place it in $OUTPUT_FILE.
# `sort -u` is for eliminating duplicates- we don't actually care about the order
sed -nE 's/^\s*build_rpm_in_chroot_no_install\s+([A-Za-z0-9_-]+).*$/\1/pgm' $TOOLCHAIN_BUILD_FILE | sort -u > $OUTPUT_FILE

# Special case to add msopenjdk-11 RPM which is downloaded instead of built
echo "msopenjdk-11" >> $OUTPUT_FILE
