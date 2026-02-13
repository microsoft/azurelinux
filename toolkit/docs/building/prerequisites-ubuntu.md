
# Build Requirements for Azure Linux Toolkit on Ubuntu

This page outlines the requirements for building with the Azure Linux toolkit on Ubuntu.

## System-Specific Requirements

### Golang Package Requirements

The Azure Linux toolkit on Ubuntu has been validated with the following:

- **Ubuntu 22.04**: Validated with `go1.21.1` (available as `golang-1.21-go` package)

## Installation Methods

### Method 1: Using Make Targets (Recommended)

The make targets automatically install the appropriate packages:

```bash
# For interactive development environments (local machines)
# Installs prerequisites but doesn't modify system configuration
sudo make -C toolkit install-prereqs

# Manually create Go symlinks for proper PATH integration
sudo ln -sf /usr/lib/go-1.21/bin/go /usr/bin/go
sudo ln -sf /usr/lib/go-1.21/bin/gofmt /usr/bin/gofmt

# Manually configure Docker if needed
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
# Note: You will need to log out and log back in for user changes to take effect

# the above 2 steps can alternatively be done using the following command if preferred:
# sudo ./toolkit/docs/building/prerequisites-ubuntu.sh --no-install-prereqs --fix-go-links --configure-docker

----------------------

# For automated environments (CI/CD pipelines) or complete setup
# Installs prerequisites AND configures Docker and Go links
sudo make -C toolkit install-prereqs-and-configure
```

**Recommendation**: 
- Use `install-prereqs` on your local development machine
- Use `install-prereqs-and-configure` in CI/CD pipelines or when you need a complete environment setup

### Method 2: Direct Script Execution

If you prefer running the script directly, you have several options:

```bash
# Basic installation with Go
sudo ./toolkit/docs/building/prerequisites-ubuntu.sh

# Manually create Go symlinks for proper PATH integration
sudo ln -sf /usr/lib/go-1.23/bin/go /usr/bin/go
sudo ln -sf /usr/lib/go-1.23/bin/gofmt /usr/bin/gofmt

# Manually configure Docker if needed
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
# Note: You will need to log out and log back in for user changes to take effect

# the above 2 steps can alternatively be done using the following command if preferred:
# sudo ./toolkit/docs/building/prerequisites-ubuntu.sh --no-install-prereqs --fix-go-links --configure-docker
```

## Script Options

The `prerequisites-ubuntu.sh` script supports the following options:

- `--fix-go-links`: Creates symbolic links for Go binaries to make them available in your PATH
- `--configure-docker`: Installs Docker and adds your user to the docker group
- `--no-install-prereqs`: Skips installation of prerequisite packages
- `--help`: Displays usage information

> **Note**: If you use `--configure-docker`, you will need to log out and log back in for the user changes to take effect.
