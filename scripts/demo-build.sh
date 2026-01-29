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

TARGET_DIR="/var/tmp/azl-vm-images"

image_type="container"
if [[ "$#" -eq 1 && "$1" == "vm" ]] ; then
    image_type="vm"
    sudo rm -rf "$TARGET_DIR"
fi

echo "Building a '$image_type' image"

# Build azurelinux-rpm-config to generate systemd macros, etc.
azldev comp build azurelinux-rpm-config && createrepo_c ./base/out

# Build azurelinux-release and azurelinux-repos to provide repo files and release info.
# They require the rpm-config package to be built first.
azldev comp build azurelinux-release --local-repo ./base/out && createrepo_c ./base/out
azldev comp build azurelinux-repos --local-repo ./base/out && createrepo_c ./base/out
azldev comp build azurelinux-overrides --local-repo ./base/out && createrepo_c ./base/out

# Build rpm to ensure the azl-specific vendor tag is configured.
azldev comp build rpm --local-repo ./base/out && createrepo_c ./base/out

function kiwi_container_build() {
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

function kiwi_vm_image_build() {
    # Build the VM image using KIWI
    sudo kiwi --loglevel 10 \
         --kiwi-file vm-base.kiwi \
         system build  \
         --description ./base/images/vm-base \
         --target-dir "$TARGET_DIR" \
         --add-repo="file:///$PWD/base/out,rpm-md,azl,1"

    # boot QEMU VM, C-a x to quit. VM port 22 is forwarded to host:2222
    echo "Launching azl4 VM, type 'C-a x' to quit."
    echo "To login as azureuser: ssh -p 2222 azureuser@localhost"
    sudo qemu-system-x86_64 -enable-kvm -m 2048 -cpu host \
         -bios /usr/share/edk2/ovmf/OVMF.stateless.fd \
         -drive file="$TARGET_DIR/azl4-vm-base.x86_64-0.1.vhdx",format=vhdx \
         -netdev user,id=net0,hostfwd=tcp::2222-:22 -device virtio-net-pci,netdev=net0 \
         -nographic -serial mon:stdio
}

if [[ "$image_type" == "container" ]] ; then
    kiwi_container_build
elif [[ "$image_type" == "vm" ]] ; then
    kiwi_vm_image_build
else
    echo "Unknown image type '$image_type'"
fi
