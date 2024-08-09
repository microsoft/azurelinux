#!/bin/sh

/usr/lib/rpm/perl.req $* | grep -v "Net::Telnet"
