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

    sudo cp -a /dev/console $outputRootDir/dev
    # sudo cp -a /dev/ramdisk $outputRootDir/dev
    # sudo cp -a /dev/ram0 $outputRootDir/dev
    sudo cp -a /dev/null $outputRootDir/dev
    sudo cp -a /dev/tty1 $outputRootDir/dev
    sudo cp -a /dev/tty2 $outputRootDir/dev
}

function create_init_script() {
    local outputRootDir=$1

    ls -la $outputRootDir/init
    sudo rm $outputRootDir/init

    cat >> $outputRootDir/init << EOF
#!/usr/bin/bash
export TERMINFO=/usr/lib/mariner/terminfo
export TERM=mariner-installer
echo
echo "Simple initrd is active"
echo
mount -t proc /proc /proc
mount -t sysfs none /sys
/usr/bin/bash
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

# ---- main ----

sudo rm -rf $outputRootDir
mkdir -p $outputRootDir
sudo cp -r -a $inputRootDir/* $outputRootDir

add_start_up_script $outputRootDir
create_init_script $outputRootDir
remove_systemd $outputRootDir
copy_devics $outputRootDir

