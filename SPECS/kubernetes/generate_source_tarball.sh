#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Quit on failure
set -e

PKG_VERSION=""
SRC_TARBALL=""
VENDOR_VERSION=""
OUT_FOLDER="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

GRPC_VERSION="v1.83.2"
CEL_GO_VERSION="v0.31.0"
X_CRYPTO_VERSION="v0.57.0"
# otel/sdk must be pinned too; MVS alone leaves it at v1.44.0.
OTEL_VERSION="v1.47.0"
GO_DIRECTIVE="1.26.0"

# parameters:
#
# --srcTarball    : src tarball file
#                   this file contains the 'initial' source code of the component
#                   and should be replaced with the new/modified src code
# --outFolder     : folder where to copy the new tarball(s)
# --pkgVersion    : package version
# --vendorVersion : vendor tarball version; must match the -vN suffix of
#                   Source2 in kubernetes.spec (e.g. 2 -> kubernetes-v<ver>-vendor-v2.tar.gz)
#
# Usage: ./generate_source_tarball.sh --srcTarball <tarball> --pkgVersion <ver> --vendorVersion <n> [--outFolder <dir>]
#
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
        --vendorVersion)
        if [ -n "$2" ] && [ ${2:0:1} != "-" ]; then
            VENDOR_VERSION=$2
            shift 2
        else
            echo "Error: Argument for $1 is missing" >&2
            exit 1
        fi
        ;;
        -*|--*=) # unsupported flags
        echo "Error: Unsupported flag $1" >&2
        exit 1
        ;;
        *) # preserve positional arguments
        PARAMS="$PARAMS $1"
        shift
        ;;
  esac
done

echo "--srcTarball      -> $SRC_TARBALL"
echo "--outFolder       -> $OUT_FOLDER"
echo "--pkgVersion      -> $PKG_VERSION"
echo "--vendorVersion   -> $VENDOR_VERSION"

if [ -z "$PKG_VERSION" ]; then
    echo "--pkgVersion parameter cannot be empty"
    exit 1
fi

if [ -z "$VENDOR_VERSION" ]; then
    echo "--vendorVersion parameter cannot be empty"
    exit 1
fi

echo "-- create temp folder"
tmpdir=$(mktemp -d)
function cleanup {
    echo "+++ cleanup -> remove $tmpdir"
    rm -rf $tmpdir
}
trap cleanup EXIT

SRC_TARBALL=$(readlink -f "$SRC_TARBALL")
OUT_FOLDER=$(readlink -f "$OUT_FOLDER")

TARBALL_FOLDER="$tmpdir/tarballFolder"
mkdir -p $TARBALL_FOLDER

pushd $TARBALL_FOLDER > /dev/null

PKG_NAME="kubernetes"
VENDOR_TARBALL="$OUT_FOLDER/$PKG_NAME-v$PKG_VERSION-vendor-v$VENDOR_VERSION.tar.gz"

echo "Unpacking source tarball..."
# The kubernetes source tarball has no top-level directory.
tar -xf $SRC_TARBALL

echo "Bumping vendored modules..."
# kubernetes is a Go workspace: the root module plus 30 staging modules under
# staging/src/k8s.io. Every module that pins one of these dependencies has to be
# raised together, otherwise the workspace resolves a mixture of versions.
go mod edit -go=$GO_DIRECTIVE go.mod
go mod edit -require=google.golang.org/grpc@$GRPC_VERSION \
            -require=github.com/google/cel-go@$CEL_GO_VERSION \
            -require=golang.org/x/crypto@$X_CRYPTO_VERSION \
            -require=go.opentelemetry.io/otel@$OTEL_VERSION \
            -require=go.opentelemetry.io/otel/sdk@$OTEL_VERSION go.mod

for module in staging/src/k8s.io/*/; do
    go mod edit -go=$GO_DIRECTIVE "$module/go.mod"
    grep -q 'google.golang.org/grpc v' "$module/go.mod" && \
        go mod edit -require=google.golang.org/grpc@$GRPC_VERSION "$module/go.mod"
    grep -q 'github.com/google/cel-go v' "$module/go.mod" && \
        go mod edit -require=github.com/google/cel-go@$CEL_GO_VERSION "$module/go.mod"
    grep -q 'golang.org/x/crypto v' "$module/go.mod" && \
        go mod edit -require=golang.org/x/crypto@$X_CRYPTO_VERSION "$module/go.mod"
    grep -q 'go.opentelemetry.io/otel v' "$module/go.mod" && \
        go mod edit -require=go.opentelemetry.io/otel@$OTEL_VERSION "$module/go.mod"
    grep -q 'go.opentelemetry.io/otel/sdk v' "$module/go.mod" && \
        go mod edit -require=go.opentelemetry.io/otel/sdk@$OTEL_VERSION "$module/go.mod"
done

go work edit -go=$GO_DIRECTIVE

echo "Vendor go modules..."
GOFLAGS=-mod=mod go mod tidy
rm -rf vendor
# "go work vendor" (not "go mod vendor") is required here: the latter ignores the
# workspace and copies the 30 staging modules into vendor/, which upstream does not do.
go work vendor

echo ""
echo "========================="
echo "Tar vendored modules"
tar  --sort=name \
     --mtime="2021-04-26 00:00Z" \
     --owner=0 --group=0 --numeric-owner \
     --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
     -czf "$VENDOR_TARBALL" vendor

popd > /dev/null
echo "$PKG_NAME vendored modules are available at $VENDOR_TARBALL"
