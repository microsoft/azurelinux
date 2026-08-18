
# Build Requirements for Azure Linux Toolkit on Ubuntu

This page outlines the requirements for building with the Azure Linux toolkit on Ubuntu.

## System-Specific Requirements

### Golang Package Requirements

The prerequisite script installs `golang-1.24-go` as a bootstrap toolchain. Toolkit Go commands use Go's automatic toolchain management to download and run the version required by `toolkit/tools/go.mod`. This allows the same prerequisite package to support Ubuntu 24.04 and 26.04 when the toolkit requires a newer Go release.

Automatic toolchain downloads use the configured `GOPROXY` and are stored in the invoking user's Go module cache. Each account that builds the toolkit, including `root` when invoking Make with `sudo`, must have network access or a pre-populated cache.

Downloaded toolchains omit the `covdata` executable used by toolkit coverage tests. The `tool cmd/covdata` directive in `toolkit/tools/go.mod` makes Go build and run it from the selected toolchain's source when needed.

To download the required toolchain before starting a build:

```bash
cd toolkit/tools
GOTOOLCHAIN=auto go version
```

## Installation Methods

### Method 1: Using Make Targets (Recommended)

The make targets automatically install the appropriate packages:

```bash
# For interactive development environments (local machines)
# Installs prerequisites but doesn't modify system configuration
sudo make -C toolkit install-prereqs

# Manually create Go symlinks for proper PATH integration
sudo ln -sf /usr/lib/go-1.24/bin/go /usr/bin/go
sudo ln -sf /usr/lib/go-1.24/bin/gofmt /usr/bin/gofmt

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
sudo ln -sf /usr/lib/go-1.24/bin/go /usr/bin/go
sudo ln -sf /usr/lib/go-1.24/bin/gofmt /usr/bin/gofmt

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
