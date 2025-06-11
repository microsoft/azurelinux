#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e

# Define usage function
usage() {
    echo "Usage: $0 [OPTIONS]"
    echo "Install prerequisites for Azure Linux toolkit"
    echo ""
    echo "Options:"
    echo "  --configure-docker    Enable Docker service and add current user to docker group"
    echo "  --no-install-prereqs  Skip installation of prerequisite packages"
    echo "  --help                Display this help message"
    exit 1
}

# Initialize option flags
CONFIGURE_DOCKER=false
INSTALL_PREREQS=true

# Parse command line arguments
while [ $# -gt 0 ]; do
    case "$1" in
        --configure-docker)
            CONFIGURE_DOCKER=true
            ;;
        --no-install-prereqs)
            INSTALL_PREREQS=false
            ;;
        --help)
            usage
            ;;
        *)
            echo "Unknown option: $1"
            usage
            ;;
    esac
    shift
done

# Install prerequisites if not disabled
# golang version pinned for stability to avoid breaking changes. As of 11-Jun-2025 we are using golang-1.24.3.
# When making a breaking change to the toolkit which requires a newer golang version, update this version.
if [ "$INSTALL_PREREQS" = true ]; then
    echo "Installing required packages..."
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
    golang-1.24.3 \
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
else
    echo "Skipping installation of prerequisite packages..."
fi

# Configure Docker if requested
if [ "$CONFIGURE_DOCKER" = true ]; then
    echo "Enabling Docker service..."
    systemctl enable --now docker.service
    
    echo "Adding current user to 'docker' group..."
    usermod -aG docker $USER
    
    echo "*** NOTE: You will need to log out and log back in for user changes to take effect. ***"
fi

script_file=$(readlink -f "$0")
# md file is the same name as the script file, but with a .md extension
md_file="${script_file%.*}.md"

echo ""
echo "Install complete..."
echo ""
if [ "$CONFIGURE_DOCKER" = false ]; then
    echo "**** Additional optional steps are available. Run with --help for more information. ****"
    echo "**** Refer to ${md_file} for more details. ****"
fi
echo ""
