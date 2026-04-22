#!/bin/sh
# This script outputs the value for the %{dist} tag.
RELEASEFILE=/etc/azurelinux-release
 
function check_num {
    MAINVER=$(cut -d "(" -f 1 < $RELEASEFILE | sed -e "s/[^0-9.]//g" -e "s/$//g" | cut -d "." -f 1)
    echo $MAINVER | grep -q '[0-9]' && echo $MAINVER
}

DISTNUM=$(check_num)
DISTTYPE=azl

[ -n "$DISTTYPE" -a -n "$DISTNUM" ] && DISTTAG=".${DISTTYPE}${DISTNUM}"

	
case "$1" in
    --distnum) echo -n "$DISTNUM" ;;
    --disttype) echo -n "$DISTTYPE" ;;
    --help)
	printf "Usage: $0 [OPTIONS]\n"
	printf " Default mode is --dist. Possible options:\n"
	printf " --dist\t\tfor distribution tag\n"
	printf " --distnum\tfor distribution number (major)\n"
	printf " --disttype\tfor distribution type\n" ;;
    *) echo -n "$DISTTAG" ;;
esac
