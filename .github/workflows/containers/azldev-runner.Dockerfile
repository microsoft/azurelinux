FROM mcr.microsoft.com/azurelinux/base/core:3.0

# Generic azldev runner image for CI PR checks. Provides the toolchain
# required to run arbitrary `azldev` subcommands (render, build, ...)
# against an untrusted PR checkout.
#
# Callers are expected to bind-mount:
#   /workdir   : PR checkout (typically rw — azldev writes specs/ and build/)
#   /output    : trusted-shape outputs produced by the container (ro on host)
#   /scripts   : trusted helper scripts from the base branch (ro)
#
# `azldev` is baked into the image (installed to /usr/local/bin) so callers
# don't need to set up Go or bind-mount a GOPATH.
#
# Kept intentionally minimal — anything that isn't needed by every azldev
# workflow should be added by the caller (e.g. via a derived image) rather
# than baked in here.
# build-essential + openssl/symcrypt/symcrypt-openssl: required by Microsoft
# Go's default `systemcrypto` GOEXPERIMENT (cgo at build time, system crypto
# libs at run time). See:
# https://github.com/microsoft/go/blob/microsoft/main/eng/doc/MigrationGuide.md
RUN tdnf -y install \
    build-essential \
    ca-certificates \
    git \
    golang \
    jq \
    mock \
    mock-rpmautospec \
    openssl \
    python3 \
    shadow-utils \
    sudo \
    symcrypt \
    symcrypt-openssl \
    && tdnf clean all

# The version is passed in as a build arg from .azldev-version in the repo
# root.  Callers (check-rendered-specs.yml, etc.) read the file and pass it
# via --build-arg so the Dockerfile never needs repo-root build context.
# No default — omitting --build-arg will fail the build loudly.
ARG AZLDEV_VERSION
RUN test -n "${AZLDEV_VERSION}" || { echo "ERROR: AZLDEV_VERSION build-arg is required (read from .azldev-version)" >&2; exit 1; } \
    && GOBIN=/usr/local/bin go install \
    "github.com/microsoft/azure-linux-dev-tools/cmd/azldev@${AZLDEV_VERSION}" \
    && rm -rf /root/go /root/.cache

ARG UID=1000

RUN useradd -u "${UID}" -G mock -m builduser

USER builduser
WORKDIR /workdir
