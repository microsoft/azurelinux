#!/bin/bash
# Generate a /proc/version override that includes both "CBL-Mariner" and
# "azurelinux" identifiers, then bind-mount it over /proc/version.
#
# This preserves backward compatibility with tools that grep /proc/version
# for "Mariner" (e.g. Guest-Configuration-Extension) while also advertising
# the current distro name.

set -euo pipefail

OVERRIDE=/run/proc_version_override

# `mount --bind` on a file target is not idempotent; repeated runs can stack
# mounts on /proc/version. Unwind any existing mount layers before reading
# the real /proc/version and rebinding.
while findmnt -n /proc/version >/dev/null 2>&1; do
    umount /proc/version
done

# Build a version string using the real kernel version, replacing only
# the (user@host) field with (root@CBL-Mariner-azurelinux).
#
# Real /proc/version format:
#   Linux version <uname -r> (mockbuild@koji-builder-...) (gcc (GCC) ...) #1 SMP ...
# Override:
#   Linux version <uname -r> (root@CBL-Mariner-azurelinux) (gcc (GCC) ...) #1 SMP ...
#
# We strip the first parenthesized group (user@host) and keep everything
# after it (compiler info, build config, timestamp) verbatim.
# Also replace "Red Hat" in the GCC version string so tools that pattern-match
# /proc/version (e.g. GCE's guest-configuration-shim) don't misidentify AZL as
# RHEL based on the compiler tag.
KVER=$(uname -r)
TAIL=$(sed 's/^[^)]*)[[:space:]]*//' /proc/version | sed 's/Red Hat/Azure Linux/g')

install -m 0444 /dev/null "$OVERRIDE"
cat > "$OVERRIDE" <<EOF
Linux version ${KVER} (root@CBL-Mariner-azurelinux) ${TAIL}
EOF
chmod 0444 "$OVERRIDE"

mount --bind "$OVERRIDE" /proc/version
mount -o remount,bind,ro /proc/version
