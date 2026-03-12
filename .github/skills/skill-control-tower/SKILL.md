---
name: skill-control-tower
description: "[Skill] Interact with Control Tower and get information about builds. Use when you want to check build status, view logs, or query build metadata. Triggers: control tower, build status, view logs, query build info."
---

# Control Tower Interaction
Control Tower is the central hub for managing and monitoring Azure Linux builds. Use the following commands to interact with Control Tower and retrieve information about your builds.

## Find Builds
To list all recent builds, use the control-tower mcp. This can be package builds or image builds. For package builds, we could ask for a package by name. We could also ask for builds based on the "target" type. A target like `*bootstrap*` is considered a "bootstrap" build or "stage 1" build. A target like `*rpms-target*` is considered a "stage 2" build.
