#!/bin/sh

/usr/lib/rpm/perl.req $* | grep -v "Authen::Smb"
