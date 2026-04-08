#!/bin/bash
#
# Copyright (c) Neal Gompa <ngompa@fedoraproject.org>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# shellcheck disable=2181

export LC_COLLATE="C.UTF-8"

PKGNAME="xevd"
PKGNAME_SUFFIX="-free"
VERSION="$(rpmspec -P ${PKGNAME}.spec | grep ^Version | sed -e 's/Version:[ ]*//g')"
TARBALL_URL="https://github.com/mpeg5/${PKGNAME}/archive/v${VERSION}/${PKGNAME}-${VERSION}.tar.gz"
TARBALL="$(basename "${TARBALL_URL}")"
PKG_DIR="$(pwd)"
TMPDIR=$(mktemp --tmpdir -d "${PKGNAME}-XXXXXXXX")

if [[ ! -w "${TARBALL}" ]]; then
    echo ">>> Downloading ${TARBALL}"
    wget "${TARBALL_URL}"
fi

echo ">>> Unpacking ${TARBALL}"

tar -xf "${TARBALL}" -C "${TMPDIR}"

echo
echo ">>> Cleaning up sources for new tarball ..."

pushd "${TMPDIR}"
rm -rf "${PKGNAME}-${VERSION}/src_main"

echo ">>> Create new tarball ${PKGNAME}${PKGNAME_SUFFIX}-${VERSION}.tar.gz ..."
tar -czf "${PKG_DIR}/${PKGNAME}${PKGNAME_SUFFIX}-${VERSION}.tar.gz" "${PKGNAME}-${VERSION}"
popd

du -sh "${PKGNAME}${PKGNAME_SUFFIX}-${VERSION}.tar.gz"
echo

echo ">>> Cleaning up working area ..."
rm -rf "${TMPDIR}"
