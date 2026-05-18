#!/usr/bin/env bash
#
# rubygem-pdf-reader: strip pathological PDF test fixtures from
# `Source1` (`pdf-reader-2.4.2-spec.txz`, the upstream `spec/` test
# tree) and gracefully degrade the test helper so the remaining
# `%check` run skips (rather than fails) the affected contexts. The
# full list of stripped paths lives in the `FIXTURES_TO_REMOVE`
# array below.
#
# Output lands under <repo-root>/base/build/work/scratch/rubygem-pdf-reader/.

set -euo pipefail

VERSION="2.4.2"
ORIGINAL_NAME="pdf-reader-${VERSION}-spec.txz"
MODIFIED_NAME="pdf-reader-${VERSION}-spec-azl-fixtures-stripped.txz"

# Upstream Source1 lookaside URL (standard `pkgs/` prefix; published
# alongside `Source0`, the .gem from rubygems.org).
UPSTREAM_SHA512="2421b51f1c8d8dbc23f9b542a1c0f32542667639c859656b44b67b34e0262a132d443419604469d7fb1ef7b2861401fd4f8fb7fb94bc14f8d11fc3c04abe3c3c"
UPSTREAM_URL="https://azltempstaginglookaside.blob.core.windows.net/repo/pkgs/rubygem-pdf-reader/${ORIGINAL_NAME}/sha512/${UPSTREAM_SHA512}/${ORIGINAL_NAME}"

# PDF test fixtures removed from spec/data/ to avoid scan failures on
# the SRPM. All 47 are benign upstream regression PDFs (deliberately-
# malformed structures, encrypted-cipher variants) not consumed at
# AZL runtime. Paths are relative to the extracted top-level dir of
# the tarball (which has no version-named top-level directory; spec/
# sits at the root). Sorted alphabetically.
FIXTURES_TO_REMOVE=(
    spec/data/broken_string.pdf
    spec/data/clearscan-with-image-removed.pdf
    spec/data/clearscan.pdf
    spec/data/content_stream_as_array.pdf
    spec/data/content_stream_missing_final_operator.pdf
    spec/data/content_stream_refers_to_invalid_font.pdf
    spec/data/difference_table2.pdf
    spec/data/difference_table_encrypted.pdf
    spec/data/encrypted_version1_revision2_128bit_rc4_blank_user_password.pdf
    spec/data/encrypted_version1_revision2_128bit_rc4_no_doc_id.pdf
    spec/data/encrypted_version1_revision2_40bit_rc4_user_pass_apples.pdf
    spec/data/encrypted_version2_revision3_128bit_rc4_blank_user_pass.pdf
    spec/data/encrypted_version2_revision3_128bit_rc4_user_pass_apples.pdf
    spec/data/encrypted_version4_revision4_128bit_aes_user_pass_apples_enc_metadata.pdf
    spec/data/encrypted_version4_revision4_128bit_aes_user_pass_apples_unenc_metadata.pdf
    spec/data/encrypted_version4_revision4_128bit_rc4_user_pass_apples_enc_metadata.pdf
    spec/data/encrypted_version4_revision4_128bit_rc4_user_pass_apples_unenc_metadata.pdf
    spec/data/encrypted_version5_revision5_256bit_aes_user_pass_apples_enc_metadata.pdf
    spec/data/encrypted_version5_revision5_256bit_aes_user_pass_apples_unenc_metadata.pdf
    spec/data/encrypted_version5_revision6_256bit_aes_user_pass_apples_enc_metadata.pdf
    spec/data/encrypted_version5_revision6_256bit_aes_user_pass_apples_unenc_metadata.pdf
    spec/data/form_xobject_recursive.pdf
    spec/data/hard_lock_under_osx.pdf
    spec/data/indirect_mediabox.pdf
    spec/data/invisible.pdf
    spec/data/junk_prefix.pdf
    spec/data/junk_prefix_1024.pdf
    spec/data/kids-as-direct-objects.pdf
    spec/data/mediabox_and_cropbox_are_references.pdf
    spec/data/mediabox_missing.pdf
    spec/data/one-byte-identity.pdf
    spec/data/overlapping-chars-x-fake-bold.pdf
    spec/data/overlapping-chars-xy-fake-bold.pdf
    spec/data/pages_object_missing_type.pdf
    spec/data/rotate-180.pdf
    spec/data/rotate-then-undo.pdf
    spec/data/screwey_xref_offsets.pdf
    spec/data/standard_font_with_no_difference.pdf
    spec/data/symbol.pdf
    spec/data/times-with-control-character.pdf
    spec/data/truetype-arial.pdf
    spec/data/type1-arial.pdf
    spec/data/type3_font.pdf
    spec/data/type3_font_with_rare_font_matrix.pdf
    spec/data/zapf.pdf
    spec/data/zeroed_xref_entry.pdf
    spec/data/zlib_stream_issue.pdf
)

# Helper file whose missing-fixture branch is patched from
# `raise ArgumentError, ...` to `skip "..."` so rspec gracefully
# marks affected examples pending instead of failing them.
HELPER_FILE="spec/support/reader_spec_helper.rb"

SCRIPT_DIR="$(cd "$(dirname "$(realpath "$0")")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../.." && pwd)"
WORKDIR="${REPO_ROOT}/base/build/work/scratch/rubygem-pdf-reader"
mkdir -p "${WORKDIR}"
cd "${WORKDIR}"

echo "[1/6] Downloading ${ORIGINAL_NAME}"
[[ -f "${ORIGINAL_NAME}" ]] || curl -fsSL --retry 3 -o "${ORIGINAL_NAME}" "${UPSTREAM_URL}"

echo "[2/6] Verifying upstream SHA512"
computed=$(sha512sum "${ORIGINAL_NAME}" | awk '{print $1}')
if [[ "${computed}" != "${UPSTREAM_SHA512}" ]]; then
    echo "ERROR: upstream SHA512 mismatch" >&2
    echo "  expected: ${UPSTREAM_SHA512}" >&2
    echo "  computed: ${computed}" >&2
    exit 1
fi

echo "[3/6] Extracting"
EXTRACT_DIR="extracted"
rm -rf "${EXTRACT_DIR}"
mkdir "${EXTRACT_DIR}"
tar -xf "${ORIGINAL_NAME}" -C "${EXTRACT_DIR}"

echo "[4/6] Removing ${#FIXTURES_TO_REMOVE[@]} flagged PDF fixtures"
for rel in "${FIXTURES_TO_REMOVE[@]}"; do
    target="${EXTRACT_DIR}/${rel}"
    if [[ ! -f "${target}" ]]; then
        echo "ERROR: expected fixture not present in upstream tarball: ${rel}" >&2
        exit 1
    fi
    rm -f "${target}"
done

echo "[5/6] Patching ${HELPER_FILE} (skip only for stripped fixtures; still raise otherwise)"
helper="${EXTRACT_DIR}/${HELPER_FILE}"
if [[ ! -f "${helper}" ]]; then
    echo "ERROR: helper missing from upstream tarball: ${HELPER_FILE}" >&2
    exit 1
fi
# The original helper has a single `else / raise ArgumentError, ...` arm for
# the missing-fixture case. We surgically insert a new `elsif` arm BEFORE the
# existing `else`, gated by an explicit allow-list of the stripped basenames
# (with `.pdf` extension). Any other missing fixture still raises,
# so an unrelated upstream change that drops a different fixture surfaces as
# a hard error rather than a silent skip.
if ! grep -qF 'raise ArgumentError, "#{valid_filename} not found"' "${helper}"; then
    echo "ERROR: anchor line not found in ${HELPER_FILE} -- upstream may have changed" >&2
    exit 1
fi
# Build the Ruby allow-list literal from FIXTURES_TO_REMOVE basenames so
# script + comp.toml stay in lock-step.
allow_list_lines=""
for rel in "${FIXTURES_TO_REMOVE[@]}"; do
    allow_list_lines+="    ${rel##spec/data/}
"
done
# Pass values to Python via env vars (heredoc + bash quoting do not interop
# cleanly with Python literals for multi-line strings).
export HELPER_PATH="${helper}"
export ALLOW_LIST_LINES="${allow_list_lines}"
python3 <<'PY'
import io, os
path = os.environ["HELPER_PATH"]
allow_list_lines = os.environ["ALLOW_LIST_LINES"]
expected = (
    '    else\n'
    '      raise ArgumentError, "#{valid_filename} not found"\n'
    '    end'
)
replacement = (
    '    elsif AZL_STRIPPED_FIXTURES.include?("#{base}.pdf")\n'
    '      skip "PDF fixture #{File.basename(valid_filename)} stripped for downstream scan compliance"\n'
    + expected
)
with io.open(path, "r", encoding="utf-8") as fh:
    text = fh.read()
if text.count(expected) != 1:
    raise SystemExit(
        f"expected exactly 1 occurrence of else/raise anchor block, found {text.count(expected)}"
    )
text = text.replace(expected, replacement)
module_anchor = "module ReaderSpecHelper\n"
if module_anchor not in text:
    raise SystemExit("module anchor not found")
const_block = (
    "\n"
    "  # AZL downstream: fixtures stripped from spec/data/ for package-\n"
    "  # signing-scan compliance. pdf_spec_file() skips (rather than raises)\n"
    "  # ONLY for entries in this set; any other missing fixture still raises.\n"
    "  AZL_STRIPPED_FIXTURES = %w[\n"
    + allow_list_lines
    + "  ].freeze\n"
)
text = text.replace(module_anchor, module_anchor + const_block, 1)
with io.open(path, "w", encoding="utf-8") as fh:
    fh.write(text)
PY
unset HELPER_PATH ALLOW_LIST_LINES
# Post-condition checks.
grep -qF 'AZL_STRIPPED_FIXTURES = %w[' "${helper}" || { echo "ERROR: allow-list constant not injected" >&2; exit 1; }
grep -qF 'elsif AZL_STRIPPED_FIXTURES.include?' "${helper}" || { echo "ERROR: elsif clause not inserted" >&2; exit 1; }
grep -qF 'raise ArgumentError, "#{valid_filename} not found"' "${helper}" || { echo "ERROR: original raise clause was unexpectedly removed" >&2; exit 1; }

echo "[6/6] Repacking deterministically"
# Stable byte output: sorted names, fixed mtime, zeroed owner/group,
# single-threaded xz.
rm -f "${MODIFIED_NAME}"
(
    cd "${EXTRACT_DIR}"
    tar --sort=name \
        --mtime='2024-01-01 00:00:00 UTC' \
        --owner=0 --group=0 --numeric-owner \
        -cf - .
) | xz -T1 -9e > "${MODIFIED_NAME}"

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
      --name "pkgs_modified/rubygem-pdf-reader/${ORIGINAL_NAME}/sha512/${MODIFIED_SHA512}/${ORIGINAL_NAME}" \\
      --file "${WORKDIR}/${MODIFIED_NAME}"
EOF
