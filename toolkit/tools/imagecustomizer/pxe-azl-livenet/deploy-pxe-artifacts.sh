#!/bin/bash

set -x
set -e

if [ -z "$1" ]; then
    echo "Must provide the name of the iso image file."
    exit 1
fi

scriptPath=$(realpath ${BASH_SOURCE[0]})
scriptDir=$(dirname "$scriptPath")

sourceIsoPath=$1
mount_dir=/mnt/$(basename $sourceIsoPath)

tftpboot_dir=/var/lib/tftpboot
http_dir=/etc/httpd/marineros

function clean_tftp_folder() {
    rm -rf $tftpboot_dir/boot
    rm -rf $tftpboot_dir/liveos
    rm -f  $tftpboot_dir/bootx64.efi
    rm -f  $tftpboot_dir/grubx64.efi
}

function clean_http_folder() {
    rm -rf $http_dir/liveos
}

function copy_file () {
    local source_file=$1
    local target_file=$2
    cp $source_file $target_file
    chmod 755 $target_file
    chown root:root $target_file
}

function createPxeGrubCfg() {
    local pxeGrubCfg=$1

    cat <<EOF > $pxeGrubCfg
set timeout=0
set bootprefix=/boot

menuentry "CBL-Mariner" {
        linux /boot/vmlinuz \\
                ip=dhcp \\
                root=live:http://192.168.0.1/marineros/liveos/azure-linux.iso \\
                rd.auto=1 \\
                console=tty0 console=ttyS0 \\
                sysctl.kernel.unprivileged_bpf_disabled=1 \\
                rd.info \\
                log_buf_len=1M \\
                rd.shell \\
                rd.live.image \\
                rd.live.dir=liveos \\
                rd.live.squashimg=rootfs.img \\
                rd.live.overlay=1 \\
                rd.live.overlay.nouserconfirmprompt

        initrd /boot/initrd.img
}
EOF

    chmod 755 $pxeGrubCfg
    chown root:root $pxeGrubCfg
}

function deploy_tftp_folder() {
    copy_file $mount_dir/efi/boot/grubx64.efi $tftpboot_dir/grubx64.efi
    copy_file $mount_dir/efi/boot/bootx64.efi $tftpboot_dir/bootx64.efi

    mkdir -p $tftpboot_dir/boot
    copy_file $mount_dir/boot/vmlinuz $tftpboot_dir/boot/vmlinuz
    copy_file $mount_dir/boot/initrd.img $tftpboot_dir/boot/initrd.img

    mkdir -p $tftpboot_dir/boot/grub2
    copy_file $mount_dir/boot/grub2/efiboot.img $tftpboot_dir/boot/grub2/efiboot.img
    # copy_file $mount_dir/boot/grub2/grub.cfg $tftpboot_dir/boot/grub2/grub.cfg
    createPxeGrubCfg $tftpboot_dir/boot/grub2/grub.cfg
}

function deploy_http_folder() {
    mkdir -p $http_dir/liveos
    chmod 755 $http_dir/liveos
    # copy_file $mount_dir/liveos/rootfs.img $http_dir/liveos/rootfs.img
    copy_file $sourceIsoPath $http_dir/liveos/azure-linux.iso
}

function clean() {
    clean_tftp_folder
    clean_http_folder
}

function deploy() {
    sudo rm -rf $mount_dir
    sudo mkdir -p $mount_dir
    sudo mount $sourceIsoPath $mount_dir

    deploy_tftp_folder
    deploy_http_folder
    systemctl restart httpd

    sudo umount $mount_dir
    sudo rm -r $mount_dir
}

# ---- main ----

clean
deploy
