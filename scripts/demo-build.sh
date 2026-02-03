#!/bin/bash
set -euxo pipefail

#
# NOTE: This script is a throwaway script. Please think ~~twice~~ thrice before you
# consider adding anything to it.
#

# Confirm working dir.
if [ ! -f azldev.toml ]; then
    echo "ERROR: This script must be run from the root of the repo" >&2
    exit 1
fi

# Check prereqs.
for prereq in azldev kiwi createrepo_c docker; do
    if ! command -v $prereq >/dev/null 2>&1; then
        echo "ERROR: Missing prerequisite '$prereq'." >&2
        exit 1
    fi
done

# Build necessary components in specified order, adding to repo along the way:
azldev comp build --local-repo-with-publish ./base/out azurelinux-rpm-config azurelinux-release azurelinux-repos rpm

# Build a base container image using these private RPMs and upstream Fedora packages.
azldev image build --local-repo ./base/out container-base

# Run a command in the container to verify.
xzcat ./base/out/images/container-base/azl4-container-base.x86_64-0.1.docker.tar.xz | docker load
docker run -it --rm microsoft/azurelinux/base/core:4.0 cat /etc/os-release
