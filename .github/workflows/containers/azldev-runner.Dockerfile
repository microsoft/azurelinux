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
    mock \
    mock-rpmautospec \
    openssl \
    python3 \
    shadow-utils \
    sudo \
    symcrypt \
    symcrypt-openssl \
    && tdnf clean all

# TODO: pin to a tagged release once azure-linux-dev-tools cuts one.
# `@main` is a moving target — fine while azldev is pre-1.0 and we want
# CI to track upstream, but we should swap to `@vX.Y.Z` (and bump it
# deliberately) once the tool stabilizes. ADO #18834
RUN GOBIN=/usr/local/bin go install \
    github.com/microsoft/azure-linux-dev-tools/cmd/azldev@main \
    && rm -rf /root/go /root/.cache

ARG UID=1000

RUN useradd -u "${UID}" -G mock -m builduser

USER builduser
WORKDIR /workdir
