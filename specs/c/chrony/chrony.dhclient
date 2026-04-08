#!/bin/bash

CHRONY_SOURCEDIR=/run/chrony-dhcp
SERVERFILE=$CHRONY_SOURCEDIR/$interface.sources

chrony_config() {
	# Disable modifications if called from a NM dispatcher script
	[ -n "$NM_DISPATCHER_ACTION" ] && return 0

	rm -f "$SERVERFILE"
	if [ "$PEERNTP" != "no" ]; then
		mkdir -p $CHRONY_SOURCEDIR
		for server in $new_ntp_servers; do
			echo "server $server ${NTPSERVERARGS:-iburst}" >> "$SERVERFILE"
		done
		/usr/bin/chronyc reload sources > /dev/null 2>&1 || :
	fi
}

chrony_restore() {
	[ -n "$NM_DISPATCHER_ACTION" ] && return 0

	if [ -f "$SERVERFILE" ]; then
		rm -f "$SERVERFILE"
		/usr/bin/chronyc reload sources > /dev/null 2>&1 || :
	fi
}
