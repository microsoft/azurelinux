#!/bin/bash

SERVERFILE=$SAVEDIR/chrony.servers.$interface

chrony_config() {
	rm -f "$SERVERFILE"
	if [ "$PEERNTP" != "no" ]; then
		for server in $new_ntp_servers; do
			echo "$server ${NTPSERVERARGS:-iburst}" >> "$SERVERFILE"
		done
		/usr/libexec/chrony-helper update-daemon || :
	fi
}

chrony_restore() {
	if [ -f "$SERVERFILE" ]; then
		rm -f "$SERVERFILE"
		/usr/libexec/chrony-helper update-daemon || :
	fi
}
