#!/bin/bash
# SPDX-License-Identifier: MIT

set -euo pipefail

fail() {
    echo "Experimental no-initrd boot: $*" >&2
    exit 1
}

[[ $# == 2 ]] || fail "expected disk image and boot partition device"
root_device="$2"
[[ "$(blkid -p -s TYPE -o value "$root_device")" == ext4 ]] \
    || fail "boot partition must be the plain ext4 root (no separate /boot)"
partuuid="$(blkid -p -s PART_ENTRY_UUID -o value "$root_device")"
[[ "$partuuid" =~ ^[[:xdigit:]]{8}-[[:xdigit:]]{4}-[[:xdigit:]]{4}-[[:xdigit:]]{4}-[[:xdigit:]]{12}$ ]] \
    || fail "root must have a GPT partition UUID"
filesystem_uuid="$(blkid -p -s UUID -o value "$root_device")"

# KIWI has unmounted the final disk here; the working tree is not the disk.
root="$(mktemp -d "$PWD/.experimental-noinitrd.XXXXXX")"
mounted=false
cleanup() {
    status=$?
    if "$mounted"; then
        umount "$root" || status=$?
    fi
    rmdir "$root" || status=$?
    exit "$status"
}
trap cleanup EXIT
mount "$root_device" "$root"
mounted=true

fstab_root="$(awk '$2 == "/" {print $1}' "$root/etc/fstab")"
[[ "$fstab_root" == "UUID=$filesystem_uuid" || "$fstab_root" == "PARTUUID=$partuuid" ]] \
    || fail "boot partition does not match the final disk's root in fstab"

shopt -s nullglob
entries=("$root"/boot/loader/entries/*.conf)
[[ ${#entries[@]} == 1 ]] || fail "expected exactly one initrd-backed BLS entry"
recovery="${entries[0]}"
kernel_path="$(awk '$1 == "linux" {print $2}' "$recovery")"
[[ "$kernel_path" =~ ^/boot/vmlinuz-[^/]+$ && -s "$root$kernel_path" ]] \
    || fail "expected a kernel on the root filesystem under /boot"
version="${kernel_path#/boot/vmlinuz-}"
config="$root/usr/lib/modules/$version/config"
if [[ ! -f "$config" ]]; then
    config="$root/boot/config-$version"
fi
[[ -f "$config" ]] || fail "missing kernel configuration for $version"
for option in \
    X86_64 EFI EFI_PARTITION DEVTMPFS DEVTMPFS_MOUNT \
    NVME_CORE BLK_DEV_NVME SCSI BLK_DEV_SD HYPERV HYPERV_STORAGE \
    EXT4_FS JBD2 SECURITY_SELINUX CRYPTO_CRC32C CRC32; do
    grep -Fxq "CONFIG_$option=y" "$config" \
        || fail "CONFIG_$option must be built in"
done
for module in hv_netvsc hv_sock; do
    chroot "$root" modinfo -k "$version" "$module" > /dev/null
done

mapfile -t initrds < <(awk '$1 == "initrd" {for (i = 2; i <= NF; i++) print $i}' "$recovery")
[[ ${#initrds[@]} -gt 0 ]] || fail "missing initrd-backed recovery entry"
for initrd in "${initrds[@]}"; do
    [[ "$initrd" == /boot/* && -s "$root$initrd" ]] \
        || fail "recovery initrd is missing: $initrd"
done
grep -Eq '^GRUB_DEFAULT="?saved"?$' "$root/etc/default/grub" \
    || fail "GRUB must use the saved entry"
grep -q 'saved_entry' "$root/boot/grub2/grub.cfg" \
    || fail "generated GRUB configuration does not use saved_entry"

recovery_id="$(basename "$recovery" .conf)"
entry_id="$recovery_id-noinitrd"
entry="$root/boot/loader/entries/$entry_id.conf"
awk -v partuuid="$partuuid" '
    $1 == "initrd" { next }
    $1 == "linux" { kernels++ }
    $1 == "title" { titles++; print $0 " (experimental no initrd)"; next }
    $1 == "options" {
        options++
        printf "options"
        for (i = 2; i <= NF; i++) {
            if ($i ~ /^(fips=1|rd\.luks|rd\.lvm|rd\.md|\$kernelopts)/) exit 1
            if ($i !~ /^(root=|rootfstype=|rootwait(=|$)|ro$|rw$)/) printf " %s", $i
        }
        printf " root=PARTUUID=%s rootfstype=ext4 ro rootwait\n", partuuid
        next
    }
    { print }
    END { if (kernels != 1 || titles != 1 || options != 1) exit 1 }
' "$recovery" > "$entry" || fail "unsupported BLS entry or initrd-dependent options"
chmod --reference="$recovery" "$entry"
printf '%s\n' "$recovery_id" > "$root/etc/azurelinux-noinitrd-recovery-entry"
chroot "$root" restorecon "/boot/loader/entries/$entry_id.conf" /etc/azurelinux-noinitrd-recovery-entry
chroot "$root" grub2-editenv /boot/grub2/grubenv set "saved_entry=$entry_id"
chroot "$root" grub2-editenv /boot/grub2/grubenv list | grep -Fxq "saved_entry=$entry_id" \
    || fail "no-initrd default was not saved"
echo "Experimental default: $entry_id; initrd recovery: $recovery_id"
