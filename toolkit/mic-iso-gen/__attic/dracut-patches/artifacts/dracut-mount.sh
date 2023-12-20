#!/bin/sh

echo "---- dracut-mount.sh ---- welcome to mount script ----"
# sleep 1s

export DRACUT_SYSTEMD=1
if [ -f /dracut-state.sh ]; then
    . /dracut-state.sh 2> /dev/null
fi
type getarg > /dev/null 2>&1 || . /lib/dracut-lib.sh

source_conf /etc/conf.d

make_trace_mem "hook mount" '1:shortmem' '2+:mem' '3+:slab'

echo "---- dracut-mount.sh ---- 1 ----"
# sleep 1s

getarg 'rd.break=mount' -d 'rdbreak=mount' && emergency_shell -n mount "Break mount"
# mount scripts actually try to mount the root filesystem, and may
# be sourced any number of times. As soon as one suceeds, no more are sourced.
i=0
while :; do

    echo "---- dracut-mount.sh ---- 2 ----"
    # sleep 1s

    if ismounted "$NEWROOT"; then
        usable_root "$NEWROOT" && break
        umount "$NEWROOT"
    fi

    echo "---- dracut-mount.sh ---- 3 ----"
    # sleep 1

    for f in "$hookdir"/mount/*.sh; do

        echo "---- dracut-mount.sh ---- 4 ----"
        # sleep 1s

        # shellcheck disable=SC1090
        [ -f "$f" ] && . "$f"
        if ismounted "$NEWROOT"; then

            echo "---- dracut-mount.sh ---- 5 ----"
            # sleep 1s

            usable_root "$NEWROOT" && break
            warn "$NEWROOT has no proper rootfs layout, ignoring and removing offending mount hook"
            umount "$NEWROOT"
            rm -f -- "$f"
        fi
    done

    echo "---- dracut-mount.sh ---- 6 ----"
    # sleep 1s

    i=$((i + 1))
    [ $i -gt 5 ] && emergency_shell "Can't mount root filesystem"

    echo "---- dracut-mount.sh ---- 7 ----"
    # sleep 1s

done

echo "---- dracut-mount.sh ---- 8 ----"
# sleep 1s

export -p > /dracut-state.sh

echo "---- dracut-mount.sh ---- 9 ----"
# sleep 1s

exit 0
