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
    ~/git/CBL-Mariner/toolkit/mic-iso-gen/files/grub.cfg \
    $INTERMEDIATE_ARTIFACTS_DIR/disk0.raw \
    ~/git/CBL-Mariner/toolkit/mic-iso-gen/files/host-configuration.json \
    $OUTPUT_DIR
```