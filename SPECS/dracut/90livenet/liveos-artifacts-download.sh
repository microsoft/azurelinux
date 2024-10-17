#!/bin/bash

# This script retrieves the value of the 'root' kernel parameter and checks
# whether it is either 'live:http://' or 'http://' and points to an ISO image.
# If so, it downloads the ISO image, creates a loop device, and calls
# dmsquash-live to proceed with mounting the rootfs and pivoting.
#
# The ISO image to download must be a liveos ISO (i.e. uses Dracut's
# dmsquash-live module internally to boot and pivot to an embedded root file
# system).

echo "executing liveos-artifacts-download.sh" > /dev/kmsg

. /usr/lib/dracut-lib.sh
root=$(getarg root -d "")

downloadedArtifactsDirs=/run/initramfs/downloaded-artifacts

set -e

function isSupportedProtocol() {
    local kernelParamValue=$1

    case "$kernelParamValue" in
        live:http://* | http://*)
            # remove `live:` if it exists
            urlValue="${kernelParamValue#live:}"
            ;;
    esac

    echo $urlValue
}

function downloadArtifact () {
    local paramValueNoLive=$1

    IFS=';'
    read -ra valueParts <<< "$paramValueNoLive"
    IFS=$' \t\n'

    sourceUrl=${valueParts[0]}
    targetDir=
    targetPath=
    arrayLength=${#valueParts[@]}
    if (( arrayLength > 1 )); then
        targetPath=${valueParts[1]}
    else
        targetPath=$downloadedArtifactsDirs/${sourceUrl##*/}
    fi
    targetDir="${targetPath%/*}"

    mkdir -p $targetDir
    httpRetCode=$(curl $sourceUrl -o $targetPath -w "%{http_code}\n")
    if [ $httpRetCode -ne 200 ]; then
        echo "error: failed to download $sourceUrl" > /dev/kmsg
        exit 0
    fi

    echo $targetPath
}

# is protocol supported?
isoUrl=$(isSupportedProtocol "$root")
if [[ -z "$isoUrl" ]]; then
    echo "error: root URL value is set to a non-supported network protocol ($root). Supported protocols: http" > /dev/kmsg
    exit 0
fi

# is artifact an iso image?
isoUrlArtifactExtension=${isoUrl##*.}
if [[ "$isoUrlArtifactExtension" != "iso" ]]; then
    echo "error: root URL value is set to a non-supported image type ($isoUrl). Supported image types: iso" > /dev/kmsg
    exit 0
fi

# download iso image
localIsoPath=$(downloadArtifact "$isoUrl")
if [[ "$localIsoPath" == "error:"* ]]; then
    echo "error: failed to download ($isoUrl)" > /dev/kmsg
    exit 1
fi

# create a loopback device and prepare rootfs
rootDevice=$(losetup -f --show $localIsoPath)

# set dracut environment
export fstype="auto"
export DRACUT_SYSTEMD=1

# let dmsquash-live-root handle the mounting as before
/usr/sbin/dmsquash-live-root $rootDevice
