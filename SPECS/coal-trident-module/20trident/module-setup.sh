#!/bin/bash
# Portions Copyright (c) 2020 Microsoft Corporation


check() {
    # Only include if requested by the dracut configuration files
    require_binaries trident || return 1
    return 255
}

depends() {
    # Return 0 to include the dependent module(s) in the initramfs
    return 0
}

install() {
    inst "trident"
}