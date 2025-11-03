#! /bin/sh
#
# Wrapper script for mysql_config to support multilib
#
# This command respects setarch

bits=$(rpm --eval %__isa_bits)

case $bits in
    32|64) status=known ;;
        *) status=unknown ;;
esac

if [ "$status" = "unknown" ] ; then
    echo "$0: error: command 'rpm --eval %__isa_bits' returned unknown value: $bits"
    exit 1
fi


if [ -x @bindir@/mysql_config-$bits ] ; then
    @bindir@/mysql_config-$bits "$@"
else
    echo "$0: error: needed binary: @bindir@/mysql_config-$bits is missing"
    exit 1
fi

