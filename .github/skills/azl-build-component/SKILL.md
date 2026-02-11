---
name: azl-build-component
description: "Build and test Azure Linux components using azldev. Use when building packages, debugging build failures, inspecting mock chroots, preparing sources, or working with the build inner loop. Triggers: build component, build failed, mock shell, prepare sources, debug build, build error."
---

# Build & Debug Components

> **Never install built RPMs on the host.** They target Azure Linux, not your dev machine. Use [`azl-mock`](../azl-mock/SKILL.md) for testing.

## Mandatory Testing

> **A successful build is NOT the finish line.** If your change could affect the built RPMs, smoke-test before reporting success. See [`azl-mock`](../azl-mock/SKILL.md).

Pure organizational changes (moving definitions between files, editing comments/descriptions) don't need a rebuild. When in doubt, test.

## Build Output Directories

Build output paths are configured in `base/project.toml` (`output-dir`, `log-dir`, `work-dir`). Default layout:

| `project.toml` key | Default value | Resolves to | Contents |
|---------------------|---------------|-------------|----------|
| `output-dir` | `out` | `base/out/` | Built RPMs and SRPMs |
| `log-dir` | `build/logs` | `base/build/logs/` | Build logs |
| `work-dir` | `build/work` | `base/build/work/` | Per-component working dirs (`<name>/`) |

Paths are relative to the project root (`base/`). Don't edit anything in these dirs — they are generated output.

> **`prep-sources` output is separate.** `comp prep-sources -o <dir>` writes to a user-specified directory, NOT to the project's configured output dirs. Don't look in `base/out/` for `prep-sources` results.

## Build Sequence

```bash
# Build a single component
azldev comp build -p <name> -q

# Build multiple components, auto-publishing RPMs to local repo for chained deps
azldev comp build --local-repo-with-publish ./base/out -p <dep1> -p <dep2> -q

# Rebuild a single component against an already-populated local repo
azldev comp build -p <name> --local-repo ./base/out -q
```

Build foundational packages first (e.g., `azurelinux-rpm-config`), then dependents. See [`scripts/demo-build.sh`](../../../scripts/demo-build.sh) for a working example.

## Dev Inner Loop

The standard cycle for investigating, modifying, and verifying components:

```
investigate → modify → verify → build → test → inspect
```

| Step | Command | What to check |
|------|---------|---------------|
| **Investigate** | `prep-sources --skip-overlays -o my/build/dir/<name>-pre` | Upstream spec/sources as-is |
| **Compare** | `prep-sources -o my/build/dir/<name>-post` + `diff -r ...-pre ...-post` | Current overlay effect |
| **Modify** | Edit `*.comp.toml` (overlays, defines, without) | — |
| **Verify** | `rm -rf .../<name>-post && prep-sources -o my/build/dir/<name>-post` | Overlay applies cleanly |
| **Build** | `comp build -p <name>` | RPMs appear in `base/out/` |
| **Test** | `adv mock shell --add-package base/out/<name>*.rpm` | Package installs, binary runs, basic functionality works |
| **Inspect** | `comp build --preserve-buildenv always` + `adv mock shell` | BUILDROOT contents, file lists |

> Use a temp dir for `prep-sources` output. Clean before each run with `rm -rf` since `prep-sources` fails on non-empty dirs (no `--force` flag).

## Debugging Build Failures

### 1. Diff sources pre/post overlay

```bash
# Clean scratch dirs before each run (prep-sources fails on non-empty dirs)
rm -rf my/build/dir/<name>-pre my/build/dir/<name>-post
azldev comp prep-sources -p <name> --skip-overlays -o my/build/dir/<name>-pre -q
azldev comp prep-sources -p <name> -o my/build/dir/<name>-post -q
diff -r my/build/dir/<name>-pre my/build/dir/<name>-post
```

This reveals whether overlays apply as intended or whether upstream changed.

### 2. Preserve build environment on failure

```bash
azldev comp build -p <name> --preserve-buildenv on-failure -q
# Use `always` to inspect even successful builds
```

### 3. Enter mock shell (deep debug)

For testing built RPMs or inspecting the chroot, see the [`azl-mock`](../azl-mock/SKILL.md) skill. Quick reference:

```bash
# Non-interactive (preferred for agents)
azldev adv mock shell --add-package /path/to/rpm <<'CMDS'
rpm -q <name>
exit
CMDS

# Interactive (requires user cooperation — see azl-mock for agent workflow)
azldev adv mock shell --add-package /path/to/rpm --enable-network
```

> ⚠️ **Don't mix `-p <name>` with `--add-package` for the same package.** `-p` is shorthand for `--add-package`, so `-p cowsay --add-package ./cowsay.rpm` installs two conflicting builds. Use one or the other. See [`azl-mock`](../azl-mock/SKILL.md) for details.

Inside the chroot: `rpmbuild`, `find`, `dnf5` — standard RPM tooling. `BUILDROOT` is at `builddir/build/BUILD/<pkg>-<ver>-build/BUILDROOT/`.

## Per-Component Build Overrides

Use `build.defines` (macros) and `build.without` (disable conditionals) in the component's `.comp.toml`. See [`comp-toml.instructions.md`](../../instructions/comp-toml.instructions.md#build-configuration) for syntax and examples.

Verify with `prep-sources` before doing a full build.

## Reference
- CLI help: `azldev comp build --help`, `azldev advanced mock --help`
- `azldev advanced` (alias `adv`) is hidden from `azldev --help` but contains `mock shell`, `mock build-rpms`, `mcp`, and `wget`.
- [schema reference](../../../external/schemas/azldev.schema.json) (or `azldev config generate-schema > /tmp/schema.json` for latest changes)
