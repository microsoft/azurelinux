#!/bin/bash
set -euo pipefail

# Assemble the UkiBootCore EFI system partition during KIWI image preparation.
# KIWI's systemd_boot support cannot install shim or consume Azure Linux's
# packaged virt UKI, so this hook stages the existing package payloads into the
# shim -> systemd-boot -> UKI layout.

die() {
    echo "ERROR: $*" >&2
    exit 1
}

# KIWI runs the hook inside the image root. UKI_ROOT provides an equivalent
# root prefix for isolated tests. The stable token keeps initial and updated
# UKI filenames in the same boot-loader entry namespace.
root="${UKI_ROOT:-}"
token_file="$root/etc/kernel/entry-token"
[[ -f "$token_file" ]] || die "missing kernel entry token: $token_file"
IFS= read -r token < "$token_file" ||
    die "kernel entry token must be exactly azurelinux followed by a newline"
[[ "$token" == azurelinux && $(wc -c < "$token_file") -eq 11 ]] ||
    die "kernel entry token must be exactly azurelinux followed by a newline"

# Identify the packaged systemd-boot payload and map its architecture-specific
# filename to the fallback name used by firmware and the second-stage name
# compiled into shim. Despite its name, grubx64.efi contains systemd-boot.
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

# Shim packages may expose multiple version-directory aliases for one file.
# Resolve those aliases and reject genuinely ambiguous shim payloads.
shims=("$root"/usr/share/shim/*/x64/"$shim_name")
declare -A resolved_shims=()
for shim in "${shims[@]}"; do
    resolved=$(realpath -e -- "$shim") || die "cannot resolve shim payload: $shim"
    resolved_shims["$resolved"]=1
done
((${#resolved_shims[@]} == 1)) || die "expected exactly one unsigned $shim_name payload"
shims=("${!resolved_shims[@]}")

# Select the newest packaged virt UKI using version-aware ordering. The derived
# module-directory name becomes the version portion of the Type #2 entry name.
ukis=("$root"/lib/modules/*/vmlinuz-virt.efi)
((${#ukis[@]} > 0)) || die "no packaged virt UKI found"
mapfile -t sorted_ukis < <(printf '%s\n' "${ukis[@]}" | sort -V)
uki="${sorted_ukis[-1]}"
version="${uki%/vmlinuz-virt.efi}"
version="${version##*/}"

# Stage the firmware fallback, shim's second stage, and the Type #2 UKI entry.
esp="$root/boot/efi"
target_uki="$esp/EFI/Linux/$token-$version.efi"
install -Dm0644 "${shims[0]}" "$esp/EFI/BOOT/$fallback"
install -Dm0644 "${boot_payloads[0]}" "$esp/EFI/BOOT/$second_stage"
install -Dm0644 "$uki" "$target_uki"

# Configure systemd-boot to select this token's newest UKI.
mkdir -p "$esp/loader"
printf 'default %s-*\ntimeout 1\n' "$token" > "$esp/loader/loader.conf"
chmod 0644 "$esp/loader/loader.conf"
