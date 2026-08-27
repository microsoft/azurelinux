
# Build Requirements for Azure Linux Toolkit on Ubuntu

This page outlines the requirements for building with the Azure Linux toolkit on Ubuntu.

## System-Specific Requirements

### Golang Package Requirements

The Azure Linux toolkit requires Go 1.25 or newer.

Ubuntu 26.04 packages Go 1.25 as `golang-1.25-go`, but the older releases still in common use
(22.04, 24.04) do not package it at all. Unless your `PATH` already has Go 1.25 or newer, the
prerequisites script picks a source at runtime:

1. **The distro package**, when apt has a `golang-1.25-go` candidate (Ubuntu 26.04 and newer). Go is
   installed into `/usr/lib/go-1.25`. This keeps working on hosts that can reach an apt mirror but
   have no access to the public internet.
2. **The upstream toolchain**, when apt has no candidate. The pinned tarball is downloaded from
   [go.dev/dl](https://go.dev/dl), verified against a SHA256 checksum, and unpacked into
   `/usr/local/go`. `amd64` and `arm64` are supported; on any other architecture the script stops and
   asks you to install Go yourself.

Either way `go` and `gofmt` are symlinked into `/usr/bin`, so no separate step is needed.

A Go toolchain that is already installed in either location and reports 1.25 or newer is reused
as-is — the script only ever replaces a `/usr/local/go` that is too old, and says so before it does.

If some other `go` sits earlier on `PATH` than `/usr/bin` — `/usr/local/bin/go` is the usual
culprit, since both Ubuntu's default `PATH` and `sudo`'s `secure_path` list `/usr/local/bin` first —
the script names it and warns that it will be used instead. That is only a problem if the shadowing
copy is too old — remove it if the build later reports an unsupported Go version.

The pinned version and its checksums are the `GO_VERSION`/`GO_SHA256_*` variables at the top of
`prerequisites-ubuntu.sh` and must be updated together.

To use a Go you have installed yourself instead, make sure it is on `PATH` and reports 1.25 or
newer; the script will detect it and skip the download.

#### Updating the pinned Go version

Go supports only the two most recent release series: when 1.N ships, 1.(N-2) stops receiving
security fixes. This pin therefore moves on Go's release cadence rather than Azure Linux's, and
CVE fixes are a routine reason to move it. <https://go.dev/dl> lists the supported releases.

Bumping the *patch* release (1.25.x → 1.25.y) means editing `prerequisites-ubuntu.sh` alone:

1. Set `GO_VERSION`.
2. Set `GO_SHA256_AMD64` and `GO_SHA256_ARM64` from <https://go.dev/dl> in the same change — the
   checksums are version-specific, and a stale one aborts the install with a message naming the
   constant that needs refreshing.

Bumping the *minor* release (1.25 → 1.26) additionally requires, all in one change:

| Location | What to change |
| --- | --- |
| `prerequisites-ubuntu.sh` | `GO_APT_PACKAGE`, `GO_APT_ROOT`, and the version regex in `go_version_ok` |
| `toolkit/tools/go.mod` | the `go` directive, which `toolkit/scripts/tools.mk` turns into the build-time minimum |
| `.github/workflows/go-test-coverage.yml` | `EXPECTED_GO_VERSION`, which both selects the CI toolchain and asserts the `go.mod` directive matches |
| `prerequisites-ubuntu.md`, `prerequisites-mariner.md` | the stated minimum version |

Leaving any of them behind either fails CI or, worse, installs a toolchain the build then rejects.

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

- `--fix-go-links`: Re-creates the `/usr/bin` symlinks for the Go binaries, pointing them at
  whichever Go root is installed (`/usr/lib/go-1.<minor_version>` or `/usr/local/go`). The
  prerequisites installation already does this, so it is only needed to repair the links.
- `--configure-docker`: Installs Docker and adds your user to the docker group
- `--no-install-prereqs`: Skips installation of prerequisite packages
- `--help`: Displays usage information

> **Note**: If you use `--configure-docker`, you will need to log out and log back in for the user changes to take effect.
