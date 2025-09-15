#!/bin/sh

# args
repo="${1%/}"
ref="${2-HEAD}"
ab="${3-12}"

# check
if test ! -d "${repo}/.git"; then
    echo "usage: $0 <repodir> [ <ref> [ <abbrev> ] ]"
    exit 1
fi

# get + print info
commit=$(cd $repo; git show --abbrev=$ab --pretty='format:%h' $ref | head -1)
date=$(cd $repo; git show --pretty='format:%cs' $ref | head -1 | tr -d '-')
echo "# $repo $ref  ->  commit $commit - date $date"

# create tarball
name="${repo##*/}"
file="${name}-${commit}.tar.xz"
(cd $repo; git archive --format=tar --prefix=${name}-${commit}/ ${commit}) \
    | xz -9ev > "$file"
echo "# $file written"
