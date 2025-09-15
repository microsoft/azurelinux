#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
set -exuo pipefail

# Create local ISO repo for RPMS directory
createrepo /RPMS

# RPM packages are generated under rootfs RPMS folder.
# Hence update baseurl path 
sed -i 's|baseurl=file:///mnt/cdrom/RPMS|baseurl=file:///RPMS|' /etc/yum.repos.d/mariner-iso.repo

# RPM packages should be installed from ISO local repo
# Remove PMC official base repo from ISO
rm -r /etc/yum.repos.d/azurelinux-official-base.repo
