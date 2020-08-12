#!/bin/sh

SRC_FILE_MB=$1

while true
do
    DD_PID=`pidof dd`
    if [ -n "$DD_PID" ]; then
        break
    fi
done

while true
do
    sleep 5
    if [ ! -d /proc/$DD_PID ]; then
        break
    fi

    kill -s USR1 $DD_PID
    CURRENT_SIZE=`tail -n 1 /tmp/dd_progress_file | sed "s/[^0-9].*//g"`
    [ -n "$CURRENT_SIZE" ] && {
        CURRENT_MB=$(($CURRENT_SIZE / 1048576))
        echo -e "Copied $CURRENT_MB MB / $SRC_FILE_MB MB\r"
    }
done

rm -f /tmp/dd_progress_file
