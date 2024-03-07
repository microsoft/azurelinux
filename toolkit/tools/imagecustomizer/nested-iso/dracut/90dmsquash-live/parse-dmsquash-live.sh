#!/bin/sh
# live images are specified with
# root=live:backingdev

echo "------ parse-dmsquash-live.sh ----- 1 -----"
echo "------ parse-dmsquash-live.sh ----- 1 /dev/kmsg -----" > /dev/kmsg
sleep 1s

[ -z "$root" ] && root=$(getarg root=)

# support legacy syntax of passing liveimg and then just the base root
if getargbool 0 rd.live.image -d -y liveimg; then
    liveroot="live:$root"
fi

echo "------ parse-dmsquash-live.sh ----- 2 /dev/kmsg root=$root -----" > /dev/kmsg
sleep 1s

if [ "${root%%:*}" = "live" ]; then
    liveroot=$root
fi

echo "------ parse-dmsquash-live.sh ----- 3 /dev/kmsg liveroot=$liveroot -----" > /dev/kmsg
sleep 1s

[ "${liveroot%%:*}" = "live" ] || return 1

echo "------ parse-dmsquash-live.sh ----- 4 -----" > /dev/kmsg
sleep 1s

modprobe -q loop


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
        echo "------ parse-dmsquash-live.sh ----- 5 -----" > /dev/kmsg
        imageFileName=${root#live:}
        echo "------ parse-dmsquash-live.sh ----- 6 imageFileName=$imageFileName -----" > /dev/kmsg
        pwd  > /dev/kmsg
        ls -la  > /dev/kmsg
        if [ -f "${root#live:}" ]; then
            echo "------ parse-dmsquash-live.sh ----- 6 imageFileName=$imageFileName is present -----" > /dev/kmsg
        else
            echo "------ parse-dmsquash-live.sh ----- 6 imageFileName=$imageFileName is NOT present -----" > /dev/kmsg
        fi
        sleep 1s
        working start
        root="${root#live:}"
        root="liveiso:${root}"
        rootok=1
        ;;
        # working end
        # not working start
        # [ -f "${root#live:}" ] && rootok=1
        # ;;
        # not working end
esac

echo "------ parse-dmsquash-live.sh ----- 10 -----" > /dev/kmsg
sleep 1s

[ "$rootok" = "1" ] || return 1

echo "------ parse-dmsquash-live.sh ----- 11 -----" > /dev/kmsg
sleep 1s

info "root was $liveroot, is now $root"

echo "------ parse-dmsquash-live.sh ----- 12 -----" > /dev/kmsg
sleep 1s

# make sure that init doesn't complain
[ -z "$root" ] && root="live"

echo "------ parse-dmsquash-live.sh ----- 13 -----" > /dev/kmsg
wait_for_dev -n /dev/root

echo "------ parse-dmsquash-live.sh ----- 14 -----" > /dev/kmsg
sleep 2s

return 0
