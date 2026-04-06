#!/bin/sh

/usr/lib/rpm/find-provides "$@" | grep -v 'perl(\(SNMP_util\|SNMP_Session\|BER\|SNMPv1_Session\|SNMPv2c_Session\))'
exit 0
