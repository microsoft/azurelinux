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
    RDSOSREPORT="$(rdsosreport)"
    source_hook "$hook"
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
    [ -f /etc/profile ] && . /etc/profile
    [ -z "$PS1" ] && export PS1="$_name:\${PWD}# "
    # exec sulogin -e
    /bin/bash
else
    export hook="shutdown-emergency"
    warn "$action has failed. To debug this issue add \"rd.shell rd.debug\" to the kernel command line."
    source_hook "$hook"
    [ -z "$_emergency_action" ] && _emergency_action=halt
fi

/bin/rm -f -- /.console_lock

case "$_emergency_action" in
    reboot)
        reboot || exit 1
        ;;
    poweroff)
        poweroff || exit 1
        ;;
    halt)
        halt || exit 1
        ;;
esac

exit 0
