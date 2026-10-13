#!/bin/sh

set -eu

# KIWI invokes this without arguments; a path may be supplied for direct testing.
fstab=${1:-/etc/fstab}

# KIWI generates this row, so only the filesystem UUID is image-specific.
# Accept the generated row and an already-configured row so reruns are safe.
efi_entry='^[[:space:]]*(UUID=[^[:space:]]+)[[:space:]]+/boot/efi[[:space:]]+vfat[[:space:]]+defaults(,umask=[^,[:space:]]+)?(,noexec,nodev,nosuid,nosymfollow)?[[:space:]]+0[[:space:]]+0[[:space:]]*$'

# Reject an unexpected fstab shape instead of preserving fields that KIWI owns.
if ! grep -Eq "$efi_entry" "$fstab"; then
    echo "Expected KIWI EFI system partition entry not found in $fstab" >&2
    exit 1
fi

# FAT has no Unix mode bits. Restrict access and apply the Boot Loader
# Specification mount flags through the ESP's mount options.
sed -E -i "s|$efi_entry|\\1 /boot/efi vfat defaults,umask=0077,noexec,nodev,nosuid,nosymfollow 0 0|" "$fstab"
