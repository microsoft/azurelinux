#!/usr/bin/env bash
#
# kf6-karchive: deterministic strip-and-repack of upstream `karchive-6.23.0.tar.xz`
# with autotest fixtures that trip anti-malware scanning on the AZL
# RPM-signing pipeline removed. Rationale lives in the comp.toml `replace-reason` field.
#
# Usage:   bash base/comps/kf6-karchive/modify_source.sh
# Output:  base/build/work/scratch/kf6-karchive/karchive-6.23.0.tar.xz (+ .sha512)
# The upstream tarball is cached under a `.upstream` suffix; re-runs reuse it.

set -euo pipefail

# --- Constants --------------------------------------------------------------

readonly COMPONENT="kf6-karchive"
readonly UPSTREAM_VERSION="6.23.0"
# KDE stable URL is .../stable/frameworks/<MAJOR>.<MINOR>/<filename>.
readonly UPSTREAM_MAJMIN="${UPSTREAM_VERSION%.*}"
readonly UPSTREAM_FILENAME="karchive-${UPSTREAM_VERSION}.tar.xz"
readonly UPSTREAM_TOPDIR="karchive-${UPSTREAM_VERSION}"
readonly UPSTREAM_URL="https://download.kde.org/stable/frameworks/${UPSTREAM_MAJMIN}/${UPSTREAM_FILENAME}"

readonly UPSTREAM_SHA512="28e10e9de84304a0d025fd1304738de2fc15812cbca33c77ed174e3ec614ebd4b2ff2896380b600f978682cdecdb464e1b8bd0abacde1d3d92197d18d6957cd8"

# Paths (relative to ${UPSTREAM_TOPDIR}) to strip. Each is a karchive autotest
# fixture flagged as an encrypted or unscannable payload by anti-malware
# scanning on the AZL RPM-signing pipeline. The autotests are not built or
# run in our spec (no %check, BUILD_TESTING is off), so stripping fixtures
# is functionally inert.
#
#   - autotests/data/password_protected.7z
#       Deliberately password-protected 7-Zip archive.
#   - autotests/data/zip64_extra_zip64_size_first.zip.gz
#       Gzipped ZIP64 edge-case fixture; the scanner decompresses the .gz
#       wrapper and the inner .zip trips its detector.
readonly REMOVE_PATHS=(
    "autotests/data/password_protected.7z"
    "autotests/data/zip64_extra_zip64_size_first.zip.gz"
)

# Deterministic-repack mtime: 2020-01-01T00:00:00Z (1577836800).
# Any fixed epoch works; do not change without also bumping the
# `hash` in kf6-karchive.comp.toml.
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
    curl -fsSL --retry 3 -o "${UPSTREAM_CACHE}.part" "${UPSTREAM_URL}"
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

echo "[4/5] Extracting and stripping ${#REMOVE_PATHS[@]} fixture(s) from ${UPSTREAM_TOPDIR}"
rm -rf "${WORKDIR}/${UPSTREAM_TOPDIR}"
tar -C "${WORKDIR}" -xf "${UPSTREAM_CACHE}"
for REMOVE_PATH in "${REMOVE_PATHS[@]}"; do
    if [[ ! -f "${WORKDIR}/${UPSTREAM_TOPDIR}/${REMOVE_PATH}" ]]; then
        echo "ERROR: expected '${UPSTREAM_TOPDIR}/${REMOVE_PATH}' not present in upstream tarball" >&2
        exit 1
    fi
    echo "    stripping ${UPSTREAM_TOPDIR}/${REMOVE_PATH}"
    rm -f "${WORKDIR}/${UPSTREAM_TOPDIR}/${REMOVE_PATH}"
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
# xz -T 1 forces single-threaded encoding; multi-threaded xz splits
# the stream into non-reproducible blocks unless --block-size is
# also pinned, and the savings are marginal for a tarball this size.
MODIFIED_TARBALL="${WORKDIR}/${UPSTREAM_FILENAME}"
rm -f "${MODIFIED_TARBALL}"
LC_ALL=C tar \
    -C "${WORKDIR}" \
    --sort=name \
    --owner=0 --group=0 --numeric-owner \
    --mtime="${DETERMINISTIC_MTIME}" \
    --format=gnu \
    -cf - "${UPSTREAM_TOPDIR}" \
    | xz -T 1 -9 -c > "${MODIFIED_TARBALL}"

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
