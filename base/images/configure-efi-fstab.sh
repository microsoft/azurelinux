#!/bin/sh

set -eu

# KIWI invokes this without arguments; a path may be supplied for direct testing.
fstab=${1:-/etc/fstab}

# FAT has no Unix mode bits, so restrict the ESP through its mount options.
# fstab field 2 is the mountpoint and field 4 contains the mount options.
# Match an active row whose first field is a device and whose second field is
# either of the conventional EFI system partition mountpoints.
efi_entry='^[[:space:]]*[^#[:space:]][^[:space:]]*[[:space:]]+/(boot/)?efi[[:space:]]+'

# sed exits successfully when no rows match, so detect a malformed UEFI image
# before attempting the edit.
if ! grep -Eq "$efi_entry" "$fstab"; then
    echo "No EFI system partition entry found in $fstab" >&2
    exit 1
fi

sed -E -i "
# Use | as the address delimiter because the mountpoint pattern contains /.
\\|$efi_entry| {
    # Replace any existing umask value and stop processing this row so the
    # append expression below does not add a duplicate.
    /umask=[^,[:space:]]+/ {
        s/umask=[^,[:space:]]+/umask=0077/g
        b
    }

    # No umask exists: capture fields 1-4, then append to the options field
    # before preserving the remaining dump and pass fields unchanged.
    s/^(([^[:space:]]+[[:space:]]+){3}[^[:space:]]+)/\\1,umask=0077/
}
" "$fstab"
