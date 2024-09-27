#!/bin/bash

# set -x
set -e

if [ -z "$1" ]; then
    echo "Must provide the name of the iso image file."
    exit 1
fi

scriptPath=$(realpath ${BASH_SOURCE[0]})
scriptDir=$(dirname "$scriptPath")

sourceIsoPath=$1
mount_dir=/mnt/$(basename $sourceIsoPath)

# ---- constants ----

# required arguments
tftpbootLocalDir="/var/lib/tftpboot"
httpLocalDir="/etc/httpd/marineros"
httpRoot="http://192.168.0.1/marineros"
isoRelativePath=liveos/

# ---- helper functions ----

function clean_tftp_folder() {
    rm -rf $tftpbootLocalDir/boot
    rm -rf $tftpbootLocalDir/liveos
    rm -f  $tftpbootLocalDir/bootx64.efi
    rm -f  $tftpbootLocalDir/grubx64.efi
}

function clean_http_folder() {
    rm -rf $httpLocalDir/liveos
}

function copy_file () {
    local source_file=$1
    local target_file=$2
    cp $source_file $target_file
    chmod 755 $target_file
    chown root:root $target_file
}

function deploy_tftp_folder() {
    local isoRelativePath=$1

    copy_file $mount_dir/efi/boot/grubx64.efi $tftpbootLocalDir/grubx64.efi
    copy_file $mount_dir/efi/boot/bootx64.efi $tftpbootLocalDir/bootx64.efi

    mkdir -p $tftpbootLocalDir/boot
    copy_file $mount_dir/boot/vmlinuz $tftpbootLocalDir/boot/vmlinuz
    copy_file $mount_dir/boot/initrd.img $tftpbootLocalDir/boot/initrd.img

    mkdir -p $tftpbootLocalDir/boot/grub2
    copy_file $mount_dir/boot/grub2/grub-pxe.cfg $tftpbootLocalDir/boot/grub2/grub.cfg

    sed -i 's/iso-publish-path/192.168.0.1\/marineros\/liveos/g' $tftpbootLocalDir/boot/grub2/grub.cfg
}

function deploy_http_folder() {
    local isoRelativePath=$1
    mkdir -p $httpLocalDir/liveos
    chmod 755 $httpLocalDir/liveos
    copy_file $sourceIsoPath $httpLocalDir/$isoRelativePath/$(basename $sourceIsoPath)
}

function clean() {
    clean_tftp_folder
    clean_http_folder
}

function deploy() {
    sudo rm -rf $mount_dir
    sudo mkdir -p $mount_dir
    sudo mount $sourceIsoPath $mount_dir

    deploy_http_folder $isoRelativePath
    deploy_tftp_folder $isoRelativePath
    systemctl restart httpd

    sudo umount $mount_dir
    sudo rm -r $mount_dir
}

# ---- main ----

clean
deploy

iptables -P INPUT ACCEPT
iptables -P OUTPUT ACCEPT
iptables -P FORWARD ACCEPT

sudo find $tftpbootLocalDir -type f
sudo find $httpLocalDir -type f
