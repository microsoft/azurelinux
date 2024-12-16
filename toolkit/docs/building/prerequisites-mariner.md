
# Build Requirements on `Azure Linux`

## Requirements were validated on `Azure Linux`

This page lists host machine requirements for building with the Azure Linux toolkit. They cover building the toolchain, packages, and images on an Azure Linux host.

```bash
# Install required dependencies.
sudo ./toolkit/docs/building/prerequisites-mariner.sh

# Also supported is:
#    make -C toolkit install-prereqs

# Enable Docker daemon at boot
sudo systemctl enable --now docker.service

# Add current user to docker group
sudo usermod -aG docker $USER
```
