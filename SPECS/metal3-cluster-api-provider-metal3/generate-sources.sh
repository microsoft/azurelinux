#!/usr/bin/env bash
#
# Source0 is the upstream source tarball of a golang project with the vendor dir
# included for offline build. It also have a top-level directory normalized to
# <package-name>-<version>. It can't simply be downloaded by URL. This script
# will regenerate the tarball in a reproducible such that the hash will be
# consistent with previous runs.
#
# The script may be run in any directory using no arguments.
#
# Usage: /path/to/generate-source.sh
#
set -eu

# reproducible-tar <archive> <file>..
#
#   Create a reproducible tarball. Requires tar version >=1.28. The tarball is
#   created so that file metadata and order will be consistent across any
#   system.
#
reproducible-tar() {
  local archive="$1"
  shift

  #  An explanation of the options to tar:
  #
  #    - File mtime is pinned to a static value (epoch time).
  #    - Files are sorted in a locale-independent way.
  #    - File owner and group are pinned to 0
  #    - File ctime and atime, and process PID, is removed from pax headers
  #
  tar \
    --mtime="1970-01-01 00:00Z" \
    --sort=name \
    --owner=0 \
    --group=0 \
    --numeric-owner \
    --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
    -cf "$archive" \
    $@
}

main() {
  set -x

  spec_dir="$(dirname "$(realpath "$0")")"
  spec=$(echo $spec_dir/*.spec)

  #
  # Extract info from spec.
  #
  name=$(grep "^Name:" "$spec" | awk '{ print $2 }')
  version=$(grep "^Version:" "$spec" | awk '{ print $2}')
  url="$(grep "^URL:" "$spec" | awk '{ print $2}')/archive/refs/tags/v$version.tar.gz"

  #
  # Do the rest of the work within a temp dir so the wd is clean.
  #
  temp_dir=$(mktemp -d)
  trap "rm -rf $temp_dir" EXIT
  cd $temp_dir

  source0=$name-$version.tar.gz

  wget -O $source0 $url
  tar xf $source0
  rm $source0
  mv * $name-$version
  pushd *
  go mod vendor
  popd
  reproducible-tar $source0 *
  mv $source0 "$spec_dir"
}

if [[ $# != 0 ]]; then
  echo "Error: Unknown argument: $1"
  echo "Usage: $0"
  exit -1
fi

main
