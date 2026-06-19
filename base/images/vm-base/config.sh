#!/bin/bash
# config.sh — Kiwi config.sh hook for the Azure Linux VM base image.
#
# Removes build-time, machine-id-specific boot state so the published base
# image boots cleanly after its /etc/machine-id is regenerated on first boot.
# Kiwi runs this automatically at the end of the prepare step, inside the image
# root, for every vm-base profile.
#
# Background:
#   The image is built with `<bootloader ... bls="true">` and ships an empty
#   /etc/machine-id (systemd regenerates a unique id on first boot). When the
#   kernel package is installed during the build, kernel-install uses the BUILD
#   machine's machine-id as the BootLoaderSpec entry-token, so:
#     * the BLS entry is named <build-machine-id>-<kver>.conf, and
#     * grubby records that entry id in /boot/grub2/grubenv as `saved_entry`.
#   Because /etc/machine-id is wiped for first-boot regeneration, both the entry
#   filename and the saved default reference a machine-id the running system
#   will never have again — a stale default + orphan that mislead boot tooling
#   which filters entries by the current machine-id.
#
# This hook does two things, both scoped to grub boot state:
#   1. Clears the grubenv `saved_entry` (and related volatile defaults).
#   2. Pins a stable BLS entry-token (/etc/kernel/entry-token) and renames any
#      machine-id-prefixed entry to it, so neither the shipped entry nor future
#      kernel-install runs depend on the volatile machine-id.
#
# The BLS entry *contents* identify the root by UUID and carry no machine-id, so
# renaming the entry file is equivalent to regenerating it under the new token,
# without re-running kernel-install/dracut.

set -euo pipefail
if [[ -f /.profile ]]; then
    . /.profile
fi

echo "config.sh: resetting grub environment for profile(s): ${kiwi_profiles:-<none>}"

GRUBENV="/boot/grub2/grubenv"

if ! command -v grub2-editenv >/dev/null 2>&1; then
    echo "ERROR: grub2-editenv not found in image — cannot reset ${GRUBENV}" >&2
    exit 1
fi

if [[ ! -f "${GRUBENV}" ]]; then
    echo "ERROR: ${GRUBENV} not found — cannot reset saved_entry" >&2
    exit 1
fi

echo "config.sh: grubenv before reset:"
grub2-editenv "${GRUBENV}" list || true

# Remove the build-time default selection and related volatile state so the
# shipped grubenv carries no machine-id-specific data. `unset` is a no-op for
# variables that are not present.
grub2-editenv "${GRUBENV}" unset saved_entry
grub2-editenv "${GRUBENV}" unset prev_saved_entry
grub2-editenv "${GRUBENV}" unset next_entry

# Fail the build if a saved_entry survives — shipping a stale default is exactly
# the defect this hook exists to prevent.
if grub2-editenv "${GRUBENV}" list | grep -q '^saved_entry='; then
    echo "ERROR: saved_entry is still set in ${GRUBENV} after reset" >&2
    exit 1
fi

echo "config.sh: grubenv after reset:"
grub2-editenv "${GRUBENV}" list || true

# ---------------------------------------------------------------------------
# Pin a stable BLS entry-token and reconcile existing entries.
# ---------------------------------------------------------------------------
# entry-token is the prefix kernel-install uses when naming BootLoaderSpec
# entries (<entry-token>-<kver>.conf). Without /etc/kernel/entry-token it falls
# back to /etc/machine-id, which is volatile for a redistributable image. Pin it
# to the os-release ID so entry names are stable across the first-boot
# machine-id regeneration and all later kernel installs.
ENTRY_TOKEN="azurelinux"
BLS_DIR="/boot/loader/entries"

mkdir -p /etc/kernel
printf '%s\n' "${ENTRY_TOKEN}" > /etc/kernel/entry-token
echo "config.sh: pinned BLS entry-token to '${ENTRY_TOKEN}'"

if [[ -d "${BLS_DIR}" ]]; then
    shopt -s nullglob
    for conf in "${BLS_DIR}"/*.conf; do
        base="$(basename "${conf}")"
        # Match entries named <32-hex-machine-id>-<kver>.conf and rebase them
        # onto the stable entry-token. Entries that already use a non-machine-id
        # token are left untouched.
        if [[ "${base}" =~ ^[0-9a-f]{32}-(.+)\.conf$ ]]; then
            kver="${BASH_REMATCH[1]}"
            dest="${BLS_DIR}/${ENTRY_TOKEN}-${kver}.conf"
            echo "config.sh: renaming BLS entry ${base} -> $(basename "${dest}")"
            mv -f "${conf}" "${dest}"
        fi
    done
    shopt -u nullglob
fi

# Fail the build if any machine-id-prefixed entry survives — shipping one is the
# defect this hook exists to prevent.
stale_entries="$(find "${BLS_DIR}" -maxdepth 1 -type f -name '*.conf' \
    -regextype posix-extended -regex '.*/[0-9a-f]{32}-.*\.conf' 2>/dev/null || true)"
if [[ -n "${stale_entries}" ]]; then
    echo "ERROR: machine-id-prefixed BLS entries remain after reconciliation:" >&2
    echo "${stale_entries}" >&2
    exit 1
fi

# Never ship an image with no boot entries.
if ! compgen -G "${BLS_DIR}/*.conf" >/dev/null; then
    echo "ERROR: no BLS entries present in ${BLS_DIR} after reconciliation" >&2
    exit 1
fi

echo "config.sh: BLS entries after reconciliation:"
ls -1 "${BLS_DIR}"
