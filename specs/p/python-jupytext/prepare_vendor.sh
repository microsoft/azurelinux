#!/bin/bash

PKG_URL=$(spectool *.spec --source 0 | sed -e 's/Source0:[ ]*//g')
PKG_TARBALL=$(basename $PKG_URL)
PKG_NAME=$(rpmspec -q --queryformat="%{NAME}" *.spec --srpm | sed 's/^python-//')
PKG_VERSION=$(rpmspec -q --queryformat="%{VERSION}" *.spec --srpm)
PKG_SRCDIR="${PKG_NAME}-${PKG_VERSION}/jupyterlab"
PKG_DIR="$PWD"
PKG_TMPDIR=$(mktemp --tmpdir -d ${PKG_NAME}-XXXXXXXX)
PKG_PATH="$PKG_TMPDIR/$PKG_SRCDIR/"

echo "URL:     $PKG_URL"
echo "TARBALL: $PKG_TARBALL"
echo "NAME:    $PKG_NAME"
echo "VERSION: $PKG_VERSION"
echo "PATH:    $PKG_PATH"

cleanup_tmpdir() {
    popd 2>/dev/null
    rm -rf $PKG_TMPDIR
    rm -rf /tmp/yarn--*
}
trap cleanup_tmpdir SIGINT

cleanup_and_exit() {
    cleanup_tmpdir
    if test "$1" = 0 -o -z "$1" ; then
        exit 0
    else
        exit $1
    fi
}

if [ ! -w "$PKG_TARBALL" ]; then
    wget "$PKG_URL"
fi

mkdir -p $PKG_TMPDIR
tar -xf $PKG_TARBALL -C $PKG_TMPDIR

cd $PKG_PATH

export HATCH_BUILD_HOOKS_ENABLE=true
export YARN_CACHE_FOLDER="$PWD/.package-cache"
echo ">>>>>> Install npm modules"
jlpm install
if [ $? -ne 0 ]; then
    echo "ERROR: jlpm install failed"
    cleanup_and_exit 1
fi

echo ">>>>>> Package vendor files"
rm -f $PKG_DIR/${PKG_NAME}-${PKG_VERSION}-vendor.tar.xz
XZ_OPT="-9e -T$(nproc)" tar cJf $PKG_DIR/${PKG_NAME}-${PKG_VERSION}-vendor.tar.xz .package-cache yarn.lock
if [ $? -ne 0 ]; then
    echo "ERROR: vendor tarball creation failed"
    cleanup_and_exit 1
fi

echo ">>>>>> Find licenses"
jlpm add license-checker
jlpm license-checker --summary | sed "s#$PKG_PATH#/tmp/#g" > $PKG_DIR/${PKG_NAME}-${PKG_VERSION}-vendor-licenses.txt

cd -

rm -rf .package-cache node_modules

echo ">>>>>> Remember to run this script on both x86_64 AND aarch64 and merge"

cleanup_and_exit 0
