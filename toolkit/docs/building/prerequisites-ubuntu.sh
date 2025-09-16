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
    echo "  --fix-go-links       Create symlinks for Go binaries"
    echo "  --configure-docker   Install and configure Docker"
    echo "  --no-install-prereqs Skip installation of prerequisite packages"
    echo "  --help               Display this help message"
    exit 1
}

# Initialize option flags
FIX_GO_LINKS=false
INSTALL_DOCKER=false
INSTALL_PREREQS=true

# Parse command line arguments
while [ $# -gt 0 ]; do
    case "$1" in
        --fix-go-links)
            FIX_GO_LINKS=true
            ;;
        --configure-docker)
            INSTALL_DOCKER=true
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
# golang version pinned for stability to avoid breaking changes. As of 11-Jun-2025 we are using golang-1.23.1 on Ubuntu 22.04 since it is the most recent release available.
# When making a breaking change to the toolkit which requires a newer golang version, update this version if needed. 
# If no newer version is available, suggest moving to a newer Ubuntu LTS version
if [ "$INSTALL_PREREQS" = true ]; then
    echo "Installing required packages..."
    apt update
    apt install -y \
    acl \
    curl \
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
    xfsprogs
else
    echo "Skipping installation of prerequisite packages..."
fi

# Fix go 1.23 links if requested
if [ "$FIX_GO_LINKS" = true ]; then
    echo "Creating Go symlinks..."
    ln -vsf /usr/lib/go-1.21/bin/go /usr/bin/go
    ln -vsf /usr/lib/go-1.21/bin/gofmt /usr/bin/gofmt
fi

# Install and configure Docker if requested
if [ "$INSTALL_DOCKER" = true ]; then
    echo "Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    
    echo "Adding current user to 'docker' group..."
    usermod -aG docker $USER
    
    echo "*** NOTE: You will need to log out and log back in for user changes to take effect. ***"
fi

script_file=$(readlink -f "$0")
# md file is the same name as the script file, but with a .md extension
md_file="${script_file%.*}.md"

echo ""
if [ "$FIX_GO_LINKS" = false ] || [ "$INSTALL_DOCKER" = false ]; then
    echo "**** Additional optional steps are available. Run with --help for more information. ****"
    echo "**** Refer to ${md_file} for more details. ****"
fi
echo ""
