
# Build Requirements on `Azure Linux`

## Requirements were validated on `Azure Linux`

This page lists host machine requirements for building with the Azure Linux toolkit. They cover building the toolchain, packages, and images on an Azure Linux host.

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
    xfsprogs \
    zstd

# Enable Docker daemon at boot
sudo systemctl enable --now docker.service

# Add current user to docker group
sudo usermod -aG docker $USER
```
