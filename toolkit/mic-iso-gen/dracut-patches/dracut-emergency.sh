#!/bin/sh

export DRACUT_SYSTEMD=1
if [ -f /dracut-state.sh ]; then
    . /dracut-state.sh 2> /dev/null
fi
type getarg > /dev/null 2>&1 || . /lib/dracut-lib.sh

source_conf /etc/conf.d

type plymouth > /dev/null 2>&1 && plymouth quit

export _rdshell_name="dracut" action="Boot" hook="emergency"
_emergency_action=$(getarg rd.emergency)

if getargbool 1 rd.shell -d -y rdshell || getarg rd.break -d rdbreak; then
    FSTXT="/run/dracut/fsck/fsck_help_$fstype.txt"
    echo "---- dracut-emergency.sh ---- 0 ----"
    sleep 1s

    RDSOSREPORT="$(rdsosreport)"
    echo "---- dracut-emergency.sh ---- 1 -----"
    sleep 1s

    source_hook "$hook"
    echo "---- dracut-emergency.sh ---- 2 -----"
    sleep 1s

    while read -r _tty rest; do
        (
            echo
            echo "$RDSOSREPORT"
            echo
            echo
            echo 'Entering emergency mode. Exit the shell to continue.'
            echo 'Type "journalctl" to view system logs.'
            echo 'You might want to save "/run/initramfs/rdsosreport.txt" to a USB stick or /boot'
            echo 'after mounting them and attach it to a bug report.'
            echo
            echo
            [ -f "$FSTXT" ] && cat "$FSTXT"
        ) > /dev/"$_tty"
    done < /proc/consoles

    echo "---- dracut-emergency.sh ---- 3 ----"
    sleep 1s

    [ -f /etc/profile ] && . /etc/profile
    [ -z "$PS1" ] && export PS1="$_name:\${PWD}# "

    echo "---- dracut-emergency.sh ---- 4 ----"
    sleep 1s

    exec sulogin -e

    echo "---- dracut-emergency.sh ---- 5 ----"
    sleep 1s

else
    export hook="shutdown-emergency"
    warn "$action has failed. To debug this issue add \"rd.shell rd.debug\" to the kernel command line."
    source_hook "$hook"
    [ -z "$_emergency_action" ] && _emergency_action=halt
fi

echo "---- dracut-emergency.sh ---- 6 ----"
sleep 1s

/bin/rm -f -- /.console_lock

echo "---- dracut-emergency.sh ---- 7 ----"
sleep 1s

case "$_emergency_action" in
    reboot)
        echo "---- dracut-emergency.sh ---- 8 -----"
        sleep 1s
        reboot || exit 1
        ;;
    poweroff)
        echo "---- dracut-emergency.sh ----- 9 -----"
        sleep 1s
        poweroff || exit 1
        ;;
    halt)
        echo "---- dracut-emergency.sh ----- 10 -----"
        sleep 1s
        halt || exit 1
        ;;
esac

echo "---- dracut-emergency.sh ---- 11 ----"
sleep 5s

exit 0
