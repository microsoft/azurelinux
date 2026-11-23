#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
#
# Vendors gosu's Go dependencies into a `vendor/` directory for azldev to archive.
#
# NOTE: This custom-source generator is invoked by azldev, never during rpmbuild.
# Run it through azldev's custom-source workflow; do not invoke it directly on the host.
# azldev provides the source archive and `/azldev-gen/output`, then packages the generated
# `vendor/` directory as `%{archivename}-vendor.tar.gz`.

set -euo pipefail

readonly PKG_NAME="gosu"
readonly PKG_VERSION="1.19"
readonly SRC_TARBALL_NAME="gosu-${PKG_VERSION}.tar.gz"
readonly SRC_TARBALL_SHA512="00ef15d982eb58d62cf67c6517d9560bb92cff5d1347f16b03e03bb3a6da08f2b85e8c3e6c23ae644f174f8da8e9154dcfe4ee379f894882e92b3602d7d079ed"
readonly OUT_FOLDER="/azldev-gen/output"

usage() {
    echo "This generator is invoked by azldev's custom-source workflow." >&2
    echo "Do not run ${0##*/} directly on the host." >&2
    echo >&2
    echo "azldev provides ${SRC_TARBALL_NAME} and archives ${OUT_FOLDER}/vendor as" >&2
    echo "${PKG_NAME}-${PKG_VERSION}-vendor.tar.gz." >&2
}

if [ "$#" -gt 0 ]; then
    case "${1}" in
        -h|--help) usage; exit 0 ;;
        *) echo "Error: unexpected argument '${1}'" >&2; usage; exit 1 ;;
    esac
fi

WORKDIR=$(mktemp -d)
cleanup() {
    rm -rf "${WORKDIR}"
}
trap cleanup EXIT

SRC_TARBALL="${PWD}/${SRC_TARBALL_NAME}"
if [ ! -f "${SRC_TARBALL}" ]; then
    echo "Error: source tarball not found: ${SRC_TARBALL}" >&2
    exit 1
fi

ACTUAL_SRC_SHA512="$(sha512sum "${SRC_TARBALL}" | awk '{print $1}')"
if [ "${ACTUAL_SRC_SHA512}" != "${SRC_TARBALL_SHA512}" ]; then
    echo "Error: input tarball SHA512 does not match the hard-coded value." >&2
    echo "  expected: ${SRC_TARBALL_SHA512}" >&2
    echo "  actual:   ${ACTUAL_SRC_SHA512}" >&2
    exit 1
fi

echo "Toolchain:"
echo "  go -> $(go version 2>/dev/null || echo 'NOT FOUND')"

pushd "${WORKDIR}" > /dev/null
tar -xf "${SRC_TARBALL}"
cd "${PKG_NAME}-${PKG_VERSION}"
go mod vendor
mkdir -p "${OUT_FOLDER}"
mv vendor "${OUT_FOLDER}/"
popd > /dev/null
