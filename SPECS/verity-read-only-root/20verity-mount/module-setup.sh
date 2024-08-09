#!/bin/bash
# Portions Copyright (c) 2020 Microsoft Corporation

# See verity-parse.sh for documentation.

check() {
    # Only include if requested by the dracut configuration files
    require_binaries veritysetup || return 1
    return 255
}

depends() {
    echo systemd dm
}

# Omit cmdline() since it does not make sense to auto populate the cmdline.
# The initramfs needs to be modified out of band after the fact anyways
# with updated hashes.

install() {
    inst "veritysetup"
    inst "grep"
    inst_hook cmdline 20 "$moddir/verity-parse.sh"
    inst_hook pre-mount 10 "$moddir/verity-mount.sh"
    dracut_need_initqueue
}