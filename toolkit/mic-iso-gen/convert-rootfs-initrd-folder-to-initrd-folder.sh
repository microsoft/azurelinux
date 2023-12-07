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

function copy_devices() {
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

modprobe xen-scsifront
modprobe xen-blkfront
modprobe xen-acpi-processor
modprobe xen-evtchn
modprobe xen-gntalloc
modprobe xen-gntdev
modprobe xen-privcmd
modprobe xen-pciback
modprobe xenfs
modprobe hv_sock
modprobe virtio_blk
modprobe virtio-rng
modprobe virtio_console
modprobe virtio_crypto
modprobe virtio_mem
modprobe vmw_vsock_virtio_transport
modprobe vmw_vsock_virtio_transport_common
modprobe 9pnet_virtio
modprobe vrf

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
#
# patch dracut script file to have delays and echo check points for debugging.
# this does not seem to help much.
#
# cp ~/git/CBL-Mariner/toolkit/mic-iso-gen/files/dracut-patch/dracut-lib.sh $outputRootDir/usr/lib/
# cp ~/git/CBL-Mariner/toolkit/mic-iso-gen/files/dracut-patch/dracut-cmdline  $outputRootDir/usr/bin/
# cp ~/git/CBL-Mariner/toolkit/mic-iso-gen/files/dracut-patch/initqueue $outputRootDir/usr/sbin/
#
# copying dracut files does not seem to have any effect.
# cp -r ~/temp/baremetal-minimal-iso/extracted/usr/lib64/dracut $outputRootDir/usr/lib64/
#
# uncommenting the following line causes the boot process to abort very early with
# an error about a missing system call. Most likely systemd binaries got copied without
# their dependencies.
#
# cp -r ~/temp/baremetal-minimal-iso/extracted/usr/lib64/systemd $outputRootDir/usr/lib64/
#
# create_init_script $outputRootDir
# remove_systemd $outputRootDir
copy_devices $outputRootDir
copy_binaries $outputRootDir
