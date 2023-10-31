# Image configuration

Image configuration consists of two sections - Disks and SystemConfigs - that describe the produced artifact(image). Image configuration code can be found in (configuration.go)[../../tools/imagegen/configuration/configuration.go] and validity of the configuration file can be verified by the [imageconfigvalidator](../../tools/imageconfigvalidator/imageconfigvalidator.go)


## Disks
Disks entry specifies the disk configuration like its size (for virtual disks), partitions and partition table.

## TargetDisk
Required when building unattended ISO installer. This field defines the physical disk to which Mariner should be installed. The `Type` field must be set to `path` and the `Value` field must be set to the desired target disk path.

### Artifacts
Artifact (non-ISO image building only) defines the name, type and optional compression of the output CBL-Mariner image.

Sample Artifacts entry, creating a raw rootfs, compressed to .tar.gz format(note that this format does not support partitions, so there would be no "Partitions" entry):

``` json
"Artifacts": [
    {
        "Name": "core",
        "Compression": "tar.gz"
    }
]

```
Sample Artifacts entry, creating a vhdx disk image:

``` json
"Artifacts": [
    {
        "Name": "otherName",
        "Type": "vhdx"
    }
],
```

### Partitions
"Partitions" key holds an array of Partition entries.

Partition defines the size, name and file system type for a partition.
"Start" and "End" fields define the offset from the beginning of the disk in MBs.
An "End" value of 0 will determine the size of the partition using the next
partition's start offset or the value defined by "MaxSize", if this is the last
partition on the disk.

Note that Partitions do not have to be provided; the resulting image is going to be a rootfs.

Supported partition FsTypes: fat32, fat16, vfat, ext2, ext3, ext4, xfs, linux-swap.

Sample partitions entry, specifying a boot partition and a root partition:

``` json
"Partitions": [
    {
        "ID": "boot",
        "Flags": [
            "esp",
            "boot"
        ],
        "Start": 1,
        "End": 9,
        "FsType": "fat32"
    },
    {
        "ID": "rootfs",
        "Start": 9,
        "End": 0,
        "FsType": "ext4"
    }
]
```

#### Flags
"Flags" key controls special handling for certain partitions.

- `esp` indicates this is the UEFI esp partition
- `grub` indicates this is a grub boot partition
- `bios_grub` indicates this is a bios grub boot partition
- `boot` indicates this is a boot partition
- `dmroot` indicates this partition will be used for a device mapper root device (i.e. `Encryption` or `ReadOnlyVerityRoot`)

## SystemConfigs

SystemConfigs is an array of SystemConfig entries.

SystemConfig defines how each system present on the image is supposed to be configured.

### IsKickStartBoot

IsKickStartBoot is a boolean that determines whether this is a kickstart-style installation. It will determine whether to perform kickstart-specific operations like executing preinstall scripts and parsing kickstart partitioning file.

### PartitionSettings

PartitionSettings key is an array of PartitionSetting entries.

PartitionSetting holds the mounting information for each partition.

A sample PartitionSettings entry, designating an EFI and a root partitions:

``` json
"PartitionSettings": [
    {
        "ID": "boot",
        "MountPoint": "/boot/efi",
        "MountOptions" : "umask=0077"
    },
    {
        "ID": "rootfs",
        "MountPoint": "/"
    }
],
```

A PartitionSetting may set a `MountIdentifier` to control how a partition is identified in the `fstab` file. The supported options are `uuid`, `partuuid`, and `partlabel`. If the `MountIdentifier` is omitted `partuuid` will be selected by default.

`partlabel` may not be used with `mbr` disks, and requires the `Name` key in the corresponding `Partition` be populated. An example with the rootfs mounted via `PARTLABEL=my_rootfs`, but the boot mount using the default `PARTUUID=<PARTUUID>`:
``` json
"Partitions": [
    
    ...
    
    {
        "ID": "rootfs",
        "Name": "my_rootfs",
        "Start": 9,
        "End": 0,
        "FsType": "ext4"
    }
]
```
``` json
"PartitionSettings": [
    {
        "ID": "boot",
        "MountPoint": "/boot/efi",
        "MountOptions" : "umask=0077"
    },
    {
        "ID": "rootfs",
        "MountPoint": "/",
        "MountIdentifier": "partlabel"
    }
],
```

It is possible to use `PartitionSettings` to configure diff disk image creation. Two types of diffs are possible.
`rdiff` and `overlay` diff.

For small and deterministic images `rdiff` is a better algorithm.
For large images based on `ext4` `overlay` diff is a better algorithm.

A sample `ParitionSettings` entry using `rdiff` algorithm:

``` json
{
    "ID": "boot",
    "MountPoint": "/boot/efi",
    "MountOptions" : "umask=0077",
    "RdiffBaseImage" : "../out/images/core-efi/core-efi-1.0.20200918.1751.ext4"
},
 ```

A sample `ParitionSettings` entry using `overlay` algorithm:

``` json
{
   "ID": "rootfs",
   "MountPoint": "/",
   "OverlayBaseImage" : "../out/images/core-efi/core-efi-rootfs-1.0.20200918.1751.ext4"
}

```
`RdiffBaseImage` represents the base image when `rdiff` algorithm is used.
`OverlayBaseImage` represents the base image when `overlay` algorithm is used.

### EnableGrubMkconfig
EnableGrubMkconfig is a optional boolean that controls whether the image uses grub2-mkconfig to generate the boot configuration (/boot/grub2/grub.cfg) or not. If EnableGrubMkconfig is specified, only valid values are `true` and `false`.

### PackageLists

PackageLists key consists of an array of relative paths to the package lists (JSON files).

All of the files listed in PackageLists are going to be scanned in a linear order to obtain a final list of packages for the resulting image by taking a union of all packages. **It is recommended that initramfs is the last package to speed up the installation process.**

PackageLists **must not include kernel packages**! To provide a kernel, use KernelOptions instead. Providing a kernel package in any of the PackageLists files results in an **undefined behavior**.

If any of the packages depends on a kernel, make sure that the required kernel is provided with KernelOptions.

A sample PackageLists entry pointing to three files containing package lists:
``` json
"PackageLists": [
    "packagelists/hyperv-packages.json",
    "packagelists/core-packages-image.json",
    "packagelists/cloud-init-packages.json"
],
```

### Customization Scripts
The tools offer the option of executing arbitrary shell scripts during various points of the image generation process. There are three points that scripts can be executed: `PreInstall`, `PostInstall`, and `ImageFinalize`.

>Installer starts -> `PreInstallScripts` -> Create Partitions -> Install Packages -> `PostInstallScripts` -> Configure Bootloader (if any) -> Calculate dm-verity hashes (if configured) -> `ImageFinalizeScripts`

Each of the `PreInstallScripts`, `PostInstallScripts`, and `FinalizeImageScripts` entires are an array of file paths and the corresponding input arguments. The scripts will be executed in sequential order and within the context of the final image. The file paths are relative to the image configuration file. Scripts may be passed without arguments if desired.

All scripts follow the same format in the image config .json file:
``` json
"PreInstallScripts | PostInstallScripts | FinalizeImageScripts":[
    {
        "Path": "arglessScript.sh"
    },
    {
        "Path": "ScriptWithArguments.sh",
        "Args": "--input abc --output cba"
    }
],
```

#### PreInstallScripts

There are customer requests that would like to use a Kickstart file to install Mariner OS. Kickstart installation normally includes pre-install scripts that run before installation begins and are normally used to handle tasks like network configuration, determining partition schema etc. The `PreInstallScripts` field allows for running customs scripts for similar purposes. Sample Kickstart pre-install script [here](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/5/html/installation_guide/s1-kickstart2-preinstallconfig). You must set the `IsKickStartBoot` to true in order to make the installer execute the preinstall scripts.

The preinstall scripts are run from the context of the installer, NOT the installed system (since it doesn't exist yet).

**NOTE**: currently, Mariner's pre-install scripts are mostly intended to provide support for partitioning schema configuration. For this purpose, make sure the script creates a proper configuration file (example [here](https://www.golinuxhub.com/2018/05/sample-kickstart-partition-example-raid/)) under `/tmp/part-include` in order for it to be consumed by Mariner's image building tools.

#### PostInstallScripts

PostInstallScripts run immediately after all packages have been installed, but before image finalization steps are taken (configure bootloader, record read-only disks, etc). The postinstall scripts are run from the context of the installed system.

#### FinalizeImageScripts

FinalizeImageScripts provide the opportunity to run shell scripts to customize the image before it is finalized (converted to .vhdx, etc.). The finalizeimage scripts are run from the context of the installed system.

### AdditionalFiles

The `AdditionalFiles` list provides a mechanism to add arbitrary files to the image. The elements are are `"src": "dst"` pairs.

`src` is relative to the image config `.json` file.

The `dst` can be one of:

- A string representing the destination absolute path, OR
- An object (`FileConfig`) containing the destination absolute path and other file options, OR
- An array containing a mixture of strings and objects, which allows a single source file to be copied to multiple destination paths.

ISO installers will include the files on the installation media and will place them into the final installed image.

```json
    "AdditionalFiles": [
        "../../out/tools/imager": "/installer/imager",
        "additionalconfigs": [
            "/etc/my/config.conf",
            {
                "Path": "/etc/yours/config.conf",
                "Permissions": "664"
            }
        ]
    ]
```

#### FileConfig

`FileConfig` provides options to modify metadata of files copied using `AdditionalFiles`.

Fields:

- `Path`: The destination absolute path.
- `Permissions`: The file permissions to apply to the file.

  Supported value formats:

  - Octal string: A JSON string containing an octal number. e.g. `"664"`

### Networks

The `Networks` entry is added to enable the users to specify the network configuration parameters to enable users to set IP address, configure the hostname, DNS etc. Currently, the Mariner tooling only supports a subset of the kickstart network command options: `bootproto`, `gateway`, `ip`, `net mask`, `DNS` and `device`. Hostname can be configured using the `Hostname` entry of the image config. 

A sample Networks entry pointing to one network configuration:
``` json
    "Networks":[
    {
        "BootProto": "dhcp",
        "GateWay":   "192.168.20.4",
        "Ip":        "192.169.20.148",
        "NetMask":   "255.255.255.0",
        "OnBoot":    false,
        "NameServers": [
            "192.168.30.23"
        ],
        "Device": "eth0"
    }
],
```

### PackageRepos

The `PackageRepos` list defines custom package repos to use with **ISO installers**. Each repo must set `Name` and `BaseUrl`. Each repo may also set `GPGCheck`/`RepoGPGCheck` (both default to `true`), `GPGKeys` (a string of the form `file:///path/to/key1 file:///path/to/key2 ...`. `GPGKeys` defaults to the Microsoft RPM signing keys if left unset), and `Install` which causes the repo file to be installed into the final image.

If a custom repo entry is present, the default local file repo entires **will not be used during install**. If you want to also use them you will need to add an entry for [local.repo](toolkit/resources/manifests/image/local.repo) into the repo list. The default behavior is to pre-download the required packages into the ISO installer from repos defined in `REPO_LIST`.

By default the repo will only be used during ISO install, it may also be made available to the installed image by setting `Install` to `true`.

> **Currently ISO installers don't support custom keys. Only installed repos support them. The keys must be provisioned via [AdditionalFiles](#additionalfiles)**

```json
"PackageRepos": [
    {
        "Name":     "PackageMicrosoftComMirror",
        "BaseUrl":  "https://contoso.com/pmc-mirror/$releasever/prod/base/$basearch",
        "Install":  false,
    },
    {
        "Name":     "MyCopyOfOfficialRepo",
        "BaseUrl":  "https://contoso.com/cbl-mariner-custom-packages/$releasever/prod/base/$basearch",
        "Install":  true,
        "GPGCheck": true,
        "RepoGPGCheck": false,
        "GPGKeys": "file:///etc/pki/rpm-gpg/my-custom-key"
    }
]
```

### RemoveRpmDb

RemoveRpmDb triggers RPM database removal after the packages have been installed.
Removing the RPM database may break any package managers inside the image.

### KernelOptions

KernelOptions key consists of a map of key-value pairs, where a key is an identifier and a value is a name of the package (kernel) used in a scenario described by the identifier. During the build time, all kernels provided in KernelOptions will be built.

KernelOptions is mandatory for all non-`rootfs` image types.

KernelOptions may be included in `rootfs` images which expect a kernel, such as the initrd for an ISO, if desired.

Currently there is only one key with an assigned meaning:
- `default` key needs to be always provided. It designates a kernel that is used when no other scenario is applicable (i.e. by default).

Keys starting with an underscore are ignored - they can be used for providing comments.

A sample KernelOptions specifying a default kernel:

``` json
"KernelOptions": {
    "default": "kernel"
},
```

### ReadOnlyVerityRoot
"ReadOnlyVerityRoot" key controls making the root filesystem read-only using dm-verity.
It will create a verity disk from the partition mounted at "/". The verity data is stored as
part of the image's initramfs. More details can be found in [Misc: Read Only Roots](../how_it_works/5_misc.md#dm-verity-read-only-roots)

#### Considerations
Having a read-only root filesystem will change the behavior of the image in some fundamental ways. There are several areas that should be considered before enabling a read-only root:

##### Writable Data
Any writable data which needs to be preserved will need to be stored into a separate writable partition. The `TmpfsOverlays` key will create throw-away writable partitions which are reset on every boot. The example configs create an overlay on `/var`, but the more refined the overlays are, the more secure they will be.

##### GPL Licensing
If using a read-only root in conjunction with a verified boot flow that uses a signed initramfs, carefully consider the implications on GPLv3 code. The read-only nature of the filesystem means a user cannot replace GPLv3 components without re-signing a new initramfs.

##### Users
Since users are controlled by files in `/etc`, these files are read-only when this is set. It is recommended to either use SSH key based login or pre-hash the password to avoid storing passwords in plain text in the config files (See [Users](#users)).

##### Separate `/boot` Partition
Since the root partition's hash tree is stored as part of the initramfs, the initramfs cannot be stored on the same root partition (it would invalidate the measurements). To avoid this a separate `/boot` partition is needed to house the hash tree (via the initramfs).

##### ISO
The ISO command line installer supports enabling read-only roots if they are configured through the configuration JSON file (see [full.json's](../../imageconfigs/full.json) `"CBL-Mariner Core Read-Only"` entry). The automatic partition creation mode will create the required `/boot` partition if the read-only root is enabled.

The GUI installer does not currently support read-only roots.
- `Enable`: Enable dm-verity on the root filesystem
- `Name`: Custom name for the mounted root (default is `"verity_root_fs"`)
- `ErrorCorrectionEnable`: Enable automatic error correction of modified blocks (default is `true`)
- `ErrorCorrectionEncodingRoots`: Increase overhead to increase resiliency of the forward error correction (default is `2` bytes of code per 255 bytes of data)
- `RootHashSignatureEnable`: Validate the root hash against a key stored in the kernel's system keyring. The signature file should be called `<Name>.p7` and must be stored in the initramfs. This signature WILL NOT BE included automatically in the initramfs. It must be included via an out of band build step.
- `ValidateOnBoot`: Run a validation of the full disk at boot time, normally blocks are validated only as needed. This can take several minutes if the disk is corrupted.
- `VerityErrorBehavior`: Indicate additional special system behavior when encountering an unrecoverable verity corruption. One of `"ignore"`, `"restart"`, `"panic"`. Normal behavior is to return an IO error when reading corrupt blocks.
- `TmpfsOverlays`: Mount these paths as writable overlays backed by a tmpfs in memory.
- `TmpfsOverlaySize`: Maximum amount of memory the overlays may use. Maybe be one of three forms: `"1234"`, `"1234[k,m,g]"`, `"20%"` (default is `"20%"`) 
- `TmpfsOverlayDebugEnabled`: Make the tmpfs overlay mounts easily accessible for debugging purposes. They can be found in /mnt/verity_overlay_debug_tmpfs. Include the
    `verity-read-only-root-debug-tools` package to create the required mount points.

A sample ReadOnlyVerityRoot specifying a basic read-only root using default error correction. This configuration may be used for both normal images and ISO configurations:
``` json
"ReadOnlyVerityRoot": {
    "Enable": true,
    "TmpfsOverlays": [
        "/var"
    ],
},
```

### KernelCommandLine

KernelCommandLine is an optional key which allows additional parameters to be passed to the kernel when it is launched from Grub.

#### ImaPolicy
ImaPolicy is a list of Integrity Measurement Architecture (IMA) policies to enable, they may be any combination of `tcb`, `appraise_tcb`, `secure_boot`.

#### EnableFIPS
EnableFIPS is a optional boolean option that controls whether the image tools create the image with FIPS mode enabled or not. If EnableFIPS is specificed, only valid values are `true` and `false`.

#### ExtraCommandLine
ExtraCommandLine is a string which will be appended to the end of the kernel command line and may contain any additional parameters desired. The `` ` `` character is reserved and may not be used. **Note: Some kernel command line parameters are already configured by default in [grub.cfg](../../resources/assets/grub2/grub.cfg) and [/etc/default/grub](../../resources/assets/grub2/grub) for mkconfig-based images. Many command line options may be overwritten by passing a new value. If a specific argument must be removed from the existing grub template a `FinalizeImageScript` is currently required.

#### SELinux
The Security Enhanced Linux (SELinux) feature is enabled by using the `SELinux` key, with value containing the mode to use on boot.  The `enforcing` and `permissive` values will set the mode in /etc/selinux/config.
This will instruct init (systemd) to set the configured mode on boot.  The `force_enforcing` option will set enforcing in the config and also add `enforcing=1` in the kernel command line,
which is a higher precedent than the config file. This ensures SELinux boots in enforcing even if the /etc/selinux/config was altered.

#### CGroup
The version for CGroup in Mariner images can be enabled by using the `CGroup` key with value containing which version to use on boot. The value that can be chosen is either `version_one` or `version_two`. 
The `version_two` value will set the cgroupv2 to be used in Mariner by setting the config value `systemd.unified_cgroup_hierarchy=1` in the default kernel command line. The value `version_one` or no value set will keep cgroupv1 (current default) to be enabled on boot.
For more information about cgroups with Kubernetes, see [About cgroupv2](https://kubernetes.io/docs/concepts/architecture/cgroups/).

A sample KernelCommandLine enabling a basic IMA mode and passing two additional parameters:

``` json
"KernelCommandLine": {
    "ImaPolicy": ["tcb"],
    "ExtraCommandLine": "my_first_param=foo my_second_param=\"bar baz\""
},
```

A sample KernelCommandLine enabling SELinux and booting in enforcing mode:

``` json
"KernelCommandLine": {
    "SELinux": "enforcing"
},
```

A sample KernelCommandLine enabling CGroup and booting with cgroupv2 enabled:

``` json
"KernelCommandLine": {
    "CGroup": "version_two"
},
```

### HidepidDisabled

An optional flag that removes the `hidepid` option from `/proc`. `Hidepid` prevents proc IDs from being visible to all users. Set this flag if mounting `/proc` in postinstall scripts to ensure the mount options are set correctly.

### Users

Users is an array of user information. The User information is a map of key value pairs.

The image generated has users matching the values specified in Users.

The table below are the keys for the users.

|Key                |Type               |Restrictions
--------------------|:------------------|:------------------------------------------------
|Name               |string             |Cannot be empty
|UID                |string             |Must be in range 0-60000
|PasswordHashed     |bool               |
|Password           |string             |
|PasswordExpiresDays|number             |Must be in range 0-99999 or -1 for no expiration
|SSHPubKeyPaths     |array of strings   |
|PrimaryGroup       |string             |
|SecondaryGroups    |array of strings   |
|StartupCommand     |string             |

An example usage for users "root" and "basicUser" would look like:

``` json
"Users": [
    {
        "Name": "root",
        "Password": "somePassword"
    },
    {
        "Name": "basicUser",
        "Password": "someOtherPassword",
        "UID": 1001
    }
]
```

# Sample image configuration

A sample image configuration, producing a VHDX disk image:

``` json
{
    "Disks": [
        {
            "PartitionTableType": "gpt",
            "MaxSize": 11264,
            "Artifacts": [
                {
                    "Name": "core",
                    "Type": "vhdx"
                }
            ],
            "Partitions": [
                {
                    "ID": "boot",
                    "Flags": [
                        "esp",
                        "boot"
                    ],
                    "Start": 1,
                    "End": 9,
                    "FsType": "fat32"
                },
                {
                    "ID": "rootfs",
                    "Start": 9,
                    "End": 0,
                    "FsType": "ext4"
                }
            ]
        }
    ],
    "SystemConfigs": [
        {
            "Name": "Standard",
            "BootType": "efi",
            "PartitionSettings": [
                {
                    "ID": "boot",
                    "MountPoint": "/boot/efi",
                    "MountOptions" : "umask=0077",
                    "RdiffBaseImage" : "../out/images/core-efi/core-efi-1.0.20200918.1751.ext4"
                },
                {
                    "ID": "rootfs",
                    "MountPoint": "/",
                     "OverlayBaseImage" : "../out/images/core-efi/core-efi-rootfs-1.0.20200918.1751.ext4"
                }
            ],
            "PackageLists": [
                "packagelists/hyperv-packages.json",
                "packagelists/core-packages-image.json",
                "packagelists/cloud-init-packages.json"
            ],
            "KernelOptions": {
                "default": "kernel"
            },
            "KernelCommandLine": {
                "ImaPolicy": ["tcb"],
                "ExtraCommandLine": "my_first_param=foo my_second_param=\"bar baz\""
            },
            "Hostname": "cbl-mariner"
        }
    ]
}

```
