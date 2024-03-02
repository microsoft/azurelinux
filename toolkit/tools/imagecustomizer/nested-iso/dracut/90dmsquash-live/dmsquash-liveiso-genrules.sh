#!/bin/sh

echo "------ dmsquash-liveiso-genrules.sh ----- 1 -----" > /dev/kmsg
sleep 5s

if [ "${root%%:*}" = "liveiso" ]; then
    echo "------ dmsquash-liveiso-genrules.sh ----- 2 ----- /sbin/losetup -f --show ${root#liveiso:}" > /dev/kmsg
    sleep 5s
    {
        # printf 'ls -la > /dev/kmsg\n'
        # printf 'find / -name %s > /dev/kmsg\n' "${root#liveiso:}"
        # shellcheck disable=SC2016
        # printf 'KERNEL=="loop-control", RUN+="/sbin/initqueue --settled --onetime --unique /sbin/dmsquash-live-root `/sbin/losetup -f --show %s`"\n' \
        #    "${root#liveiso:}"
        printf 'KERNEL=="loop-control", RUN+="/sbin/initqueue --settled --onetime --unique /sbin/dmsquash-live-root /dev/sr0"\n'
    } >> /etc/udev/rules.d/99-liveiso-mount.rules
    echo "------ dmsquash-liveiso-genrules.sh ----- 3 ----- /sbin/losetup -f --show ${root#liveiso:}" > /dev/kmsg
    cat /etc/udev/rules.d/99-liveiso-mount.rules > /dev/kmsg
    echo "------ dmsquash-liveiso-genrules.sh ----- 4 ----- /sbin/losetup -f --show ${root#liveiso:}" > /dev/kmsg
    sleep 5s
fi
