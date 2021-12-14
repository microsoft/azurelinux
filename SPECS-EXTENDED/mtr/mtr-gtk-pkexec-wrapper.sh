#!/bin/sh

error_message="You are trying to run mtr-gtk in a Wayland session, however mtr-gtk requires root privileges and such graphical applications are not allowed to run on Wayland by default.\n\nSee https://fedoraproject.org/wiki/Common_F25_bugs\#wayland-root-apps for more details and possible workarounds.\n"

if [ "$XDG_SESSION_TYPE" = wayland ]; then
    zenity --error --title "mtr-gtk on Wayland" --text "$error_message" --width=600 2>/dev/null || printf "$error_message" >&2
    exit 1
fi

/usr/bin/pkexec /usr/bin/xmtr.bin
