#!/bin/bash

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# gen-ld-script.sh
# Generate linker script to embed ELF binaries with build metadata

# /usr/lib/rpm/mariner/gen-ld-script.sh %{name} %{version}
echo "gen-ld-script.sh name($1) version($2)"

OS_ID=$(grep -oP '(?<=^ID=).+' /etc/os-release | tr -d '"')
OS_VERSION=$(grep -oP '(?<=^VERSION_ID=).+' /etc/os-release | tr -d '"')

# Count number of dot separators in $2 (version)
NUM_DOT_SEPARATORS="${2//[^.]}"
# Ensure moduleVersion contains 4 version parts by adding ".0" padding
case ${#NUM_DOT_SEPARATORS} in
  0)
    MODULEVERSION=$2".0.0.0"
    ;;
  1)
    MODULEVERSION=$2".0.0"
    ;;
  2)
    MODULEVERSION=$2".0"
    ;;
  *)
    MODULEVERSION=$2
    ;;
esac

/usr/lib/rpm/mariner/generate-package-note.py \
   --os "$OS_ID" \
   --osVersion "$OS_VERSION" \
   --type "rpm" \
   --name "$1" \
   --version "$2" \
   --moduleVersion "$MODULEVERSION" \
   --stamp "LinkerOnly" \
   --outdir "/usr/src/mariner/BUILD/"


# Verify if .note.package is properly included in a binary
# /usr/lib/rpm/mariner/verify-package-notes.sh <input_binary> <input_note_section_binary> .note.package

