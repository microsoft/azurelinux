#!/bin/sh
set -x

# On the review request (rh bug 477526) it is found that
# boingboing.html are under CC-BY-NC (non-commercial)...
# too bad, not allowed on Fedora.

VERSION=${VERSION:-0.6.164}
URL=http://rubygems.org/downloads

wget -N ${URL}/hpricot-${VERSION}.gem

TMPDIR=$(mktemp -d /tmp/hpricot-XXXXXX)
tar -C $TMPDIR -xf hpricot-${VERSION}.gem
pushd $TMPDIR
mkdir TMP
tar -C TMP -xf data.tar.gz
cd TMP

# Remove CC-BY-NC licensed file
find . -name \*boingboing\* | xargs rm -f
# Ah.. fixing Rakefile
find . -name Rakefile | \
	xargs sed -i -e '\@s\.version@s|VERS$|VERS.dup|'
# Recreate gem
VERSION=${VERSION} rake gem --trace

popd
mv ${TMPDIR}/TMP/pkg/*.gem hpricot-${VERSION}-modified.gem
chmod 0644 hpricot-${VERSION}-modified.gem
rm -rf $TMPDIR
