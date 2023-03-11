
# Build Requirements on `Ubuntu`

## Requirements were validated on `Ubuntu 18.04`

This page lists host machine requirements for building with the CBL-Mariner toolkit. They cover building the toolchain, packages, and images on an Ubuntu 18.04 host.

```bash
# Add a backports repo in order to install the latest version of Go.
sudo add-apt-repository ppa:longsleep/golang-backports
sudo apt-get update

# Install required dependencies.
sudo apt -y install curl gawk genisoimage git golang-1.17-go make parted qemu-utils rpm tar wget

# Recommended but not required: `pigz` for faster compression operations.
sudo apt -y install pigz

# Fix go 1.17 link
sudo ln -vsf /usr/lib/go-1.17/bin/go /usr/bin/go

# Install and configure Docker.
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
# Log into the docker group, to avoid needing to first log out / log in
newgrp docker
```
