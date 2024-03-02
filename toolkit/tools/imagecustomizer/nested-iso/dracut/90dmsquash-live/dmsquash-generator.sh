#!/bin/bash

type getarg > /dev/null 2>&1 || . /lib/dracut-lib.sh

[ -z "$root" ] && root=$(getarg root=)

# support legacy syntax of passing liveimg and then just the base root
if getargbool 0 rd.live.image -d -y liveimg; then
    liveroot="live:$root"
fi

echo "------ dmsquash-generator.sh ----- 1 -----" > /dev/kmsg
echo "------ dmsquash-generator.sh ----- 2 -----" > /dev/kmsg
echo "------ dmsquash-generator.sh 2.1 root= $root" > /dev/kmsg 
echo "------ dmsquash-generator.sh 2.2 liveroot= $liveroot" > /dev/kmsg 
# sleep 5s

if [ "${root%%:*}" = "live" ]; then
    liveroot=$root
fi

echo "------ dmsquash-generator.sh ----- 3 -----" > /dev/kmsg
echo "------ dmsquash-generator.sh 3.1 root= $root" > /dev/kmsg 
echo "------ dmsquash-generator.sh 3.2 liveroot= $liveroot" > /dev/kmsg 
# sleep 2s

[ "${liveroot%%:*}" = "live" ] || exit 0

echo "------ dmsquash-generator.sh ----- 4 -----" > /dev/kmsg
# sleep 2s

case "$liveroot" in
    live:LABEL=* | LABEL=* | live:UUID=* | UUID=* | live:PARTUUID=* | PARTUUID=* | live:PARTLABEL=* | PARTLABEL=*)
        root="live:$(label_uuid_to_dev "${root#live:}")"
        rootok=1
        ;;
    live:CDLABEL=* | CDLABEL=*)
        root="${root#live:}"
        root="$(echo "$root" | sed 's,/,\\x2f,g;s, ,\\x20,g')"
        root="live:/dev/disk/by-label/${root#CDLABEL=}"
        rootok=1
        ;;
    live:/*.[Ii][Ss][Oo] | /*.[Ii][Ss][Oo])
        root="${root#live:}"
        root="liveiso:${root}"
        rootok=1
        ;;
    live:/dev/*)
        rootok=1
        ;;
    live:/*.[Ii][Mm][Gg] | /*.[Ii][Mm][Gg])
        echo "------ dmsquash-generator.sh ----- 5 -----" > /dev/kmsg
        # working start
        root="${root#live:}"
        root="liveiso:${root}"
        echo "------ dmsquash-generator.sh 5.1 root= $root" > /dev/kmsg 
        rootok=1
        # sleep 1s
        ;;
        # working end
        # not working start
        # [ -f "${root#live:}" ] && rootok=1
        # ;;
        # not working end
esac

echo "------ dmsquash-generator.sh 6 root= $root" > /dev/kmsg 
# sleep 1s

[ "$rootok" != "1" ] && exit 0

echo "------ dmsquash-generator.sh 7 root= $root" > /dev/kmsg 
# sleep 1s

GENERATOR_DIR="$2"
[ -z "$GENERATOR_DIR" ] && exit 1
[ -d "$GENERATOR_DIR" ] || mkdir -p "$GENERATOR_DIR"

getargbool 0 rd.live.overlay.readonly -d -y readonly_overlay && readonly_overlay="--readonly" || readonly_overlay=""
getargbool 0 rd.live.overlay.overlayfs && overlayfs="yes"
[ -e /xor_overlayfs ] && xor_overlayfs="yes"
[ -e /xor_readonly ] && xor_readonly="--readonly"
ROOTFLAGS="$(getarg rootflags)"
{
    echo "[Unit]"
    echo "Before=initrd-root-fs.target"
    echo "[Mount]"
    echo "Where=/sysroot"
    if [ "$overlayfs$xor_overlayfs" = "yes" ]; then
        echo "What=LiveOS_rootfs"
        if [ "$readonly_overlay$xor_readonly" = "--readonly" ]; then
            ovlfs=lowerdir=/run/overlayfs-r:/run/rootfsbase
        else
            ovlfs=lowerdir=/run/rootfsbase
        fi
        echo "Options=${ROOTFLAGS},${ovlfs},upperdir=/run/overlayfs,workdir=/run/ovlwork"
        echo "Type=overlay"
        _dev=LiveOS_rootfs
    else
        echo "What=/dev/mapper/live-rw"
        [ -n "$ROOTFLAGS" ] && echo "Options=${ROOTFLAGS}"
        _dev=$'dev-mapper-live\\x2drw'
    fi
} > "$GENERATOR_DIR"/sysroot.mount

echo "------ dmsquash-generator.sh 8 root= $root" > /dev/kmsg 
# sleep 1s

mkdir -p "$GENERATOR_DIR/$_dev.device.d"
{
    echo "[Unit]"
    echo "JobTimeoutSec=180"
    echo "JobRunningTimeoutSec=180"
} > "$GENERATOR_DIR/$_dev.device.d/timeout.conf"

echo "------ dmsquash-generator.sh 9 root= $root" > /dev/kmsg 
# sleep 1s
