#!/bin/bash
if [ -f /etc/sysconfig/squid ]; then
	. /etc/sysconfig/squid
fi

SQUID_CONF=${SQUID_CONF:-"/etc/squid/squid.conf"}

CACHE_SWAP=`awk '/^[[:blank:]]*cache_dir/ { print $3 }' "$SQUID_CONF"`

init_cache_dirs=0
for adir in $CACHE_SWAP; do
	if [ ! -d $adir/00 ]; then
		echo -n "init_cache_dir $adir... "
		init_cache_dirs=1
	fi
done

if [ $init_cache_dirs -ne 0 ]; then
	echo ""
	squid --foreground -z -f "$SQUID_CONF" >> /var/log/squid/squid.out 2>&1
fi
