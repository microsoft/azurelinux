#!/bin/sh

[ $# -lt 1 ] && echo "Usage: $(basename "$0") GHCVERSION INFOFIELD" && exit 1

GHCVER="$1"
FIELD="$2"

if [ -z "$FIELD" ]; then
    /usr/bin/ghc-${GHCVER} --info | sed -e 's/.*(\(".*"\),\(".*"\).*/\1: \2/' -e '/]/d'
else
    /usr/bin/ghc-${GHCVER} --info | grep \""$FIELD"\" | sed -e 's/.*","\(.*\)")/\1/'
fi
