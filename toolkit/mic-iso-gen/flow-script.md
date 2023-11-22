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
# ~/temp/iso-intermediates/baremetal.iso
./toolkit/mic-iso-gen/0-build-baremetal-iso.sh gmileka/assemble-iso $INTERMEDIATE_ARTIFACTS_DIR

# ~/temp/iso-intermediates/disk0.raw
./toolkit/mic-iso-gen/1-build-rootfs.sh ~/git/CBL-Mariner/imageconfigs/baremetal.json $INTERMEDIATE_ARTIFACTS_DIR

# ~/temp/iso-output
./toolkit/mic-iso-gen/2-create-iso-2.sh \
    $INTERMEDIATE_ARTIFACTS_DIR/baremetal.iso \
    ~/git/CBL-Mariner/toolkit/mic-iso-gen/files/stock/grub.cfg \
    ~/git/CBL-Mariner/toolkit/mic-iso-gen/files/stock/iso-image-installer/iso-image-installer.sh \
    ~/git/CBL-Mariner/toolkit/mic-iso-gen/files/stock/iso-image-installer/host-configuration.json \
    $INTERMEDIATE_ARTIFACTS_DIR/disk0.raw \
    $OUTPUT_DIR
```

```bash
OUTPUT_DIR=~/temp/iso-output
sudo rm -rf $OUTPUT_DIR
mkdir -p $OUTPUT_DIR

INTERMEDIATE_ARTIFACTS_DIR=$OUTPUT_DIR/iso-intermediates
mkdir -p $INTERMEDIATE_ARTIFACTS_DIR

cd ~/git/CBL-Mariner/

# ~/temp/iso-output/iso-intermediates/disk0.raw
./toolkit/mic-iso-gen/1-build-rootfs.sh ~/git/CBL-Mariner/imageconfigs/baremetal.json $INTERMEDIATE_ARTIFACTS_DIR

# /home/george/temp/extracted-artifacts-dir/original-initrd-extracted/<initrd-file-system>
# /home/george/temp/extracted-artifacts-dir/original-vmlinuz-extracted/vmlinuz-5.15.137.1-1.cm2
./toolkit/mic-iso-gen/0-0-extract-initrd-and-vmlinuz.sh \
  ~/temp/iso-output/iso-intermediates/disk0.raw \
  /mnt/full-disk-rootfs-mount \
  /home/george/temp/extracted-artifacts-dir

./toolkit/mic-iso-gen/0-1-derive-initrd.sh \
  /home/george/temp/extracted-artifacts-dir/original-initrd-extracted \
  /home/george/temp/derived-initrd-working-dir \
  /home/george/temp/derived-initrd-working-dir/initrd.img-5.15.135.1-1.cm2

# ~/temp/iso-output
./toolkit/mic-iso-gen/2-create-iso.sh \
    /home/george/temp/derived-initrd-working-dir/initrd.img-5.15.135.1-1.cm2 \
    /home/george/temp/extracted-artifacts-dir/original-vmlinuz-extracted/vmlinuz-5.15.137.1-1.cm2 \
    ~/git/CBL-Mariner/toolkit/mic-iso-gen/files/stock/grub.cfg \
    ~/git/CBL-Mariner/toolkit/mic-iso-gen/files/stock/iso-image-installer/iso-image-installer.sh \
    ~/git/CBL-Mariner/toolkit/mic-iso-gen/files/stock/iso-image-installer/host-configuration.json \
    ~/temp/iso-output/iso-intermediates/disk0.raw \
    $OUTPUT_DIR
```