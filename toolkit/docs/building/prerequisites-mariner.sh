#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e

tdnf -y install \
    acl \
    binutils \
    cdrkit \
    curl \
    diffutils \
    dosfstools \
    gawk \
    genisoimage \
    git \
    glibc-devel \
    golang \
    jq \
    kernel-headers \
    make \
    moby-cli \
    moby-engine \
    openssl \
    parted \
    pigz \
    qemu-img \
    rpm \
    rpm-build \
    sudo \
    systemd \
    tar \
    wget \
    xfsprogs \
    zstd

script_file=$(readlink -f "$0")
# md file is the same name as the script file, but with a .md extension
md_file="${script_file%.*}.md"

echo ""
echo "Install complete..."
echo ""
echo "**** Refer to ${md_file} for additional steps to complete the setup. ****"
echo ""
