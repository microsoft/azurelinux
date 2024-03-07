#!/bin/sh

echo "------ dmsquash-live-genrules.sh ----- 1 -----" > /dev/kmsg
sleep 5s


case "$root" in
    live:/dev/*)
        echo "------ dmsquash-live-genrules.sh ----- 2 -----" > /dev/kmsg
        sleep 5s

        {
            printf 'KERNEL=="%s", RUN+="/sbin/initqueue --settled --onetime --unique /sbin/dmsquash-live-root %s"\n' \
                "${root#live:/dev/}" "${root#live:}"
            printf 'SYMLINK=="%s", RUN+="/sbin/initqueue --settled --onetime --unique /sbin/dmsquash-live-root %s"\n' \
                "${root#live:/dev/}" "${root#live:}"
        } >> /etc/udev/rules.d/99-live-squash.rules
        wait_for_dev -n "${root#live:}"
        ;;
    live:*)
        echo "------ dmsquash-live-genrules.sh ----- 3 -----" > /dev/kmsg
        sleep 5s

        if [ -f "${root#live:}" ]; then
            /sbin/initqueue --settled --onetime --unique /sbin/dmsquash-live-root "${root#live:}"
        fi
        ;;
esac
