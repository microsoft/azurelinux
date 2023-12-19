#!/bin/bash

set -x
set -e

function install_pkgs() {

    sudo cat > /etc/resolv.conf <<EOF
nameserver 127.0.0.53
options edns0 trust-ad
search .
EOF

    sudo chmod 777 /etc/resolv.conf
    sudo cat /etc/resolv.conf
    sudo tdnf install squashfs-tools
}

# fails because it is unable to get pgp files.
# work around is to include it in source image definition.
# install_pkgs

kernelVersion=$(ls /usr/lib/modules)
echo "kernelVersion=$kernelVersion"

sudo dracut /initrd.img \
    --kver $kernelVersion \
    --filesystems "squashfs" \
    --include /usr/bin/more /usr/sbin/more \
    --include /usr/bin/vim /usr/sbin/vim \
    --include /usr/bin/lsblk /usr/sbin/lsblk \
    --include /usr/bin/grep /usr/bin/grep