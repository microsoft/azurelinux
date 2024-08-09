#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

if [[ -z "$LFS" ]]; then
    echo "Must define LFS in environment" 1>&2
    exit 1
fi
echo LFS root is: $LFS

# 7.2. Changing Ownership
# Change temp tools to root ownership
chown -R root:root $LFS/{usr,lib,var,etc,bin,sbin,tools}
case $(uname -m) in
  x86_64) chown -R root:root $LFS/lib64 ;;
esac

# 7.3. Preparing Virtual Kernel File Systems
mkdir -pv $LFS/{dev,proc,sys,run}
mknod -m 600 $LFS/dev/console c 5 1
mknod -m 666 $LFS/dev/null c 1 3
mount -v --bind /dev $LFS/dev
mount -vt devpts devpts $LFS/dev/pts -o gid=5,mode=620
#mount -v --bind /dev/pts $LFS/dev/pts
mount -vt proc proc $LFS/proc
mount -vt sysfs sysfs $LFS/sys
mount -vt tmpfs tmpfs $LFS/run
# Fix /dev/shm
if [ -h $LFS/dev/shm ]; then
  mkdir -pv $LFS/$(readlink $LFS/dev/shm)
else
  mount -t tmpfs -o nosuid,nodev tmpfs $LFS/dev/shm
fi

echo Root folder before entering chroot
ls -la /

# Enter the chroot environment
chroot "$LFS" /usr/bin/env -i   \
    HOME=/root                  \
    TERM="$TERM"                \
    PS1='\u:\w\$ '              \
    PATH=/usr/bin:/usr/sbin     \
    LFS="$LFS"                  \
    LC_ALL="$LC_ALL"            \
    LFS_TGT="$LFS_TGT"          \
    /bin/bash --login +h        \
    -c "sh /tools/toolchain_build_in_chroot.sh"

sh /tools/unmount_chroot.sh
