#!/bin/bash

set -euo pipefail

esp=/boot/efi
vendor_dir="$esp/EFI/azurelinux"
fallback_dir="$esp/EFI/BOOT"
uki_dir="$esp/EFI/Linux"

shim=$(find /usr/share/shim -type f -path '*/x64/shimx64.efi' -print -quit)
systemd_boot=/usr/lib/systemd/boot/efi/systemd-bootx64.efi
uki=$(find /lib/modules -mindepth 2 -maxdepth 2 -type f -name 'vmlinuz-virt.efi' -print | sort -V | tail -n 1)

if [[ -z "$shim" || ! -f "$systemd_boot" || -z "$uki" ]]; then
    echo "Missing shim, systemd-boot, or UKI payload" >&2
    echo "shim=${shim:-<missing>}" >&2
    echo "systemd_boot=$systemd_boot" >&2
    echo "uki=${uki:-<missing>}" >&2
    exit 1
fi

mkdir -p "$vendor_dir" "$fallback_dir" "$uki_dir" "$esp/loader"

# Shim is built with \\grubx64.efi as its second-stage path. Keep that ABI while
# placing systemd-boot, rather than GRUB, at the expected location.
install -m 0644 "$shim" "$vendor_dir/shimx64.efi"
install -m 0644 "$systemd_boot" "$vendor_dir/grubx64.efi"
install -m 0644 "$shim" "$fallback_dir/BOOTX64.EFI"
install -m 0644 "$systemd_boot" "$fallback_dir/grubx64.efi"

kernel_version=$(basename "$(dirname "$uki")")
install -m 0644 "$uki" "$uki_dir/azurelinux-$kernel_version.efi"

cat > "$esp/loader/loader.conf" <<'EOF'
default azurelinux-*
timeout 3
console-mode keep
EOF

systemctl enable cloud-init-local.service cloud-init.service cloud-config.service cloud-final.service
systemctl enable sshd.service systemd-networkd.service systemd-resolved.service
ln -sfn /run/systemd/resolve/stub-resolv.conf /etc/resolv.conf

rm -f /etc/machine-id
touch /etc/machine-id

echo "CVM PoC ESP staging complete:"
find "$esp/EFI" -maxdepth 3 -type f -print