#!/bin/bash

# called by dracut
check() {
    # a live host-only image doesn't really make a lot of sense
    [[ $hostonly ]] && return 1
    return 255
}

# called by dracut
depends() {
    # if dmsetup is not installed, then we cannot support fedora/red hat
    # style live images
    echo dm rootfs-block img-lib bash
    return 0
}

# called by dracut
installkernel() {
    instmods squashfs loop iso9660 overlay
}

# called by dracut
install() {
    echo "------ dmsquash - module-setup.sh ----- 1 packing tools"
    inst_multiple umount dmsetup blkid lsblk dd losetup blockdev find
    inst_multiple -o checkisomd5
    echo "------ dmsquash - module-setup.sh ----- 2 creating hooks..."
    inst_hook cmdline 30 "$moddir/parse-dmsquash-live.sh"
    inst_hook cmdline 31 "$moddir/parse-iso-scan.sh"
    inst_hook pre-udev 30 "$moddir/dmsquash-live-genrules.sh"
    inst_hook pre-udev 30 "$moddir/dmsquash-liveiso-genrules.sh"
    inst_hook pre-pivot 20 "$moddir/apply-live-updates.sh"
    echo "------ dmsquash - module-setup.sh ----- 3 installing scripts..."
    inst_script "$moddir/dmsquash-live-root.sh" "/sbin/dmsquash-live-root"
    inst_script "$moddir/iso-scan.sh" "/sbin/iso-scan"
    inst_script "$moddir/dmsquash-generator.sh" "$systemdutildir"/system-generators/dracut-dmsquash-generator
    echo "------ dmsquash - module-setup.sh ----- 4 installing rules..."
    # should probably just be generally included
    inst_rules 60-cdrom_id.rules
    echo "------ dmsquash - module-setup.sh ----- 5 installing 'simple'..."
    inst_simple "$moddir/checkisomd5@.service" "/etc/systemd/system/checkisomd5@.service"
    echo "------ dmsquash - module-setup.sh ----- 9 dracut_need_initqueue"
    dracut_need_initqueue
}
