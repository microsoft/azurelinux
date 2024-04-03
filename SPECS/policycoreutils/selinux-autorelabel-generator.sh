#!/bin/bash
# This systemd.generator(7) detects if SELinux is running and if the
# user requested an autorelabel, and if so sets the default target to
# selinux-autorelabel.target, which will cause the filesystem to be
# relabelled and then the system will reboot again and boot into the
# real default target.

PATH=/usr/sbin:$PATH
unitdir=/usr/lib/systemd/system

# If invoked with no arguments (for testing) write to /tmp.
earlydir="/tmp"
if [ -n "$2" ]; then
    earlydir="$2"
fi

set_target ()
{
    ln -sf "$unitdir/selinux-autorelabel.target" "$earlydir/default.target"
    AUTORELABEL="1"
    source /etc/selinux/config
    if [ "$AUTORELABEL" = "0" ]; then
        mkdir -p "$earlydir/selinux-autorelabel.service.d"
        cat > "$earlydir/selinux-autorelabel.service.d/tty.conf" <<EOF
[Service]
StandardInput=tty
EOF
    fi
}

if selinuxenabled; then
    if test -f /.autorelabel; then
        set_target
    elif grep -sqE "\bautorelabel\b" /proc/cmdline; then
        set_target
    fi
fi