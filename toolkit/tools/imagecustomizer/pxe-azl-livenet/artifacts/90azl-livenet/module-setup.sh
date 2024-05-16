#!/bin/bash

# called by dracut
check() {
    return 0
}

# called by dracut
depends() {
    echo livenet
    return 0
}

# called by dracut
install() {
    inst_simple /etc/systemd/system/liveos-artifacts-download.service
    inst_script "$moddir/liveos-artifacts-download.sh" "/sbin/liveos-artifacts-download"
    inst_script "$moddir/schedule-liveos-artifacts-download.sh" "/sbin/schedule-liveos-artifacts-download"
    inst_hook pre-udev 30 "$moddir/azl-livenet-genrules.sh"
    # systemctl --root "$initdir" enable liveos-artifacts-download
    dracut_need_initqueue
}
