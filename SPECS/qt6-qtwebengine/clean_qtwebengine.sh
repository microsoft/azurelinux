#!/bin/bash
# Copyright 2015-2017 Kevin Kofler <Kevin@tigcc.ticalc.org>
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

if [ -z "$1" ] ; then
  echo "usage: ./clean_qtwebengine.sh VERSION"
  echo "e.g.: ./clean_qtwebengine.sh 6.10.0"
  exit 1
fi

DIRNAME="qtwebengine-everywhere-src-$1"

echo "removing $DIRNAME"
rm -rf "$DIRNAME" || exit $?

if [ -f "$DIRNAME.tar.xz" ] ; then
  echo "unpacking $DIRNAME.tar.xz"
  XZ_OPT="-T 4" tar xJf "$DIRNAME.tar.xz" || exit $?
elif [ -f "$DIRNAME.tar.bz2" ] ; then
  echo "unpacking $DIRNAME.tar.bz2"
  tar xjf "$DIRNAME.tar.bz2" || exit $?
elif [ -f "$DIRNAME.tar.gz" ] ; then
  echo "unpacking $DIRNAME.tar.gz"
  tar xzf "$DIRNAME.tar.gz" || exit $?
elif [ -f "$DIRNAME.7z" ] ; then
  echo "unpacking $DIRNAME.7z"
  if type 7za >/dev/null 2>/dev/null ; then
    7za x "$DIRNAME.7z" || exit $?
  elif type 7z >/dev/null 2>/dev/null ; then
    7z x "$DIRNAME.7z" || exit $?
  else
    echo "error: p7zip required"
    exit 1
  fi
else
  echo "error: no archive for $DIRNAME found"
  exit 1
fi

echo "running clean_ffmpeg.sh"
./clean_ffmpeg.sh "$DIRNAME/src/3rdparty/chromium" || exit $?

echo "ripping out openh264 sources, keeping just header files"
find "$DIRNAME/src/3rdparty/chromium/third_party/openh264/src" -type f -not -name '*.h' -delete || exit $?

echo "repacking as $DIRNAME-clean.tar.xz"
XZ_OPT="-8 -T 2" tar cJf "$DIRNAME-clean.tar.xz" "$DIRNAME" || exit $?

echo "removing $DIRNAME"
rm -rf "$DIRNAME" || exit $?

echo "done"
exit 0
