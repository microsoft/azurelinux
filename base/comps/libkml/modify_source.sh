#!/usr/bin/env bash
#
# libkml — strip benign-but-scanner-tripping test fixtures from upstream
# tarball.
#
# Background
# ----------
# An automated FS-aware deep scanner in the package-signing pipeline
# flags `testdata/kmz/bad-too-large.kmz` inside the upstream
# `libkml-1.3.0.tar.gz` tarball as malicious.
#
# Upstream intent of the fixture
# ------------------------------
# `bad-too-large.kmz` is an intentionally-malformed ZIP whose
# uncompressed-size field is crafted to report 4,294,967,294 bytes
# (decompression-bomb shape). It is a test input by design, used by
# libkml's Google Test suite to verify parser-rejection of crafted
# decompression-bomb archives. The fixture is exercised by exactly
# one test case, `ZipFileTest.TestBadTooLarge` in
# `tests/kml/base/zip_file_test.cc`. The scanner flags the fixture
# because its on-disk shape matches the malicious-archive heuristics
# the test was designed to defeat.
#
# What this script does
# ---------------------
# 1. Removes `testdata/kmz/bad-too-large.kmz` from the tarball.
# 2. Surgically deletes the `ZipFileTest.TestBadTooLarge` block from
#    `tests/kml/base/zip_file_test.cc`. Every sibling test in that
#    file remains intact. The other 7 "bad" / "overflow" KMZ test
#    fixtures shipped under `testdata/kmz/` are kept as-is (the
#    scanner cleared them in the latest scan pass).
# 3. Repacks the tarball deterministically so the SHA512 is stable
#    across re-runs.
#
# Loss in %check
# --------------
# One Google Test case (out of >200 in the libkml test suite) is no
# longer compiled. The runtime code path it exercises (ZIP open
# rejection of a crafted oversized-uncompressed-size record) is
# unchanged and remains exercised indirectly by sibling tests that
# feed valid and invalid inputs through the same open / parse APIs.
#
# Block-removal anchoring
# -----------------------
# Each `TEST_F` block has a unique `^TEST_F(Class, Name) {$` opening
# line and a matching `^}$` closing line at column 0. The remover
# uses the sed range `/^TEST_F(Class, Name) {$/,/^}$/d`, which is
# safe in this codebase because:
#   * Nested braces inside the test body are always indented, so
#     they never match `^}$`.
#   * The closing `}` of an enclosing `namespace { ... }` is
#     followed by `// end namespace ...`, so it does not match
#     `^}$` either.
# Pre- and post-condition greps in `delete_test_f` enforce these
# invariants for every block.
#
# Reproducibility notes
# ---------------------
# - `tar --sort=name --mtime=...` produces a byte-deterministic output.
# - `gzip -n` strips mtime/filename metadata from the gzip header for
#   the same reason.
#
# Output location
# ---------------
# The script writes its outputs to `base/build/work/scratch/libkml/`
# (resolved relative to the repository root). This path is covered by
# the repository's top-level `.gitignore` via `build/`, so no
# component-level `.gitignore` is needed and no script artefact can be
# accidentally committed.
#
# Usage:
#   bash modify_source.sh
#
# Outputs (under base/build/work/scratch/libkml/):
#   libkml-1.3.0-azl-stripped.tar.gz
#   libkml-1.3.0-azl-stripped.tar.gz.sha512
#
# After running, upload `libkml-1.3.0-azl-stripped.tar.gz` as the blob
# payload at the lookaside URL pattern (modified container) for
# filename `libkml-1.3.0.tar.gz`. The exact URL is printed by this
# script.

set -euo pipefail

UPSTREAM_URL="https://github.com/libkml/libkml/archive/1.3.0/libkml-1.3.0.tar.gz"
ORIGINAL_NAME="libkml-1.3.0.tar.gz"
ORIGINAL_SHA512="aa48158103d3af764bf98c1fb4cf3e1356b9cc6c8e79d80b96850916f0a8ccb1dac3a46427735dd0bf20647daa047d10e722ac3da2a214d4c1559bf6d5d7c853"
MODIFIED_NAME="libkml-1.3.0-azl-stripped.tar.gz"
EXTRACTED_DIRNAME="libkml-1.3.0"

# Files to remove from the upstream tarball. See the header comment
# for the per-fixture upstream intent and the `TEST_F` block(s) that
# reference each one.
declare -a STRIP_PATHS=(
    "${EXTRACTED_DIRNAME}/testdata/kmz/bad-too-large.kmz"
)

# TEST_F blocks to surgically remove. Format: "file|Class|Name".
# Each entry is processed by `delete_test_f` below.
declare -a TEST_F_REMOVALS=(
    "${EXTRACTED_DIRNAME}/tests/kml/base/zip_file_test.cc|ZipFileTest|TestBadTooLarge"
)

# After all strips and TEST_F removals, every fixture basename below
# must have ZERO remaining references anywhere under `src/` or `tests/`.
declare -a FIXTURE_BASENAMES=(
    "bad-too-large.kmz"
)

# Sibling TEST_F cases that MUST survive in each touched `.cc` file.
# Drift here means the sed range was too greedy and stole an adjacent
# block.
declare -a TEST_F_RETAINED=(
    "${EXTRACTED_DIRNAME}/tests/kml/base/zip_file_test.cc|ZipFileTest|TestBadPkZipData"
    "${EXTRACTED_DIRNAME}/tests/kml/base/zip_file_test.cc|ZipFileTest|TestMaxUncompressedSize"
    "${EXTRACTED_DIRNAME}/tests/kml/base/zip_file_test.cc|ZipFileTest|TestOpenFromString"
    "${EXTRACTED_DIRNAME}/tests/kml/base/zip_file_test.cc|ZipFileTest|TestOpenFromFile"
    "${EXTRACTED_DIRNAME}/tests/kml/base/zip_file_test.cc|ZipFileTest|TestCreate"
    "${EXTRACTED_DIRNAME}/tests/kml/base/zip_file_test.cc|ZipFileTest|TestAddEntryBad"
)

# Surgically delete a single `TEST_F(Class, Name) { ... }` block.
# Pre- and post-condition checks guard against drift.
delete_test_f() {
    local file="$1"
    local class="$2"
    local name="$3"

    if [[ ! -f "${file}" ]]; then
        echo "ERROR: file not present: ${file}" >&2
        exit 1
    fi
    if ! grep -qE "^TEST_F\(${class}, ${name}\) \{$" "${file}"; then
        echo "ERROR: TEST_F(${class}, ${name}) header not found in ${file}" >&2
        exit 1
    fi

    # sed range: from the unique `TEST_F(Class, Name) {` opening line
    # through the next column-0 `}` (= the closing brace of the test
    # body). Both anchors are validated by the surrounding greps.
    sed -i "/^TEST_F(${class}, ${name}) {$/,/^}$/d" "${file}"

    if grep -qE "^TEST_F\(${class}, ${name}\) \{$" "${file}"; then
        echo "ERROR: TEST_F(${class}, ${name}) still present after delete in ${file}" >&2
        exit 1
    fi
}

SCRIPT_DIR="$(cd "$(dirname "$(realpath "$0")")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../.." && pwd)"
WORKDIR="${REPO_ROOT}/base/build/work/scratch/libkml"
mkdir -p "${WORKDIR}"
cd "${WORKDIR}"

echo "[1/6] Downloading ${ORIGINAL_NAME} from upstream into ${WORKDIR}"
curl -fsSL --retry 3 -o "${ORIGINAL_NAME}" "${UPSTREAM_URL}"

echo "[2/6] Verifying original SHA512"
COMPUTED_ORIGINAL_SHA512=$(sha512sum "${ORIGINAL_NAME}" | awk '{print $1}')
if [[ "${COMPUTED_ORIGINAL_SHA512}" != "${ORIGINAL_SHA512}" ]]; then
    echo "ERROR: upstream SHA512 mismatch" >&2
    echo "  expected: ${ORIGINAL_SHA512}" >&2
    echo "  computed: ${COMPUTED_ORIGINAL_SHA512}" >&2
    exit 1
fi

echo "[3/6] Extracting"
rm -rf "${EXTRACTED_DIRNAME}"
tar -xzf "${ORIGINAL_NAME}"

echo "[4/6] Stripping flagged paths"
for p in "${STRIP_PATHS[@]}"; do
    if [[ ! -e "${p}" ]]; then
        echo "ERROR: expected path not present in upstream: ${p}" >&2
        exit 1
    fi
    rm -v "${p}"
done

echo "[5/6] Removing dependent TEST_F blocks"
for entry in "${TEST_F_REMOVALS[@]}"; do
    IFS='|' read -r f cls nm <<<"${entry}"
    echo "  - ${f}: TEST_F(${cls}, ${nm})"
    delete_test_f "${f}" "${cls}" "${nm}"
done

echo "[5a/6] Post-condition: stripped fixture names must have no remaining references"
pushd "${EXTRACTED_DIRNAME}" >/dev/null
for fixture in "${FIXTURE_BASENAMES[@]}"; do
    # Match the basename surrounded by ZIP-style "/kmz/" prefix to avoid
    # `bad.kmz` matching `zermatt-photo-bad.kmz` (and similar substring
    # collisions). All upstream references to these fixtures use that
    # exact prefix.
    if grep -rln --include='*.cc' --include='*.h' --include='*.cmake' --include='CMakeLists.txt' \
            -- "/kmz/${fixture}" src/ tests/ 2>/dev/null; then
        echo "ERROR: post-edit source tree still references /kmz/${fixture}" >&2
        exit 1
    fi
done
popd >/dev/null

echo "[5b/6] Post-condition: sibling TEST_F cases must still be present"
for entry in "${TEST_F_RETAINED[@]}"; do
    IFS='|' read -r f cls nm <<<"${entry}"
    if ! grep -qE "^TEST_F\(${cls}, ${nm}\) \{$" "${f}"; then
        echo "ERROR: retained sibling TEST_F(${cls}, ${nm}) missing from ${f}; sed range too greedy" >&2
        exit 1
    fi
done

echo "[6/6] Repacking deterministically as ${MODIFIED_NAME}"
# --sort=name        : deterministic file ordering
# --mtime            : pin mtime to a fixed epoch so the output is reproducible
# --owner=0 --group=0 --numeric-owner : strip uid/gid/uname/gname
# gzip -n            : do not store the mtime/filename in the gzip header
rm -f "${MODIFIED_NAME}"
LC_ALL=C tar --sort=name \
    --mtime='2024-01-01 00:00:00 UTC' \
    --owner=0 --group=0 --numeric-owner \
    -cf - "${EXTRACTED_DIRNAME}" | gzip -n -9 > "${MODIFIED_NAME}"

MODIFIED_SHA512=$(sha512sum "${MODIFIED_NAME}" | awk '{print $1}')
echo "${MODIFIED_SHA512}  ${MODIFIED_NAME}" > "${MODIFIED_NAME}.sha512"

cat <<EOF

================================================================
DONE
  modified tarball: ${WORKDIR}/${MODIFIED_NAME}
  SHA512:           ${MODIFIED_SHA512}
================================================================

Next steps:
  1. Make sure you are logged in to Azure (one-time per shell):
       az login
  2. Upload the modified tarball with this ready-to-paste command
     (uploads to the lookaside 'repo' container under the
     'pkgs_modified/' prefix at the exact path
     base/comps/libkml/libkml.comp.toml's source-files.origin.uri
     expects):

       az storage blob upload \\
           --auth-mode login \\
           --account-name azltempstaginglookaside \\
           --container-name repo \\
           --name "pkgs_modified/libkml/libkml-1.3.0.tar.gz/sha512/${MODIFIED_SHA512}/libkml-1.3.0.tar.gz" \\
           --file "${WORKDIR}/${MODIFIED_NAME}"

  3. The hash + URI in base/comps/libkml/libkml.comp.toml are
     already populated for SHA512 ${MODIFIED_SHA512:0:16}...; if the
     SHA512 above does NOT match, this means the regeneration was not
     deterministic. This requires further investigation and the comp
     TOML must NOT be updated with the new hash/URI until the root
     cause of non-determinism is identified and resolved.
EOF
