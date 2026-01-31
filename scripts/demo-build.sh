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

# Build azurelinux-rpm-config to generate system macros, etc.
azldev comp build azurelinux-rpm-config && createrepo_c ./base/out
# Build azurelinux-release and azurelinux-repos to provide repo files and release info.
# They require the rpm-config package to be built first.
azldev comp build azurelinux-release --local-repo ./base/out && createrepo_c ./base/out
azldev comp build azurelinux-repos --local-repo ./base/out && createrepo_c ./base/out
# Build rpm to ensure the azl-specific vendor tag is configured.
azldev comp build rpm --local-repo ./base/out && createrepo_c ./base/out
# Build a base container image using these private RPMs and upstream Fedora packages.
# sudo kiwi --loglevel 10 \
#     --kiwi-file container-base.kiwi \
#     system build \
#     --description ./base/images/container-base \
#     --target-dir ./base/out/images \
#     --add-repo="file:///$PWD/base/out,rpm-md,azl,1"

# # Run a command in the container to verify.
# xzcat ./base/out/images/azl4-container-base.x86_64-0.1.docker.tar.xz | docker load
# docker run -it --rm microsoft/azurelinux/base/core:4.0 cat /etc/os-release
