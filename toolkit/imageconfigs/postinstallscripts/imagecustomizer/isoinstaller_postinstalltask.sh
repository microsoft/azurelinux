#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# isoinstaller_postinstalltask.sh

set -exuo pipefail

# Check if config file path is provided
if [[ $# -eq 0 ]]; then
    echo "Usage: $0 <config-file-path>" >&2
    exit 1
fi

# Create RPMS directory
mkdir -p /RPMS

# # Path to the main config JSON
# CONFIG_JSON="$1"
# CONFIG_DIR="$(dirname "$CONFIG_JSON")"

# echo "CONFIG_DIR: $CONFIG_DIR"
# echo "CONFIG_JSON: $CONFIG_JSON"

# # Find all package list files referenced in the config
# pkglist_files=( $(jq -r '.SystemConfigs[].PackageLists[]' "$CONFIG_JSON") )

# # Recursively parse and add each package and it dependencies to RPMS folder
# for pkglist in "${pkglist_files[@]}"; do
#     # Make path relative to config file directory
#     full_path="$CONFIG_DIR/$pkglist"
#     if [[ -f "$full_path" ]]; then
#         tdnf -y install --downloadonly --alldeps --nogpgcheck --downloaddir /RPMS $(jq -r '.packages[]' "$full_path")
#     fi
# done

# # Get kernel packages from KernelOptions (if present)
# tdnf -y install --downloadonly --alldeps --nogpgcheck --downloaddir /RPMS $(jq -r '.SystemConfigs[] | select(.KernelOptions) | .KernelOptions[]' "$CONFIG_JSON")


# # Create local ISO repo for RPMS directory
createrepo /RPMS

# RPM packages are generated under rootfs RPMS folder.
# Hence update baseurl path 
sed -i 's|baseurl=file:///mnt/cdrom/RPMS|baseurl=file:///RPMS|' /etc/yum.repos.d/mariner-iso.repo

# RPM packages should be installed from ISO local repo
# Remove PMC official base repo from ISO
rm -r /etc/yum.repos.d/azurelinux-official-base.repo
