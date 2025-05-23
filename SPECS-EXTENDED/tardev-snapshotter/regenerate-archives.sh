#!/bin/bash

set -euox pipefail

NAME=tardev-snapshotter
VERSION=3.2.0.tardev1

SOURCE_DIR=$(pwd)
WORK_DIR=$(mktemp -d)
pushd $WORK_DIR

trap "popd && rm -rf $WORK_DIR" EXIT

git clone -b "3.2.0.tardev1" https://github.com/microsoft/kata-containers
pushd kata-containers
cp LICENSE src/tardev-snapshotter
mv src/tardev-snapshotter $NAME-$VERSION
tar -czf $NAME-$VERSION.tar.gz $NAME-$VERSION
mv $NAME-$VERSION.tar.gz $WORK_DIR
popd

wget https://raw.githubusercontent.com/microsoft/azurelinux/3.0/toolkit/scripts/build_cargo_cache.sh
chmod +x ./build_cargo_cache.sh
./build_cargo_cache.sh $NAME-$VERSION.tar.gz $NAME-$VERSION

mv $NAME-$VERSION.tar.gz $SOURCE_DIR/
mv $NAME-$VERSION-cargo.tar.gz $SOURCE_DIR/

function update-signature {
    local FILE=$1

    jq ".Signatures.\"$FILE\" = \"$(sha256sum $FILE | cut -d ' ' -f 1)\"" $NAME.signatures.json > $NAME.signatures.json.tmp
    mv $NAME.signatures.json.tmp $NAME.signatures.json
}

# Update the signatures json with the new sha256 hashes
pushd $SOURCE_DIR
update-signature $NAME-$VERSION.tar.gz
update-signature $NAME-$VERSION-cargo.tar.gz
popd
