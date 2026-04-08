#!/bin/bash
# -*- mode: shell-script; indent-tabs-mode: nil; sh-basic-offset: 4; -*-
# ex: ts=8 sw=4 sts=4 et filetype=sh

check() {
    return 255
}

depends() {
    return 0
}

install() {
    local _dir

    inst_libdir_file libfreeblpriv3.so libfreeblpriv3.chk \
        libfreebl3.so
}
