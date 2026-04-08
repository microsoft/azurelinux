#!/bin/sh

# This script creates the mysql data directory during first service start.
# In subsequent starts, it does nothing much.
#
# This script is meant to be run as non-root user either during initscript
# or systemd service execution, before starting the mysqld daemon.
# Running it as root may have some security risks, because it touches files
# that can be symlinks pointing to unexpected locations.
#
# On the other hand, when using non-standard locations for datadir and logfile,
# this script might not be able to create the files and the daemon won't start
# properly. A solution for that is to created the locations for datadir and
# logfile with correct ownership before starting the daemon.

source "`dirname ${BASH_SOURCE[0]}`/mysql-scripts-common"

# If two args given first is user, second is group
# otherwise the arg is the systemd service file
if [ "$#" -eq 2 ]
then
    myuser="$1"
    mygroup="$2"
else
    # Absorb configuration settings from the specified systemd service file,
    # or the default service if not specified
    SERVICE_NAME="$1"
    if [ x"$SERVICE_NAME" = x ]
    then
        SERVICE_NAME=@DAEMON_NAME@.service
    fi

    myuser=`systemctl show -p User "${SERVICE_NAME}" |
      sed 's/^User=//'`
    if [ x"$myuser" = x ]
    then
        myuser=mysql
    fi

    mygroup=`systemctl show -p Group "${SERVICE_NAME}" |
      sed 's/^Group=//'`
    if [ x"$mygroup" = x ]
    then
        mygroup=mysql
    fi
fi

# Set up the errlogfile with appropriate permissions
if [ ! -e "$errlogfile" -a ! -h "$errlogfile" -a x$(dirname "$errlogfile") = "x/var/log" ]; then
    case $(basename "$errlogfile") in
        mysql*.log|mariadb*.log) install /dev/null -m0640 -o$myuser -g$mygroup "$errlogfile" ;;
        *) ;;
    esac
else
    # Provide some advice if the log file cannot be created by this script
    errlogdir=$(dirname "$errlogfile")
    if ! [ -d "$errlogdir" ] ; then
        echo "The directory $errlogdir does not exist."
        exit 1
    elif [ -e "$errlogfile" -a ! -w "$errlogfile" ] ; then
        echo "The log file $errlogfile cannot be written, please, fix its permissions."
        echo "The daemon will be run under $myuser:$mygroup"
        exit 1
    fi
fi



export LC_ALL=C

# Returns content of the specified directory
# If listing files fails, fake-file is returned so which means
# we'll behave like there was some data initialized
# Some files or directories are fine to be there, so those are
# explicitly removed from the listing
# @param <dir> datadir
list_datadir ()
{
    ( ls -1A "$1" 2>/dev/null || echo "fake-file" ) | grep -v \
    -e '^lost+found$' \
    -e '\.err$' \
    -e '^\.bash_history$'
}

# Checks whether datadir should be initialized
# @param <dir> datadir
should_initialize ()
{
    test -z "$(list_datadir "$1")"
}

# Make the data directory if doesn't exist or empty
if should_initialize "$datadir" ; then

    # Now create the database
    echo "Initializing @NICE_PROJECT_NAME@ database"
    @libexecdir@/mysqld --initialize-insecure --datadir="$datadir" --user="$myuser"
    ret=$?
    if [ $ret -ne 0 ] ; then
        echo "Initialization of @NICE_PROJECT_NAME@ database failed." >&2
        echo "Perhaps @sysconfdir@/my.cnf is misconfigured." >&2
        # Clean up any partially-created database files
        if [ ! -e "$datadir/mysql/user.frm" ] ; then
            rm -rf "$datadir"/*
        fi
        exit $ret
    fi
    # upgrade does not need to be run on a fresh datadir
    echo "@VERSION@" >"$datadir/mysql_upgrade_info"
fi

exit 0
