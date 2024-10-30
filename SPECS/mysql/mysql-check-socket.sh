#!/bin/sh

# We check if there is already a process using the socket file,
# since otherwise the systemd service file could report false
# positive result when starting and mysqld_safe could remove
# a socket file, which is actually being used by a different daemon.

source "`dirname ${BASH_SOURCE[0]}`/mysql-scripts-common"

if test -e "$socketfile" ; then
    echo "Socket file $socketfile exists." >&2

    # no write permissions
    if ! test -w "$socketfile" ; then
        echo "Not enough permission to write to the socket file $socketfile, which is suspicious." >&2
        echo "Please, remove $socketfile manually to start the service." >&2
        exit 1
    fi

    # not a socket file
    if ! test -S "$socketfile" ; then
        echo "The file $socketfile is not a socket file, which is suspicious." >&2
        echo "Please, remove $socketfile manually to start the service." >&2
        exit 1
    fi

    # some process uses the socket file
    if fuser "$socketfile" &>/dev/null ; then
        socketpid=$(fuser "$socketfile" 2>/dev/null)
        echo "Is another MySQL daemon already running with the same unix socket?" >&2
        echo "Please, stop the process $socketpid or remove $socketfile manually to start the service." >&2
        exit 1
    fi

    # socket file is a garbage
    echo "No process is using $socketfile, which means it is a garbage, so it will be removed automatically." >&2
fi

exit 0
