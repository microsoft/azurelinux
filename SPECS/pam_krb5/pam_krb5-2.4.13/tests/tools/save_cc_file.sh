#!/bin/sh
ccin=`echo "$KRB5CCNAME" | cut -f2- -d:`
cp -v "$ccin" "$CCSAVE"
