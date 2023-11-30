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
  /home/george/temp/derived-initrd-working-dir/initrd.img-5.15.137.1-1.cm2

# ~/temp/iso-output
./toolkit/mic-iso-gen/2-create-iso.sh \
    /home/george/temp/derived-initrd-working-dir/initrd.img-5.15.137.1-1.cm2 \
    /home/george/temp/extracted-artifacts-dir/original-vmlinuz-extracted/vmlinuz-5.15.137.1-1.cm2 \
    ~/git/CBL-Mariner/toolkit/mic-iso-gen/files/stock/grub.cfg \
    ~/git/CBL-Mariner/toolkit/mic-iso-gen/files/stock/iso-image-installer/iso-image-installer.sh \
    ~/git/CBL-Mariner/toolkit/mic-iso-gen/files/stock/iso-image-installer/host-configuration.json \
    ~/temp/iso-output/iso-intermediates/disk0.raw \
    $OUTPUT_DIR
```

```bash
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

# Test our ability to re-package it...
#
./toolkit/mic-iso-gen/0-0-extract-initrd-from-full-image.sh \
  ~/temp/iso-output/iso-intermediates/disk0.raw \
  /mnt/full-disk-rootfs-mount \
  /home/george/temp/extracted-artifacts-dir

/home/george/git/CBL-Mariner/toolkit/mic-iso-gen/test-roast.sh \
  /home/george/temp/experiment/in/extracted

```

```bash
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------


OUTPUT_DIR=~/temp/iso-output
# sudo rm -rf $OUTPUT_DIR
mkdir -p $OUTPUT_DIR

INTERMEDIATE_ARTIFACTS_DIR=$OUTPUT_DIR/iso-intermediates
mkdir -p $INTERMEDIATE_ARTIFACTS_DIR

cd ~/git/CBL-Mariner/

#------------------------------------------------------------------------------
# ~/temp/iso-output/iso-intermediates/disk0.raw
./toolkit/mic-iso-gen/1-build-rootfs.sh ~/git/CBL-Mariner/imageconfigs/baremetal.json $INTERMEDIATE_ARTIFACTS_DIR

#------------------------------------------------------------------------------
# Extract vmlinuz...
#
# Output:
# ls -la /home/george/temp/extracted-artifacts-dir/original-vmlinuz-extracted/vmlinuz-5.15.137.1-1.cm2
#
./toolkit/mic-iso-gen/0-0-extract-vmlinuz-from-full-image.sh \
  ~/temp/iso-output/iso-intermediates/disk0.raw \
  /mnt/full-disk-rootfs-mount \
  /home/george/temp/extracted-artifacts-dir

#------------------------------------------------------------------------------
# extract rootfs to be the seed for initrd...
#
# Output:
# ls -la /home/george/temp/extracted-artifacts-dir/new-initrd-root
#
./toolkit/mic-iso-gen/0-0-b-extract-rootfs.sh \
    ~/temp/iso-output/iso-intermediates/disk0.raw \
    /mnt/full-disk-rootfs-mount \
    /home/george/temp/tmp-extract-rootfs \
    /home/george/temp/extracted-artifacts-dir

#------------------------------------------------------------------------------
## modify rootfs into initrd...
#
# Output:
# ls -la ~/temp/extracted-artifacts-dir/new-initrd-root/
#
# Compare with: ls -la ~/temp/iso-minimal-initrd/extracted/
#
sudo cp ~/temp/iso-minimal-initrd/extracted/root/mariner-iso-start-up.sh \
    /home/george/temp/extracted-artifacts-dir/new-initrd-root/root/

sudo cp ~/git/CBL-Mariner/toolkit/mic-iso-gen/0-0-c-rpm-uninstall-packages.sh \
    /home/george/temp/extracted-artifacts-dir/new-initrd-root

sudo rm /home/george/temp/extracted-artifacts-dir/new-initrd-root/etc/fstab
sudo touch /home/george/temp/extracted-artifacts-dir/new-initrd-root/etc/fstab

pushd /home/george/temp/extracted-artifacts-dir/new-initrd-root/
sudo patch -p1 -i /home/george/git/CBL-Mariner/toolkit/mic-iso-gen/passwd.patch

popd

sudo chroot /home/george/temp/extracted-artifacts-dir/new-initrd-root/
sudo chown -R root:root .
/0-0-c-rpm-uninstall-packages.sh
exit

sudo chmod 744 /home/george/temp/extracted-artifacts-dir/new-initrd-root/boot

#------------------------------------------------------------------------------
# Re-package
#
# Output:
# ls -la /home/george/temp/experiment-roast-out/initrd.img
#
/home/george/git/CBL-Mariner/toolkit/mic-iso-gen/0-0-d-create-initrd-using-roast.sh \
  /home/george/temp/extracted-artifacts-dir/new-initrd-root/

# create an initrd...

# ~/temp/iso-output

# INITRD_FILE=/home/george/temp/derived-initrd-working-dir/initrd.img-5.15.137.1-1.cm2
# INITRD_FILE=/home/george/temp/reduced-rootfs-to-initrd/initrd.img
# INITRD_FILE=/mnt/full-initrd-iso/isolinux/initrd.img
# INITRD_FILE=~/temp/experiment/new/compressed/initrd.img
# INITRD_FILE=/home/george/temp/experiment-roast-out/initrd.img
INITRD_FILE=/home/george/temp/experiment-roast-out/initrd.img
OUTPUT_DIR=~/temp/iso-output
mkdir -p $OUTPUT_DIR

INTERMEDIATE_ARTIFACTS_DIR=$OUTPUT_DIR/iso-intermediates
mkdir -p $INTERMEDIATE_ARTIFACTS_DIR

./toolkit/mic-iso-gen/2-create-iso.sh \
    $INITRD_FILE \
    /home/george/temp/extracted-artifacts-dir/original-vmlinuz-extracted/vmlinuz-5.15.137.1-1.cm2 \
    ~/git/CBL-Mariner/toolkit/mic-iso-gen/files/stock/grub.cfg \
    ~/git/CBL-Mariner/toolkit/mic-iso-gen/files/stock/iso-image-installer/iso-image-installer.sh \
    ~/git/CBL-Mariner/toolkit/mic-iso-gen/files/stock/iso-image-installer/host-configuration.json \
    ~/temp/iso-output/iso-intermediates/disk0.raw \
    $OUTPUT_DIR

```