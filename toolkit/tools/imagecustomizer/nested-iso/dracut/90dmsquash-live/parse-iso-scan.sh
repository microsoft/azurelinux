#!/bin/sh
# live images are specified with
# root=live:backingdev

echo "------ parse-iso-scan.sh ----- 1 -----"
echo "------ parse-iso-scan.sh ----- 1 /dev/kmsg -----" > /dev/kmsg
sleep 2s

isofile=$(getarg iso-scan/filename)

echo "------ parse-iso-scan.sh ----- 2 /dev/kmsg ----- $isofile" > /dev/kmsg
sleep 2s

if [ -n "$isofile" ]; then
    echo "------ parse-iso-scan.sh ----- 3 /dev/kmsg ----- $isofile" > /dev/kmsg
    sleep 2s

    /sbin/initqueue --settled --unique /sbin/iso-scan "$isofile"

    exitCode=$?

    echo "------ parse-iso-scan.sh ----- 4 /dev/kmsg ----- exitCode=$exitCode - $isofile" > /dev/kmsg
    ls -la /lib/dracut/hooks/initqueue/settled > /dev/kmsg
    echo "------ parse-iso-scan.sh ----- 5 /dev/kmsg ----- $isofile" > /dev/kmsg
    sleep 8s
fi
