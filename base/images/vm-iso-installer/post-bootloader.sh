#!/bin/bash
# post-bootloader.sh — UEFI bootloader setup (%post --nochroot script for kickstart)
# Runs in the installer environment (NOT chrooted into the target).
# Validates grub.cfg, copies EFI binaries to fallback path, fixes NVRAM.
set -x
SYSROOT=/mnt/sysroot

fail() {
    echo "FATAL: $*" >&2
    exit 1
}

echo "=== Target mounts ==="
findmnt -R "$SYSROOT" 2>/dev/null || mount | grep sysroot

echo "=== fstab ==="
cat "$SYSROOT/etc/fstab" 2>/dev/null
echo "=== crypttab ==="
cat "$SYSROOT/etc/crypttab" 2>/dev/null

# --- Get partition UUIDs via blkid (direct device access) ---
BOOT_DEV=$(findmnt -n -o SOURCE "$SYSROOT/boot" 2>/dev/null)
BOOT_UUID=$(blkid -s UUID -o value "$BOOT_DEV" 2>/dev/null)
echo "Boot: dev=$BOOT_DEV uuid=$BOOT_UUID"

# Fallback: parse fstab
if [ -z "$BOOT_UUID" ]; then
    BOOT_UUID=$(awk '$2 == "/boot" { sub(/^UUID=/, "", $1); print $1 }' "$SYSROOT/etc/fstab" 2>/dev/null)
fi
[ -n "$BOOT_UUID" ] || fail "Could not determine the target boot UUID"

# Never accept a static fallback: it would stay pinned after kernel updates.
GRUB_CONFIG="$SYSROOT/boot/grub2/grub.cfg"
[ -s "$GRUB_CONFIG" ] || fail "Target GRUB configuration is missing"
chroot "$SYSROOT" grub2-script-check /boot/grub2/grub.cfg ||
    fail "Target GRUB configuration is invalid"
grep -Eq '^[[:space:]]*blscfg([[:space:]]|$)' "$GRUB_CONFIG" ||
    fail "Target GRUB configuration does not use blscfg"
grub_env=$(chroot "$SYSROOT" grub2-editenv - list) ||
    fail "Cannot read the target GRUB environment"
saved_entry=$(awk -F= '$1 == "saved_entry" {print $2}' <<< "$grub_env")
[[ -n "$saved_entry" && "$saved_entry" != */* &&
   -s "$SYSROOT/boot/loader/entries/${saved_entry}.conf" ]] ||
    fail "Target GRUB saved default has no BLS entry"

set -eE -o pipefail
trap 'echo "FATAL: EFI bootloader setup failed at line $LINENO" >&2' ERR

# --- Find or create EFI vendor directory ---
EFI_VENDOR=""
for d in "$SYSROOT/boot/efi/EFI/azurelinux" "$SYSROOT/boot/efi/EFI/fedora"; do
    [ -d "$d" ] && { EFI_VENDOR="$d"; break; }
done
[ -z "$EFI_VENDOR" ] && { EFI_VENDOR="$SYSROOT/boot/efi/EFI/azurelinux"; mkdir -p "$EFI_VENDOR"; }
EFI_VENDOR_NAME=$(basename "$EFI_VENDOR")
echo "EFI vendor dir: $EFI_VENDOR"
ls -la "$EFI_VENDOR/" 2>/dev/null

echo "--- /boot/grub2/grub.cfg ---"
cat "$GRUB_CONFIG"

# --- Create EFI stub grub.cfg ---
if [ -n "$BOOT_UUID" ]; then
    cat > "$EFI_VENDOR/grub.cfg" << STUBCFG
search --no-floppy --root-dev-only --fs-uuid --set=dev ${BOOT_UUID}
set prefix=(\$dev)/grub2
export \$prefix
configfile \$prefix/grub.cfg
STUBCFG
fi

# --- Detect architecture for EFI binary names ---
EFI_ARCH=$(uname -m)
case "$EFI_ARCH" in
    x86_64)  SHIM_EFI="shimx64.efi"; GRUB_EFI="grubx64.efi"; BOOT_EFI="BOOTX64.EFI" ;;
    aarch64) SHIM_EFI="shimaa64.efi"; GRUB_EFI="grubaa64.efi"; BOOT_EFI="BOOTAA64.EFI" ;;
    *) fail "Unsupported EFI architecture: $EFI_ARCH" ;;
esac

# --- Copy EFI binaries + grub.cfg to fallback boot path ---
mkdir -p "$SYSROOT/boot/efi/EFI/BOOT"
if [ -f "$EFI_VENDOR/$SHIM_EFI" ]; then
    cp -vf "$EFI_VENDOR/$SHIM_EFI"   "$SYSROOT/boot/efi/EFI/BOOT/$BOOT_EFI"
    cp -vf "$EFI_VENDOR/$GRUB_EFI"   "$SYSROOT/boot/efi/EFI/BOOT/$GRUB_EFI"
    cp -vf "$EFI_VENDOR/grub.cfg"    "$SYSROOT/boot/efi/EFI/BOOT/grub.cfg"
elif [ -f "$EFI_VENDOR/$GRUB_EFI" ]; then
    cp -vf "$EFI_VENDOR/$GRUB_EFI"   "$SYSROOT/boot/efi/EFI/BOOT/$BOOT_EFI"
    cp -vf "$EFI_VENDOR/grub.cfg"    "$SYSROOT/boot/efi/EFI/BOOT/grub.cfg"
else
    fail "No EFI binaries found in $EFI_VENDOR"
fi

echo "=== Final ESP contents ==="
ls -laR "$SYSROOT/boot/efi/" 2>/dev/null

# --- Fix UEFI NVRAM boot entry ---
ESP_DEV=$(findmnt -n -o SOURCE "$SYSROOT/boot/efi" 2>/dev/null) || ESP_DEV=""
if [ -n "$ESP_DEV" ]; then
    ESP_DISK=$(echo "$ESP_DEV" | sed 's/[0-9]*$//')
    ESP_PART=$(echo "$ESP_DEV" | grep -o '[0-9]*$')
    echo "ESP: dev=$ESP_DEV disk=$ESP_DISK part=$ESP_PART"

    echo "=== Current UEFI boot entries ==="
    efibootmgr 2>/dev/null || true
    for bootnum in $(efibootmgr 2>/dev/null | grep -i 'default\\\|anaconda\|fedora\|azurelinux' | sed 's/Boot\([0-9A-Fa-f]*\).*/\1/'); do
        echo "Removing stale entry Boot$bootnum"
        efibootmgr -b "$bootnum" -B 2>/dev/null || true
    done

    EFI_NVRAM_PATH="\\EFI\\${EFI_VENDOR_NAME}\\${SHIM_EFI}"
    efibootmgr -c -d "$ESP_DISK" -p "$ESP_PART" \
        -L "Azure Linux" -l "$EFI_NVRAM_PATH" 2>/dev/null && \
        echo "Created UEFI boot entry: Azure Linux -> $EFI_NVRAM_PATH" || \
        echo "WARNING: efibootmgr -c failed"

    echo "=== Updated UEFI boot entries ==="
    efibootmgr 2>/dev/null || true
else
    echo "WARNING: Could not find ESP mount — skipping NVRAM fix"
fi
