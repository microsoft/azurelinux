#!/bin/bash

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# gen-ld-script.sh
# Generate linker script to embed ELF binaries with build metadata

# /usr/lib/rpm/azl/gen-ld-script.sh %{name} %{?epoch:%{epoch}:}%{version}-%{release} %{_topdir} %{distro_release_version}
echo "gen-ld-script.sh name($1) version($2) _topdir($3) osversion($4)"

OS_VERSION=$(echo $4 | cut -d. -f1,2)

# When generating moduleVersion, strip everything after the dash. Also remove the epoch, if present
# ex: "1.8.0-2.azl3" -> "1.8.0"
# ex: "1:3.0.0-7.azl3" -> "3.0.0"
VERSION_NO_RELEASE=$(echo $2 | cut -d- -f1 | cut -d: -f2)

# Azure Watson requires a "moduleVersion" field, which always contains a 4-part version number.
# Ensure moduleVersion contains 4 version parts by adding ".0" padding
# Count number of dot separators in $2 (version)
NUM_DOT_SEPARATORS="${VERSION_NO_RELEASE//[^.]}"
case ${#NUM_DOT_SEPARATORS} in
  0)
    MODULEVERSION=$VERSION_NO_RELEASE".0.0.0"
    ;;
  1)
    MODULEVERSION=$VERSION_NO_RELEASE".0.0"
    ;;
  2)
    MODULEVERSION=$VERSION_NO_RELEASE".0"
    ;;
  *)
    MODULEVERSION=$VERSION_NO_RELEASE
    ;;
esac

MODULE_INFO_DIR="$3/BUILD/"

mkdir -pv $MODULE_INFO_DIR

/usr/lib/rpm/azl/generate-package-note.py \
   --os "mariner" \
   --osVersion "$OS_VERSION" \
   --type "rpm" \
   --name "$1" \
   --version "$2" \
   --moduleVersion "$MODULEVERSION" \
   --stamp "LinkerOnly" \
   --outdir $MODULE_INFO_DIR


# Verify if .note.package is properly included in a binary
# /usr/lib/rpm/azl/verify-package-notes.sh <input_binary> <input_note_section_binary> .note.package
