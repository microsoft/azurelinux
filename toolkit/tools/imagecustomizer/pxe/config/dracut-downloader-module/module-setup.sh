#!/bin/bash

# called by dracut
check() {
    return 0
}

# called by dracut
depends() {
    return 0
}

# called by dracut
install() {
    inst_multiple grep cut ip
    inst_hook pre-pivot 90 "$moddir/download-artifacts.sh"
}
