# Azure Linux Image Customizer configuration

The Azure Linux Image Customizer is configured using a YAML (or JSON) file.

### Operation ordering

1. If partitions were specified in the config, customize the disk partitions.

2. Override the `/etc/resolv.conf` file with the version from the host OS.

3. Update packages:

   1. Remove packages ([packageListsRemove](#packagelistsremove-string),
   [packagesRemove](#packagesremove-string))

   2. Update base image packages ([updateBaseImagePackages](#updatebaseimagepackages-bool)).

   3. Install packages ([packageListsInstall](#packagelistsinstall-string),
   [packagesInstall](#packagesinstall-string))

   4. Update packages ([packageListsUpdate](#packagelistsupdate-string),
   [packagesUpdate](#packagesupdate-string))

4. Update hostname. ([hostname](#hostname-string))

5. Copy additional files. ([additionalFiles](#additionalfiles-mapstring-fileconfig))

6. Add/update users. ([users](#users-user))

7. Enable/disable services. ([services](#services-type))

8. Configure kernel modules. ([modules](#modules-type))

9. Write the `/etc/mariner-customizer-release` file.

10. Run post-install scripts. ([postInstallScripts](#postinstallscripts-script))

11. If [resetBootLoaderType](#resetbootloadertype-string) is set to `hard-reset`, then
    reset the boot-loader.

    If [resetBootLoaderType](#resetbootloadertype-string) is not set, then
    append the [extraCommandLine](#extracommandline-string) value to the existing
    `grub.cfg` file.

12. Change SELinux mode and, if SELinux is enabled, call `setfiles`.

13. Run finalize image scripts. ([finalizeImageScripts](#finalizeimagescripts-script))

14. Delete `/etc/resolv.conf` file.

15. Enable dm-verity root protection.

16. if the output format is set to `iso`, copy additional iso media files.
([iso](#iso-type))

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
existing package using [packagesRemove](#packagesremove-string) and then install the
new package with [packagesInstall](#packagesinstall-string).

Example:

```yaml
os:
  packagesRemove:
  - kernel

  packagesInstall:
  - kernel-uvm
```

## Schema Overview

- [config type](#config-type)
  - [disks](#disks-disk)
    - [disk type](#disk-type)
      - [partitionTableType](#partitiontabletype-string)
      - [maxSize](#maxsize-uint64)
      - [partitions](#partitions-partition)
        - [partition type](#partition-type)
          - [id](#id-string)
          - [fileSystemType](#filesystemtype-string)
          - [label](#partition-label)
          - [start](#start-uint64)
          - [end](#end-uint64)
          - [size](#size-uint64)
          - [flag](#flags-string)
  - [iso](#iso-type)
    - [additionalFiles](#additionalfiles-mapstring-fileconfig)
      - [fileConfig type](#fileconfig-type)
        - [path](#path-string)
        - [permissions](#permissions-string)
  - [os type](#os-type)
    - [bootType](#boottype-string)
    - [resetBootLoaderType](#resetbootloadertype-string)
    - [hostname](#hostname-string)
    - [kernelCommandLine](#kernelcommandline-type)
      - [extraCommandLine](#extracommandline-string)
    - [updateBaseImagePackages](#updatebaseimagepackages-bool)
    - [packageListsInstall](#packagelistsinstall-string)
      - [packageList type](#packagelist-type)
        - [packages](#packages-string)
    - [packagesInstall](#packagesinstall-string)
    - [packageListsRemove](#packagelistsremove-string)
      - [packageList type](#packagelist-type)
        - [packages](#packages-string)
    - [packagesRemove](#packagesremove-string)
    - [packageListsUpdate](#packagelistsupdate-string)
    - [packagesUpdate](#packagesupdate-string)
    - [additionalFiles](#additionalfiles-mapstring-fileconfig)
      - [fileConfig type](#fileconfig-type)
        - [path](#path-string)
        - [permissions](#permissions-string)
    - [partitionSettings](#partitionsettings-partitionsetting)
      - [partitionSetting type](#partitionsetting-type)
        - [id](#id-string)
        - [mountIdentifierType](#mountidentifiertype-string)
        - [mountOptions](#mountoptions-string)
        - [mountPoint](#mountpoint-string)
    - [postInstallScripts](#postinstallscripts-script)
      - [script type](#script-type)
        - [path](#path-string)
        - [args](#args-string)
    - [finalizeImageScripts](#finalizeimagescripts-script)
      - [script type](#script-type)
        - [path](#path-string)
        - [args](#args-string)
    - [users](#users-user)
      - [user type](#user-type)
        - [name](#user-name)
        - [uid](#uid-int)
        - [passwordHashed](#passwordhashed-bool)
        - [password](#password-string)
        - [passwordPath](#passwordpath-string)
        - [passwordExpiresDays](#passwordexpiresdays-int)
        - [sshPublicKeyPaths](#sshpublickeypaths-string)
        - [primaryGroup](#primarygroup-string)
        - [secondaryGroups](#secondarygroups-string)
        - [startupCommand](#startupcommand-string)
    - [services](#services-type)
      - [enable](#enable-string)
      - [disable](#disable-string)
    - [modules](#modules-type)
      - [load](#load-module)
        - [module type](#module-type)
          - [name](#module-name)
      - [disable](#disable-module)
        - [module type](#module-type)
          - [name](#module-name)
    - [verity type](#verity-type)

## Top-level

The top level type for the YAML file is the [config](#config-type) type.

## config type

The top-level type of the configuration.

### disks [[disk](#disk-type)[]]

Contains the options for provisioning disks and their partitions.

If the Disks field isn't specified, then the partitions of the base image aren't
changed.

If Disks is specified, then both [os.bootType](#boottype-string) and
[os.resetBootLoaderType](#resetbootloadertype-string) must also be
specified.

While Disks is a list, only 1 disk is supported at the moment.
Support for multiple disks may (or may not) be added in the future.

```yaml
disks:
- partitionTableType: gpt
  maxSize: 4096
  partitions:
  - id: esp
    flags:
    - esp
    - boot
    start: 1
    end: 9
    fileSystemType: fat32

  - id: rootfs
    start: 9
    fileSystemType: ext4

os:
  bootType: efi
  resetBootLoaderType: hard-reset
  partitionSettings:
  - id: esp
    mountPoint: /boot/efi
    mountOptions: umask=0077

  - id: rootfs
    mountPoint: /
```

### os [[os](#os-type)]

Contains the configuration options for the OS.

Example:

```yaml
os:
  hostname: example-image
```

## disk type

Specifies the properties of a disk, including its partitions.

### partitionTableType [string]

Specifies how the partition tables are laid out.

Supported options:

- `gpt`: Use the GUID Partition Table (GPT) format.

### maxSize [uint64]

The size of the disk, specified in mebibytes (MiB).

### partitions [[partition](#partition-type)[]]

The partitions to provision on the disk.

## iso type

Specifies the configuration for the generated ISO media.

### kernelExtraCommandLine [string]

- See [extraCommandLine](#extracommandline-string).

### additionalFiles

- See [additionalFiles](#additionalfiles-mapstring-fileconfig).

## verity type

Specifies the configuration for dm-verity root integrity verification.

- `dataPartition`: A partition configured with dm-verity, which verifies integrity
  at each system boot.

  - `idType`: Specifies the type of id for the partition. The options are
    `part-label` (partition label), `uuid` (filesystem UUID), and `part-uuid`
    (partition UUID).

  - `id`: The unique identifier value of the partition, corresponding to the
    specified IdType.

- `hashPartition`: A partition used exclusively for storing a calculated hash
  tree.

Example:

```yaml
os:
  verity:
    dataPartition:
      idType: part-uuid
      id: 00000000-0000-0000-0000-000000000000
    hashPartition:
      idType: part-label
      Id: hash_partition
```

## fileConfig type

Specifies options for placing a file in the OS.

Type is used by: [additionalFiles](#additionalfiles-mapstring-fileconfig)

### path [string]

The absolute path of the destination file.

Example:

```yaml
os:
  additionalFiles:
    files/a.txt:
    - path: /a.txt
```

### permissions [string]

The permissions to set on the destination file.

Supported formats:

- String containing an octal string. e.g. `"664"`

Example:

```yaml
os:
  additionalFiles:
    files/a.txt:
    - path: /a.txt
      permissions: "664"
```

## kernelCommandLine type

Options for configuring the kernel.

### extraCommandLine [string]

Additional Linux kernel command line options to add to the image.

If [resetBootLoaderType](#resetbootloadertype-string) is set to `"hard-reset"`, then the
`extraCommandLine` value will be appended to the new `grub.cfg` file.

If [resetBootLoaderType](#resetbootloadertype-string) is not set, then the
`extraCommandLine` value will be appended to the existing `grub.cfg` file.

### selinuxMode

Specifies the mode to set SELinux to.

If this field is not specified, then the existing SELinux mode in the base image is
maintained.
Otherwise, the image is modified to match the requested SELinux mode.

The Azure Linux Image Customizer tool can enable SELinux on a base image with SELinux
disabled and it can disable SELinux on a base image that has SELinux enabled.
However, using a base image that already has the required SELinux mode will speed-up the
customization process.

If SELinux is enabled, then all the file-systems that support SELinux will have their
file labels updated/reset (using the `setfiles` command).

Supported options:

- `disabled`: Disables SELinux.

- `permissive`: Enables SELinux but only logs access rule violations.

- `enforcing`: Enables SELinux and enforces all the access rules.

- `force-enforcing`: Enables SELinux and sets it to enforcing in the kernel
  command-line.
  This means that SELinux can't be set to `permissive` using the `/etc/selinux/config`
  file.

Note: For images with SELinux enabled, the `selinux-policy` package must be installed.
This package contains the default SELinux rules and is required for SELinux-enabled
images to be functional.
The Azure Linux Image Customizer tool will report an error if the package is missing from
the image.

Note: If you wish to apply additional SELinux policies on top of the base SELinux
policy, then it is recommended to apply these new policies using
([postInstallScripts](#postinstallscripts-script)).
After applying the policies, you do not need to call `setfiles` manually since it will
called automatically after the `postInstallScripts` are run.

Example:

```yaml
os:
  kernelCommandLine:
    selinuxMode: enforcing

  packagesInstall:
  # Required packages for SELinux.
  - selinux-policy
  - selinux-policy-modules
  
  # Optional packages that contain useful SELinux utilities.
  - setools-console
  - policycoreutils-python-utils
```

## module type

Options for configuring a kernel module.

<div id="module-name"></div>

### name

Name of the module.

```yaml
os:
  modules:
    load:
    - name: br_netfilter
```

## modules type

Options for configuring kernel modules.

### load [[module](#module-type)[]]

Sets kernel modules to be loaded automatically on boot.

Implemented by adding an entry to `/etc/modules-load.d/`.

```yaml
OS:
  Modules:
    Load:
    - Name: br_netfilter
```

### disable [[module](#module-type)[]]

Disable kernel modules from being loaded.

Implemented by adding a "blacklist" entry to `/etc/modprobe.d/`.

```yaml
os:
  modules:
    disable:
    - name: mousedev
```

## packageList type

Used to split off lists of packages into a separate file.
This is useful for sharing list of packages between different configuration files.

This type is used by:

- [packageListsInstall](#packagelistsinstall-string)
- [packageListsRemove](#packagelistsremove-string)
- [packageListsUpdate](#packagelistsupdate-string)

### packages [string[]]

Specifies a list of packages.

Example:

```yaml
packages:
- openssh-server
```

## partition type

### id [string]

Required.

The ID of the partition.
This is used to correlate Partition objects with [partitionSetting](#partitionsetting-type)
objects.

### fileSystemType [string]

Required.

The filesystem type of the partition.

Supported options:

- `ext4`
- `fat32`
- `xfs`

<div id="partition-label"></div>

### label [string]

The label to assign to the partition.

### start [uint64]

Required.

The start location (inclusive) of the partition, specified in MiBs.

### end [uint64]

The end location (exclusive) of the partition, specified in MiBs.

The End and Size fields cannot be specified at the same time.

Either the Size or End field is required for all partitions except for the last
partition.
When both the Size and End fields are omitted, the last partition will fill the
remainder of the disk (based on the disk's [maxSize](#maxsize-uint64) field).

### size [uint64]

The size of the partition, specified in MiBs.

### flags [string[]]

Specifies options for the partition.

Supported options:

- `esp`: The UEFI System Partition (ESP).
  The partition must have a `fileSystemType` of `fat32`.

  When specified on a GPT formatted disk, the `boot` flag must also be added.

- `bios-grub`: Specifies this partition is the BIOS boot partition.
  This is required for GPT disks that wish to be bootable using legacy BIOS mode.

  This partition must start at block 1.

  This flag is only supported on GPT formatted disks.

  For further details, see: https://en.wikipedia.org/wiki/BIOS_boot_partition

- `boot`: Specifies that this partition contains the boot loader.

  When specified on a GPT formatted disk, the `esp` flag must also be added.

These options mirror those in
[parted](https://www.gnu.org/software/parted/manual/html_node/set.html).

## partitionSetting type

Specifies the mount options for a partition.

### id [string]

Required.

The ID of the partition.
This is used correlate [partition](#partition-type) objects with PartitionSetting
objects.

### mountIdentifierType [string]

Default: `part-uuid`

The partition ID type that should be used to recognize the partition on the disk.

Supported options:

- `uuid`: The filesystem's partition UUID.

- `part-uuid`: The partition UUID specified in the partition table.

- `part-label`: The partition label specified in the partition table.

### mountOptions [string]

The additional options used when mounting the file system.

These options are in the same format as [mount](https://linux.die.net/man/8/mount)'s
`-o` option (or the `fs_mntops` field of the
[fstab](https://man7.org/linux/man-pages/man5/fstab.5.html) file).

### mountPoint [string]

Required.

The absolute path of where the partition should be mounted.

The mounts will be sorted to ensure that parent directories are mounted before child
directories.
For example, `/boot` will be mounted before `/boot/efi`.

## script type

Points to a script file (typically a Bash script) to be run during customization.

### path [string]

The path of the script.

This must be in the same directory or a sub-directory that the config file is located
in.

Example:

```yaml
os:
  postInstallScripts:
  - path: scripts/a.sh
```

### args [string]

Additional arguments to pass to the script.

Example:

```yaml
os:
  postInstallScripts:
  - path: scripts/a.sh
    args: abc
```

## services type

Options for configuring systemd services.

### enable [string[]]

A list of services to enable.
That is, services that will be set to automatically run on OS boot.

Example:

```yaml
os:
  services:
    enable:
    - sshd
```

### disable [string[]]

A list of services to disable.
That is, services that will be set to not automatically run on OS boot.

Example:

```yaml
os:
  services:
    disable:
    - sshd
```

## os type

Contains the configuration options for the OS.

### bootType [string]

Specifies the boot system that the image supports.

Supported options:

- `legacy`: Support booting from BIOS firmware.

  When this option is specified, the partition layout must contain a partition with the
  `bios-grub` flag.

- `efi`: Support booting from UEFI firmware.

  When this option is specified, the partition layout must contain a partition with the
  `esp` flag.

### resetBootLoaderType [string]

Specifies that the boot-loader configuration should be reset and how it should be reset.

Supported options:

- `hard-reset`: Fully reset the boot-loader and its configuration.
  This includes removing any customized kernel command-line arguments that were added to
  base image.

This field can only be specified if [Disks](#disks-disk) is also specified.

### hostname [string]

Specifies the hostname for the OS.

Implemented by writing to the `/etc/hostname` file.

Example:

```yaml
os:
  hostname: example-image
```

### kernelCommandLine [[kernelCommandLine](#kernelcommandline-type)]

Specifies extra kernel command line options, as well as other configuration values
relating to the kernel.

### updateBaseImagePackages [bool]

Updates the packages that exist in the base image.

Implemented by calling: `tdnf update`

Example:

```yaml
os:
  updateBaseImagePackages: true
```

### packageListsInstall [string[]]

Same as [packagesInstall](#packagesinstall-string) but the packages are specified in a
separate YAML (or JSON) file.

The other YAML file schema is specified by [packageList](#packagelist-type).

Example:

```yaml
os:
  packageListsRemove:
  - lists/ssh.yaml
```

### packagesInstall [string[]]

Installs packages onto the image.

Implemented by calling: `tdnf install`.

Example:

```yaml
os:
  packagesInstall:
  - openssh-server
```

### packageListsRemove [string[]]

Same as [packagesRemove](#packagesremove-string) but the packages are specified in a
separate YAML (or JSON) file.

The other YAML file schema is specified by [packageList](#packagelist-type).

Example:

```yaml
os:
  packageListsRemove:
  - lists/ssh.yaml
```

### packagesRemove [string[]]

Removes packages from the image.

Implemented by calling: `tdnf remove`

Example:

```yaml
os:
  packagesRemove:
  - openssh-server
```

### packageListsUpdate [string[]]

Same as [packagesUpdate](#packagesupdate-string) but the packages are specified in a
separate YAML (or JSON) file.

The other YAML file schema is specified by [packageList](#packagelist-type).

Example:

```yaml
os:
  packageListsUpdate:
  - lists/ssh.yaml
```

### packagesUpdate [string[]]

Updates packages on the system.

Implemented by calling: `tdnf update`

Example:

```yaml
os:
  packagesUpdate:
  - openssh-server
```

### additionalFiles [map\<string, [fileConfig](#fileconfig-type)[]>]

Copy files into the OS image.

This property is a dictionary of source file paths to destination files.

The destination files value can be one of:

- The absolute path of a destination file.
- A [fileConfig](#fileconfig-type) object.
- A list containing a mixture of paths and [fileConfig](#fileconfig-type) objects.

Example:

```yaml
os:
  additionalFiles:
    # Single destination.
    files/a.txt: /a.txt

    # Single destinations with options.
    files/b.txt:
      path: /b.txt
      permissions: "664"

    # Multiple destinations.
    files/c.txt:
    - /c1.txt
    - path: /c2.txt
      permissions: "664"
```

### partitionSettings [[partitionSetting](#partitionsetting-type)[]]

Specifies the mount options of the partitions.

### postInstallScripts [[script](#script-type)[]]

Scripts to run against the image after the packages have been added and removed.

These scripts are run under a chroot of the customized OS.

Note: Scripts must be in the same directory or a child directory of the directory
that contains the config file.

Example:

```yaml
os:
  postInstallScripts:
  - path: scripts/a.sh
```

### finalizeImageScripts [[script](#script-type)[]]

Scripts to run against the image just before the image is finalized.

These scripts are run under a chroot of the customized OS.

Note: Scripts must be in the same directory or a child directory of the directory
that contains the config file.

Example:

```yaml
os:
  finalizeImageScripts:
  - path: scripts/a.sh
```

### users [[user](#user-type)]

Used to add and/or update user accounts.

Example:

```yaml
os:
  users:
  - name: test
```

### services [[services](#services-type)]

Options for configuring systemd services.

```yaml
os:
  services:
    enable:
    - sshd
```

### modules [[modules](#modules-type)]

Options for configuration kernel modules.

## user type

Options for configuring a user account.

<div id="user-name"></div>

### name [string]

Required.

The name of the user.

Example:

```yaml
os:
  users:
  - name: test
```

### uid [int]

The ID to use for the user.
This value is not used if the user already exists.

Valid range: 0-60000

Example:

```yaml
os:
  users:
  - name: test
    uid: 1000
```

### passwordHashed [bool]

Default: `false`.

When set to true, specifies that the password provided by either `password` or
`passwordPath` has already been hashed and may be copied directly into the
`/etc/shadow` file.

Example:

```yaml
os:
  users:
  - name: test
    # Generated by:
    #   PASSWORD="password"
    #   SALT=$(tr -dc "A-Za-z0-9" < /dev/urandom 2> /dev/null | head -c 12)
    #   openssl passwd -6 -salt "$SALT" "$PASSWORD"
    password: "$6$XH9YwqAMPohT$YQ0fqon.KOXz9AfjP5LE6VHifnNcsIgxmeX/iM5VF1GpFJTOpnTY.UGVRA.Xb8gYdVFqkYnnpJwlaIU1LhNHB/"
    passwordHashed: true
```

Note: Modern GPUs have gotten incredibly good at brute forcing hashed passwords.
While hashing passwords is still considered best practice, unless the password is
incredibly strong (32+ randomly generated characters), then it is recommended
that you treat a hashed password with the same care as a plain-text password.

### password [string]

Sets the user's password.

Use of this property is strongly discouraged, except when debugging.

Example:

```yaml
os:
  users:
  - name: test
    password: testpassword
```

### passwordPath [string]

Sets the user's password.
The password is read from the file path specified.

Example:

```yaml
os:
  users:
  - name: test
    passwordPath: test-password.txt
```

### PasswordExpiresDays [int]

The number of days until the password expires and the user can no longer login.

Valid range: 0-99999. Set to -1 to remove expiry.

Example:

```yaml
os:
  users:
  - name: test
    passwordPath: test-password.txt
    passwordHashed: true
    passwordExpiresDays: 120
```

### sshPublicKeyPaths [string[]]

File paths to SSH public key files.
These public keys will be copied into the user's `~/.ssh/authorized_keys` file.

Example:

```yaml
os:
  users:
  - name: test
    sshPublicKeyPaths:
    - id_ed25519.pub
```

### primaryGroup [string]

The primary group of the user.

Example:

```yaml
os:
  users:
  - name: test
    primaryGroup: testgroup
```

### secondaryGroups [string[]]

Additional groups to assign to the user.

Example:

```yaml
os:
  users:
  - name: test
    secondaryGroups:
    - sudo
```

### startupCommand [string]

The command run when the user logs in.

Example:

```yaml
os:
  users:
  - name: test
    startupCommand: /sbin/nologin
```
