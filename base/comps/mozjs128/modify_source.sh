#!/usr/bin/env bash
#
# mozjs128: download upstream Firefox ESR source, drop subtrees not needed
# for the SpiderMonkey build, and repack deterministically as a .tar.xz.
# All output lands under <repo-root>/base/build/work/scratch/mozjs128/.
# Rationale for the strip lives in mozjs128.comp.toml (replace-reason).

set -euo pipefail

VERSION="128.11.0"
ORIGINAL_NAME="firefox-${VERSION}esr.source.tar.xz"
EXTRACTED_DIRNAME="firefox-${VERSION}"
MODIFIED_NAME="firefox-${VERSION}esr-azl-mozjs-stripped.tar.xz"
UPSTREAM_URL="https://ftp.mozilla.org/pub/firefox/releases/${VERSION}esr/source/${ORIGINAL_NAME}"

# From https://ftp.mozilla.org/pub/firefox/releases/128.11.0esr/SHA512SUMS
ORIGINAL_SHA512="80af64c1dce6d7a25111480567a3251cc2d1edce00acc4d85bbaa44590f5bbf4c0716f9490c3ab8ef1e6fc2bbabb2379029c2dee51ce477933c7a5935092d279"

# Top-level entries kept inside firefox-${VERSION}/. Everything else at the
# top level is deleted. Derived from what mozjs128.spec actually touches.
# `configure.py` is the top-level Python entrypoint that `js/src/configure`
# execs into (it is shared between the Firefox and SpiderMonkey configure
# flows); its imports only reach into python/ and third_party/python/ which
# are kept below.
KEEP_TOP=(
    LICENSE
    Cargo.toml
    Cargo.lock
    configure.py
    moz.configure
    build
    config
    intl
    js
    mfbt
    memory
    mozglue
    python
    third_party
)

# Extra nested subtrees pruned from inside kept top-level dirs:
# - js/src/* entries are fuzzer corpora & test inputs the build does not need.
# - intl/icu is the bundled ICU source; not compiled with --with-system-icu.
NESTED_STRIP=(
    intl/icu
    js/src/fuzz-tests
    js/src/devtools/automation/variants
    js/src/octane
    js/src/ctypes/libffi
)

# Specific nested paths kept even though their top-level dir is NOT in
# KEEP_TOP (or has been stripped via NESTED_STRIP). Restored from the
# upstream tarball after the top-level strip.
# - testing/mozbase: pure-Python helper packages (mozfile, mozinfo, mozprocess,
#   ...) that the `mach` site adds to sys.path. The configure machinery in
#   `build/moz.configure/util.configure` imports `mozfile.which` from it.
#   The rest of `testing/` (mochitest, web-platform, marionette, raptor,
#   etc.) carries fuzzer corpora and crash fixtures that trip the scanner;
#   mozbase itself is ~12 MB of plain Python with no such content.
# - intl/icu/source/common/unicode/uvernum.h: a single 4 KB header that
#   `js/moz.configure`'s `icu_version()` opens to extract
#   `U_ICU_VERSION_MAJOR_NUM` even when `--with-system-icu` is set
#   (configure does NOT skip the version read; the system-ICU flag only
#   redirects the build/link path). Restoring this one file lets us keep
#   the rest of bundled `intl/icu` (~157 MB) stripped.
NESTED_KEEP=(
    testing/mozbase
    intl/icu/source/common/unicode/uvernum.h
)

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

echo "[4/5] Stripping"
(
    cd "${EXTRACTED_DIRNAME}"
    for entry in $(ls -A); do
        keep=0
        for k in "${KEEP_TOP[@]}"; do
            [[ "${entry}" == "${k}" ]] && { keep=1; break; }
        done
        (( keep )) || rm -rf "${entry}"
    done
)
for p in "${NESTED_STRIP[@]}"; do
    rm -rf "${EXTRACTED_DIRNAME}/${p}"
done

# Restore NESTED_KEEP paths from the upstream tarball (their top-level
# dirs are not in KEEP_TOP, so the strip above removed them).
for p in "${NESTED_KEEP[@]}"; do
    tar -xf "${ORIGINAL_NAME}" "${EXTRACTED_DIRNAME}/${p}"
done

echo "[5/5] Repacking deterministically"
# Stable byte output requires: sorted names, fixed mtime, zeroed owner/group,
# and single-threaded xz (xz -T0 block boundaries vary by host CPU count).
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
