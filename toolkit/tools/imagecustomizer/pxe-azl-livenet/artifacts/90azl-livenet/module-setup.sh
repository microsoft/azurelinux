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
    # todo: consider using: inst_script
    inst_simple /usr/local/bin/liveos-artifacts-download.sh
    inst_simple /usr/local/bin/schedule-liveos-artifacts-download.sh
    inst_hook pre-udev 30 "$moddir/azl-livenet-genrules.sh"
    # systemctl --root "$initdir" enable liveos-artifacts-download
    dracut_need_initqueue
}
