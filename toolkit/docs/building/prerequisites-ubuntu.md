
# Build Requirements on `Ubuntu`

## Requirements were validated on `Ubuntu 22.04`

This page lists host machine requirements for building with the Azure Linux toolkit. They cover building the toolchain, packages, and images on an Ubuntu 22.04 host.

```bash
# Install required dependencies
sudo ./toolkit/docs/building/prerequisites-ubuntu.sh

# Alternatively, install dependencies and fix Go links
sudo ./toolkit/docs/building/prerequisites-ubuntu.sh --fix-go-links

# Or install dependencies, fix Go links, and set up Docker
sudo ./toolkit/docs/building/prerequisites-ubuntu.sh --fix-go-links --configure-docker

# To see all available options
sudo ./toolkit/docs/building/prerequisites-ubuntu.sh --help

# Also supported is:
#    make -C toolkit install-prereqs
```

If you chose to configure Docker with `--configure-docker`, **you will need to log out and log back in** for the user changes to take effect.

### Script Options

The `prerequisites-ubuntu.sh` script supports the following options:

- `--fix-go-links`: Creates symbolic links for Go binaries to make them available in your PATH
- `--configure-docker`: Installs Docker and adds your user to the docker group
- `--no-install-prereqs`: Skips installation of prerequisite packages
- `--help`: Displays usage information
