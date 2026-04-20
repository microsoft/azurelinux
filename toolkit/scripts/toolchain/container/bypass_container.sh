#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -x
set -e

. .bashrc
export PATH=$LFS/tools/bin:$PATH

mkdir -pv $LFS/sources
chmod -v a+wt $LFS/sources
mkdir -pv $LFS/logs/temptoolchain
mkdir -pv $LFS/tools

cp version-check-container.sh toolchain-sha256sums toolchain-remote-wget-list toolchain-local-wget-list toolchain_build_temp_tools.sh sanity_check.sh CVE-2023-4039.patch rpm-define-RPM-LD-FLAGS.patch toolchain_initial_chroot_setup.sh toolchain_build_in_chroot.sh mount_chroot_start_build.sh unmount_chroot.sh $LFS/tools

$LFS/tools/version-check-container.sh

pushd $LFS/sources

wget -nv --no-clobber --timeout=30 --continue --input-file=$LFS/tools/toolchain-local-wget-list --directory-prefix=$LFS/sources || true
# need to skip this if it already exists because it inexplicably turns kernel-6.6.96.2.tar.gz into a 0-byte file
[ -f kernel-6.6.96.2.tar.gz ] || wget -nv --no-clobber --timeout=30 --continue https://github.com/microsoft/CBL-Mariner-Linux-Kernel/archive/rolling-lts/mariner-3/6.6.96.2.tar.gz -O kernel-6.6.96.2.tar.gz --directory-prefix=$LFS/sources || true

mkdir -pv $LFS/{etc,var} $LFS/usr/{bin,lib,sbin}
[ -L $LFS/bin ] || ln -sv usr/bin $LFS/bin
[ -L $LFS/lib ] || ln -sv usr/lib $LFS/lib
[ -L $LFS/sbin ] || ln -sv usr/sbin $LFS/sbin
mkdir -pv $LFS/lib64
mkdir -pv $LFS/usr/share

sha256sum -c $LFS/tools/toolchain-sha256sums
# groupadd lfs
# useradd -s /bin/bash -g lfs -m -k /dev/null lfs
# usermod -a -G sudo lfs
# echo "lfs ALL = NOPASSWD : ALL" >> /etc/sudoers
# echo 'Defaults env_keep += "LFS LC_ALL LFS_TGT PATH MAKEFLAGS FETCH_TOOLCHAIN_MODE LFS_TEST LFS_DOCS JOB_COUNT LOOP IMAGE_SIZE INITRD_TREE IMAGE"' >> /etc/sudoers
chown -Rv lfs $LFS/usr
chown -Rv lfs $LFS/{usr{,/*},lib,var,etc,bin,sbin,tools}
chown -v lfs $LFS/lib64
chown -v lfs $LFS/sources
chown -Rv lfs $LFS/logs

popd
echo "exec env -i HOME=$HOME TERM=$TERM PS1='\u:\w\$ ' /bin/bash" >> /home/lfs/.bash_profile
cp .bashrc /home/lfs/
chown -Rv lfs $LFS/tools
chown -Rv lfs $LFS/usr
chown -Rv lfs:lfs /home/lfs/

sudo --preserve-env=PATH -u lfs $LFS/tools/toolchain_build_temp_tools.sh

$LFS/tools/mount_chroot_start_build.sh
