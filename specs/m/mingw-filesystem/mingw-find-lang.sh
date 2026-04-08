#!/bin/bash

# Wrapper for the %find_lang macro which splits out the various translations in per-target lists

PACKAGE_NAME=$2

# If previous result from native find-lang exists, filter mingw entries and move it out of the way
test -f ${PACKAGE_NAME}.lang && grep -v mingw32 ${PACKAGE_NAME}.lang > ${PACKAGE_NAME}-native.lang

/usr/lib/rpm/find-lang.sh $*

if test $? != 0 ; then
    test -f ${PACKAGE_NAME}-native.lang && mv ${PACKAGE_NAME}-native.lang ${PACKAGE_NAME}.lang
    exit 1
fi

targets=`rpm --eval '%{mingw_build_targets}'`
for target in $targets; do
	prefix=`rpm --eval "%{${target}_prefix}"`
	cat ${PACKAGE_NAME}.lang | grep "$prefix" > ${target}-$PACKAGE_NAME.lang
done

test -f ${PACKAGE_NAME}-native.lang && mv ${PACKAGE_NAME}-native.lang ${PACKAGE_NAME}.lang
exit 0
