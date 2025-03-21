#!/bin/bash

set -euox pipefail

NAME=tardev-snapshotter
VERSION=0.0.13

SOURCE_DIR=$(pwd)
WORK_DIR=$(mktemp -d)
pushd $WORK_DIR

trap "popd && rm -rf $WORK_DIR" EXIT

git clone -b "jiria/signature-support-for-ts" https://github.com/microsoft/kata-containers
pushd kata-containers/src
mv tardev-snapshotter $NAME-$VERSION
tar -czf $NAME-$VERSION.tar.gz $NAME-$VERSION
mv $NAME-$VERSION.tar.gz $WORK_DIR
popd

/tmp/mariner/uki/build/azurelinux/toolkit/scripts/build_cargo_cache.sh $NAME-$VERSION.tar.gz $NAME-$VERSION

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
