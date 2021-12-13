#!/bin/sh
#
# Mailx's upstream provides only the CVS method of downloading source code.
# This script can be used for downloading the CVS repository and creating
# the tarball.
#
# Usage:  ./get-upstream-tarball.sh
#
# This code is in the public domain; do with it what you wish.
#
# Copyright (C) 2012 Peter Schiffer <pschiffe@redhat.com>
#

newdir=new-upstream-tarball

mkdir $newdir
cd $newdir

# checkout cvs
echo "== Just press Enter =="
cvs -d:pserver:anonymous@nail.cvs.sourceforge.net:/cvsroot/nail login
cvs -d:pserver:anonymous@nail.cvs.sourceforge.net:/cvsroot/nail co nail

# remove CVS folders
rm -rf nail/CVS nail/catd/CVS

# find version in nail/version.c file defined as: #define V "xxx"
ver=$(sed -rn 's/#define\s+V\s+\"([0-9.]+)\"/\1/p' nail/version.c)

mv nail mailx-$ver
tar cJf mailx-$ver.tar.xz mailx-$ver

rm -rf mailx-$ver

