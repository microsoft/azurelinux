
# Build Requirements for Azure Linux Toolkit

This page outlines the requirements for building with the Azure Linux toolkit on different versions of Azure Linux/Mariner.

## System-Specific Requirements

### Golang Package Requirements

Different versions of Azure Linux have been validated with the following Golang packages:

- **Azure Linux 2.0 (CBL-Mariner)**: Validated with `msft-golang-1.24.1`
- **Azure Linux 3.0**: Validated with `golang-1.24.3`

## Installation Methods

### Method 1: Using Make Targets (Recommended)

The make targets automatically detect your OS version and install the appropriate packages:

```bash
# For interactive development environments (local machines)
# Installs prerequisites but doesn't modify system configuration
# Note: On Azure Linux 2.0, this will remove golang if installed in favor of msft-golang due to the golang version requirement
sudo make -C toolkit install-prereqs

# Manually configure Docker if needed
sudo systemctl enable --now docker.service
sudo usermod -aG docker $USER
# Note: You will need to log out and log back in for user changes to take effect

# the above step can alternatively be done using the following command if preferred:
# sudo ./toolkit/docs/building/prerequisites-mariner.sh --no-install-prereqs --configure-docker

--------------

# For automated environments (CI/CD pipelines) or complete setup
# Installs prerequisites AND configures Docker and user settings
sudo make -C toolkit install-prereqs-and-configure
```

**Recommendation**: 
- Use `install-prereqs` on your local development machine
- Use `install-prereqs-and-configure` in CI/CD pipelines or when you need a complete environment setup

### Method 2: Direct Script Execution

If you prefer running the script directly, use the appropriate options for your OS version:

#### For Azure Linux 2.0 (CBL-Mariner):
```bash
# Install prerequisites with msft-golang
# Note: This will remove golang if installed in favor of msft-golang due to the golang version requirement
sudo ./toolkit/docs/building/prerequisites-mariner.sh --use-msft-golang

# Manually configure Docker if needed
sudo systemctl enable --now docker.service
sudo usermod -aG docker $USER
# Note: You will need to log out and log back in for user changes to take effect

# the above step can alternatively be done using the following command if preferred:
# sudo ./toolkit/docs/building/prerequisites-mariner.sh --no-install-prereqs --configure-docker
```

#### For Azure Linux 3.0:
```bash
# Install prerequisites with standard golang
sudo ./toolkit/docs/building/prerequisites-mariner.sh

# Manually configure Docker if needed
sudo systemctl enable --now docker.service
sudo usermod -aG docker $USER
# Note: You will need to log out and log back in for user changes to take effect

# the above step can alternatively be done using the following command if preferred:
# sudo ./toolkit/docs/building/prerequisites-mariner.sh --no-install-prereqs --configure-docker
```

## Script Options

The `prerequisites-mariner.sh` script supports the following options:

- `--configure-docker`: Enables Docker service at boot and adds your user to the docker group
- `--no-install-prereqs`: Skips installation of prerequisite packages
- `--use-msft-golang`: Uses `msft-golang-1.24.1` instead of `golang-1.24.3` (required for Azure Linux 2.0)
- `--help`: Displays usage information

> **Note**: If you use `--configure-docker`, you will need to log out and log back in for the user changes to take effect.