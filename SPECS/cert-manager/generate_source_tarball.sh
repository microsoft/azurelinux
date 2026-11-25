#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Quit on failure
set -eo pipefail
umask 022
export LC_ALL=C
export GOWORK=off GOTOOLCHAIN=local

PKG_VERSION=""
SRC_TARBALL=""
VENDOR_VERSION="4"
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
OUT_FOLDER="${SCRIPT_DIR}"

# parameters:
#
# --srcTarball  : src tarball file
#                 this file contains the 'initial' source code of the component
#                 and should be replaced with the new/modified src code
# --outFolder   : folder where to copy the new tarball(s)
# --pkgVersion  : package version
# --vendorVersion : vendor archive revision (default: 4)
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
        if [ -n "$2" ] && [ "${2:0:1}" != "-" ]; then
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
        PARAMS="${PARAMS} $1"
        shift
        ;;
  esac
done

echo "--srcTarball   -> ${SRC_TARBALL}"
echo "--outFolder    -> ${OUT_FOLDER}"
echo "--pkgVersion   -> ${PKG_VERSION}"
echo "--vendorVersion -> ${VENDOR_VERSION}"

if [ -z "${SRC_TARBALL}" ]; then
    echo "--srcTarball parameter cannot be empty"
    exit 1
fi

SRC_TARBALL=$(realpath -e "${SRC_TARBALL}")

if [ -z "${PKG_VERSION}" ]; then
    echo "--pkgVersion parameter cannot be empty"
    exit 1
fi

if [[ ! "${VENDOR_VERSION}" =~ ^[0-9]+$ ]]; then
    echo "--vendorVersion must be numeric" >&2
    exit 1
fi

mkdir -p "${OUT_FOLDER}"
OUT_FOLDER=$(realpath "${OUT_FOLDER}")

echo "-- create temp folder"
tmpdir=$(mktemp -d)
function cleanup {
    echo "+++ cleanup -> remove ${tmpdir}"
    rm -rf -- "${tmpdir}"
}
trap cleanup EXIT

pushd "${tmpdir}" > /dev/null

echo "Unpacking source tarball..."
tar -xf "${SRC_TARBALL}"

cd "cert-manager-${PKG_VERSION}"

# Preserve the existing Kubernetes and gRPC dependency upgrades.
patch --batch --forward --fuzz=0 -p1 < "${SCRIPT_DIR}/CVE-2026-84445.patch"

# We need to individually vendor each cmd we will build
vendor_directories=()

echo "Get vendored modules for each command"
for command in acmesolver controller cainjector ctl webhook; do
    case "${command}" in
        controller|webhook|ctl)
            requirements=(
                -require=go.opentelemetry.io/otel@v1.47.0
                -require=go.opentelemetry.io/otel/metric@v1.47.0
                -require=go.opentelemetry.io/otel/trace@v1.47.0
            )
            if [ "${command}" != "ctl" ]; then
                requirements+=(
                    -require=google.golang.org/grpc@v1.83.2
                    -require=go.opentelemetry.io/otel/sdk@v1.47.0
                )
            fi
            go -C "cmd/${command}" mod edit -go=1.26.0 -toolchain=none "${requirements[@]}"
            go -C "cmd/${command}" mod tidy -go=1.26.0
            ;;
    esac
    echo "Vendoring 'cmd/${command}'"
    go -C "cmd/${command}" mod vendor
    vendor_directories+=("cmd/${command}/vendor")
done

echo "Tar vendored modules"
VENDOR_TARBALL="${OUT_FOLDER}/cert-manager-${PKG_VERSION}-vendor-v${VENDOR_VERSION}.tar.gz"
tar  --sort=name \
     --mtime="2021-04-26 00:00Z" \
     --owner=0 --group=0 --numeric-owner \
     --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
     -cf - "${vendor_directories[@]}" | gzip -n > "${VENDOR_TARBALL}"

popd > /dev/null
echo "cert-manager vendored modules are available at ${VENDOR_TARBALL}"
sha256sum "${VENDOR_TARBALL}"
