# Package Management

This fork ships both `tdnf` and `dnf`. They are used for different purposes.

---

## The Split Role Model

| Tool | Role | When to use |
|------|------|-------------|
| `tdnf` (v3.5.8) | Default system/CLI package manager | Day-to-day package installs, scripted provisioning, image builds |
| `dnf` (v4.19.0) | Desktop tooling compatibility layer | GUI software centers, admin tooling that expects a DNF Python API |

`tdnf` is the primary package manager in this distro — it is the tool that the Azure Linux build pipeline (`imager`) itself uses internally and the one that starts faster, uses less memory, and runs with no Python dependency. It is the default `yum`-compatible command on the system (`tdnf` obsoletes `yum`).

`dnf` is installed alongside `tdnf` to support desktop-layer tooling (e.g., future PackageKit backends, `dnf-automatic`, admin scripts written against the DNF Python API). Both managers read the same `/etc/yum.repos.d/` repository configuration and operate on the same RPM database, so they are safe to use interchangeably from the user's perspective.

---

## Common Operations

Both `tdnf` and `dnf` share the same command interface. Substitute either command name.

### Install a package

```bash
sudo tdnf install <package>
```

### Remove a package

```bash
sudo tdnf remove <package>
```

### Update all packages

```bash
sudo tdnf update
```

### Search for a package

```bash
tdnf search <keyword>
```

### List installed packages

```bash
tdnf list installed
```

### Query package information

```bash
tdnf info <package>
```

### Check for available updates

```bash
tdnf check-update
```

### Clean cached metadata

```bash
sudo tdnf clean all
```

---

## Repository Configuration

Repositories are configured in `/etc/yum.repos.d/` as standard `.repo` files, identical in format to Fedora/RHEL. Both `tdnf` and `dnf` read from the same directory.

Example repository file:

```ini
[protagonist-base]
name=Protagonist Linux - Base
baseurl=https://packages.example.com/protagonist/3.0/$basearch/
enabled=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-protagonist
```

The `tdnf-plugin-repogpgcheck` plugin (enabled by default in this distro) additionally verifies **repository metadata GPG signatures**, not just package signatures. Do not disable it.

---

## Desktop GUI Software Management

COSMIC's `cosmic-store` is the intended graphical package manager for this distro. It will target the DNF/PackageKit stack. Until `cosmic-store` is packaged and a PackageKit backend is available, use `tdnf` or `dnf` from the terminal for all package management.

---

## Notes for Package Maintainers

- **New packages** go in `SPECS/<name>/<name>.spec` with a corresponding `<name>.signatures.json` sidecar — the build system picks them up automatically.
- The build pipeline invokes `tdnf` (not `dnf`) internally inside chroot environments during image assembly.
- `dnf-plugins-core` (v4.x) is available in `SPECS/dnf-plugins-core/` if additional DNF plugin functionality is needed.
- `dnf5` is also present in `SPECS/dnf5/` as a future migration path, but is not the default in this release.
