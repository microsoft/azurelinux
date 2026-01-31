#!/bin/bash
set -euo pipefail
exec 3> ./demo-build.trc
BASH_XTRACEFD=3
set -x

echo -e "\e[0;33mbash trace, -x output is in ./demo-build.trc\e[0m"

#
# NOTE: This script is a throwaway script. Please think ~~twice~~ thrice before you
# consider adding anything to it. Let us push all dev-tooling into azldev.
#

# Confirm working dir.
if [ ! -f azldev.toml ]; then
    echo "ERROR: This script must be run from the root of the repo" >&2
    exit 1
fi

# Check prereqs.
for prereq in azldev kiwi createrepo_c docker mock qemu-system-x86_64 ; do
    if ! command -v $prereq >/dev/null 2>&1; then
        echo "ERROR: Missing prerequisite '$prereq'." >&2
        exit 1
    fi
done

if [ "$(getenforce)" != "Permissive" ] ; then
    echo "SElinux is not set to 'Permissive'."
    echo "That is required for kiwi to build images, aborting."
    exit 1
fi

if [[ "$#" -ne 1 || ! "$1" =~ container|vm|vm-boot ]] ; then
    echo "Usage: $0 <container|vm|vm-boot>"
    echo "Build container or vm image, or build vm image and boot with qemu."
    exit 1
fi

image_type="$1"
echo "Building a \"$image_type\" image"

# Build azurelinux-rpm-config to generate systemd macros, etc.
azldev comp build azurelinux-rpm-config && createrepo_c ./base/out

# Build azurelinux-release and azurelinux-repos to provide repo files and release info.
# They require the rpm-config package to be built first.
azldev comp build azurelinux-release --local-repo ./base/out && createrepo_c ./base/out
azldev comp build azurelinux-repos --local-repo ./base/out && createrepo_c ./base/out
azldev comp build azurelinux-config --local-repo ./base/out && createrepo_c ./base/out

# Build rpm to ensure the azl-specific vendor tag is configured.
azldev comp build rpm --local-repo ./base/out && createrepo_c ./base/out

function build_container_image() {
    # Build a base container image using these private RPMs and upstream Fedora packages.
    sudo kiwi --loglevel 10 \
         --kiwi-file container-base.kiwi \
         system build \
         --description ./base/images/container-base \
         --target-dir ./base/out/images \
         --add-repo="file:///$PWD/base/out,rpm-md,azl,1"

    # Run a command in the container to verify.
    xzcat ./base/out/images/azl4-container-base.x86_64-0.1.docker.tar.xz | docker load
    docker run -it --rm microsoft/azurelinux/base/core:4.0 cat /etc/os-release
}

function build_vm_image() {
    # Build the VM image using kiwi via azldev 
    azldev image build vm-base --local-repo base/out
}

function boot_vm() {
    # boot QEMU VM, C-a x to quit. VM port 22 is forwarded to host:2222
    echo "Launching VM from image 'vm-base', type 'C-a x' to quit."
    echo "Login as user/pass: 'test/${1}': ssh -p 8888 test@localhost"
    azldev image boot vm-base --test-password "${1}"
}

if [[ "$image_type" == "container" ]] ; then
    build_container_image
elif [[ "$image_type" == "vm" || "$image_type" == "vm-boot" ]] ; then
    # You may need this cleanup until azldev is fixed:
    # sudo rm -rf $(git rev-parse --show-toplevel)/base/out/images
    build_vm_image
    if [[ "$image_type" == "vm-boot" ]] ; then
	boot_vm "$(mktemp -u XXXXXX)"
    fi
else
    echo "Unknown image type '$image_type'"
fi
