#!/bin/bash
# post-bootloader.sh — UEFI bootloader setup (%post --nochroot script for kickstart)
# Runs in the installer environment (NOT chrooted into the target).
# Generates grub.cfg, copies EFI binaries to fallback path, fixes NVRAM.
set -x
SYSROOT=/mnt/sysroot

echo "=== Target mounts ==="
findmnt -R "$SYSROOT" 2>/dev/null || mount | grep sysroot

echo "=== fstab ==="
cat "$SYSROOT/etc/fstab" 2>/dev/null
echo "=== crypttab ==="
cat "$SYSROOT/etc/crypttab" 2>/dev/null

# --- Get partition UUIDs via blkid (direct device access) ---
BOOT_DEV=$(findmnt -n -o SOURCE "$SYSROOT/boot" 2>/dev/null)
BOOT_UUID=$(blkid -s UUID -o value "$BOOT_DEV" 2>/dev/null)
ROOT_DEV=$(findmnt -n -o SOURCE "$SYSROOT" 2>/dev/null)
ROOT_UUID=$(blkid -s UUID -o value "$ROOT_DEV" 2>/dev/null)

echo "Boot: dev=$BOOT_DEV uuid=$BOOT_UUID"
echo "Root: dev=$ROOT_DEV uuid=$ROOT_UUID"

# Fallback: parse fstab
if [ -z "$BOOT_UUID" ]; then
    BOOT_UUID=$(awk '$2 == "/boot" { sub(/^UUID=/, "", $1); print $1 }' "$SYSROOT/etc/fstab" 2>/dev/null)
fi
if [ -z "$ROOT_UUID" ]; then
    ROOT_UUID=$(awk '$2 == "/" { sub(/^UUID=/, "", $1); print $1 }' "$SYSROOT/etc/fstab" 2>/dev/null)
fi

# --- Find installed kernel and initramfs ---
KERNEL=$(ls "$SYSROOT"/boot/vmlinuz-* 2>/dev/null | sort -V | tail -1)
INITRD=$(ls "$SYSROOT"/boot/initramfs-*.img 2>/dev/null | sort -V | tail -1)
KERNEL_NAME=$(basename "$KERNEL")
INITRD_NAME=$(basename "$INITRD")
echo "Kernel: $KERNEL_NAME  Initrd: $INITRD_NAME"

if [ -z "$BOOT_UUID" ] || [ -z "$ROOT_UUID" ]; then
    echo "!!! FATAL: Could not determine boot ($BOOT_UUID) or root ($ROOT_UUID) UUID"
    echo "!!! Bootloader setup SKIPPED — system may not boot"
    echo "=== blkid output ==="
    blkid 2>/dev/null
    echo "=== mount output ==="
    mount 2>/dev/null
    exit 0
fi

if [ -z "$KERNEL_NAME" ] || [ -z "$INITRD_NAME" ]; then
    echo "!!! FATAL: No kernel ($KERNEL_NAME) or initramfs ($INITRD_NAME) found in $SYSROOT/boot/"
    ls -la "$SYSROOT/boot/" 2>/dev/null
    exit 0
fi

# --- Detect LUKS encryption ---
LUKS_PARAMS=""
for luks_dev in $(blkid -t TYPE=crypto_LUKS -o device 2>/dev/null); do
    LUKS_UUID=$(cryptsetup luksUUID "$luks_dev" 2>/dev/null) && {
        LUKS_PARAMS="rd.luks.uuid=luks-${LUKS_UUID}"
        echo "Detected LUKS device: $luks_dev UUID=$LUKS_UUID"
        break
    }
done

# --- Find or create EFI vendor directory ---
EFI_VENDOR=""
for d in "$SYSROOT/boot/efi/EFI/azurelinux" "$SYSROOT/boot/efi/EFI/fedora"; do
    [ -d "$d" ] && { EFI_VENDOR="$d"; break; }
done
[ -z "$EFI_VENDOR" ] && { EFI_VENDOR="$SYSROOT/boot/efi/EFI/azurelinux"; mkdir -p "$EFI_VENDOR"; }
EFI_VENDOR_NAME=$(basename "$EFI_VENDOR")
echo "EFI vendor dir: $EFI_VENDOR"
ls -la "$EFI_VENDOR/" 2>/dev/null

# --- Generate /boot/grub2/grub.cfg ---
mkdir -p "$SYSROOT/boot/grub2"
cat > "$SYSROOT/boot/grub2/grub.cfg" << GRUBCFG
set default=0
set timeout=2
serial --speed=115200 --unit=0 --word=8 --parity=no --stop=1
terminal_output console serial
terminal_input console serial

menuentry "Azure Linux" {
    search --no-floppy --fs-uuid --set=root ${BOOT_UUID}
    linux /${KERNEL_NAME} root=UUID=${ROOT_UUID} ${LUKS_PARAMS} console=ttyS0,115200 console=tty0 ro
    initrd /${INITRD_NAME}
}

menuentry "Azure Linux (rescue)" {
    search --no-floppy --fs-uuid --set=root ${BOOT_UUID}
    linux /${KERNEL_NAME} root=UUID=${ROOT_UUID} ${LUKS_PARAMS} console=ttyS0,115200 console=tty0 ro systemd.unit=rescue.target
    initrd /${INITRD_NAME}
}

menuentry "UEFI Firmware Settings" --id "uefi-firmware" {
    fwsetup
}
GRUBCFG
echo "--- /boot/grub2/grub.cfg ---"
cat "$SYSROOT/boot/grub2/grub.cfg"

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
esac

# --- Copy EFI binaries + grub.cfg to fallback boot path ---
mkdir -p "$SYSROOT/boot/efi/EFI/BOOT"
if [ -f "$EFI_VENDOR/$SHIM_EFI" ]; then
    cp -vf "$EFI_VENDOR/$SHIM_EFI"   "$SYSROOT/boot/efi/EFI/BOOT/$BOOT_EFI"
    cp -vf "$EFI_VENDOR/$GRUB_EFI"   "$SYSROOT/boot/efi/EFI/BOOT/$GRUB_EFI"   2>/dev/null || true
    cp -vf "$EFI_VENDOR/grub.cfg"    "$SYSROOT/boot/efi/EFI/BOOT/grub.cfg"     2>/dev/null || true
elif [ -f "$EFI_VENDOR/$GRUB_EFI" ]; then
    cp -vf "$EFI_VENDOR/$GRUB_EFI"   "$SYSROOT/boot/efi/EFI/BOOT/$BOOT_EFI"
    cp -vf "$EFI_VENDOR/grub.cfg"    "$SYSROOT/boot/efi/EFI/BOOT/grub.cfg"     2>/dev/null || true
else
    echo "!!! WARNING: No EFI binaries found!"
    find "$SYSROOT/boot/efi" -type f -name "*.efi" 2>/dev/null
fi

echo "=== Final ESP contents ==="
ls -laR "$SYSROOT/boot/efi/" 2>/dev/null

# --- Fix UEFI NVRAM boot entry ---
ESP_DEV=$(findmnt -n -o SOURCE "$SYSROOT/boot/efi" 2>/dev/null)
if [ -n "$ESP_DEV" ]; then
    ESP_DISK=$(echo "$ESP_DEV" | sed 's/[0-9]*$//')
    ESP_PART=$(echo "$ESP_DEV" | grep -o '[0-9]*$')
    echo "ESP: dev=$ESP_DEV disk=$ESP_DISK part=$ESP_PART"

    echo "=== Current UEFI boot entries ==="
    efibootmgr 2>/dev/null
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
    efibootmgr 2>/dev/null
else
    echo "WARNING: Could not find ESP mount — skipping NVRAM fix"
fi
