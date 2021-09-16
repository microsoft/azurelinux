#!/bin/bash

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# gen-ld-script.sh
# Generate linker script to embed ELF binaries with build metadata

# /usr/lib/rpm/mariner/gen-ld-script.sh %{name} %{version}
echo "gen-ld-script.sh name($1) version($2)"

OS_ID=$(grep -oP '(?<=^ID=).+' /etc/os-release | tr -d '"')
OS_VERSION=$(grep -oP '(?<=^VERSION_ID=).+' /etc/os-release | tr -d '"')

/usr/lib/rpm/mariner/generate-package-note.py \
   --os "$OS_ID" \
   --osVersion "$OS_VERSION" \
   --type "rpm" \
   --name "$1" \
   --version "$2" \
   --moduleVersion "$2" \
   --stamp "LinkerOnly"
