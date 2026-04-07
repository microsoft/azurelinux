#!/bin/bash

SPOOLDIR=/var/spool/exim

cd $SPOOLDIR/db
for a in retry misc wait-* callout ratelimit; do
    [ -r "$a" ] || continue
    [ "${a%%.lockfile}" = "$a" ] || continue
    /usr/sbin/exim_tidydb $SPOOLDIR $a >/dev/null
done
