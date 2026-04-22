#!/bin/bash -eux
VERSION=$(rpm --specfile ./*.spec --qf '%{VERSION}\n' | head -1)
RELEASE=$(rpm --specfile ./*.spec --qf '%{RELEASE}\n' | head -1 | cut -d. -f1)
CHANGELOGTIME=$(rpm --specfile ./*.spec --qf '%{CHANGELOGTIME}\n' | head -1)
SOURCE_DATE_EPOCH=$((CHANGELOGTIME - CHANGELOGTIME % 86400))

SOURCE_DIR=grafana-pcp-$VERSION
SOURCE_TAR=grafana-pcp-$VERSION.tar.gz
VENDOR_TAR=grafana-pcp-vendor-$VERSION-$RELEASE.tar.xz
WEBPACK_TAR=grafana-pcp-webpack-$VERSION-$RELEASE.tar.gz


## Download and extract source tarball
spectool -g grafana-pcp.spec
rm -rf "${SOURCE_DIR}"
tar xf "${SOURCE_TAR}"


## Create vendor bundle
pushd "${SOURCE_DIR}"

# patch the go.mod file to work in the container
patch -p1 --fuzz=0 < ../0003-fix-create_bundles-issue.patch

# Vendor Go dependencies
go mod vendor

# List bundled dependencies
awk '$2 ~ /^v/ && $4 != "indirect" {print "Provides: bundled(golang(" $1 ")) = " substr($2, 2)}' go.mod | \
    sed -E 's/=(.*)-(.*)-(.*)/=\1-\2.\3/g' > "../${VENDOR_TAR}.manifest"

# patch the top consumers dashboard to remove tables visualizing faulty metrics
patch -p1 --fuzz=0 < ../0002-remove-faulty-metric-tables.patch

# Vendor Node.js dependencies
patch -p1 --fuzz=0 < ../0001-remove-unused-frontend-crypto.patch
yarn install --frozen-lockfile

# Remove files with licensing issues
find . -type d -name 'node-notifier' -prune -exec rm -r {} \;
find . -type f -name '*.exe' -delete

# List bundled dependencies
../list_bundled_nodejs_packages.py . >> "../${VENDOR_TAR}.manifest"

# Vendor Jsonnet dependencies
jb --jsonnetpkg-home=vendor_jsonnet install

popd

# Create tarball
# shellcheck disable=SC2046
XZ_OPT=-9 tar \
    --sort=name \
    --mtime="@${SOURCE_DATE_EPOCH}" --clamp-mtime \
    --owner=0 --group=0 --numeric-owner \
    -cJf "${VENDOR_TAR}" \
    "${SOURCE_DIR}/vendor" \
    "${SOURCE_DIR}/node_modules" \
    "${SOURCE_DIR}/vendor_jsonnet"


## Create webpack
pushd "${SOURCE_DIR}"
../build_frontend.sh
popd

# Create tarball
tar \
    --sort=name \
    --mtime="@${SOURCE_DATE_EPOCH}" --clamp-mtime \
    --owner=0 --group=0 --numeric-owner \
    -czf "${WEBPACK_TAR}" \
    "${SOURCE_DIR}/dist"
