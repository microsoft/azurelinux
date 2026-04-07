#!/bin/bash
set -eou pipefail

if [ -n "$(grep fedora-iot /sysroot/ostree/repo/config)" ] && [ -f "/etc/ostree/remotes.d/fedora-iot.conf" ]; then
        echo "Detected fedora-iot remote conflict, removing remote in /sysroot."
        rm /etc/ostree/remotes.d/fedora-iot.conf
        ostree remote delete fedora-iot --if-exists
        cp /usr/etc/ostree/remotes.d/fedora-iot.conf /etc/ostree/remotes.d/fedora-iot.conf
fi

touch /var/lib/fedora-iot-config-remote-fix.stamp
