# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Currently assumes you have already run busybox_cross.sh, kernel_cross.sh, and generate_minimal_rootfs.sh

# Kernel should be located at /opt/cross/kernel
# Rootfs should be located as a cpio.gz in /opt/cross/rootfs

installDir="/opt/cross"
kernelStandaloneInstallDir=${installDir}/kernel
standaloneRootfsDir=${installDir}/rootfs
kernelVersion="5.15.48.1"

# Note: Current rootfs unpacks to be fairly big. 2GB memory was not enough size to hold the unpacked initramfs
# so when QEMU ran, it would fail with:
#
# [   16.532507] ---[ end Kernel panic - not syncing: VFS: Unable to mount root fs on unknown-block(0,0) ]---
#
# But this is a lie - the true error is immediately after the unpacking initramfs message:
#
# [    0.321246] Unpacking initramfs...
# [   15.549898] Initramfs unpacking failed: write error
#
# 4GB can hold the current rootfs. But tweak the -m parameter as necessary.
qemu-system-aarch64 \
    -M virt \
    -cpu cortex-a57 \
    -machine type=virt \
    -smp 1 \
    -m 4096 \
    -kernel ${kernelStandaloneInstallDir}/vmlinuz-${kernelVersion} \
    -initrd ${standaloneRootfsDir}/rootfs.cpio.gz \
    -nographic \
    -append "console=ttyAMA0"
