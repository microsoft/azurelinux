#!/bin/bash

LUAJIT_PKGNAME="LuaJIT"
LUAJIT_URL=$(rpmspec -P *.spec | awk '/Source0/ { print $NF }')
LUAJIT_TARBALL=$(basename $LUAJIT_URL)
LUAJIT_VERSION_MAJOR=$(awk '/%global luajit_version_major/ { print $NF }' *.spec)
LUAJIT_VERSION_MINOR=$(awk '/%global luajit_version_minor/ { print $NF }' *.spec)
LUAJIT_VERSION_PATCH=$(awk '/%global luajit_version_patch/ { print $NF }' *.spec)
LUAJIT_VERSION="${LUAJIT_VERSION_MAJOR}.${LUAJIT_VERSION_MINOR}.${LUAJIT_VERSION_PATCH}"

LUAJIT_PKGDIR="$(pwd)"
LUAJIT_TMPDIR=$(mktemp --tmpdir -d luajit-XXXXXXXX)

cleanup_tmpdir() {
    popd 2>/dev/null || true
    rm -rf "${LUAJIT_TMPDIR}"
}
trap cleanup_tmpdir SIGINT

cleanup_and_exit() {
    cleanup_tmpdir
    if test "$1" = 0 -o -z "$1" ; then
        exit 0
    else
        exit "${1}"
    fi
}

pushd "${LUAJIT_TMPDIR}" || cleanup_and_exit 1

wget "${LUAJIT_URL}"

tar xf ${LUAJIT_PKGNAME}-${LUAJIT_VERSION}.tar.gz

# commiter date, unix timestamp
LUAJIT_VERSION_PATCH_NEW=$(<${LUAJIT_PKGNAME}-${LUAJIT_VERSION_MAJOR}.${LUAJIT_VERSION_MINOR}/.relver)
LUAJIT_VERSION_NEW="${LUAJIT_VERSION_MAJOR}.${LUAJIT_VERSION_MINOR}.${LUAJIT_VERSION_PATCH_NEW}"
echo "LUAJIT_VERSION=${LUAJIT_VERSION_NEW}"

mv "${LUAJIT_PKGNAME}-${LUAJIT_VERSION}.tar.gz" "${LUAJIT_PKGDIR}/${LUAJIT_PKGNAME}-${LUAJIT_VERSION_NEW}.tar.gz"
echo
echo ">>> New tarball, run: fedpkg new-sources ${LUAJIT_PKGNAME}-${LUAJIT_VERSION_NEW}.tar.gz LuaJIT-test-cleanup.tar.gz"

popd || cleanup_and_exit 1

echo
echo ">>> Update spec file with: %global luajit_version_patch ${LUAJIT_VERSION_PATCH_NEW}"
echo

cleanup_and_exit 0
