# Azure Linux Image Customizer configuration

The Azure Linux Image Customizer is configured using a YAML (or JSON) file.

### Operation ordering

1. If partitions were specified in the config, customize the disk partitions.

2. Override the `/etc/resolv.conf` file with the version from the host OS.

3. Update packages:

   1. Remove packages ([removeLists](#removelists-string),
   [remove](#remove-string))

   2. Update base image packages ([updateExistingPackages](#updateexistingpackages-bool)).

   3. Install packages ([installLists](#installlists-string),
   [install](#install-string))

   4. Update packages ([updateLists](#removelists-string),
   [update](#update-string))

4. Update hostname. ([hostname](#hostname-string))

5. Copy additional files. ([additionalFiles](#additionalfiles-mapstring-fileconfig))
  
5. Copy additional directories. ([additionalDirs](#additionaldirs-dirconfig))

6. Add/update users. ([users](#users-user))

7. Enable/disable services. ([services](#services-type))

8. Configure kernel modules. ([modules](#modules-module))

10. Write the `/etc/mariner-customizer-release` file.

11. If [resetBootLoaderType](#resetbootloadertype-string) is set to `hard-reset`, then
    reset the boot-loader.

    If [resetBootLoaderType](#resetbootloadertype-string) is not set, then
    append the [extraCommandLine](#extracommandline-string) value to the existing
    `grub.cfg` file.

12. Update the SELinux mode.

13. If ([overlays](#overlay-type)) are specified, then add the overlays dracut module
    and update the grub config.

14. If ([verity](#verity-type)) is specified, then add the dm-verity dracut driver
    and update the grub config.

15. Regenerate the initramfs file (if needed).

16. Run ([postCustomization](#postcustomization-script)) scripts.

17. If SELinux is enabled, call `setfiles`.

18. Delete `/etc/resolv.conf` file.

19. Run finalize image scripts. ([finalizeCustomization](#finalizecustomization-script))

20. If [--shrink-filesystems](./cli.md#shrink-filesystems) is specified, then shrink
    the file systems.

21. If ([verity](#verity-type)) is specified, then create the hash tree and update the
    grub config.

22. if the output format is set to `iso`, copy additional iso media files.
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
existing package using [remove](#remove-string) and then install the
new package with [install](#install-string).

Example:

```yaml
os:
  packages:
    remove:
    - kernel

    install:
    - kernel-uvm
```

## Schema Overview

- [Azure Linux Image Customizer configuration](#azure-linux-image-customizer-configuration)
    - [Operation ordering](#operation-ordering)
    - [/etc/resolv.conf](#etcresolvconf)
    - [Replacing packages](#replacing-packages)
  - [Schema Overview](#schema-overview)
  - [Top-level](#top-level)
  - [config type](#config-type)
    - [storage \[storage\]](#storage-storage)
    - [os \[os\]](#os-os)
  - [disk type](#disk-type)
    - [partitionTableType \[string\]](#partitiontabletype-string)
    - [maxSize \[uint64\]](#maxsize-uint64)
    - [partitions \[partition\[\]\]](#partitions-partition)
  - [iso type](#iso-type)
    - [kernelExtraCommandLine \[string\]](#kernelextracommandline-string)
    - [additionalFiles](#additionalfiles)
  - [overlay type](#overlay-type)
  - [verity type](#verity-type)
  - [fileConfig type](#fileconfig-type)
    - [path \[string\]](#path-string)
    - [permissions \[string\]](#permissions-string)
  - [dirConfig type](#dirconfig-type)
    - [sourcePath \[string\]](#sourcepath-string)
    - [destinationPath \[string\]](#destinationpath-string)
    - [newDirPermissions \[int\]](#newdirpermissions-int)
    - [mergedDirPermissions \[int\]](#mergeddirpermissions-int)
    - [childFilePermissions \[int\]](#childfilepermissions-int)
  - [fileSystem type](#filesystem-type)
    - [deviceId \[string\]](#deviceid-string)
    - [type \[string\]](#type-string)
    - [mountPoint \[mountPoint\]](#mountpoint-mountpoint)
  - [kernelCommandLine type](#kernelcommandline-type)
    - [extraCommandLine \[string\]](#extracommandline-string)
    - [selinuxMode](#selinuxmode)
  - [module type](#module-type)
    - [name \[string\]](#name-string)
    - [loadMode \[string\]](#loadmode-string)
    - [options \[map\<string, string\>\]](#options-mapstring-string)
  - [packageList type](#packagelist-type)
    - [packages \[string\[\]\]](#packages-string)
  - [packages type](#packages-type)
    - [updateExistingPackages \[bool\]](#updateexistingpackages-bool)
    - [installLists \[string\[\]\]](#installlists-string)
    - [install \[string\[\]\]](#install-string)
    - [removeLists \[string\[\]\]](#removelists-string)
    - [remove \[string\[\]\]](#remove-string)
    - [updateLists \[string\[\]\]](#updatelists-string)
    - [update \[string\[\]\]](#update-string)
  - [partition type](#partition-type)
    - [id \[string\]](#id-string)
    - [label \[string\]](#label-string)
    - [start \[uint64\]](#start-uint64)
    - [end \[uint64\]](#end-uint64)
    - [size \[uint64\]](#size-uint64)
    - [type \[string\]](#type-string-1)
  - [mountPoint type](#mountpoint-type)
    - [idType \[string\]](#idtype-string)
    - [options \[string\]](#options-string)
    - [path \[string\]](#path-string-1)
  - [script type](#script-type)
    - [path \[string\]](#path-string-2)
    - [args \[string\]](#args-string)
  - [scripts type](#scripts-type)
    - [postCustomization \[script\[\]\]](#postcustomization-script)
    - [finalizeCustomization \[script\[\]\]](#finalizecustomization-script)
  - [services type](#services-type)
    - [enable \[string\[\]\]](#enable-string)
    - [disable \[string\[\]\]](#disable-string)
  - [os type](#os-type)
    - [resetBootLoaderType \[string\]](#resetbootloadertype-string)
    - [hostname \[string\]](#hostname-string)
    - [kernelCommandLine \[kernelCommandLine\]](#kernelcommandline-kernelcommandline)
    - [packages packages](#packages-packages)
    - [additionalFiles \[map\<string, fileConfig\[\]\>\]](#additionalfiles-mapstring-fileconfig)
    - [additionalDirs \[dirConfig\[\]\]](#additionaldirs-dirconfig)
    - [users \[user\]](#users-user)
    - [modules \[module\[\]\]](#modules-module)
    - [services \[services\]](#services-services)
  - [user type](#user-type)
    - [name \[string\]](#name-string-1)
    - [uid \[int\]](#uid-int)
    - [passwordHashed \[bool\]](#passwordhashed-bool)
    - [password \[string\]](#password-string)
    - [passwordPath \[string\]](#passwordpath-string)
    - [PasswordExpiresDays \[int\]](#passwordexpiresdays-int)
    - [sshPublicKeyPaths \[string\[\]\]](#sshpublickeypaths-string)
    - [primaryGroup \[string\]](#primarygroup-string)
    - [secondaryGroups \[string\[\]\]](#secondarygroups-string)
    - [startupCommand \[string\]](#startupcommand-string)
  - [storage type](#storage-type)
    - [bootType \[string\]](#boottype-string)
    - [disks \[disk\[\]\]](#disks-disk)
    - [fileSystems \[fileSystem\[\]\]](#filesystems-filesystem)

## Top-level

The top level type for the YAML file is the [config](#config-type) type.

## config type

The top-level type of the configuration.

### storage [[storage](#storage-type)]

Contains the options for provisioning disks, partitions, and file systems.

While Disks is a list, only 1 disk is supported at the moment.
Support for multiple disks may (or may not) be added in the future.

```yaml
storage:
  bootType: efi

  disks:
  - partitionTableType: gpt
    maxSize: 4096M
    partitions:
    - id: esp
      type: esp
      start: 1M
      end: 9M

    - id: rootfs
      start: 9M
      
  fileSystems:
  - deviceId: esp
    type: fat32
    mountPoint:
      path: /boot/efi
      options: umask=0077

  - deviceId: rootfs
    type: ext4
    mountPoint:
      path: /

os:
  resetBootLoaderType: hard-reset
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

The size of the disk.

Supported format: `<NUM>(K|M|G|T)`: A size in KiB (`K`), MiB (`M`), GiB (`G`), or TiB
(`T`).

Must be a multiple of 1 MiB.

### partitions [[partition](#partition-type)[]]

The partitions to provision on the disk.

## iso type

Specifies the configuration for the generated ISO media.

### kernelExtraCommandLine [string]

- See [extraCommandLine](#extracommandline-string).

### additionalFiles

- See [additionalFiles](#additionalfiles-mapstring-fileconfig).

## overlay type

Specifies the configuration for overlay filesystem.

- `lowerDir`: This directory acts as the read-only layer in the overlay
  filesystem. It contains the base files and directories which will be overlaid
  by the upperDir. Changes to the overlay filesystem do not affect the contents
  of lowerDir.

- `upperDir`: This directory is the writable layer of the overlay filesystem.
  Any modifications, such as file additions, deletions, or changes, are made in
  the upperDir. These changes are what make the overlay filesystem appear
  different from the lowerDir alone.

- `workDir`: This is a required directory used for preparing files before they
  are merged into the upperDir. It needs to be on the same filesystem as the
  upperDir and is used for temporary storage by the overlay filesystem to ensure
  atomic operations. The workDir is not directly accessible to users.

- `partition`: Optional field: If configured, a partition will be attached to
  the current targeted overlay, making it persistent and ensuring that changes
  are retained. If not configured, the overlay will be volatile.

  - `idType`: Specifies the type of id for the partition. The options are
    `part-label` (partition label), `uuid` (filesystem UUID), and `part-uuid`
    (partition UUID).

  - `id`: The unique identifier value of the partition, corresponding to the
    specified IdType.

Example:

```yaml
os:
  overlays:
    - lowerDir: /etc
      upperDir: /upper_etc
      workDir: /work_etc
      partition:
        idType: part-label
        id: partition-etc
    - lowerDir: /var/lib
      upperDir: /upper_var_lib
      workDir: /work_var_lib
    - lowerDir: /var/log
      upperDir: /upper_var_log
      workDir: /work_var_log
```

## verity type

Specifies the configuration for dm-verity root integrity verification. Please
execute `sudo modprobe nbd` before building the image with verity enablement.

Please enable overlays for the `/var/lib` and `/var/log` directories, along with
verity enablement, to ensure proper functioning of services. For an example,
please refer to the [overlay type](#overlay-type) section.

- `dataPartition`: A partition configured with dm-verity, which verifies integrity
  at each system boot.

  - `idType`: Specifies the type of id for the partition. The options are
    `part-label` (partition label), `uuid` (filesystem UUID), and `part-uuid`
    (partition UUID).

  - `id`: The unique identifier value of the partition, corresponding to the
    specified IdType.

- `hashPartition`: A partition used exclusively for storing a calculated hash
  tree.

- `corruptionOption`: Optional. Specifies the behavior in case of detected
  corruption. This is configurable with the following options:
  - `io-error`: Default setting. Fails the I/O operation with an I/O error.
  - `ignore`: ignores the corruption and continues operation.
  - `panic`: causes the system to panic (print errors) and then try restarting
    if corruption is detected.
  - `restart`: attempts to restart the system upon detecting corruption.

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
    corruptionOption: panic
```

## fileConfig type

Specifies options for placing a file in the OS.

Type is used by: [additionalFiles](#additionalfiles-mapstring-fileconfig)

<div id="fileconfig-path"></div>

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

## dirConfig type

Specifies options for placing a directory in the OS.

Type is used by: [additionalDirs](#additionaldirs-dirconfig)

<div id="dirconfig-path"></div>

### sourcePath [string]

The absolute path to the source directory that will be copied.

### destinationPath [string]

The absolute path in the target OS that the source directory will be copied to.

Example:

```yaml
os:
  additionalDirs:
    - sourcePath: "home/files/targetDir"
      destinationPath: "usr/project/targetDir"
```

### newDirPermissions [int]

The permissions to set on all of the new directories being created on the target OS (including the top-level directory). **Note:** If this value is not specified in the config, the permissions for these directories will be set to `0755`.

### mergedDirPermissions [int]

The permissions to set on the directories being copied that already do exist on the target OS (including the top-level directory). **Note:** If this value is not specified in the config, the permissions for this field will be the same as that of the pre-existing directory.

### childFilePermissions [int]

The permissions to set on the children file of the directory. **Note:** If this value is not specified in the config, the permissions for these directories will be set to `0755`.

Supported formats for permission values:

- Int containing an octal value. e.g. `664`

Example:

```yaml
os:
  additionalFiles:
    - sourcePath: "home/files/targetDir"
      destinationPath: "usr/project/targetDir"
      newDirPermissions: 0644
      mergedDirPermissions: 0777
      childFilePermissions: 0644
```

## fileSystem type

Specifies the mount options for a partition.

### deviceId [string]

Required.

The ID of the partition.
This is used correlate [partition](#partition-type) objects with fileSystem objects.

### type [string]

Required.

The filesystem type of the partition.

Supported options:

- `ext4`
- `fat32`
- `xfs`

### mountPoint [[mountPoint](#mountpoint-type)]

Optional settings for where and how to mount the filesystem.

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

### name [string]

Name of the module.

```yaml
os:
  modules:
  - name: br_netfilter
```

### loadMode [string]

The loadMode setting for kernel modules dictates how and when these modules 
are loaded or disabled in the system.

Supported loadmodes:

- `always`: Set kernel modules to be loaded automatically at boot time.
  - If the module is blacklisted in the base image, remove the blacklist entry.
  - Add the module to `/etc/modules-load.d/modules-load.conf`.
  - Write the options, if provided.

- `auto`: Used for modules that are automatically loaded by the kernel as needed,
    without explicit configuration to load them at boot.
  - If the module is disabled in the base image, remove the blacklist entry to
    allow it to be loaded automatically.
  - Write the provided options to `/etc/modprobe.d/module-options.conf`, but do not
    add the module to `/etc/modules-load.d/modules-load.conf`, as it should be loaded automatically by
    the kernel when necessary.

- `disable`: Configures kernel modules to be explicitly disabled, preventing them from
  loading automatically.
  - If the module is not already disabled in the base image, a blacklist entry will
    be added to `/etc/modprobe.d/blacklist.conf` to ensure the module is disabled.

- `inherit`: Configures kernel modules to inherit the loading behavior set in the base
  image. Only applying new options where they are explicitly provided and applicable.
  - If the module is not disabled, and options are provided, these options will be
    written to `/etc/modprobe.d/module-options.conf`.

-  empty string or not set, it will default to `inherit`.


### options [map\<string, string>]

Kernel options for modules can specify how these modules interact with the system, 
and adjust performance or security settings specific to each module.

```yaml
os:
  modules:
  - name: vfio
    loadMode: always
    options:
      enable_unsafe_noiommu_mode: Y
      disable_vga: Y
```

## packageList type

Used to split off lists of packages into a separate file.
This is useful for sharing list of packages between different configuration files.

This type is used by:

- [installLists](#installlists-string)
- [removeLists](#removelists-string)
- [updateLists](#updatelists-string)

### packages [string[]]

Specifies a list of packages.

Example:

```yaml
packages:
- openssh-server
```

## packages type

### updateExistingPackages [bool]

Updates the packages that exist in the base image.

Implemented by calling: `tdnf update`

Example:

```yaml
os:
  packages:
    updateExistingPackages: true
```

### installLists [string[]]

Same as [install](#install-string) but the packages are specified in a
separate YAML (or JSON) file.

The other YAML file schema is specified by [packageList](#packagelist-type).

Example:

```yaml
os:
  packages:
    installLists:
    - lists/ssh.yaml
```

### install [string[]]

Installs packages onto the image.

Implemented by calling: `tdnf install`.

Example:

```yaml
os:
  packages:
    install:
    - openssh-server
```

### removeLists [string[]]

Same as [remove](#remove-string) but the packages are specified in a
separate YAML (or JSON) file.

The other YAML file schema is specified by [packageList](#packagelist-type).

Example:

```yaml
os:
  packages:
    removeLists:
    - lists/ssh.yaml
```

### remove [string[]]

Removes packages from the image.

Implemented by calling: `tdnf remove`

Example:

```yaml
os:
  packages:
    remove:
    - openssh-server
```

### updateLists [string[]]

Same as [update](#update-string) but the packages are specified in a
separate YAML (or JSON) file.

The other YAML file schema is specified by [packageList](#packagelist-type).

Example:

```yaml
os:
  packages:
    updateLists:
    - lists/ssh.yaml
```

### update [string[]]

Updates packages on the system.

Implemented by calling: `tdnf update`

Example:

```yaml
os:
  packages:
    update:
    - openssh-server
```

## partition type

### id [string]

Required.

The ID of the partition.
This is used to correlate Partition objects with [fileSystem](#filesystem-type)
objects.

### label [string]

The label to assign to the partition.

### start [uint64]

Required.

The start location (inclusive) of the partition.

Supported format: `<NUM>(K|M|G|T)`: A size in KiB (`K`), MiB (`M`), GiB (`G`), or TiB
(`T`).

Must be a multiple of 1 MiB.

### end [uint64]

The end location (exclusive) of the partition.

The `end` and `size` fields cannot be specified at the same time.

Either the `size` or `end` field is required for all partitions except for the last
partition.
When both the `size` and `end` fields are omitted or when the `size` field is set to the
value `grow`, the last partition will fill the remainder of the disk based on the disk's
[maxSize](#maxsize-uint64) field.

Supported format: `<NUM>(K|M|G|T)`: A size in KiB (`K`), MiB (`M`), GiB (`G`), or TiB
(`T`).

Must be a multiple of 1 MiB.

### size [uint64]

The size of the partition.

Supported formats:

- `<NUM>(K|M|G|T)`: An explicit size in KiB (`K`), MiB (`M`), GiB (`G`), or TiB (`T`).

- `grow`: Fill up the remainder of the disk. Must be the last partition.

Must be a multiple of 1 MiB.

<div id="partition-type-string"></div>

### type [string]

Specifies options for the partition.

Supported options:

- `esp`: The UEFI System Partition (ESP).
  The partition must have a `fileSystemType` of `fat32`.

- `bios-grub`: Specifies this partition is the BIOS boot partition.
  This is required for GPT disks that wish to be bootable using legacy BIOS mode.

  This partition must start at block 1.

  This flag is only supported on GPT formatted disks.

  For further details, see: https://en.wikipedia.org/wiki/BIOS_boot_partition

## mountPoint type

### idType [string]

Default: `part-uuid`

The partition ID type that should be used to recognize the partition on the disk.

Supported options:

- `uuid`: The filesystem's partition UUID.

- `part-uuid`: The partition UUID specified in the partition table.

- `part-label`: The partition label specified in the partition table.

### options [string]

The additional options used when mounting the file system.

These options are in the same format as [mount](https://linux.die.net/man/8/mount)'s
`-o` option (or the `fs_mntops` field of the
[fstab](https://man7.org/linux/man-pages/man5/fstab.5.html) file).

<div id="mountpoint-path"></div>

### path [string]

Required.

The absolute path of where the partition should be mounted.

The mounts will be sorted to ensure that parent directories are mounted before child
directories.
For example, `/boot` will be mounted before `/boot/efi`.

## script type

Points to a script file (typically a Bash script) to be run during customization.

<div id="script-path"></div>

### path [string]

The path of the script.

This must be in the same directory or a sub-directory that the config file is located
in.

Example:

```yaml
scripts:
  postCustomization:
  - path: scripts/a.sh
```

### args [string]

Additional arguments to pass to the script.

Example:

```yaml
scripts:
  postCustomization:
  - path: scripts/a.sh
    args: abc
```

## scripts type

Note: Script files must be in the same directory or a child directory of the directory
that contains the config file.

### postCustomization [[script](#script-type)[]]

Scripts to run after all the in-built customization steps have run.

These scripts are run under a chroot of the customized OS.

Example:

```yaml
scripts:
  postCustomization:
  - path: scripts/a.sh
```

### finalizeCustomization [[script](#script-type)[]]

Scripts to run at the end of the customization process.

In particular, these scripts run after:

1. The `setfiles` command has been called to update/fix the SELinux files labels (if
   SELinux is enabled), and

2. The temporary `/etc/resolv.conf` file has been deleted,

but before the conversion to the requested output type.
(See, [Operation ordering](#operation-ordering) for details.)

Most scripts should be added to [postCustomization](#postcustomization-script).
Only add scripts to [finalizeCustomization](#finalizecustomization-script) if you want
to customize the `/etc/resolv.conf` file or you want manually set SELinux file labels.

These scripts are run under a chroot of the customized OS.

Example:

```yaml
os:
  finalizeCustomization:
  - path: scripts/b.sh
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

### packages [packages](#packages-type)

Remove, update, and install packages on the system.

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

### additionalDirs [[dirConfig](#dirconfig-type)[]]

Copy directories into the OS image.

This property is a list of [dirConfig](#dirconfig-type) objects.

Example:

```yaml
os:
  additionalDirs:
    # Copying directory with default permission options.
    - sourcePath: "path/to/local/directory/"
      destinationPath: "/path/to/destination/directory/"
    # Copying directory with specific permission options.
    - sourcePath: "path/to/local/directory/"
      destinationPath: "/path/to/destination/directory/"
      newDirPermissions: 0644
      mergedDirPermissions: 0777
      childFilePermissions: 0644
```

### users [[user](#user-type)]

Used to add and/or update user accounts.

Example:

```yaml
os:
  users:
  - name: test
```

### modules [[module](#module-type)[]]

Used to configure kernel modules.

Example:

```yaml
os:
  modules:
    - name: vfio
```

### services [[services](#services-type)]

Options for configuring systemd services.

```yaml
os:
  services:
    enable:
    - sshd
```

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

## storage type

### bootType [string]

Specifies the boot system that the image supports.

Supported options:

- `legacy`: Support booting from BIOS firmware.

  When this option is specified, the partition layout must contain a partition with the
  `bios-grub` flag.

- `efi`: Support booting from UEFI firmware.

  When this option is specified, the partition layout must contain a partition with the
  `esp` flag.

### disks [[disk](#disk-type)[]]

Contains the options for provisioning disks and their partitions.

### fileSystems [[fileSystem](#filesystem-type)[]]

Specifies the mount options of the partitions.
