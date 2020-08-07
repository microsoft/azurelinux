#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

if [[ -z "$LFS" ]]; then
    echo "Must define LFS in environment" 1>&2
    exit 1
fi
echo LFS root is: $LFS

# Change temp tools to root ownership
chown -R root:root $LFS/tools

# build jdk before mknod and other toolchain changes
sh /tools/toolchain-jdk8-build.sh 2>&1 | tee $LFS/logs/openjdk8.log

mkdir -pv $LFS/{dev,proc,sys,run}
mknod -m 600 $LFS/dev/console c 5 1
mknod -m 666 $LFS/dev/null c 1 3
mount -v --bind /dev $LFS/dev
mount -vt devpts devpts $LFS/dev/pts -o gid=5,mode=620
mount -vt proc proc $LFS/proc
mount -vt sysfs sysfs $LFS/sys
mount -vt tmpfs tmpfs $LFS/run

# Fix /dev/shm
if [ -h $LFS/dev/shm ]; then
  mkdir -pv $LFS/$(readlink $LFS/dev/shm)
fi

echo Root folder before entering chroot
ls -la /

# Enter the chroot environment
chroot "$LFS" /tools/bin/env -i \
    HOME=/root \
    TERM="$TERM" \
    PS1='\u:\w\$ ' \
    PATH=/bin:/usr/bin:/sbin:/usr/sbin:/tools/bin \
    LFS="$LFS" \
    LC_ALL="$LC_ALL" \
    LFS_TGT="$LFS_TGT" \
    /tools/bin/bash --login +h \
    -c "sh /tools/toolchain_build_in_chroot.sh"

sh /tools/unmount_chroot.sh