#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
set -e
set -x

if [[ -z "$LFS" ]]; then
    echo "Must define LFS in environment" 1>&2
    exit 1
fi
echo LFS root is: $LFS

version=212-b04

sourceTarball=http://hg.openjdk.java.net/jdk8u/jdk8u/archive/jdk8u${version}.tar.bz2
if [ ! -f ${LFS}/sources/jdk8u${version}.tar.bz2 ]; then
    wget -nv --no-clobber --timeout=30 --continue ${sourceTarball} -O ${LFS}/sources/jdk8u${version}.tar.bz2
fi

# The sub-projects all have the same tag as the master repository.
# This results in source tarballs all having the same name (but different URIs).
# Rename the tarballs as they are downloaded so they don't overwrite each other.
# This means the names in toolchain-jdk8-md5sums do not match the source tarball names, 
# but they are all there.
for subproject in corba hotspot jaxp jaxws langtools jdk nashorn; do
  if [ ! -f ${LFS}/sources/jdk8u${version}-${subproject}.tar.bz2 ]; then
    wget -nv --no-clobber --timeout=30 --continue \
         http://hg.openjdk.java.net/jdk8u/jdk8u/${subproject}/archive/jdk8u${version}.tar.bz2 \
         -O ${LFS}/sources/jdk8u${version}-${subproject}.tar.bz2
  fi
done

### Now download aarch64 sources

version=181-b13

sourceTarball=http://hg.openjdk.java.net/aarch64-port/jdk8u/archive/aarch64-jdk8u${version}.tar.bz2
if [ ! -f ${LFS}/sources/jdk8u${version}.tar.bz2 ]; then
    wget -nv --no-clobber --timeout=30 --continue ${sourceTarball} -O ${LFS}/sources/aarch64-jdk8u${version}.tar.bz2
fi

# The sub-projects all have the same tag as the master repository.
# This results in source tarballs all having the same name (but different URIs).
# Rename the tarballs as they are downloaded so they don't overwrite each other.
# This means the names in toolchain-jdk8-md5sums do not match the source tarball names, 
# but they are all there.
for subproject in corba hotspot jaxp jaxws langtools jdk nashorn; do
  if [ ! -f ${LFS}/sources/aarch64-jdk8u${version}-${subproject}.tar.bz2 ]; then
    wget -nv --no-clobber --timeout=30 --continue \
         http://hg.openjdk.java.net/aarch64-port/jdk8u/${subproject}/archive/aarch64-jdk8u${version}.tar.bz2 \
         -O ${LFS}/sources/aarch64-jdk8u${version}-${subproject}.tar.bz2
  fi
done
