#!/bin/sh
#this script is used to remove babled and ldpd from the tar sources
#Usage: sh remove-babeld-ldpd.sh <VERSION>
#Example: sh remove-babeld-ldpd.sh 7.3.1 - this is for frr-7.3.1.tar.gz file

VERSION=$1
TAR=frr-${VERSION}.tar.gz
DIR=frr-${VERSION}

echo ${VERSION}
echo ${TAR}
echo ${DIR}

tar -xzf ${TAR}
rm -rf ${DIR}/babeld ${DIR}/ldpd
tar -czf ${TAR} ${DIR}
