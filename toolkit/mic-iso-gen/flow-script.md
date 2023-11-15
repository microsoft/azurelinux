# Flow Script

```bash
export INTERMEDIATE_ARTIFACTS_DIR=~/temp/iso-intermediates

sudo rm -rf $INTERMEDIATE_ARTIFACTS_DIR
mkdir -p $INTERMEDIATE_ARTIFACTS_DIR

cd ~/git/CBL-Mariner/

# ~/temp/iso-intermediates/iso-initrd.img
# ~/temp/iso-intermediates/vmlinuz
./toolkit/mic-iso-gen/0-build-initrd.sh gmileka/assemble-iso $INTERMEDIATE_ARTIFACTS_DIR

# ~/temp/iso-intermediates/disk0.raw
./toolkit/mic-iso-gen/1-build-rootfs.sh ~/git/CBL-Mariner/imageconfigs/baremetal.json $INTERMEDIATE_ARTIFACTS_DIR

# ~/temp/iso-intermediates/host-configuration.yaml
cp ~/git/CBL-Mariner/toolkit/mic-iso-gen/files/host-configuration.yaml $INTERMEDIATE_ARTIFACTS_DIR

# ~/temp/iso-output
./toolkit/mic-iso-gen/2-create-iso.sh \
    $INTERMEDIATE_ARTIFACTS_DIR/iso-initrd.img \
    $INTERMEDIATE_ARTIFACTS_DIR/vmlinuz \
    ~/git/CBL-Mariner/toolkit/mic-iso-gen/files/grub.cfg \
    $INTERMEDIATE_ARTIFACTS_DIR/disk0.raw \
    $INTERMEDIATE_ARTIFACTS_DIR/host-configuration.yaml \
    ~/temp/iso-output
```