#!/bin/bash
# post-install.sh — Target system configuration (%post script for kickstart)
# Called from within the installed chroot during anaconda %post.
set -x

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
cat > /etc/default/grub << 'GRUBDEF'
GRUB_TIMEOUT=2
GRUB_DISTRIBUTOR="Azure Linux"
GRUB_DEFAULT=0
GRUB_DISABLE_SUBMENU=true
GRUB_TERMINAL_OUTPUT="console serial"
GRUB_SERIAL_COMMAND="serial --speed=115200 --unit=0 --word=8 --parity=no --stop=1"
GRUB_CMDLINE_LINUX="console=ttyS0,115200 console=tty0"
GRUB_DISABLE_RECOVERY=true
GRUBDEF

# --- BLS boot entry reconciliation ---
# anaconda's kernel install runs kernel-install, which names BootLoaderSpec
# entries <machine-id>-<kver>.conf using the machine-id present at install time.
# Because /etc/machine-id is reset below (regenerated on first boot), that prefix
# becomes stale, and any entry for a superseded kernel is left orphaned under a
# defunct machine-id (ADO #20509). Pin a stable entry-token, drop entries whose
# kernel is no longer installed, and rebase surviving machine-id-prefixed entries
# onto the token so entry names no longer depend on the volatile machine-id.
# Mirrors base/images/vm-base/config.sh. The grub menu kernel sort order is a
# separate grub2 blscfg concern and is not addressed here.
ENTRY_TOKEN="azurelinux"
BLS_DIR="/boot/loader/entries"
mkdir -p /etc/kernel
printf '%s\n' "${ENTRY_TOKEN}" > /etc/kernel/entry-token

if [ -d "${BLS_DIR}" ]; then
    # Collect the set of actually-installed kernel versions from real vmlinuz files.
    installed_kvers=()
    for vmlinuz in /boot/vmlinuz-*; do
        [ -e "${vmlinuz}" ] && installed_kvers+=("${vmlinuz#/boot/vmlinuz-}")
    done

    shopt -s nullglob
    for conf in "${BLS_DIR}"/*.conf; do
        base="$(basename "${conf}")"
        kver="$(awk '$1 == "version" { print $2; exit }' "${conf}")"

        # Drop entries for kernels that are no longer installed, but never prune
        # when the installed set is unknown/empty (avoid emptying the directory).
        if [ "${#installed_kvers[@]}" -gt 0 ] && [ -n "${kver}" ]; then
            installed=0
            for k in "${installed_kvers[@]}"; do
                [ "${k}" = "${kver}" ] && { installed=1; break; }
            done
            if [ "${installed}" -eq 0 ]; then
                echo "post-install: removing orphaned BLS entry ${base} (kernel ${kver} not installed)"
                rm -f "${conf}"
                continue
            fi
        fi

        # Rebase a machine-id-prefixed entry onto the stable entry-token.
        if [[ "${base}" =~ ^[0-9a-f]{32}-(.+)\.conf$ ]]; then
            dest="${BLS_DIR}/${ENTRY_TOKEN}-${BASH_REMATCH[1]}.conf"
            echo "post-install: rebasing BLS entry ${base} -> $(basename "${dest}")"
            mv -f "${conf}" "${dest}"
        fi
    done
    shopt -u nullglob
fi

# --- Encrypted disk: regenerate initramfs with LUKS support ---
if [ -f /etc/crypttab ] && [ -s /etc/crypttab ]; then
    echo "LUKS detected — regenerating initramfs with crypt module..."
    dracut --regenerate-all --force --add crypt
fi

# --- Security hardening ---
# Remove SSH host keys — sshd-keygen regenerates on first boot
rm -f /etc/ssh/ssh_host_*_key /etc/ssh/ssh_host_*_key.pub

# Reset machine-id — systemd regenerates on first boot
: > /etc/machine-id

# Disable root SSH login with password (key-based only)
sed -i 's/^#*PermitRootLogin.*/PermitRootLogin prohibit-password/' /etc/ssh/sshd_config 2>/dev/null || true

# Trigger SELinux relabel on first boot
touch /.autorelabel
