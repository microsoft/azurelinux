# Mariner Image Customizer configuration

The Mariner Image Customizer is configured using a YAML (or JSON) file.
The top level type for this YAML file is the [Config](#config-type) type.

### Operation ordering

1. Override the `/etc/resolv.conf` file with the version from the host OS.

2. Update packages:

   1. Remove packages ([PackageListsRemove](#packagelistsremove-string),
   [PackagesRemove](#packagesremove-string))

   2. Update base image packages ([UpdateBaseImagePackages](#updatebaseimagepackages-bool)).

   3. Install packages ([PackageListsInstall](#packagelistsinstall-string),
   [PackagesInstall](#packagesinstall-string))

   4. Update packages ([PackageListsUpdate](#packagelistsupdate-string),
   [PackagesUpdate](#packagesupdate-string))

3. Update hostname. ([Hostname](#hostname-string))

4. Copy additional files. ([AdditionalFiles](#additionalfiles-mapstring-fileconfig))

5. Add/update users. ([Users](#users-user))

6. Enable/disable services. ([Services](#services-type))

7. Configure kernel modules.

8. Run post-install scripts. ([PostInstallScripts](#postinstallscripts-script))

9. Run finalize image scripts. ([FinalizeImageScripts](#finalizeimagescripts-script))

10. Delete `/etc/resolv.conf` file.

### /etc/resolv.conf

The `/etc/resolv.conf` file is overridden so that the package installation and
customization scripts can have access to the network.
It is assumed there is a process that runs on boot that will write the
`/etc/resolv.conf` file.
For example, `systemd-resolved`.
Hence, the `/etc/resolv.conf` file is simply deleted at the end instead of being
restored to its original contents.

### Replacing packages

If you wish to replace a package with conflicting package, then you can remove the
existing package using [PackagesRemove](#packagesremove-string) and then install the
new package with [PackagesInstall](#packagesinstall-string).

Example:

```yaml
SystemConfig:
  PackagesRemove:
  - kernel

  PackagesInstall:
  - kernel-hci
```

## Config type

The top-level type of the configuration.

### SystemConfig [[SystemConfig](#systemconfig-type)]

Contains the configuration options for the OS.

```yaml
SystemConfig:
  Hostname: example-image
```

## FileConfig type

Specifies options for placing a file in the OS.

Type is used by: [AdditionalFiles](#additionalfiles-mapstring-fileconfig)

### Path [string]

The absolute path of the destination file.

Example:

```yaml
SystemConfig:
  AdditionalFiles:
    files/a.txt:
    - Path: /a.txt
```

### Permissions [string]

The permissions to set on the destination file.

Supported formats:

- String containing an octal string. e.g. `"664"`

Example:

```yaml
SystemConfig:
  AdditionalFiles:
    files/a.txt:
    - Path: /a.txt
      Permissions: "664"
```

## Module type

Options for configuring a kernel module.

### Name

Name of the module.

```yaml
SystemConfig:
  Modules:
    Load:
    - Name: br_netfilter
```

## Modules type

Options for configuring kernel modules.

### Load [[Module](#module-type)[]]

Sets kernel modules to be loaded automatically on boot.

Implemented by adding an entry to `/etc/modules-load.d/`.

```yaml
SystemConfig:
  Modules:
    Load:
    - Name: br_netfilter
```

### Disable [[Module](#module-type)[]]

Disable kernel modules from being loaded.

Implemented by adding a "blacklist" entry to `/etc/modprobe.d/`.

```yaml
SystemConfig:
  Modules:
    Disable:
    - Name: mousedev
```

## PackageList type

Used to split off lists of packages into a separate file.
This is useful for sharing list of packages between different configuration files.

This type is used by:

- [PackageListsInstall](#packagelistsinstall-string)
- [PackageListsRemove](#packagelistsremove-string)
- [PackageListsUpdate](#packagelistsupdate-string)

### Packages [string[]]

Specifies a list of packages.

Example:

```yaml
Packages:
- openssh-server
```

## Script type

Points to a script file (typically a Bash script) to be run during customization.

### Path [string]

The path of the script.

This must be in the same directory or a sub-directory that the config file is located
in.

Example:

```yaml
SystemConfig:
  PostInstallScripts:
  - Path: scripts/a.sh
```

### Args [string]

Additional arguments to pass to the script.

Example:

```yaml
SystemConfig:
  PostInstallScripts:
  - Path: scripts/a.sh
    Args: abc
```

## Services type

Options for configuring systemd services.

### Enable

A list of services to enable.
That is, services that will be set to automatically run on OS boot.

Example:

```yaml
SystemConfig:
  Services:
    Enable:
    - sshd
```

### Disable

A list of services to disable.
That is, services that will be set to not automatically run on OS boot.

Example:

```yaml
SystemConfig:
  Services:
    Disable:
    - sshd
```

## SystemConfig type

Contains the configuration options for the OS.

### Hostname [string]

Specifies the hostname for the OS.

Implemented by writing to the `/etc/hostname` file.

Example:

```yaml
SystemConfig:
  Hostname: example-image
```

### UpdateBaseImagePackages [bool]

Updates the packages that exist in the base image.

Implemented by calling: `tdnf update`

Example:

```yaml
SystemConfig:
  UpdateBaseImagePackages: true
```

### PackageListsInstall [string[]]

Same as [PackagesInstall](#packagesinstall-string) but the packages are specified in a
separate YAML (or JSON) file.

The other YAML file schema is specified by [PackageList](#packagelist-type).

Example:

```yaml
SystemConfig:
  PackageListsRemove:
  - lists/ssh.yaml
```

### PackagesInstall [string[]]

Installs packages onto the image.

Implemented by calling: `tdnf install`.

Example:

```yaml
SystemConfig:
  PackagesInstall:
  - openssh-server
```

### PackageListsRemove [string[]]

Same as [PackagesRemove](#packagesremove-string) but the packages are specified in a
separate YAML (or JSON) file.

The other YAML file schema is specified by [PackageList](#packagelist-type).

Example:

```yaml
SystemConfig:
  PackageListsRemove:
  - lists/ssh.yaml
```

### PackagesRemove [string[]]

Removes packages from the image.

Implemented by calling: `tdnf remove`

Example:

```yaml
SystemConfig:
  PackagesRemove:
  - openssh-server
```

### PackageListsUpdate [string[]]

Same as [PackagesUpdate](#packagesupdate-string) but the packages are specified in a
separate YAML (or JSON) file.

The other YAML file schema is specified by [PackageList](#packagelist-type).

Example:

```yaml
SystemConfig:
  PackageListsUpdate:
  - lists/ssh.yaml
```

### PackagesUpdate [string[]]

Updates packages on the system.

Implemented by calling: `tdnf update`

Example:

```yaml
SystemConfig:
  PackagesUpdate:
  - openssh-server
```

### AdditionalFiles [Map\<string, [FileConfig](#fileconfig-type)[]>]

Copy files into the OS image.

This property is a dictionary of source file paths to destination files.

The destination files value can be one of:

- The absolute path of a destination file.
- A [FileConfig](#fileconfig-type) object.
- A list containing a mixture of paths and [FileConfig](#fileconfig-type) objects.

Example:

```yaml
SystemConfig:
  AdditionalFiles:
    # Single destination.
    files/a.txt: /a.txt

    # Single destinations with options.
    files/b.txt:
      Path: /b.txt
      Permissions: "664"

    # Multiple destinations.
    files/c.txt:
    - /c1.txt
    - Path: /c2.txt
      Permissions: "664"
```

### PostInstallScripts [[Script](#script-type)[]]

Scripts to run against the image after the packages have been added and removed.

These scripts are run under a chroot of the customized OS.

Example:

```yaml
SystemConfig:
  PostInstallScripts:
  - Path: scripts/a.sh
```

### FinalizeImageScripts [[Script](#script-type)[]]

Scripts to run against the image just before the image is finalized.

These scripts are run under a chroot of the customized OS.

Example:

```yaml
SystemConfig:
  FinalizeImageScripts:
  - Path: scripts/a.sh
```

### Users [[User](#user-type)]

Used to add and/or update user accounts.

Example:

```yaml
SystemConfig:
  Users:
  - Name: test
```

### Services [[Services](#services-type)]

Options for configuring systemd services.

```yaml
SystemConfig:
  Services:
    Enable:
    - sshd
```

### Modules [[Modules](#modules-type)]

Options for configuration kernel modules.

## User type

Options for configuring a user account.

### Name [string]

Required.

The name of the user.

Example:

```yaml
SystemConfig:
  Users:
  - Name: test
```

### UID [int]

The ID to use for the user.
This value is not used if the user already exists.

Valid range: 0-60000

Example:

```yaml
SystemConfig:
  Users:
  - Name: test
    UID: 1000
```

### PasswordHashed [bool]

Default: `false`.

When set to true, specifies that the password provided by either `Password` or
`PasswordPath` has already been hashed and may be copied directly into the
`/etc/shadow` file.

Example:

```yaml
SystemConfig:
  Users:
  - Name: test
    # Generated by:
    #   PASSWORD="password"
    #   SALT=$(tr -dc "A-Za-z0-9" < /dev/urandom 2> /dev/null | head -c 12)
    #   openssl passwd -6 -salt "$SALT" "$PASSWORD"
    Password: "$6$XH9YwqAMPohT$YQ0fqon.KOXz9AfjP5LE6VHifnNcsIgxmeX/iM5VF1GpFJTOpnTY.UGVRA.Xb8gYdVFqkYnnpJwlaIU1LhNHB/"
    PasswordHashed: true
```

Note: Modern GPUs have gotten incredibly good at brute forcing hashed passwords.
While hashing passwords is still considered best practice, unless the password is
incredibly strong (32+ randomly generated characters), then it is recommended
that you treat a hashed password with the same care as a plain-text password.

### Password [string]

Sets the user's password.

Use of this property is strongly discouraged, except when debugging.

Example:

```yaml
SystemConfig:
  Users:
  - Name: test
    Password: testpassword
```

### PasswordPath [string]

Sets the user's password.
The password is read from the file path specified.

Example:

```yaml
SystemConfig:
  Users:
  - Name: test
    PasswordPath: test-password.txt
```

### PasswordExpiresDays [int]

The number of days until the password expires and the user can no longer login.

Valid range: 0-99999. Set to -1 to remove expiry.

Example:

```yaml
SystemConfig:
  Users:
  - Name: test
    PasswordPath: test-password.txt
    PasswordHashed: true
    PasswordExpiresDays: 120
```

### SSHPubKeyPaths [string[]]

File paths to SSH public key files.
These public keys will be copied into the user's `~/.ssh/authorized_keys` file.

Example:

```yaml
SystemConfig:
  Users:
  - Name: test
    SSHPubKeyPaths:
    - id_ed25519.pub
```

### PrimaryGroup [string]

The primary group of the user.

Example:

```yaml
SystemConfig:
  Users:
  - Name: test
    PrimaryGroup: testgroup
```

### SecondaryGroups [string[]]

Additional groups to assign to the user.

Example:

```yaml
SystemConfig:
  Users:
  - Name: test
    SecondaryGroups:
    - sudo
```

### StartupCommand [string]

The command run when the user logs in.

Example:

```yaml
SystemConfig:
  Users:
  - Name: test
    StartupCommand: /sbin/nologin
```
