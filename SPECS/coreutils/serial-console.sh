#
# Copyright (C) 2018 VMware Inc.
# Author: Alexey Makhalov <amakhalov@vmware.com>
#
# Copyright (C) 2024 Microsoft Corporation
# Author: Dan Streetman <ddstreet@microsoft.com>
#
# Correctly set tty rows/cols for serial ports where the kernel does
# not support NAWS. This is a simpler version of what the xterm-based
# 'resize' program does. If the serial port client terminal window is
# resized, this (or the 'resize' command) will need to be re-run.
#

case $( tty ) in
    /dev/ttyS*|/dev/ttyUSB*|/dev/ttyAMA*|/dev/ttyXRUSB*)
        # This will only work if both stdin and stdout are opened on a terminal
        [[ -t 0 && -t 1 ]] || break

        # terminfo 'save cursor'
        tput sc

        # set cursor pos to (0-based) row,col
        tput cup 998 998

        # Cursor Position Request (CPR)
        echo -ne '\e[6n'

        # read CPR (format is: '\e[' rows ';' cols 'R')
        read -sd '['
        read -sd ';' rows
        read -sd 'R' cols

        # terminfo 'restore cursor'
        tput rc

        if [[ "$( stty size )" != "${rows} ${cols}" ]]; then
            stty rows ${rows} cols ${cols}
        fi
        ;;
esac

