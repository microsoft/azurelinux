#!/bin/sh
#
# This script will initialise token storage of softhsm PKCS11 provider
# in custom location. Is useful to store tokens in non-standard location.
#
# Output can be evaluated from bash, it will prepare it for usage of temporary tokens.
# Quotes around eval are mandatory!
# Recommended use:
# eval "$(bash setup-named-softhsm.sh -A)"
#

SOFTHSM2_CONF="$1"
TOKENPATH="$2"
GROUPNAME="$3"
# Do not use this script for real keys worth protection
# This is intended for crypto accelerators using PKCS11 interface.
# Uninitialized token would fail any crypto operation.
PIN=1234
SO_PIN=1234
LABEL=rpm

set -e

echo_i()
{
	echo "#" $@
}

random()
{
	if [ -x "$(which openssl 2>/dev/null)" ]; then
		openssl rand -base64 $1
	else
		dd if=/dev/urandom bs=1c count=$1 | base64
	fi
}

usage()
{
	echo "Usage: $0 -A [token directory] [group]"
	echo "   or: $0 <config file> <token directory> [group]"
}

if [ "$SOFTHSM2_CONF" = "-A" -a -z "$TOKENPATH" ]; then
	TOKENPATH=$(mktemp -d /var/tmp/softhsm-XXXXXX)
fi

if [ -z "$SOFTHSM2_CONF" -o -z "$TOKENPATH" ]; then
	usage >&2
	exit 1
fi

if [ "$SOFTHSM2_CONF" = "-A" ]; then
	# Automagic mode instead
	MODE=secure
	SOFTHSM2_CONF="$TOKENPATH/softhsm2.conf"
	PIN_SOURCE="$TOKENPATH/pin"
	SOPIN_SOURCE="$TOKENPATH/so-pin"
	TOKENPATH="$TOKENPATH/tokens"
else
	MODE=legacy
fi

[ -d "$TOKENPATH" ] || mkdir -p "$TOKENPATH"

umask 0022

if ! [ -f "$SOFTHSM2_CONF" ]; then
cat  << SED > "$SOFTHSM2_CONF"
# SoftHSM v2 configuration file

directories.tokendir = ${TOKENPATH}
objectstore.backend = file

# ERROR, WARNING, INFO, DEBUG
log.level = ERROR

# If CKF_REMOVABLE_DEVICE flag should be set
slots.removable = false
SED
else
	echo_i "Config file $SOFTHSM2_CONF already exists" >&2
fi

if [ -n "$PIN_SOURCE" ]; then
	touch "$PIN_SOURCE" "$SOPIN_SOURCE"
	chmod 0600 "$PIN_SOURCE" "$SOPIN_SOURCE"
	if [ -n "$GROUPNAME" ]; then
		chgrp "$GROUPNAME" "$PIN_SOURCE" "$SOPIN_SOURCE"
		chmod g+r "$PIN_SOURCE" "$SOPIN_SOURCE"
	fi
fi

export SOFTHSM2_CONF

if softhsm2-util --show-slots | grep 'Initialized:[[:space:]]*yes' > /dev/null
then
	echo_i "Token in ${TOKENPATH} is already initialized" >&2

	[ -f "$PIN_SOURCE" ] && PIN=$(cat "$PIN_SOURCE")
	[ -f "$SOPIN_SOURCE" ] && SO_PIN=$(cat "$SOPIN_SOURCE")
else
	PIN=$(random 6)
	SO_PIN=$(random 18)
	if [ -n "$PIN_SOURCE" ]; then
		echo -n "$PIN" > "$PIN_SOURCE"
		echo -n "$SO_PIN" > "$SOPIN_SOURCE"
	fi

	echo_i "Initializing tokens to ${TOKENPATH}..."
	softhsm2-util --init-token --free --label "$LABEL" --pin "$PIN" --so-pin "$SO_PIN" | sed -e 's/^/# /'

	if [ -n "$GROUPNAME" ]; then
		chgrp -R -- "$GROUPNAME" "$TOKENPATH"
		chmod -R -- g=rX,o= "$TOKENPATH"
	fi
fi

echo "export SOFTHSM2_CONF=\"$SOFTHSM2_CONF\""
echo "export PIN_SOURCE=\"$PIN_SOURCE\""
echo "export SOPIN_SOURCE=\"$SOPIN_SOURCE\""
# These are intentionaly not exported
echo "PIN=\"$PIN\""
echo "SO_PIN=\"$SO_PIN\""
