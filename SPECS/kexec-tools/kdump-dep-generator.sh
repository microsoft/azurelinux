#!/bin/sh

# More details about systemd generator:
# http://www.freedesktop.org/wiki/Software/systemd/Generators/

. /usr/lib/kdump/kdump-lib.sh

# If invokded with no arguments for testing purpose, output to /tmp to
# avoid overriding the existing.
dest_dir="/tmp"

if [ -n "$1" ]; then
    dest_dir=$1
fi

systemd_dir=/usr/lib/systemd/system
kdump_wants=$dest_dir/kdump.service.wants

if is_ssh_dump_target; then
    mkdir -p $kdump_wants
    ln -sf $systemd_dir/network-online.target $kdump_wants/
fi
