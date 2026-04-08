#!/bin/bash
#Try to get upstream latest files

DATE=$(date -u +%Y%m%d)
ARCHIVE="google-droid-fonts-$DATE"
TMPDIR=$(mktemp -d --tmpdir=/var/tmp getdroid-XXXXXXXXXX)
[ $? != 0 ] && exit 1
umask 022
pushd "$TMPDIR"
git init
git remote add -t HEAD origin https://android.googlesource.com/platform/frameworks/base.git
git config core.sparseCheckout true
git config diff.renameLimit 999999
cat > .git/info/sparse-checkout << EOF
data/fonts/*
!data/fonts/*ttf
!data/fonts/*xml
!data/fonts/*mk
!MODULE_LICENSE_APACHE2
data/fonts/Droid*
EOF
git pull --no-tags origin HEAD
for file in $(git log --diff-filter=D --summary | grep delete | cut -d ' ' -f 5 |\
              grep 'data/fonts/Droid.*ttf' | sort -u | \
              grep -v data/fonts/DroidSansFallback | \
              grep -v data/fonts/DroidSansHebrew.ttf | \
              grep -v data/fonts/DroidNaskh-Regular-Shift.ttf | \
              grep -v data/fonts/DroidNaskhUI-Regular.ttf | \
              grep -v data/fonts/DroidSansArabic.ttf) ; do
  git checkout $(git log --all -- ${file} | \
                 grep '^commit' | head -2 | tail -1 | cut -d ' ' -f 2) -- "${file}"
done
install -m 0755 -d "$ARCHIVE"
install -m 0644 -p data/fonts/* "$ARCHIVE"
tar -cvJf "$ARCHIVE.tar.xz" "$ARCHIVE"
popd
mv "$TMPDIR/$ARCHIVE.tar.xz" .
rm -fr "$TMPDIR"
