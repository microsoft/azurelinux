#!/bin/bash
# strip-rar-support.sh

if [[ $# -ne 1 ]]; then
  echo Usage: strip-rar-support.sh 7zip-\$version.tar.gz
  exit 1
fi

ORIG_TARBALL=$1
SRC_DIR=${ORIG_TARBALL%.tar.gz}
TEMP_DIR=$(mktemp -d)

tar -C $TEMP_DIR -xf $ORIG_TARBALL

pushd ${TEMP_DIR}/${SRC_DIR}
echo $PWD
rm -rf CPP/7zip/Archive/Rar/
rm -f CPP/7zip/Compress/Rar*.*
rm -f CPP/7zip/Crypto/Rar*.*
rm -f DOC/unRarLicense.txt
popd

tar --zstd -cf $PWD/${SRC_DIR}.tar.zst -C $TEMP_DIR ${SRC_DIR}

rm -R ${TEMP_DIR}
