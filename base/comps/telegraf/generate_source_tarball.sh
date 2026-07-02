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
# ---------------------------------------------------------------------------
# Reproducibility contract
# ---------------------------------------------------------------------------
# For supply-chain reasons this vendor archive must be reproducible (within
# toolchain tolerance). Every input that determines the archive's contents is
# HARD-CODED below, so this script alone documents exactly how the pinned
# vendor tarball was produced — there are no version/output arguments to get
# wrong or forget to record.
#
# By default the script downloads the upstream source tarball itself from the
# hard-coded SRC_TARBALL_URI, so it controls the entire source path — the package
# version (hard-coded below) is the only thing that varies. An optional path
# argument overrides the download with a pre-fetched local copy (e.g. an
# air-gapped or lookaside mirror). In both cases the tarball's SHA512 is verified
# against the hard-coded value before vendoring. This is not a security mechanism
# (the script can be edited); it exists to stop us from accidentally vendoring the
# wrong input.
#
# The produced archive's SHA512 is compared against the hard-coded expected
# value at the end. A mismatch is a non-fatal warning: it almost always means a
# toolchain difference (the Go toolchain writes vendor/modules.txt, so the Go
# version dominates), which is the "certain tolerance" for reproducibility. To
# reproduce the pinned hash byte-for-byte, use the canonical toolchain below.
#
# Canonical toolchain used to produce EXPECTED_VENDOR_SHA512:
#   go     : go1.26.4
#   tar    : tar (GNU tar) 1.35
#   bzip2  : bzip2 1.0.8
#
# Bumping the telegraf version: update PKG_VERSION, SRC_TARBALL_URI,
# SRC_TARBALL_SHA512, and (after a canonical-toolchain run) EXPECTED_VENDOR_SHA512
# below, then update the matching hashes in telegraf.comp.toml.
#
# Usage:
#   ./generate_source_tarball.sh                     # download the pinned tarball
#   ./generate_source_tarball.sh <path-to-tarball>   # use a pre-fetched copy

set -euo pipefail

# ---------------------------------------------------------------------------
# Hard-coded inputs — the complete, documented recipe
# ---------------------------------------------------------------------------
readonly PKG_NAME="telegraf"
readonly PKG_VERSION="1.38.2"

# Upstream source archive (the one argument must match this):
readonly SRC_TARBALL_NAME="telegraf-${PKG_VERSION}.tar.gz"
readonly SRC_TARBALL_URI="https://github.com/influxdata/telegraf/archive/v${PKG_VERSION}/${SRC_TARBALL_NAME}"
readonly SRC_TARBALL_SHA512="36c419978e98da9809e18865053399dd2198abc3d650f54424e3eb359ff8dfcb615f8b0a82dba484d03acfe5abe51a160a41ef486e5602f99400bd69e7afe48d"

# Expected output (verified, non-fatally, at the end). Reproducible with the
# canonical toolchain documented in the header; may differ otherwise.
readonly EXPECTED_VENDOR_SHA512="1108fe48086a7051c5cb89935c6de1c675c3ea8212a979d147ad0c03aef327c6234fa9eee292e4f9594ba9ec2cb757fc9eff46630aea43551bca3d948b30b27f"

# Output lands next to this script (not committed; upload to the lookaside).
readonly OUT_FOLDER="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

usage() {
    echo "Usage: ${0##*/} [path-to-${SRC_TARBALL_NAME}]" >&2
    echo >&2
    echo "Produces ${PKG_NAME}-${PKG_VERSION}-vendor.tar.bz2 (reproducible)." >&2
    echo "With no argument the pinned source tarball is downloaded from:" >&2
    echo "  ${SRC_TARBALL_URI}" >&2
    echo "Pass a path to use a pre-fetched local copy instead (offline override)." >&2
}

# ---------------------------------------------------------------------------
# Argument: an OPTIONAL path to a pre-fetched source tarball. With no argument
# the script downloads the tarball itself from the pinned SRC_TARBALL_URI, so it
# controls the entire source path; only the (hard-coded) package version varies.
# ---------------------------------------------------------------------------
if [ "$#" -gt 1 ]; then
    usage
    exit 1
fi
case "${1:-}" in
    -h|--help)
        usage
        exit 0
        ;;
esac
SRC_OVERRIDE="${1:-}"

echo "Package        -> ${PKG_NAME}-${PKG_VERSION}"
echo "Output folder  -> ${OUT_FOLDER}"

echo "Creating a tempdir."
WORKDIR=$(mktemp -d)
function cleanup {
    echo "Clean-up: removing tempdir (${WORKDIR})."
    rm -rf "${WORKDIR}"
}
trap cleanup EXIT

# ---------------------------------------------------------------------------
# Obtain the source tarball: use the offline override if given, otherwise
# download it from the pinned upstream URI. Either way it is hash-verified below.
# ---------------------------------------------------------------------------
if [ -n "${SRC_OVERRIDE}" ]; then
    if [ ! -f "${SRC_OVERRIDE}" ]; then
        echo "Error: source tarball not found: ${SRC_OVERRIDE}" >&2
        exit 1
    fi
    SRC_TARBALL="$(realpath "${SRC_OVERRIDE}")"
    echo "Source tarball -> ${SRC_TARBALL} (offline override)"
else
    SRC_TARBALL="${WORKDIR}/${SRC_TARBALL_NAME}"
    echo "Source tarball -> downloading ${SRC_TARBALL_URI}"
    curl -fSL --retry 3 --retry-delay 2 -o "${SRC_TARBALL}" "${SRC_TARBALL_URI}"
fi

# ---------------------------------------------------------------------------
# Verify the input against the hard-coded hash (accident prevention)
# ---------------------------------------------------------------------------
echo "Verifying input tarball against hard-coded SHA512..."
ACTUAL_SRC_SHA512="$(sha512sum "${SRC_TARBALL}" | awk '{print $1}')"
if [ "${ACTUAL_SRC_SHA512}" != "${SRC_TARBALL_SHA512}" ]; then
    echo "Error: input tarball SHA512 does not match the hard-coded value." >&2
    echo "  expected: ${SRC_TARBALL_SHA512}" >&2
    echo "  actual:   ${ACTUAL_SRC_SHA512}" >&2
    echo "  file:     ${SRC_TARBALL}" >&2
    echo >&2
    echo "This is not a security check; it prevents accidentally vendoring the wrong input." >&2
    echo "If you are intentionally bumping the version, update the hard-coded inputs in this" >&2
    echo "script (and telegraf.comp.toml) before re-running." >&2
    exit 1
fi
echo "  OK (${SRC_TARBALL_SHA512})"

# ---------------------------------------------------------------------------
# Toolchain report — the documented "tolerance" for reproducibility
# ---------------------------------------------------------------------------
echo "Toolchain (canonical: go1.26.4 / tar (GNU tar) 1.35 / bzip2 1.0.8):"
echo "  go    -> $(go version 2>/dev/null || echo 'NOT FOUND')"
echo "  tar   -> $(tar --version | head -1)"
echo "  bzip2 -> $(bzip2 --version 2>&1 | head -1)"

pushd "${WORKDIR}" > /dev/null

NAME_VER="${PKG_NAME}-${PKG_VERSION}"
# Fedora forge macros expect the vendor archive as %{archivename}-vendor.tar.bz2.
VENDOR_TARBALL="${OUT_FOLDER}/${NAME_VER}-vendor.tar.bz2"

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

# ---------------------------------------------------------------------------
# Verify the produced archive against the documented expected hash
# ---------------------------------------------------------------------------
ACTUAL_VENDOR_SHA512="$(sha512sum "${VENDOR_TARBALL}" | awk '{print $1}')"
echo "Telegraf vendored modules are available at (${VENDOR_TARBALL})."
echo "SHA512: ${ACTUAL_VENDOR_SHA512}"
if [ "${ACTUAL_VENDOR_SHA512}" = "${EXPECTED_VENDOR_SHA512}" ]; then
    echo "  MATCH: reproduces the pinned vendor archive."
else
    echo "  WARNING: does not match the pinned SHA512:" >&2
    echo "    expected: ${EXPECTED_VENDOR_SHA512}" >&2
    echo "    actual:   ${ACTUAL_VENDOR_SHA512}" >&2
    echo "  This usually means a toolchain difference (the Go version writes" >&2
    echo "  vendor/modules.txt). Reproduce with the canonical toolchain above before" >&2
    echo "  uploading, or update EXPECTED_VENDOR_SHA512 (and telegraf.comp.toml) if this" >&2
    echo "  is an intentional change." >&2
fi
