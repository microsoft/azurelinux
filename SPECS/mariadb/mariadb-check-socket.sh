#!/bin/sh

# We check if there is already a process using the socket file,
# since otherwise the systemd service file could report false
# positive result when starting and mysqld_safe could remove
# a socket file, which is actually being used by a different daemon.

source "`dirname ${BASH_SOURCE[0]}`/mariadb-scripts-common"

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
    response=`@bindir@/mariadb-admin --no-defaults --socket="$socketfile" --user=UNKNOWN_MYSQL_USER --connect-timeout="${CHECKSOCKETTIMEOUT:-10}" ping 2>&1`
    if [ $? -eq 0 ] || echo "$response" | grep -q "Access denied for user" ; then
        echo "Is another MariaDB daemon already running with the same unix socket?" >&2
        echo "Please, stop the process using the socket $socketfile or remove the file manually to start the service." >&2
        exit 1
    fi

    # socket file is a garbage
    echo "No process is using $socketfile, which means it is a garbage, so it will be removed automatically." >&2
fi

exit 0
