#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -eo pipefail

# Ubuntu 26.04 packages Go 1.25, but the older releases still used by developers and CI (22.04,
# 24.04) do not package it at all. Rather than special-casing releases, install the upstream
# toolchain whenever the Go already on PATH is missing or older than 1.25.
# Checksums are from https://go.dev/dl and must be updated together with GO_VERSION.
GO_VERSION=1.25.14
GO_SHA256_AMD64=a21ae5633a269bcd7e90cf767e48225633795e99d831742cbf3397064fee7712
GO_SHA256_ARM64=9bf234ea70ffec9347fdf6b22ce4add51717d3386a38a441e8c8743fceb5eaee

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
if [ "$INSTALL_PREREQS" = true ]; then
    echo "Installing required packages..."
    apt update
    apt install -y \
    acl \
    curl \
    diffutils \
    gawk \
    genisoimage \
    git \
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

    # Ubuntu 26.04 ships golang-1.25-go, but 22.04 and 24.04 do not package Go 1.25 at all, and the
    # apt package is not on PATH anyway. Install the upstream toolchain unless PATH already has
    # Go 1.25 or newer.
    if go version 2>/dev/null | grep -qE 'go1\.(2[5-9]|[3-9][0-9])'; then
        echo "Found $(go version), skipping Go installation..."
    else
        go_arch="$(dpkg --print-architecture)"
        case "$go_arch" in
            amd64) go_sha256="$GO_SHA256_AMD64" ;;
            arm64) go_sha256="$GO_SHA256_ARM64" ;;
            *)
                echo "ERROR: no upstream Go build is pinned for architecture '$go_arch'." >&2
                echo "Install Go $GO_VERSION or newer manually, then re-run with --no-install-prereqs." >&2
                exit 1
                ;;
        esac

        echo "Installing Go $GO_VERSION ($go_arch) from https://go.dev/dl..."
        go_tmp_dir="$(mktemp -d)"
        trap 'rm -rf "$go_tmp_dir"' EXIT
        curl -fsSL -o "$go_tmp_dir/go.tar.gz" \
          "https://go.dev/dl/go${GO_VERSION}.linux-${go_arch}.tar.gz"
        echo "$go_sha256  $go_tmp_dir/go.tar.gz" | sha256sum -c -

        rm -rf /usr/local/go
        tar -C /usr/local -xzf "$go_tmp_dir/go.tar.gz"
        ln -vsf /usr/local/go/bin/go /usr/bin/go
        ln -vsf /usr/local/go/bin/gofmt /usr/bin/gofmt
    fi
else
    echo "Skipping installation of prerequisite packages..."
fi

# Fix go 1.25 links if requested
if [ "$FIX_GO_LINKS" = true ]; then
    if [ -x /usr/local/go/bin/go ]; then
        echo "Creating Go symlinks..."
        ln -vsf /usr/local/go/bin/go /usr/bin/go
        ln -vsf /usr/local/go/bin/gofmt /usr/bin/gofmt
    else
        echo "No Go installation in /usr/local/go, skipping Go symlinks..."
    fi
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
