#!/bin/bash

user="tianocore"
repo="edk2"
branch="master"

uri="https://github.com/${user}/${repo}"
api="${uri/github.com/api.github.com/repos}"
tar="${uri/github.com/codeload.github.com}/legacy.tar.gz"

if test $# -ge 1; then
  hash=$1
  short=$1
else
  hash=$(curl -s "${api}/git/refs/heads/${branch}" | grep '"sha"' | cut -d'"' -f4)
  if test "$hash" = ""; then
	echo "# failed to fetch $branch hash"
	exit 1
  fi
  short=$(echo $hash | sed -e 's/^\(.......\).*/\1/')
fi

if test $# = 2; then
  date=$2
else
  date=$(curl -s "${api}/git/commits/$hash" | awk '
	  /"committer"/	{ c=1 }
	  /"date"/	{ if (c) { print } }
  ' | cut -d'"' -f4)
  date="${date%T*}"
  date="${date//-/}"
fi

name="${repo}-${date}-${short}.tar.xz"

if test -f "$name"; then
	echo "# exists: $name"
	exit 1
fi

echo
echo "# specfile update: version $date, release $short"
sed -i.old \
        -e "s/\(%global edk2_date[ \t]\+\)\(.*\)/\1$date/" \
        -e "s/\(%global edk2_githash[ \t]\+\)\(.*\)/\1$short/" \
        edk2.spec
diff -u edk2.spec.old edk2.spec

echo
echo "# cleanup ..."
rm -vf ${repo}-*.tar*
echo "# fetching $name ..."
curl "$tar/$hash" | zcat | xz -9e > "$name"
exit 0
