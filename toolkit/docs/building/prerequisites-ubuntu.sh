#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e

apt update
apt install -y \
    acl \
    curl \
    diffutils \
    gawk \
    genisoimage \
    git \
    golang-1.21-go \
    jq \
    make \
    openssl \
    parted \
    pigz \
    qemu-utils \
    rpm \
    systemd \
    tar \
    wget \
    xfsprogs \
    zstd

script_file=$(readlink -f "$0")
# md file is the same name as the script file, but with a .md extension
md_file="${script_file%.*}.md"

echo ""
echo "**** Refer to ${md_file} for additional steps to complete the setup. ****"
echo ""
