# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Currently assumes you have already run busybox_cross.sh and kernel_cross.sh

toolchainTuple="aarch64-linux-gnu"
installDir="/opt/cross"
sysrootDir="/opt/cross/${toolchainTuple}/sysroot"
scriptDir="$( cd "$( dirname "$0" )" && pwd )"
standaloneRootfsDir=${installDir}/rootfs

sudo rm -rf ${standaloneRootfsDir}

mkdir -p ${standaloneRootfsDir}

# Create mountpoint directories in sysroot
# This step is not required for extremely barebones busybox systems
# but I have included it here since these are common mountpoints to have
#mkdir -p ${sysrootDir}/proc
#mkdir -p ${sysrootDir}/sys
#
# Then in your custom init script, do the following:
#mount -t proc none /proc
#mount -t sysfs none /sys

# Symlink busybox's /sbin/init to /init so QEMU runs it
ln -sf /sbin/init ${sysrootDir}/init

# Copy our custom busybox inittab over to sysroot/etc/inittab
cp ${scriptDir}/inittab ${sysrootDir}/etc

# Create gziped cpio archive so we can load this as an initramfs
cd ${sysrootDir}
find . -print0 | cpio --null -ov --format=newc | gzip -9 > ${standaloneRootfsDir}/rootfs.cpio.gz