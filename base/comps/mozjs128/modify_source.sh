#!/usr/bin/env bash
#
# mozjs128: download upstream Firefox ESR source, remove a single
# scanner-tripping test fixture, and repack deterministically as a
# .tar.xz. The single removed file is:
#
#   firefox-128.11.0/third_party/rust/zip/tests/data/aes_archive.zip
#
# (AES-encrypted ZIP test vector for the cargo-vendored `zip` crate;
# never read at AZL build time -- mozjs128 only consumes `js/src/`.)
#
# Rationale lives in mozjs128.comp.toml (replace-reason). All output
# lands under <repo-root>/base/build/work/scratch/mozjs128/.

set -euo pipefail

VERSION="128.11.0"
ORIGINAL_NAME="firefox-${VERSION}esr.source.tar.xz"
EXTRACTED_DIRNAME="firefox-${VERSION}"
MODIFIED_NAME="firefox-${VERSION}esr-azl-aes-fixture-removed.tar.xz"
UPSTREAM_URL="https://ftp.mozilla.org/pub/firefox/releases/${VERSION}esr/source/${ORIGINAL_NAME}"

# From https://ftp.mozilla.org/pub/firefox/releases/128.11.0esr/SHA512SUMS
ORIGINAL_SHA512="80af64c1dce6d7a25111480567a3251cc2d1edce00acc4d85bbaa44590f5bbf4c0716f9490c3ab8ef1e6fc2bbabb2379029c2dee51ce477933c7a5935092d279"

# Single path (relative to the extracted top-level dir) to remove.
REMOVE_PATH="third_party/rust/zip/tests/data/aes_archive.zip"

SCRIPT_DIR="$(cd "$(dirname "$(realpath "$0")")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../.." && pwd)"
WORKDIR="${REPO_ROOT}/base/build/work/scratch/mozjs128"
mkdir -p "${WORKDIR}"
cd "${WORKDIR}"

echo "[1/5] Downloading ${ORIGINAL_NAME}"
[[ -f "${ORIGINAL_NAME}" ]] || curl -fsSL --retry 3 -o "${ORIGINAL_NAME}" "${UPSTREAM_URL}"

echo "[2/5] Verifying upstream SHA512"
computed=$(sha512sum "${ORIGINAL_NAME}" | awk '{print $1}')
if [[ "${computed}" != "${ORIGINAL_SHA512}" ]]; then
    echo "ERROR: upstream SHA512 mismatch" >&2
    echo "  expected: ${ORIGINAL_SHA512}" >&2
    echo "  computed: ${computed}" >&2
    exit 1
fi

echo "[3/5] Extracting"
rm -rf "${EXTRACTED_DIRNAME}"
tar -xf "${ORIGINAL_NAME}"

echo "[4/5] Removing ${EXTRACTED_DIRNAME}/${REMOVE_PATH}"
if [[ ! -f "${EXTRACTED_DIRNAME}/${REMOVE_PATH}" ]]; then
    echo "ERROR: expected file not present in upstream tarball: ${REMOVE_PATH}" >&2
    exit 1
fi
rm -f "${EXTRACTED_DIRNAME}/${REMOVE_PATH}"

echo "[5/5] Repacking deterministically"
# Stable byte output requires: sorted names, fixed mtime, zeroed
# owner/group, and single-threaded xz (xz -T0 block boundaries vary
# by host CPU count).
rm -f "${MODIFIED_NAME}"
tar --sort=name \
    --mtime='2024-01-01 00:00:00 UTC' \
    --owner=0 --group=0 --numeric-owner \
    -cf - "${EXTRACTED_DIRNAME}" | xz -T1 -9e > "${MODIFIED_NAME}"

MODIFIED_SHA512=$(sha512sum "${MODIFIED_NAME}" | awk '{print $1}')
echo "${MODIFIED_SHA512}  ${MODIFIED_NAME}" > "${MODIFIED_NAME}.sha512"

cat <<EOF

modified tarball: ${WORKDIR}/${MODIFIED_NAME}
SHA512:           ${MODIFIED_SHA512}

Upload (after \`az login\`):
  az storage blob upload \\
      --auth-mode login \\
      --account-name azltempstaginglookaside \\
      --container-name repo \\
      --name "pkgs_modified/mozjs128/${ORIGINAL_NAME}/sha512/${MODIFIED_SHA512}/${ORIGINAL_NAME}" \\
      --file "${WORKDIR}/${MODIFIED_NAME}"
EOF
