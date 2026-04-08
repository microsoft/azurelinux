#!/bin/sh

/usr/lib/rpm/find-requires "$@" | grep -v 'perl(\(GD\|MRP::BaseClass\|Net::SNMP\))'
