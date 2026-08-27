
# Build Requirements for Azure Linux Toolkit on Ubuntu

This page outlines the requirements for building with the Azure Linux toolkit on Ubuntu.

## System-Specific Requirements

### Golang Package Requirements

The Azure Linux toolkit requires Go 1.25 or newer.

Ubuntu 26.04 packages Go 1.25 as `golang-1.25-go`, but the older releases still in common use
(22.04, 24.04) do not package it at all. The prerequisites script therefore checks the Go already on
your `PATH` and, unless it is 1.25 or newer, downloads the pinned upstream toolchain from
[go.dev/dl](https://go.dev/dl), verifies its SHA256 checksum, unpacks it into `/usr/local/go` and
symlinks `go` and `gofmt` into `/usr/bin`. `amd64` and `arm64` are supported; on any other
architecture the script stops and asks you to install Go yourself.

The pinned version and its checksums are the `GO_VERSION`/`GO_SHA256_*` variables at the top of
`prerequisites-ubuntu.sh` and must be updated together.

To use a Go you have installed yourself instead, make sure it is on `PATH` and reports 1.25 or
newer; the script will detect it and skip the download.

## Installation Methods

### Method 1: Using Make Targets (Recommended)

The make targets automatically install the appropriate packages:

```bash
# For interactive development environments (local machines)
# Installs prerequisites but doesn't modify system configuration
sudo make -C toolkit install-prereqs

# Manually configure Docker if needed
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
# Note: You will need to log out and log back in for user changes to take effect

# the above step can alternatively be done using the following command if preferred:
# sudo ./toolkit/docs/building/prerequisites-ubuntu.sh --no-install-prereqs --configure-docker

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

# Manually configure Docker if needed
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
# Note: You will need to log out and log back in for user changes to take effect

# the above step can alternatively be done using the following command if preferred:
# sudo ./toolkit/docs/building/prerequisites-ubuntu.sh --no-install-prereqs --configure-docker
```

## Script Options

The `prerequisites-ubuntu.sh` script supports the following options:

- `--fix-go-links`: Re-creates the `/usr/bin` symlinks for the Go binaries in `/usr/local/go`. The
  prerequisites installation already does this, so it is only needed to repair the links.
- `--configure-docker`: Installs Docker and adds your user to the docker group
- `--no-install-prereqs`: Skips installation of prerequisite packages
- `--help`: Displays usage information

> **Note**: If you use `--configure-docker`, you will need to log out and log back in for the user changes to take effect.
