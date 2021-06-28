#!/usr/bin/env sh

set -e

abort() {
	echo "$@"
	return 1
}

if [ -z "${CHECK_VERSION}" ]; then
	abort "Version must not be empty"
fi
if [ "${CHECK_VERSION}" = "${DEFAULT_VERSION}" ]; then
	abort "Version must not match default version: ${DEFAULT_VERSION}"
fi

