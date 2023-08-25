
# Build Requirements on `Ubuntu`

## Requirements were validated on `Ubuntu 18.04`

This page lists host machine requirements for building with the CBL-Mariner toolkit. They cover building the toolchain, packages, and images on an Ubuntu 18.04 host.

```bash
# Add a backports repo in order to install the latest version of Go.
sudo add-apt-repository ppa:longsleep/golang-backports
sudo apt-get update

# Install required dependencies.
# Recommended but not required: `pigz` for faster compression operations.
sudo apt -y install \
    acl \
    curl \
    gawk \
    genisoimage \
    git \
    golang-1.19-go \
    make \
    parted \
    pigz \
    qemu-utils \
    rpm \
    tar \
    wget \
    xfsprogs

# Fix go 1.19 link
sudo ln -vsf /usr/lib/go-1.19/bin/go /usr/bin/go

# Install and configure Docker.
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

**You will need to log out and log back in** for user changes to take effect.
