#!/usr/bin/bash

set -e

CRATE="fiat-crypto"
NAME="rust-${CRATE}"

VERSION=$(rpmspec -q $NAME.spec --srpm --qf "%{version}")
URL="https://crates.io/api/v1/crates/${CRATE}/${VERSION}/download"

ROOTDIR="${CRATE}-${VERSION}"

# download and extract published crate from crates.io
wget $URL -O ${ROOTDIR}.crate
tar -xzf ${ROOTDIR}.crate
rm ${ROOTDIR}.crate

pushd ${ROOTDIR}

# remove code related to the p434 curve which is not permitted in Fedora:
# https://lists.fedoraproject.org/archives/list/legal@lists.fedoraproject.org/thread/FBZU2X7ZKTK2BVZKBHFUCI44SMY4UQCE/
rm src/p434_64.rs

# clean up cargo files
rm .cargo_vcs_info.json
mv Cargo.toml.orig Cargo.toml

# initialize git repo and remove references to code related to the p434 curve
git init
git add .
git apply ../0001-remove-references-to-code-related-to-the-p434-curve.patch
git commit -a -m "import"

# repackage crate
cargo package

# move clean crate
mv target/package/${ROOTDIR}.crate ../${ROOTDIR}-clean.crate
popd

# remove temporary directory
rm -rf ${ROOTDIR}

