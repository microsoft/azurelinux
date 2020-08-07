#
# Copyright (C) 2018 VMware Inc.
# Author: Alexey Makhalov <amakhalov@vmware.com>
#
# Expand screen terminal to the full screen mode.
# Known side effect: screen might be "garbaged" by reply string.

full_screen () {
	if [[ -t 0 ]] && [[ -t 1 ]]; then
		# s - save cursor position
		# [r;cH - set cursor position to r;c
		# [6n - get cursor position
		# u - restore cursor position
		#
		# reply from terminal: [r;cR
		echo -ne '\es\e[999;999H\e[6n\eu'
		read -sd '['
		read -sd ';' rows
		read -sd 'R' cols
		if [[ "$( stty size )" != "${rows} ${cols}" ]] ; then
			stty rows ${rows} cols ${cols}
		fi
	fi
}


case $( tty ) in
	/dev/ttyS*|/dev/ttyUSB*|/dev/ttyAMA*|/dev/ttyXRUSB*)
		export TERM=screen
		full_screen
		;;
esac

