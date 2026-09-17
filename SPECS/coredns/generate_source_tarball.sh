#!/bin/bash
set -e

PKG_VERSION=""
SRC_TARBALL=""
OUT_FOLDER="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

PARAMS=""
while (( "$#" )); do
    case "$1" in
        --srcTarball)
        if [ -n "$2" ] && [ ${2:0:1} != "-" ]; then
            SRC_TARBALL=$2
            shift 2
        else
            echo "Error: Argument for $1 is missing" >&2
            exit 1
        fi
        ;;
        --outFolder)
        if [ -n "$2" ] && [ ${2:0:1} != "-" ]; then
            OUT_FOLDER=$2
            shift 2
        else
            echo "Error: Argument for $1 is missing" >&2
            exit 1
        fi
        ;;
        --pkgVersion)
        if [ -n "$2" ] && [ ${2:0:1} != "-" ]; then
            PKG_VERSION=$2
            shift 2
        else
            echo "Error: Argument for $1 is missing" >&2
            exit 1
        fi
        ;;
        -*|--*=)
        echo "Error: Unsupported flag $1" >&2
        exit 1
        ;;
        *)
        PARAMS="$PARAMS $1"
        shift
        ;;
  esac
done

if [ -z "$PKG_VERSION" ]; then
    echo "--pkgVersion parameter cannot be empty"
    exit 1
fi

tmpdir=$(mktemp -d)
function cleanup {
    rm -rf $tmpdir
}
trap cleanup EXIT

pushd $tmpdir > /dev/null

NAME_VER="coredns-$PKG_VERSION"
VENDOR_TARBALL="$OUT_FOLDER/$NAME_VER-vendor-v2.tar.gz"

echo "Unpacking source tarball..."
tar -xf $SRC_TARBALL

cd "$NAME_VER"
go mod edit -modfile=go.mod -require=google.golang.org/grpc@v1.83.2
go mod tidy
echo "Get vendored modules"
go mod vendor

echo "Tar vendored modules"
tar --sort=name \
    --mtime="2021-04-26 00:00Z" \
    --owner=0 --group=0 --numeric-owner \
    --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
    -cf "$VENDOR_TARBALL" vendor

popd > /dev/null
echo "coredns vendored modules are available at $VENDOR_TARBALL"
