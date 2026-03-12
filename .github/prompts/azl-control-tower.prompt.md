---
description: "Get information about Azure Linux builds from Control Tower. Use this prompt to check build status, view logs, or query build metadata. You can ask for specific builds by package name or target type (e.g., bootstrap/stage 1 vs rpms-target/stage 2)."
---

# Control Tower Build Information
- **Package name**: `${input:package_name:name of the package}`
- **Target type**: `${input:target_type:type of build target (e.g., *bootstrap* for stage 1, *rpms-target* for stage 2)}`

Follow the [skill-control-tower skill](../skills/skill-control-tower/SKILL.md) to retrieve information about builds matching the specified package name or target type. You can check build status, view logs, and query build metadata to get insights into the build process and diagnose any issues.
