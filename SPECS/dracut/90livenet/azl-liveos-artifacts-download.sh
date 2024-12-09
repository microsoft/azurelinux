#!/bin/bash

# Dracut version 102 does not implement the code path that handles livenet
# rootfs download (i.e. by calling /sbin/livenetroot) when systemd-networkd
# is the underlying networking manager.
#
# This has been implemented in 103 (see https://github.com/dracut-ng/dracut-ng/pull/388)
#
# As a mitigation for 102, this script will be scheduled to be run after the
# network stack is up and will basically call into the same livenet rootfs
# handling code.

echo "executing azl-liveos-artifacts-download.sh" > /dev/kmsg

. /usr/lib/dracut-lib.sh
. /lib/url-lib.sh

root=$(getarg root -d "")

# set dracut environment
export fstype="auto"
export DRACUT_SYSTEMD=1

# replace 'live:' with 'livetnet' so that livenetroot can detect it correctly.
isoUrl="${root#live:}"
netroot="livenet:"${isoUrl}

# Looking at livenetroot.sh, the first argument is unused in livenetroot.
# So, we are just providing a placehold here to preserve the order.
/sbin/livenetroot dummy $netroot
