#!/bin/bash

check() {
    return 0
}

depends() {
    echo base
}

installkernel() {
    instmods overlay
}

install() {
    inst_hook pre-pivot 10 "$moddir/overlayfs-mount.sh"
}
