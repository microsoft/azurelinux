# Image configuration

Image configuration consists of two sections - Disks and SystemConfigs - that describe the produced artifact(image). Image configuration code can be found in (configuration.go)[../../tools/imagegen/configuration/configuration.go] and validity of the configuration file can be verified by the [imageconfigvalidator](../../tools/imageconfigvalidator/imageconfigvalidator.go)


## Disks
Disks entry specifies the disk configuration like its size (for virtual disks), partitions and partition table.

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

## SystemConfigs

SystemConfigs is an array of SystemConfig entries.

SystemConfig defines how each system present on the image is supposed to be configured.

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
### KernelOptions

KernelOptions key consists of a map of key-value pairs, where a key is an identifier and a value is a name of the package (kernel) used in a scenario described by the identifier. During the build time, all kernels provided in KernelOptions will be built.

KernelOptions is mandatory for all image types except for rootfs.

Currently there are only two keys with an assigned meaning:
- `default` key needs to be always provided. It designates a kernel that is used when no other scenario is applicable (i.e. by default).
- `hyperv` key is an optional key that is only meaningful in ISO context. It provides a kernel that will be chosen by the installer instead of the default one if the installer detects that the installation is conducted in the Hyper-V environment.


Keys starting with an underscore are ignored - they can be used for providing comments.

A sample KernelOptions specifying a default kernel:

``` json
"KernelOptions": {
    "default": "kernel-hyperv"
},
```

A sample KernelOptions specifying a default kernel and a specialized kernel for Hyper-V scenario:

``` json
"KernelOptions": {
    "default": "kernel",
    "hyperv": "kernel-hyperv"
},
```

### KernelCommandLine

KernelCommandLine is an optional key which allows additional parameters to be passed to the kernel when it is launched from Grub.

ImaPolicy is a list of Integrity Measurement Architecture (IMA) policies to enable, they may be any combination of `tcb`, `appraise_tcb`, `secure_boot`.

ExtraCommandLine is a string which will be appended to the end of the kernel command line and may contain any additional parameters desired. The `` ` `` character is reserved and may not be used.

A sample KernelCommandLine enabling a basic IMA mode and passing two additional parameters:

``` json
"KernelCommandLine": {
    "ImaPolicy": ["tcb"],
    "ExtraCommandLine": "my_first_param=foo my_second_param=\"bar baz\""
},
```

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
                    "MountOptions" : "umask=0077"
                },
                {
                    "ID": "rootfs",
                    "MountPoint": "/"
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
