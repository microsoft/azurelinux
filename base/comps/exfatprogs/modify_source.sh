#!/usr/bin/env bash
#
# exfatprogs: deterministic strip-and-repack of upstream `exfatprogs-1.3.1.tar.xz`
# with the `tests/` directory removed. Rationale lives in the comp.toml
# `replace-reason` field; see also `.github/skills/skill-modify-source/SKILL.md`.
#
# Usage:   bash base/comps/exfatprogs/modify_source.sh
# Output:  base/build/work/scratch/exfatprogs/exfatprogs-1.3.1.tar.xz (+ .sha512)
# The upstream tarball is cached under a `.upstream` suffix; re-runs reuse it.

set -euo pipefail

# --- Constants --------------------------------------------------------------

readonly COMPONENT="exfatprogs"
readonly UPSTREAM_VERSION="1.3.1"
readonly UPSTREAM_FILENAME="exfatprogs-${UPSTREAM_VERSION}.tar.xz"
readonly UPSTREAM_TOPDIR="exfatprogs-${UPSTREAM_VERSION}"
readonly UPSTREAM_URL="https://github.com/${COMPONENT}/${COMPONENT}/releases/download/${UPSTREAM_VERSION}/${UPSTREAM_FILENAME}"

readonly UPSTREAM_SHA512="28afefa6a4460a52d8078c47bcb63fdde42778a44e428481beff401f5f2ea305409ba42ae4357e03d7f3c9169e874c99c8caf00aca4d6223561cde11ac886cad"

# Deterministic-repack mtime: 2020-01-01T00:00:00Z (1577836800).
# Any fixed epoch works; do not change without also bumping the
# `hash` in exfatprogs.comp.toml.
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

echo "[4/5] Extracting and stripping ${UPSTREAM_TOPDIR}/tests/"
rm -rf "${WORKDIR}/${UPSTREAM_TOPDIR}"
tar -C "${WORKDIR}" -xf "${UPSTREAM_CACHE}"
if [[ ! -d "${WORKDIR}/${UPSTREAM_TOPDIR}/tests" ]]; then
    echo "ERROR: expected '${UPSTREAM_TOPDIR}/tests/' not present in upstream tarball" >&2
    exit 1
fi
rm -rf "${WORKDIR}/${UPSTREAM_TOPDIR}/tests"

# --- Repack deterministically -----------------------------------------------

echo "[5/5] Repacking deterministically as ${UPSTREAM_FILENAME}"
# Deterministic flags:
#   --sort=name             stable entry order
#   --owner=0 --group=0     no host uid/gid leakage
#   --numeric-owner         force numeric uid/gid
#   --mtime=@<epoch>        fixed mtime
#   --format=gnu            handles long paths deterministically
# LC_ALL=C pins sort collation so --sort=name is locale-independent.
# xz -T 1 forces single-threaded encoding; multi-threaded xz splits
# the stream into non-reproducible blocks unless --block-size is
# also pinned, and the savings are marginal for a tarball this size.
MODIFIED_TARBALL="${WORKDIR}/${UPSTREAM_FILENAME}"
rm -f "${MODIFIED_TARBALL}"
LC_ALL=C tar \
    -C "${WORKDIR}" \
    --sort=name \
    --owner=0 --group=0 --numeric-owner \
    --mtime="${DETERMINISTIC_MTIME}" \
    --format=gnu \
    -cf - "${UPSTREAM_TOPDIR}" \
    | xz -T 1 -9 -c > "${MODIFIED_TARBALL}"

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
