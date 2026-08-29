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

# Returns zero when the given go binary meets the toolkit's minimum. Prereleases of the minimum
# series must not qualify -- go1.25rc1 predates go1.25.0 and the toolkit would reject it -- while
# prereleases of later series (go1.26rc1) are new enough.
go_version_ok() {
    "$1" version 2>/dev/null | grep -qE 'go1\.(25\.[0-9]|2[6-9]|[3-9][0-9])'
}

# Echoes the root of an installed Go toolchain, preferring the distro package over the upstream
# tarball, and a toolchain that meets the minimum over one that does not -- so a stale apt root
# does not get linked over a good upstream one. Returns non-zero when neither root has a Go.
go_root() {
    go_root_fallback=""
    for root in "$GO_APT_ROOT" /usr/local/go; do
        if [ -x "$root/bin/go" ]; then
            go_version_ok "$root/bin/go" && { echo "$root"; return 0; }
            [ -z "$go_root_fallback" ] && go_root_fallback="$root"
        fi
    done

    [ -n "$go_root_fallback" ] && { echo "$go_root_fallback"; return 0; }
    return 1
}

# Returns zero when a Go new enough for the toolkit is already available, whether it is first on
# PATH or sitting unlinked in one of the roots this script manages.
go_is_supported() {
    go_version_ok go && return 0

    go_installed_root="$(go_root)" || return 1
    go_version_ok "$go_installed_root/bin/go"
}

# Installs Go from the distro when it is packaged, otherwise from the pinned upstream tarball.
install_go() {
    echo "Checking apt for '$GO_APT_PACKAGE' (not packaged before Ubuntu 26.04)..."
    if apt install -y "$GO_APT_PACKAGE" && [ -x "$GO_APT_ROOT/bin/go" ]; then
        echo "Installed $GO_APT_PACKAGE from apt."
        return
    fi

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
    # Deliberately not 'local': the EXIT trap below runs after this function has returned, when a
    # function-scoped variable would already be out of scope and the temp dir would leak.
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
}

# Points /usr/bin/go and /usr/bin/gofmt at the installed Go root, then checks the links actually win.
link_go() {
    if ! go_link_root="$(go_root)"; then
        echo "No Go installation in $GO_APT_ROOT or /usr/local/go, skipping Go symlinks..."
        return
    fi

    echo "Creating Go symlinks from $go_link_root..."
    ln -vsf "$go_link_root/bin/go" /usr/bin/go
    ln -vsf "$go_link_root/bin/gofmt" /usr/bin/gofmt

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

    # Install Go separately from the packages above: which source it comes from depends on the
    # Ubuntu release, and a toolchain that is already good enough is reused rather than replaced.
    if go_is_supported; then
        echo "Found a Go toolchain that meets the minimum, skipping Go installation..."
    else
        install_go
    fi
else
    echo "Skipping installation of prerequisite packages..."
fi

# Neither Go root this script manages ($GO_APT_ROOT, /usr/local/go) is on PATH, so a toolchain
# installed above stays invisible to the toolkit until /usr/bin/go points at it. Refresh the links
# only when the 'go' on PATH cannot build the toolkit: one that is already good enough is left
# alone, whether this run installed it or it was there all along. --fix-go-links forces the
# refresh, to repair the links or to pair with --no-install-prereqs.
hash -r
if [ "$FIX_GO_LINKS" = true ] || { [ "$INSTALL_PREREQS" = true ] && ! go_version_ok go; }; then
    link_go
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
