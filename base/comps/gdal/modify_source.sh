#!/usr/bin/env bash
#
# gdal: deterministic strip-and-repack of upstream `gdalautotest-3.11.5.tar.gz`
# with the autotest fixture that trips anti-malware scanning on the AZL
# RPM-signing pipeline removed. Rationale lives in the comp.toml `replace-reason` field.
#
# Usage:   bash base/comps/gdal/modify_source.sh
# Output:  base/build/work/scratch/gdal/gdalautotest-3.11.5.tar.gz (+ .sha512)
# The upstream tarball is cached under a `.upstream` suffix; re-runs reuse it.

set -euo pipefail

# --- Constants --------------------------------------------------------------

readonly COMPONENT="gdal"
readonly UPSTREAM_VERSION="3.11.5"
readonly UPSTREAM_FILENAME="gdalautotest-${UPSTREAM_VERSION}.tar.gz"
readonly UPSTREAM_TOPDIR="gdalautotest-${UPSTREAM_VERSION}"
readonly UPSTREAM_URL="https://download.osgeo.org/gdal/${UPSTREAM_VERSION}/${UPSTREAM_FILENAME}"

readonly UPSTREAM_SHA512="cb97beed516fa74d3744da62e8cf0c1438d32063ec8bc5fea5b8a4bc3c7097553bb4045766e7d77f7c87456f44b37aae0961ff73b1a5f8cd4ad1ecb5351c3986"

# Paths (relative to ${UPSTREAM_TOPDIR}) to strip. Each is a gdalautotest
# fixture flagged as an encrypted or unscannable payload by anti-malware
# scanning on the AZL RPM-signing pipeline. The autotest tarball is extracted
# in %prep but the %check section is a no-op (exits 0; gcore tests OOM-kill
# the build POD), so stripping fixtures is functionally inert.
#
#   - gcore/data/zero_5GB_sozip_of_sozip.zip
#       A SOZip-of-SOZip test fixture: a ZIP containing zero_5GB.bin.zip,
#       which in turn wraps a sparse 5 GiB all-zero file. AV scanners flag
#       the nested archive (and the layered re-decompressions of the outer
#       .tar.gz wrapper) as a Trojan.
readonly REMOVE_PATHS=(
    "gcore/data/zero_5GB_sozip_of_sozip.zip"
)

# Deterministic-repack mtime: 2020-01-01T00:00:00Z (1577836800).
# Any fixed epoch works; do not change without also bumping the
# `hash` in gdal.comp.toml.
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

echo "[4/5] Extracting and stripping ${#REMOVE_PATHS[@]} fixture(s) from ${UPSTREAM_TOPDIR}"
rm -rf "${WORKDIR}/${UPSTREAM_TOPDIR}"
# `--no-same-owner` / `--no-same-permissions` prevent tar from applying the
# archive's uid/gid/mode bits to the extracted tree. They are already the
# default for non-root users, but explicit hardening makes the script safe
# to run under sudo (where the defaults flip) and defends against any
# setuid/setgid bits or unexpected ownership in the upstream tarball.
# Deterministic owner/group is re-asserted in the repack step below.
tar -C "${WORKDIR}" --no-same-owner --no-same-permissions -xf "${UPSTREAM_CACHE}"
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
# gzip -n strips the original filename and mtime from the gzip header,
# which would otherwise vary between runs. -9 picks max compression.
MODIFIED_TARBALL="${WORKDIR}/${UPSTREAM_FILENAME}"
rm -f "${MODIFIED_TARBALL}"
LC_ALL=C tar \
    -C "${WORKDIR}" \
    --sort=name \
    --owner=0 --group=0 --numeric-owner \
    --mtime="${DETERMINISTIC_MTIME}" \
    --format=gnu \
    -cf - "${UPSTREAM_TOPDIR}" \
    | gzip -n -9 -c > "${MODIFIED_TARBALL}"

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
