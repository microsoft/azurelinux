#!/bin/sh

source "`dirname ${BASH_SOURCE[0]}`/mysql-scripts-common"

# This script waits for mysqld to be properly stopped
# (which can be many seconds in some large load).
# Running this as ExecStopPost is useful so that starting which is done
# as part of restart doesn't see the former process still running.

# Wait for the server to properly end the main server
ret=0
TIMEOUT=60
SECONDS=0

if ! [ -f "$pidfile" ]; then
	exit 0
fi

MYSQLPID=`cat "$pidfile" 2>/dev/null`
if [ -z "$MYSQLPID" ] ; then
	exit 2
fi

while /bin/true; do
	# Check process still exists
	if ! [ -d "/proc/${MYSQLPID}" ] ; then
	    break
	fi
	if [ $SECONDS -gt $TIMEOUT ] ; then
	    ret=3
	    break
	fi
	sleep 1
done

exit $ret
