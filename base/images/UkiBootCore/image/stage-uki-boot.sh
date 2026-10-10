#!/bin/bash
set -euo pipefail

die() {
    echo "ERROR: $*" >&2
    exit 1
}

root="${UKI_ROOT:-}"
token_file="$root/etc/kernel/entry-token"
[[ -f "$token_file" ]] || die "missing kernel entry token: $token_file"
IFS= read -r token < "$token_file" ||
    die "kernel entry token must be exactly azurelinux followed by a newline"
[[ "$token" == azurelinux && $(wc -c < "$token_file") -eq 11 ]] ||
    die "kernel entry token must be exactly azurelinux followed by a newline"

shopt -s nullglob
boot_payloads=("$root"/usr/lib/systemd/boot/efi/systemd-boot*.efi)
((${#boot_payloads[@]} == 1)) || die "expected exactly one systemd-boot EFI payload"
case "${boot_payloads[0]##*/}" in
    systemd-bootx64.efi)
        shim_name=shimx64.efi
        second_stage=grubx64.efi
        fallback=BOOTX64.EFI
        ;;
    *)
        die "unsupported systemd-boot EFI payload: ${boot_payloads[0]##*/}"
        ;;
esac

shims=("$root"/usr/share/shim/*/x64/"$shim_name")
declare -A resolved_shims=()
for shim in "${shims[@]}"; do
    resolved=$(realpath -e -- "$shim") || die "cannot resolve shim payload: $shim"
    resolved_shims["$resolved"]=1
done
((${#resolved_shims[@]} == 1)) || die "expected exactly one unsigned $shim_name payload"
shims=("${!resolved_shims[@]}")
ukis=("$root"/lib/modules/*/vmlinuz-virt.efi)
((${#ukis[@]} > 0)) || die "no packaged virt UKI found"
mapfile -t sorted_ukis < <(printf '%s\n' "${ukis[@]}" | sort -V)
uki="${sorted_ukis[-1]}"
version="${uki%/vmlinuz-virt.efi}"
version="${version##*/}"

# KIWI's systemd_boot bootloader cannot install shim or consume the packaged UKI.
esp="$root/boot/efi"
install -Dm0644 "${shims[0]}" "$esp/EFI/BOOT/$fallback"
install -Dm0644 "${boot_payloads[0]}" "$esp/EFI/BOOT/$second_stage"
install -Dm0644 "$uki" "$esp/EFI/Linux/$token-$version.efi"
mkdir -p "$esp/loader"
printf 'default %s-*\ntimeout 1\n' "$token" > "$esp/loader/loader.conf"
chmod 0644 "$esp/loader/loader.conf"
