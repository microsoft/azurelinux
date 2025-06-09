#!/bin/bash

# called by dracut
check() {
    return 255
}

# called by dracut
depends() {
    return 0
}

# called by dracut
installkernel() {
    return 0
}

# called by dracut
install() {
    # install utilities
    inst_multiple lsblk umount
    # generate udev rule - i.e. schedule things post udev settlement
    inst_hook pre-udev 30 "$moddir/mountbootpartition-genrules.sh"
    # script to run post udev to mout
    inst_script "$moddir/mountbootpartition.sh" "/sbin/mountbootpartition"
    # script runs early on when systemd is initialized...
    if dracut_module_included "systemd-initrd"; then
        inst_script "$moddir/mountbootpartition-generator.sh" "$systemdutildir"/system-generators/dracut-mountbootpartition-generator
    fi
    dracut_need_initqueue
}
