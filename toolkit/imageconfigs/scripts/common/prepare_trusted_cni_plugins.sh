#!/bin/bash

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -eux

CNI_BIN_DIR="/opt/cni/bin"
CNI_TRUSTED_DIR="/usr/libexec/cni"

mkdir -p "$CNI_TRUSTED_DIR"

# Copy all plugins to trusted dir
for plugin in "$CNI_BIN_DIR"/*; do
  name=$(basename "$plugin")
  target="$CNI_TRUSTED_DIR/$name"

  rm -f "$target"
  cp "$plugin" "$target"
done
