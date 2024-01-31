#!/bin/bash -eu

if [ $UID -ne 0 ]; then
    echo "WARNING: This script needs to run as root to be effective"
    exit 1
fi

export SYSTEMD_NSS_BYPASS_SYNTHETIC=1

if [ "${1:-}" = "--ignore-journal" ]; then
    shift
    ignore_journal=1
else
    ignore_journal=0
fi

echo "Checking processes..."
if ps h -u 99 | grep .; then
    echo "ERROR: ps reports processes with UID 99!"
    exit 2
fi
echo "... not found"

echo "Checking UTMP..."
if w -h 199 | grep . ; then
    echo "ERROR: w reports UID 99 as active!"
    exit 2
fi
if w -h nobody | grep . ; then
    echo "ERROR: w reports user nobody as active!"
    exit 2
fi
echo "... not found"

echo "Checking the journal..."
if [ "$ignore_journal" = 0 ] && journalctl -q -b -n10 _UID=99 | grep . ; then
    echo "ERROR: journalctl reports messages from UID 99 in current boot!"
    exit 2
fi
echo "... not found"

echo "Looking for files in /etc, /run, /tmp, and /var..."
if find /etc /run /tmp /var -uid 99 -print | grep -m 10 . ; then
    echo "ERROR: found files belonging to UID 99"
    exit 2
fi
echo "... not found"

echo "Checking if nobody is defined correctly..."
if getent passwd nobody |
	grep '^nobody:[x*]:65534:65534:.*:/:/sbin/nologin';
then
    echo "OK, nothing to do."
    exit 0
else
    echo "NOTICE: User nobody is not defined correctly"
fi

echo "Checking if nfsnobody or something else is using the uid..."
if getent passwd 65534 | grep . ; then
    echo "NOTICE: will have to remove this user"
else
    echo "... not found"
fi

if [ "${1:-}" = "-x" ]; then
    if getent passwd nobody >/dev/null; then
	# this will remove both the user and the group.
	( set -x
   	  userdel nobody
	)
    fi

    if getent passwd 65534 >/dev/null; then
	# Make sure the uid is unused. This should free gid too.
	name="$(getent passwd 65534 | cut -d: -f1)"
	( set -x
	  userdel "$name"
	)
    fi

    if grep -qE '^(passwd|group):.*\bsss\b' /etc/nsswitch.conf; then
	echo "Sleeping, so sss can catch up"
	sleep 3
    fi

    if getent group 65534; then
	# Make sure the gid is unused, even if uid wasn't.
	name="$(getent group 65534 | cut -d: -f1)"
	( set -x
	  groupdel "$name"
	)
    fi

    # systemd-sysusers uses the same gid and uid
    ( set -x
      systemd-sysusers --inline 'u nobody 65534 "Kernel Overflow User" / /sbin/nologin'
    )
else
    echo "Pass '-x' to perform changes"
fi
