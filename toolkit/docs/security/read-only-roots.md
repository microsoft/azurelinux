Read-Only Roots
===

- [dm-verity Read Only Roots](#dm-verity-read-only-roots)
  - [Creating Verity Disks](#Creating-Verity-Disks)
  - [Writable Areas](#Writable-Areas)
  - [Root of Trust](#Root-of-Trust)
  - [Users, Machine ID, Misc. Configuration](#Users-Machine-ID-Misc-Configuration)
  - [Forward Error Correction (FEC)](#Forward-Error-Correction-(FEC))
  - [Hash Tree and FEC Overhead](#Hash-Tree-and-FEC-Overhead)
  - [Debugging](#Debugging)
  - [ISO Installers](#ISO-Installers)

## dm-verity Read Only Roots
`dm-verity` is a Device Mapper target which creates read-only partitions with built-in integrity checking. This means a verity partition can detect (and if FEC is enabled, fix) changes to the data in the partition.

A Merkle hash tree is created from the measurements of each block in the partition (Hash each 4k block, then hash those hashes. Repeat until you have a single hash). The root node of the tree, a single hash, is called the `root hash`.

When data is read from disk the blocks are hashed and checked against the hash tree to detect any changes. Any change to a block will modify its branch of the tree, all the way down to the root hash. By securing the root hash the entire partition can be secured.

### Creating Verity Disks
Read-only roots can be enabled using the `"ReadOnlyVerityRoot"` key in the image configuration JSON file (See [imageconfig.md](../formats/imageconfig.md#ReadOnlyVerityRoot) for details)
Since the read-only partition becomes unmodifiable as soon as it's measured, the snapshot must be taken at the very end of the build process. The `imager` tool switches the root to read-only mode, then uses the `veritysetup` tool to measure the root into a hash tree, FEC data, and compute the root hash. These files are then placed into the `initramfs`.

Any non-standard modifications to the image (adding symlinks, generating custom machine IDs, changing configs, etc.) need to be made prior to this point by using the `"PostInstallScripts"` key in the image config.

### Writable Areas
The build system currently supports two types of writable areas which are useful for read-only verity disks:

#### Temporary Overlays
Passing a list of directories using the `"TmpfsOverlays"` key in the `"ReadOnlyVerityRoot"` config will cause the initramfs to add `tmpfs` based writable overlays to each listed directory. These overlays are backed in RAM and will be reset after a reboot. These are useful for logging, or other transient data that is not security critical. Ideally the overlays should be kept as small as possible to minimize the number of files which may be maliciously modified at run time. The example configurations mount `/var` under a single overlay, but a more targeted approach is desirable. By default the overlays will consume at most 20% of the available memory. This can be configured using the `"TmpfsOverlaysSize"` key.

#### Writable Mount Points
Traditional mount points still function as expected. A writable data partition can be mounted using the normal configuration keys if desired.

### Root of Trust
The root of trust for a verity partition is the root hash. If this single hash is trusted, the entire hash tree, and subsequently the root partition, can also be trusted. 

The root hash may be protected in three ways:
- The file itself is stored in a safe location (signed `initramfs`)
- The root hash is accompanied by a signature file which is validated against the kernel key ring
- The root hash is passed on the kernel's command line in a secure manner

The `imager` tool automatically places the root hash and hash tree in the initramfs and sets the kernel command line in the `grub.cfg` file to use the verity files. This means that both the grub configuration files and the initramfs must be part of the verified boot chain to fully tie the verity root filesystem into the chain of trust.

### Users, Machine ID, Misc. Configuration
Files in `/etc` such as the `passwd` and `machine-id` files are also part of the read-only filesystem, making them unmodifiable. If the machine-id is blank on system start, and the file is read-only, the systemd `systemd-machine-id-setup` command will create a tmpfs backed machine-id which will be different for every boot. If a stable `machine-id` is desired this file will need to be writable. Consider bind mounting the file early using the `x-initrd.mount` mount option and adding it to the `fstab` with `"PostInstallScripts"`.

Ideally as much of `/etc` as possible should be left read-only to avoid miss-configuration.

### Forward Error Correction (FEC)
Verity supports error correction which will return the original data even if the underlying blocks have been modified (it does not restore the underlying data stored on disk however). FEC incurs some overhead but the hash tree, which is a sunk cost, makes it much more effective than normal Reed-Solomon codes. For a 2GiB disk, FEC with 2 roots (i.e. 2 bytes of error correction codes per 255 bytes of real data) can correct ~16MiB of errors with ~16MiB of overhead. See [veritydisk.go](../../tools/imagegen/configuration/veritydisk.go) for calculation details.

### Hash Tree and FEC Overhead
The extra data required for verity needs to be stored outside the measured partition. In the case of Mariner it is stored in the initramfs. Assuming the Merkle tree is a full m-ary tree with m=128 (128 branches per node, from `4k/sizeof(sha256)`), the size of the Merkle tree is:
```
blockSize = 4k
m = blockSize / sizeof(sha256)
leafNodes = diskSize/blockSize
totalNodes = ceil((leafNodes*m - 1) / (m - 1))
totalTreeSize = totalNodes * sizeof(sha256)
```

The FEC data grows linearly with the disk size. By default two bytes of error correction data are used for every 255 bytes of actual data. This gives:
```
fecBytesPerBlock = 2
fecBlockSize = 255
fecDataSize = ceil(diskSize / fecBlockSize) * fecBytesPerBlock
```

#### Examples
For a 2GiB root disk we would expect:
```
leafNodes = 2GiB / 4KiB = 524288
totalTreeSize = ceil((524288*128 - 1) / (128 - 1)) * 256 = 135274752 bits = 16.13 MiB

fecDataSize = ceil(2GiB / 255 bits) * 2 bits = 134700000 = 16.06 MiB

totalOverhead = 32.19 MiB (1.5% overhead)
```
For a 20GiB root disk we would expect:
```
totalTreeSize = 161.3 MiB

fecDataSize = 160.6 MiB

totalOverhead = 321.9 MiB (1.6% overhead)
```

### Debugging
The read-only nature of these images can make debugging quite challenging.
#### Serial Debugging
Adding the following config will enable serial output (useful for both hardware and VM images), and will set `dracut` (The package which runs in the initramfs) to log its output and drop to an interactive shell in the event of a failure.
```json
"KernelCommandLine": {
                "ExtraCommandLine": "console=tty0 console=ttyS0=9800 rd.debug rd.shell=1"
}
```

#### Overlay Debugging
If the `verity-read-only-root-debug-tools` package is included in the image, and the `"TmpfsOverlayDebugEnabled"` key is set to `true`, a read-only copy of the overlay upper directories (which will show the modified files for each overlay) will be visible under `/mnt/verity_overlay_debug_tmpfs`.

#### Error Handling Debugging
The `verity-read-only-root-debug-tools` package also includes the `/mnt/create_linear_mount.sh` script which will freeze the verity root and make a new, writable, mount at `/mnt/verity_writable_debug`. Interacting with the system while the root is frozen can be unstable however, so proceed with caution.

Once the writable mount is created it is possible to write data back to the underlying disk. If the root partition is unfrozen again the changes will begin to be detected. Most changes will not show since the view of the disk is cached, but any changes to uncached files should trigger the error behavior. If FEC is enabled errors will simply be fixed until enough blocks are corrupted. The FEC correction is visible in the `dmesg` log.

If enough blocks are corrupted the system will eventually be unable to recover them with FEC and the error handling behavior will trigger. The default behavior is to simply return an IO error, but other options are available by setting the `"VerityErrorBehavior"` key in the configuration file.

## ISO Installers
If a configuration used to create an ISO has a read-only root configured, the ISO installer will honor that configuration. (See `full.json`'s `"CBL-Mariner Core Read-Only"` entry).
