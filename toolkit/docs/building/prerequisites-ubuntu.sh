#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -eo pipefail

# Go is installed separately from the other packages because its source depends on the release.
# Ubuntu 26.04 packages Go 1.25 as golang-1.25-go; 22.04 and 24.04 do not package it at all, so
# those fall back to the upstream toolchain. The distro package is preferred so that hosts which
# can reach an apt mirror but not go.dev keep working without external egress.
#
# Go supports only the two most recent release series, so this pin has to keep moving. See
# "Updating the pinned Go version" in prerequisites-ubuntu.md before changing any of it: the
# minimum version is spelled out in four other places that must move at the same time.
# Checksums are from https://go.dev/dl and must be updated together with GO_VERSION.
GO_APT_PACKAGE=golang-1.25-go
GO_APT_ROOT=/usr/lib/go-1.25
GO_VERSION=1.25.14
GO_SHA256_AMD64=a21ae5633a269bcd7e90cf767e48225633795e99d831742cbf3397064fee7712
GO_SHA256_ARM64=9bf234ea70ffec9347fdf6b22ce4add51717d3386a38a441e8c8743fceb5eaee

# Echoes the root of an installed Go toolchain, preferring the distro package over the upstream
# tarball. Returns non-zero when neither is present.
go_root() {
    for root in "$GO_APT_ROOT" /usr/local/go; do
        [ -x "$root/bin/go" ] && { echo "$root"; return 0; }
    done
    return 1
}

# Returns zero when the given go binary meets the toolkit's minimum. A prerelease of the minimum
# series must not qualify: go1.25rc1 predates go1.25.0, so the toolkit would reject it. Prereleases
# of later series (go1.26rc1) are new enough and stay accepted.
go_is_supported() {
    "$1" version 2>/dev/null | grep -qE 'go1\.(25\.[0-9]|2[6-9]|[3-9][0-9])'
}

# Points /usr/bin/go and /usr/bin/gofmt at the given Go root, then checks the links actually win.
link_go() {
    ln -vsf "$1/bin/go" /usr/bin/go
    ln -vsf "$1/bin/gofmt" /usr/bin/gofmt

    # Ubuntu's default PATH, and sudo's secure_path, list /usr/local/bin ahead of /usr/bin, so a
    # stray go left there keeps winning. Without this warning the toolkit's own version gate fails
    # much later, from a different script, with nothing pointing back to the real cause.
    hash -r
    go_on_path="$(command -v go 2>/dev/null || true)"
    if [ -n "$go_on_path" ] && ! [ "$go_on_path" -ef /usr/bin/go ]; then
        echo "WARNING: '$go_on_path' precedes /usr/bin/go on PATH and will be used instead:" >&2
        echo "WARNING:   $("$go_on_path" version 2>&1 | head -n 1)" >&2
        echo "WARNING: remove it if the build later reports an unsupported Go version." >&2
    fi
}

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

    # Install Go from the distro when it is packaged, otherwise from the pinned upstream tarball.
    if go_is_supported go; then
        echo "Found $(go version), skipping Go installation..."
    else
        if go_existing_root="$(go_root)" && go_is_supported "$go_existing_root/bin/go"; then
            # Installed, just not on PATH. Relinking below is enough, and reinstalling would
            # overwrite a toolchain that may well be newer than the one pinned here.
            echo "Found $("$go_existing_root/bin/go" version) in $go_existing_root, reusing it..."
        else
            echo "Checking apt for '$GO_APT_PACKAGE' (not packaged before Ubuntu 26.04)..."
            if apt install -y "$GO_APT_PACKAGE" && [ -x "$GO_APT_ROOT/bin/go" ]; then
                echo "Installed $GO_APT_PACKAGE from apt."
            else
                echo "'$GO_APT_PACKAGE' is unavailable on this release, using the upstream toolchain..."
                go_arch="$(dpkg --print-architecture)"
                case "$go_arch" in
                    amd64) go_sha256="$GO_SHA256_AMD64"; go_sha256_var=GO_SHA256_AMD64 ;;
                    arm64) go_sha256="$GO_SHA256_ARM64"; go_sha256_var=GO_SHA256_ARM64 ;;
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
                if echo "$go_sha256  $go_tmp_dir/go.tar.gz" | sha256sum --status -c -; then
                    echo "Checksum OK."
                else
                    echo "ERROR: go${GO_VERSION}.linux-${go_arch}.tar.gz does not match its pinned checksum." >&2
                    echo "  expected: $go_sha256" >&2
                    echo "  actual:   $(sha256sum < "$go_tmp_dir/go.tar.gz" | cut -d ' ' -f 1)" >&2
                    echo "Either the download was corrupted or tampered with, or GO_VERSION was changed in" >&2
                    echo "$0 without refreshing $go_sha256_var. The expected value for a given release is" >&2
                    echo "published at https://go.dev/dl. Nothing has been installed." >&2
                    exit 1
                fi

                if [ -e /usr/local/go ]; then
                    echo "WARNING: replacing the Go installation in /usr/local/go, it is older than $GO_VERSION." >&2
                fi
                rm -rf /usr/local/go
                tar -C /usr/local -xzf "$go_tmp_dir/go.tar.gz"
            fi
        fi

        go_installed_root="$(go_root)"
        link_go "$go_installed_root"
    fi
else
    echo "Skipping installation of prerequisite packages..."
fi

# Fix go 1.25 links if requested
if [ "$FIX_GO_LINKS" = true ]; then
    if go_link_root="$(go_root)"; then
        echo "Creating Go symlinks from $go_link_root..."
        link_go "$go_link_root"
    else
        echo "No Go installation in $GO_APT_ROOT or /usr/local/go, skipping Go symlinks..."
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
