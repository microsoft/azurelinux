#!/usr/bin/env bash
#
# The Source0 of this package is the upstream source tarball with the vendor dir
# included for offline builds and its top-level directory renamed to
# <name>-<version>. This script will regenerate Source0 in a reproducible way
# such that its cyptographic hash in *.signatures.json will not need to be
# changed. It may be run in any directory.
#
# Usage: /path/to/generate-sources.sh
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
  # Extract values of Name, Version, and Source0 directives from spec file.
  #
  name=$(grep "^Name:" "$spec" | awk '{ print $2 }')
  version=$(grep "^Version:" "$spec" | awk '{ print $2}')
  source0=$(grep "^Source0:" "$spec" | awk '{ print $2}')

  #
  # Expand all instances of %{name} and %{version} macros.
  #
  source0=${source0//%\{name\}/$name}
  source0=${source0//%\{version\}/$version}

  #
  # Extract url and name from Source0, formatted as <url>#/<name>.
  #
  source0_url=${source0%#/*}
  source0_name=${source0#*#/}

  #
  # Do the rest of the work within a temp dir so the wd is clean.
  #
  temp_dir=$(mktemp -d)
  trap "rm -rf $temp_dir" EXIT
  cd $temp_dir

  wget -O $source0_name $source0_url
  tar xf $source0_name
  rm $source0_name
  mv * $name-$version
  pushd *
  go mod vendor
  popd
  reproducible-tar $source0_name *
  mv $source0_name "$spec_dir"
}

if [[ $# != 0 ]]; then
  echo "Error: Unknown argument: $1"
  echo "Usage: $0"
  exit -1
fi

main
