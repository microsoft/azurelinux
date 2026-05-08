#!/bin/bash
# KIWI config.sh — post-bootstrap configuration for Anaconda TUI Offline Installer ISO
set -euo pipefail

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
    azurelinux-repos-dev
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
    mtools
    grub2-tools-extra
    libaio
)

echo "=== Downloading target-install packages + dependencies ==="
# Kiwi removes repo configs after package installation, so repos from the .kiwi
# file are NOT available during config.sh. Use --repofrompath with the CDN URL
# directly. The URL matches the "azurelinux-base" repo in vm-iso-installer.kiwi.

AZL_BASE_URL="https://stcontroltowerdevjwisitg.blob.core.windows.net/azl4-dev/base/$ARCH"
dnf5 download \
    --setopt=reposdir=/dev/null \
    --repofrompath=azl-base,"$AZL_BASE_URL" \
    --repo=azl-base \
    --resolve \
    --alldeps \
    --skip-unavailable \
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
DRYRUN_ERRORS=$(dnf5 install \
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
# Anaconda launcher symlink (script deployed via kiwi <file>)
#----------------------------------------------------------------------
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
# Generate kickstart files from templates (deployed via kiwi <file>)
#----------------------------------------------------------------------

# Helper: generate %packages section from INSTALL_PKGS array.
generate_packages_section() {
    echo "# Packages — minimal Azure Linux system"
    echo "# --nocore: AZL repo has no comps groups, so @core would fail"
    echo "%packages --nocore"
    for pkg in "${INSTALL_PKGS[@]}"; do
        echo "$pkg"
    done
    echo "%end"
}

# Expand @@PACKAGES@@ placeholder in each template
for ks_in in /root/azl-install.ks.in /root/azl-install-encrypted.ks.in; do
    ks_out="${ks_in%.in}"
    {
        sed '/@@PACKAGES@@/,$d' "$ks_in"
        generate_packages_section
        sed '1,/@@PACKAGES@@/d' "$ks_in"
    } > "$ks_out"
    rm -f "$ks_in"
done
