#!/usr/bin/env bash
#
# espeak-ng: deterministic strip-and-repack of upstream `espeak-ng-1.51.1.tar.gz`
# with the demo file that trips anti-malware scanning on the AZL RPM-signing
# pipeline removed. Rationale lives in the comp.toml `replace-reason` field.
#
# Usage:   bash base/comps/espeak-ng/modify_source.sh
# Output:  base/build/work/scratch/espeak-ng/espeak-ng-1.51.1.tar.gz (+ .sha512)
# The upstream tarball is cached under a `.upstream` suffix; re-runs reuse it.

set -euo pipefail

# --- Constants --------------------------------------------------------------

readonly COMPONENT="espeak-ng"
readonly UPSTREAM_VERSION="1.51.1"
readonly UPSTREAM_FILENAME="espeak-ng-${UPSTREAM_VERSION}.tar.gz"
readonly UPSTREAM_TOPDIR="espeak-ng-${UPSTREAM_VERSION}"
readonly UPSTREAM_URL="https://github.com/espeak-ng/espeak-ng/archive/${UPSTREAM_VERSION}/${UPSTREAM_FILENAME}"

readonly UPSTREAM_SHA512="291958c2d3a1e38f9006416347d40d98be7afc84057475c9394788610897d19c02fabc32ebb8efa6dac291d106f97bf63907d0688ef7d93ea24439cba22392d1"

# Paths (relative to ${UPSTREAM_TOPDIR}) to strip. Each is a demo asset
# flagged as malicious by anti-malware scanning on the AZL RPM-signing
# pipeline. The `chromium_extension/` directory is a sample browser-extension
# demo that is not referenced by the spec or built into any binary RPM, so
# stripping fixtures here is functionally inert.
#
#   - chromium_extension/index.php
#       A 10-line demo PHP shim for the sample Chromium extension that
#       forwards POST-ed shell commands via `passthru($_POST["espeakng"])`.
#       AV scanners flag it as PHP/Webshell.NWM trojan (correctly: by design
#       it executes arbitrary attacker-supplied shell input).
readonly REMOVE_PATHS=(
    "chromium_extension/index.php"
)

# Deterministic-repack mtime: 2020-01-01T00:00:00Z (1577836800).
# Any fixed epoch works; do not change without also bumping the
# `hash` in espeak-ng.comp.toml.
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
# `--no-same-owner` / `--no-same-permissions` prevent tar from applying the
# archive's uid/gid/mode bits to the extracted tree. They are already the
# default for non-root users, but explicit hardening makes the script safe
# to run under sudo (where the defaults flip) and defends against any
# setuid/setgid bits or unexpected ownership in the upstream tarball.
# `-z` requests gzip decompression explicitly rather than relying on tar's
# magic-byte auto-detection (GNU tar default, but not POSIX/BSD tar).
# Deterministic owner/group is re-asserted in the repack step below.
tar -C "${WORKDIR}" --no-same-owner --no-same-permissions -xzf "${UPSTREAM_CACHE}"
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
echo " To upload the modified tarball to the lookaside (both paths):"
for SUBPATH in pkgs pkgs_modified; do
    echo "       az storage blob upload \\"
    echo "           --auth-mode login \\"
    echo "           --account-name azltempstaginglookaside \\"
    echo "           --container-name repo \\"
    echo "           --name \"${SUBPATH}/${COMPONENT}/${UPSTREAM_FILENAME}/sha512/${MODIFIED_SHA512}/${UPSTREAM_FILENAME}\" \\"
    echo "           --file \"${WORKDIR}/${UPSTREAM_FILENAME}\""
    echo
done
