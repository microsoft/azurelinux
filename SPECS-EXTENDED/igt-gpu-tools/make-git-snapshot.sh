#!/bin/sh

# Usage: ./make-git-snapshot.sh [COMMIT]
#
# to make a snapshot of the given tag/branch.  Defaults to HEAD. Point env var REF to a local
# igt-gpu-tools repo to reduce clone time. Also gathers version information using meson introspect,
# point env var MESON_BIN if your copy of meson lives somewhere else

DIRNAME=igt-gpu-tools-$( date +%Y%m%d )

REF=${REF:+--reference $REF}
HEAD=${1:-HEAD}

meson() {
	${MESON_BIN:-$(whereis -b meson | cut -f 2 -d ' ')} "$@"
}

echo REF ${REF:+--reference $REF}
echo DIRNAME $DIRNAME
echo HEAD $HEAD

rm -rf $DIRNAME
trap 'rm -rf $DIRNAME' EXIT

git clone ${REF:+--reference $REF} \
	https://gitlab.freedesktop.org/drm/igt-gpu-tools.git $DIRNAME

export GIT_DIR=$DIRNAME/.git

sed -i "igt-gpu-tools.spec" \
	-e "s/%global gitcommit [0-9a-f]\+/%global gitcommit $(git rev-parse $HEAD)/" \
	-e "s/%global gitdate [0-9]\+/%global gitdate $(date +%Y%m%d)/"

# Extract the version number
VERSION=$(meson introspect --projectinfo -i $DIRNAME/meson.build | \
	grep -oPm1 '(?<="version": ")[0-9]+\.[0-9]+')
echo "Version is $VERSION"

# rpmdev-bumpspec won't notice that we're actually trying to add a new comment if the actual igt
# version is identical to the previous one, since rpmdev-bumpspec doesn't expand spec files. So, we
# set it to a fake version then just correct it with sed
rpmdev-bumpspec \
	-c "New git snapshot" \
	-n "___IGT_FAKE_VERSION___-1%{?gitrev}%{?dist}" \
	igt-gpu-tools.spec
sed -i "igt-gpu-tools.spec" -e "s/___IGT_FAKE_VERSION___/$VERSION/g"

git archive --format=tar $HEAD | bzip2 > $DIRNAME.tar.bz2

# vim: tw=100 :
