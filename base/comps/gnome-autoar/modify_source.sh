#!/usr/bin/env bash
#
# gnome-autoar: strip the three encrypted extract-test fixtures whose
# `input/arextract.zip` (password-protected zips) are rejected by the
# package-signing scan, and drop the three
# meson test cases that read them so `%check` (`%meson_test`) still passes.
#
# NOTE: this component uses `modify_source.sh` + `origin=download` (not an
# azldev archive overlay) because the upstream tarball ships an absolute-target
# symlink test fixture (`tests/files/extract/test-symlink-parent/reference/
# arextract -> /tmp`) that azldev's overlay extractor refuses to extract. Plain
# `tar` handles it, so we repack out-of-band and serve the result from the
# staging lookaside.
#
# Output lands under <repo-root>/base/build/work/scratch/gnome-autoar/.

set -euo pipefail

VERSION="0.4.5"
ORIGINAL_NAME="gnome-autoar-${VERSION}.tar.xz"

# Upstream Source0 (download.gnome.org) SHA512, from specs/g/gnome-autoar/sources.
UPSTREAM_SHA512="ba38dfc0ad3c00fd8316d02d1a8e38ce3c743e11032f7c4efff74e7c3f8e8e815a1debe51eae8e2ee653155356d34992f1bc0e35e6cfab82398265fde8648050"
UPSTREAM_URL="https://download.gnome.org/sources/gnome-autoar/0.4/${ORIGINAL_NAME}"

TOPDIR="gnome-autoar-${VERSION}"

# Encrypted extract-test fixture directories removed to avoid scan failures on
# the SRPM. Each ships an encrypted input/arextract.zip. Paths are relative to
# the tarball's top-level directory. Sorted alphabetically.
FIXTURE_DIRS_TO_REMOVE=(
    tests/files/extract/test-encrypted
    tests/files/extract/test-encrypted-request-passphrase
    tests/files/extract/test-encrypted-wrong-passphrase
)

# The meson extract-unit test hard-codes three encrypted cases that read the
# fixtures above; drop their function definitions and g_test_add_func
# registrations so the remaining suite still runs.
TEST_FILE="tests/test-extract-unit.c"

SCRIPT_DIR="$(cd "$(dirname "$(realpath "$0")")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../.." && pwd)"
WORKDIR="${REPO_ROOT}/base/build/work/scratch/gnome-autoar"
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

echo "[4/6] Removing ${#FIXTURE_DIRS_TO_REMOVE[@]} encrypted fixture dirs"
for rel in "${FIXTURE_DIRS_TO_REMOVE[@]}"; do
    target="${EXTRACT_DIR}/${TOPDIR}/${rel}"
    if [[ ! -d "${target}" ]]; then
        echo "ERROR: expected fixture dir not present in upstream tarball: ${rel}" >&2
        exit 1
    fi
    rm -rf "${target}"
done

echo "[5/6] Dropping encrypted test cases from ${TEST_FILE}"
export TEST_PATH="${EXTRACT_DIR}/${TOPDIR}/${TEST_FILE}"
python3 <<'PY'
import io, os, re
path = os.environ["TEST_PATH"]
with io.open(path, "r", encoding="utf-8") as fh:
    text = fh.read()

# 1) Remove the three contiguous encrypted test function definitions
#    (test_encrypted, test_encrypted_request_passphrase,
#     test_encrypted_wrong_passphrase).
defs = re.compile(
    r"\nstatic void\ntest_encrypted \(void\)\n.*?"
    r"\nstatic void\ntest_encrypted_wrong_passphrase \(void\)\n\{.*?\n\}\n",
    re.DOTALL,
)
text, n_defs = defs.subn("", text, count=1)
if n_defs != 1:
    raise SystemExit(f"expected 1 encrypted-def block, removed {n_defs}")

# 2) Remove the three contiguous g_test_add_func registrations.
regs = re.compile(
    r'\n\n  g_test_add_func \("/autoar-extract/test-encrypted",\n'
    r'.*?test_encrypted_wrong_passphrase\);',
    re.DOTALL,
)
text, n_regs = regs.subn("", text, count=1)
if n_regs != 1:
    raise SystemExit(f"expected 1 encrypted-registration block, removed {n_regs}")

if "test_encrypted" in text:
    raise SystemExit("residual test_encrypted reference remains after edit")

with io.open(path, "w", encoding="utf-8") as fh:
    fh.write(text)
PY
unset TEST_PATH
# Sanity: sibling tests must survive.
grep -qF "test_readonly_directory" "${EXTRACT_DIR}/${TOPDIR}/${TEST_FILE}" \
    || { echo "ERROR: sibling test unexpectedly removed" >&2; exit 1; }

echo "[6/6] Repacking deterministically"
# Stable byte output: sorted names, fixed mtime, zeroed owner/group, single-threaded xz.
rm -f "${ORIGINAL_NAME}.modified"
(
    cd "${EXTRACT_DIR}"
    tar --sort=name \
        --mtime='2024-01-01 00:00:00 UTC' \
        --owner=0 --group=0 --numeric-owner \
        -cf - "${TOPDIR}"
) | xz -T1 -9e > "${ORIGINAL_NAME}.modified"

MODIFIED_SHA512=$(sha512sum "${ORIGINAL_NAME}.modified" | awk '{print $1}')
echo "${MODIFIED_SHA512}  ${ORIGINAL_NAME}" > "${ORIGINAL_NAME}.sha512"

cat <<EOF

modified tarball: ${WORKDIR}/${ORIGINAL_NAME}.modified
SHA512:           ${MODIFIED_SHA512}

Upload (after \`az login\`):
  az storage blob upload \\
      --auth-mode login \\
      --account-name azltempstaginglookaside \\
      --container-name repo \\
      --name "pkgs_modified/gnome-autoar/${ORIGINAL_NAME}/sha512/${MODIFIED_SHA512}/${ORIGINAL_NAME}" \\
      --file "${WORKDIR}/${ORIGINAL_NAME}.modified"
EOF
