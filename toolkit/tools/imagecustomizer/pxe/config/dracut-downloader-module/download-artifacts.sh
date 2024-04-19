#!/bin/bash

set -e
set -x

echo "Hello from the dracut downloader module script!"

# ---- constants

urlArgumentName=url
urlArgumentValue=
downloadFolder=/run/initramfs/downloaded-artifacts
downloadFileName=test.txt

# ---- functions

downloadFilePath=$downloadFolder/$downloadFileName

function setUrlFromKernelCmdLine() {

    cmdline=$(cat /proc/cmdline)

    if [[ $cmdline == *"$urlArgumentName"* ]]; then
        urlArgumentValue=$(echo "$cmdline" | grep -oE "\b$urlArgumentName=[^[:space:]]+" | cut -d= -f2)
        echo "Kernel parameter $urlArgumentName is set to $urlArgumentValue"
    else
        echo "Kernel parameter $urlArgumentName is not set"
    fi
}

# ---- main ----

# read configuration from grub.cfg
setUrlFromKernelCmdLine

# verify network connectivity
systemctl status systemd-networkd
sleep 2s

ip a
sleep 2s

ip link set dev eth0 up
sleep 2s

ip a
sleep 2s

# use configuration to write file
mkdir -p $downloadFolder
echo "Testing: $urlArgumentValue" > $downloadFilePath