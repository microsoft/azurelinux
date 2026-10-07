#!/bin/bash

set -euo pipefail

esp=/boot/efi
vendor_dir="$esp/EFI/azurelinux"
fallback_dir="$esp/EFI/BOOT"
uki_dir="$esp/EFI/Linux"

shopt -s nullglob
systemd_boot_payloads=(/usr/lib/systemd/boot/efi/systemd-boot*.efi)
if ((${#systemd_boot_payloads[@]} != 1)); then
    echo "Expected exactly one systemd-boot EFI payload, found ${#systemd_boot_payloads[@]}" >&2
    exit 1
fi
systemd_boot=${systemd_boot_payloads[0]}
efi_name=${systemd_boot##*/}
efi_arch=${efi_name#systemd-boot}
efi_arch=${efi_arch%.efi}
case "$efi_arch" in
    x64)
        shim_dir=x64
        shim_name=shimx64.efi
        second_stage=grubx64.efi
        fallback_name=BOOTX64.EFI
        ;;
    *)
        echo "Unsupported systemd-boot EFI architecture: $efi_arch" >&2
        exit 1
        ;;
esac

shim=$(find /usr/share/shim -type f -path "*/$shim_dir/$shim_name" -print -quit)
uki=$(find /lib/modules -mindepth 2 -maxdepth 2 -type f -name 'vmlinuz-virt.efi' -print | sort -V | tail -n 1)

if [[ -z "$shim" || ! -f "$systemd_boot" || -z "$uki" ]]; then
    echo "Missing shim, systemd-boot, or UKI payload" >&2
    echo "shim=${shim:-<missing>}" >&2
    echo "systemd_boot=$systemd_boot" >&2
    echo "uki=${uki:-<missing>}" >&2
    exit 1
fi

entry_token_file=/etc/kernel/entry-token
if [[ ! -f "$entry_token_file" ]]; then
    echo "Missing kernel entry token: $entry_token_file" >&2
    exit 1
fi
entry_token=$(< "$entry_token_file")
if [[ "$entry_token" != azurelinux ]]; then
    echo "Unexpected kernel entry token: $entry_token" >&2
    exit 1
fi

mkdir -p "$vendor_dir" "$fallback_dir" "$uki_dir" "$esp/loader"

# Shim expects a GRUB-named second stage; keep that ABI with systemd-boot.
install -m 0644 "$shim" "$vendor_dir/$shim_name"
install -m 0644 "$systemd_boot" "$vendor_dir/$second_stage"
install -m 0644 "$shim" "$fallback_dir/$fallback_name"
install -m 0644 "$systemd_boot" "$fallback_dir/$second_stage"

kernel_version=$(basename "$(dirname "$uki")")
install -m 0644 "$uki" "$uki_dir/$entry_token-$kernel_version.efi"

printf 'default %s-*\ntimeout 3\nconsole-mode keep\n' "$entry_token" > "$esp/loader/loader.conf"

echo "CVM ESP staging complete:"
find "$esp/EFI" -maxdepth 3 -type f -print
