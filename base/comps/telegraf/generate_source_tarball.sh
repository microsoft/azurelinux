#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
#
# Generates a reproducible vendored Go-module tarball for telegraf.
#
# NOTE: This is an out-of-band maintainer tool — it is NEVER invoked during rpmbuild.
# It is run by hand (or by the sources-upload pipeline) to (re)produce the vendor
# archive, which is then uploaded to the lookaside and pinned by hash as
# `Source1: %{archivename}-vendor.tar.bz2`. The spec's %build consumes that prebuilt
# archive; it never runs `go mod vendor`. Consequently the pinned timestamp here only
# affects reproducibility of this generation step, not the package build.
#
# The custom (minimal-plugin) build still vendors the *full* dependency tree so
# the build is hermetic and offline; only the selected plugins are compiled in
# (see %{buildtags} in telegraf.spec). Pruning vendor/ is intentionally NOT
# done — it would break reproducibility and `go mod verify`.
#
# Usage:
#   ./generate_source_tarball.sh --srcTarball <path> --pkgVersion <version> [--outFolder <dir>]

set -e

get_param() {
    if [ -n "${2}" ] && [ "${2:0:1}" != "-" ]; then
        echo "${2}"
    else
        echo "Error: argument for (${1}) is missing." >&2
        return 1
    fi
}

PKG_VERSION=""
SRC_TARBALL=""
OUT_FOLDER="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

while (( "$#" )); do
    case "${1}" in
        --srcTarball)
            SRC_TARBALL="$(get_param "${1}" "${2}")"
            shift 2
            ;;
        --outFolder)
            OUT_FOLDER="$(get_param "${1}" "${2}")"
            shift 2
            ;;
        --pkgVersion)
            PKG_VERSION="$(get_param "${1}" "${2}")"
            shift 2
            ;;
        -*)
            echo "Error: unsupported flag ${1}." >&2
            exit 1
            ;;
        *)
            echo "Error: unexpected argument ${1}." >&2
            exit 1
            ;;
    esac
done

echo "--srcTarball   -> ${SRC_TARBALL}"
echo "--outFolder    -> ${OUT_FOLDER}"
echo "--pkgVersion   -> ${PKG_VERSION}"

if [ -z "${PKG_VERSION}" ]; then
    echo "Error: --pkgVersion parameter cannot be empty." >&2
    exit 1
fi

if [ ! -f "${SRC_TARBALL}" ]; then
    echo "Error: --srcTarball is not a file." >&2
    exit 1
fi

SRC_TARBALL="$(realpath "${SRC_TARBALL}")"
# Create the output folder up front so realpath can resolve the (not-yet-existing)
# vendor archive path below, and so a nested --outFolder works on a clean tree.
mkdir -p "${OUT_FOLDER}"
OUT_FOLDER="$(realpath "${OUT_FOLDER}")"

echo "Creating a tempdir."
TMPDIR=$(mktemp -d)
function cleanup {
    echo "Clean-up: removing tempdir (${TMPDIR})."
    rm -rf "${TMPDIR}"
}
trap cleanup EXIT

pushd "${TMPDIR}" > /dev/null

NAME_VER="telegraf-${PKG_VERSION}"
# Fedora forge macros expect the vendor archive as %{archivename}-vendor.tar.bz2.
VENDOR_TARBALL="$(realpath "${OUT_FOLDER}/${NAME_VER}-vendor.tar.bz2")"

echo "Unpacking the source tarball."
tar -xf "${SRC_TARBALL}"

cd "${NAME_VER}"

echo "Getting the vendored modules."
go mod vendor


echo "Tar vendored modules (deterministic flags for reproducibility)."
# Pin every archived timestamp to the Unix epoch (@0 = 1970-01-01): --mtime sets it and
# --clamp-mtime caps anything newer. --mode normalizes permission bits (0644 files / 0755 dirs)
# so the hash is independent of the maintainer's umask. Combined with --sort=name, fixed
# owner/group and stripped pax atime/ctime, the tarball's hash depends solely on file content,
# independent of the host clock, locale, umask, or how the source was unpacked.
tar  --sort=name \
     --mode='go-w,u+rw,a+rX' \
     --mtime="@0" --clamp-mtime \
     --owner=0 --group=0 --numeric-owner \
     --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
     -cjf "${VENDOR_TARBALL}" vendor

popd > /dev/null

echo "Telegraf vendored modules are available at (${VENDOR_TARBALL})."
echo "SHA512: $(sha512sum "${VENDOR_TARBALL}")."
