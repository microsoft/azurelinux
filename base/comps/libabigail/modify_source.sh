#!/usr/bin/env bash
#
# libabigail: deterministic strip-and-repack of upstream `libabigail-2.9.tar.xz`
# with the PR30329 testsuite fixture set (which trips anti-malware scanning on
# the AZL RPM-signing pipeline) removed. The corresponding two entries in
# `tests/test-abidiff-exit.cc` that exercise the removed fixture are dropped
# by a companion overlay patch (see `libabigail.comp.toml`); this script does
# file removal only, no in-tarball source patching.
# Rationale lives in the comp.toml `replace-reason` field.
#
# Usage:   bash base/comps/libabigail/modify_source.sh
# Output:  base/build/work/scratch/libabigail/libabigail-2.9.tar.xz (+ .sha512)
# The upstream tarball is cached under a `.upstream` suffix; re-runs reuse it.

set -euo pipefail

# Pin umask so the extraction step below produces the same mode bits
# regardless of the caller's umask. With `--no-same-permissions`, tar ANDs
# each entry's mode against `~umask`, so e.g. umask 077 would silently strip
# group/other read bits and change the bytes of the repacked tarball. The
# repack step does not re-assert per-file modes (only owner/group/mtime), so
# this pin is what guarantees a byte-identical output across machines.
umask 022

# --- Constants --------------------------------------------------------------

readonly COMPONENT="libabigail"
readonly UPSTREAM_VERSION="2.9"
readonly UPSTREAM_FILENAME="${COMPONENT}-${UPSTREAM_VERSION}.tar.xz"
readonly UPSTREAM_TOPDIR="${COMPONENT}-${UPSTREAM_VERSION}"
readonly UPSTREAM_URL="https://mirrors.kernel.org/sourceware/libabigail/${UPSTREAM_FILENAME}"

readonly UPSTREAM_SHA512="5bdf5ec49a5931a61bf28317b41eee583d6277d00ac621b2d2a97bbc0d816c3662bcfe13a5ac7aeee11c947afb69a5a0a9a8015fcebad09965b45af9b1e23606"

# Directory (relative to ${UPSTREAM_TOPDIR}) to strip in its entirety. The
# PR30329 fixture set is a libabigail abidiff regression test built around a
# pair of stripped sqlite3 shared libraries + their separated debuginfo +
# dwz-multifile components. The two `libsqlite3.so.0.8.6.debug` separated-
# debuginfo files inside it are flagged as encrypted/unscannable payloads by
# the AV scanner ("packer_high_entropy:eod") in the AZL RPM-signing pipeline.
# We strip the whole PR30329/ directory (not just the two .debug files) so
# nothing in the tarball still references the missing pieces; the two
# corresponding `InOutSpec` entries in tests/test-abidiff-exit.cc are dropped
# by the companion overlay patch
# `tests-drop-PR30329-fixture-entries.patch` (see libabigail.comp.toml) so
# `make check` still passes.
readonly REMOVE_DIRS=(
    "tests/data/test-abidiff-exit/PR30329"
)

# Deterministic-repack mtime: 2020-01-01T00:00:00Z (1577836800).
# Any fixed epoch works; do not change without also bumping the
# `hash` in libabigail.comp.toml.
readonly DETERMINISTIC_MTIME="@1577836800"

# --- Work directory ---------------------------------------------------------

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../.." && pwd)"
WORKDIR="${REPO_ROOT}/base/build/work/scratch/${COMPONENT}"

mkdir -p "${WORKDIR}"
cd "${WORKDIR}"

echo "[1/5] Working in ${WORKDIR}"

# --- Download upstream ------------------------------------------------------
#
# The upstream tarball is cached under a `.upstream` suffix so that
# the repacked output written at the canonical `${UPSTREAM_FILENAME}`
# path below cannot clobber the cache on re-runs. Treat the cache
# as authoritative only after SHA-512 verification.

UPSTREAM_CACHE="${WORKDIR}/${UPSTREAM_FILENAME}.upstream"

if [[ ! -f "${UPSTREAM_CACHE}" ]]; then
    echo "[2/5] Downloading ${UPSTREAM_FILENAME} from ${UPSTREAM_URL}"
    # `--proto` / `--proto-redir` restrict the initial request *and* any
    # redirect target to HTTPS, so a downgrade to plain HTTP is refused.
    curl -fsSL --retry 3 \
        --proto '=https' --proto-redir '=https' \
        -o "${UPSTREAM_CACHE}.part" "${UPSTREAM_URL}"
    mv "${UPSTREAM_CACHE}.part" "${UPSTREAM_CACHE}"
else
    echo "[2/5] Using cached upstream tarball ${UPSTREAM_CACHE}"
fi

# --- Verify upstream SHA-512 ------------------------------------------------

echo "[3/5] Verifying upstream SHA-512"
COMPUTED_UPSTREAM_SHA512="$(sha512sum "${UPSTREAM_CACHE}" | awk '{print $1}')"
if [[ "${COMPUTED_UPSTREAM_SHA512}" != "${UPSTREAM_SHA512}" ]]; then
    echo "ERROR: upstream SHA-512 mismatch (cache may be corrupt; delete ${UPSTREAM_CACHE} and re-run)" >&2
    echo "  expected: ${UPSTREAM_SHA512}" >&2
    echo "  computed: ${COMPUTED_UPSTREAM_SHA512}" >&2
    exit 1
fi

# --- Extract + strip --------------------------------------------------------

echo "[4/5] Extracting and stripping ${#REMOVE_DIRS[@]} fixture dir(s) from ${UPSTREAM_TOPDIR}"
rm -rf "${WORKDIR}/${UPSTREAM_TOPDIR}"
# `--no-same-owner` / `--no-same-permissions` prevent tar from applying the
# archive's uid/gid/mode bits to the extracted tree. They are already the
# default for non-root users, but explicit hardening makes the script safe
# to run under sudo (where the defaults flip) and defends against any
# setuid/setgid bits or unexpected ownership in the upstream tarball.
# Deterministic owner/group is re-asserted in the repack step below.
tar -C "${WORKDIR}" --no-same-owner --no-same-permissions -xf "${UPSTREAM_CACHE}"
for REMOVE_DIR in "${REMOVE_DIRS[@]}"; do
    if [[ ! -d "${WORKDIR}/${UPSTREAM_TOPDIR}/${REMOVE_DIR}" ]]; then
        echo "ERROR: expected '${UPSTREAM_TOPDIR}/${REMOVE_DIR}' not present in upstream tarball" >&2
        exit 1
    fi
    echo "    stripping ${UPSTREAM_TOPDIR}/${REMOVE_DIR}"
    rm -rf "${WORKDIR}/${UPSTREAM_TOPDIR}/${REMOVE_DIR}"
done

# --- Repack deterministically -----------------------------------------------

echo "[5/5] Repacking deterministically as ${UPSTREAM_FILENAME}"
# Deterministic flags:
#   --sort=name             stable entry order
#   --owner=0 --group=0     no host uid/gid leakage
#   --numeric-owner         force numeric uid/gid
#   --mtime=@<epoch>        fixed mtime
#   --format=gnu            handles long paths deterministically
# LC_ALL=C pins sort collation so --sort=name is locale-independent.
# xz -9e -T1 picks max compression with single-threaded output (multi-threaded
# xz produces non-deterministic byte streams). The upstream tarball is .xz so
# we re-emit .xz to keep the filename and Source0 unchanged.
#
# Heads-up: this step is slow. libabigail-2.9 unpacks to ~990 MiB (the source
# tree is dominated by abidiff regression-test fixtures), so the single-
# threaded `xz -9e` pass below is on the order of minutes, not seconds.
# Reference timing on a 12th-gen Intel desktop (i9-12900K, 12 vCPUs): ~6-7
# minutes wall time for the full tar+xz pipeline (xz dominates; tar itself
# is a few seconds). The download (~500 MiB) and extract/strip steps before
# this finish in well under a minute on the same hardware. Slower CPUs can
# easily push this past 10 minutes -- so if it looks hung, give it time.
MODIFIED_TARBALL="${WORKDIR}/${UPSTREAM_FILENAME}"
rm -f "${MODIFIED_TARBALL}"
LC_ALL=C tar \
    -C "${WORKDIR}" \
    --sort=name \
    --owner=0 --group=0 --numeric-owner \
    --mtime="${DETERMINISTIC_MTIME}" \
    --format=gnu \
    -cf - "${UPSTREAM_TOPDIR}" \
    | xz -9e -T1 -c > "${MODIFIED_TARBALL}"

MODIFIED_SHA512="$(sha512sum "${MODIFIED_TARBALL}" | awk '{print $1}')"
echo "${MODIFIED_SHA512}  ${UPSTREAM_FILENAME}" > "${MODIFIED_TARBALL}.sha512"

echo
echo "================================================================"
echo "DONE"
echo "  modified tarball: ${WORKDIR}/${UPSTREAM_FILENAME}"
echo "  SHA512:           ${MODIFIED_SHA512}"
echo "================================================================"
echo
echo " To upload the modified tarball to the lookaside:"
echo "       az storage blob upload \\"
echo "           --auth-mode login \\"
echo "           --account-name azltempstaginglookaside \\"
echo "           --container-name repo \\"
echo "           --name \"pkgs_modified/${COMPONENT}/${UPSTREAM_FILENAME}/sha512/${MODIFIED_SHA512}/${UPSTREAM_FILENAME}\" \\"
echo "           --file \"${WORKDIR}/${UPSTREAM_FILENAME}\""
