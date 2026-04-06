#!/bin/sh

DATE=$( date +%Y%m%d )
DIRNAME=libpciaccess
REV=${1:-master}

if test -e $DIRNAME.git; then
    GIT_DIR=$DIRNAME.git git fetch git://git.freedesktop.org/git/xorg/lib/libpciaccess
else
    git clone --bare git://git.freedesktop.org/git/xorg/lib/libpciaccess $DIRNAME.git
    GIT_DIR=$DIRNAME.git git archive --prefix=$DIRNAME-$DATE/ --format=tar $REV | \
	bzip2 -c > $DIRNAME-$DATE.tar.bz2
fi

HASH=$(GIT_DIR=$DIRNAME.git git show-ref -s $REV)

echo $HASH

exit 

# the rest of this is supposed to work?  i guess.

version=$(sed -n -e "s/^Version: *\(.*\)/\1/p" < libpciaccess.spec)
release=$(sed -n -e "s/^Release: *\([^.]*\).*/\1/p" < libpciaccess.spec)
release=$(($release + 1))

user=$(id -un)
IFS=: info=($(grep ^$user: /etc/passwd))

msg="* $(date +'%a %b %d %Y') ${info[4]} <$user@redhat.com> $version-$release.$DATE\\
- New snapshot, git revision $HASH.\\
"

sed -i -e "s/^%define gitdate.*/%define gitdate $DATE/" \
	-e "s/^%define gitrev.*/%define gitrev $HASH/" \
	-e "s/^Source0:.*/Source0:        $DIRNAME-$DATE.tar.bz2/" \
	-e "s/^Release:.*/Release:        $release.%{gitdate}%{?dist}/" \
	-e "/%changelog/ a $msg" \
	libpciaccess.spec

make new-sources FILES=$DIRNAME-$DATE.tar.bz2
