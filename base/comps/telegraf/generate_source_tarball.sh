#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
#
# Vendors Telegraf's Go dependencies into a `vendor/` directory for azldev to archive.
#
# NOTE: This custom-source generator is invoked by azldev, never during rpmbuild.
# Run it through azldev's custom-source workflow; do not invoke it directly on the host.
# azldev provides the source archive and `/azldev-gen/output`, then packages the generated
# `vendor/` directory as `%{archivename}-vendor.tar.gz`. That archive is uploaded to the
# lookaside and pinned by hash in telegraf.comp.toml. The spec's %build consumes the
# prebuilt archive and never runs `go mod vendor`.
#
# The custom (minimal-plugin) build still vendors the *full* dependency tree so
# the build is hermetic and offline; only the selected plugins are compiled in
# (see %{buildtags} in telegraf.spec). Pruning vendor/ is intentionally NOT
# done — it would break reproducibility and `go mod verify`.
#
# ---------------------------------------------------------------------------
# Reproducibility contract
# ---------------------------------------------------------------------------
# For supply-chain traceability, every input that determines the vendored source
# tree is HARD-CODED below. This script documents exactly how it was produced —
# there are no version/output arguments to get wrong or forget to record.
#
# The script expects the upstream source tarball to already be present in the current
# working directory. Its SHA512 is verified against the hard-coded value
# before vendoring. This is not a security mechanism (the script can be edited); it
# exists to stop us from accidentally vendoring the wrong input.
#
# Canonical toolchain used to vendor dependencies:
#   go  : go1.26.4
#
# Bumping the telegraf version: update PKG_VERSION and SRC_TARBALL_SHA512 below,
# then update the matching hashes in telegraf.comp.toml.
#
# Invocation:
#   azldev comp prepare-sources -p telegraf -o <output-directory>

set -euo pipefail

# ---------------------------------------------------------------------------
# Hard-coded inputs — the complete, documented recipe
# ---------------------------------------------------------------------------
readonly PKG_NAME="telegraf"
readonly PKG_VERSION="1.38.2"

# Upstream source archive — expected in the current working directory.
readonly SRC_TARBALL_NAME="telegraf-${PKG_VERSION}.tar.gz"
readonly SRC_TARBALL_SHA512="36c419978e98da9809e18865053399dd2198abc3d650f54424e3eb359ff8dfcb615f8b0a82dba484d03acfe5abe51a160a41ef486e5602f99400bd69e7afe48d"

# azldev's custom source workflow archives the `vendor/` directory placed here.
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
# Locate the source tarball — expected in the current working directory.
# ---------------------------------------------------------------------------
SRC_TARBALL="${PWD}/${SRC_TARBALL_NAME}"
if [ ! -f "${SRC_TARBALL}" ]; then
    echo "Error: source tarball not found: ${SRC_TARBALL}" >&2
    echo "Place ${SRC_TARBALL_NAME} in the current working directory and re-run." >&2
    exit 1
fi
echo "Source tarball -> ${SRC_TARBALL}"

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
echo "Toolchain (canonical: go1.26.4):"
echo "  go -> $(go version 2>/dev/null || echo 'NOT FOUND')"

pushd "${WORKDIR}" > /dev/null

NAME_VER="${PKG_NAME}-${PKG_VERSION}"

echo "Unpacking the source tarball."
tar -xf "${SRC_TARBALL}"

cd "${NAME_VER}"

echo "Getting the vendored modules."
go mod vendor

echo "Moving vendor directory to output folder."
mkdir -p "${OUT_FOLDER}"
mv vendor "${OUT_FOLDER}/"

popd > /dev/null

echo "Vendor directory is available at ${OUT_FOLDER}/vendor."
