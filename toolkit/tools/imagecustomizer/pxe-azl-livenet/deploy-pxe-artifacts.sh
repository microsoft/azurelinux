#!/bin/bash

set -x
set -e

if [ -z "$1" ]; then
    echo "Must provide the name of the iso image file."
    exit 1
fi

scriptPath=$(realpath ${BASH_SOURCE[0]})
scriptDir=$(dirname "$scriptPath")

sourcePath=$1

# ---- constants ----

tftpLocalDir="/var/lib/tftpboot"
httpLocalDir="/etc/httpd/marineros"
httpRootPlaceHolder="iso-publish-path"
httpRoot="192.168.0.1/marineros/liveos"
isoRelativePath=liveos/

# ---- helper functions ----

function mount_iso() {
    local isoPath=$1
    local mountDir=$2
    sudo rm -rf $mountDir
    sudo mkdir -p $mountDir
    sudo mount $isoPath $mountDir
}

function unmount_iso() {
    local mountDir=$1    
    sudo umount $mountDir
    sudo rm -r $mountDir
}

function clean_tftp_folder() {
    rm -rf $tftpLocalDir/boot
    rm -rf $tftpLocalDir/liveos
    rm -f  $tftpLocalDir/bootx64.efi
    rm -f  $tftpLocalDir/grubx64.efi
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
    local artifactsRootDir=$1
    local tftpLocalDir=$2

    copy_file $artifactsRootDir/efi/boot/grubx64.efi $tftpLocalDir/grubx64.efi
    copy_file $artifactsRootDir/efi/boot/bootx64.efi $tftpLocalDir/bootx64.efi

    mkdir -p $tftpLocalDir/boot
    copy_file $artifactsRootDir/boot/vmlinuz $tftpLocalDir/boot/vmlinuz
    copy_file $artifactsRootDir/boot/initrd.img $tftpLocalDir/boot/initrd.img

    mkdir -p $tftpLocalDir/boot/grub2
    if [[ -f $artifactsRootDir/boot/grub2/grub-pxe.cfg ]]; then
        copy_file $artifactsRootDir/boot/grub2/grub-pxe.cfg $tftpLocalDir/boot/grub2/grub.cfg
    else
        copy_file $artifactsRootDir/boot/grub2/grub.cfg $tftpLocalDir/boot/grub2/grub.cfg
    fi
    copy_file $artifactsRootDir/boot/grub2/grubenv $tftpLocalDir/boot/grub2/grubenv    

    # replace every '/' with a '\/' to avoid breaking sed search/replace syntax.
    escapedHttpRoot=${httpRoot//\//\\\/}
    set -x
    sed -i "s/$httpRootPlaceHolder/$escapedHttpRoot/g" $tftpLocalDir/boot/grub2/grub.cfg
    set +x
}

function deploy_http_folder() {
    local sourceIsoPath=$1
    local isoRelativePath=$2
    local httpLocalDir=$3

    mkdir -p $httpLocalDir/liveos
    chmod 755 $httpLocalDir/liveos
    copy_file $sourceIsoPath $httpLocalDir/$isoRelativePath/$(basename $sourceIsoPath)
}

function deploy() {
    local artifactsRootDir=$1
    local sourceIsoPath=$2

    deploy_http_folder $sourceIsoPath $isoRelativePath $httpLocalDir
    deploy_tftp_folder $artifactsRootDir $tftpLocalDir
    systemctl restart httpd
}

function clean() {
    clean_tftp_folder
    clean_http_folder
}

function list_deployed_files() {
    sudo find $tftpLocalDir -type f
    sudo find $httpLocalDir -type f
}

# ---- main ----

clean

# if sourcePath is a file, we assume it's the path to the iso image.
if [[ -f "$sourcePath" ]]; then
    isoMountDir=/mnt/$(basename $sourcePath)
    sourceIsoPath=$sourcePath

    mount_iso $sourceIsoPath $isoMountDir
    deploy $isoMountDir $sourceIsoPath
    # unmount_iso $isoMountDir

elif [[ -d "$sourcePath" ]]; then

    sourceIsoPath=$(find "$sourcePath" -name "*.iso")
    deploy $sourcePath $sourceIsoPath
fi

# todo: open only what's necessary
iptables -P INPUT ACCEPT
iptables -P OUTPUT ACCEPT
iptables -P FORWARD ACCEPT

list_deployed_files
