#!/bin/sh

# This script creates the MariaDB data directory during first service start.
# In subsequent starts, it does nothing much.

source "`dirname ${BASH_SOURCE[0]}`/mariadb-scripts-common"

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
    -e '^.bash_history$'
}

# Checks whether datadir should be initialized
# @param <dir> datadir
should_initialize ()
{
    test -z "$(list_datadir "$1")"
}

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
        echo "The directory $errlogdir does not exist." >&2
        exit 1
    elif [ -e "$errlogfile" -a ! -w "$errlogfile" ] ; then
        echo "The log file $errlogfile cannot be written, please, fix its permissions." >&2
        echo "The daemon will be run under $myuser:$mygroup" >&2
        exit 1
    fi
fi

# Make the data directory if doesn't exist or empty
if should_initialize "$datadir" ; then
    # First, make sure $datadir is there with correct permissions
    # (note: if it's not, and we're not root, this'll fail ...)
    if [ ! -e "$datadir" -a ! -h "$datadir" ]
    then
        mkdir -p "$datadir" || exit 1
    fi
    chown "$myuser:$mygroup" "$datadir"
    chmod 0755 "$datadir"
    [ -x /sbin/restorecon ] && /sbin/restorecon "$datadir"

    # Now create the database
    echo "Initializing @NICE_PROJECT_NAME@ database" >&2
    # Avoiding deletion of files not created by mysql_install_db is
    # guarded by time check and sleep should help work-arounded
    # potential issues on systems with 1 second resolution timestamps
    # https://bugzilla.redhat.com/show_bug.cgi?id=1335849#c19
    INITDB_TIMESTAMP=`LANG=C date -u`
    sleep 1
    @bindir@/mariadb-install-db --rpm --datadir="$datadir" --user="$myuser" --skip-test-db >&2
    ret=$?
    if [ $ret -ne 0 ] ; then
        echo "Initialization of @NICE_PROJECT_NAME@ database failed." >&2
        echo "Perhaps @sysconfdir@/my.cnf is misconfigured or there is some problem with permissions of $datadir." >&2
        # Clean up any partially-created database files
        if [ ! -e "$datadir/mysql/user.frm" ] && [ -d "$datadir" ] ; then
            echo "Initialization of @NICE_PROJECT_NAME@ database was not finished successfully." >&2
            echo "Files created so far will be removed." >&2
            find "$datadir" -mindepth 1 -maxdepth 1 -newermt "$INITDB_TIMESTAMP" \
                 -not -name "lost+found" -exec rm -rf {} +
            if [ $? -ne 0 ] ; then
                echo "Removing of created files was not successfull." >&2
                echo "Please, clean directory $datadir manually." >&2
            fi
        else
            echo "However, part of data has been initialized and those will not be removed." >&2
            echo "Please, clean directory $datadir manually." >&2
        fi
        exit $ret
    fi
    # upgrade does not need to be run on a fresh datadir
    echo "@VERSION@-MariaDB" >"$datadir/mysql_upgrade_info"
else
    if [ -d "$datadir/mysql/" ] ; then
        # mysql dir exists, it seems data are initialized properly
        echo "Database @NICE_PROJECT_NAME@ is probably initialized in $datadir already, nothing is done."
        echo "If this is not the case, make sure the $datadir is empty before running `basename $0`."
    else
        # if the directory is not empty but mysql/ directory is missing, then
        # print error and let user to initialize manually or empty the directory
        echo "Database @NICE_PROJECT_NAME@ is not initialized, but the directory $datadir is not empty, so initialization cannot be done." >&2
        echo "Make sure the $datadir is empty before running `basename $0`." >&2
        exit 1
    fi
fi

exit 0
