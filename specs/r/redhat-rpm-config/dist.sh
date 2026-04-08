#!/bin/bash
# dist.sh
# Author: Tom "spot" Callaway <tcallawa@redhat.com>
# License: GPL
# This is a script to output the value for the %{dist}
# tag. The dist tag takes the following format: .$type$num
# Where $type is one of: el, fc, rh
# (for RHEL, Fedora Core, and RHL, respectively)
# And $num is the version number of the distribution.
# NOTE: We can't detect Rawhide or Fedora Test builds properly.
# If we successfully detect the version number, we output the
# dist tag. Otherwise, we exit with no output.

RELEASEFILE=/etc/redhat-release

function check_num {
    MAINVER=`cut -d "(" -f 1 < $RELEASEFILE | \
	sed -e "s/[^0-9.]//g" -e "s/$//g" | cut -d "." -f 1`

    echo $MAINVER | grep -q '[0-9]' && echo $MAINVER
}

function check_rhl {
    grep -q "Red Hat Linux" $RELEASEFILE && ! grep -q "Advanced" $RELEASEFILE && echo $DISTNUM
}

function check_rhel {
    grep -Eq "(Enterprise|Advanced|CentOS)" $RELEASEFILE && echo $DISTNUM
}

function check_fedora {
    grep -q Fedora $RELEASEFILE && echo $DISTNUM
}

DISTNUM=`check_num`
DISTFC=`check_fedora`
DISTRHL=`check_rhl`
DISTRHEL=`check_rhel`
if [ -n "$DISTNUM" ]; then
    if [ -n "$DISTFC" ]; then
	DISTTYPE=fc
    elif [ -n "$DISTRHEL" ]; then
	DISTTYPE=el
    elif [ -n "$DISTRHL" ]; then
	DISTTYPE=rhl
    fi
fi
[ -n "$DISTTYPE" -a -n "$DISTNUM" ] && DISTTAG=".${DISTTYPE}${DISTNUM}"

case "$1" in
    --el) echo -n "$DISTRHEL" ;;
    --fc) echo -n "$DISTFC" ;;
    --rhl) echo -n "$DISTRHL" ;;
    --distnum) echo -n "$DISTNUM" ;;
    --disttype) echo -n "$DISTTYPE" ;;
    --help)
	printf "Usage: $0 [OPTIONS]\n"
	printf " Default mode is --dist. Possible options:\n"
	printf " --el\t\tfor RHEL version (if RHEL)\n"
	printf " --fc\t\tfor Fedora version (if Fedora)\n"
	printf " --rhl\t\tfor RHL version (if RHL)\n"
	printf " --dist\t\tfor distribution tag\n"
	printf " --distnum\tfor distribution number (major)\n"
	printf " --disttype\tfor distribution type\n" ;;
    *) echo -n "$DISTTAG" ;;
esac
