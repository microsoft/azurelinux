---
name: azl-mock
description: "Test and inspect packages in Azure Linux mock chroots. Use when testing built RPMs, inspecting dependencies, debugging runtime issues, or verifying package contents. Triggers: test package, mock shell, inspect rpm, smoke test, chroot, verify build output."
---

# Test & Inspect in Mock Chroot

> **Never install built RPMs on the host.** They target Azure Linux, not your dev machine. Use the methods below instead.

## Resetting the Mock Chroot

`azldev` has no built-in mock reset. Use `mock` directly when you need to clear stale state:

```bash
# Clean just the chroot (fast, keeps bootstrap)
mock --quiet -r distro/mock/azurelinux-4.0-x86_64.cfg --configdir distro/mock --scrub=chroot

# Nuclear — clean everything including bootstrap
mock --quiet -r distro/mock/azurelinux-4.0-x86_64.cfg --configdir distro/mock --scrub=all
```

## Non-Interactive Chroot (preferred for agents)

Pipe commands via heredoc — fully autonomous, no user interaction needed:

```bash
azldev adv mock shell --add-package /path/to/package.rpm <<'CMDS'
<command> --version
echo "exit code: $?"
exit
CMDS
```

Use this for automated checks: running binaries, querying installed packages, inspecting paths.

## Inspect RPM Without Installing (debug failed installs, examine contents)

When `--add-package` fails, or you just want to inspect without installing, use `mock --copyin` to copy the RPM into the chroot and inspect it there:

```bash
# Copy the RPM into the chroot (does NOT install it)
mock -r distro/mock/azurelinux-4.0-x86_64.cfg --configdir distro/mock \
  --copyin base/out/<name>*.rpm /tmp/

# Enter the chroot and inspect
azldev adv mock shell <<'CMDS'
rpm -qip /tmp/<name>*.rpm       # package info
rpm -qlp /tmp/<name>*.rpm       # file list
rpm -qRp /tmp/<name>*.rpm       # dependencies
dnf install /tmp/<name>*.rpm    # retry install to see error details
exit
CMDS
```

This avoids installing on the host and gives you the full Azure Linux environment for debugging dependency issues, file conflicts, etc.

## Interactive Chroot

Use when you need to explore interactively or run multiple diagnostic commands:

```bash
azldev adv mock shell --add-package /path/to/package.rpm --enable-network
```

### Agent workflow — follow these steps exactly:

1. Run a simple command (e.g., `echo "ready"`) in a **non-background** terminal to establish the shared shell.
2. Ask the user to run the `azldev adv mock shell` command above **in that same terminal**.
3. Wait for the user to confirm they are in the mock shell.
4. Run diagnostic commands in the **same non-background terminal** — they execute inside the chroot. Do NOT use background terminals (`isBackground=true`) — you cannot send commands to them.
5. The Ctrl+C sent before each command is harmless — interactive shells trap SIGINT.
6. Run `exit` when done to leave the chroot.

Prefer the non-interactive heredoc approach when possible. Use interactive only when you need to react to output between commands.

## Key Flags

| Flag | Purpose |
|------|---------|
| `-p`, `--add-package <path>` | Install a package into the chroot before entering. Accepts RPM file paths or package names. Can be repeated. |
| `--enable-network` | Allow network access (dependency resolution, downloads) |

> ⚠️ **`-p` means `--add-package`, not component name.** Unlike `comp build -p <name>`, `mock shell` has no component selector. The `-p` shorthand is `--add-package`. Passing `-p <name>` installs a package by name from configured repos — it does NOT set up a chroot with that component's build dependencies.

## Gotchas

- **Don't mix `-p <name>` with `--add-package /path/to/name.rpm` for the same package.** Since `-p` IS `--add-package`, passing both `-p cowsay --add-package ./cowsay.rpm` tells dnf to install the repo version AND your local RPM — two different builds of the same package, which conflicts. Use one or the other:
  - `--add-package /path/to/rpm` to install your locally built RPM
  - `-p <name>` to install a package by name from configured repos
- **Mock chroot is persistent.** State survives between `azldev adv mock shell` sessions — installed packages, created files, etc. all persist. This is useful (install once, re-enter later) but can cause confusion from stale state. Use `mock --scrub=chroot` to reset when needed (see "Resetting the Mock Chroot" above).
- **Use a temp dir for `prep-sources` output.** Use `--force` to overwrite an existing output dir. Note that `prep-sources -o <dir>` writes to a user-specified dir, NOT `base/out/` (that's for `comp build` output).
- **One mock session per terminal.** If a terminal is already inside mock shell, running `azldev adv mock shell` again will fail. Run `exit` first.
- **`advanced` is hidden.** `azldev adv` (alias for `advanced`) doesn't appear in `azldev --help` but contains `mock shell`, `mock build-rpms`, `mcp`, and `wget`.
