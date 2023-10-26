
# Build Requirements on `Mariner`

## Requirements were validated on `Mariner 2.0`

This page lists host machine requirements for building with the CBL-Mariner toolkit. They cover building the toolchain, packages, and images on a Mariner host.

```bash
# Install required dependencies.
# Recommended but not required: `pigz` for faster compression operations.
sudo tdnf -y install \
    acl \
    binutils \
    cdrkit \
    curl \
    dosfstools \
    gawk \
    glibc-devel \
    genisoimage \
    git \
    golang \
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
    tar \
    wget \
    xfsprogs

# Enable Docker daemon at boot
sudo systemctl enable --now docker.service

# Add current user to docker group
sudo usermod -aG docker $USER
```
