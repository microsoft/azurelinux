#!/bin/bash

# set -x

echo "executing liveos-artifacts-download.sh - v0.1" > /dev/kmsg

. /usr/lib/dracut-lib.sh
root=$(getarg root -d "")
hostConfig=$(getarg rd.host.config -d "")
hostScript=$(getarg rd.host.script -d "")

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
    # echo "curl returned ($httpRetCode)" > /dev/kmsg
    if [ $httpRetCode -ne 200 ]; then
        echo "error: failed to download $sourceUrl" > /dev/kmsg
        exit 0
    fi

    echo $targetPath
}

#localIsoPath=$downloadedArtifactsDirs/${rootNoLive##*/}

# download

isoUrl=$(isSupportedProtocol "$root")
if [[ -z "$isoUrl" ]]; then
    # this is not a live iso url, there is nothing for us to do.
    echo "root is set to a non-live iso url ($root)" > /dev/kmsg
    exit 0
fi
localIsoPath=$(downloadArtifact "$isoUrl")
if [[ "$localIsoPath" == "error:"* ]]; then
    echo "failed to download ($isoUrl)" > /dev/kmsg
    exit 1
fi

hostConfigUrl=$(isSupportedProtocol "$hostConfig")
if [[ -n "$hostConfigUrl" ]]; then
    hostConfigPath=$(downloadArtifact "$hostConfigUrl")
    if [[ "$hostConfigPath" == "error:"* ]]; then
        echo "failed to download ($hostConfigUrl)" > /dev/kmsg
        exit 1
    fi
fi

hostScriptUrl=$(isSupportedProtocol "$hostScript")
if [[ -n "$hostScriptUrl" ]]; then
    hostScriptPath=$(downloadArtifact "$hostScriptUrl")
    if [[ "$hostScriptPath" == "error:"* ]]; then
        echo "failed to download ($hostScriptUrl)" > /dev/kmsg
        exit 1
    fi
fi

echo "localIsoPath   : $localIsoPath" > /dev/kmsg
echo "hostConfigPath : $hostConfigPath" > /dev/kmsg
echo "hostScriptPath : $hostScriptPath" > /dev/kmsg

# invoke custom script
if [[ -n "$hostScriptPath" ]]; then
    echo "launching $hostScriptPath" > /dev/kmsg
    chmod +x $hostScriptPath
    $hostScriptPath $hostConfigPath
fi

echo "launching dmsquash-live-root" > /dev/kmsg

# create a loopback device and prepare rootfs
rootDevice=$(losetup -f --show $localIsoPath)

# see: c:\temp\dracut\modules.d\98dracut-systemd\dracut-cmdline.sh
# if ! root="$(getarg root=)"; then
#     root_unset='UNSET'
# fi
# rflags="$(getarg rootflags=)"
# fstype="$(getarg rootfstype=)"
export fstype="auto"
export DRACUT_SYSTEMD=1
/usr/sbin/dmsquash-live-root $rootDevice
