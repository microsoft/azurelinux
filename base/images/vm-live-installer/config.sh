#!/bin/bash
# KIWI config.sh — runs inside the image chroot during build.
# Installs the azl-install script for install-to-disk from live session.

set -e

# Install the azl-install script (embedded inline)
install -m 0755 /dev/stdin /usr/local/bin/azl-install << 'INSTALLER_EOF'
#!/bin/bash
# azl-install — Install Azure Linux from the live session to a target disk.
# Supports both interactive and unattended modes.
#
# Interactive:
#   sudo azl-install
#
# Unattended (command-line):
#   sudo azl-install --disk vda --root-password secret \
#       [--user admin --user-password secret] [--encrypt --luks-passphrase secret] \
#       [--yes] [--reboot]
#
# Unattended (config file):
#   sudo azl-install --config /path/to/azl-install.conf
#
# Config file format (shell variables):
#   AZL_DISK=vda
#   AZL_ROOT_PASSWORD=secret
#   AZL_USER=admin
#   AZL_USER_PASSWORD=secret
#   AZL_ENCRYPT=yes
#   AZL_LUKS_PASSPHRASE=secret
#   AZL_CONFIRM=yes
#   AZL_REBOOT=yes
#   AZL_HOSTNAME=azurelinux

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m'

INSTALL_ROOT="/mnt/azl-install"

# Cleanup on failure: unmount and close LUKS devices
cleanup() {
    local rc=$?
    if [ $rc -ne 0 ]; then
        echo ""
        error "Installation failed (exit $rc). Cleaning up..."
    fi
    umount -l "$INSTALL_ROOT/run" 2>/dev/null || true
    umount -l "$INSTALL_ROOT/proc" 2>/dev/null || true
    umount -l "$INSTALL_ROOT/sys" 2>/dev/null || true
    umount -l "$INSTALL_ROOT/dev" 2>/dev/null || true
    umount -l "$INSTALL_ROOT/boot/efi" 2>/dev/null || true
    umount -l "$INSTALL_ROOT/boot" 2>/dev/null || true
    umount -l "$INSTALL_ROOT" 2>/dev/null || true
    cryptsetup luksClose luks-root 2>/dev/null || true
    cryptsetup luksClose luks-swap 2>/dev/null || true
}
trap cleanup EXIT

info()  { echo -e "${GREEN}>>>${NC} $*"; }
warn()  { echo -e "${YELLOW}WARNING:${NC} $*"; }
error() { echo -e "${RED}ERROR:${NC} $*" >&2; }
fatal() { error "$@"; exit 1; }

usage() {
    cat << EOF
Usage: azl-install [OPTIONS]

Install Azure Linux from the live session to a target disk.

Options:
  --disk DEVICE          Target disk (e.g., vda, sda, nvme0n1)
  --root-password PASS   Set root password
  --user USERNAME        Create additional user with sudo access
  --user-password PASS   Password for the additional user
  --encrypt              Enable LUKS encryption on root and swap partitions
  --luks-passphrase PASS LUKS passphrase (required with --encrypt in unattended mode)
  --hostname NAME        Set system hostname (default: azurelinux)
  --config FILE          Read settings from config file
  --yes                  Skip confirmation prompt
  --reboot               Reboot after installation
  -h, --help             Show this help

Interactive mode (no arguments):
  sudo azl-install

Unattended mode:
  sudo azl-install --disk vda --root-password secret --yes

Config file mode:
  sudo azl-install --config /path/to/azl-install.conf
EOF
    exit 0
}

# --- Defaults ---
AZL_DISK=""
AZL_ROOT_PASSWORD=""
AZL_USER=""
AZL_USER_PASSWORD=""
AZL_HOSTNAME="azurelinux"
AZL_ENCRYPT=""
AZL_LUKS_PASSPHRASE=""
AZL_CONFIRM=""
AZL_REBOOT=""
INTERACTIVE=true

# --- Parse arguments ---
while [[ $# -gt 0 ]]; do
    case "$1" in
        --disk)         AZL_DISK="$2"; INTERACTIVE=false; shift 2 ;;
        --root-password) AZL_ROOT_PASSWORD="$2"; shift 2 ;;
        --user)         AZL_USER="$2"; shift 2 ;;
        --user-password) AZL_USER_PASSWORD="$2"; shift 2 ;;
        --encrypt)      AZL_ENCRYPT="yes"; shift ;;
        --luks-passphrase) AZL_LUKS_PASSPHRASE="$2"; shift 2 ;;
        --hostname)     AZL_HOSTNAME="$2"; shift 2 ;;
        --config)
            if [ ! -f "$2" ]; then
                fatal "Config file not found: $2"
            fi
            # Source config file (shell variables)
            . "$2"
            INTERACTIVE=false
            shift 2
            ;;
        --yes)          AZL_CONFIRM="yes"; shift ;;
        --reboot)       AZL_REBOOT="yes"; shift ;;
        -h|--help)      usage ;;
        *)              fatal "Unknown option: $1. Use --help for usage." ;;
    esac
done

# Validate unattended mode has required arguments
if [ "$INTERACTIVE" = false ]; then
    [ -z "$AZL_DISK" ] && fatal "--disk is required for unattended mode"
    [ -z "$AZL_ROOT_PASSWORD" ] && fatal "--root-password is required for unattended mode"
    if [ -n "$AZL_USER" ] && [ -z "$AZL_USER_PASSWORD" ]; then
        fatal "--user-password is required when --user is specified"
    fi
    if [ "$AZL_ENCRYPT" = "yes" ] && [ -z "$AZL_LUKS_PASSPHRASE" ]; then
        fatal "--luks-passphrase is required when --encrypt is specified in unattended mode"
    fi
fi

if [ "$(id -u)" -ne 0 ]; then
    fatal "Must run as root. Use: sudo azl-install"
fi

echo ""
echo -e "${BOLD}=============================================${NC}"
echo -e "${BOLD}  Azure Linux 4.0 — Disk Installer${NC}"
echo -e "${BOLD}=============================================${NC}"
echo ""

# --- Select target disk ---
if [ "$INTERACTIVE" = true ]; then
    info "Available disks:"
    echo ""
    lsblk -d -o NAME,SIZE,MODEL,TYPE | grep -E "disk|TYPE"
    echo ""
    while true; do
        read -rp "Enter target disk (e.g., sda, vda, nvme0n1): " DISK_INPUT
        TARGET="/dev/${DISK_INPUT}"
        if [ -b "$TARGET" ]; then
            break
        fi
        error "'$TARGET' is not a valid block device."
    done
else
    TARGET="/dev/${AZL_DISK}"
    if [ ! -b "$TARGET" ]; then
        fatal "'$TARGET' is not a valid block device."
    fi
    info "Target disk: $TARGET"
fi

# --- Confirm ---
if [ "$INTERACTIVE" = true ]; then
    echo ""
    warn "This will ERASE ALL DATA on ${TARGET}!"
    lsblk "$TARGET"
    echo ""
    read -rp "Type 'yes' to continue: " CONFIRM
    if [ "$CONFIRM" != "yes" ]; then
        echo "Aborted."
        exit 0
    fi
elif [ "$AZL_CONFIRM" != "yes" ]; then
    warn "This will ERASE ALL DATA on ${TARGET}!"
    lsblk "$TARGET"
    echo ""
    read -rp "Type 'yes' to continue: " CONFIRM
    if [ "$CONFIRM" != "yes" ]; then
        echo "Aborted."
        exit 0
    fi
else
    info "Unattended mode — skipping confirmation."
fi

# --- Encryption prompt (interactive) ---
if [ "$INTERACTIVE" = true ] && [ "$AZL_ENCRYPT" != "yes" ]; then
    echo ""
    read -rp "Enable disk encryption (LUKS)? (y/n): " ENCRYPT_CHOICE
    if [ "$ENCRYPT_CHOICE" = "y" ] || [ "$ENCRYPT_CHOICE" = "Y" ]; then
        AZL_ENCRYPT="yes"
    fi
fi

if [ "$AZL_ENCRYPT" = "yes" ] && [ -z "$AZL_LUKS_PASSPHRASE" ]; then
    echo ""
    echo "Set the LUKS disk encryption passphrase:"
    while true; do
        read -srp "Passphrase: " LUKS_PW
        echo
        read -srp "Retype passphrase: " LUKS_PW2
        echo
        if [ -z "$LUKS_PW" ]; then
            echo "Passphrase cannot be empty."
            continue
        fi
        if [ "$LUKS_PW" != "$LUKS_PW2" ]; then
            echo "Passphrases do not match. Try again."
            continue
        fi
        AZL_LUKS_PASSPHRASE="$LUKS_PW"
        LUKS_PW=""
        LUKS_PW2=""
        break
    done
fi

# --- Check minimum disk size ---
DISK_SIZE_MB=$(( $(blockdev --getsize64 "$TARGET") / 1048576 ))
if [ "$AZL_ENCRYPT" = "yes" ]; then
    MIN_SIZE_MB=3072  # 200M EFI + 512M boot + 512M swap + ~1.8G root
else
    MIN_SIZE_MB=2048  # 200M EFI + 512M swap + ~1.3G root
fi
if [ "$DISK_SIZE_MB" -lt "$MIN_SIZE_MB" ]; then
    fatal "Disk ${TARGET} is too small (${DISK_SIZE_MB} MB). Minimum required: ${MIN_SIZE_MB} MB."
fi

# --- Partition disk ---
# Encrypted:     EFI(200M) + /boot(512M) + swap(512M) + root(rest)
# Non-encrypted: EFI(200M) + swap(512M) + root(rest)
PART_PREFIX="${TARGET}"
if [[ "$TARGET" == *nvme* ]] || [[ "$TARGET" == *mmcblk* ]]; then
    PART_PREFIX="${TARGET}p"
fi

info "Partitioning ${TARGET}..."
wipefs -af "$TARGET"
parted -s "$TARGET" mklabel gpt

if [ "$AZL_ENCRYPT" = "yes" ]; then
    parted -s "$TARGET" mkpart "EFI"  fat32       1MiB    201MiB
    parted -s "$TARGET" set 1 esp on
    parted -s "$TARGET" mkpart "boot" ext4      201MiB    713MiB
    parted -s "$TARGET" mkpart "swap" linux-swap 713MiB   1225MiB
    parted -s "$TARGET" mkpart "root" ext4      1225MiB   100%

    EFI_PART="${PART_PREFIX}1"
    BOOT_PART="${PART_PREFIX}2"
    SWAP_PART="${PART_PREFIX}3"
    ROOT_PART="${PART_PREFIX}4"
else
    parted -s "$TARGET" mkpart "EFI"  fat32       1MiB    201MiB
    parted -s "$TARGET" set 1 esp on
    parted -s "$TARGET" mkpart "swap" linux-swap 201MiB   713MiB
    parted -s "$TARGET" mkpart "root" ext4       713MiB   100%

    EFI_PART="${PART_PREFIX}1"
    BOOT_PART=""
    SWAP_PART="${PART_PREFIX}2"
    ROOT_PART="${PART_PREFIX}3"
fi

sleep 2
partprobe "$TARGET"
sleep 1

info "Formatting partitions..."
mkfs.vfat -F 32 -n EFI "$EFI_PART"

if [ -n "$BOOT_PART" ]; then
    mkfs.ext4 -L boot -F "$BOOT_PART"
fi

LUKS_ROOT_NAME="luks-root"
LUKS_SWAP_NAME="luks-swap"

if [ "$AZL_ENCRYPT" = "yes" ]; then
    info "Setting up LUKS encryption on root partition..."
    printf '%s' "$AZL_LUKS_PASSPHRASE" | cryptsetup luksFormat --batch-mode "$ROOT_PART" --key-file=-
    printf '%s' "$AZL_LUKS_PASSPHRASE" | cryptsetup luksOpen "$ROOT_PART" "$LUKS_ROOT_NAME" --key-file=-
    ROOT_DEV="/dev/mapper/$LUKS_ROOT_NAME"

    info "Setting up LUKS encryption on swap partition..."
    printf '%s' "$AZL_LUKS_PASSPHRASE" | cryptsetup luksFormat --batch-mode "$SWAP_PART" --key-file=-
    printf '%s' "$AZL_LUKS_PASSPHRASE" | cryptsetup luksOpen "$SWAP_PART" "$LUKS_SWAP_NAME" --key-file=-
    SWAP_DEV="/dev/mapper/$LUKS_SWAP_NAME"

    mkswap -L swap "$SWAP_DEV"
    mkfs.ext4 -L root -F "$ROOT_DEV"
else
    ROOT_DEV="$ROOT_PART"
    SWAP_DEV="$SWAP_PART"
    mkswap -L swap "$SWAP_DEV"
    mkfs.ext4 -L root -F "$ROOT_DEV"
fi
# Clear passphrase from memory
AZL_LUKS_PASSPHRASE=""

mkdir -p "$INSTALL_ROOT"
mount "$ROOT_DEV" "$INSTALL_ROOT"
mkdir -p "$INSTALL_ROOT/boot"
if [ -n "$BOOT_PART" ]; then
    mount "$BOOT_PART" "$INSTALL_ROOT/boot"
fi
mkdir -p "$INSTALL_ROOT/boot/efi"
mount "$EFI_PART" "$INSTALL_ROOT/boot/efi"

# --- Copy filesystem ---
info "Copying live filesystem to disk (this may take a few minutes)..."
rsync -aAXH --info=progress2 \
    --exclude='/proc/*' \
    --exclude='/sys/*' \
    --exclude='/dev/*' \
    --exclude='/run/*' \
    --exclude='/tmp/*' \
    --exclude='/mnt/*' \
    --exclude='/media/*' \
    --exclude='/lost+found' \
    --exclude='/isofrom' \
    --exclude='/read-only' \
    --exclude='/boot/efi' \
    / "$INSTALL_ROOT/"

# Copy EFI partition contents without xattrs (FAT32 does not support them)
rsync -rltDH --info=progress2 \
    /boot/efi/ "$INSTALL_ROOT/boot/efi/"

mkdir -p "$INSTALL_ROOT"/{proc,sys,dev,run,tmp,mnt,media}

# --- Generate fstab ---
info "Generating fstab..."
ROOT_UUID=$(blkid -s UUID -o value "$ROOT_DEV")
EFI_UUID=$(blkid -s UUID -o value "$EFI_PART")
SWAP_UUID=$(blkid -s UUID -o value "$SWAP_DEV")

if [ "$AZL_ENCRYPT" = "yes" ]; then
    ROOT_PART_UUID=$(blkid -s UUID -o value "$ROOT_PART")
    SWAP_PART_UUID=$(blkid -s UUID -o value "$SWAP_PART")
    BOOT_UUID=$(blkid -s UUID -o value "$BOOT_PART")

    cat > "$INSTALL_ROOT/etc/fstab" << FSTAB_EOF
# /etc/fstab — generated by azl-install
/dev/mapper/$LUKS_ROOT_NAME  /          ext4  defaults  1 1
UUID=${BOOT_UUID}            /boot      ext4  defaults  1 2
UUID=${EFI_UUID}             /boot/efi  vfat  umask=0077  0 2
/dev/mapper/$LUKS_SWAP_NAME  swap       swap  defaults  0 0
FSTAB_EOF

    # --- Generate crypttab ---
    info "Generating crypttab..."
    cat > "$INSTALL_ROOT/etc/crypttab" << CRYPTTAB_EOF
# /etc/crypttab — generated by azl-install
$LUKS_ROOT_NAME  UUID=${ROOT_PART_UUID}  none  luks
$LUKS_SWAP_NAME  UUID=${SWAP_PART_UUID}  none  luks
CRYPTTAB_EOF
else
    cat > "$INSTALL_ROOT/etc/fstab" << FSTAB_EOF
# /etc/fstab — generated by azl-install
UUID=${ROOT_UUID}  /          ext4  defaults  1 1
UUID=${EFI_UUID}   /boot/efi  vfat  umask=0077  0 2
UUID=${SWAP_UUID}  swap       swap  defaults  0 0
FSTAB_EOF
fi

# --- Set hostname ---
echo "$AZL_HOSTNAME" > "$INSTALL_ROOT/etc/hostname"

# --- Install GRUB bootloader ---
info "Installing GRUB bootloader..."
mount --bind /dev  "$INSTALL_ROOT/dev"
mount --bind /proc "$INSTALL_ROOT/proc"
mount --bind /sys  "$INSTALL_ROOT/sys"
mount --bind /run  "$INSTALL_ROOT/run"

FEDORA_EFI="$INSTALL_ROOT/boot/efi/EFI/fedora"
BOOT_EFI="$INSTALL_ROOT/boot/efi/EFI/BOOT"

# Build kernel cmdline based on encryption
KCMD="console=ttyS0,115200 console=tty0"
if [ "$AZL_ENCRYPT" = "yes" ]; then
    KCMD="rd.luks.uuid=$ROOT_PART_UUID rd.luks.name=${ROOT_PART_UUID}=${LUKS_ROOT_NAME} rd.luks.uuid=$SWAP_PART_UUID rd.luks.name=${SWAP_PART_UUID}=${LUKS_SWAP_NAME} $KCMD"
    # GRUB searches for the separate /boot partition (unencrypted)
    GRUB_SEARCH_UUID="$BOOT_UUID"
    GRUB_BOOT_PREFIX=""
    GRUB_ROOT_PARAM="/dev/mapper/$LUKS_ROOT_NAME"
else
    # /boot lives inside root — GRUB uses root UUID and /boot prefix
    GRUB_SEARCH_UUID="$ROOT_UUID"
    GRUB_BOOT_PREFIX="/boot"
    GRUB_ROOT_PARAM="UUID=${ROOT_UUID}"
fi

for d in "$FEDORA_EFI" "$BOOT_EFI"; do
    [ -d "$d" ] || mkdir -p "$d"
    cat > "$d/grub.cfg" << GRUBSHIM_EOF
search --no-floppy --fs-uuid --set=dev ${GRUB_SEARCH_UUID}
set prefix=(\$dev)${GRUB_BOOT_PREFIX}/grub2
export \$prefix
configfile \$prefix/grub.cfg
GRUBSHIM_EOF
done

if [ ! -f "$BOOT_EFI/BOOTX64.EFI" ]; then
    [ -f "$FEDORA_EFI/shimx64.efi" ] && cp "$FEDORA_EFI/shimx64.efi" "$BOOT_EFI/BOOTX64.EFI"
fi
if [ ! -f "$BOOT_EFI/grubx64.efi" ]; then
    [ -f "$FEDORA_EFI/grubx64.efi" ] && cp "$FEDORA_EFI/grubx64.efi" "$BOOT_EFI/grubx64.efi"
fi

cat > "$INSTALL_ROOT/etc/default/grub" << GRUBDEF_EOF
GRUB_TIMEOUT=5
GRUB_DISTRIBUTOR="Azure Linux"
GRUB_DEFAULT=saved
GRUB_DISABLE_SUBMENU=true
GRUB_TERMINAL="console serial"
GRUB_SERIAL_COMMAND="serial --speed=115200 --unit=0 --word=8 --parity=no --stop=1"
GRUB_CMDLINE_LINUX="${KCMD}"
GRUB_DISABLE_RECOVERY=true
GRUBDEF_EOF

KERNEL_VER=$(ls "$INSTALL_ROOT/boot/vmlinuz-"* 2>/dev/null | head -1 | sed "s|.*/vmlinuz-||")
if [ -z "$KERNEL_VER" ]; then
    warn "No kernel found in /boot — grub.cfg will be empty!"
fi

cat > "$INSTALL_ROOT/boot/grub2/grub.cfg" << GRUBCFG_EOF
# grub.cfg — generated by azl-install
set pager=1
set timeout=5

serial --speed=115200 --unit=0 --word=8 --parity=no --stop=1
terminal_input console serial
terminal_output console serial

menuentry 'Azure Linux 4.0 ($KERNEL_VER)' --class azurelinux --class gnu-linux --class gnu --class os {
    search --no-floppy --fs-uuid --set=root ${GRUB_SEARCH_UUID}
    linux ${GRUB_BOOT_PREFIX}/vmlinuz-${KERNEL_VER} root=${GRUB_ROOT_PARAM} ro ${KCMD}
    initrd ${GRUB_BOOT_PREFIX}/initramfs-${KERNEL_VER}.img
}

menuentry 'UEFI Firmware Settings' --id 'uefi-firmware' {
    fwsetup
}
GRUBCFG_EOF

# Create a proper UEFI NVRAM boot entry for Azure Linux
EFI_DISK="$TARGET"
EFI_PARTNUM=$(echo "$EFI_PART" | grep -o '[0-9]*$')
chroot "$INSTALL_ROOT" efibootmgr -c -d "$EFI_DISK" -p "$EFI_PARTNUM" \
    -L "Azure Linux" -l "\\EFI\\fedora\\shimx64.efi" 2>/dev/null || true

chroot "$INSTALL_ROOT" rpm -e dracut-kiwi-live 2>/dev/null || true

# Rebuild initramfs with crypt module for LUKS support
if [ "$AZL_ENCRYPT" = "yes" ]; then
    info "Rebuilding initramfs with LUKS support..."
    chroot "$INSTALL_ROOT" dracut --force --add "crypt dm" \
        "/boot/initramfs-${KERNEL_VER}.img" "$KERNEL_VER"
fi

# Remove live session artifacts from installed system
rm -f "$INSTALL_ROOT/usr/local/bin/azl-install" "$INSTALL_ROOT/usr/local/sbin/azl-install"
: > "$INSTALL_ROOT/etc/motd"

# --- Helper: set password by writing hash directly to /etc/shadow ---
set_password() {
    local SHADOW_FILE="$INSTALL_ROOT/etc/shadow"
    local USERNAME="$1"
    local PASSWORD="$2"
    local HASH
    HASH=$(openssl passwd -6 "$PASSWORD")
    sed -i "s|^${USERNAME}:[^:]*:|${USERNAME}:${HASH}:|" "$SHADOW_FILE"
}

# --- Helper: create user directly on target filesystem ---
create_user() {
    local USERNAME="$1"
    if grep -q "^${USERNAME}:" "$INSTALL_ROOT/etc/passwd"; then
        warn "User '$USERNAME' already exists — skipping creation."
        return 0
    fi
    local NEXT_UID
    NEXT_UID=$(awk -F: '{if($3>=1000 && $3>max)max=$3}END{print (max==""?1000:max+1)}' "$INSTALL_ROOT/etc/passwd")
    echo "$USERNAME:x:$NEXT_UID:$NEXT_UID::/home/$USERNAME:/bin/bash" >> "$INSTALL_ROOT/etc/passwd"
    echo "$USERNAME:!:19821:0:99999:7:::" >> "$INSTALL_ROOT/etc/shadow"
    echo "$USERNAME:x:$NEXT_UID:" >> "$INSTALL_ROOT/etc/group"
    # Add to wheel group
    if grep -q "^wheel:.*:$" "$INSTALL_ROOT/etc/group"; then
        sed -i "s/^wheel:\([^:]*:[^:]*:\)$/wheel:\1$USERNAME/" "$INSTALL_ROOT/etc/group"
    else
        sed -i "s/^wheel:\([^:]*:[^:]*:.*\)/wheel:\1,$USERNAME/" "$INSTALL_ROOT/etc/group"
    fi
    # Create home directory
    mkdir -p "$INSTALL_ROOT/home/$USERNAME"
    cp -a "$INSTALL_ROOT/etc/skel/." "$INSTALL_ROOT/home/$USERNAME/" 2>/dev/null || true
    chown -R "$NEXT_UID:$NEXT_UID" "$INSTALL_ROOT/home/$USERNAME"
}

# --- Set up accounts ---
echo ""
echo -e "${BOLD}----------------------------------------------${NC}"
echo -e "${BOLD}  Set up user account${NC}"
echo -e "${BOLD}----------------------------------------------${NC}"
echo ""

if [ "$INTERACTIVE" = true ]; then
    # Interactive: prompt for root password
    echo "Set the root password for the installed system:"
    while true; do
        read -srp "New password: " ROOT_PW
        echo
        read -srp "Retype new password: " ROOT_PW2
        echo
        if [ -z "$ROOT_PW" ]; then
            echo "Password cannot be empty."
            continue
        fi
        if [ "$ROOT_PW" != "$ROOT_PW2" ]; then
            echo "Passwords do not match. Try again."
            continue
        fi
        set_password root "$ROOT_PW" && break
        echo "Failed to set password. Try again."
    done
    ROOT_PW=""
    ROOT_PW2=""

    # Interactive: prompt for user creation
    echo ""
    read -rp "Create an additional user? (y/n): " CREATE_USER
    if [ "$CREATE_USER" = "y" ] || [ "$CREATE_USER" = "Y" ]; then
        while true; do
            read -rp "Enter username: " NEW_USER
            if [ -z "$NEW_USER" ]; then
                echo "Username cannot be empty."
                continue
            fi
            break
        done
        create_user "$NEW_USER"
        echo "Set password for '$NEW_USER':"
        while true; do
            read -srp "New password: " USER_PW
            echo
            read -srp "Retype new password: " USER_PW2
            echo
            if [ -z "$USER_PW" ]; then
                echo "Password cannot be empty."
                continue
            fi
            if [ "$USER_PW" != "$USER_PW2" ]; then
                echo "Passwords do not match. Try again."
                continue
            fi
            set_password "$NEW_USER" "$USER_PW" && break
            echo "Failed to set password. Try again."
        done
        USER_PW=""
        USER_PW2=""
        info "User '$NEW_USER' created with sudo access."
    fi
else
    # Unattended: set root password
    info "Setting root password..."
    set_password root "$AZL_ROOT_PASSWORD"

    # Unattended: create user if specified
    if [ -n "$AZL_USER" ]; then
        info "Creating user '$AZL_USER'..."
        create_user "$AZL_USER"
        set_password "$AZL_USER" "$AZL_USER_PASSWORD"
        info "User '$AZL_USER' created with sudo access."
    fi
fi

# --- Enable services ---
chroot "$INSTALL_ROOT" systemctl enable sshd.service 2>/dev/null || true
chroot "$INSTALL_ROOT" systemctl enable systemd-networkd.service 2>/dev/null || true
chroot "$INSTALL_ROOT" systemctl enable systemd-resolved.service 2>/dev/null || true

# Trigger SELinux relabel on first boot
touch "$INSTALL_ROOT/.autorelabel"

# Cleanup is handled by the EXIT trap — just disarm set -e for final messages
set +e

echo ""
echo -e "${GREEN}=============================================${NC}"
echo -e "${GREEN}  Installation complete!${NC}"
echo -e "${GREEN}=============================================${NC}"
echo ""

if [ "$AZL_REBOOT" = "yes" ]; then
    info "Rebooting in 5 seconds..."
    sleep 5
    reboot
else
    echo "Remove the ISO/USB media and reboot to start Azure Linux."
    echo "  reboot"
    echo ""
fi
INSTALLER_EOF

# Add a login banner mentioning the installer
cat >> /etc/motd << 'MOTD_EOF'

============================================
  Azure Linux 4.0 — Live Session
============================================
  Interactive install:
    sudo azl-install

  Unattended install:
    sudo azl-install --disk vda \
      --root-password secret \
      --user admin --user-password secret \
      --yes --reboot

  Encrypted install:
    sudo azl-install --disk vda \
      --root-password secret --encrypt \
      --luks-passphrase secret --yes --reboot

  Config file install:
    sudo azl-install --config /path/to/conf
============================================

MOTD_EOF

