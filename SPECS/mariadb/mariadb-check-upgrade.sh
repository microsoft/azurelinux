#!/bin/sh

source "`dirname ${BASH_SOURCE[0]}`/mariadb-scripts-common"

upgrade_info_file="$datadir/mysql_upgrade_info"
version=0
# get version as integer from mysql_upgrade_info file
if [ -f "$upgrade_info_file" ] && [ -r "$upgrade_info_file" ] ; then
    version_major=$(cat "$upgrade_info_file" | head -n 1 | sed -e 's/\([0-9]*\)\.\([0-9]*\)\..*$/\1/')
    version_minor=$(cat "$upgrade_info_file" | head -n 1 | sed -e 's/\([0-9]*\)\.\([0-9]*\)\..*$/\2/')
    if [[ $version_major =~ ^[0-9]+$ ]] && [[ $version_minor =~ ^[0-9]+$ ]] ; then
        version=$((version_major*100+version_minor))
    fi
fi

# compute current version as integer
thisversion=$((@MAJOR_VERSION@*100+@MINOR_VERSION@))

# provide warning in cases we should run mysql_upgrade
if [ $version -ne $thisversion ] ; then

    # give extra warning if some version seems to be skipped
    if [ $version -gt 0 ] && [ $version -lt 505 ] ; then
        echo "The datadir located at $datadir seems to be older than of a version 5.5. Please, mind that as a general rule, to upgrade from one release series to another, go to the next series rather than skipping a series." >&2
    fi

    cat <<EOF >&2
The datadir located at $datadir needs to be upgraded using 'mariadb-upgrade' tool. This can be done using the following steps:

  1. Back-up your data before with 'mariadb-upgrade'
  2. Start the database daemon using 'systemctl start @DAEMON_NAME@.service'
  3. Run 'mariadb-upgrade' with a database user that has sufficient privileges

Read more about 'mariadb-upgrade' usage at:
https://mariadb.com/kb/en/mysql_upgrade/
EOF
fi

exit 0
