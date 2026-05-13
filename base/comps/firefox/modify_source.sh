#!/usr/bin/env bash
#
# Reproducibly rebuild firefox-<VERSION>.source.tar.xz with a curated set of
# files stripped out (see REMOVE_PATHS below). These are upstream Mozilla
# test fixtures flagged by the AZL RPM signing pipeline as obfuscated /
# malware-like content (e.g. an obfuscated Windows executable used only by
# media-sniffer unit tests, crashtest HTML that trips malware scanners,
# etc.). Such content blocks the SRPM from being published.
#
# This script is fully deterministic: given the same upstream tarball and
# the same REMOVE_PATHS list, it always produces a byte-identical output
# (so the SHA-512 in the `source-files` entry of firefox.comp.toml is
# stable).
#
# Determinism is achieved by:
#   * tar --sort=name  (stable file order, independent of FS readdir order)
#   * --owner=0 --group=0 --numeric-owner  (no host-specific uid/gid)
#   * --mtime=@<fixed epoch>  (fixed mtime for every entry)
#   * --format=gnu  (handles long paths > 100/255 bytes via ././@LongLink;
#                    ustar would silently drop Firefox test files with very
#                    long names, breaking the build. gnu is deterministic.)
#   * xz -T 4 -9 --block-size=256MiB  (deterministic: output depends only on
#                    these two values, not on host CPU count. Changing -T or
#                    --block-size changes the SHA-512, so bump the hash in
#                    firefox.comp.toml if you change them. -e is omitted for
#                    speed; size penalty is ~1-2%.)
#   * LC_ALL=C  (locale-independent sort)
#
# Usage:
#   modify_source.sh [--workdir DIR] [--keep]
#
# To bump the package version: edit VERSION and UPSTREAM_SHA512 below in
# lockstep, then re-run. There is no CLI flag for VERSION because the
# repacked tarball's hash and the upstream-verification hash are version-
# specific, so they must change together (and the comp.toml hash must be
# updated too).
#
# Output: <workdir>/firefox-<VERSION>.azl.source.tar.xz  (+ .sha512)

set -euo pipefail

# Pinned package version. To bump, also update UPSTREAM_SHA512 below and
# the `hash` field in firefox.comp.toml.
VERSION="148.0"
KEEP=0
# Default workdir lives under the project work dir to comply with AGENTS.md.
# Convention from Task 19805: base/build/work/scratch/<component>/.
WORKDIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)/base/build/work/scratch/firefox"

while [[ $# -gt 0 ]]; do
    case "$1" in
        --workdir) WORKDIR="$2"; shift 2 ;;
        --keep)    KEEP=1; shift ;;
        -h|--help)
            sed -n '2,22p' "$0"; exit 0 ;;
        *) echo "unknown arg: $1" >&2; exit 2 ;;
    esac
done

UPSTREAM_NAME="firefox-${VERSION}.source.tar.xz"
OUTPUT_NAME="firefox-${VERSION}.azl.source.tar.xz"
TOPDIR="firefox-${VERSION}"

# Files (relative to ${TOPDIR}) to strip from the upstream tarball. These trip
# the AZL RPM signing pipeline (obfuscated/malware-flagged content in upstream
# test fixtures). Add new entries here as they are discovered. Every change
# to this list alters the repacked SHA-512 — bump the `hash` in
# firefox.comp.toml accordingly.
REMOVE_PATHS=(
    "toolkit/components/mediasniffer/test/unit/data/ff-inst.exe"
    "dom/base/crashtests/607222.html"
)

# Known upstream SHA-512 (from specs/f/firefox/sources). Bump when version changes.
UPSTREAM_SHA512="b0e862091f3a07a02890f6414e77b433893364a8beaf522d440e97ed0060c9b14bdb2fffdecdf12dca849efce8c57d95a534b23e04259d83a96ee8f29e078349"

# Fixed mtime for every entry in the repacked tarball:
# 2020-01-01T00:00:00Z (1577836800). Any fixed epoch works; do not change
# without also bumping the `hash` in firefox.comp.toml.
MTIME_EPOCH=1577836800

UPSTREAM_URL="https://archive.mozilla.org/pub/firefox/releases/${VERSION}/source/${UPSTREAM_NAME}"

mkdir -p "${WORKDIR}"
cd "${WORKDIR}"

echo "[1/5] downloading ${UPSTREAM_NAME}"
if [[ ! -f "${UPSTREAM_NAME}" ]]; then
    curl -fsSL --retry 3 -o "${UPSTREAM_NAME}.part" "${UPSTREAM_URL}"
    mv "${UPSTREAM_NAME}.part" "${UPSTREAM_NAME}"
fi

echo "[2/5] verifying upstream SHA-512"
echo "${UPSTREAM_SHA512}  ${UPSTREAM_NAME}" | sha512sum -c -

echo "[3/5] extracting"
rm -rf "${TOPDIR}"
# Use multi-threaded xz for the *decompress* — output goes to disk, no
# determinism requirement here.
XZ_OPT="-T0" tar -xJf "${UPSTREAM_NAME}"

echo "[4/5] removing ${#REMOVE_PATHS[@]} file(s) from tarball"
for rel in "${REMOVE_PATHS[@]}"; do
    full="${TOPDIR}/${rel}"
    if [[ ! -f "${full}" ]]; then
        echo "ERROR: expected file not found in upstream tarball: ${full}" >&2
        exit 1
    fi
    echo "  - ${full}"
    rm -f "${full}"
done

echo "[5/5] repacking deterministically -> ${OUTPUT_NAME}"
rm -f "${OUTPUT_NAME}"
# Build the file list with a stable, locale-independent sort. Pass it to tar
# via --files-from so `tar --sort=name` only has to do a final stable sort.
LC_ALL=C find "${TOPDIR}" -print0 \
  | LC_ALL=C sort -z \
  | LC_ALL=C tar \
        --create \
        --format=gnu \
        --sort=name \
        --owner=0 --group=0 --numeric-owner \
        --mtime="@${MTIME_EPOCH}" \
        --null --files-from=- \
  | xz -T 4 -9 --block-size=268435456 -c > "${OUTPUT_NAME}"

sha512sum "${OUTPUT_NAME}" | tee "${OUTPUT_NAME}.sha512"

if [[ "${KEEP}" -eq 0 ]]; then
    rm -rf "${TOPDIR}"
fi

cat <<EOF

Done.
  Output:        ${WORKDIR}/${OUTPUT_NAME}
  SHA-512 file:  ${WORKDIR}/${OUTPUT_NAME}.sha512

Next steps:
  1. Upload to the AZL modified-source lookaside (pkgs_modified path, per Task 19805).
     NOTE: the blob is uploaded under the *upstream* filename (no .azl. suffix)
     because the comp.toml uses 'replace-upstream' to swap it into the Fedora
     'sources' manifest in place, which matches entries by filename.
       UPLOAD_NAME="${UPSTREAM_NAME}"
       az storage blob upload \\
         --account-name azltempstaginglookaside \\
         --container-name repo \\
         --name "pkgs_modified/firefox/\${UPLOAD_NAME}/sha512/\$(awk '{print \$1}' ${OUTPUT_NAME}.sha512)/\${UPLOAD_NAME}" \\
         --file ${OUTPUT_NAME} \\
         --auth-mode login --overwrite false
  2. Update base/comps/firefox/firefox.comp.toml:
       - source-files entry 'hash' to the SHA-512 above
EOF
