#!/bin/sh
sleep 10
if test -s "$@" ; then
	exec grep -q starting "$*" 2> /dev/null
else
	exit 0
fi
