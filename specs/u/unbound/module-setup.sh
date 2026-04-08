#!/usr/bin/bash

check() {
    require_binaries unbound unbound-checkconf unbound-control || return 1
    # the module will be only included if explicitly required either
    # by configuration or another module
    return 255
}

depends() {
    # because of pid file we need sysusers to create unbound user
    echo systemd systemd-sysusers
    return 0
}

install() {
    # We have to make unbound wanted by network-online target to make sure
    # there is a synchronization point when other services are able
    # to make queries
    inst_simple "$moddir"/unbound-initrd.conf /etc/systemd/system/unbound.service.d/unbound-initrd.conf

    # /etc and /var/lib do not have its variables
    inst_multiple -o \
    "$systemdsystemunitdir"/unbound.service \
    /etc/unbound/conf.d/remote-control.conf \
    /etc/unbound/openssl-sha1.conf \
    /usr/share/unbound/fedora-defaults.conf \
    /usr/share/unbound/conf.d/*.conf \
    /etc/unbound/local.d/*.conf \
    /etc/unbound/keys.d/*.key \
    /etc/unbound/unbound.conf \
    /etc/unbound/unbound_control.key \
    /etc/unbound/unbound_control.pem \
    /etc/unbound/unbound_server.key \
    /etc/unbound/unbound_server.pem \
    "$sysusers"/unbound.conf \
    "$tmpfilesdir"/unbound.conf \
    /var/lib/unbound/root.key \
    unbound \
    unbound-checkconf \
    unbound-control

    $SYSTEMCTL -q --root "$initdir" enable unbound.service
}
