#!/bin/bash

check() {
    return 0
}

depends() {
    return 0
}

install() {
    inst_hook pre-mount 99 "$moddir/overlays-mount.sh"
    dracut_need_initqueue
}
