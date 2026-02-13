---
name: azl-build-component
description: |
  Build and test Azure Linux components using azldev. Use when building packages,
  debugging build failures, inspecting mock chroots, preparing sources, or working
  with the build inner loop. Triggers: "build component", "build failed",
  "mock shell", "prepare sources", "debug build", "build error", etc.
---

# Build & Debug Components

> **TODO:** This skill is a placeholder. Full instructions will cover:
>
> - Basic build sequence (`azldev comp build -p <name>`, `createrepo_c`, chained builds)
> - Debugging: inspecting pre/post overlay sources with `azldev comp prep-sources`
> - Preserving the build environment on failure (`--preserve-buildenv on-failure`)
> - Entering a mock shell for interactive debugging (`azldev advanced mock shell`)
> - Per-component build overrides via `build.defines`
> - Key locations: `base/out/`, `base/build/logs/`, mock chroot
