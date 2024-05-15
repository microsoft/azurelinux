#!/bin/bash

set -x

echo "executing liveos-artifacts-download.sh"

type getarg > /dev/null 2>&1 || . /usr/lib/dracut-lib.sh
root=$(getarg root -d unknown)

set -e

case "$root" in
    live:http://* | http://*)
        # remove `live:` if it exists
        rootUrl="${root#live:}"
        ;;
    live:https://* | https://*)
        # remove `live:` if it exists
        rootUrl="${root#live:}"
        ;;
esac

[ -z "$rootUrl" ] && exit 0

rootImageDir=/run/initramfs/downloaded-artifacts
rootImageFile=${rootUrl##*/}
rootImagePath=$rootImageDir/$rootImageFile

# download
mkdir -p $rootImageDir
curl $rootUrl -o $rootImagePath

# create a loopback device
rootDevice=$(losetup -f --show $rootImagePath)

# see: c:\temp\dracut\modules.d\98dracut-systemd\dracut-cmdline.sh
# if ! root="$(getarg root=)"; then
#     root_unset='UNSET'
# fi
# rflags="$(getarg rootflags=)"
# fstype="$(getarg rootfstype=)"
export fstype="auto"
export DRACUT_SYSTEMD=1
/usr/sbin/dmsquash-live-root $rootDevice