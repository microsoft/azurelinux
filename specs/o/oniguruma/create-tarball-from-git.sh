#!/bin/sh

set -e
set -x

CURRENTDIR=$(pwd)
PKGNAME=oniguruma
TARNAME=onig

TMPDIR=$(mktemp -d /var/tmp/$PKGNAME-XXXXXX)
pushd $TMPDIR

GITSCM=https://github.com/kkos/$PKGNAME.git

git clone $GITSCM
pushd $PKGNAME

COMMIT=$(git log | head -n 1 | sed -e 's|^.*[ \t]||')
SHORTCOMMIT=$(echo $COMMIT | cut -c-7)
DATE=$(git show --format=%ci $COMMIT | head -n 1 | sed -e 's|[ \t].*$||')
SHORTDATE=$(echo $DATE | sed -e 's|-||g')
VERSION=$(cat configure.ac | grep AC_INIT | sed -n -e 's|^.*,[ \t]*\([0-9\.][0-9\.]*\).*$|\1|p')

git log --format=fuller | head -n 12

echo "VERSION=$VERSION"
echo "COMMIT=$COMMIT"
echo "DATE=$DATE"

echo
popd

TARDIR=${TARNAME}-${VERSION}-${SHORTDATE}git${SHORTCOMMIT}
ln -sf $PKGNAME $TARDIR
tar czf ${TARDIR}.tar.gz ${TARDIR}/./ 

mv ${TARDIR}.tar.gz ${CURRENTDIR}/
popd

rm -rf $TMPDIR

