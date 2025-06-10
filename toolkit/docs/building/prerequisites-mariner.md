
# Build Requirements on `Azure Linux`

## Requirements were validated on `Azure Linux`

This page lists host machine requirements for building with the Azure Linux toolkit. They cover building the toolchain, packages, and images on an Azure Linux host.

```bash
# Install required dependencies
sudo ./toolkit/docs/building/prerequisites-mariner.sh

# Install dependencies and configure Docker
sudo ./toolkit/docs/building/prerequisites-mariner.sh --configure-docker

# To see all available options
sudo ./toolkit/docs/building/prerequisites-mariner.sh --help

# Also supported is:
#    make -C toolkit install-prereqs
```

If you chose to configure Docker with `--configure-docker`, **you will need to log out and log back in** for the user changes to take effect.

### Script Options

The `prerequisites-mariner.sh` script supports the following options:

- `--configure-docker`: Enables Docker service at boot and adds your user to the docker group
- `--no-install-prereqs`: Skips installation of prerequisite packages
- `--help`: Displays usage information
