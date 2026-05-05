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
