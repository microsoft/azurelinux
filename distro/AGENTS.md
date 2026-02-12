# Distro Configuration — Agent Guide

⚠️ Distro-wide config — changes here affect every component build. (See [azldev.toml](../azldev.toml) — `distro/` is shared across all projects.)

## Structure

- `distro.toml` — includes all `*.distro.toml`
- `azurelinux.distro.toml` — Azure Linux 4.0 definition (versions, mock configs, build defaults)
- `fedora.distro.toml` — Fedora definition (dist-git URIs, lookaside, version branches)
- `mock/` — Mock build environment configs

## Build Defaults

Default upstream: **Fedora 43** (in `azurelinux.distro.toml`). Inherited by all components unless overridden via `build.defines`:

- `dist = ".azl4"`, `vendor = "Microsoft Corporation"`, `distribution = "Azure Linux"`, `rhel = "10"`
