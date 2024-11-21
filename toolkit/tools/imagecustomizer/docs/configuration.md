# Azure Linux Image Customizer configuration

The Azure Linux Image Customizer is configured using a YAML (or JSON) file.

### Operation ordering

1. If partitions were specified in the config, customize the disk partitions.

   Otherwise, if the [resetpartitionsuuidstype](#resetpartitionsuuidstype-string) value
   is specified, then the partitions' UUIDs are changed.

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

5. Copy additional files. ([additionalFiles](#os-additionalfiles))
  
6. Copy additional directories. ([additionalDirs](#additionaldirs-dirconfig))

7. Add/update users. ([users](#users-user))

8. Enable/disable services. ([services](#services-type))

9. Configure kernel modules. ([modules](#modules-module))

10. Write the `/etc/image-customizer-release` file.

11. If [resetBootLoaderType](#resetbootloadertype-string) is set to `hard-reset`, then
    reset the boot-loader.

    If [resetBootLoaderType](#resetbootloadertype-string) is not set, then
    append the [extraCommandLine](#extracommandline-string) value to the existing
    `grub.cfg` file.

12. Update the SELinux mode. [mode](#mode-string)

13. If ([overlays](#overlay-type)) are specified, then add the overlay driver
    and update the fstab file with the overlay mount information.

14. If a ([verity](#verity-type)) device is specified, then add the dm-verity dracut
    driver and update the grub config.

15. Regenerate the initramfs file (if needed).

16. Run ([postCustomization](#postcustomization-script)) scripts.

17. Restore the `/etc/resolv.conf` file.

18. If SELinux is enabled, call `setfiles`.

19. Run finalize image scripts. ([finalizeCustomization](#finalizecustomization-script))

20. If [--shrink-filesystems](./cli.md#shrink-filesystems) is specified, then shrink
    the file systems.

21. If a ([verity](#verity-type)) device is specified, then create the hash tree and
    update the grub config.

22. If the output format is set to `iso`, copy additional iso media files.
    ([iso](#iso-type))

23. If [--output-pxe-artifacts-dir](./cli.md#output-pxe-artifacts-dir) is specified,
    then export the ISO image contents to the specified folder.

### /etc/resolv.conf

The `/etc/resolv.conf` file is overridden during customization so that the package
installation and customization scripts can have access to the network.

Near the end of customization, the `/etc/resolv.conf` file is restored to its original
state.

However, if the `/etc/resolv.conf` did not exist in the base image and
`systemd-resolved` service is enabled, then the `/etc/resolv.conf` file is symlinked to
the `/run/systemd/resolve/stub-resolv.conf` file. (This would happen anyway during
first-boot. But doing this during customization is useful for verity enabled images
where the filesystem is readonly.)

If you want to explicitly set the `/etc/resolv.conf` file contents, you can do so within
a [finalizeCustomization](#finalizecustomization-script) script, since those scripts run
after the `/etc/resolv.conf` is deleted.

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

- [config type](#config-type)
  - [storage](#storage-storage)
    - [bootType](#boottype-string)
    - [disks](#disks-disk)
      - [disk type](#disk-type)
        - [partitionTableType](#partitiontabletype-string)
        - [maxSize](#maxsize-uint64)
        - [partitions](#partitions-partition)
          - [partition type](#partition-type)
            - [id](#id-string)
            - [label](#label-string)
            - [start](#start-uint64)
            - [end](#end-uint64)
            - [size](#size-uint64)
            - [type](#partition-type-string)
    - [verity](#verity-verity)
      - [verity type](#verity-type)
        - [id](#verity-id)
        - [name](#verity-name)
        - [dataDeviceId](#datadeviceid-string)
        - [hashDeviceId](#hashdeviceid-string)
        - [corruptionOption](#corruptionoption-string)
    - [filesystems](#filesystems-filesystem)
      - [filesystem type](#filesystem-type)
        - [deviceId](#deviceid-string)
        - [type](#type-string)
        - [mountPoint](#mountpoint-mountpoint)
          - [mountPoint type](#mountpoint-type)
            - [idType](#idtype-string)
            - [options](#options-string)
            - [path](#mountpoint-path)
    - [resetPartitionsUuidsType](#resetpartitionsuuidstype-string)
  - [iso](#iso-type)
    - [additionalFiles](#iso-additionalfiles)
      - [additionalFile type](#additionalfile-type)
        - [source](#source-string)
        - [content](#content-string)
        - [destination](#destination-string)
        - [permissions](#permissions-string)
    - [kernelCommandLine](#iso-kernelcommandline)
      - [extraCommandLine](#extracommandline-string)
  - [pxe](#pxe-type)
    - [isoImageBaseUrl](#isoimagebaseurl-string)
    - [isoImageFileUrl](#isoimagefileurl-string)
  - [os type](#os-type)
    - [resetBootLoaderType](#resetbootloadertype-string)
    - [hostname](#hostname-string)
    - [kernelCommandLine](#os-kernelcommandline)
      - [extraCommandLine](#extracommandline-string)
    - [packages](#packages-packages)
      - [packages type](#packages-type)
        - [updateExistingPackages](#updateexistingpackages-bool)
        - [installLists](#installlists-string)
          - [packageList type](#packagelist-type)
            - [packages](#packages-string)
        - [install](#install-string)
        - [removeLists](#removelists-string)
          - [packageList type](#packagelist-type)
            - [packages](#packages-string)
        - [remove](#remove-string)
        - [updateLists](#updatelists-string)
        - [update](#update-string)
    - [additionalFiles](#os-additionalfiles)
      - [additionalFile type](#additionalfile-type)
        - [source](#source-string)
        - [content](#content-string)
        - [destination](#destination-string)
        - [permissions](#permissions-string)
    - [additionalDirs](#additionaldirs-dirconfig)
      - [dirConfig](#dirconfig-type)
        - [source](#dirconfig-source)
        - [destination](#dirconfig-destination)
        - [newDirPermissions](#newdirpermissions-string)
        - [mergedDirPermissions](#mergeddirpermissions-string)
        - [childFilePermissions](#childfilepermissions-string)
    - [users](#users-user)
      - [user type](#user-type)
        - [name](#user-name)
        - [uid](#uid-int)
        - [password](#password-password)
          - [password type](#password-type)
            - [type](#password-type-type)
            - [value](#password-type-value)
        - [passwordExpiresDays](#passwordexpiresdays-int)
        - [sshPublicKeyPaths](#sshpublickeypaths-string)
        - [primaryGroup](#primarygroup-string)
        - [secondaryGroups](#secondarygroups-string)
        - [startupCommand](#startupcommand-string)
    - [selinux](#selinux-type)
      - [mode](#mode-string)
    - [services](#services-type)
      - [enable](#enable-string)
      - [disable](#disable-string)
    - [modules](#modules-module)
      - [module type](#module-type)
        - [name](#module-name)
        - [loadMode](#loadmode-string)
        - [options](#options-mapstring-string)
    - [overlays](#overlays-overlay)
      - [overlay type](#overlay-type)
  - [scripts type](#scripts-type)
    - [postCustomization](#postcustomization-script)
      - [script type](#script-type)
        - [path](#script-path)
        - [content](#content-string)
        - [interpreter](#interpreter-string)
        - [arguments](#arguments-string)
        - [environmentVariables](#environmentvariables-mapstring-string)
        - [name](#script-name)
    - [finalizeCustomization](#finalizecustomization-script)
      - [script type](#script-type)
        - [path](#script-path)
        - [content](#content-string)
        - [interpreter](#interpreter-string)
        - [arguments](#arguments-string)
        - [environmentVariables](#environmentvariables-mapstring-string)
        - [name](#script-name)

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

  filesystems:
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

### iso [[iso](#iso-type)]

Optionally specifies the configuration for the generated ISO media.

### pxe [[pxe](#pxe-type)]

Optionally specifies the PXE-specific configuration for the generated OS artifacts.

### os [[os](#os-type)]

Contains the configuration options for the OS.

Example:

```yaml
os:
  hostname: example-image
```

### scripts [[scripts](#scripts-type)]

Specifies custom scripts to run during the customization process.

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

## pxe type

Specifies the PXE-specific configuration for the generated OS artifacts.

### isoImageBaseUrl [string]

Specifies the base URL for the ISO image to download at boot time. The Azure
Linux Image Customizer will append the output image name to the specified base
URL to form the full URL for downloading the image. The output image name is
specified on the command-line using the `--output-image file` argument (see the
  [command-line interface](./cli.md) document for more details).

This can be useful if the ISO image name changes with each build and the
script deploying the artifacts to the PXE server does not update grub.cfg with
the ISO image name.

For example,

- If the user has the following content in the configuration file:

  ```yaml
  pxe:
    isoImageBaseUrl: http://hostname-or-ip/iso-publish-path
  ```

- and specifies the following on the command line:

  ```bash
  sudo imagecustomizer \
    --image-file "./input/azure-linux.vhdx" \
    --config-file "./input/customization-config.yaml" \
    --rpm-source "./input/rpms" \
    --build-dir "./build" \
    --output-image-format "iso" \
    --output-image-file "./build/output/output.iso" \
    --output-pxe-artifacts-dir "./build/output/pxe-artifacts"
  ```

- then, during PXE booting, the ISO image will be downloaded from:

  ```bash
  http://hostname-or-ip/iso-publish-path/output.iso
  ```

This field is mutually exclusive with `isoImageFileUrl`.

For an overview of Azure Linux Image Customizer support for PXE, see the 
[PXE support page](./pxe.md).

### isoImageFileUrl [string]

Specifies the URL of the ISO image to download at boot time.
The ISO image must be a LiveOS ISO image generated by the Azure Linux Image
Customizer. The booting process will pivot to the root file system embedded
in the ISO image after downloading it.

PXE Configuration Example:

- ```yaml
  pxe:
    isoImageFileUrl: http://hostname-or-ip/iso-publish-path/my-liveos.iso
  ```

The supported download protocols are: nfs, http, https, ftp, torent, tftp.

This field is mutually exclusive with `isoImageBaseUrl`.

For an overview of Azure Linux Image Customizer support for PXE, see the 
[PXE support page](./pxe.md).

## iso type

Specifies the configuration for the generated ISO media.

<div id="iso-kernelcommandline"></div>

### kernelCommandLine [[kernelCommandLine](#kernelcommandline-type)]

Specifies extra kernel command line options.

<div id="iso-additionalfiles"></div>

### additionalFiles [[additionalFile](#additionalfile-type)[]>]

Adds files to the ISO.

## overlay type

Specifies the configuration for overlay filesystem.

Overlays Configuration Example:

```yaml
storage:
  disks:
  bootType: efi
  - partitionTableType: gpt
    maxSize: 4G
    partitions:
    - id: esp
      type: esp
      start: 1M
      end: 9M
    - id: boot
      start: 9M
      end: 108M
    - id: rootfs
      label: rootfs
      start: 108M
      end: 2G
    - id: var
      start: 2G

  filesystems:
  - deviceId: esp
    type: fat32
    mountPoint:
      path: /boot/efi
      options: umask=0077
  - deviceId: boot
    type: ext4
    mountPoint:
      path: /boot
  - deviceId: rootfs
    type: ext4
    mountPoint:
      path: /
  - deviceId: var
    type: ext4
    mountPoint:
      path: /var
      options: defaults,x-initrd.mount

os:
  resetBootLoaderType: hard-reset
  overlays:
    - mountPoint: /etc
      lowerDirs:
      - /etc
      upperDir: /var/overlays/etc/upper
      workDir: /var/overlays/etc/work
      isInitrdOverlay: true
      mountDependencies:
      - /var
    - mountPoint: /media
      lowerDirs:
      - /media
      - /home
      upperDir: /overlays/media/upper
      workDir: /overlays/media/work
```

### `mountPoint` [string]

The directory where the combined view of the `upperDir` and `lowerDir` will be
mounted. This is the location where users will see the merged contents of the
overlay filesystem. It is common for the `mountPoint` to be the same as the
`lowerDir`. But this is not required.

Example: `/etc`

### `lowerDirs` [string[]]

These directories act as the read-only layers in the overlay filesystem. They
contain the base files and directories which will be overlaid by the `upperDir`.
Multiple lower directories can be specified by providing a list of paths, which
will be joined using a colon (`:`) as a separator.

Example:

```yaml
lowerDirs: 
- /etc
```

### `upperDir` [string]

This directory is the writable layer of the overlay filesystem. Any
modifications, such as file additions, deletions, or changes, are made in the
upperDir. These changes are what make the overlay filesystem appear different
from the lowerDir alone. 
  
Example: `/var/overlays/etc/upper`

### `workDir` [string]

This is a required directory used for preparing files before they are merged
into the upperDir. It needs to be on the same filesystem as the upperDir and
is used for temporary storage by the overlay filesystem to ensure atomic
operations. The workDir is not directly accessible to users. 
  
Example: `/var/overlays/etc/work`

### `isInitrdOverlay` [bool]

A boolean flag indicating whether this overlay is part of the root filesystem.
If set to `true`, specific adjustments will be made, such as prefixing certain
paths with `/sysroot`, and the overlay will be added to the fstab file with the
`x-initrd.mount` option to ensure it is available during the initrd phase.

This is an optional argument.

Example: `False`

### `mountDependencies` [string[]]

Specifies a list of directories that must be mounted before this overlay. Each
directory in the list should be mounted and available before the overlay
filesystem is mounted.

This is an optional argument.

Example:

```yaml
mountDependencies: 
- /var
```

**Important**: If any directory specified in `mountDependencies` needs to be
available during the initrd phase, you must ensure that this directory's mount
configuration in the `filesystems` section includes the `x-initrd.mount` option.
For example:

```yaml
filesystems:
  - deviceId: var
    type: ext4
    mountPoint:
      path: /var
      options: defaults,x-initrd.mount
```

### `mountOptions` [string]

A string of additional mount options that can be applied to the overlay mount.
Multiple options should be separated by commas.

This is an optional argument.

Example: `noatime,nodiratime`

## verity type

Specifies the configuration for dm-verity integrity verification.

Note: Currently only root partition (`/`) is supported. Support for other partitions
(e.g. `/usr`) may be added in the future.

There are multiple ways to configure a verity enabled image. For
recommendations, see [Verity Image Recommendations](./verity.md).

<div id="verity-id"></div>

### id [string]

Required.

The ID of the verity object.
This is used to correlate verity objects with [filesystem](#filesystem-type)
objects.

<div id="verity-name"></div>

### name [string]

Required.

The name of the device mapper block device.

The value must be:

- `root` for root partition (i.e. `/`)

### dataDeviceId [string]

The ID of the [partition](#partition-type) to use as the verity data partition.

### hashDeviceId [string]

The ID of the [partition](#partition-type) to use as the verity hash partition.

### corruptionOption [string]

Optional.

Specifies how a mismatch between the hash and the data partition is handled.

Supported values:

- `io-error`: Fails the I/O operation with an I/O error.
- `ignore`: Ignores the corruption and continues operation.
- `panic`: Causes the system to panic (print errors) and then try restarting.
- `restart`: Attempts to restart the system.

Default value: `io-error`.

## additionalFile type

Specifies options for placing a file in the OS.

Type is used by: [additionalFiles](#additionalfiles-additionalfile)

### source [string]

The path of the source file to copy to the destination path.

Example:

```yaml
os:
  additionalFiles:
    files/a.txt:
    - path: /a.txt
```

### content [string]

The contents of the file to write to the destination path.

Example:

```yaml
os:
  additionalFiles:
  - content: |
      abc
    destination: /a.txt
```

### destination [string]

The absolute path of the destination file.

Example:

```yaml
os:
  additionalFiles:
  - source: files/a.txt
    destination: /a.txt
```

### permissions [string]

The permissions to set on the destination file.

Supported formats:

- String containing an octal string. e.g. `"664"`

Example:

```yaml
os:
  additionalFiles:
  - source: files/a.txt
    destination: /a.txt
    permissions: "664"
```

## dirConfig type

Specifies options for placing a directory in the OS.

Type is used by: [additionalDirs](#additionaldirs-dirconfig)

<div id="dirconfig-source"></div>

### source [string]

The absolute path to the source directory that will be copied.

<div id="dirconfig-destination"></div>

### destination [string]

The absolute path in the target OS that the source directory will be copied to.

Example:

```yaml
os:
  additionalDirs:
    - source: "home/files/targetDir"
      destination: "usr/project/targetDir"
```

### newDirPermissions [string]

The permissions to set on all of the new directories being created on the target OS
(including the top-level directory). Default value: `755`.

### mergedDirPermissions [string]

The permissions to set on the directories being copied that already do exist on the
target OS (including the top-level directory). **Note:** If this value is not specified
in the config, the permissions for this field will be the same as that of the
pre-existing directory.

### childFilePermissions [string]

The permissions to set on the children file of the directory. Default value: `755`.

Supported formats for permission values:

- String containing an octal value. e.g. `664`

Example:

```yaml
os:
  additionalDirs:
    - source: "home/files/targetDir"
      destination: "usr/project/targetDir"
      newDirPermissions: "644"
      mergedDirPermissions: "777"
      childFilePermissions: "644"
```

## filesystem type

Specifies the mount options for a partition.

### deviceId [string]

Required.

The ID of the [partition](#partition-type) or [verity](#verity-type) object.

### type [string]

Required.

The filesystem type of the partition.

Supported options:

- `ext4`
- `fat32` (alias for `vfat`)
- `vfat` (will select either FAT12, FAT16, or FAT32 based on the size of the partition)
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

<div id="partition-id"></div>

### id [string]

Required.

The ID of the partition.
This is used to correlate Partition objects with [filesystem](#filesystem-type)
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
  The partition must have a `fileSystemType` of `fat32` or `vfat`.

- `bios-grub`: Specifies this partition is the BIOS boot partition.
  This is required for GPT disks that wish to be bootable using legacy BIOS mode.

  This partition must start at block 1.

  This flag is only supported on GPT formatted disks.

  For further details, see: https://en.wikipedia.org/wiki/BIOS_boot_partition

## password type

Specifies a password for a user.

WARNING: Passwords should not be used in images used in production.

This feature is intended for debugging purposes only.
As such, this feature has been disabled in official builds of the Image Customizer tool.

Instead of using passwords, you should use an authentication system that relies on
cryptographic keys.
For example, SSH with Microsoft Entra ID authentication.

Example:

```yaml
os:
  users:
  - name: test
    password:
      type: locked
```

<div id="password-type-type"></div>

### type [string]

The manner in which the password is provided.

Supported options:

- `locked`: Password login is disabled for the user. This is the default behavior.

Options for debugging purposes only (disabled by default):

- `plain-text`: The value is a plain-text password.

- `hashed`: The value is a password that has been pre-hashed.
  (For example, by using `openssl passwd`.)

- `plain-text-file`: The value is a path to a file containing a plain-text password.

- `hashed-file`: The value is a path to a file containing a pre-hashed password.

<div id="password-type-value"></div>

### value [string]

The password's value.
The meaning of this value depends on the type property.

## mountPoint type

You can configure `mountPoint` in one of two ways:

1. **Structured Format**: Use `idType`, `options`, and `path` fields for a more detailed configuration.
   
   ```yaml
   mountPoint:
     path: /boot/efi
     options: umask=0077
     idType: part-uuid
   ```

2. **Shorthand Path Format**: Provide the mount path directly as a string when only `path` is required.

   ```yaml
   mountPoint: /boot/efi
   ```

   In this shorthand format, only the `path` is specified, and default values will be applied to any optional fields.

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

Only one of `path` or `content` may be specified.

Example:

```yaml
scripts:
  postCustomization:
  - path: scripts/a.sh
```

### content [string]

The contents of the script to run.

The script is written to a temporary file under the customized OS's `/tmp` directory.

Only one of `path` or `content` may be specified.

Example:

```yaml
scripts:
  postCustomization:
  - content: |
      echo "Hello, World"
```

### interpreter [string]

The program to run the script with.

If not specified, then the script is run by `/bin/sh`.

Example:

```yaml
scripts:
  postCustomization:
  - content: |
      print("Hello, World")
    interpreter: python3
```

### arguments [string[]]

Additional arguments to pass to the script.

Example:

```yaml
scripts:
  postCustomization:
  - path: scripts/a.sh
    arguments:
    - abc
```

### environmentVariables [map\<string, string>]

Additional environment variables to set on the program.

Example:

```yaml
scripts:
  postCustomization:
  - content: |
      echo "$a $b"
    environmentVariables:
      a: hello
      b: world
```

<div id="script-name"></div>

### name [string]

The name of the script.

This field is only used to refer to the script in the logs.
It is particularly useful when `content` is used.

Example:

```yaml
scripts:
  postCustomization:
  - content: |
      echo "Hello, World"
    name: greetings
```

## scripts type

Specifies custom scripts to run during the customization process.

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
scripts:
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

### hostname [string]

Specifies the hostname for the OS.

Implemented by writing to the `/etc/hostname` file.

Example:

```yaml
os:
  hostname: example-image
```

<div id="os-kernelcommandline"></div>

### kernelCommandLine [[kernelCommandLine](#kernelcommandline-type)]

Specifies extra kernel command line options.

### packages [packages](#packages-type)

Remove, update, and install packages on the system.

<div id="os-additionalfiles"></div>

### additionalFiles [[additionalFile](#additionalfile-type)[]>]

Copy files into the OS image.

```yaml
os:
  additionalFiles:
  - source: files/a.txt
    destination: /a.txt

  - content: |
      abc
    destination: /b.txt
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
    - source: "path/to/local/directory/"
      destination: "/path/to/destination/directory/"
    # Copying directory with specific permission options.
    - source: "path/to/local/directory/"
      destination: "/path/to/destination/directory/"
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

### overlays [[overlay](#overlay-type)[]]

Used to add filesystem overlays.

### selinux [[selinux](#selinux-type)]

Options for configuring SELinux.

Example:

```yaml
os:
  selinux:
    mode: permissive
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

### password [[password](#password-type)]

Specifies the user's password.

WARNING: Passwords should not be used in images used in production.

### passwordExpiresDays [int]

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

A list of file paths to SSH public key files.
These public keys will be copied into the user's `~/.ssh/authorized_keys` file.

Note: It is preferable to use Microsoft Entra ID for SSH authentication, instead of
individual public keys.

Example:

```yaml
os:
  users:
  - name: test
    sshPublicKeyPaths:
    - id_ed25519.pub
```

### sshPublicKeys [string[]]

A list of SSH public keys.
These public keys will be copied into the user's `~/.ssh/authorized_keys` file.

Note: It is preferable to use Microsoft Entra ID for SSH authentication, instead of
individual public keys.

Example:

```yaml
os:
  users:
  - name: test
    sshPublicKeys:
    - ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIFyWtgGE06d/uBFQm70tYKvJKwJfRDoh06bWQQwC6Qkm test@test-machine
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

## selinux type

### mode [string]

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
policy, then it is recommended to apply these new policies using a
([postCustomization](#postcustomization-script)) script.
After applying the policies, you do not need to call `setfiles` manually since it will
called automatically after the `postCustomization` scripts are run.

Example:

```yaml
os:
  selinux:
    mode: enforcing

  packages:
    install:
    # Required packages for SELinux.
    - selinux-policy
    - selinux-policy-modules
    
    # Optional packages that contain useful SELinux utilities.
    - setools-console
    - policycoreutils-python-utils
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

### verity [[verity](#verity-type)[]]

Configure verity block devices.

### filesystems [[filesystem](#filesystem-type)[]]

Specifies the mount options of the partitions.

### resetPartitionsUuidsType [string]

Specifies that the partition UUIDs and filesystem UUIDs should be reset.

Value is optional.

This value cannot be specified if [storage](#storage-storage) is specified (since
customizing the partition layout resets all the UUIDs anyway).

If this value is specified, then [os.resetBootLoaderType](#resetbootloadertype-string)
must also be specified.

Supported options:

- `reset-all`: Resets the partition UUIDs and filesystem UUIDs for all the partitions.

Example:

```yaml
storage:
  resetPartitionsUuidsType: reset-all

os:
  resetBootLoaderType: hard-reset
```
