#!/usr/bin/env bash
#
# yara — strip benign-but-scanner-tripping fixture from upstream tarball.
#
# Background
# ----------
# An automated malware scan in the package signing pipeline rejects
# `tests/oss-fuzz/dotnet_fuzzer_corpus/obfuscated` inside the upstream
# `yara-4.5.4.tar.gz` tarball.  The file is a deliberately obfuscated
# .NET binary used as an oss-fuzz seed-corpus input for YARA's `.NET`
# parser fuzzer; it is benign but matches generic .NET-obfuscator
# heuristics by design.
#
# The `*_fuzzer.cc` oss-fuzz harnesses (and their `*_fuzzer_corpus/`
# directories) are NOT referenced from upstream's `Makefile.am`, so the
# autotools `make check` driver does not exercise them.  Removing
# `tests/oss-fuzz/dotnet_fuzzer_corpus/obfuscated` (and, optionally,
# the rest of the dotnet fuzzer corpus) does not affect the Azure Linux
# build or `%check`.
#
# This script repacks the upstream tarball with the offending file
# stripped, then prints the SHA512 of the modified artefact for use in
# `base/comps/yara/yara.comp.toml`'s `source-files` block.  The
# modified tarball must be uploaded to the Azure Linux modified-source
# blob storage; its blob URL becomes the `source-files.origin.uri` in
# the comp TOML.
#
# Reproducibility notes
# ---------------------
# - The script uses `tar --sort=name --mtime=` flags to produce a
#   byte-deterministic output, so re-running on the same upstream
#   tarball must always yield the same SHA512.
# - `gzip -n` strips mtime/filename metadata from the gzip header for
#   the same reason.
#
# Output location
# ---------------
# The script writes its outputs to `base/build/work/scratch/yara/`
# (resolved relative to the repository root).  This path is covered by
# the repository's top-level `.gitignore` via `build/`, so no
# component-level `.gitignore` is needed and no script artefact can be
# accidentally committed.
#
# Usage:
#   bash modify_source.sh
#
# Outputs (under base/build/work/scratch/yara/):
#   yara-4.5.4-azl-stripped.tar.gz
#   yara-4.5.4-azl-stripped.tar.gz.sha512
#
# After running upload `yara-4.5.4-azl-stripped.tar.gz` as the blob payload at
# the lookaside URL pattern (modified container) for filename
# `yara-4.5.4.tar.gz`.  The exact URL is printed by this script.

set -euo pipefail

UPSTREAM_URL="https://github.com/VirusTotal/yara/archive/v4.5.4.tar.gz"
ORIGINAL_NAME="yara-4.5.4.tar.gz"
ORIGINAL_SHA512="b1da40636f9e55bb07cc911479e6dfa8dc7a4fa3f6b9f10b9f669d741d7af51a1d31e044f9842ec3ab9c6ac9788fbdb89a1686c9e3f22f68d1f9e5fb3db22167"
MODIFIED_NAME="yara-4.5.4-azl-stripped.tar.gz"
EXTRACTED_DIRNAME="yara-4.5.4"

# Files to remove from the upstream tarball.
#
# `tests/oss-fuzz/dotnet_fuzzer_corpus/obfuscated` is a deliberately
# obfuscated .NET binary used as an oss-fuzz seed-corpus input for
# YARA's .NET parser fuzzer; it is referenced only by libFuzzer
# harnesses (not by the autotools `make check` test suite).
#
# The three SHA-256-named fixtures under `tests/data/` are real malware
# samples used by `tests/test-pe.c` (PE-format parser test) — one is
# UPX-packed. The autotools `make check` driver runs `test-pe`, which
# references these files by name. Stripping the files alone would make
# `test-pe` fail at runtime, so we also drop the `test-pe` line from
# `Makefile.am` below (see the `Makefile.am` edit step), which causes
# autoreconf in %prep to regenerate a Makefile without `test-pe` in
# the TESTS list. Loss: build-time PE-parser regression coverage from
# upstream's own test corpus. The runtime PE rule-scanning code path
# (the same one consumers exercise via the `yara` CLI) is unaffected.
declare -a STRIP_PATHS=(
    "${EXTRACTED_DIRNAME}/tests/oss-fuzz/dotnet_fuzzer_corpus/obfuscated"
    "${EXTRACTED_DIRNAME}/tests/data/05cd06e6a202e12be22a02700ed6f1604e803ca8867277d852e8971efded0650"
    "${EXTRACTED_DIRNAME}/tests/data/079a472d22290a94ebb212aa8015cdc8dd28a968c6b4d3b88acdd58ce2d3b885"
    "${EXTRACTED_DIRNAME}/tests/data/079a472d22290a94ebb212aa8015cdc8dd28a968c6b4d3b88acdd58ce2d3b885.upx"
    "${EXTRACTED_DIRNAME}/tests/data/e3d45a2865818756068757d7e319258fef40dad54532ee4355b86bc129f27345"
)

SCRIPT_DIR="$(cd "$(dirname "$(realpath "$0")")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../.." && pwd)"
WORKDIR="${REPO_ROOT}/base/build/work/scratch/yara"
mkdir -p "${WORKDIR}"
cd "${WORKDIR}"

echo "[1/5] Downloading ${ORIGINAL_NAME} from upstream into ${WORKDIR}"
curl -fsSL --retry 3 -o "${ORIGINAL_NAME}" "${UPSTREAM_URL}"

echo "[2/5] Verifying original SHA512"
COMPUTED_ORIGINAL_SHA512=$(sha512sum "${ORIGINAL_NAME}" | awk '{print $1}')
if [[ "${COMPUTED_ORIGINAL_SHA512}" != "${ORIGINAL_SHA512}" ]]; then
    echo "ERROR: upstream SHA512 mismatch" >&2
    echo "  expected: ${ORIGINAL_SHA512}" >&2
    echo "  computed: ${COMPUTED_ORIGINAL_SHA512}" >&2
    exit 1
fi

echo "[3/5] Extracting"
rm -rf "${EXTRACTED_DIRNAME}"
tar -xzf "${ORIGINAL_NAME}"

echo "[4/5] Stripping flagged paths"
for p in "${STRIP_PATHS[@]}"; do
    if [[ ! -e "${p}" ]]; then
        echo "ERROR: expected path not present in upstream: ${p}" >&2
        exit 1
    fi
    rm -v "${p}"
done

# Drop `test-pe` from the autotools `check_PROGRAMS` list in
# `Makefile.am`. `test-pe` references the four hash-named fixtures in
# `tests/data/` we just stripped (see STRIP_PATHS above); leaving the
# test in the autotools TESTS list would make `make check` fail at
# runtime. The spec runs `autoreconf --force --install` in %prep, so
# the regenerated `Makefile.in` picks up the edit and `test-pe` is
# omitted from the build's test driver entirely. `test-pe.c` itself
# stays in the tarball — harmless, unused.
#
# We also drop the now-orphan `test_pe_SOURCES`, `test_pe_LDADD`,
# `test_pe_LDFLAGS` variable declarations. `automake` runs with
# `-Werror` in upstream's configuration; leaving the orphan vars
# triggers a "variable defined but no program has 'test_pe' as
# canonical name (possible typo)" warning that fails autoreconf.
MAKEFILE_AM="${EXTRACTED_DIRNAME}/Makefile.am"
if ! grep -qE '^  test-pe \\$' "${MAKEFILE_AM}"; then
    echo "ERROR: expected '  test-pe \\' line not found in ${MAKEFILE_AM}" >&2
    exit 1
fi
if ! grep -qE '^test_pe_SOURCES\s*=' "${MAKEFILE_AM}"; then
    echo "ERROR: expected 'test_pe_SOURCES =' line not found in ${MAKEFILE_AM}" >&2
    exit 1
fi
sed -i '/^  test-pe \\$/d' "${MAKEFILE_AM}"
sed -i '/^test_pe_SOURCES\s*=/d;/^test_pe_LDADD\s*=/d;/^test_pe_LDFLAGS\s*=/d' "${MAKEFILE_AM}"
echo "  dropped 'test-pe' entry and its test_pe_{SOURCES,LDADD,LDFLAGS} variables from ${MAKEFILE_AM}"

echo "[5/5] Repacking deterministically as ${MODIFIED_NAME}"
# --sort=name        : deterministic file ordering
# --mtime            : pin mtime to a fixed epoch so the output is reproducible
# --owner=0 --group=0 --numeric-owner : strip uid/gid/uname/gname
# gzip -n            : do not store the mtime/filename in the gzip header
rm -f "${MODIFIED_NAME}"
tar --sort=name \
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
     base/comps/yara/yara.comp.toml's source-files.origin.uri expects):

       az storage blob upload \\
           --auth-mode login \\
           --account-name azltempstaginglookaside \\
           --container-name repo \\
           --name "pkgs_modified/yara/yara-4.5.4.tar.gz/sha512/${MODIFIED_SHA512}/yara-4.5.4.tar.gz" \\
           --file "${WORKDIR}/${MODIFIED_NAME}"

  3. The hash + URI in base/comps/yara/yara.comp.toml are
     already populated for SHA512 ${MODIFIED_SHA512:0:16}...; if the
     SHA512 above does NOT match, this means the regeneration was not deterministic.
     This requires further investigation and the comp TOML must NOT be updated with
     the new hash/URI until the root cause of non-determinism is identified and resolved.
EOF
