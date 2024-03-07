
# Build Requirements on `Ubuntu`

## Requirements were validated on `Ubuntu 22.04`

This page lists host machine requirements for building with the CBL-Mariner toolkit. They cover building the toolchain, packages, and images on an Ubuntu 22.04 host.

```bash
sudo apt-get update

# Install required dependencies.
# Recommended but not required: `pigz` for faster compression operations.
sudo apt -y install \
    acl \
    curl \
    gawk \
    genisoimage \
    git \
    golang-1.20-go \
    make \
    parted \
    pigz \
    openssl \
    qemu-utils \
    rpm \
    tar \
    wget \
    xfsprogs

# Fix go 1.20 link
sudo ln -vsf /usr/lib/go-1.20/bin/go /usr/bin/go
sudo ln -vsf /usr/lib/go-1.20/bin/gofmt /usr/bin/gofmt

# Install and configure Docker.
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

**You will need to log out and log back in** for user changes to take effect.
