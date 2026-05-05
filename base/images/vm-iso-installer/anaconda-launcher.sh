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
