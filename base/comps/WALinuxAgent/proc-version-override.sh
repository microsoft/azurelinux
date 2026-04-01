#!/usr/bin/bash
# Generate a /proc/version override file that includes "CBL-Mariner" in the
# user@host field so legacy tools (e.g. Guest-Configuration-Extension) that
# grep for "Mariner" can identify this OS.
#
# The real kernel version, compiler string, and build timestamp are preserved.
# Only the "(user@host)" group is replaced with "(root@CBL-Mariner-azurelinux)".

set -euo pipefail

OVERRIDE="/run/proc_version_override"
KVER=$(uname -r)

# Strip the first parenthesised group (user@host) and keep everything after it.
TAIL=$(sed 's/^[^)]*)[[:space:]]*//' /proc/version)

printf 'Linux version %s (root@CBL-Mariner-azurelinux) %s\n' \
    "${KVER}" "${TAIL}" > "${OVERRIDE}"
