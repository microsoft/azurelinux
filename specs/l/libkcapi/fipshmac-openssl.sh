#!/bin/bash

# Mocks fipshmac using the openssl tool.
# Only for use during RPM build.

[ "$1" = '-d' ] || exit 1

openssl sha256 -hmac orboDeJITITejsirpADONivirpUkvarP -hex "$3" | cut -f 2 -d ' ' \
	>"$2/$(basename "$3").hmac"
