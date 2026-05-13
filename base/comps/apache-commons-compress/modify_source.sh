#!/usr/bin/env bash
#
# Reproducibly rebuild commons-compress-<VERSION>-src.tar.gz with a curated
# set of files stripped out (see REMOVE_PATHS below). These are upstream
# Apache Commons Compress encrypted-archive test fixtures flagged by
# anti-malware scanning on the AZL RPM signing pipeline as suspicious /
# malware-like content. Such content blocks the SRPM from being published.
#
# This script is fully deterministic: given the same upstream tarball and
# the same REMOVE_PATHS list, it always produces a byte-identical output
# (so the SHA-512 in the `source-files` entry of
# apache-commons-compress.comp.toml is stable).
#
# Determinism is achieved by:
#   * tar --sort=name  (stable file order, independent of FS readdir order)
#   * --owner=0 --group=0 --numeric-owner  (no host-specific uid/gid)
#   * --mtime=@<fixed epoch>  (fixed mtime for every entry)
#   * --format=gnu  (consistent header format, handles long paths)
#   * gzip -n -9  (no filename/mtime in gzip header; -n is essential —
#                  without it, gzip embeds the local mtime and breaks
#                  determinism. Changing -9 or adding flags changes the
#                  SHA-512, so bump the hash in the comp.toml if you do.)
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
# Output: <workdir>/commons-compress-<VERSION>-src.azl.tar.gz  (+ .sha512)

set -euo pipefail

# Pinned package version. To bump, also update UPSTREAM_SHA512 below and
# the `hash` field in apache-commons-compress.comp.toml.
VERSION="1.27.1"
KEEP=0
# Default workdir lives under the project work dir to comply with AGENTS.md.
WORKDIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)/base/build/work/scratch/apache-commons-compress"

while [[ $# -gt 0 ]]; do
    case "$1" in
        --workdir) WORKDIR="$2"; shift 2 ;;
        --keep)    KEEP=1; shift ;;
        -h|--help)
            sed -n '2,28p' "$0"; exit 0 ;;
        *) echo "unknown arg: $1" >&2; exit 2 ;;
    esac
done

UPSTREAM_NAME="commons-compress-${VERSION}-src.tar.gz"
# Local-only artifact name (different from UPSTREAM_NAME so it doesn't
# collide with the downloaded upstream tarball in the same workdir). The
# blob uploaded to the lookaside MUST use UPSTREAM_NAME (replace-upstream
# matches by filename).
OUTPUT_NAME="commons-compress-${VERSION}-src.azl.tar.gz"
TOPDIR="commons-compress-${VERSION}-src"

# Files (relative to ${TOPDIR}) to strip from the upstream tarball. These
# trip anti-malware scanning on the AZL RPM signing pipeline — an AV
# engine flags them as Trojan (or, for the two encrypted archives, as a
# generic "File is encrypted!" heuristic). Add new entries here as they
# are discovered. Every change to this list alters the repacked SHA-512 —
# bump the `hash` in apache-commons-compress.comp.toml accordingly.
#
# Categories:
#   * Encrypted-archive test fixtures (bla.encrypted.7z,
#     password-encrypted.zip): trip generic "encrypted archive" / malware
#     heuristics. After other blockers were removed these dropped to
#     non-blocking, but we keep them stripped so the scan report stays
#     clean.
#   * Crafted archive test fixtures (COMPRESS-256.7z,
#     zip64support.tar.bz2): named Trojan blockers per the AV scan on
#     2026-05-15. These
#     are small, intentionally-malformed/edge-case archives used by the
#     project's read-side unit tests; same false-positive family as the
#     encrypted fixtures.
REMOVE_PATHS=(
    "src/test/resources/bla.encrypted.7z"
    "src/test/resources/password-encrypted.zip"
    "src/test/resources/COMPRESS-256.7z"
    "src/test/resources/zip64support.tar.bz2"
)

# Known upstream SHA-512 (from specs/a/apache-commons-compress/sources).
# Bump when version changes.
UPSTREAM_SHA512="c7a2cef26959e687ad19b96b5ba8393d7514095e13bf0f29bd41e6b3c3cb2260d8ff23283ff3d5fd137b2522b843e7f0f50ab46bcf0f66df5383674f35f223ab"

# Fixed mtime for every entry in the repacked tarball:
# 2020-01-01T00:00:00Z (1577836800). Any fixed epoch works; do not change
# without also bumping the `hash` in the comp.toml.
MTIME_EPOCH=1577836800

UPSTREAM_URL="https://archive.apache.org/dist/commons/compress/source/${UPSTREAM_NAME}"

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
tar -xzf "${UPSTREAM_NAME}"

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
# gzip -n strips the filename and mtime from the gzip header (essential for
# determinism).
LC_ALL=C find "${TOPDIR}" -print0 \
  | LC_ALL=C sort -z \
  | LC_ALL=C tar \
        --create \
        --format=gnu \
        --sort=name \
        --owner=0 --group=0 --numeric-owner \
        --mtime="@${MTIME_EPOCH}" \
        --null --files-from=- \
  | gzip -n -9 -c > "${OUTPUT_NAME}"

sha512sum "${OUTPUT_NAME}" | tee "${OUTPUT_NAME}.sha512"

if [[ "${KEEP}" -eq 0 ]]; then
    rm -rf "${TOPDIR}"
fi

cat <<EOF

Done.
  Output:        ${WORKDIR}/${OUTPUT_NAME}
  SHA-512 file:  ${WORKDIR}/${OUTPUT_NAME}.sha512

Next steps:
  1. Upload to the AZL modified-source lookaside (pkgs_modified path).
     NOTE: the blob is uploaded under the *upstream* filename (no .azl. suffix)
     because the comp.toml uses 'replace-upstream' to swap it into the Fedora
     'sources' manifest in place, which matches entries by filename.
       UPLOAD_NAME="${UPSTREAM_NAME}"
       az storage blob upload \\
         --account-name azltempstaginglookaside \\
         --container-name repo \\
         --name "pkgs_modified/apache-commons-compress/\${UPLOAD_NAME}/sha512/\$(awk '{print \$1}' ${OUTPUT_NAME}.sha512)/\${UPLOAD_NAME}" \\
         --file ${OUTPUT_NAME} \\
         --auth-mode login --overwrite false
  2. Update base/comps/apache-commons-compress/apache-commons-compress.comp.toml:
       - source-files entry 'hash' to the SHA-512 above
       - update both SHA-512 occurrences in the origin.uri
EOF
