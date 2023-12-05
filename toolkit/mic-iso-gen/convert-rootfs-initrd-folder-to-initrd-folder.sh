#!/bin/bash

set -x
set -e

inputRootDir=$1
outputRootDir=$2

function remove_systemd() {
    local outputRootDir=$1

    sudo rm -r $outputRootDir/etc/systemd
    sudo rm -r $outputRootDir/usr/lib/systemd

    sudo rm -r $outputRootDir/usr/bin/systemd-ask-password
    sudo rm -r $outputRootDir/usr/bin/systemd-escape
    sudo rm -r $outputRootDir/usr/bin/systemd-tty-ask-password-agent
    sudo rm -r $outputRootDir/usr/bin/systemd-tmpfiles
    sudo rm -r $outputRootDir/usr/bin/systemd-cgls
    sudo rm -r $outputRootDir/usr/bin/systemd-run
    sudo rm -r $outputRootDir/usr/lib/libsystemd.so.0.33.0
    sudo rm -r $outputRootDir/usr/lib/modprobe.d/systemd.conf
    sudo rm -r $outputRootDir/usr/lib/libnss_systemd.so.2
    sudo rm -r $outputRootDir/usr/lib/libsystemd.so.0
    sudo rm -r $outputRootDir/usr/lib/tmpfiles.d/systemd.conf
    sudo rm -r $outputRootDir/usr/lib/libsystemd.so
    sudo rm -r $outputRootDir/usr/lib/udev/rules.d/99-systemd.rules
    sudo rm -r $outputRootDir/etc/conf.d/systemd.conf
}

function copy_devics() {
    local outputRootDir=$1

    # pkggen/worker/create_worker_chroot.sh

    # sudo cp -a /dev/console $outputRootDir/dev
    # sudo cp -a /dev/ramdisk $outputRootDir/dev # doesn't exist
    # sudo cp -a /dev/ram0 $outputRootDir/dev  # doesn't exist
    # sudo cp -a /dev/null $outputRootDir/dev
    sudo cp -a /dev/tty1 $outputRootDir/dev
    sudo cp -a /dev/tty2 $outputRootDir/dev

    sudo mknod -m 600 $outputRootDir/dev/console c 5 1
    sudo mknod -m 666 $outputRootDir/dev/null c 1 3
    sudo mknod -m 444 $outputRootDir/dev/urandom c 1 9    
}

function create_init_script() {
    local outputRootDir=$1

    ls -la $outputRootDir/init
    sudo rm $outputRootDir/init

    cat >> $outputRootDir/init << EOF
#!/usr/bin/bash
set -x
export TERMINFO=/usr/share/terminfo
export TERM=linux
echo "------------ 0 ------------"
mount -t proc /proc /proc
echo "------------ 1 ------------"
mount -t sysfs none /sys
echo "------------ 4 ------------"
mount
echo "------------ 7 ------------"
modprobe pci-hyperv-intf
modprobe pci-hyperv
modprobe hv_storvsc
modprobe hyperv-keyboard
modprobe hid-hyperv
modprobe scsi_transport_fc
modprobe hv_netvsc
modprobe crc32c-intel
modprobe hv_balloon
modprobe hv_utils
modprobe hv_vmbus
modprobe virtiofs
modprobe fuse
modprobe configfs
modprobe autofs4
echo "------------ 8 ------------"
lsmod
echo "------------ 2 ------------"
ls /dev
echo "------------ 6 ------------"
blkid
echo "------------ 9 ------------"
lsblk -o NAME,FSTYPE,SIZE,MOUNTPOINT,LABEL,UUID,PARTLABEL,PARTUUID
echo "------------ 10 ------------"
mkdir -p /mnt/cdrom
mount /dev/sr0 /mnt/cdrom
ls -la /mnt/cdrom
echo "------------ 11 ------------"
/usr/bin/bash --verbose
EOF

    chmod +x $outputRootDir/init
}

function add_start_up_script() {
    cp /home/george/git/CBL-Mariner/toolkit/mic-iso-gen/files/prov/mariner-iso-start-up-minimal.sh \
        $outputRootDir

    pushd $outputRootDir
    cat $outputRootDir/etc/passwd
    patch -p0 -i /home/george/git/CBL-Mariner/toolkit/mic-iso-gen/rootfs-initrd-etc-passwd.patch
    popd
}

function copy_binaries() {
    local outputRootDir=$1

    cp ~/temp/iso-build/intermediates/extract-artifacts-from-rootfs-out-dir/extracted-rootfs/usr/bin/lsblk \
        $outputRootDir/usr/bin/
}

# --- - main --- -

sudo rm -rf $outputRootDir
mkdir -p $outputRootDir
sudo cp -r -a $inputRootDir/* $outputRootDir

add_start_up_script $outputRootDir
create_init_script $outputRootDir
remove_systemd $outputRootDir
copy_devics $outputRootDir
copy_binaries $outputRootDir
