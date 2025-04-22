
# Build Requirements on `Ubuntu`

## Requirements were validated on `Ubuntu 22.04`

This page lists host machine requirements for building with the Azure Linux toolkit. They cover building the toolchain, packages, and images on an Ubuntu 22.04 host.

```bash
# Install required dependencies.
sudo ./toolkit/docs/building/prerequisites-ubuntu.sh

# Also supported is:
#    make -C toolkit install-prereqs

# Fix go 1.21 link
sudo ln -vsf /usr/lib/go-1.21/bin/go /usr/bin/go
sudo ln -vsf /usr/lib/go-1.21/bin/gofmt /usr/bin/gofmt

# Install and configure Docker.
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

**You will need to log out and log back in** for user changes to take effect.
