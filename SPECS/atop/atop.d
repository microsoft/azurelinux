#!/bin/bash

# load sysconfig atop

[ -f /etc/sysconfig/atop ] && . /etc/sysconfig/atop
# Current Day format
[ -z $CURDAY ] && CURDAY=`date +%Y%m%d`
# Log files path
[ -z $LOGPATH ] && LOGPATH=/var/log/atop
# Binaries path
[ -z $BINPATH ] && BINPATH=/usr/bin
# PID File
[ -z $PIDFILE ] && PIDFILE=/var/run/atop.pid
# interval (default 10 minutes)
[ -z $INTERVAL ] && INTERVAL=600


start_atop() {
# start atop for all processes with interval of $INTERVAL 
# (by default 10) minutes
$BINPATH/atop -a -w $LOGPATH/atop_$CURDAY $INTERVAL > $LOGPATH/atop.log 2>&1 &
echo $! > $PIDFILE
}

# verify if atop still runs for daily logging
#
if [ -f $PIDFILE ]; then
	PID=`cat $PIDFILE`
	if [ -s $PIDFILE ] && ps -p $PID | grep 'atop$' > /dev/null
	then
	        kill -USR1 $PID       # take final sample
	        sleep 3
	        kill -TERM $PID
	        rm $PIDFILE
	        sleep 1
	else
	        exit 1
	fi
fi
start_atop 
exit 0
