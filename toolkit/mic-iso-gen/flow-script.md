# Flow Script

```bash
export INTERMEDIATE_ARTIFACTS_DIR=~/temp/iso-intermediates

sudo rm -rf $INTERMEDIATE_ARTIFACTS_DIR
mkdir -p $INTERMEDIATE_ARTIFACTS_DIR

./0-build-initrd.sh

# ~/temp/iso-intermediates/disk0.raw
./1-build-rootfs.sh ~/git/CBL-Mariner/imageconfigs/baremetal.json $INTERMEDIATE_ARTIFACTS_DIR

```