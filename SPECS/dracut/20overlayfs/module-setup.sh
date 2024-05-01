#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

check() {
    return 0
}

depends() {
    echo base
}

# Install Overlay driver.
installkernel() {
    instmods overlay
}

install() {
    inst_hook cmdline 20 "$moddir/overlayfs-parse.sh"
    inst_hook pre-pivot 10 "$moddir/overlayfs-mount.sh"
    dracut_need_initqueue
}
