#!/bin/bash
# post-install.sh — Target system configuration (%post script for kickstart)
# Called from within the installed chroot during anaconda %post.
set -exE -o pipefail
trap 'echo "FATAL: target configuration failed at line $LINENO" >&2' ERR

fail() {
    echo "FATAL: $*" >&2
    exit 1
}

# --- Network configuration ---
cat > /etc/systemd/network/20-wired-dhcp.network << 'NET'
[Match]
Name=en* eth*

[Network]
DHCP=yes

[DHCPv4]
UseDNS=yes
NET

# --- GRUB defaults ---
# GRUB_ENABLE_BLSCFG=true -> grub.cfg uses blscfg to enumerate
#     /boot/loader/entries/ at boot time, so new kernels are picked up
#     automatically instead of a static config pinned to the install kernel.
# Preserve Anaconda's target-specific LVM, LUKS and other boot arguments.
if [ -f /etc/default/grub ]; then
    . /etc/default/grub
fi
target_args="${GRUB_CMDLINE_LINUX:-} ${GRUB_CMDLINE_LINUX_DEFAULT:-}"
target_args+=" console=ttyS0,115200 console=tty0"

# GRUB_DEFAULT=saved lets the distro hooks select newly installed eligible
# kernels, while still supporting an administrator's persistent selection.
cat > /etc/default/grub << 'GRUBDEF'
GRUB_TIMEOUT=2
GRUB_DISTRIBUTOR="Azure Linux"
GRUB_DEFAULT=saved
GRUB_ENABLE_BLSCFG=true
GRUB_DISABLE_SUBMENU=true
GRUB_TERMINAL_OUTPUT="console serial"
GRUB_SERIAL_COMMAND="serial --speed=115200 --unit=0 --word=8 --parity=no --stop=1"
GRUB_DISABLE_RECOVERY=true
GRUBDEF

# --- Boot-order normalization ---
# AZL's grub2 owns kernel-install via 20-grub.install, which writes BLS
# snippets and kernel images to /boot. layout=other avoids systemd's
# alternative layout and lets the distro GRUB/dracut hooks own these files.
mkdir -p /etc/kernel
cat > /etc/kernel/install.conf << 'KINSTALL'
layout=other
initrd_generator=dracut
KINSTALL

# Never inherit /proc/cmdline here: it belongs to the installer, not the target.
root_uuid=$(grub2-probe --target=fs_uuid /)
[ -n "$root_uuid" ] || fail "Cannot determine the target root filesystem UUID"
if [ -s /etc/crypttab ]; then
    while read -r name device rest; do
        [[ -z "$name" || "$name" == \#* ]] && continue
        if [[ "$device" == UUID=* ]]; then
            luks_uuid="${device#UUID=}"
        else
            luks_uuid=$(blkid -s UUID -o value "$device")
        fi
        [ -n "$luks_uuid" ] || fail "Cannot determine LUKS UUID for $name"
        target_args+=" rd.luks.uuid=luks-${luks_uuid}"
    done < /etc/crypttab
fi
read -r -a boot_args <<< "$target_args"
target_args=""
for arg in "${boot_args[@]}"; do
    case "$arg" in
        root=*|ro|rw|BOOT_IMAGE=*|initrd=*) continue ;;
    esac
    target_args+="${target_args:+ }$arg"
done
printf 'GRUB_CMDLINE_LINUX=%q\n' "$target_args" >> /etc/default/grub
kernel_cmdline="root=UUID=${root_uuid} ro ${target_args}"
printf '%s\n' "$kernel_cmdline" > /etc/kernel/cmdline
read -r -a required_args <<< "ro $target_args"

mkdir -p /etc/sysconfig
touch /etc/sysconfig/kernel
sed -i '/^[[:space:]]*UPDATEDEFAULT=/d' /etc/sysconfig/kernel
echo 'UPDATEDEFAULT=yes' >> /etc/sysconfig/kernel
kernel_settings=$(grub2-get-kernel-settings)
grep -qx 'GRUB_UPDATE_DEFAULT_KERNEL=true' <<< "$kernel_settings" ||
    fail "The distro hooks are not configured to update the saved kernel"

# 20-grub.install requires a machine ID; it is cleared again before first boot.
if [ ! -s /etc/machine-id ]; then
    systemd-machine-id-setup
fi

shopt -s nullglob
kernel_versions=()
for kdir in /usr/lib/modules/*; do
    [ -d "$kdir" ] || continue
    kver="${kdir##*/}"
    if [ -f "$kdir/vmlinuz" ] || [ -f "/boot/vmlinuz-$kver" ]; then
        kernel_versions+=("$kver")
    fi
done
[ "${#kernel_versions[@]}" -gt 0 ] || fail "No installed kernels found"
sorted_versions=$(printf '%s\n' "${kernel_versions[@]}" | sort -V)

# Keep existing and rescue entries. Process each kernel once, oldest first,
# so the distro hooks leave the newest eligible kernel as the saved default.
while read -r kver; do
    kimg="/usr/lib/modules/$kver/vmlinuz"
    [ -f "$kimg" ] || kimg="/boot/vmlinuz-$kver"
    echo "Regenerating BLS entry for kernel $kver"
    kernel-install add "$kver" "$kimg"
done <<< "$sorted_versions"

# Regenerate last, so an encrypted target cannot lose crypt support to a
# subsequent kernel-install initramfs rebuild.
if [ -s /etc/crypttab ]; then
    dracut --regenerate-all --force --add crypt
fi
mkdir -p /boot/grub2
grub2-mkconfig -o /boot/grub2/grub.cfg
grub2-script-check /boot/grub2/grub.cfg
grep -Eq '^[[:space:]]*blscfg([[:space:]]|$)' /boot/grub2/grub.cfg ||
    fail "Generated GRUB configuration does not use blscfg"

boot_prefix=""
boot_relpath=$(grub2-mkrelpath /boot)
[ -n "$boot_relpath" ] || boot_prefix="/boot"
validated_entries=()
for kver in "${kernel_versions[@]}"; do
    entries=(/boot/loader/entries/*-"$kver".conf)
    [ "${#entries[@]}" -gt 0 ] || fail "No BLS entry generated for $kver"
    for entry in "${entries[@]}"; do
        linux_path=$(awk '$1 == "linux" {print $2}' "$entry")
        initrd_paths=$(awk '$1 == "initrd" {$1=""; print}' "$entry")
        options=$(awk '$1 == "options" {sub(/^options[ \t]+/, ""); print}' "$entry")
        [[ "$linux_path" == /* && -s "${boot_prefix}${linux_path}" ]] ||
            fail "Missing kernel referenced by $entry"
        [ -n "$initrd_paths" ] || fail "No initramfs referenced by $entry"
        for initrd_path in $initrd_paths; do
            [[ "$initrd_path" == /* && -s "${boot_prefix}${initrd_path}" ]] ||
                fail "Missing initramfs referenced by $entry"
            lsinitrd "${boot_prefix}${initrd_path}" > /dev/null
        done
        # grub2-mkconfig can use a device path instead of UUID for LVM roots.
        # Validate filesystem identity and required arguments, not serialization.
        read -r -a option_args <<< "$options"
        root_count=0
        for arg in "${option_args[@]}"; do
            case "$arg" in
                root=*)
                    root_count=$((root_count + 1))
                    root_spec="${arg#root=}"
                    case "$root_spec" in
                        UUID=*) entry_root_uuid="${root_spec#UUID=}" ;;
                        /dev/*) entry_root_uuid=$(blkid -s UUID -o value "$root_spec") ;;
                        LABEL=*|PARTUUID=*|PARTLABEL=*)
                            root_device=$(findfs "$root_spec")
                            entry_root_uuid=$(blkid -s UUID -o value "$root_device")
                            ;;
                        *) fail "Unsupported root argument in $entry: $arg" ;;
                    esac
                    [ "$entry_root_uuid" = "$root_uuid" ] ||
                        fail "Root argument in $entry does not identify the target filesystem"
                    ;;
                rw) fail "Conflicting root mount mode in $entry" ;;
            esac
        done
        [ "$root_count" -eq 1 ] || fail "Expected one root argument in $entry"
        for arg in "${required_args[@]}"; do
            [[ " ${option_args[*]} " == *" $arg "* ]] ||
                fail "Missing target boot argument in $entry: $arg"
        done
        validated_entries+=("$entry")
    done
done
grub_env=$(grub2-editenv - list)
saved_entry=$(awk -F= '$1 == "saved_entry" {print $2}' <<< "$grub_env")
[[ -n "$saved_entry" && "$saved_entry" != */* &&
   -s "/boot/loader/entries/${saved_entry}.conf" ]] ||
    fail "Saved default does not reference an installed BLS entry"
[[ " ${validated_entries[*]} " == *" /boot/loader/entries/${saved_entry}.conf "* ]] ||
    fail "Saved default does not reference a validated installed kernel"
if grep -q '^tmp_saved_entry=' <<< "$grub_env"; then
    fail "The saved default was not finalized by the distro hooks"
fi
awk '$1 == "options" {sub(/^options[ \t]+/, ""); print}' \
    "/boot/loader/entries/${saved_entry}.conf" > /etc/kernel/cmdline

# --- Security hardening ---
# Remove SSH host keys — sshd-keygen regenerates on first boot
rm -f /etc/ssh/ssh_host_*_key /etc/ssh/ssh_host_*_key.pub

# Reset machine-id — systemd regenerates on first boot
: > /etc/machine-id

# Disable root SSH login with password (key-based only)
sed -i 's/^#*PermitRootLogin.*/PermitRootLogin prohibit-password/' /etc/ssh/sshd_config 2>/dev/null || true

# Trigger SELinux relabel on first boot
touch /.autorelabel
