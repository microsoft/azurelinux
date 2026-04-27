#!/bin/bash
# KIWI config.sh — post-bootstrap configuration for Anaconda TUI Offline Installer ISO
set -euo pipefail

#----------------------------------------------------------------------
# Azure Linux product configuration for Anaconda
#----------------------------------------------------------------------

CONF_DIR="/etc/anaconda/conf.d"
mkdir -p "$CONF_DIR"

cat > "$CONF_DIR/azurelinux.conf" << 'PRODUCTEOF'
# Azure Linux 4.0 — Anaconda configuration overrides
# Loaded via conf.set_from_files() from /etc/anaconda/conf.d/

[Storage]
default_scheme = LVM
file_system_type = ext4

[Storage Constraints]
root_device_types = LVM PARTITION MD LVM_THINP
must_not_be_on_root = /boot /boot/efi
req_partition_sizes =
    /boot     1 GiB
    /boot/efi  600 MiB

[Network]
default_on_boot = DEFAULT_ROUTE_DEVICE

[Bootloader]
efi_dir = fedora

[User Interface]
hidden_spokes = NetworkSpoke

[License]
eula =
PRODUCTEOF

#----------------------------------------------------------------------
# Enable services needed by anaconda at ISO boot
#----------------------------------------------------------------------

systemctl enable dbus-broker.service 2>/dev/null || systemctl enable dbus.service 2>/dev/null || true
systemctl enable NetworkManager.service 2>/dev/null || true
systemctl enable systemd-networkd.service 2>/dev/null || true
systemctl enable systemd-resolved.service 2>/dev/null || true

#----------------------------------------------------------------------
# Architecture detection — set arch-specific package and EFI names
#----------------------------------------------------------------------
ARCH=$(uname -m)
case "$ARCH" in
    x86_64)
        GRUB_EFI_PKG="grub2-efi-x64"
        GRUB_EFI_MOD_PKG="grub2-efi-x64-modules"
        GRUB_EFI_CDBOOT_PKG="grub2-efi-x64-cdboot"
        SHIM_EFI="shimx64.efi"
        GRUB_EFI="grubx64.efi"
        BOOT_EFI="BOOTX64.EFI"
        ;;
    aarch64)
        GRUB_EFI_PKG="grub2-efi-aa64"
        GRUB_EFI_MOD_PKG="grub2-efi-aa64-modules"
        GRUB_EFI_CDBOOT_PKG="grub2-efi-aa64-cdboot"
        SHIM_EFI="shimaa64.efi"
        GRUB_EFI="grubaa64.efi"
        BOOT_EFI="BOOTAA64.EFI"
        ;;
    *)
        echo "ERROR: Unsupported architecture: $ARCH" >&2
        exit 1
        ;;
esac
echo "=== Architecture: $ARCH ==="
echo "  GRUB EFI package: $GRUB_EFI_PKG"
echo "  Shim EFI binary:  $SHIM_EFI"

#----------------------------------------------------------------------
# Download all target-install packages + deps for the offline repo
#----------------------------------------------------------------------
# During the ISO build we have network access to the repo.
# Download every package that anaconda will install on the target,
# including all transitive dependencies, into /opt/azl-offline-repo/.
# This lets the offline kickstart install from file:// with no network.

OFFLINE_REPO="/opt/azl-offline-repo"
mkdir -p "$OFFLINE_REPO"

# === Single source of truth for target-install packages ===
# These go into the kickstart %packages and the offline repo.
# Any package needed on the installed system belongs here.
INSTALL_PKGS=(
    bash
    coreutils
    systemd
    systemd-networkd
    systemd-resolved
    dnf5
    grub2
    "$GRUB_EFI_PKG"
    "$GRUB_EFI_MOD_PKG"
    shim
    efibootmgr
    kernel
    kernel-modules
    openssh-server
    openssh-clients
    sudo
    vim-minimal
    ca-certificates
    azurelinux-release
    setup
    shadow-utils
    util-linux
    selinux-policy-targeted
    audit
    chrony
    cracklib-dicts
    glibc
    glibc-langpack-en
    cryptsetup
    firewalld
    iproute
)

# Extra packages needed in the offline repo for anaconda's runtime deps
# but not listed in kickstart %packages (pulled via --resolve --alldeps).
EXTRA_REPO_PKGS=(
    "$GRUB_EFI_CDBOOT_PKG"
    lvm2
    e2fsprogs
    dosfstools
    device-mapper-persistent-data
    fonts-filesystem
    default-fonts-core-sans
    google-noto-fonts-common
    google-noto-sans-vf-fonts
    google-noto-sans-mono-vf-fonts
    google-noto-serif-vf-fonts
    abattis-cantarell-vf-fonts
    liberation-sans-fonts
    liberation-mono-fonts
    liberation-serif-fonts
    langpacks-en
    langpacks-core-en
    langpacks-fonts-en
    hunspell
    hunspell-en
    hunspell-en-US
    hunspell-en-GB
    hunspell-filesystem
    harfbuzz
    freetype
    graphite2
    libpng
    mtools
    grub2-tools-extra
    libaio
)

echo "=== Downloading target-install packages + dependencies ==="
dnf download \
    --resolve \
    --alldeps \
    --destdir="$OFFLINE_REPO" \
    "${INSTALL_PKGS[@]}" "${EXTRA_REPO_PKGS[@]}" || {
    echo "WARNING: dnf download had errors — some packages may be missing"
}

RPM_COUNT=$(ls "$OFFLINE_REPO"/*.rpm 2>/dev/null | wc -l)
echo "=== Downloaded $RPM_COUNT RPMs ==="
ls "$OFFLINE_REPO"/*.rpm 2>/dev/null | head -20 || true
echo "..."

# Build repo metadata
createrepo_c "$OFFLINE_REPO"

#----------------------------------------------------------------------
# Validate offline repo completeness (dry-run install)
#----------------------------------------------------------------------
echo "=== Validating offline repo completeness ==="

DRYRUN_ROOT=$(mktemp -d /tmp/azl-dryrun-XXXXXX)
DRYRUN_ERRORS=$(dnf install \
    --assumeno \
    --installroot="$DRYRUN_ROOT" \
    --releasever=4.0 \
    --setopt=reposdir=/dev/null \
    --repofrompath=offline,"file://$OFFLINE_REPO" \
    --repo=offline \
    "${INSTALL_PKGS[@]}" 2>&1) || true

rm -rf "$DRYRUN_ROOT"

if echo "$DRYRUN_ERRORS" | grep -qiE "No match for argument|nothing provides|cannot install"; then
    echo "!!!"
    echo "!!! FATAL: Offline repo is missing packages required by the kickstart!"
    echo "!!!"
    echo "$DRYRUN_ERRORS" | grep -iE "No match for argument|nothing provides|cannot install"
    echo ""
    echo "Fix: add the missing packages to INSTALL_PKGS."
    exit 1
else
    echo "=== Dry-run passed — all kickstart packages resolve from offline repo ==="
fi

echo "=== Offline repo ready at $OFFLINE_REPO ==="

#----------------------------------------------------------------------
# Anaconda launcher script
#----------------------------------------------------------------------

cat > /usr/local/bin/anaconda-launcher.sh << 'LAUNCHEOF'
#!/bin/bash
mkdir -p /run/install

# Clean up stale PID file from any previous run
rm -f /run/user/0/anaconda.pid

# Disable all system repos so anaconda only uses the offline repo.
# This prevents silent network fetches even when a NIC is present.
for repo_file in /etc/yum.repos.d/*.repo; do
    [ -f "$repo_file" ] && sed -i -E 's/^enabled\s*=\s*.*/enabled=0/' "$repo_file"
done

# Check kernel cmdline for custom kickstart (inst.ks=<url>)
CUSTOM_KS=""
if grep -qo 'inst\.ks=[^ ]*' /proc/cmdline 2>/dev/null; then
    CUSTOM_KS=$(grep -o 'inst\.ks=[^ ]*' /proc/cmdline | sed 's/inst\.ks=//')
    echo ""
    echo "========================================"
    echo "  Azure Linux 4.0 Offline Installer"
    echo "========================================"
    echo ""
    echo "  Custom kickstart detected: $CUSTOM_KS"
    echo "  Launching anaconda with custom kickstart..."
    echo ""
    /usr/sbin/anaconda --text --kickstart="$CUSTOM_KS"
    RC=$?
    rm -f /run/install/ks.cfg
    if [ $RC -eq 0 ]; then
        echo "Installation complete."
        echo "Press Enter to reboot..."
        read -r
        systemctl reboot
    else
        echo "Anaconda exited with code $RC. Dropping to shell."
        exec /bin/bash
    fi
    exit 0
fi

echo ""
echo "========================================"
echo "  Azure Linux 4.0 Offline Installer"
echo "========================================"
echo ""
echo "  1) Standard installation"
echo "  2) Encrypted disk (LUKS)"
echo ""
read -rp "Select installation type [1]: " CHOICE

case "$CHOICE" in
    2)
        echo "*** Disk encryption ENABLED ***"
        echo "  Anaconda will prompt you for the LUKS passphrase during install."
        echo ""
        cp /root/azl-install-encrypted.ks /run/install/ks.cfg
        ;;
    *)
        echo "*** Standard installation (offline) ***"
        cp /root/azl-install.ks /run/install/ks.cfg
        ;;
esac

echo "=== Kickstart storage config ==="
grep -E 'autopart|clearpart|part |volgroup|logvol|--encrypted' /run/install/ks.cfg
echo "==============================="
echo ""
/usr/sbin/anaconda --text --kickstart=/run/install/ks.cfg
RC=$?

rm -f /run/install/ks.cfg

if [ $RC -eq 0 ]; then
    echo ""
    echo "Installation complete."
    echo ""
    echo "=== Bootloader log (from %post --nochroot) ==="
    for mnt in /mnt/sysroot /mnt/sysimage; do
        [ -f "$mnt/var/log/anaconda-bootloader.log" ] && {
            tail -60 "$mnt/var/log/anaconda-bootloader.log"
            break
        }
    done
    echo ""
    echo "Ejecting installation media..."
    eject /dev/sr0 2>/dev/null || eject /dev/cdrom 2>/dev/null || true
    echo "Press Enter to reboot into the installed system..."
    read -r
    systemctl reboot
else
    echo ""
    echo "======================================================"
    echo " Anaconda exited with code $RC."
    echo " You are now in the live ISO shell."
    echo " Run 'anaconda --text' to retry, or investigate logs."
    echo " Logs: /tmp/anaconda.log, /tmp/packaging.log"
    echo "======================================================"
    exec /bin/bash
fi
LAUNCHEOF
chmod +x /usr/local/bin/anaconda-launcher.sh
ln -sf /usr/local/bin/anaconda-launcher.sh /usr/local/bin/install-azl

#----------------------------------------------------------------------
# Welcome banner
#----------------------------------------------------------------------

cat > /root/.bash_profile << 'PROFILEEOF'
# Auto-install mode: if "azl.autoinstall" is on the kernel cmdline
# (selected via the "Install Azure Linux 4.0" GRUB entry), launch
# the installer automatically.
#
# Console selection logic:
#   - Hyper-V (systemd-detect-virt = "microsoft") → user is on VGA (tty1)
#   - QEMU/KVM/bare-metal with serial in cmdline  → user is on serial (ttyS0)
#   - QEMU/KVM/bare-metal without serial          → user is on VGA (tty1)
# This prevents the invisible tty1 from stealing the installer on QEMU -nographic.
if grep -q 'azl\.autoinstall' /proc/cmdline 2>/dev/null; then
    MY_TTY=$(tty 2>/dev/null)
    VIRT=$(systemd-detect-virt 2>/dev/null)
    LAUNCH=false
    if [ "$VIRT" = "microsoft" ]; then
        # Hyper-V: user interacts via VGA console
        [ "$MY_TTY" = "/dev/tty1" ] && LAUNCH=true
    else
        # QEMU/KVM/bare-metal
        case "$MY_TTY" in
            /dev/ttyS0)
                LAUNCH=true
                ;;
            /dev/tty1|/dev/hvc0)
                # Only autoinstall on VGA if serial is NOT in kernel cmdline
                # (otherwise ttyS0 will handle it)
                if ! grep -q 'console=ttyS' /proc/cmdline 2>/dev/null; then
                    LAUNCH=true
                fi
                ;;
        esac
    fi
    if [ "$LAUNCH" = true ]; then
        echo ""
        echo "========================================"
        echo "  Azure Linux 4.0 — Offline Installer"
        echo "========================================"
        echo ""
        echo "  Starting installer automatically..."
        echo ""
        exec /usr/local/bin/anaconda-launcher.sh
    fi
fi
echo ""
echo "========================================"
echo "  Azure Linux 4.0 — Offline Installer"
echo "========================================"
echo ""
echo "  To start the installer, run:"
echo ""
echo "    install-azl"
echo ""
echo "========================================"
echo ""
PROFILEEOF

cat > /root/.bashrc << 'RCEOF'
if [[ $- == *i* ]] && [ ! -f /tmp/.azl-banner-shown ]; then
    touch /tmp/.azl-banner-shown
    source /root/.bash_profile
fi
RCEOF

#----------------------------------------------------------------------
# Autologin on serial and VGA consoles
#----------------------------------------------------------------------

mkdir -p /etc/systemd/system/serial-getty@ttyS0.service.d
cat > /etc/systemd/system/serial-getty@ttyS0.service.d/autologin.conf << 'AUTOEOF'
[Service]
ExecStart=
ExecStart=-/sbin/agetty --autologin root --noclear %I 115200 linux
AUTOEOF

mkdir -p /etc/systemd/system/getty@tty1.service.d
cat > /etc/systemd/system/getty@tty1.service.d/autologin.conf << 'AUTOEOF'
[Service]
ExecStart=
ExecStart=-/sbin/agetty --autologin root --noclear %I linux
AUTOEOF

#----------------------------------------------------------------------
# Embedded kickstart — OFFLINE: all packages from local ISO repo
#----------------------------------------------------------------------

# Helper: generate %packages section from INSTALL_PKGS array.
# Replaces arch-specific variables with their actual package names.
generate_packages_section() {
    echo "# Packages — minimal Azure Linux system"
    echo "# --nocore: AZL repo has no comps groups, so @core would fail"
    echo "%packages --nocore"
    for pkg in "${INSTALL_PKGS[@]}"; do
        echo "$pkg"
    done
    echo "%end"
}

cat > /root/azl-install.ks << 'KSEOF'
# Azure Linux 4.0 — Anaconda Kickstart (Offline)

# Installation source — local repo bundled on the ISO
repo --name=azl-offline --baseurl=file:///opt/azl-offline-repo/

# Disable any system repos so only the offline repo is used
# (handled by disabling .repo files before anaconda starts)

# System settings
lang en_US.UTF-8
keyboard us
timezone UTC --utc
selinux --enforcing
firewall --enabled --ssh
network --hostname=azurelinux
services --enabled=sshd,systemd-networkd,systemd-resolved

# Bootloader
bootloader --location=mbr --append="console=ttyS0,115200 console=tty0"

# Eject installation media and reboot automatically after install
reboot --eject

# Disk layout — LVM without encryption
clearpart --all --initlabel
part /boot/efi --fstype=efi --size=600
part /boot --fstype=ext4 --size=1024
part pv.01 --size=1 --grow
volgroup vg_azl pv.01
logvol swap --vgname=vg_azl --name=lv_swap --fstype=swap --size=512
logvol / --vgname=vg_azl --name=lv_root --fstype=ext4 --size=1 --grow

KSEOF

# Append generated %packages section
generate_packages_section >> /root/azl-install.ks

cat >> /root/azl-install.ks << 'KSEOF'

%post --log=/var/log/anaconda-post.log
set -x

# Enable networking
systemctl enable systemd-networkd
systemctl enable systemd-resolved
systemctl enable sshd

cat > /etc/systemd/network/20-wired-dhcp.network << 'NET'
[Match]
Name=en* eth*

[Network]
DHCP=yes

[DHCPv4]
UseDNS=yes
NET

# Write /etc/default/grub for grub2-mkconfig
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

# --- Security hardening for the installed target ---
# Remove SSH host keys — sshd-keygen regenerates unique keys on first boot
rm -f /etc/ssh/ssh_host_*_key /etc/ssh/ssh_host_*_key.pub

# Reset machine-id — systemd regenerates on first boot
: > /etc/machine-id

# Disable root SSH login with password (key-based only)
sed -i 's/^#*PermitRootLogin.*/PermitRootLogin prohibit-password/' /etc/ssh/sshd_config 2>/dev/null || true

# Trigger SELinux relabel on first boot
touch /.autorelabel
%end

# ===================================================================
# UEFI Bootloader setup — runs in the installer environment (NOT chrooted)
# ===================================================================
%post --nochroot --log=/mnt/sysroot/var/log/anaconda-bootloader.log
set -x
SYSROOT=/mnt/sysroot

echo "=== Target mounts ==="
findmnt -R "$SYSROOT" 2>/dev/null || mount | grep sysroot

echo "=== fstab ==="
cat "$SYSROOT/etc/fstab" 2>/dev/null

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
for d in "$SYSROOT/boot/efi/EFI/fedora" "$SYSROOT/boot/efi/EFI/azurelinux"; do
    [ -d "$d" ] && { EFI_VENDOR="$d"; break; }
done
[ -z "$EFI_VENDOR" ] && { EFI_VENDOR="$SYSROOT/boot/efi/EFI/fedora"; mkdir -p "$EFI_VENDOR"; }
echo "EFI vendor dir: $EFI_VENDOR"
ls -la "$EFI_VENDOR/" 2>/dev/null

# --- Generate /boot/grub2/grub.cfg manually ---
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
    for bootnum in $(efibootmgr 2>/dev/null | grep -i 'default\\\|anaconda\|fedora' | sed 's/Boot\([0-9A-Fa-f]*\).*/\1/'); do
        echo "Removing stale entry Boot$bootnum"
        efibootmgr -b "$bootnum" -B 2>/dev/null || true
    done

    efibootmgr -c -d "$ESP_DISK" -p "$ESP_PART" \
        -L "Azure Linux" -l "\\EFI\\fedora\\$SHIM_EFI" 2>/dev/null && \
        echo "Created UEFI boot entry: Azure Linux -> \\EFI\\fedora\\$SHIM_EFI" || \
        echo "WARNING: efibootmgr -c failed"

    echo "=== Updated UEFI boot entries ==="
    efibootmgr 2>/dev/null
else
    echo "WARNING: Could not find ESP mount — skipping NVRAM fix"
fi
%end
KSEOF

# --- Encrypted variant kickstart (offline) ---
cat > /root/azl-install-encrypted.ks << 'KSENCEOF'
# Azure Linux 4.0 — Anaconda Kickstart (Offline, Encrypted)

# Installation source — local repo bundled on the ISO
repo --name=azl-offline --baseurl=file:///opt/azl-offline-repo/

# Disable any system repos so only the offline repo is used
# (handled by disabling .repo files before anaconda starts)

# System settings
lang en_US.UTF-8
keyboard us
timezone UTC --utc
selinux --enforcing
firewall --enabled --ssh
network --hostname=azurelinux
services --enabled=sshd,systemd-networkd,systemd-resolved

# Bootloader
bootloader --location=mbr --append="console=ttyS0,115200 console=tty0"

# Eject installation media and reboot automatically after install
reboot --eject

# Disk layout — LUKS-encrypted LVM via autopart
# No --passphrase here: anaconda will prompt the user interactively.
clearpart --all --initlabel
autopart --type=lvm --encrypted

KSENCEOF

# Append generated %packages section
generate_packages_section >> /root/azl-install-encrypted.ks

cat >> /root/azl-install-encrypted.ks << 'KSENCEOF'

%post --log=/var/log/anaconda-post.log
set -x
systemctl enable systemd-networkd
systemctl enable systemd-resolved
systemctl enable sshd

cat > /etc/systemd/network/20-wired-dhcp.network << 'NET'
[Match]
Name=en* eth*

[Network]
DHCP=yes

[DHCPv4]
UseDNS=yes
NET

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

# Regenerate initramfs with LUKS/crypt support
if [ -f /etc/crypttab ] && [ -s /etc/crypttab ]; then
    echo "LUKS detected — regenerating initramfs with crypt module..."
    dracut --regenerate-all --force --add crypt
fi

# --- Security hardening for the installed target ---
rm -f /etc/ssh/ssh_host_*_key /etc/ssh/ssh_host_*_key.pub
: > /etc/machine-id
sed -i 's/^#*PermitRootLogin.*/PermitRootLogin prohibit-password/' /etc/ssh/sshd_config 2>/dev/null || true

# Trigger SELinux relabel on first boot
touch /.autorelabel
%end

%post --nochroot --log=/mnt/sysroot/var/log/anaconda-bootloader.log
set -x
SYSROOT=/mnt/sysroot

echo "=== fstab ==="
cat "$SYSROOT/etc/fstab" 2>/dev/null
echo "=== crypttab ==="
cat "$SYSROOT/etc/crypttab" 2>/dev/null

BOOT_DEV=$(findmnt -n -o SOURCE "$SYSROOT/boot" 2>/dev/null)
BOOT_UUID=$(blkid -s UUID -o value "$BOOT_DEV" 2>/dev/null)
ROOT_DEV=$(findmnt -n -o SOURCE "$SYSROOT" 2>/dev/null)
ROOT_UUID=$(blkid -s UUID -o value "$ROOT_DEV" 2>/dev/null)

echo "Boot: dev=$BOOT_DEV uuid=$BOOT_UUID"
echo "Root: dev=$ROOT_DEV uuid=$ROOT_UUID"

if [ -z "$BOOT_UUID" ]; then
    BOOT_UUID=$(awk '$2 == "/boot" { sub(/^UUID=/, "", $1); print $1 }' "$SYSROOT/etc/fstab" 2>/dev/null)
fi
if [ -z "$ROOT_UUID" ]; then
    ROOT_UUID=$(awk '$2 == "/" { sub(/^UUID=/, "", $1); print $1 }' "$SYSROOT/etc/fstab" 2>/dev/null)
fi

KERNEL=$(ls "$SYSROOT"/boot/vmlinuz-* 2>/dev/null | sort -V | tail -1)
INITRD=$(ls "$SYSROOT"/boot/initramfs-*.img 2>/dev/null | sort -V | tail -1)
KERNEL_NAME=$(basename "$KERNEL")
INITRD_NAME=$(basename "$INITRD")

if [ -z "$BOOT_UUID" ] || [ -z "$ROOT_UUID" ] || [ -z "$KERNEL_NAME" ] || [ -z "$INITRD_NAME" ]; then
    echo "!!! FATAL: Missing UUID or kernel — bootloader setup skipped"
    blkid 2>/dev/null
    exit 0
fi

LUKS_PARAMS=""
for luks_dev in $(blkid -t TYPE=crypto_LUKS -o device 2>/dev/null); do
    LUKS_UUID=$(cryptsetup luksUUID "$luks_dev" 2>/dev/null) && {
        LUKS_PARAMS="rd.luks.uuid=luks-${LUKS_UUID}"
        echo "Detected LUKS: $luks_dev UUID=$LUKS_UUID"
        break
    }
done

EFI_VENDOR=""
for d in "$SYSROOT/boot/efi/EFI/fedora" "$SYSROOT/boot/efi/EFI/azurelinux"; do
    [ -d "$d" ] && { EFI_VENDOR="$d"; break; }
done
[ -z "$EFI_VENDOR" ] && { EFI_VENDOR="$SYSROOT/boot/efi/EFI/fedora"; mkdir -p "$EFI_VENDOR"; }

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

mkdir -p "$SYSROOT/boot/efi/EFI/BOOT"
if [ -f "$EFI_VENDOR/$SHIM_EFI" ]; then
    cp -vf "$EFI_VENDOR/$SHIM_EFI"   "$SYSROOT/boot/efi/EFI/BOOT/$BOOT_EFI"
    cp -vf "$EFI_VENDOR/$GRUB_EFI"   "$SYSROOT/boot/efi/EFI/BOOT/$GRUB_EFI"   2>/dev/null || true
    cp -vf "$EFI_VENDOR/grub.cfg"    "$SYSROOT/boot/efi/EFI/BOOT/grub.cfg"     2>/dev/null || true
elif [ -f "$EFI_VENDOR/$GRUB_EFI" ]; then
    cp -vf "$EFI_VENDOR/$GRUB_EFI"   "$SYSROOT/boot/efi/EFI/BOOT/$BOOT_EFI"
    cp -vf "$EFI_VENDOR/grub.cfg"    "$SYSROOT/boot/efi/EFI/BOOT/grub.cfg"     2>/dev/null || true
fi

echo "=== Final ESP ==="
ls -laR "$SYSROOT/boot/efi/" 2>/dev/null

# --- Fix UEFI NVRAM boot entry ---
ESP_DEV=$(findmnt -n -o SOURCE "$SYSROOT/boot/efi" 2>/dev/null)
if [ -n "$ESP_DEV" ]; then
    ESP_DISK=$(echo "$ESP_DEV" | sed 's/[0-9]*$//')
    ESP_PART=$(echo "$ESP_DEV" | grep -o '[0-9]*$')
    echo "ESP: dev=$ESP_DEV disk=$ESP_DISK part=$ESP_PART"

    echo "=== Current UEFI boot entries ==="
    efibootmgr 2>/dev/null
    for bootnum in $(efibootmgr 2>/dev/null | grep -i 'default\\\|anaconda\|fedora' | sed 's/Boot\([0-9A-Fa-f]*\).*/\1/'); do
        echo "Removing stale entry Boot$bootnum"
        efibootmgr -b "$bootnum" -B 2>/dev/null || true
    done

    efibootmgr -c -d "$ESP_DISK" -p "$ESP_PART" \
        -L "Azure Linux" -l "\\EFI\\fedora\\$SHIM_EFI" 2>/dev/null && \
        echo "Created UEFI boot entry: Azure Linux" || \
        echo "WARNING: efibootmgr -c failed"

    echo "=== Updated UEFI boot entries ==="
    efibootmgr 2>/dev/null
else
    echo "WARNING: Could not find ESP mount — skipping NVRAM fix"
fi
%end
KSENCEOF

#----------------------------------------------------------------------
# Serial console getty
#----------------------------------------------------------------------
systemctl enable serial-getty@ttyS0.service 2>/dev/null || true
