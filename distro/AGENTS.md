# Distro Configuration — Agent Guide

⚠️ Distro-wide config — changes here affect every component build. (See [azldev.toml](../azldev.toml) — `distro/` is shared across all projects.)

## Structure

- `distro.toml` — includes all `*.distro.toml`
- `azurelinux.distro.toml` — Azure Linux distro definitions and build defaults
- `fedora.distro.toml` — Fedora definition (dist-git URIs, lookaside, version branches)
- `mock/` — Mock build environment configs

## Build Defaults

Default upstream: **Fedora 43** (in `azurelinux.distro.toml`), unless overridden by a component's spec source.
