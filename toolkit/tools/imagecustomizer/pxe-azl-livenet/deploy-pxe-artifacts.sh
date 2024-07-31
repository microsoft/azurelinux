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
isoRelativePath=liveos/azure-linux.iso
# optional arguments
hostScriptRelativePath=liveos/host-script.sh
hostConfigRelativePath=liveos/host-config.cfg

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

function createPxeGrubCfg() {
    local pxeGrubCfg=$1
    local isoRelativePath=$2
    local hostScriptRelativePath=$3
    local hostConfigRelativePath=$4

    if [[ -z $httpRoot ]]; then
        echo "error: failed to create grub.cfg. An http root path must be specified."
        exit 1
    fi

    if [[ -z $isoRelativePath ]]; then
        echo "error: failed to create grub.cfg. An iso relative path must be specified."
        exit 1
    fi

    rdRoot="root=live:$httpRoot/$isoRelativePath"

    if [[ -n $hostScriptRelativePath ]]; then
        rdHostScript="rd.host.script=live:$httpRoot/$hostScriptRelativePath"
    fi

    if [[ -n $hostConfigRelativePath ]]; then
        rdHostConfig="rd.host.config=live:$httpRoot/$hostConfigRelativePath"
    fi

    cat <<EOF > $pxeGrubCfg
set timeout=10
set bootprefix=/boot
set debug=all

menuentry "CBL-Mariner" {
        linux /boot/vmlinuz \\
                ip=dhcp \\
                $rdRoot \\
                $rdHostScript \\
                $rdHostConfig \\
                rd.auto=1 \\
                selinux=0 security= \\
                console=tty0 console=ttyS0 \\
                sysctl.kernel.unprivileged_bpf_disabled=1 \\
                rd.info \\
                log_buf_len=1M \\
                rd.shell \\
                rd.live.image \\
                rd.live.dir=liveos \\
                rd.live.squashimg=rootfs.img \\
                rd.live.overlay=1 \\
                rd.live.overlay.overlayfs \\
                rd.live.overlay.nouserconfirmprompt

        initrd /boot/initrd.img
}
EOF

    chmod 755 $pxeGrubCfg
    chown root:root $pxeGrubCfg
}

function createPxeHostCfg() {
    local pxeHostConfig=$1

    cat <<EOF > $pxeHostConfig
hostname=pxetestclient
configserver=http://192.168.0.1
EOF

    chmod 644 $pxeHostConfig
    chown root:root $pxeHostConfig
}

function createPxeHostScript() {
    local pxeHostScript=$1

    cat <<EOF > $pxeHostScript
#!/bin/bash
# set -x
set -e    
echo "executing pre-pivote user script with (\$1)" > /dev/kmsg

filename=\$1
if [[ -n "\$filename" ]]; then
    while IFS='=' read -r key value; do
    # Skip empty lines
    [ -z "\$key" ] && continue

    # Process the key and value
    echo "Key: \$key" > /dev/kmsg
    echo "Value: \$value" > /dev/kmsg
    done < "\$filename"
fi
EOF

    chmod 755 $pxeHostScript
    chown root:root $pxeHostScript
}

function deploy_tftp_folder() {
    local isoRelativePath=$1
    local hostScriptRelativePath=$2
    local hostConfigRelativePath=$3

    copy_file $mount_dir/efi/boot/grubx64.efi $tftpbootLocalDir/grubx64.efi
    copy_file $mount_dir/efi/boot/bootx64.efi $tftpbootLocalDir/bootx64.efi

    mkdir -p $tftpbootLocalDir/boot
    copy_file $mount_dir/boot/vmlinuz $tftpbootLocalDir/boot/vmlinuz
    copy_file $mount_dir/boot/initrd.img $tftpbootLocalDir/boot/initrd.img

    mkdir -p $tftpbootLocalDir/boot/grub2
    #
    # this file is only needed for the iso
    # copy_file $mount_dir/boot/grub2/efiboot.img $tftpbootLocalDir/boot/grub2/efiboot.img
    #

    # copy_file $mount_dir/boot/grub2/grub.cfg $tftpbootLocalDir/boot/grub2/grub.cfg
    createPxeGrubCfg \
        $tftpbootLocalDir/boot/grub2/grub.cfg \
        $isoRelativePath \
        $hostScriptRelativePath \
        $hostConfigRelativePath
}

function deploy_http_folder() {
    local isoRelativePath=$1
    local hostScriptRelativePath=$2
    local hostConfigRelativePath=$3
    mkdir -p $httpLocalDir/liveos
    chmod 755 $httpLocalDir/liveos
    # copy_file $mount_dir/liveos/rootfs.img $httpLocalDir/liveos/rootfs.img
    copy_file $sourceIsoPath $httpLocalDir/$isoRelativePath
    if [[ -n $hostScriptRelativePath ]]; then
        createPxeHostScript $httpLocalDir/$hostScriptRelativePath
    fi
    if [[ -n $hostConfigRelativePath ]]; then
        createPxeHostCfg $httpLocalDir/$hostConfigRelativePath
    fi
}

function clean() {
    clean_tftp_folder
    clean_http_folder
}

function deploy() {
    sudo rm -rf $mount_dir
    sudo mkdir -p $mount_dir
    sudo mount $sourceIsoPath $mount_dir

    deploy_http_folder $isoRelativePath $hostScriptRelativePath $hostConfigRelativePath
    deploy_tftp_folder $isoRelativePath $hostScriptRelativePath $hostConfigRelativePath
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