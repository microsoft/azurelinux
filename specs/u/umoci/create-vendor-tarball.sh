#!/usr/bin/bash

tag=$1

if [[ -z $tag ]]; then
    echo "This script requires the tag as an argument."
    exit 1
fi

set -euo pipefail

PKG="umoci"
REPO="https://github.com/opencontainers/$PKG"

# transform tag into version

case $tag in
    *beta*)
        # v2.0.0-beta.1 -> 2.0.0~beta1
        temp=${tag#v}
        version=${temp/-beta./~beta}
        ;;
    *rc*)
        # v2.0.0-rc.1 -> 2.0.0~rc1
        temp=${tag#v}
        version=${temp/-rc./~rc}
        ;;
    *)
        # v2.0.0 -> 2.0.0
        version=${tag#v}
        ;;
esac

echo "Using tag: $tag"
echo "Using version: $version"

git -c advice.detachedHead=false clone --branch $tag --depth 1 $REPO.git $PKG-$version
pushd $PKG-$version
GOPROXY='https://proxy.golang.org,direct' go mod vendor
popd
tar -C $PKG-$version -czf $PKG-$version-vendor.tar.gz vendor
