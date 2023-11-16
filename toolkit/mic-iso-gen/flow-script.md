# Flow Script

```bash
OUTPUT_DIR=~/temp/iso-output
sudo rm -rf $OUTPUT_DIR
mkdir -p $OUTPUT_DIR

INTERMEDIATE_ARTIFACTS_DIR=$OUTPUT_DIR/iso-intermediates
mkdir -p $INTERMEDIATE_ARTIFACTS_DIR

cd ~/git/CBL-Mariner/

# ~/temp/iso-intermediates/iso-initrd.img
# ~/temp/iso-intermediates/vmlinuz
./toolkit/mic-iso-gen/0-build-initrd.sh gmileka/assemble-iso $INTERMEDIATE_ARTIFACTS_DIR

# ~/temp/iso-intermediates/disk0.raw
./toolkit/mic-iso-gen/1-build-rootfs.sh ~/git/CBL-Mariner/imageconfigs/baremetal.json $INTERMEDIATE_ARTIFACTS_DIR

# ~/temp/iso-output
./toolkit/mic-iso-gen/2-create-iso.sh \
    $INTERMEDIATE_ARTIFACTS_DIR/iso-initrd.img \
    $INTERMEDIATE_ARTIFACTS_DIR/vmlinuz \
    ~/git/CBL-Mariner/toolkit/mic-iso-gen/files/stock/grub.cfg \
    ~/git/CBL-Mariner/toolkit/mic-iso-gen/files/stock/iso-image-installer/iso-image-installer.sh \
    ~/git/CBL-Mariner/toolkit/mic-iso-gen/files/stock/iso-image-installer/host-configuration.json \
    $INTERMEDIATE_ARTIFACTS_DIR/disk0.raw \
    $OUTPUT_DIR
```

# mount
```bash
sudo mkdir /mnt/isomount
sudo mount -o loop ~/temp/iso-output/iso/baremetal-20231115-155831.iso /mnt/isomount
# /mnt/isomount/
# /mnt/isomount/artifacts
# /mnt/isomount/artifacts/disk0.raw
# /mnt/isomount/artifacts/host-configuration.json
# /mnt/isomount/boot
# /mnt/isomount/boot/grub
# /mnt/isomount/boot/grub/bios.img    [grub.cfg embedded]
# /mnt/isomount/boot/grub/boot.cat
# /mnt/isomount/boot/grub/efiboot.img [grub.cfg embedded]
# /mnt/isomount/boot/initrd.img
# /mnt/isomount/boot/vmlinuz
# /mnt/isomount/EFI
# /mnt/isomount/EFI/efiboot.img       [grub.cfg embedded]
```

## Flow

- build
  - an iso that does not do anything by default.
  - it has an agent/start-up script that can look for host-configuration and act on it.
  - it has an agent/start-up script that looks for a script in the artifacts folder
    (outside the initrd) and runs it.
- customize
  - download iso
  - read out:
    - initrd.img
    - vmlinuz
    - artifacts/grub.cfg [for re-building the bootloader images]
  - write
    - provide your own grub.cfg
    - add artifact files.

    - add packages to initrd.img [can mic work with initrd.img]
